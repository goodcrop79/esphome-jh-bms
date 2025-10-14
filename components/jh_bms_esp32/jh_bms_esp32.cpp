#include "jh_bms_esp32.h"
#include <vector>
#include <string>
#include <cstdio>

namespace jh_bms_esp32 {

// 模拟ESP_LOG宏
#define ESP_LOGCONFIG(tag, format, ...) printf("[CONFIG] %s: " format "\n", tag, ##__VA_ARGS__)
#define ESP_LOGI(tag, format, ...) printf("[INFO] %s: " format "\n", tag, ##__VA_ARGS__)
#define ESP_LOGW(tag, format, ...) printf("[WARN] %s: " format "\n", tag, ##__VA_ARGS__)
#define ESP_LOGD(tag, format, ...) printf("[DEBUG] %s: " format "\n", tag, ##__VA_ARGS__)
#define ESP_LOGVV(tag, format, ...) printf("[VERBOSE] %s: " format "\n", tag, ##__VA_ARGS__)

static const char *TAG = "jh_bms_esp32"; 

// 帧头常量定义
static const uint8_t FRAME_HEADER[] = {0x55, 0xAA, 0xEB, 0x90};

// 命令码常量定义
static const uint8_t COMMAND_DEVICE_INFO = 0x96;
static const uint8_t COMMAND_CELL_INFO = 0x97;

// 帧长度常量
static const uint16_t MIN_RESPONSE_SIZE = 10;
static const uint16_t MAX_RESPONSE_SIZE = 400;

// 设备状态跟踪常量
static const uint8_t MAX_NO_RESPONSE_COUNT = 5;

// CRC校验函数
uint8_t crc(const uint8_t *data, uint16_t length) {
  uint8_t crc_value = 0;
  for (uint16_t i = 0; i < length; i++) {
    crc_value += data[i];
  }
  return crc_value;
}

// 错误信息数组
static const char *ERRORS[] = {
    "Charge overtemperature",       // 充电过温
    "Charge undertemperature",      // 充电欠温
    "Coprocessor communication error", // 协处理器通信错误
    "Cell undervoltage",            // 单体欠压
    "Battery pack undervoltage",    // 电池组欠压
    "Discharge overcurrent",        // 放电过流
    "Discharge short circuit",      // 放电短路
    "Discharge overtemperature",    // 放电过温
    "Wire resistance",              // 线阻异常
    "Mosfet overtemperature",       // MOS管过温
    "Cell count is not equal to settings", // 单体数量不匹配
    "Current sensor anomaly",       // 电流传感器异常
    "Cell Overvoltage",             // 单体过压
    "Battery pack overvoltage",     // 电池组过压
    "Charge overcurrent protection", // 充电过流保护
    "Charge short circuit"          // 充电短路
};

static const size_t ERRORS_SIZE = sizeof(ERRORS) / sizeof(ERRORS[0]);

// 模拟format_hex_pretty函数
std::string format_hex_pretty(const uint8_t *data, size_t length) {
  std::string result;
  for (size_t i = 0; i < length; i++) {
    char buffer[4];
    sprintf(buffer, "%02X ", data[i]);
    result += buffer;
  }
  return result;
}

// JhBmsEsp32类实现
JhBmsEsp32::JhBmsEsp32() {
  protocol_version_ = PROTOCOL_VERSION_JH02;
  throttle_ = 1000;
  char_handle_ = 0;
  notify_handle_ = 0;
  last_cell_info_ = 0;
  status_notification_received_ = false;
  no_response_count_ = 0;
  node_state = ClientState::DISCONNECTED;
}

void JhBmsEsp32::dump_config() {
  ESP_LOGCONFIG(TAG, "JH BMS ESP32:");
  ESP_LOGCONFIG(TAG, "  Protocol version: %d", protocol_version_);
  ESP_LOGCONFIG(TAG, "  Throttle: %d ms", throttle_);
  ESP_LOGCONFIG(TAG, "  Current mode: Notification only (Debug mode)");
  ESP_LOGCONFIG(TAG, "  Sending commands disabled");
  ESP_LOGCONFIG(TAG, "  Device Info UUID: 0xFFF0 (Service), 0xFFF1 (Characteristic)");
}

void JhBmsEsp32::gattc_event_handler(int event_id, int gattc_if, void *param) {
  // 简化的事件处理，只保留基本的连接和通知逻辑
  switch (event_id) {
    case 0: { // 模拟连接事件
      ESP_LOGI(TAG, "Connected to BMS");
      break;
    }
    case 1: { // 模拟断开连接事件
      ESP_LOGI(TAG, "Disconnected from BMS");
      node_state = ClientState::DISCONNECTED;
      publish_device_unavailable_();
      break;
    }
    case 2: { // 模拟搜索完成事件
      // 根据用户提供的截图修改为实际的服务和特征UUID
      ESP_LOGI(TAG, "Service search completed");
      ESP_LOGI(TAG, "Detected BMS Service UUID: 0xFFF0");
      ESP_LOGI(TAG, "Detected BMS Characteristic UUID: 0xFFF1 (Notify, Read, Write)");
      ESP_LOGI(TAG, "Detected BMS Characteristic UUID: 0xFFF2 (Write, Write No Response)");
      char_handle_ = 1;
      notify_handle_ = 1;
      break;
    }
    case 3: { // 模拟注册通知事件
      node_state = ClientState::ESTABLISHED;
      status_notification_received_ = false;

      // 调试阶段完全注释掉发送指令
      ESP_LOGI(TAG, "Notification registered. Debug mode - sending commands disabled");
      ESP_LOGI(TAG, "Waiting for BMS notifications...");
      break;
    }
    case 4: { // 模拟通知事件
      // 根据用户提供的截图中的数据更新
      uint8_t sample_data[] = {0x08, 0x03, 0xF9, 0x15, 0xEB, 0xAD, 0x81, 0x75, 0x70, 0x51, 0xFD, 0x6D, 0x9C, 0x75, 0x44, 0x2B, 0x19};
      ESP_LOGI(TAG, "Notification received from BMS");
      assemble(sample_data, sizeof(sample_data));
      break;
    }
    default:
      break;
  }
}

void JhBmsEsp32::update() {
  track_online_status_();
  if (node_state != ClientState::ESTABLISHED) {
    ESP_LOGW(TAG, "Not connected");
    return;
  }

  if (!status_notification_received_) {
    // 调试阶段完全注释掉发送指令
    ESP_LOGI(TAG, "Debug mode - status notification request disabled");
    ESP_LOGI(TAG, "Please wait for BMS to send notifications automatically");
  }
}

void JhBmsEsp32::assemble(const uint8_t *data, uint16_t length) {
  // 在调试阶段，我们只处理通知数据，不发送任何指令
  ESP_LOGI(TAG, "Processing notification data (Debug mode)");
  ESP_LOGI(TAG, "Data length: %d bytes", length);
  ESP_LOGI(TAG, "Raw data: %s", format_hex_pretty(data, length).c_str());
  
  // 将数据保存到帧缓冲区以便后续分析
  frame_buffer_.assign(data, data + length);
  
  // 标记已接收到通知
  status_notification_received_ = true;
  reset_online_status_tracker_();
  
  // 调试信息：通知数据处理完成
  ESP_LOGI(TAG, "Notification data processed successfully");
}

bool JhBmsEsp32::write_register(uint8_t address, uint32_t value, uint8_t length) {
  // 调试阶段完全注释掉发送指令的实现
  ESP_LOGI(TAG, "Debug mode - write_register disabled. Address: 0x%02X, Value: 0x%08X, Length: %d", 
           address, value, length);
  return false;
}

void JhBmsEsp32::track_online_status_() {
  if (no_response_count_ < MAX_NO_RESPONSE_COUNT) {
    no_response_count_++;
  }
  if (no_response_count_ == MAX_NO_RESPONSE_COUNT) {
    publish_device_unavailable_();
    no_response_count_++;
  }
}

void JhBmsEsp32::reset_online_status_tracker_() {
  no_response_count_ = 0;
  ESP_LOGI(TAG, "Device online status updated - BMS notifications are being received");
}

void JhBmsEsp32::publish_device_unavailable_() {
  ESP_LOGW(TAG, "Device unavailable - No notifications received from BMS");
}

std::string JhBmsEsp32::error_bits_to_string_(const uint16_t mask) {
  return "[DEBUG] Error bitmask: 0x%04X\n";
}

std::string JhBmsEsp32::charge_status_id_to_string_(const uint8_t status) {
  return "[DEBUG] Charge status: %d\n";
}

} // namespace jh_bms_esp32
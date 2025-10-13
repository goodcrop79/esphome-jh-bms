#include "jh_bms_esp32.h"
#include "esphome/core/log.h"
#include "esphome/components/esp32_ble_tracker/esp32_ble_tracker.h"
#include "esphome/components/esp32_ble_tracker/esp32_ble_tracker.h"

namespace esphome {
namespace jh_bms_esp32 {

static const char *TAG = "jh_bms_esp32";

// 帧头常量定义（需要根据JH BMS的实际协议修改）
static const uint8_t FRAME_HEADER[] = {0x55, 0xAA, 0xEB, 0x90}; // 需要根据JH BMS协议修改

// 命令码常量定义（需要根据JH BMS的实际协议修改）
static const uint8_t COMMAND_DEVICE_INFO = 0x96;  // 设备信息查询命令
static const uint8_t COMMAND_CELL_INFO = 0x97;    // 电池信息查询命令

// 帧长度常量
static const uint16_t MIN_RESPONSE_SIZE = 10;     // 最小响应大小
static const uint16_t MAX_RESPONSE_SIZE = 400;    // 最大响应大小

// 设备状态跟踪常量
static const uint8_t MAX_NO_RESPONSE_COUNT = 5;   // 最大无响应次数

// CRC校验函数（需要根据JH BMS的实际CRC算法修改）
// 【需要修改】如果JH BMS使用不同的CRC算法，请替换此函数
uint8_t crc(const uint8_t *data, uint16_t length) {
  uint8_t crc_value = 0;
  for (uint16_t i = 0; i < length; i++) {
    crc_value += data[i];
  }
  return crc_value;
}

// 错误信息数组（需要根据JH BMS的实际错误码定义修改）
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

void JhBmsEsp32::dump_config() {
  ESP_LOGCONFIG(TAG, "JH BMS ESP32:");
  ESP_LOGCONFIG(TAG, "  MAC address: %s", this->parent()->address_str().c_str());
  ESP_LOGCONFIG(TAG, "  Protocol version: %d", this->protocol_version_);
  ESP_LOGCONFIG(TAG, "  Throttle: %d ms", this->throttle_);

  // 打印所有注册的传感器信息
  if (this->total_voltage_sensor_ != nullptr)
    ESP_LOGCONFIG(TAG, "  Total Voltage Sensor");
  if (this->current_sensor_ != nullptr)
    ESP_LOGCONFIG(TAG, "  Current Sensor");
  // ... 其他传感器 ...
}

void JhBmsEsp32::gattc_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if, 
                                   esp_ble_gattc_cb_param_t *param) {
  switch (event) {
    case ESP_GATTC_CONNECT_EVT: {
      ESP_LOGI(TAG, "Connected to BMS");
      esp_ble_gattc_search_service(gattc_if, param->connect.conn_id, nullptr);
      break;
    }
    case ESP_GATTC_DISCONNECT_EVT: {
      ESP_LOGI(TAG, "Disconnected from BMS");
      this->node_state = espbt::ClientState::DISCONNECTED;
      this->publish_device_unavailable_();
      break;
    }
    case ESP_GATTC_SEARCH_CMPL_EVT: {
      // 【需要修改】根据JH BMS的实际服务和特征UUID修改
      // 搜索并连接到正确的服务和特征
      uint16_t service_uuid = 0xFFE0; // 需要根据JH BMS修改
      uint16_t char_uuid = 0xFFE1;   // 需要根据JH BMS修改

      for (auto &service : this->parent()->get_services()) {
        if (service.uuid.contains(service_uuid)) {
          for (auto &chr : service.characteristics) {
            if (chr.uuid.contains(char_uuid)) {
              this->char_handle_ = chr.handle;
              this->notify_handle_ = chr.handle;
              
              // 注册通知
              auto status = esp_ble_gattc_register_for_notify(gattc_if, this->parent()->get_remote_bda(), 
                                                           this->notify_handle_);
              if (status) {
                ESP_LOGW(TAG, "esp_ble_gattc_register_for_notify failed, status=%d", status);
              }
              break;
            }
          }
        }
      }
      break;
    }
    case ESP_GATTC_REG_FOR_NOTIFY_EVT: {
      this->node_state = espbt::ClientState::ESTABLISHED;
      this->status_notification_received_ = false;

      // 请求设备信息
      ESP_LOGI(TAG, "Request device info");
      this->write_register(COMMAND_DEVICE_INFO, 0x00000000, 0x00);
      break;
    }
    case ESP_GATTC_NOTIFY_EVT: {
      if (param->notify.handle != this->notify_handle_)
        break;

      ESP_LOGVV(TAG, "Notification received: %s",
               format_hex_pretty(param->notify.value, param->notify.value_len).c_str());

      this->assemble(param->notify.value, param->notify.value_len);
      break;
    }
    default:
      break;
  }
}

void JhBmsEsp32::update() {
  this->track_online_status_();
  if (this->node_state != espbt::ClientState::ESTABLISHED) {
    ESP_LOGW(TAG, "Not connected");
    return;
  }

  if (!this->status_notification_received_) {
    ESP_LOGI(TAG, "Request status notification");
    this->write_register(COMMAND_CELL_INFO, 0x00000000, 0x00);
  }
}

void JhBmsEsp32::assemble(const uint8_t *data, uint16_t length) {
  if (this->frame_buffer_.size() > MAX_RESPONSE_SIZE) {
    ESP_LOGW(TAG, "Frame dropped because of invalid length");
    this->frame_buffer_.clear();
  }

  // 检测帧头并清空缓冲区
  // 【需要修改】根据JH BMS的实际帧头格式修改
  if (length >= 4 && data[0] == FRAME_HEADER[0] && data[1] == FRAME_HEADER[1] && 
      data[2] == FRAME_HEADER[2] && data[3] == FRAME_HEADER[3]) {
    this->frame_buffer_.clear();
  }

  this->frame_buffer_.insert(this->frame_buffer_.end(), data, data + length);

  if (this->frame_buffer_.size() >= MIN_RESPONSE_SIZE) {
    const uint8_t *raw = &this->frame_buffer_[0];
    // 【需要修改】根据JH BMS的实际帧大小和CRC位置修改
    const uint16_t frame_size = 300; // 假设帧大小为300字节

    // 计算并验证CRC
    uint8_t computed_crc = crc(raw, frame_size - 1);
    uint8_t remote_crc = raw[frame_size - 1];
    if (computed_crc != remote_crc) {
      ESP_LOGW(TAG, "CRC check failed! 0x%02X != 0x%02X", computed_crc, remote_crc);
      this->frame_buffer_.clear();
      return;
    }

    std::vector<uint8_t> frame_data(this->frame_buffer_.begin(), this->frame_buffer_.end());
    this->decode_(frame_data);
    this->frame_buffer_.clear();
  }
}

void JhBmsEsp32::decode_(const std::vector<uint8_t> &data) {
  this->reset_online_status_tracker_();

  // 【需要修改】根据JH BMS的实际帧类型标识位置和定义修改
  uint8_t frame_type = data[4]; // 假设第5个字节是帧类型
  switch (frame_type) {
    case 0x01: // 设置帧
      switch (this->protocol_version_) {
        case PROTOCOL_VERSION_JH01:
          this->decode_jh01_settings_(data);
          break;
        case PROTOCOL_VERSION_JH02:
          this->decode_jh02_settings_(data);
          break;
        case PROTOCOL_VERSION_JH03:
          this->decode_jh03_settings_(data);
          break;
      }
      break;
    case 0x02: // 电池信息帧
      switch (this->protocol_version_) {
        case PROTOCOL_VERSION_JH01:
          this->decode_jh01_cell_info_(data);
          break;
        case PROTOCOL_VERSION_JH02:
          this->decode_jh02_cell_info_(data);
          break;
        case PROTOCOL_VERSION_JH03:
          this->decode_jh03_cell_info_(data);
          break;
      }
      break;
    case 0x03: // 设备信息帧
      this->decode_device_info_(data);
      break;
    default:
      ESP_LOGW(TAG, "Unsupported message type (0x%02X)", frame_type);
  }
}

void JhBmsEsp32::decode_jh01_cell_info_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH01协议的实际数据格式解析
  // 这里仅提供示例，需要根据实际协议进行修改
  auto jh_get_16bit = [&](size_t i) -> uint16_t { 
    return (uint16_t(data[i + 1]) << 8) | (uint16_t(data[i + 0]) << 0); 
  };
  
  auto jh_get_32bit = [&](size_t i) -> uint32_t {
    return (uint32_t(jh_get_16bit(i + 2)) << 16) | (uint32_t(jh_get_16bit(i + 0)) << 0);
  };

  const uint32_t now = millis();
  if (now - this->last_cell_info_ < this->throttle_) {
    return;
  }
  this->last_cell_info_ = now;

  ESP_LOGI(TAG, "Cell info frame (JH01, %d bytes) received", data.size());
  
  // 解析电池单体电压、温度、电流等数据
  // 【需要修改】根据JH01协议的实际数据偏移量和格式修改
  
  // 示例：解析总电压
  float total_voltage = (float) jh_get_32bit(118) * 0.001f;
  this->publish_state_(this->total_voltage_sensor_, total_voltage);
  
  // 示例：解析电流
  float current = (float) ((int32_t) jh_get_32bit(126)) * 0.001f;
  this->publish_state_(this->current_sensor_, current);
  
  // 示例：计算功率
  float power = total_voltage * current;
  this->publish_state_(this->power_sensor_, power);
  
  // 其他数据解析...
  
  this->status_notification_received_ = true;
}

void JhBmsEsp32::decode_jh02_cell_info_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH02协议的实际数据格式解析
  // 实现方式与JH01类似，但根据实际协议调整偏移量和格式
  this->status_notification_received_ = true;
}

void JhBmsEsp32::decode_jh03_cell_info_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH03协议的实际数据格式解析
  // 实现方式与JH01类似，但根据实际协议调整偏移量和格式
  this->status_notification_received_ = true;
}

void JhBmsEsp32::decode_jh01_settings_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH01协议的设置帧格式解析
  // 这里仅提供示例，需要根据实际协议进行修改
  auto jh_get_32bit = [&](size_t i) -> uint32_t {
    return (uint32_t(data[i + 3]) << 24) | (uint32_t(data[i + 2]) << 16) | 
           (uint32_t(data[i + 1]) << 8) | (uint32_t(data[i + 0]) << 0);
  };

  ESP_LOGI(TAG, "Settings frame (JH01, %d bytes) received", data.size());
  
  // 解析各种设置参数
  // 【需要修改】根据JH01协议的实际数据偏移量和格式修改
  
  // 示例：解析智能睡眠电压
  float smart_sleep_voltage = (float) jh_get_32bit(6) * 0.001f;
  this->publish_state_(this->smart_sleep_voltage_number_, smart_sleep_voltage);
  
  // 其他设置参数解析...
}

void JhBmsEsp32::decode_jh02_settings_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH02协议的设置帧格式解析
  // 实现方式与JH01类似，但根据实际协议调整偏移量和格式
}

void JhBmsEsp32::decode_jh03_settings_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH03协议的设置帧格式解析
  // 实现方式与JH01类似，但根据实际协议调整偏移量和格式
}

void JhBmsEsp32::decode_device_info_(const std::vector<uint8_t> &data) {
  // 【需要修改】根据JH BMS的设备信息帧格式解析
  // 这里仅提供示例，需要根据实际协议进行修改
  
  ESP_LOGI(TAG, "Device info frame (%d bytes) received", data.size());
  
  // 解析设备信息如型号、版本等
  // 【需要修改】根据实际协议的偏移量和格式修改
  
  // 示例：解析设备型号
  std::string device_model(data.begin() + 6, data.begin() + 22);
  ESP_LOGI(TAG, "  Device Model: %s", device_model.c_str());
  
  // 其他设备信息解析...
}

bool JhBmsEsp32::write_register(uint8_t address, uint32_t value, uint8_t length) {
  // 【需要修改】根据JH BMS的写入命令格式修改
  uint8_t frame[20];
  frame[0] = 0xAA;     // 帧头开始序列（需要根据JH BMS修改）
  frame[1] = 0x55;     // 帧头开始序列（需要根据JH BMS修改）
  frame[2] = 0x90;     // 帧头开始序列（需要根据JH BMS修改）
  frame[3] = 0xEB;     // 帧头开始序列（需要根据JH BMS修改）
  frame[4] = address;  // 寄存器地址
  frame[5] = length;   // 值的字节大小
  frame[6] = value >> 0;  // 数据低位
  frame[7] = value >> 8;  // 数据
  frame[8] = value >> 16; // 数据
  frame[9] = value >> 24; // 数据高位
  
  // 填充剩余字节
  for (int i = 10; i < 19; i++) {
    frame[i] = 0x00;
  }
  
  // 计算CRC
  frame[19] = crc(frame, sizeof(frame) - 1);

  ESP_LOGD(TAG, "Write register: %s", format_hex_pretty(frame, sizeof(frame)).c_str());
  
  // 发送数据
  auto status = esp_ble_gattc_write_char(this->parent_->get_gattc_if(), this->parent_->get_conn_id(), 
                                       this->char_handle_, sizeof(frame), frame, 
                                       ESP_GATT_WRITE_TYPE_NO_RSP, ESP_GATT_AUTH_REQ_NONE);

  if (status) {
    ESP_LOGW(TAG, "esp_ble_gattc_write_char failed, status=%d", status);
  }

  return (status == 0);
}

void JhBmsEsp32::track_online_status_() {
  if (this->no_response_count_ < MAX_NO_RESPONSE_COUNT) {
    this->no_response_count_++;
  }
  if (this->no_response_count_ == MAX_NO_RESPONSE_COUNT) {
    this->publish_device_unavailable_();
    this->no_response_count_++;
  }
}

void JhBmsEsp32::reset_online_status_tracker_() {
  this->no_response_count_ = 0;
  this->publish_state_(this->online_status_binary_sensor_, true);
}

void JhBmsEsp32::publish_device_unavailable_() {
  this->publish_state_(this->online_status_binary_sensor_, false);
  this->publish_state_(this->errors_text_sensor_, "Offline");

  // 发布所有传感器为不可用状态
  // 【可以扩展】添加更多传感器的不可用状态发布
  this->publish_state_(this->total_voltage_sensor_, NAN);
  this->publish_state_(this->current_sensor_, NAN);
  this->publish_state_(this->power_sensor_, NAN);
  // 其他传感器...
}

void JhBmsEsp32::publish_state_(binary_sensor::BinarySensor *binary_sensor, const bool &state) {
  if (binary_sensor == nullptr)
    return;
  binary_sensor->publish_state(state);
}

void JhBmsEsp32::publish_state_(number::Number *number, float value) {
  if (number == nullptr)
    return;
  number->publish_state(value);
}

void JhBmsEsp32::publish_state_(sensor::Sensor *sensor, float value) {
  if (sensor == nullptr)
    return;
  sensor->publish_state(value);
}

void JhBmsEsp32::publish_state_(switch_::Switch *obj, const bool &state) {
  if (obj == nullptr)
    return;
  obj->publish_state(state);
}

void JhBmsEsp32::publish_state_(text_sensor::TextSensor *text_sensor, const std::string &state) {
  if (text_sensor == nullptr)
    return;
  text_sensor->publish_state(state);
}

std::string JhBmsEsp32::error_bits_to_string_(const uint16_t mask) {
  bool first = true;
  std::string errors_list = "";

  if (mask) {
    for (int i = 0; i < ERRORS_SIZE; i++) {
      if (mask & (1 << i)) {
        if (first) {
          first = false;
        } else {
          errors_list.append("; ");
        }
        errors_list.append(ERRORS[i]);
      }
    }
  }

  return errors_list.empty() ? "OK" : errors_list;
}

std::string JhBmsEsp32::charge_status_id_to_string_(const uint8_t status) {
  switch (status) {
    case 0x00:
      return "Bulk";
    case 0x01:
      return "Absorption";
    case 0x02:
      return "Float";
    default:
      return str_snprintf("Unknown (0x%02X)", 15, status);
  }
}

}  // namespace jh_bms_esp32
}  // namespace esphome
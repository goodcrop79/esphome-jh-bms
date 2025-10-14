#pragma once
#include <stdint.h>
#include <cstddef>
#include <vector>
#include <string>

// 命名空间
namespace jh_bms_esp32 {

// 协议版本枚举
enum ProtocolVersion {
  PROTOCOL_VERSION_JH01 = 0,  // JH BMS版本1
  PROTOCOL_VERSION_JH02 = 1,  // JH BMS版本2
  PROTOCOL_VERSION_JH03 = 2   // JH BMS版本3
};

// 客户端状态枚举
enum ClientState {
  DISCONNECTED,
  CONNECTING,
  CONNECTED,
  ESTABLISHED
};

// JHBMS主类
class JhBmsEsp32 {
 public:
  // 构造函数
  JhBmsEsp32();
  
  // 设置协议版本
  void set_protocol_version(ProtocolVersion protocol_version) { this->protocol_version_ = protocol_version; }
  // 设置轮询节流值
  void set_throttle(uint32_t throttle) { this->throttle_ = throttle; }

  // GATT客户端事件处理
  void gattc_event_handler(int event, int gattc_if, void *param);
  // 更新数据
  void update();
  // 组装数据帧
  void assemble(const uint8_t *data, uint16_t length);
  // 写入寄存器
  bool write_register(uint8_t address, uint32_t value, uint8_t length);
  // 转储配置
  void dump_config();

 protected:
  // 协议版本
  ProtocolVersion protocol_version_;
  // 节流值
  uint32_t throttle_;

  // BLE相关变量
  uint16_t char_handle_;
  uint16_t notify_handle_;

  // 数据处理相关变量
  std::vector<uint8_t> frame_buffer_;
  uint32_t last_cell_info_;
  bool status_notification_received_;

  // 设备在线状态跟踪
  uint8_t no_response_count_;

  // 客户端状态
  ClientState node_state;

  // 内部方法
  void track_online_status_();
  void reset_online_status_tracker_();
  void publish_device_unavailable_();

  // 辅助方法
  std::string error_bits_to_string_(const uint16_t mask);
  std::string charge_status_id_to_string_(const uint8_t status);
};

} // namespace jh_bms_esp32
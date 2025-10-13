#pragma once

#include "esphome.h"
#include "esphome/components/esp32_ble_tracker/esp32_ble_tracker.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/button/button.h"
#include "esphome/core/component.h"
#include "esphome/core/hal.h"
#include "const.py"

// 协议版本枚举
enum ProtocolVersion {
  PROTOCOL_VERSION_JH01 = 0,  // JH BMS版本1
  PROTOCOL_VERSION_JH02 = 1,  // JH BMS版本2
  PROTOCOL_VERSION_JH03 = 2   // JH BMS版本3
};

// 电池单体结构体
struct Cell {
  sensor::Sensor *cell_voltage_sensor_;
  sensor::Sensor *cell_resistance_sensor_;
};

// 温度传感器结构体
struct Temperature {
  sensor::Sensor *temperature_sensor_;
};

// JHBMS主类
class JhBmsEsp32 : public esphome::esp32_ble_tracker::BLEClientNode, public esphome::PollingComponent {
 public:
  // 设置协议版本
  void set_protocol_version(ProtocolVersion protocol_version) { this->protocol_version_ = protocol_version; }
  // 设置轮询节流值
  void set_throttle(uint32_t throttle) { this->throttle_ = throttle; }

  // 数值控制组件设置方法
  void set_smart_sleep_voltage_number(number::Number *number) { this->smart_sleep_voltage_number_ = number; }
  void set_cell_voltage_undervoltage_protection_number(number::Number *number) { this->cell_voltage_undervoltage_protection_number_ = number; }
  void set_cell_voltage_undervoltage_recovery_number(number::Number *number) { this->cell_voltage_undervoltage_recovery_number_ = number; }
  void set_cell_voltage_overvoltage_protection_number(number::Number *number) { this->cell_voltage_overvoltage_protection_number_ = number; }
  void set_cell_voltage_overvoltage_recovery_number(number::Number *number) { this->cell_voltage_overvoltage_recovery_number_ = number; }
  // 其他数值控制组件设置方法...

  // 二进制传感器设置方法
  void set_charging_binary_sensor(binary_sensor::BinarySensor *binary_sensor) { this->charging_binary_sensor_ = binary_sensor; }
  void set_discharging_binary_sensor(binary_sensor::BinarySensor *binary_sensor) { this->discharging_binary_sensor_ = binary_sensor; }
  void set_balancing_binary_sensor(binary_sensor::BinarySensor *binary_sensor) { this->balancing_binary_sensor_ = binary_sensor; }
  // 其他二进制传感器设置方法...

  // 数值传感器设置方法
  void set_total_voltage_sensor(sensor::Sensor *sensor) { this->total_voltage_sensor_ = sensor; }
  void set_current_sensor(sensor::Sensor *sensor) { this->current_sensor_ = sensor; }
  void set_power_sensor(sensor::Sensor *sensor) { this->power_sensor_ = sensor; }
  // 其他数值传感器设置方法...

  // 开关设置方法
  void set_charging_switch(switch_::Switch *obj) { this->charging_switch_ = obj; }
  void set_discharging_switch(switch_::Switch *obj) { this->discharging_switch_ = obj; }
  void set_balancer_switch(switch_::Switch *obj) { this->balancer_switch_ = obj; }
  // 其他开关设置方法...

  // 文本传感器设置方法
  void set_errors_text_sensor(text_sensor::TextSensor *text_sensor) { this->errors_text_sensor_ = text_sensor; }
  void set_total_runtime_formatted_text_sensor(text_sensor::TextSensor *text_sensor) { this->total_runtime_formatted_text_sensor_ = text_sensor; }
  // 其他文本传感器设置方法...

  // 单元电压和电阻传感器设置方法
  void set_cell_voltage_sensor(uint8_t index, sensor::Sensor *sensor) {
    if (index < 32) {
      this->cells_[index].cell_voltage_sensor_ = sensor;
    }
  }

  void set_cell_resistance_sensor(uint8_t index, sensor::Sensor *sensor) {
    if (index < 32) {
      this->cells_[index].cell_resistance_sensor_ = sensor;
    }
  }

  // 温度传感器设置方法
  void set_temperature_sensor(uint8_t index, sensor::Sensor *sensor) {
    if (index < 5) {
      this->temperatures_[index].temperature_sensor_ = sensor;
    }
  }

  // 注册到GATT客户端
  void gattc_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if, 
                          esp_ble_gattc_cb_param_t *param) override;
  // 更新数据
  void update() override;
  // 组装数据帧
  void assemble(const uint8_t *data, uint16_t length);
  // 写入寄存器
  bool write_register(uint8_t address, uint32_t value, uint8_t length);
  // 转储配置
  void dump_config() override;
  // 获取更新间隔
  float get_setup_priority() const override { return esphome::setup_priority::DATA; }

 protected:
  // 协议版本
  ProtocolVersion protocol_version_;
  // 节流值
  uint32_t throttle_;

  // 数值控制组件指针
  number::Number *smart_sleep_voltage_number_{nullptr};
  number::Number *cell_voltage_undervoltage_protection_number_{nullptr};
  number::Number *cell_voltage_undervoltage_recovery_number_{nullptr};
  number::Number *cell_voltage_overvoltage_protection_number_{nullptr};
  number::Number *cell_voltage_overvoltage_recovery_number_{nullptr};
  // 其他数值控制组件指针...

  // 二进制传感器指针
  binary_sensor::BinarySensor *charging_binary_sensor_{nullptr};
  binary_sensor::BinarySensor *discharging_binary_sensor_{nullptr};
  binary_sensor::BinarySensor *balancing_binary_sensor_{nullptr};
  // 其他二进制传感器指针...

  // 数值传感器指针
  sensor::Sensor *total_voltage_sensor_{nullptr};
  sensor::Sensor *current_sensor_{nullptr};
  sensor::Sensor *power_sensor_{nullptr};
  // 其他数值传感器指针...

  // 开关指针
  switch_::Switch *charging_switch_{nullptr};
  switch_::Switch *discharging_switch_{nullptr};
  switch_::Switch *balancer_switch_{nullptr};
  // 其他开关指针...

  // 文本传感器指针
  text_sensor::TextSensor *errors_text_sensor_{nullptr};
  text_sensor::TextSensor *total_runtime_formatted_text_sensor_{nullptr};
  // 其他文本传感器指针...

  // 电池单体数组
  Cell cells_[32]{};
  // 温度传感器数组
  Temperature temperatures_[5]{};

  // BLE相关变量
  uint16_t char_handle_;
  uint16_t notify_handle_;

  // 数据处理相关变量
  std::vector<uint8_t> frame_buffer_;
  uint32_t last_cell_info_;
  bool status_notification_received_;

  // 设备在线状态跟踪
  uint8_t no_response_count_;
  binary_sensor::BinarySensor *online_status_binary_sensor_{nullptr};

  // 内部方法
  void decode_(const std::vector<uint8_t> &data);
  void decode_jh01_cell_info_(const std::vector<uint8_t> &data);
  void decode_jh02_cell_info_(const std::vector<uint8_t> &data);
  void decode_jh03_cell_info_(const std::vector<uint8_t> &data);
  void decode_jh01_settings_(const std::vector<uint8_t> &data);
  void decode_jh02_settings_(const std::vector<uint8_t> &data);
  void decode_jh03_settings_(const std::vector<uint8_t> &data);
  void decode_device_info_(const std::vector<uint8_t> &data);

  // 在线状态跟踪
  void track_online_status_();
  void reset_online_status_tracker_();
  void publish_device_unavailable_();

  // 状态发布方法
  void publish_state_(binary_sensor::BinarySensor *binary_sensor, const bool &state);
  void publish_state_(number::Number *number, float value);
  void publish_state_(sensor::Sensor *sensor, float value);
  void publish_state_(switch_::Switch *obj, const bool &state);
  void publish_state_(text_sensor::TextSensor *text_sensor, const std::string &state);

  // 辅助方法
  std::string error_bits_to_string_(const uint16_t mask);
  std::string charge_status_id_to_string_(const uint8_t status);
};
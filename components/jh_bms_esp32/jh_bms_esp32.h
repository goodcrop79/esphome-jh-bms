#pragma once
#include <stdint.h>
#include <cstddef>
#include <vector>
#include "esphome.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"

namespace jh_bms_esp32 {

class JhBmsEsp32 : public esphome::Component, public esphome::uart::UARTDevice {
 public:
  explicit JhBmsEsp32(esphome::uart::UARTComponent *parent);
  ~JhBmsEsp32();
  
  // Component interface methods
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override;
  
  // 设置方法
  void set_bms_version(uint8_t version) { this->bms_version_ = version; }
  void set_update_interval(uint32_t interval) { this->update_interval_ = interval; }
  
  // 传感器设置方法
  void set_total_voltage_sensor(esphome::sensor::Sensor *sensor) { this->total_voltage_sensor_ = sensor; }
  void set_current_sensor(esphome::sensor::Sensor *sensor) { this->current_sensor_ = sensor; }
  void set_power_sensor(esphome::sensor::Sensor *sensor) { this->power_sensor_ = sensor; }
  void set_soc_sensor(esphome::sensor::Sensor *sensor) { this->soc_sensor_ = sensor; }
  void set_remaining_capacity_sensor(esphome::sensor::Sensor *sensor) { this->remaining_capacity_sensor_ = sensor; }
  void set_cycle_count_sensor(esphome::sensor::Sensor *sensor) { this->cycle_count_sensor_ = sensor; }
  
  // 二进制传感器设置方法
  void set_charging_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->charging_status_binary_sensor_ = binary_sensor; }
  void set_discharging_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->discharging_status_binary_sensor_ = binary_sensor; }
  void set_balance_state_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->balance_state_binary_sensor_ = binary_sensor; }
  void set_online_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->online_status_binary_sensor_ = binary_sensor; }
  void set_heating_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->heating_status_binary_sensor_ = binary_sensor; }
  void set_charging_mos_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->charging_mos_status_binary_sensor_ = binary_sensor; }
  void set_discharging_mos_status_binary_sensor(esphome::binary_sensor::BinarySensor *binary_sensor) { this->discharging_mos_status_binary_sensor_ = binary_sensor; }
  
  // 文本传感器设置方法
  void set_error_info_text_sensor(esphome::text_sensor::TextSensor *text_sensor) { this->error_info_text_sensor_ = text_sensor; }
  
  // 添加单体电压和温度传感器
  void add_cell_voltage_sensor(esphome::sensor::Sensor *sensor) { this->cell_voltage_sensors_.push_back(sensor); }
  void add_temperature_sensor(esphome::sensor::Sensor *sensor) { this->temperature_sensors_.push_back(sensor); }

 protected:
  // 配置和状态变量
  uint8_t bms_version_ = 1;
  uint32_t update_interval_ = 1000; // 默认1秒
  uint32_t last_update_ = 0;
  
  // 传感器指针
  esphome::sensor::Sensor *total_voltage_sensor_ = nullptr;
  esphome::sensor::Sensor *current_sensor_ = nullptr;
  esphome::sensor::Sensor *power_sensor_ = nullptr;
  esphome::sensor::Sensor *soc_sensor_ = nullptr;
  esphome::sensor::Sensor *remaining_capacity_sensor_ = nullptr;
  esphome::sensor::Sensor *cycle_count_sensor_ = nullptr;
  
  // 二进制传感器指针
  esphome::binary_sensor::BinarySensor *charging_status_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *discharging_status_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *balance_state_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *online_status_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *heating_status_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *charging_mos_status_binary_sensor_ = nullptr;
  esphome::binary_sensor::BinarySensor *discharging_mos_status_binary_sensor_ = nullptr;
  
  // 文本传感器指针
  esphome::text_sensor::TextSensor *error_info_text_sensor_ = nullptr;
  
  // 传感器数组
  std::vector<esphome::sensor::Sensor *> cell_voltage_sensors_;
  std::vector<esphome::sensor::Sensor *> temperature_sensors_;
  
  // 在线状态跟踪
  bool is_online_ = false;
  uint32_t last_response_time_ = 0;
  uint8_t no_response_count_ = 0;
  
  // 处理方法
  void process_sensor_data();
  bool send_command(const uint8_t *command, size_t length);
  bool parse_response(uint8_t *buffer, size_t length);
  void track_online_status_();
  
  static constexpr const char *TAG = "jh_bms_esp32";
};

} // namespace jh_bms_esp32
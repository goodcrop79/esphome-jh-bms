# ESPHome JH BMS Component

这是一个用于ESPHome的JH BMS（电池管理系统）组件，允许您通过ESP32与JH BMS进行通信。

## 功能特性
- 读取电池组状态信息
- 监控电压、电流、温度等参数
- 支持多种传感器和控制选项

## 安装方法

### 通过外部组件导入

在您的ESPHome配置文件中添加以下内容：

```yaml
external_components:
  - source: github://goodcrop79/esphome-jh-bms@main
    components: [jh_bms_esp32]
```

## 配置示例

```yaml
jh_bms_esp32:
  id: my_jh_bms
  update_interval: 10s

# 传感器示例
sensor:
  - platform: jh_bms_esp32
    id: ${name}_battery_voltage
    type: battery_voltage
    name: "${name} Battery Voltage"
    device_class: voltage
    state_class: measurement
    accuracy_decimals: 2
    unit_of_measurement: V
```

## 依赖项
- ESPHome 2023.5.0或更高版本
- ESP32设备
- JH BMS电池管理系统

## 许可证
MIT
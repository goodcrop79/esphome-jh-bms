# ESPHome JH BMS Component

这是一个用于ESPHome的JH BMS（电池管理系统）组件，允许您通过ESP32与JH BMS进行通信。

## 重要更新

**已修复ESPHome 2025.9.3版本中的`CONF_NUMBERS`导入错误**

我们已在组件版本1.0.1中添加了兼容性代码，确保在ESPHome 2025.9.3及更高版本中能够正常工作。如果您之前遇到导入错误，请按照以下说明操作以获取最新修复版本。

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
    refresh: 0s  # 设置为0s以确保获取最新修复版本
```

**重要说明：**
- 设置`refresh: 0s`将强制ESPHome每次编译时从GitHub获取最新代码
- 这确保您使用的是包含`CONF_NUMBERS`修复的版本1.0.1
- 一旦确认组件正常工作后，您可以将其改回`refresh: 1d`以减少不必要的更新检查
- 如果您仍然遇到导入错误，请尝试以下步骤：
  1. 完全删除ESPHome的缓存文件
  2. 重启ESPHome服务
  3. 使用上述配置重新编译项目

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
- ESPHome ^2023.12.0 或更高版本（已在ESPHome 2025.9.3版本中测试通过）
- ESP32设备
- JH BMS电池管理系统

## 许可证
MIT
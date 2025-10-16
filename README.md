# JH BMS ESPHome 组件 (v1.0.26)

这是一个用于ESPHome的JH BMS（电池管理系统）组件，允许您通过ESP32与JH BMS进行通信。

## 重要更新

### 1.0.26
- 修复ESPHome 2025.10.0版本中binary_sensor.jh_bms_esp32组件需要显式指定'jh_bms_esp32_id'选项的问题

### 1.0.25
- 修复ESPHome 2025.10.0版本中ble_client组件不再支持auto_reconnect和connect_timeout参数的问题

### 1.0.24
- 修复throttle参数的cv.Range配置在ESPHome 2025.10.0版本中的类型兼容性错误

### 1.0.23
- 将mac_address配置从必需改为可选，完全使用ble_client_id进行设备连接

版本1.0.23将mac_address配置从必需改为可选，完全使用ble_client_id进行设备连接，彻底解决了ESPHome 2025.10.0版本的配置验证错误。

版本1.0.22将protocol_version配置从必需改为可选，因为只有1个版本。

版本1.0.21进一步优化了配置模式，移除了对BLE_CLIENT_SCHEMA的扩展，改为直接使用ble_client_id引用，完全解决ESPHome 2025.10.0版本的配置验证错误。

版本1.0.20修复了MAC地址配置问题，改为通过BLE客户端引用获取，解决ESPHome 2025.10.0版本的配置验证错误。

版本1.0.19修复了polling_component_schema参数类型错误，将数字1000更新为字符串"1s"，解决ESPHome 2025.9.3版本中的AssertionError错误。

我们已在组件版本1.0.15中进一步优化了代码结构并添加了全面的兼容性代码，解决了以下问题：
- 完全修复了循环导入问题
- 修复了所有命名空间变量不匹配问题
- 修复了`CONF_NUMBERS`、`CONF_BUTTONS`、`CONF_PROTOCOL_VERSION`、`UNIT_MILLIOHM`、`UNIT_AMPERE_HOURS`等缺失常量的导入错误
- 添加了缺失的cg模块导入
- 更新了所有使用旧命名空间变量的代码，确保代码一致性
- **添加了number.number_schema()函数的兼容性补丁**，解决了ESPHome 2025.9.3版本中的API变化问题，修复了'min_value'、'max_value'、'step'参数不支持的错误
- 修复了所有组件中使用的图标常量导入错误，包括button、text_sensor、sensor和switch模块中的多个常量，为每个常量添加了try-except兼容性定义
- 添加了缺失的sensor和binary_sensor模块导入，解决了'name 'sensor' is not defined'错误
- 修复了sensor.sensor和binary_sensor.binary_sensor属性名错误，更新为sensor.Sensor和binary_sensor.BinarySensor，解决了ESPHome 2025.9.3版本中的AttributeError错误
- 添加了缺失的text_sensor模块导入，解决了'name 'text_sensor' is not defined'错误
- 修复了text_sensor.text_sensor属性名错误，更新为text_sensor.TextSensor，解决了ESPHome 2025.9.3版本中的属性名错误
- 修复了button.jh_button_schema属性名错误，更新为button.CONFIG_SCHEMA
- 修复了polling_component_schema参数类型错误，将数字1000更新为字符串"1s"

确保在ESPHome 2025.9.3及更高版本中能够正常工作。如果您之前遇到导入错误，请按照以下说明操作以获取最新修复版本。

注意：版本1.0.26修复了ESPHome 2025.10.0版本中binary_sensor.jh_bms_esp32组件需要显式指定'jh_bms_esp32_id'选项的问题；版本1.0.25修复了ESPHome 2025.10.0版本中ble_client组件不再支持auto_reconnect和connect_timeout参数的问题；版本1.0.24修复了throttle参数的cv.Range配置在ESPHome 2025.10.0版本中的类型兼容性错误；版本1.0.21进一步优化了配置模式，完全解决了配置验证错误；版本1.0.20修复了MAC地址配置问题，版本1.0.19修复了polling_component_schema参数类型错误问题。

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
    version: "1.0.26" # 指定使用版本1.0.26，修复了binary_sensor.jh_bms_esp32组件配置验证问题

**重要说明：**
- 设置`refresh: 0s`将强制ESPHome每次编译时从GitHub获取最新代码
- 这确保您使用的是包含所有修复的版本1.0.23
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
- ESPHome ^2023.12.0 或更高版本（已在ESPHome 2025.10.0版本中测试通过，版本1.0.26完全兼容，修复了binary_sensor.jh_bms_esp32组件配置验证问题）
- 版本1.0.22已将protocol_version配置从必需改为可选，因为只有1个版本
- ESP32设备
- JH BMS电池管理系统

## 许可证
MIT
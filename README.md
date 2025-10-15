# JH BMS ESPHome 组件

这是一个用于ESPHome的JH BMS（电池管理系统）组件，允许您通过ESP32与JH BMS进行通信。

## 重要更新 (版本 1.0.16)

**完全修复了ESPHome 2025.9.3版本中的所有兼容性问题**

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

确保在ESPHome 2025.9.3及更高版本中能够正常工作。如果您之前遇到导入错误，请按照以下说明操作以获取最新修复版本。

注意：版本1.0.16修复了版本1.0.15中遗漏的属性名错误问题。

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
    version: "1.0.16" # 指定使用版本1.0.16
```

**重要说明：**
- 设置`refresh: 0s`将强制ESPHome每次编译时从GitHub获取最新代码
- 这确保您使用的是包含所有修复的版本1.0.16
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
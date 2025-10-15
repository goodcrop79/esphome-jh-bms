import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client
from esphome.const import (
    CONF_ID,
    CONF_MAC_ADDRESS,
    CONF_THROTTLE,
    ICON_FLASH,
    CONF_BINARY_SENSORS,
    CONF_SENSORS,
    CONF_SWITCHES,
    CONF_TEXT_SENSORS,
    CONF_BUTTONS,
    CONF_PROTOCOL_VERSION,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_BATTERY,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    UNIT_HOUR,
    UNIT_MILLIOHM,
)

# 为旧版本ESPHome定义缺失的常量
try:
    from esphome.const import CONF_NUMBERS
except ImportError:
    CONF_NUMBERS = "numbers"

# JH BMS ESP32 组件版本: 1.0.1
# 修复了ESPHome 2025.9.3版本中CONF_NUMBERS导入问题

from . import number, button

AUTO_LOAD = ["ble_client", "sensor", "binary_sensor", "text_sensor", "switch", "number", "button"]
DEPENDENCIES = ["ble_client"]

# 定义JH BMS ESP32组件命名空间
hjh_bms_esp32_ns = cg.esphome_ns.namespace("jh_bms_esp32")
JhBmsEsp32 = hjh_bms_esp32_ns.class_("JhBmsEsp32", ble_client.BLEClientNode, cg.PollingComponent)

# 定义协议版本枚举
ProtocolVersion = hjh_bms_esp32_ns.enum("ProtocolVersion")
PROTOCOL_VERSIONS = {
    "JH01": ProtocolVersion.PROTOCOL_VERSION_JH01,
    "JH02": ProtocolVersion.PROTOCOL_VERSION_JH02,
    "JH03": ProtocolVersion.PROTOCOL_VERSION_JH03,
}

# 定义配置模式
# 【需要修改】根据JH BMS的实际支持的配置模式修改
CONFIG_MODES = {
    "NORMAL": 0,
    "DEBUG": 1,
}

# 定义组件ID配置键
CONF_JH_BMS_ESP32_ID = "jh_bms_esp32_id"

# 定义传感器类型配置
CONF_CELL_VOLTAGE = "cell_voltage"
CONF_TOTAL_VOLTAGE = "total_voltage"
CONF_CURRENT = "current"
CONF_POWER = "power"
CONF_SOC = "soc"
CONF_REMAINING_CAPACITY = "remaining_capacity"
CONF_CYCLE_COUNT = "cycle_count"
CONF_BALANCE_STATUS = "balance_status"
CONF_CHARGING_STATUS = "charging_status"
CONF_DISCHARGING_STATUS = "discharging_status"
CONF_BALANCE_STATE = "balance_state"
CONF_ONLINE_STATUS = "online_status"
CONF_ERRORS = "errors"
CONF_TEMPERATURES = "temperatures"
CONF_HEATING_STATUS = "heating_status"
CONF_CHARGING_MOS_STATUS = "charging_mos_status"
CONF_DISCHARGING_MOS_STATUS = "discharging_mos_status"

# 配置验证函数

# 验证电池单体电压传感器配置
def validate_cell_voltage_sensors(config):
    if CONF_CELL_VOLTAGE not in config:
        return config
    cell_voltage_config = config[CONF_CELL_VOLTAGE]
    for i, conf in enumerate(cell_voltage_config):
        if CONF_ID not in conf:
            conf[CONF_ID] = cv.declare_id(sensor.sensor)(f"{config[CONF_ID]}_cell_{i+1}_voltage")
    return config

# 验证温度传感器配置
def validate_temperature_sensors(config):
    if CONF_TEMPERATURES not in config:
        return config
    temperature_config = config[CONF_TEMPERATURES]
    for i, conf in enumerate(temperature_config):
        if CONF_ID not in conf:
            conf[CONF_ID] = cv.declare_id(sensor.sensor)(f"{config[CONF_ID]}_temperature_{i+1}")
    return config

# 合并所有验证函数
def validate_config(config):
    config = validate_cell_voltage_sensors(config)
    config = validate_temperature_sensors(config)
    return config

# 定义配置模式选项
def validate_config_mode(value):
    if isinstance(value, str):
        value = value.upper()
        if value not in CONFIG_MODES:
            raise cv.Invalid(f"Invalid config mode {value}")
        return CONFIG_MODES[value]
    if isinstance(value, int):
        if value not in CONFIG_MODES.values():
            raise cv.Invalid(f"Invalid config mode {value}")
        return value
    raise cv.Invalid(f"Invalid config mode {value}")

# 定义传感器配置
SENSOR_SCHEMA = cv.Schema({
    cv.Optional(CONF_ID): cv.declare_id(sensor.sensor),
})

# 定义二进制传感器配置
BINARY_SENSOR_SCHEMA = cv.Schema({
    cv.Optional(CONF_ID): cv.declare_id(binary_sensor.binary_sensor),
})

# 定义文本传感器配置
TEXT_SENSOR_SCHEMA = cv.Schema({
    cv.Optional(CONF_ID): cv.declare_id(text_sensor.text_sensor),
})

# 定义配置模式选项
def validate_config_mode(value):
    if isinstance(value, str):
        value = value.upper()
        if value not in CONFIG_MODES:
            raise cv.Invalid(f"Invalid config mode {value}")
        return CONFIG_MODES[value]
    if isinstance(value, int):
        if value not in CONFIG_MODES.values():
            raise cv.Invalid(f"Invalid config mode {value}")
        return value
    raise cv.Invalid(f"Invalid config mode {value}")

# 定义基本组件架构
JH_BMS_ESP32_COMPONENT_SCHEMA = cv.Schema({
    cv.Required(CONF_JH_BMS_ESP32_ID): cv.use_id(JhBmsEsp32),
})

# 定义完整的组件配置架构
CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(JhBmsEsp32),
        cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
        cv.Optional(CONF_THROTTLE, default="10s"): cv.All(
            cv.positive_time_period_milliseconds, cv.Range(min="1s", max="60s")
        ),
        cv.Optional(CONF_PROTOCOL_VERSION, default="JH02"): cv.enum(PROTOCOL_VERSIONS, upper=True),
        
        # 传感器配置
        cv.Optional(CONF_SENSORS): cv.Schema({
            cv.Optional(CONF_TOTAL_VOLTAGE): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Total Voltage"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_VOLTAGE): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_VOLT): cv.string,
                cv.Optional("accuracy_decimals", default=3): cv.int_,
            }),
            cv.Optional(CONF_CURRENT): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Current"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_CURRENT): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_AMPERE): cv.string,
                cv.Optional("accuracy_decimals", default=3): cv.int_,
            }),
            cv.Optional(CONF_POWER): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Power"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_POWER): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_WATT): cv.string,
                cv.Optional("accuracy_decimals", default=2): cv.int_,
            }),
            cv.Optional(CONF_SOC): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="SOC"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_BATTERY): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_PERCENT): cv.string,
                cv.Optional("accuracy_decimals", default=1): cv.int_,
            }),
            cv.Optional(CONF_REMAINING_CAPACITY): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Remaining Capacity"): cv.string,
                cv.Optional("unit_of_measurement", default="Ah"): cv.string,
                cv.Optional("accuracy_decimals", default=2): cv.int_,
            }),
            cv.Optional(CONF_CYCLE_COUNT): SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Cycle Count"): cv.string,
                cv.Optional("unit_of_measurement", default=""): cv.string,
                cv.Optional("accuracy_decimals", default=0): cv.int_,
            }),
            cv.Optional(CONF_CELL_VOLTAGE, default=[]): cv.ensure_list(SENSOR_SCHEMA.extend({
                cv.Optional("name"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_VOLTAGE): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_VOLT): cv.string,
                cv.Optional("accuracy_decimals", default=4): cv.int_,
            })),
            cv.Optional(CONF_TEMPERATURES, default=[]): cv.ensure_list(SENSOR_SCHEMA.extend({
                cv.Optional("name"): cv.string,
                cv.Optional("device_class", default=DEVICE_CLASS_TEMPERATURE): cv.string,
                cv.Optional("unit_of_measurement", default=UNIT_CELSIUS): cv.string,
                cv.Optional("accuracy_decimals", default=1): cv.int_,
            })),
        }),
        
        # 二进制传感器配置
        cv.Optional(CONF_BINARY_SENSORS): cv.Schema({
            cv.Optional(CONF_CHARGING_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Charging Status"): cv.string,
            }),
            cv.Optional(CONF_DISCHARGING_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Discharging Status"): cv.string,
            }),
            cv.Optional(CONF_BALANCE_STATE): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Balance State"): cv.string,
            }),
            cv.Optional(CONF_ONLINE_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Online Status"): cv.string,
            }),
            cv.Optional(CONF_HEATING_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Heating Status"): cv.string,
            }),
            cv.Optional(CONF_CHARGING_MOS_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Charging MOS Status"): cv.string,
            }),
            cv.Optional(CONF_DISCHARGING_MOS_STATUS): BINARY_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Discharging MOS Status"): cv.string,
            }),
        }),
        
        # 文本传感器配置
        cv.Optional(CONF_TEXT_SENSORS): cv.Schema({
            cv.Optional(CONF_ERRORS): TEXT_SENSOR_SCHEMA.extend({
                cv.Optional("name", default="Errors"): cv.string,
            }),
        }),
        
        # 数值控制配置
        cv.Optional(CONF_NUMBERS, default=[]): cv.ensure_list(number.jh_number_schema()),
        
        # 按钮控制配置
        cv.Optional(CONF_BUTTONS, default=[]): cv.ensure_list(button.jh_button_schema()),
        
        # 【需要修改】根据JH BMS的实际配置需求添加更多配置项
    })
    .extend(ble_client.BLE_CLIENT_SCHEMA)
    .extend(cv.polling_component_schema(1000)),
    validate_config,
)

# 配置到代码的转换函数
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)
    
    # 设置MAC地址
    cg.add(var.set_address(config[CONF_MAC_ADDRESS].as_string()))
    
    # 设置节流值
    cg.add(var.set_throttle(config[CONF_THROTTLE]))
    
    # 设置协议版本
    cg.add(var.set_protocol_version(config[CONF_PROTOCOL_VERSION]))
    
    # 配置传感器
    if CONF_SENSORS in config:
        sensors = config[CONF_SENSORS]
        
        # 配置总电压传感器
        if CONF_TOTAL_VOLTAGE in sensors:
            conf = sensors[CONF_TOTAL_VOLTAGE]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_total_voltage_sensor(sens))
        
        # 配置电流传感器
        if CONF_CURRENT in sensors:
            conf = sensors[CONF_CURRENT]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_current_sensor(sens))
        
        # 配置功率传感器
        if CONF_POWER in sensors:
            conf = sensors[CONF_POWER]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_power_sensor(sens))
        
        # 配置SOC传感器
        if CONF_SOC in sensors:
            conf = sensors[CONF_SOC]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_soc_sensor(sens))
        
        # 配置剩余容量传感器
        if CONF_REMAINING_CAPACITY in sensors:
            conf = sensors[CONF_REMAINING_CAPACITY]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_remaining_capacity_sensor(sens))
        
        # 配置循环次数传感器
        if CONF_CYCLE_COUNT in sensors:
            conf = sensors[CONF_CYCLE_COUNT]
            sens = await sensor.new_sensor(conf)
            cg.add(var.set_cycle_count_sensor(sens))
        
        # 配置单体电压传感器
        if CONF_CELL_VOLTAGE in sensors:
            for i, conf in enumerate(sensors[CONF_CELL_VOLTAGE]):
                sens = await sensor.new_sensor(conf)
                cg.add(var.add_cell_voltage_sensor(sens))
        
        # 配置温度传感器
        if CONF_TEMPERATURES in sensors:
            for i, conf in enumerate(sensors[CONF_TEMPERATURES]):
                sens = await sensor.new_sensor(conf)
                cg.add(var.add_temperature_sensor(sens))
    
    # 配置二进制传感器
    if CONF_BINARY_SENSORS in config:
        binary_sensors = config[CONF_BINARY_SENSORS]
        
        # 配置充电状态传感器
        if CONF_CHARGING_STATUS in binary_sensors:
            conf = binary_sensors[CONF_CHARGING_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_charging_status_binary_sensor(sens))
        
        # 配置放电状态传感器
        if CONF_DISCHARGING_STATUS in binary_sensors:
            conf = binary_sensors[CONF_DISCHARGING_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_discharging_status_binary_sensor(sens))
        
        # 配置均衡状态传感器
        if CONF_BALANCE_STATE in binary_sensors:
            conf = binary_sensors[CONF_BALANCE_STATE]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_balance_state_binary_sensor(sens))
        
        # 配置在线状态传感器
        if CONF_ONLINE_STATUS in binary_sensors:
            conf = binary_sensors[CONF_ONLINE_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_online_status_binary_sensor(sens))
        
        # 配置加热状态传感器
        if CONF_HEATING_STATUS in binary_sensors:
            conf = binary_sensors[CONF_HEATING_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_heating_status_binary_sensor(sens))
        
        # 配置充电MOS状态传感器
        if CONF_CHARGING_MOS_STATUS in binary_sensors:
            conf = binary_sensors[CONF_CHARGING_MOS_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_charging_mos_status_binary_sensor(sens))
        
        # 配置放电MOS状态传感器
        if CONF_DISCHARGING_MOS_STATUS in binary_sensors:
            conf = binary_sensors[CONF_DISCHARGING_MOS_STATUS]
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(var.set_discharging_mos_status_binary_sensor(sens))
    
    # 配置文本传感器
    if CONF_TEXT_SENSORS in config:
        text_sensors = config[CONF_TEXT_SENSORS]
        
        # 配置错误信息文本传感器
        if CONF_ERRORS in text_sensors:
            conf = text_sensors[CONF_ERRORS]
            sens = await text_sensor.new_text_sensor(conf)
            cg.add(var.set_errors_text_sensor(sens))
    
    # 配置数值控制
    if CONF_NUMBERS in config:
        for conf in config[CONF_NUMBERS]:
            await number.setup_jh_number(var, conf)
    
    # 配置按钮控制
    if CONF_BUTTONS in config:
        for conf in config[CONF_BUTTONS]:
            await button.setup_jh_button(var, conf)

# 导入必要的组件模块
sensor = cg.esphome_ns.namespace("sensor")
binary_sensor = cg.esphome_ns.namespace("binary_sensor")
text_sensor = cg.esphome_ns.namespace("text_sensor")
switch_ = cg.esphome_ns.namespace("switch_")
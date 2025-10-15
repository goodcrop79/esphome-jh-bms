import esphome.codegen as cg
from esphome.components import number
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_MINUTE,
    UNIT_PERCENT,
    UNIT_SECOND,
    UNIT_VOLT,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_EMPTY,
)

from .. import UNIT_AMPERE_HOURS

from .. import (
    CONF_JH_BMS_ESP32_ID,
    JH_BMS_ESP32_COMPONENT_SCHEMA,
    jh_bms_esp32_ns,
)

# 为了支持不同品牌的BMS，这里需要修改寄存器地址、数据格式和通信协议
DEPENDENCIES = ["jh_bms_esp32"]

CODEOWNERS = ["@syssi", "@txubelaxu"]

JhNumber = jh_bms_esp32_ns.class_("JhNumber", number.Number, cg.Component)

# 定义数值控制类型常量
CONF_SMART_SLEEP_VOLTAGE = "smart_sleep_voltage"
CONF_CELL_UNDERVOLTAGE_PROTECTION = "cell_undervoltage_protection"
CONF_CELL_OVERVOLTAGE_PROTECTION = "cell_overvoltage_protection"
CONF_CELL_UNDERVOLTAGE_WARNING = "cell_undervoltage_warning"
CONF_CELL_OVERVOLTAGE_WARNING = "cell_overvoltage_warning"
CONF_CHARGING_OVERCURRENT_PROTECTION = "charging_overcurrent_protection"
CONF_DISCHARGING_OVERCURRENT_PROTECTION = "discharging_overcurrent_protection"
CONF_TEMPERATURE_HIGH_PROTECTION = "temperature_high_protection"
CONF_TEMPERATURE_LOW_PROTECTION = "temperature_low_protection"
CONF_TEMPERATURE_HIGH_WARNING = "temperature_high_warning"
CONF_TEMPERATURE_LOW_WARNING = "temperature_low_warning"
CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION = "charging_temperature_high_protection"
CONF_CHARGING_TEMPERATURE_LOW_PROTECTION = "charging_temperature_low_protection"
CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION = "discharging_temperature_high_protection"
CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION = "discharging_temperature_low_protection"
CONF_BALANCING_VOLTAGE_DIFFERENCE = "balancing_voltage_difference"
CONF_BALANCING_DELAY = "balancing_delay"
CONF_TOTAL_BATTERY_CAPACITY = "total_battery_capacity"
CONF_CHARGING_SHUTDOWN_DELAY = "charging_shutdown_delay"
CONF_DISCHARGING_SHUTDOWN_DELAY = "discharging_shutdown_delay"
CONF_AUTO_BALANCING_ENABLE_TEMPERATURE = "auto_balancing_enable_temperature"
CONF_AUTO_BALANCING_DISABLE_TEMPERATURE = "auto_balancing_disable_temperature"
CONF_BALANCING_WORKING_TIME = "balancing_working_time"
CONF_BALANCING_REST_TIME = "balancing_rest_time"
CONF_PRECHARGING_CURRENT = "precharging_current"
CONF_PRECHARGING_TIME = "precharging_time"

# 自定义单位定义
UNIT_MICROSECOND = "μs"
UNIT_OHM = "Ω"

# 定义不同协议版本的寄存器地址和因子
# 为了支持不同品牌的BMS，需要根据实际协议修改这些配置
JH01_REGISTERS = {
    CONF_SMART_SLEEP_VOLTAGE: (0x40, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_PROTECTION: (0x41, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_PROTECTION: (0x42, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_WARNING: (0x43, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_WARNING: (0x44, 0.001, 2),
    CONF_CHARGING_OVERCURRENT_PROTECTION: (0x45, 0.1, 2),
    CONF_DISCHARGING_OVERCURRENT_PROTECTION: (0x46, 0.1, 2),
    CONF_TEMPERATURE_HIGH_PROTECTION: (0x47, 0.1, 2),
    CONF_TEMPERATURE_LOW_PROTECTION: (0x48, 0.1, 2),
    CONF_TEMPERATURE_HIGH_WARNING: (0x49, 0.1, 2),
    CONF_TEMPERATURE_LOW_WARNING: (0x4A, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION: (0x4B, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_LOW_PROTECTION: (0x4C, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION: (0x4D, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION: (0x4E, 0.1, 2),
    CONF_BALANCING_VOLTAGE_DIFFERENCE: (0x4F, 0.001, 2),
    CONF_BALANCING_DELAY: (0x50, 1, 2),
    CONF_TOTAL_BATTERY_CAPACITY: (0x51, 1, 2),
    CONF_CHARGING_SHUTDOWN_DELAY: (0x52, 1, 2),
    CONF_DISCHARGING_SHUTDOWN_DELAY: (0x53, 1, 2),
    CONF_AUTO_BALANCING_ENABLE_TEMPERATURE: (0x54, 0.1, 2),
    CONF_AUTO_BALANCING_DISABLE_TEMPERATURE: (0x55, 0.1, 2),
    CONF_BALANCING_WORKING_TIME: (0x56, 1, 2),
    CONF_BALANCING_REST_TIME: (0x57, 1, 2),
    CONF_PRECHARGING_CURRENT: (0x58, 0.1, 2),
    CONF_PRECHARGING_TIME: (0x59, 1, 2),
}

JH02_REGISTERS = {
    CONF_SMART_SLEEP_VOLTAGE: (0x60, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_PROTECTION: (0x61, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_PROTECTION: (0x62, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_WARNING: (0x63, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_WARNING: (0x64, 0.001, 2),
    CONF_CHARGING_OVERCURRENT_PROTECTION: (0x65, 0.1, 2),
    CONF_DISCHARGING_OVERCURRENT_PROTECTION: (0x66, 0.1, 2),
    CONF_TEMPERATURE_HIGH_PROTECTION: (0x67, 0.1, 2),
    CONF_TEMPERATURE_LOW_PROTECTION: (0x68, 0.1, 2),
    CONF_TEMPERATURE_HIGH_WARNING: (0x69, 0.1, 2),
    CONF_TEMPERATURE_LOW_WARNING: (0x6A, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION: (0x6B, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_LOW_PROTECTION: (0x6C, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION: (0x6D, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION: (0x6E, 0.1, 2),
    CONF_BALANCING_VOLTAGE_DIFFERENCE: (0x6F, 0.001, 2),
    CONF_BALANCING_DELAY: (0x70, 1, 2),
    CONF_TOTAL_BATTERY_CAPACITY: (0x71, 1, 2),
    CONF_CHARGING_SHUTDOWN_DELAY: (0x72, 1, 2),
    CONF_DISCHARGING_SHUTDOWN_DELAY: (0x73, 1, 2),
    CONF_AUTO_BALANCING_ENABLE_TEMPERATURE: (0x74, 0.1, 2),
    CONF_AUTO_BALANCING_DISABLE_TEMPERATURE: (0x75, 0.1, 2),
    CONF_BALANCING_WORKING_TIME: (0x76, 1, 2),
    CONF_BALANCING_REST_TIME: (0x77, 1, 2),
    CONF_PRECHARGING_CURRENT: (0x78, 0.1, 2),
    CONF_PRECHARGING_TIME: (0x79, 1, 2),
}

JH03_REGISTERS = {
    CONF_SMART_SLEEP_VOLTAGE: (0x80, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_PROTECTION: (0x81, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_PROTECTION: (0x82, 0.001, 2),
    CONF_CELL_UNDERVOLTAGE_WARNING: (0x83, 0.001, 2),
    CONF_CELL_OVERVOLTAGE_WARNING: (0x84, 0.001, 2),
    CONF_CHARGING_OVERCURRENT_PROTECTION: (0x85, 0.1, 2),
    CONF_DISCHARGING_OVERCURRENT_PROTECTION: (0x86, 0.1, 2),
    CONF_TEMPERATURE_HIGH_PROTECTION: (0x87, 0.1, 2),
    CONF_TEMPERATURE_LOW_PROTECTION: (0x88, 0.1, 2),
    CONF_TEMPERATURE_HIGH_WARNING: (0x89, 0.1, 2),
    CONF_TEMPERATURE_LOW_WARNING: (0x8A, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION: (0x8B, 0.1, 2),
    CONF_CHARGING_TEMPERATURE_LOW_PROTECTION: (0x8C, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION: (0x8D, 0.1, 2),
    CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION: (0x8E, 0.1, 2),
    CONF_BALANCING_VOLTAGE_DIFFERENCE: (0x8F, 0.001, 2),
    CONF_BALANCING_DELAY: (0x90, 1, 2),
    CONF_TOTAL_BATTERY_CAPACITY: (0x91, 1, 2),
    CONF_CHARGING_SHUTDOWN_DELAY: (0x92, 1, 2),
    CONF_DISCHARGING_SHUTDOWN_DELAY: (0x93, 1, 2),
    CONF_AUTO_BALANCING_ENABLE_TEMPERATURE: (0x94, 0.1, 2),
    CONF_AUTO_BALANCING_DISABLE_TEMPERATURE: (0x95, 0.1, 2),
    CONF_BALANCING_WORKING_TIME: (0x96, 1, 2),
    CONF_BALANCING_REST_TIME: (0x97, 1, 2),
    CONF_PRECHARGING_CURRENT: (0x98, 0.1, 2),
    CONF_PRECHARGING_TIME: (0x99, 1, 2),
}

# 合并所有协议版本的寄存器定义
NUMBERS = {
    CONF_SMART_SLEEP_VOLTAGE: {
        "JH01": JH01_REGISTERS[CONF_SMART_SLEEP_VOLTAGE],
        "JH02": JH02_REGISTERS[CONF_SMART_SLEEP_VOLTAGE],
        "JH03": JH03_REGISTERS[CONF_SMART_SLEEP_VOLTAGE],
        "unit": UNIT_VOLT,
        "min_value": 2.0,
        "max_value": 3.5,
        "step": 0.01,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_CELL_UNDERVOLTAGE_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_CELL_UNDERVOLTAGE_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_CELL_UNDERVOLTAGE_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_CELL_UNDERVOLTAGE_PROTECTION],
        "unit": UNIT_VOLT,
        "min_value": 2.0,
        "max_value": 3.0,
        "step": 0.01,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_CELL_OVERVOLTAGE_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_CELL_OVERVOLTAGE_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_CELL_OVERVOLTAGE_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_CELL_OVERVOLTAGE_PROTECTION],
        "unit": UNIT_VOLT,
        "min_value": 3.6,
        "max_value": 4.3,
        "step": 0.01,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_CELL_UNDERVOLTAGE_WARNING: {
        "JH01": JH01_REGISTERS[CONF_CELL_UNDERVOLTAGE_WARNING],
        "JH02": JH02_REGISTERS[CONF_CELL_UNDERVOLTAGE_WARNING],
        "JH03": JH03_REGISTERS[CONF_CELL_UNDERVOLTAGE_WARNING],
        "unit": UNIT_VOLT,
        "min_value": 2.2,
        "max_value": 3.2,
        "step": 0.01,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_CELL_OVERVOLTAGE_WARNING: {
        "JH01": JH01_REGISTERS[CONF_CELL_OVERVOLTAGE_WARNING],
        "JH02": JH02_REGISTERS[CONF_CELL_OVERVOLTAGE_WARNING],
        "JH03": JH03_REGISTERS[CONF_CELL_OVERVOLTAGE_WARNING],
        "unit": UNIT_VOLT,
        "min_value": 3.5,
        "max_value": 4.2,
        "step": 0.01,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_CHARGING_OVERCURRENT_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_CHARGING_OVERCURRENT_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_CHARGING_OVERCURRENT_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_CHARGING_OVERCURRENT_PROTECTION],
        "unit": UNIT_AMPERE,
        "min_value": 5.0,
        "max_value": 200.0,
        "step": 0.1,
        "device_class": DEVICE_CLASS_CURRENT,
    },
    CONF_DISCHARGING_OVERCURRENT_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_DISCHARGING_OVERCURRENT_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_DISCHARGING_OVERCURRENT_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_DISCHARGING_OVERCURRENT_PROTECTION],
        "unit": UNIT_AMPERE,
        "min_value": 5.0,
        "max_value": 300.0,
        "step": 0.1,
        "device_class": DEVICE_CLASS_CURRENT,
    },
    CONF_TEMPERATURE_HIGH_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_TEMPERATURE_HIGH_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_TEMPERATURE_HIGH_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_TEMPERATURE_HIGH_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": 45.0,
        "max_value": 80.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_TEMPERATURE_LOW_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_TEMPERATURE_LOW_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_TEMPERATURE_LOW_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_TEMPERATURE_LOW_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": -30.0,
        "max_value": 10.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_TEMPERATURE_HIGH_WARNING: {
        "JH01": JH01_REGISTERS[CONF_TEMPERATURE_HIGH_WARNING],
        "JH02": JH02_REGISTERS[CONF_TEMPERATURE_HIGH_WARNING],
        "JH03": JH03_REGISTERS[CONF_TEMPERATURE_HIGH_WARNING],
        "unit": UNIT_CELSIUS,
        "min_value": 40.0,
        "max_value": 75.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_TEMPERATURE_LOW_WARNING: {
        "JH01": JH01_REGISTERS[CONF_TEMPERATURE_LOW_WARNING],
        "JH02": JH02_REGISTERS[CONF_TEMPERATURE_LOW_WARNING],
        "JH03": JH03_REGISTERS[CONF_TEMPERATURE_LOW_WARNING],
        "unit": UNIT_CELSIUS,
        "min_value": -25.0,
        "max_value": 15.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_CHARGING_TEMPERATURE_HIGH_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": 45.0,
        "max_value": 80.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_CHARGING_TEMPERATURE_LOW_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_CHARGING_TEMPERATURE_LOW_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_CHARGING_TEMPERATURE_LOW_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_CHARGING_TEMPERATURE_LOW_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": -30.0,
        "max_value": 10.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_DISCHARGING_TEMPERATURE_HIGH_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": 45.0,
        "max_value": 80.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION: {
        "JH01": JH01_REGISTERS[CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION],
        "JH02": JH02_REGISTERS[CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION],
        "JH03": JH03_REGISTERS[CONF_DISCHARGING_TEMPERATURE_LOW_PROTECTION],
        "unit": UNIT_CELSIUS,
        "min_value": -30.0,
        "max_value": 10.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_BALANCING_VOLTAGE_DIFFERENCE: {
        "JH01": JH01_REGISTERS[CONF_BALANCING_VOLTAGE_DIFFERENCE],
        "JH02": JH02_REGISTERS[CONF_BALANCING_VOLTAGE_DIFFERENCE],
        "JH03": JH03_REGISTERS[CONF_BALANCING_VOLTAGE_DIFFERENCE],
        "unit": UNIT_VOLT,
        "min_value": 0.001,
        "max_value": 0.1,
        "step": 0.001,
        "device_class": DEVICE_CLASS_VOLTAGE,
    },
    CONF_BALANCING_DELAY: {
        "JH01": JH01_REGISTERS[CONF_BALANCING_DELAY],
        "JH02": JH02_REGISTERS[CONF_BALANCING_DELAY],
        "JH03": JH03_REGISTERS[CONF_BALANCING_DELAY],
        "unit": UNIT_MINUTE,
        "min_value": 0,
        "max_value": 60,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_TOTAL_BATTERY_CAPACITY: {
        "JH01": JH01_REGISTERS[CONF_TOTAL_BATTERY_CAPACITY],
        "JH02": JH02_REGISTERS[CONF_TOTAL_BATTERY_CAPACITY],
        "JH03": JH03_REGISTERS[CONF_TOTAL_BATTERY_CAPACITY],
        "unit": UNIT_AMPERE_HOURS,
        "min_value": 1,
        "max_value": 1000,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_CHARGING_SHUTDOWN_DELAY: {
        "JH01": JH01_REGISTERS[CONF_CHARGING_SHUTDOWN_DELAY],
        "JH02": JH02_REGISTERS[CONF_CHARGING_SHUTDOWN_DELAY],
        "JH03": JH03_REGISTERS[CONF_CHARGING_SHUTDOWN_DELAY],
        "unit": UNIT_MINUTE,
        "min_value": 0,
        "max_value": 60,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_DISCHARGING_SHUTDOWN_DELAY: {
        "JH01": JH01_REGISTERS[CONF_DISCHARGING_SHUTDOWN_DELAY],
        "JH02": JH02_REGISTERS[CONF_DISCHARGING_SHUTDOWN_DELAY],
        "JH03": JH03_REGISTERS[CONF_DISCHARGING_SHUTDOWN_DELAY],
        "unit": UNIT_MINUTE,
        "min_value": 0,
        "max_value": 60,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_AUTO_BALANCING_ENABLE_TEMPERATURE: {
        "JH01": JH01_REGISTERS[CONF_AUTO_BALANCING_ENABLE_TEMPERATURE],
        "JH02": JH02_REGISTERS[CONF_AUTO_BALANCING_ENABLE_TEMPERATURE],
        "JH03": JH03_REGISTERS[CONF_AUTO_BALANCING_ENABLE_TEMPERATURE],
        "unit": UNIT_CELSIUS,
        "min_value": 0.0,
        "max_value": 40.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_AUTO_BALANCING_DISABLE_TEMPERATURE: {
        "JH01": JH01_REGISTERS[CONF_AUTO_BALANCING_DISABLE_TEMPERATURE],
        "JH02": JH02_REGISTERS[CONF_AUTO_BALANCING_DISABLE_TEMPERATURE],
        "JH03": JH03_REGISTERS[CONF_AUTO_BALANCING_DISABLE_TEMPERATURE],
        "unit": UNIT_CELSIUS,
        "min_value": 40.0,
        "max_value": 80.0,
        "step": 1.0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
    },
    CONF_BALANCING_WORKING_TIME: {
        "JH01": JH01_REGISTERS[CONF_BALANCING_WORKING_TIME],
        "JH02": JH02_REGISTERS[CONF_BALANCING_WORKING_TIME],
        "JH03": JH03_REGISTERS[CONF_BALANCING_WORKING_TIME],
        "unit": UNIT_MINUTE,
        "min_value": 1,
        "max_value": 60,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_BALANCING_REST_TIME: {
        "JH01": JH01_REGISTERS[CONF_BALANCING_REST_TIME],
        "JH02": JH02_REGISTERS[CONF_BALANCING_REST_TIME],
        "JH03": JH03_REGISTERS[CONF_BALANCING_REST_TIME],
        "unit": UNIT_MINUTE,
        "min_value": 1,
        "max_value": 60,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
    CONF_PRECHARGING_CURRENT: {
        "JH01": JH01_REGISTERS[CONF_PRECHARGING_CURRENT],
        "JH02": JH02_REGISTERS[CONF_PRECHARGING_CURRENT],
        "JH03": JH03_REGISTERS[CONF_PRECHARGING_CURRENT],
        "unit": UNIT_AMPERE,
        "min_value": 0.5,
        "max_value": 20.0,
        "step": 0.1,
        "device_class": DEVICE_CLASS_CURRENT,
    },
    CONF_PRECHARGING_TIME: {
        "JH01": JH01_REGISTERS[CONF_PRECHARGING_TIME],
        "JH02": JH02_REGISTERS[CONF_PRECHARGING_TIME],
        "JH03": JH03_REGISTERS[CONF_PRECHARGING_TIME],
        "unit": UNIT_SECOND,
        "min_value": 1,
        "max_value": 300,
        "step": 1,
        "device_class": DEVICE_CLASS_EMPTY,
    },
}

# 创建配置模式
CONFIG_SCHEMA = JH_BMS_ESP32_COMPONENT_SCHEMA.extend({})

# 为每个数值控制类型添加配置
for key, config in NUMBERS.items():
    CONFIG_SCHEMA = CONFIG_SCHEMA.extend(
        {
            cv.Optional(key): number.number_schema(
                JhNumber,
                unit_of_measurement=config["unit"],
                min_value=config["min_value"],
                max_value=config["max_value"],
                step=config["step"],
                device_class=config["device_class"],
                entity_category=ENTITY_CATEGORY_CONFIG,
            ),
        }
    )


async def to_code(config):
    # 获取组件实例
    hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    # 获取协议版本
    protocol_version = config.get("protocol_version", "JH01")
    # 遍历所有数值控制类型
    for key, number_config in NUMBERS.items():
        # 检查配置中是否有该数值控制
        if key in config:
            # 获取数值控制配置
            conf = config[key]
            # 创建数值控制组件
            var = cg.new_Pvariable(conf["id"])
            # 注册数值控制组件
            await number.register_number(
                var,
                conf,
                min_value=number_config["min_value"],
                max_value=number_config["max_value"],
                step=number_config["step"],
            )
            # 将数值控制添加到组件
            await cg.register_component(var, conf)
            # 设置数值控制的父组件
            cg.add(var.set_parent(hub))
            # 根据协议版本设置寄存器地址、因子和长度
            # 为了支持不同品牌的BMS，这里需要根据实际协议修改
            register_info = number_config.get(protocol_version, number_config["JH01"])
            register_address, factor, length = register_info
            cg.add(var.set_register(register_address))
            cg.add(var.set_factor(factor))
            cg.add(var.set_length(length))
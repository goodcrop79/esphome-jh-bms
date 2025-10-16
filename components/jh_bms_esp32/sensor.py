import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_CURRENT,
    CONF_POWER,
    CONF_TEMPERATURE,
    CONF_VOLTAGE,
    CONF_CAPACITY,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_WATT,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ICON_CURRENT_AC,
    ICON_FLASH,
    ICON_THERMOMETER,
    ICON_BATTERY,
)

# 定义组件需要但ESPHome中不存在的单位常量和图标常量
UNIT_AMPERE_HOURS = "Ah"
UNIT_CYCLE = "cycles"
ICON_VOLTAGE = "mdi:flash"

from . import JhBmsEsp32, CONF_JH_BMS_ESP32_ID

CODEOWNERS = ["@kqepup"]
DEPENDENCIES = ["jh_bms_esp32"]

# 传感器类型
CONF_TOTAL_VOLTAGE = "total_voltage"
CONF_SOC = "state_of_charge"
CONF_REMAINING_CAPACITY = "remaining_capacity"
CONF_CYCLE_COUNT = "cycle_count"
CONF_CELL_VOLTAGES = "cell_voltages"
CONF_TEMPERATURES = "temperatures"

# 定义所有传感器配置选项
SENSORS = {
    CONF_TOTAL_VOLTAGE: sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        icon=ICON_VOLTAGE,
    ),
    CONF_CURRENT: sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        icon=ICON_CURRENT_AC,
    ),
    CONF_POWER: sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_FLASH,
    ),
    CONF_SOC: sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_BATTERY,
        icon=ICON_BATTERY,
    ),
    CONF_REMAINING_CAPACITY: sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE_HOURS,
        accuracy_decimals=1,
        icon=ICON_BATTERY,
    ),
    CONF_CYCLE_COUNT: sensor.sensor_schema(
        unit_of_measurement=UNIT_CYCLE,
        accuracy_decimals=0,
        icon=ICON_FLASH,
    ),
    CONF_TEMPERATURES: [
        sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            icon=ICON_THERMOMETER,
        )
    ],
    CONF_CELL_VOLTAGES: [
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            icon=ICON_VOLTAGE,
        )
    ],
}

# 配置模式
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_JH_BMS_ESP32_ID): cv.use_id(JhBmsEsp32),
    cv.Optional(CONF_TOTAL_VOLTAGE): SENSORS[CONF_TOTAL_VOLTAGE],
    cv.Optional(CONF_CURRENT): SENSORS[CONF_CURRENT],
    cv.Optional(CONF_POWER): SENSORS[CONF_POWER],
    cv.Optional(CONF_SOC): SENSORS[CONF_SOC],
    cv.Optional(CONF_REMAINING_CAPACITY): SENSORS[CONF_REMAINING_CAPACITY],
    cv.Optional(CONF_CYCLE_COUNT): SENSORS[CONF_CYCLE_COUNT],
    cv.Optional(CONF_CELL_VOLTAGES): cv.ensure_list(SENSORS[CONF_CELL_VOLTAGES][0]),
    cv.Optional(CONF_TEMPERATURES): cv.ensure_list(SENSORS[CONF_TEMPERATURES][0]),
})

# 代码生成
async def to_code(config):
    # 获取JH BMS ESP32组件
    parent = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    
    # 处理基本传感器
    if CONF_TOTAL_VOLTAGE in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_VOLTAGE])
        cg.add(parent.set_total_voltage_sensor(sens))
    
    if CONF_CURRENT in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT])
        cg.add(parent.set_current_sensor(sens))
    
    if CONF_POWER in config:
        sens = await sensor.new_sensor(config[CONF_POWER])
        cg.add(parent.set_power_sensor(sens))
    
    if CONF_SOC in config:
        sens = await sensor.new_sensor(config[CONF_SOC])
        cg.add(parent.set_soc_sensor(sens))
    
    if CONF_REMAINING_CAPACITY in config:
        sens = await sensor.new_sensor(config[CONF_REMAINING_CAPACITY])
        cg.add(parent.set_remaining_capacity_sensor(sens))
    
    if CONF_CYCLE_COUNT in config:
        sens = await sensor.new_sensor(config[CONF_CYCLE_COUNT])
        cg.add(parent.set_cycle_count_sensor(sens))
    
    # 处理单体电压传感器
    if CONF_CELL_VOLTAGES in config:
        for conf in config[CONF_CELL_VOLTAGES]:
            sens = await sensor.new_sensor(conf)
            cg.add(parent.add_cell_voltage_sensor(sens))
    
    # 处理温度传感器
    if CONF_TEMPERATURES in config:
        for conf in config[CONF_TEMPERATURES]:
            sens = await sensor.new_sensor(conf)
            cg.add(parent.add_temperature_sensor(sens))
CONF_CELL_RESISTANCE_13 = "cell_resistance_13"
CONF_CELL_RESISTANCE_14 = "cell_resistance_14"
CONF_CELL_RESISTANCE_15 = "cell_resistance_15"
CONF_CELL_RESISTANCE_16 = "cell_resistance_16"
CONF_CELL_RESISTANCE_17 = "cell_resistance_17"
CONF_CELL_RESISTANCE_18 = "cell_resistance_18"
CONF_CELL_RESISTANCE_19 = "cell_resistance_19"
CONF_CELL_RESISTANCE_20 = "cell_resistance_20"
CONF_CELL_RESISTANCE_21 = "cell_resistance_21"
CONF_CELL_RESISTANCE_22 = "cell_resistance_22"
CONF_CELL_RESISTANCE_23 = "cell_resistance_23"
CONF_CELL_RESISTANCE_24 = "cell_resistance_24"
CONF_CELL_RESISTANCE_25 = "cell_resistance_25"
CONF_CELL_RESISTANCE_26 = "cell_resistance_26"
CONF_CELL_RESISTANCE_27 = "cell_resistance_27"
CONF_CELL_RESISTANCE_28 = "cell_resistance_28"
CONF_CELL_RESISTANCE_29 = "cell_resistance_29"
CONF_CELL_RESISTANCE_30 = "cell_resistance_30"
CONF_CELL_RESISTANCE_31 = "cell_resistance_31"
CONF_CELL_RESISTANCE_32 = "cell_resistance_32"

# 单体电阻传感器配置（添加缺失的前12个）
CONF_CELL_RESISTANCE_1 = "cell_resistance_1"
CONF_CELL_RESISTANCE_2 = "cell_resistance_2"
CONF_CELL_RESISTANCE_3 = "cell_resistance_3"
CONF_CELL_RESISTANCE_4 = "cell_resistance_4"
CONF_CELL_RESISTANCE_5 = "cell_resistance_5"
CONF_CELL_RESISTANCE_6 = "cell_resistance_6"
CONF_CELL_RESISTANCE_7 = "cell_resistance_7"
CONF_CELL_RESISTANCE_8 = "cell_resistance_8"
CONF_CELL_RESISTANCE_9 = "cell_resistance_9"
CONF_CELL_RESISTANCE_10 = "cell_resistance_10"
CONF_CELL_RESISTANCE_11 = "cell_resistance_11"
CONF_CELL_RESISTANCE_12 = "cell_resistance_12"

# 其他传感器配置
CONF_BALANCING = "balancing"
CONF_MIN_CELL_VOLTAGE = "min_cell_voltage"
CONF_MAX_CELL_VOLTAGE = "max_cell_voltage"
CONF_MIN_VOLTAGE_CELL = "min_voltage_cell"
CONF_MAX_VOLTAGE_CELL = "max_voltage_cell"
CONF_DELTA_CELL_VOLTAGE = "delta_cell_voltage"
CONF_AVERAGE_CELL_VOLTAGE = "average_cell_voltage"
CONF_TOTAL_VOLTAGE = "total_voltage"
CONF_CURRENT = "current"
CONF_POWER = "power"
CONF_CHARGING_POWER = "charging_power"
CONF_DISCHARGING_POWER = "discharging_power"
CONF_POWER_TUBE_TEMPERATURE = "power_tube_temperature"
CONF_STATE_OF_CHARGE = "state_of_charge"
CONF_CAPACITY_REMAINING = "capacity_remaining"
CONF_TOTAL_BATTERY_CAPACITY_SETTING = "total_battery_capacity_setting"

# 单体电压传感器配置
CONF_CELL_VOLTAGE_1 = "cell_voltage_1"
CONF_CELL_VOLTAGE_2 = "cell_voltage_2"
CONF_CELL_VOLTAGE_3 = "cell_voltage_3"
CONF_CELL_VOLTAGE_4 = "cell_voltage_4"
CONF_CELL_VOLTAGE_5 = "cell_voltage_5"
CONF_CELL_VOLTAGE_6 = "cell_voltage_6"
CONF_CELL_VOLTAGE_7 = "cell_voltage_7"
CONF_CELL_VOLTAGE_8 = "cell_voltage_8"
CONF_CELL_VOLTAGE_9 = "cell_voltage_9"
CONF_CELL_VOLTAGE_10 = "cell_voltage_10"
CONF_CELL_VOLTAGE_11 = "cell_voltage_11"
CONF_CELL_VOLTAGE_12 = "cell_voltage_12"
CONF_CELL_VOLTAGE_13 = "cell_voltage_13"
CONF_CELL_VOLTAGE_14 = "cell_voltage_14"
CONF_CELL_VOLTAGE_15 = "cell_voltage_15"
CONF_CELL_VOLTAGE_16 = "cell_voltage_16"
CONF_CELL_VOLTAGE_17 = "cell_voltage_17"
CONF_CELL_VOLTAGE_18 = "cell_voltage_18"
CONF_CELL_VOLTAGE_19 = "cell_voltage_19"
CONF_CELL_VOLTAGE_20 = "cell_voltage_20"
CONF_CELL_VOLTAGE_21 = "cell_voltage_21"
CONF_CELL_VOLTAGE_22 = "cell_voltage_22"
CONF_CELL_VOLTAGE_23 = "cell_voltage_23"
CONF_CELL_VOLTAGE_24 = "cell_voltage_24"
CONF_CELL_VOLTAGE_25 = "cell_voltage_25"
CONF_CELL_VOLTAGE_26 = "cell_voltage_26"
CONF_CELL_VOLTAGE_27 = "cell_voltage_27"
CONF_CELL_VOLTAGE_28 = "cell_voltage_28"
CONF_CELL_VOLTAGE_29 = "cell_voltage_29"
CONF_CELL_VOLTAGE_30 = "cell_voltage_30"
CONF_CELL_VOLTAGE_31 = "cell_voltage_31"
CONF_CELL_VOLTAGE_32 = "cell_voltage_32"

# 其他电池参数传感器
CONF_TOTAL_VOLTAGE = "total_voltage"
CONF_CHARGING_POWER = "charging_power"
CONF_DISCHARGING_POWER = "discharging_power"
CONF_TEMPERATURE_SENSOR_1 = "temperature_sensor_1"
CONF_TEMPERATURE_SENSOR_2 = "temperature_sensor_2"
CONF_TEMPERATURE_SENSOR_3 = "temperature_sensor_3"
CONF_TEMPERATURE_SENSOR_4 = "temperature_sensor_4"
CONF_TEMPERATURE_SENSOR_5 = "temperature_sensor_5"
CONF_POWER_TUBE_TEMPERATURE = "power_tube_temperature"
CONF_STATE_OF_CHARGE = "state_of_charge"
CONF_CAPACITY_REMAINING = "capacity_remaining"
CONF_TOTAL_BATTERY_CAPACITY_SETTING = "total_battery_capacity_setting"
CONF_CHARGING_CYCLES = "charging_cycles"
CONF_TOTAL_CHARGING_CYCLE_CAPACITY = "total_charging_cycle_capacity"
CONF_TOTAL_RUNTIME = "total_runtime"
CONF_BALANCING_CURRENT = "balancing_current"
CONF_ERRORS_BITMASK = "errors_bitmask"
CONF_EMERGENCY_TIME_COUNTDOWN = "emergency_time_countdown"
CONF_HEATING_CURRENT = "heating_current"
CONF_CHARGE_STATUS_ID = "charge_status_id"
CONF_CHARGE_STATUS_TIME_ELAPSED = "charge_status_time_elapsed"

# 自定义单位定义
UNIT_AMPERE_HOURS = "Ah"
UNIT_OHM = "Ω"
UNIT_SECONDS = "s"

# 传感器图标定义
ICON_CURRENT_DC = "mdi:current-dc"
ICON_CAPACITY = "mdi:battery-medium"
ICON_MIN_VOLTAGE_CELL = "mdi:battery-minus-outline"
ICON_MAX_VOLTAGE_CELL = "mdi:battery-plus-outline"
ICON_CAPACITY_REMAINING = "mdi:battery-50"
ICON_CHARGING_CYCLES = "mdi:battery-sync"
ICON_ERRORS_BITMASK = "mdi:alert-circle-outline"
ICON_CELL_RESISTANCE = "mdi:omega"
ICON_BALANCER = "mdi:seesaw"
ICON_CHARGE_STATUS_ID = "mdi:battery-clock"
ICON_CHARGE_STATUS_TIME_ELAPSED = "mdi:timer-outline"

# 单体电压传感器列表
CELL_VOLTAGES = [
    CONF_CELL_VOLTAGE_1,
    CONF_CELL_VOLTAGE_2,
    CONF_CELL_VOLTAGE_3,
    CONF_CELL_VOLTAGE_4,
    CONF_CELL_VOLTAGE_5,
    CONF_CELL_VOLTAGE_6,
    CONF_CELL_VOLTAGE_7,
    CONF_CELL_VOLTAGE_8,
    CONF_CELL_VOLTAGE_9,
    CONF_CELL_VOLTAGE_10,
    CONF_CELL_VOLTAGE_11,
    CONF_CELL_VOLTAGE_12,
    CONF_CELL_VOLTAGE_13,
    CONF_CELL_VOLTAGE_14,
    CONF_CELL_VOLTAGE_15,
    CONF_CELL_VOLTAGE_16,
    CONF_CELL_VOLTAGE_17,
    CONF_CELL_VOLTAGE_18,
    CONF_CELL_VOLTAGE_19,
    CONF_CELL_VOLTAGE_20,
    CONF_CELL_VOLTAGE_21,
    CONF_CELL_VOLTAGE_22,
    CONF_CELL_VOLTAGE_23,
    CONF_CELL_VOLTAGE_24,
    CONF_CELL_VOLTAGE_25,
    CONF_CELL_VOLTAGE_26,
    CONF_CELL_VOLTAGE_27,
    CONF_CELL_VOLTAGE_28,
    CONF_CELL_VOLTAGE_29,
    CONF_CELL_VOLTAGE_30,
    CONF_CELL_VOLTAGE_31,
    CONF_CELL_VOLTAGE_32,
]

# 单体电阻传感器列表
CELL_RESISTANCES = [
    CONF_CELL_RESISTANCE_1,
    CONF_CELL_RESISTANCE_2,
    CONF_CELL_RESISTANCE_3,
    CONF_CELL_RESISTANCE_4,
    CONF_CELL_RESISTANCE_5,
    CONF_CELL_RESISTANCE_6,
    CONF_CELL_RESISTANCE_7,
    CONF_CELL_RESISTANCE_8,
    CONF_CELL_RESISTANCE_9,
    CONF_CELL_RESISTANCE_10,
    CONF_CELL_RESISTANCE_11,
    CONF_CELL_RESISTANCE_12,
    CONF_CELL_RESISTANCE_13,
    CONF_CELL_RESISTANCE_14,
    CONF_CELL_RESISTANCE_15,
    CONF_CELL_RESISTANCE_16,
    CONF_CELL_RESISTANCE_17,
    CONF_CELL_RESISTANCE_18,
    CONF_CELL_RESISTANCE_19,
    CONF_CELL_RESISTANCE_20,
    CONF_CELL_RESISTANCE_21,
    CONF_CELL_RESISTANCE_22,
    CONF_CELL_RESISTANCE_23,
    CONF_CELL_RESISTANCE_24,
    CONF_CELL_RESISTANCE_25,
    CONF_CELL_RESISTANCE_26,
    CONF_CELL_RESISTANCE_27,
    CONF_CELL_RESISTANCE_28,
    CONF_CELL_RESISTANCE_29,
    CONF_CELL_RESISTANCE_30,
    CONF_CELL_RESISTANCE_31,
    CONF_CELL_RESISTANCE_32,
]

# 温度传感器列表
TEMPERATURES = [
    CONF_TEMPERATURE_SENSOR_1,
    CONF_TEMPERATURE_SENSOR_2,
    CONF_TEMPERATURE_SENSOR_3,
    CONF_TEMPERATURE_SENSOR_4,
    CONF_TEMPERATURE_SENSOR_5,
]

# 其他传感器列表
SENSORS = [
    CONF_BALANCING,
    CONF_MIN_CELL_VOLTAGE,
    CONF_MAX_CELL_VOLTAGE,
    CONF_MIN_VOLTAGE_CELL,
    CONF_MAX_VOLTAGE_CELL,
    CONF_DELTA_CELL_VOLTAGE,
    CONF_AVERAGE_CELL_VOLTAGE,
    CONF_TOTAL_VOLTAGE,
    CONF_CURRENT,
    CONF_POWER,
    CONF_CHARGING_POWER,
    CONF_DISCHARGING_POWER,
    CONF_POWER_TUBE_TEMPERATURE,
    CONF_STATE_OF_CHARGE,
    CONF_CAPACITY_REMAINING,
    CONF_TOTAL_BATTERY_CAPACITY_SETTING,
    CONF_CHARGING_CYCLES,
    CONF_TOTAL_CHARGING_CYCLE_CAPACITY,
    CONF_TOTAL_RUNTIME,
    CONF_BALANCING_CURRENT,
    CONF_ERRORS_BITMASK,
    CONF_EMERGENCY_TIME_COUNTDOWN,
    CONF_HEATING_CURRENT,
    CONF_CHARGE_STATUS_ID,
    CONF_CHARGE_STATUS_TIME_ELAPSED,
]

# 定义配置模式
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(
    {
        # 均衡状态传感器
        cv.Optional(CONF_BALANCING): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_BALANCER,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 最小单体电压传感器
        cv.Optional(CONF_MIN_CELL_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 最大单体电压传感器
        cv.Optional(CONF_MAX_CELL_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 最小电压单体编号传感器
        cv.Optional(CONF_MIN_VOLTAGE_CELL): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_MIN_VOLTAGE_CELL,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 最大电压单体编号传感器
        cv.Optional(CONF_MAX_VOLTAGE_CELL): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_MAX_VOLTAGE_CELL,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 单体电压差传感器
        cv.Optional(CONF_DELTA_CELL_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # 平均单体电压传感器
        cv.Optional(CONF_AVERAGE_CELL_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# 为每个单体电压传感器添加配置
for i in range(1, 33):
    CONFIG_SCHEMA = CONFIG_SCHEMA.extend({
        cv.Optional(f"cell_voltage_{i}"): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    })

# 为每个单体电阻传感器添加配置
for i in range(1, 33):
    CONFIG_SCHEMA = CONFIG_SCHEMA.extend({
        cv.Optional(f"cell_resistance_{i}"): sensor.sensor_schema(
            unit_of_measurement=UNIT_OHM,
            icon=ICON_CELL_RESISTANCE,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    })

# 添加剩余传感器的配置
CONFIG_SCHEMA = CONFIG_SCHEMA.extend({
    # 总电压传感器
    cv.Optional(CONF_TOTAL_VOLTAGE): sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        icon=ICON_EMPTY,
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 电流传感器
    cv.Optional(CONF_CURRENT): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        icon=ICON_CURRENT_DC,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 功率传感器
    cv.Optional(CONF_POWER): sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 充电功率传感器
    cv.Optional(CONF_CHARGING_POWER): sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 放电功率传感器
    cv.Optional(CONF_DISCHARGING_POWER): sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 温度传感器配置
    cv.Optional(CONF_TEMPERATURE_SENSOR_1): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_TEMPERATURE_SENSOR_2): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_TEMPERATURE_SENSOR_3): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_TEMPERATURE_SENSOR_4): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_TEMPERATURE_SENSOR_5): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 功率管温度传感器
    cv.Optional(CONF_POWER_TUBE_TEMPERATURE): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_EMPTY,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 荷电状态传感器
    cv.Optional(CONF_STATE_OF_CHARGE): sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_BATTERY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 剩余容量传感器
    cv.Optional(CONF_CAPACITY_REMAINING): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE_HOURS,
        icon=ICON_CAPACITY_REMAINING,
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 电池总容量设置传感器
    cv.Optional(CONF_TOTAL_BATTERY_CAPACITY_SETTING): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE_HOURS,
        icon=ICON_EMPTY,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 充电循环次数传感器
    cv.Optional(CONF_CHARGING_CYCLES): sensor.sensor_schema(
        unit_of_measurement=UNIT_EMPTY,
        icon=ICON_CHARGING_CYCLES,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 总充电循环容量传感器
    cv.Optional(CONF_TOTAL_CHARGING_CYCLE_CAPACITY): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE_HOURS,
        icon=ICON_COUNTER,
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 总运行时间传感器
    cv.Optional(CONF_TOTAL_RUNTIME): sensor.sensor_schema(
        unit_of_measurement=UNIT_SECONDS,
        icon=ICON_TIMELAPSE,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    # 均衡电流传感器
    cv.Optional(CONF_BALANCING_CURRENT): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        icon=ICON_CURRENT_DC,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 错误位掩码传感器
    cv.Optional(CONF_ERRORS_BITMASK): sensor.sensor_schema(
        unit_of_measurement=UNIT_EMPTY,
        icon=ICON_ERRORS_BITMASK,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 紧急时间倒计时传感器
    cv.Optional(CONF_EMERGENCY_TIME_COUNTDOWN): sensor.sensor_schema(
        unit_of_measurement=UNIT_SECONDS,
        icon=ICON_TIMELAPSE,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
    ),
    # 加热电流传感器
    cv.Optional(CONF_HEATING_CURRENT): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        icon=ICON_CURRENT_DC,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # 充电状态ID传感器
    cv.Optional(CONF_CHARGE_STATUS_ID): sensor.sensor_schema(
        unit_of_measurement=UNIT_EMPTY,
        icon=ICON_CHARGE_STATUS_ID,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
    ),
    # 充电状态经过时间传感器
    cv.Optional(CONF_CHARGE_STATUS_TIME_ELAPSED): sensor.sensor_schema(
        unit_of_measurement=UNIT_SECONDS,
        icon=ICON_CHARGE_STATUS_TIME_ELAPSED,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_EMPTY,
    ),
})


async def to_code(config):
    # 获取组件实例 - 处理CONF_JH_BMS_ESP32_ID为可选配置的情况
    if CONF_JH_BMS_ESP32_ID in config:
        hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
        # 注册单体电压传感器
        for i, key in enumerate(CELL_VOLTAGES):
            if key in config:
                conf = config[key]
                sens = await sensor.new_sensor(conf)
                cg.add(hub.set_cell_voltage_sensor(i, sens))
        # 注册单体电阻传感器
        for i, key in enumerate(CELL_RESISTANCES):
            if key in config:
                conf = config[key]
                sens = await sensor.new_sensor(conf)
                cg.add(hub.set_cell_resistance_sensor(i, sens))
        # 注册温度传感器
        for i, key in enumerate(TEMPERATURES):
            if key in config:
                conf = config[key]
                sens = await sensor.new_sensor(conf)
                cg.add(hub.set_temperature_sensor(i, sens))
        # 注册其他传感器
        for key in SENSORS:
            if key in config:
                conf = config[key]
                sens = await sensor.new_sensor(conf)
                cg.add(getattr(hub, f"set_{key}_sensor")(sens))
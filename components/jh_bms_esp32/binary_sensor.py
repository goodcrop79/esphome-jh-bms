import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_HEAT,
    ICON_BATTERY_CHARGING,
    ICON_POWER,
    ICON_THERMOMETER,
    ICON_EMPTY,
)

# 自定义设备类常量
DEVICE_CLASS_CHARGING = ""

from . import CONF_JH_BMS_ESP32_ID

CODEOWNERS = ["@kqepup"]
DEPENDENCIES = ["jh_bms_esp32"]

# 定义配置键
CONF_CHARGING_STATUS = "charging_status"
CONF_DISCHARGING_STATUS = "discharging_status"
CONF_BALANCE_STATE = "balance_state"
CONF_ONLINE_STATUS = "online_status"
CONF_HEATING_STATUS = "heating_status"
CONF_CHARGING_MOS_STATUS = "charging_mos_status"
CONF_DISCHARGING_MOS_STATUS = "discharging_mos_status"

# 定义二进制传感器配置
BINARY_SENSORS = {
    CONF_CHARGING_STATUS: binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_CHARGING,
        icon=ICON_BATTERY_CHARGING,
    ),
    CONF_DISCHARGING_STATUS: binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_POWER,
    ),
    CONF_BALANCE_STATE: binary_sensor.binary_sensor_schema(
        icon=ICON_EMPTY,
    ),
    CONF_ONLINE_STATUS: binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_CONNECTIVITY,
        icon=ICON_EMPTY,
    ),
    CONF_HEATING_STATUS: binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_HEAT,
        icon=ICON_THERMOMETER,
    ),
    CONF_CHARGING_MOS_STATUS: binary_sensor.binary_sensor_schema(
        icon=ICON_EMPTY,
    ),
    CONF_DISCHARGING_MOS_STATUS: binary_sensor.binary_sensor_schema(
        icon=ICON_EMPTY,
    ),
}

# 配置模式
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_JH_BMS_ESP32_ID): cv.use_id(cg.Component),
    cv.Optional(CONF_CHARGING_STATUS): BINARY_SENSORS[CONF_CHARGING_STATUS],
    cv.Optional(CONF_DISCHARGING_STATUS): BINARY_SENSORS[CONF_DISCHARGING_STATUS],
    cv.Optional(CONF_BALANCE_STATE): BINARY_SENSORS[CONF_BALANCE_STATE],
    cv.Optional(CONF_ONLINE_STATUS): BINARY_SENSORS[CONF_ONLINE_STATUS],
    cv.Optional(CONF_HEATING_STATUS): BINARY_SENSORS[CONF_HEATING_STATUS],
    cv.Optional(CONF_CHARGING_MOS_STATUS): BINARY_SENSORS[CONF_CHARGING_MOS_STATUS],
    cv.Optional(CONF_DISCHARGING_MOS_STATUS): BINARY_SENSORS[CONF_DISCHARGING_MOS_STATUS],
})

# 代码生成
async def to_code(config):
    # 获取JH BMS ESP32组件
    parent = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    
    # 处理所有二进制传感器
    if CONF_CHARGING_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_STATUS])
        cg.add(parent.set_charging_status_binary_sensor(sens))
    
    if CONF_DISCHARGING_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_DISCHARGING_STATUS])
        cg.add(parent.set_discharging_status_binary_sensor(sens))
    
    if CONF_BALANCE_STATE in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_BALANCE_STATE])
        cg.add(parent.set_balance_state_binary_sensor(sens))
    
    if CONF_ONLINE_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_ONLINE_STATUS])
        cg.add(parent.set_online_status_binary_sensor(sens))
    
    if CONF_HEATING_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_HEATING_STATUS])
        cg.add(parent.set_heating_status_binary_sensor(sens))
    
    if CONF_CHARGING_MOS_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_MOS_STATUS])
        cg.add(parent.set_charging_mos_status_binary_sensor(sens))
    
    if CONF_DISCHARGING_MOS_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_DISCHARGING_MOS_STATUS])
        cg.add(parent.set_discharging_mos_status_binary_sensor(sens))
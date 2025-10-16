import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID, DEVICE_CLASS_CONNECTIVITY, ENTITY_CATEGORY_DIAGNOSTIC

from . import CONF_JH_BMS_ESP32_ID, JH_BMS_ESP32_COMPONENT_SCHEMA
from .const import CONF_BALANCING, CONF_CHARGING, CONF_DISCHARGING, CONF_HEATING

DEPENDENCIES = ["jh_bms_esp32"]

CODEOWNERS = ["@syssi", "@txubelaxu"]

# 新增的二进制传感器配置项
CONF_ONLINE_STATUS = "online_status"
CONF_DRY_CONTACT_1 = "dry_contact_1"
CONF_DRY_CONTACT_2 = "dry_contact_2"

# 传感器图标定义
ICON_CHARGING = "mdi:battery-charging"
ICON_DISCHARGING = "mdi:power-plug"
ICON_BALANCING = "mdi:battery-heart-variant"
ICON_HEATING = "mdi:radiator"
ICON_DRY_CONTACT_1 = "mdi:alarm-bell"
ICON_DRY_CONTACT_2 = "mdi:alarm-bell"

# 定义支持的二进制传感器列表
BINARY_SENSORS = [
    CONF_CHARGING,
    CONF_DISCHARGING,
    CONF_BALANCING,
    CONF_ONLINE_STATUS,
    CONF_HEATING,
    CONF_DRY_CONTACT_1,
    CONF_DRY_CONTACT_2,
]

# 定义配置模式
CONFIG_SCHEMA = JH_BMS_ESP32_COMPONENT_SCHEMA.extend(
    {
        # 充电状态传感器
        cv.Optional(CONF_CHARGING): binary_sensor.binary_sensor_schema(
            icon=ICON_CHARGING
        ),
        # 放电状态传感器
        cv.Optional(CONF_DISCHARGING): binary_sensor.binary_sensor_schema(
            icon=ICON_DISCHARGING
        ),
        # 均衡状态传感器
        cv.Optional(CONF_BALANCING): binary_sensor.binary_sensor_schema(
            icon=ICON_BALANCING
        ),
        # 加热状态传感器
        cv.Optional(CONF_HEATING): binary_sensor.binary_sensor_schema(
            icon=ICON_HEATING
        ),
        # 干接点1状态传感器
        cv.Optional(CONF_DRY_CONTACT_1): binary_sensor.binary_sensor_schema(
            icon=ICON_DRY_CONTACT_1
        ),
        # 干接点2状态传感器
        cv.Optional(CONF_DRY_CONTACT_2): binary_sensor.binary_sensor_schema(
            icon=ICON_DRY_CONTACT_2
        ),
        # 在线状态传感器
        cv.Optional(CONF_ONLINE_STATUS): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_CONNECTIVITY,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
    }
)


async def to_code(config):
    # 获取组件实例 - 处理CONF_JH_BMS_ESP32_ID为可选配置的情况
    if CONF_JH_BMS_ESP32_ID in config:
        hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
        # 为每个配置的传感器创建和注册实例
        for key in BINARY_SENSORS:
            if key in config:
                conf = config[key]
                sens = cg.new_Pvariable(conf[CONF_ID])
                await binary_sensor.register_binary_sensor(sens, conf)
                # 将传感器添加到主组件
                cg.add(getattr(hub, f"set_{key}_binary_sensor")(sens))
import esphome.codegen as cg
from esphome.components import text_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID

from . import CONF_JH_BMS_ESP32_ID, JH_BMS_ESP32_COMPONENT_SCHEMA

# 为ESPHome 2025.9.3及更高版本定义缺失的常量
try:
    from esphome.const import ICON_TIMELAPSE
except ImportError:
    ICON_TIMELAPSE = "mdi:timelapse"

DEPENDENCIES = ["jh_bms_esp32"]

CODEOWNERS = ["@syssi", "@txubelaxu"]

# 文本传感器配置项
CONF_ERRORS = "errors"
CONF_OPERATION_STATUS = "operation_status"
CONF_TOTAL_RUNTIME_FORMATTED = "total_runtime_formatted"
CONF_CHARGE_STATUS = "charge_status"

# 传感器图标定义
ICON_ERRORS = "mdi:alert-circle-outline"
ICON_OPERATION_STATUS = "mdi:heart-pulse"
ICON_CHARGE_STATUS = "mdi:battery-clock"

# 定义支持的文本传感器列表
TEXT_SENSORS = [
    CONF_ERRORS,
    CONF_OPERATION_STATUS,
    CONF_TOTAL_RUNTIME_FORMATTED,
    CONF_CHARGE_STATUS,
]

# 定义配置模式
CONFIG_SCHEMA = JH_BMS_ESP32_COMPONENT_SCHEMA.extend(
    {
        # 错误信息文本传感器
        cv.Optional(CONF_ERRORS): text_sensor.text_sensor_schema(
            text_sensor.TextSensor, icon=ICON_ERRORS
        ),
        # 操作状态文本传感器
        cv.Optional(CONF_OPERATION_STATUS): text_sensor.text_sensor_schema(
            text_sensor.TextSensor, icon=ICON_OPERATION_STATUS
        ),
        # 格式化的总运行时间文本传感器
        cv.Optional(CONF_TOTAL_RUNTIME_FORMATTED): text_sensor.text_sensor_schema(
            text_sensor.TextSensor, icon=ICON_TIMELAPSE
        ),
        # 充电状态文本传感器
        cv.Optional(CONF_CHARGE_STATUS): text_sensor.text_sensor_schema(
            text_sensor.TextSensor, icon=ICON_CHARGE_STATUS
        ),
    }
)


async def to_code(config):
    # 获取组件实例 - 处理CONF_JH_BMS_ESP32_ID为可选配置的情况
    if CONF_JH_BMS_ESP32_ID in config:
        hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
        # 为每个配置的文本传感器创建和注册实例
        for key in TEXT_SENSORS:
            if key in config:
                conf = config[key]
                sens = cg.new_Pvariable(conf[CONF_ID])
                await text_sensor.register_text_sensor(sens, conf)
                # 将传感器添加到主组件
                cg.add(getattr(hub, f"set_{key}_text_sensor")(sens))
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import (
    ICON_ERROR,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

# 导入组件
from . import CONF_JH_BMS_ESP32_ID

CODEOWNERS = ["@kqepup"]
DEPENDENCIES = ["jh_bms_esp32"]

# 文本传感器配置键
CONF_ERROR_INFO = "error_info"

# 定义文本传感器配置架构
TEXT_SENSOR_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_JH_BMS_ESP32_ID): cv.use_id(cg.Component),
    cv.Optional(CONF_ERROR_INFO): text_sensor.text_sensor_schema(
        icon=ICON_ERROR,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
})

# 注册平台
async def to_code(config):
    parent = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    
    # 设置错误信息文本传感器
    if CONF_ERROR_INFO in config:
        sens = await text_sensor.new_text_sensor(config[CONF_ERROR_INFO])
        cg.add(parent.set_error_info_text_sensor(sens))

# 导出配置架构
CONFIG_SCHEMA = TEXT_SENSOR_SCHEMA
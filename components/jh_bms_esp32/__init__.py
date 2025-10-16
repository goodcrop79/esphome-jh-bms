import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import (
    CONF_ID,
    CONF_UPDATE_INTERVAL,
)

# 定义命名空间
AUTO_LOAD = ["sensor", "binary_sensor", "text_sensor"]
CODEOWNERS = ["@kqepup"]
DEPENDENCIES = ["uart"]

# 组件命名空间
jh_bms_esp32_ns = cg.esphome_ns.namespace("jh_bms_esp32")

# 定义JhBmsEsp32类
JhBmsEsp32 = jh_bms_esp32_ns.class_("JhBmsEsp32", cg.Component, uart.UARTDevice)

# 组件配置键
CONF_JH_BMS_ESP32_ID = "jh_bms_esp32_id"
CONF_BMS_VERSION = "bms_version"

# 配置模式
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(JhBmsEsp32),
    cv.Optional(CONF_BMS_VERSION, default=1): cv.int_range(min=1, max=2),
    cv.Optional(CONF_UPDATE_INTERVAL, default="1s"): cv.update_interval,
}).extend(uart.UART_DEVICE_SCHEMA)

# 代码生成函数
async def to_code(config):
    # 获取UART组件
    uart_component = await cg.get_variable(config[uart.CONF_UART_ID])
    
    # 创建组件实例，传递UART组件
    var = cg.new_Pvariable(config[CONF_ID], uart_component)
    
    # 注册组件
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    
    # 设置BMS版本
    cg.add(var.set_bms_version(config[CONF_BMS_VERSION]))
    
    # 设置更新间隔
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL].total_milliseconds()))

# 导入子组件
from . import sensor, binary_sensor, text_sensor

# 导出必要的配置
__all__ = ["CONF_JH_BMS_ESP32_ID", "JhBmsEsp32", "CONFIG_SCHEMA"]
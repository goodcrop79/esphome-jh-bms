import esphome.codegen as cg
from esphome.components import button
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_DIAGNOSTIC,
    ENTITY_CATEGORY_CONFIG,
    ICON_FILE_FIND,
    ICON_BATTERY_PLUS,
    ICON_BATTERY_MINUS,
    ICON_RESTART,
    ICON_CIRCLE_SLICE_8,
    ICON_RELOAD,
)

# 为ESPHome 2025.9.3及更高版本定义缺失的常量
try:
    from esphome.const import ICON_SEARCH
except ImportError:
    ICON_SEARCH = "mdi:search"

from .. import (
    CONF_JH_BMS_ESP32_ID,
    JH_BMS_ESP32_COMPONENT_SCHEMA,
    jh_bms_esp32_ns,
)

# 为了支持不同品牌的BMS，这里需要修改命令码和通信协议
DEPENDENCIES = ["jh_bms_esp32"]

CODEOWNERS = ["@syssi", "@txubelaxu"]

JhButton = jh_bms_esp32_ns.class_("JhButton", button.Button, cg.Component)

# 定义按钮类型常量
CONF_SET_RETRIEVE = "set_retrieve"
CONF_DEVICE_INFO_RETRIEVE = "device_info_retrieve"
CONF_READ_BATTERY_PARAMS = "read_battery_params"
CONF_READ_BATTERY_STATUS = "read_battery_status"
CONF_READ_BALANCE_STATUS = "read_balance_status"
CONF_READ_CELL_VOLTAGES = "read_cell_voltages"
CONF_READ_CELL_RESISTANCES = "read_cell_resistances"
CONF_RESET_CHARGE_COUNTER = "reset_charge_counter"
CONF_CLEAR_ERRORS = "clear_errors"

# 定义按钮图标
ICON_SET_RETRIEVE = ICON_SEARCH
ICON_DEVICE_INFO_RETRIEVE = ICON_FILE_FIND
ICON_READ_BATTERY_PARAMS = ICON_CIRCLE_SLICE_8
ICON_READ_BATTERY_STATUS = ICON_BATTERY_PLUS
ICON_READ_BALANCE_STATUS = ICON_BATTERY_MINUS
ICON_READ_CELL_VOLTAGES = ICON_CIRCLE_SLICE_8
ICON_READ_CELL_RESISTANCES = ICON_CIRCLE_SLICE_8
ICON_RESET_CHARGE_COUNTER = ICON_RESTART
ICON_CLEAR_ERRORS = ICON_RELOAD

# 定义按钮命令码
# 为了支持不同品牌的BMS，需要根据实际协议修改这些命令码
BUTTONS = {
    # 设置检索按钮命令码
    CONF_SET_RETRIEVE: 0x96,
    # 设备信息检索按钮命令码
    CONF_DEVICE_INFO_RETRIEVE: 0x97,
    # 读取电池参数按钮命令码
    CONF_READ_BATTERY_PARAMS: 0x98,
    # 读取电池状态按钮命令码
    CONF_READ_BATTERY_STATUS: 0x99,
    # 读取均衡状态按钮命令码
    CONF_READ_BALANCE_STATUS: 0x9A,
    # 读取单体电压按钮命令码
    CONF_READ_CELL_VOLTAGES: 0x9B,
    # 读取单体电阻按钮命令码
    CONF_READ_CELL_RESISTANCES: 0x9C,
    # 重置充电计数器按钮命令码
    CONF_RESET_CHARGE_COUNTER: 0x9D,
    # 清除错误按钮命令码
    CONF_CLEAR_ERRORS: 0x9E,
}

# 定义配置模式
CONFIG_SCHEMA = JH_BMS_ESP32_COMPONENT_SCHEMA.extend(
    {
        # 设置检索按钮配置
        cv.Optional(CONF_SET_RETRIEVE): button.button_schema(
            JhButton,
            icon=ICON_SET_RETRIEVE,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 设备信息检索按钮配置
        cv.Optional(CONF_DEVICE_INFO_RETRIEVE): button.button_schema(
            JhButton,
            icon=ICON_DEVICE_INFO_RETRIEVE,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 读取电池参数按钮配置
        cv.Optional(CONF_READ_BATTERY_PARAMS): button.button_schema(
            JhButton,
            icon=ICON_READ_BATTERY_PARAMS,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 读取电池状态按钮配置
        cv.Optional(CONF_READ_BATTERY_STATUS): button.button_schema(
            JhButton,
            icon=ICON_READ_BATTERY_STATUS,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 读取均衡状态按钮配置
        cv.Optional(CONF_READ_BALANCE_STATUS): button.button_schema(
            JhButton,
            icon=ICON_READ_BALANCE_STATUS,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 读取单体电压按钮配置
        cv.Optional(CONF_READ_CELL_VOLTAGES): button.button_schema(
            JhButton,
            icon=ICON_READ_CELL_VOLTAGES,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 读取单体电阻按钮配置
        cv.Optional(CONF_READ_CELL_RESISTANCES): button.button_schema(
            JhButton,
            icon=ICON_READ_CELL_RESISTANCES,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        # 重置充电计数器按钮配置
        cv.Optional(CONF_RESET_CHARGE_COUNTER): button.button_schema(
            JhButton,
            icon=ICON_RESET_CHARGE_COUNTER,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        # 清除错误按钮配置
        cv.Optional(CONF_CLEAR_ERRORS): button.button_schema(
            JhButton,
            icon=ICON_CLEAR_ERRORS,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
    }
)


async def to_code(config):
    # 获取组件实例
    hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    # 遍历所有按钮类型
    for key in BUTTONS:
        # 检查配置中是否有该按钮
        if key in config:
            # 获取按钮配置
            conf = config[key]
            # 创建按钮组件
            var = cg.new_Pvariable(conf["id"])
            # 注册按钮组件
            await button.register_button(var, conf)
            # 将按钮添加到组件
            await cg.register_component(var, conf)
            # 设置按钮的父组件
            cg.add(var.set_parent(hub))
            # 设置按钮命令码
            # 为了支持不同品牌的BMS，这里需要根据实际协议修改命令码
            command = BUTTONS[key]
            cg.add(var.set_command(command))
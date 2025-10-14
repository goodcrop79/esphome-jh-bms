import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import (
    DEVICE_CLASS_SWITCH,
    ICON_CHARGING,
    ICON_DISCHARGE,
    ICON_COUNTER_RESET,
    ICON_POWER,
    ICON_LIGHTBULB,
    ICON_SIGNAL,
    ICON_BATTERY_CHARGING,
    ICON_HOME_LIGHTNING_BOLT,
    ICON_ALERT_CIRCLE,
    ICON_AUTORENEW,
)

from .. import (
    CONF_JH_BMS_ESP32_ID,
    JH_BMS_ESP32_COMPONENT_SCHEMA,
    jh_bms_esp32_ns,
)
from ..const import (
    CONF_BALANCER,
    CONF_CHARGING,
    CONF_DISCHARGING,
    CONF_ONE_KEY_ACTIVATION,
    CONF_BATTERY_LOW_SHUTDOWN,
    CONF_BATTERY_LOW_ALARM,
    CONF_BATTERY_HIGH_ALARM,
    CONF_TEMPERATURE_HIGH_ALARM,
    CONF_TEMPERATURE_LOW_ALARM,
    CONF_CURRENT_OVER_ALARM,
    CONF_BATTERY_UNDER_VOLTAGE_ALARM,
    CONF_BATTERY_OVER_VOLTAGE_ALARM,
)

# 为了支持不同品牌的BMS，这里需要修改寄存器地址和命令格式
DEPENDENCIES = ["jh_bms_esp32"]

CODEOWNERS = ["@syssi", "@txubelaxu"]

JhSwitch = jh_bms_esp32_ns.class_("JhSwitch", switch.Switch, cg.Component)

# 定义各开关类型的图标
ICON_BALANCER = ICON_AUTORENEW
ICON_CHARGING = ICON_BATTERY_CHARGING
ICON_DISCHARGING = ICON_DISCHARGE
ICON_ONE_KEY_ACTIVATION = ICON_POWER
ICON_BATTERY_LOW_SHUTDOWN = ICON_POWER
ICON_BATTERY_LOW_ALARM = ICON_ALERT_CIRCLE
ICON_BATTERY_HIGH_ALARM = ICON_ALERT_CIRCLE
ICON_TEMPERATURE_HIGH_ALARM = ICON_ALERT_CIRCLE
ICON_TEMPERATURE_LOW_ALARM = ICON_ALERT_CIRCLE
ICON_CURRENT_OVER_ALARM = ICON_ALERT_CIRCLE
ICON_BATTERY_UNDER_VOLTAGE_ALARM = ICON_ALERT_CIRCLE
ICON_BATTERY_OVER_VOLTAGE_ALARM = ICON_ALERT_CIRCLE

# 定义不同协议版本的寄存器地址
# 为了支持不同品牌的BMS，需要根据实际协议修改这些地址
SWITCHES = {
    # 均衡器开关
    CONF_BALANCER: {
        # JH01协议版本的寄存器地址
        "JH01": 0x00,
        # JH02协议版本的寄存器地址
        "JH02": 0x01,
        # JH03协议版本的寄存器地址
        "JH03": 0x02,
    },
    # 充电开关
    CONF_CHARGING: {
        "JH01": 0x03,
        "JH02": 0x04,
        "JH03": 0x05,
    },
    # 放电开关
    CONF_DISCHARGING: {
        "JH01": 0x06,
        "JH02": 0x07,
        "JH03": 0x08,
    },
    # 一键激活开关
    CONF_ONE_KEY_ACTIVATION: {
        "JH01": 0x09,
        "JH02": 0x0A,
        "JH03": 0x0B,
    },
    # 电池低电压关机开关
    CONF_BATTERY_LOW_SHUTDOWN: {
        "JH01": 0x0C,
        "JH02": 0x0D,
        "JH03": 0x0E,
    },
    # 电池低电压报警开关
    CONF_BATTERY_LOW_ALARM: {
        "JH01": 0x0F,
        "JH02": 0x10,
        "JH03": 0x11,
    },
    # 电池高电压报警开关
    CONF_BATTERY_HIGH_ALARM: {
        "JH01": 0x12,
        "JH02": 0x13,
        "JH03": 0x14,
    },
    # 温度高报警开关
    CONF_TEMPERATURE_HIGH_ALARM: {
        "JH01": 0x15,
        "JH02": 0x16,
        "JH03": 0x17,
    },
    # 温度低报警开关
    CONF_TEMPERATURE_LOW_ALARM: {
        "JH01": 0x18,
        "JH02": 0x19,
        "JH03": 0x1A,
    },
    # 电流过流报警开关
    CONF_CURRENT_OVER_ALARM: {
        "JH01": 0x1B,
        "JH02": 0x1C,
        "JH03": 0x1D,
    },
    # 电池欠压报警开关
    CONF_BATTERY_UNDER_VOLTAGE_ALARM: {
        "JH01": 0x1E,
        "JH02": 0x1F,
        "JH03": 0x20,
    },
    # 电池过压报警开关
    CONF_BATTERY_OVER_VOLTAGE_ALARM: {
        "JH01": 0x21,
        "JH02": 0x22,
        "JH03": 0x23,
    },
}

# 定义配置模式
CONFIG_SCHEMA = JH_BMS_ESP32_COMPONENT_SCHEMA.extend(
    {
        # 均衡器开关配置
        cv.Optional(CONF_BALANCER): switch.switch_schema(
            JhSwitch,
            icon=ICON_BALANCER,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 充电开关配置
        cv.Optional(CONF_CHARGING): switch.switch_schema(
            JhSwitch,
            icon=ICON_CHARGING,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 放电开关配置
        cv.Optional(CONF_DISCHARGING): switch.switch_schema(
            JhSwitch,
            icon=ICON_DISCHARGING,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 一键激活开关配置
        cv.Optional(CONF_ONE_KEY_ACTIVATION): switch.switch_schema(
            JhSwitch,
            icon=ICON_ONE_KEY_ACTIVATION,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电池低电压关机开关配置
        cv.Optional(CONF_BATTERY_LOW_SHUTDOWN): switch.switch_schema(
            JhSwitch,
            icon=ICON_BATTERY_LOW_SHUTDOWN,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电池低电压报警开关配置
        cv.Optional(CONF_BATTERY_LOW_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_BATTERY_LOW_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电池高电压报警开关配置
        cv.Optional(CONF_BATTERY_HIGH_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_BATTERY_HIGH_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 温度高报警开关配置
        cv.Optional(CONF_TEMPERATURE_HIGH_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_TEMPERATURE_HIGH_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 温度低报警开关配置
        cv.Optional(CONF_TEMPERATURE_LOW_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_TEMPERATURE_LOW_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电流过流报警开关配置
        cv.Optional(CONF_CURRENT_OVER_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_CURRENT_OVER_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电池欠压报警开关配置
        cv.Optional(CONF_BATTERY_UNDER_VOLTAGE_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_BATTERY_UNDER_VOLTAGE_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # 电池过压报警开关配置
        cv.Optional(CONF_BATTERY_OVER_VOLTAGE_ALARM): switch.switch_schema(
            JhSwitch,
            icon=ICON_BATTERY_OVER_VOLTAGE_ALARM,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)


async def to_code(config):
    # 获取组件实例
    hub = await cg.get_variable(config[CONF_JH_BMS_ESP32_ID])
    # 获取协议版本
    protocol_version = config.get("protocol_version", "JH01")
    # 遍历所有开关类型
    for key in SWITCHES:
        # 检查配置中是否有该开关
        if key in config:
            # 获取开关配置
            conf = config[key]
            # 创建开关组件
            var = cg.new_Pvariable(conf["id"])
            # 注册开关组件
            await switch.register_switch(var, conf)
            # 将开关添加到组件
            await cg.register_component(var, conf)
            # 设置开关的父组件
            cg.add(var.set_parent(hub))
            # 根据协议版本设置寄存器地址
            # 为了支持不同品牌的BMS，这里需要根据实际协议修改
            register_address = SWITCHES[key].get(protocol_version, SWITCHES[key]["JH01"])
            cg.add(var.set_register(register_address))
            # 调用hub的set_*_switch方法设置开关
            # 为了支持不同品牌的BMS，这里的方法名可能需要根据实际情况修改
            cg.add(getattr(hub, f"set_{key}_switch")(var))
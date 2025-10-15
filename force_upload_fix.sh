#!/bin/bash

# 强制上传修复脚本
# 此脚本将强制上传修复后的JH BMS ESP32组件到GitHub仓库

# 设置颜色变量
green='\033[0;32m'
red='\033[0;31m'
cyan='\033[0;36m'
nc='\033[0m' # No Color

# 打印脚本说明
echo "${green}JH BMS ESP32 强制上传修复脚本${nc}"
echo "此脚本将强制上传修复后的components目录结构到GitHub仓库"

sleep 1

# 检查是否在git仓库中
if [ ! -d ".git" ]; then
    echo "${red}错误: 当前目录不是一个git仓库！${nc}"
    echo "请先初始化git仓库或切换到正确的仓库目录"
    exit 1
fi

# 检查components目录是否存在
if [ ! -d "components" ]; then
    echo "${red}错误: 未找到components目录！${nc}"
    exit 1
fi

# 检查远程仓库配置
echo "\n${green}检查远程仓库配置...${nc}"
remote_url=$(git config --get remote.origin.url)

if [ -z "$remote_url" ]; then
    echo "${red}未配置远程仓库！${nc}"
    echo -n "请输入GitHub仓库URL: "
    read remote_url
    git remote add origin $remote_url
else
    echo "当前远程仓库: $remote_url"
fi

# 切换到main分支
echo "\n${green}切换到main分支...${nc}"
git checkout main

# 确保components目录被添加到git跟踪
echo "\n${green}添加并提交components目录...${nc}"
git add components/

# 强制创建提交，即使没有更改
echo -n "请输入提交信息 (默认为'修复ESPHome 2025.9.3版本兼容性问题'): "
read commit_message
commit_message=${commit_message:-"修复ESPHome 2025.9.3版本兼容性问题"}

# 尝试常规提交，如果失败则创建空提交
git commit -m "$commit_message"
if [ $? -ne 0 ]; then
    echo "${cyan}\n没有检测到更改，但仍创建强制提交...${nc}"
    git commit --allow-empty -m "强制更新: $commit_message"
fi

# 强制推送到GitHub
echo "\n${green}强制推送到GitHub仓库...${nc}"
git push --force origin main

# 检查推送是否成功
if [ $? -eq 0 ]; then
    echo "\n${green}组件修复已成功上传到GitHub！${nc}"
    echo "\n${green}请在ESPHome配置中使用以下设置:${nc}"
    echo "external_components:"
    echo "  - source: github://goodcrop79/esphome-jh-bms@main"
    echo "    components: [jh_bms_esp32]"
    echo "    refresh: 1d"
    echo "\n${cyan}注意: 由于使用了--force选项，确保没有其他协作者同时修改代码！${nc}"
else
    echo "\n${red}推送失败！请手动检查并重新上传。${nc}"
    exit 1
fi

exit 0
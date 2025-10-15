#!/bin/zsh

# 脚本功能：将完整的components目录结构上传到GitHub仓库
# 注意：运行此脚本前，请确保已安装git并配置好GitHub账号

# 设置颜色变量
green='\033[0;32m'
red='\033[0;31m'
nc='\033[0m' # No Color

# 打印脚本说明
echo "${green}JH BMS ESP32 组件上传脚本${nc}"
echo "此脚本将帮助您将完整的components目录结构上传到GitHub仓库"

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
    echo -n "是否使用此远程仓库? (y/n): "
    read use_existing
    if [ "$use_existing" != "y" ] && [ "$use_existing" != "Y" ]; then
        echo -n "请输入新的GitHub仓库URL: "
        read new_remote_url
        git remote set-url origin $new_remote_url
    fi
fi

# 确认上传的分支
echo -n "\n请输入要上传的分支名称 (默认为main): "
read branch_name
branch_name=${branch_name:-main}

# 检查分支是否存在
git show-ref --verify --quiet refs/heads/$branch_name
if [ $? -ne 0 ]; then
    echo "${green}创建新分支: $branch_name${nc}"
    git checkout -b $branch_name
else
    echo "${green}切换到分支: $branch_name${nc}"
    git checkout $branch_name
fi

sleep 1

# 添加components目录及其内容到暂存区
 echo "
${green}添加components目录到暂存区...${nc}"
 git add components/

 # 特别添加__init__.py文件以确保它被包含
 git add components/jh_bms_esp32/__init__.py

# 检查是否有未跟踪的文件
untracked_files=$(git status --porcelain | grep '^??' | wc -l)
if [ $untracked_files -gt 0 ]; then
    echo "${green}发现$untracked_files个未跟踪的文件，是否全部添加? (y/n): ${nc}"
    read add_all
    if [ "$add_all" = "y" ] || [ "$add_all" = "Y" ]; then
        git add .
    fi
fi

sleep 1

# 提交更改
 echo "
${green}创建提交...${nc}"
 echo -n "请输入提交信息: "
 read commit_message
 commit_message=${commit_message:-"上传完整的JH BMS ESP32组件目录结构"}
 git commit -m "$commit_message"

 # 检查是否有任何更改需要提交
 if [ $? -ne 0 ]; then
     echo "
${red}没有检测到更改，但仍尝试强制提交...${nc}"
     # 如果没有更改，创建一个空提交
     git commit --allow-empty -m "强制更新: $commit_message"
 fi

 sleep 1

 # 推送到GitHub，使用--force选项确保更新
 echo "
${green}推送到GitHub仓库...${nc}"
 git push --force -u origin $branch_name

# 检查推送是否成功
if [ $? -eq 0 ]; then
    echo "\n${green}组件目录上传成功！${nc}"
    echo "\n${green}上传完成后，您可以在ESPHome配置中使用以下设置从GitHub获取组件:${nc}"
    echo "external_components:"
    echo "  - source: github://goodcrop79/esphome-jh-bms@$branch_name"
    echo "    components: [jh_bms_esp32]"
    echo "    refresh: 1d"
else
    echo "\n${red}推送失败！${nc}"
    echo "请检查GitHub账号权限和网络连接，或尝试使用以下命令手动推送:"
    echo "git push -u origin $branch_name"
fi
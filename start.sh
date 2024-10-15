#!/bin/bash

# 获取脚本所在目录
SHELL_FOLDER=$(cd "$(dirname "$0")"; pwd)
echo "Script directory: $SHELL_FOLDER"

echo "Current PYTHONPATH: $PYTHONPATH"

# 设置 Python 环境变量
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER

export ENVIRONMENT=development

export HTTP_PROXY="http://172.22.220.64:7890"
export HTTPS_PROXY="http://172.22.220.64:7890"

python main.py

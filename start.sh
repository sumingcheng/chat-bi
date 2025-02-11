#!/bin/bash

# 获取脚本所在目录
SHELL_FOLDER=$(cd "$(dirname "$0")"; pwd)
echo "Script directory: $SHELL_FOLDER"

echo "Current PYTHONPATH: $PYTHONPATH"

# 设置 Python 日志不缓冲
export PYTHONUNBUFFERED=1 

# 设置 Python 路径
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER

# 设置代理
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# 设置数据库和OpenAI API的环境变量
export OPENAI_API_KEY="sk-"
export DB_HOST="127.0.0.1"
export DB_PORT=13306
export DB_USER="root"
export DB_PASSWORD="admin123456"
export DB_NAME="chat_bi"

# 启动 Python 应用
python main.py

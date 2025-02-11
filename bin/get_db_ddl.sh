#!/bin/bash

# 获取脚本所在目录
SHELL_FOLDER=$(cd "$(dirname "$0")"; pwd)
echo "Script directory: $SHELL_FOLDER"

echo "Current PYTHONPATH: $PYTHONPATH"

# 设置 Python 环境变量
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$SHELL_FOLDER

# 设置数据库和 OpenAI API 的环境变量
export OPENAI_API_KEY="sk-"
export DB_HOST="127.0.0.1"
export DB_PORT=13306
export DB_USER="root"
export DB_PASSWORD="admin123456"
export DB_NAME="chat_bi"

# 启动 Python 应用
python "$SHELL_FOLDER/ddl.py"

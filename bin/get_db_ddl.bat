@echo off
setlocal

:: 获取脚本所在目录
set SHELL_FOLDER=%~dp0
echo Script directory: %SHELL_FOLDER%

echo Current PYTHONPATH: %PYTHONPATH%

:: 设置 Python 环境变量
set PYTHONUNBUFFERED=1
set PYTHONPATH=%PYTHONPATH%;%SHELL_FOLDER%

:: 设置数据库和 OpenAI API 的环境变量
set OPENAI_API_KEY=sk-
set DB_HOST=127.0.0.1
set DB_PORT=3306
set DB_USER=root
set DB_PASSWORD=admin123456
set DB_NAME=chat_bi

:: 启动 Python 应用
python "%SHELL_FOLDER%ddl.py"

pause 
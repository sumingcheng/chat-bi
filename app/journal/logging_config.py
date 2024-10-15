import logging
from logging.handlers import RotatingFileHandler
import os

# 创建或获取一个日志记录器
logger = logging.getLogger(__name__)

# 设置日志级别
logger.setLevel(logging.INFO)

if not logger.handlers:
    # 确保日志目录存在
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # 设置日志文件路径
    log_file = os.path.join(log_dir, 'app.log')

    # 创建文件处理器，设置日志滚动：日志文件最大 5MB，保留 5 个备份
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

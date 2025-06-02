import os
import logging
from logging.handlers import RotatingFileHandler

# 确保日志目录存在
os.makedirs("logs", exist_ok=True)

# 配置根日志器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        RotatingFileHandler(  # 文件输出(带轮转)
            "logs/app.log",
            maxBytes=20 * 1024 * 1024,  # 20MB
            backupCount=5,
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger("app")

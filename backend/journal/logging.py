from loguru import logger
import sys
from pathlib import Path
from backend.config.main import Config

# 创建日志目录
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

# 移除默认处理器
logger.remove()

# 添加控制台处理器
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if Config.DEBUG else "INFO"
)

# 添加文件处理器
logger.add(
    log_path / "app_{time}.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO"
)

# 添加错误日志处理器
logger.add(
    log_path / "error_{time}.log",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR"
)

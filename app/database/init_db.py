import logging
import asyncio
import sys
from pathlib import Path
from app.database.base import init_business_db, init_system_db, close_connections

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("开始创建数据库表结构...")
        await init_business_db()
        await init_system_db()
        logger.info("✓ 数据库表创建完成")

        return True

    except Exception as e:
        logger.error(f"✗ 数据库表创建失败: {e}")
        return False

    finally:
        await close_connections()


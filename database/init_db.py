import logging
import asyncio
import sys
from pathlib import Path
from database.base import init_business_db, init_system_db, close_connections

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("创建数据库表结构...")
        await init_business_db()
        await init_system_db()
        logger.info("✓ 数据库表创建完成")
        
        logger.info("创建的表:")
        logger.info("业务库: category, customer, product, sales_order, order_item, sales")
        logger.info("系统库: sql_templates, sql_template_params, query_history")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 创建失败: {e}")
        return False
    
    finally:
        await close_connections()


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 
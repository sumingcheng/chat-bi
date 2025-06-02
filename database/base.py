import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.app_config import Config
logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()

# 业务数据库引擎
business_engine = create_async_engine(
    f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,  # 1小时回收连接
)

# 系统数据库引擎
system_engine = create_async_engine(
    f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_SYS_NAME}",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

# 创建会话工厂
BusinessSessionLocal = sessionmaker(
    business_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

SystemSessionLocal = sessionmaker(
    system_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


# 依赖注入函数
async def get_business_session():
    """获取业务数据库会话"""
    async with BusinessSessionLocal() as session:
        yield session


async def get_system_session():
    """获取系统数据库会话"""
    async with SystemSessionLocal() as session:
        yield session


# 数据库初始化
async def init_business_db():
    """初始化业务数据库表"""
    try:
        logger.info("开始初始化业务数据库表...")
        from .business_models import Category, Customer, Product, SalesOrder, OrderItem, Sales
        async with business_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("业务数据库表初始化完成")
    except Exception as e:
        logger.error(f"业务数据库表初始化失败: {e}")
        raise


async def init_system_db():
    """初始化系统数据库表"""
    try:
        logger.info("开始初始化系统数据库表...")
        from .system_models import SQLTemplate, SQLTemplateParam, QueryHistory
        async with system_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("系统数据库表初始化完成")
    except Exception as e:
        logger.error(f"系统数据库表初始化失败: {e}")
        raise


async def close_connections():
    """关闭数据库连接"""
    try:
        logger.info("正在关闭数据库连接...")
        await business_engine.dispose()
        await system_engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接时出错: {e}")
        raise 
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.app_config import Config

logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()

# 数据库引擎配置函数
def create_database_engine(database_name: str):
    """创建数据库引擎的统一配置"""
    return create_async_engine(
        f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{database_name}",
        echo=Config.DEBUG,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,  # 1小时回收连接
    )

# 业务数据库引擎
business_engine = create_database_engine(Config.DB_NAME)

# 系统数据库引擎
system_engine = create_database_engine(Config.DB_SYS_NAME)

# 创建会话工厂
BusinessSessionLocal = sessionmaker(
    business_engine, class_=AsyncSession, expire_on_commit=False
)

SystemSessionLocal = sessionmaker(
    system_engine, class_=AsyncSession, expire_on_commit=False
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


# 获取模型列表（延迟导入避免循环依赖）
def get_business_models():
    """获取业务模型列表"""
    from .business_models import Category, Customer, Product, SalesOrder, OrderItem, Sales
    return [Category, Customer, Product, SalesOrder, OrderItem, Sales]


def get_system_models():
    """获取系统模型列表"""
    from .system_models import SQLTemplate, SQLTemplateParam, QueryHistory
    return [SQLTemplate, SQLTemplateParam, QueryHistory]


# 统一的数据库初始化函数
async def _init_database(engine, models, db_type: str):
    """统一的数据库初始化逻辑"""
    try:
        table_names = [model.__tablename__ for model in models]
        logger.info(f"开始初始化{db_type}数据库表: {table_names}")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"{db_type}数据库表初始化完成")
    except Exception as e:
        logger.error(f"{db_type}数据库表初始化失败: {e}")
        raise


# 数据库初始化
async def init_business_db():
    """初始化业务数据库表"""
    await _init_database(business_engine, get_business_models(), "业务")


async def init_system_db():
    """初始化系统数据库表"""
    await _init_database(system_engine, get_system_models(), "系统")


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

# 向后兼容的导出
BUSINESS_MODELS = get_business_models()
SYSTEM_MODELS = get_system_models()

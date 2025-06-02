from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.config.app_config import Config

# 业务数据库
business_engine = create_async_engine(
    f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10,
)

# 系统数据库
system_engine = create_async_engine(
    f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10,
)

AsyncBusinessSession = sessionmaker(
    business_engine, class_=AsyncSession, expire_on_commit=False
)

AsyncSystemSession = sessionmaker(
    system_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_business_db():
    async with AsyncBusinessSession() as session:
        yield session


async def get_system_db():
    async with AsyncSystemSession() as session:
        yield session

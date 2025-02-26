from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.config.main import Config

# 业务数据库
business_engine = create_async_engine(
    f"mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/chat_bi",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10
)

# 系统数据库
system_engine = create_async_engine(
    f"mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/chat_bi_sys",
    echo=Config.DEBUG,
    pool_size=5,
    max_overflow=10
)

AsyncBusinessSession = sessionmaker(
    business_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

AsyncSystemSession = sessionmaker(
    system_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_business_db():
    async with AsyncBusinessSession() as session:
        yield session

async def get_system_db():
    async with AsyncSystemSession() as session:
        yield session 
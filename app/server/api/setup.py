from fastapi import FastAPI, APIRouter
from app.server.middleware.cors import mw_cors
from app.server.api.query import query
from app.database.base import init_business_db, init_system_db, business_engine, system_engine, get_business_models, get_system_models
# 导入日志配置，确保使用自定义配置
from app.config.app_log import logger
from sqlalchemy import text

# logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Chat-BI API", description="智能商业分析对话系统API", version="1.0.0"
)

# 应用CORS中间件
mw_cors(app)

# 创建主API路由器
api_router = APIRouter(prefix="/api")

# 将子路由器挂载到主API路由器
api_router.include_router(query, tags=["查询"])

# 将主API路由器注册到应用
app.include_router(api_router)

async def check_tables_exist():
    """检查数据库表是否已存在"""
    business_models = get_business_models()
    system_models = get_system_models()
    
    # 检查业务数据库表
    async with business_engine.connect() as conn:
        for model in business_models:
            table_name = model.__tablename__
            result = await conn.execute(text(f"SHOW TABLES LIKE '{table_name}'"))
            if result.fetchone():
                logger.info(f"✓ 业务数据库表 '{table_name}' 已存在")
            else:
                logger.info(f"✗ 业务数据库表 '{table_name}' 不存在，将创建")
    
    # 检查系统数据库表
    async with system_engine.connect() as conn:
        for model in system_models:
            table_name = model.__tablename__
            result = await conn.execute(text(f"SHOW TABLES LIKE '{table_name}'"))
            if result.fetchone():
                logger.info(f"✓ 系统数据库表 '{table_name}' 已存在")
            else:
                logger.info(f"✗ 系统数据库表 '{table_name}' 不存在，将创建")

@app.on_event("startup")
async def startup_event():
    """应用启动时自动初始化数据库表"""
    try:
        logger.info("🚀 应用启动中...")
        logger.info("📊 开始检查数据库表状态...")
        
        # 检查表是否存在
        await check_tables_exist()
        
        logger.info("📊 开始初始化数据库表...")
        
        # 初始化业务数据库表
        await init_business_db()
        
        # 初始化系统数据库表  
        await init_system_db()
        
        logger.info("✅ 数据库表初始化完成")
        logger.info("🎉 Chat-BI API 启动成功！")
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        logger.error("💡 请检查数据库配置和连接")
        # 不要让应用崩溃，只记录错误
        pass

__all__ = ["app"]

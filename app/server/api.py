from fastapi import FastAPI, APIRouter
from middleware.cors import mw_cors
from app.server.query import router as query_router
from app.server.templates import router as templates_router
from app.server.history import router as history_router
from app.server.satisfaction import router as satisfaction_router

# 创建FastAPI应用
app = FastAPI(
    title="Chat-BI API",
    description="智能商业分析对话系统API",
    version="1.0.0"
)

# 应用CORS中间件
mw_cors(app)

# 创建主API路由器
api_router = APIRouter(prefix="/api")

# 将子路由器挂载到主API路由器
api_router.include_router(query_router, tags=["查询"])
api_router.include_router(templates_router, tags=["模板管理"])
api_router.include_router(history_router, tags=["历史记录"])
api_router.include_router(satisfaction_router, tags=["满意度评价"])

# 将主API路由器注册到应用
app.include_router(api_router)

__all__ = ["app"]


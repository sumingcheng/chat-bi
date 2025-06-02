from fastapi import FastAPI, APIRouter
from middleware.cors import mw_cors
from app.server.api.query import query

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

__all__ = ["app"]

from fastapi import FastAPI
from backend.middleware.cors import mw_cors
from backend.routers.api import router
import uvicorn

# 创建FastAPI应用
app = FastAPI()
# 应用CORS中间件
mw_cors(app)
# 包含API路由
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=13000)

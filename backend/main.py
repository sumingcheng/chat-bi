from fastapi import FastAPI
from backend.middleware.cors import mw_cors
from backend.routers import api, templates
import uvicorn

# 创建FastAPI应用
app = FastAPI()
# 应用CORS中间件
mw_cors(app)

# 定义路由列表
routers = [api.router, templates.router]

# 循环注册路由
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=13000)

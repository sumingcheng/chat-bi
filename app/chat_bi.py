from fastapi import FastAPI
from app.middleware.cors import mw_cors
from app.routers.api import router

app = FastAPI()
mw_cors(app)

app.include_router(router)

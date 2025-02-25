from fastapi import FastAPI
from backend.middleware.cors import mw_cors
from backend.routers.api import router

app = FastAPI()
mw_cors(app)

app.include_router(router)

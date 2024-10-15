from fastapi import FastAPI
from app.cors.cors import setup_cors
from app.routes.api import router

app = FastAPI()
setup_cors(app)

app.include_router(router)

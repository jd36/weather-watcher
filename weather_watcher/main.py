from fastapi import FastAPI
from weather_watcher.api_router import router

app = FastAPI()

app.include_router(router, prefix="/api")

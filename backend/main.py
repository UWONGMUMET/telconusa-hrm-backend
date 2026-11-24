from fastapi import FastAPI

from routes.health import router as health_router
from routes.v1 import router as api_router

app = FastAPI(
    title="Telconusa HRM",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(api_router)
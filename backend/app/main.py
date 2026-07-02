from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from structlog import get_logger

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    lifespan=lifespan,
)

logger = get_logger(__name__)

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.get("/health/database")
async def health_check_database():
    return {"status": "ok"}

@app.get("/health/storage")
async def health_check_storage():
    return {"status": "ok"}
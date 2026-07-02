from fastapi import FastAPI
from structlog import get_logger

app = FastAPI(title="CMS WD Eventos Landing page", version="1.0.0", description="CMS WD Eventos Landing page")
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
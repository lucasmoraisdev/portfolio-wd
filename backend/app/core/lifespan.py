from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import configure_logging
from app.shared.database.session import engine
from structlog import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    logger.info(
        "Starting application",
        app_name=settings.app.name,
        version=settings.app.version,
        environment=settings.app.env
    )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        
        logger.info("Database connection successful")
    
    except Exception as e:
        logger.exception(
            "Database connection failed",
            error=str(e)
        )
        raise

    yield
    
    logger.info("Shutting down application", app_name=settings.app.name)

    engine.dispose()

    logger.info("Database connection closed")
from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from structlog import get_logger
from app.shared.exceptions import register_exception_handlers
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.shared.database import engine
from pathlib import Path

# Import module routers
from app.modules.auth.api import router as auth_router
from app.modules.user.api import router as user_router
from app.modules.toys.api import router as toys_router
from app.modules.settings.api import router as settings_router
from app.modules.events.api import router as events_router
from app.modules.testimonials.api import router as testimonials_router
from app.modules.faq.api import router as faq_router
from app.modules.contacts.api import router as contacts_router
from app.modules.hero.api import router as hero_router
from app.modules.dashboard.api import router as dashboard_router
from app.modules.upload.api import router as upload_router

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    lifespan=lifespan,
)

logger = get_logger(__name__)
register_exception_handlers(app)

# Register routers on FastAPI app instance
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(toys_router)
app.include_router(settings_router)
app.include_router(events_router)
app.include_router(testimonials_router)
app.include_router(faq_router)
app.include_router(contacts_router)
app.include_router(hero_router)
app.include_router(dashboard_router)
app.include_router(upload_router)
@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.get("/health/database")
async def health_check_database():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": f"Database connection failed: {str(e)}"}
        )

@app.get("/health/storage")
async def health_check_storage():
    try:
        upload_dir = Path(settings.storage.upload_directory)
        if not upload_dir.exists() or not upload_dir.is_dir():
            raise Exception("Upload directory does not exist or is not a directory")
        
        # Test write permission by writing a tiny temp file
        test_file = upload_dir / ".health_check_test"
        test_file.write_text("ok")
        test_file.unlink() # Delete after writing
        
        return {"status": "ok", "storage": "healthy"}
    except Exception as e:
        logger.error(f"Storage health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": f"Storage write test failed: {str(e)}"}
        )
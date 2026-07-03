from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    pool_recycle=3600,
    max_overflow=settings.database.max_overflow
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Generator

from app.core.config import settings

engine = create_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_pre_ping=settings.database.pool_size,
    max_overflow=settings.database.max_overflow
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
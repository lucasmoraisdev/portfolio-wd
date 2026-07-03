from sqlalchemy.orm import DeclarativeBase

from app.shared.database.metadata import metadata

class Base(DeclarativeBase):
    metadata = metadata
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.upload.constants import UPLOAD_TABLE_NAME

from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey

class Upload(Base, TimestampMixin):
    __tablename__ = UPLOAD_TABLE_NAME

    id: Mapped[PrimaryKey]
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    public_url: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    extension: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<Uploads(id={self.id}, public_url={self.public_url})"
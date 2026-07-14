from datetime import datetime
from sqlalchemy import Boolean, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .constants import CONTACTS_TABLE_NAME
from app.shared.database import Base
from app.shared.database.types import PrimaryKey

class ContactMessage(Base):
    __tablename__ = CONTACTS_TABLE_NAME

    id: Mapped[PrimaryKey]
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(200), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<ContactMessage(id={self.id}, name={self.name}, email={self.email})>"

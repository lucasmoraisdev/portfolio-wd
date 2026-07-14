from datetime import date

from sqlalchemy import Boolean, String, Text, Integer, ForeignKey, ARRAY, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .constants import EVENTS_TABLE_NAME
from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey
from app.modules.upload.models import Upload

class Events(Base, TimestampMixin):
    __tablename__ = EVENTS_TABLE_NAME

    id: Mapped[PrimaryKey]
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    client: Mapped[str] = mapped_column(String(100), nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)

    cover_image_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("uploads.id"),
        nullable=True,
    )

    gallery_image_ids: Mapped[list[UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True,
        default=list,
    )

    cover_image: Mapped[Upload | None] = relationship(
        "Upload",
        foreign_keys=[cover_image_id],
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Events(id={self.id}, title={self.title}, event_date={self.event_date})>"

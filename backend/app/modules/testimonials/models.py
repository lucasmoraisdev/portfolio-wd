from uuid import UUID

from sqlalchemy import Boolean, String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .constants import TESTIMONIALS_TABLE_NAME
from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey
from app.modules.upload.models import Upload

class Testimonials(Base, TimestampMixin):
    __tablename__ = TESTIMONIALS_TABLE_NAME

    id: Mapped[PrimaryKey]
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company: Mapped[str | None] = mapped_column(String(100), nullable=True)
    testimonial: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)

    photo_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("uploads.id"),
        nullable=True,
    )

    photo: Mapped[Upload | None] = relationship(
        "Upload",
        foreign_keys=[photo_id],
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Testimonials(id={self.id}, name={self.name}, rating={self.rating})>"

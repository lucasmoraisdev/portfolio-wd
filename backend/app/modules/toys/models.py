
from sqlalchemy import Boolean, String, Text, Integer, ForeignKey, UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .constants import TOYS_TABLE_NAME
from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey

from app.modules.upload.models import Upload

class Toys(Base, TimestampMixin):
    __tablename__ = TOYS_TABLE_NAME

    id: Mapped[PrimaryKey]
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    full_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    min_age: Mapped[int | None] = mapped_column(Integer, nullable=False, default=0)
    max_age: Mapped[int | None] = mapped_column(Integer, nullable=False, default=18)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=False, default=1)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=False, default=0, index=True)

    cover_image_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("uploads.id"),
        nullable=True,
    )

    gallery_image_ids: Mapped[list[UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True,
        default=list,
    )

    video_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    video_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        default="youtube",
    )

    cover_image: Mapped[Upload | None] = relationship(
        "Upload",
        foreign_keys=[cover_image_id],
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Toys(id={self.id}, name={self.name}, slug={self.slug})>"
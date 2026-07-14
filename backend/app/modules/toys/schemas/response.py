from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ToyResponse(BaseModel):
    """Resposta completa de um brinquedo."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    category: str
    short_description: str | None
    full_description: str | None
    min_age: int
    max_age: int
    capacity: int
    is_featured: bool
    is_active: bool
    display_order: int
    cover_image_id: UUID | None
    gallery_image_ids: list[UUID]
    video_url: str | None
    video_type: str | None
    created_at: datetime
    updated_at: datetime


class ToyStatusResponse(BaseModel):
    """Resposta de alteração de status."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    message: str


class ToyFeaturedResponse(BaseModel):
    """Resposta de alteração de destaque."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_featured: bool
    message: str


class ToyPositionResponse(BaseModel):
    """Resposta de alteração de posição."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    display_order: int
    message: str
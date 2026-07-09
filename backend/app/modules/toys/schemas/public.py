from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ToyPublicResponse(BaseModel):
    """Resposta pública de um brinquedo (para o site)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    category: str
    short_description: str | None
    min_age: int
    max_age: int
    capacity: int
    cover_image_url: str | None = None
    gallery_image_urls: list[str] = Field(default_factory=list)
    video_url: str | None


class ToyPublicListResponse(BaseModel):
    """Resposta pública de listagem."""

    items: list[ToyPublicResponse]
    total: int
    page: int
    per_page: int
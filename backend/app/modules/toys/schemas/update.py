from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.toys.constants import (
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    DESCRIPTION_SHORT_MAX,
    MAX_AGE,
    MIN_AGE,
    CAPACITY_MIN,
    CAPACITY_MAX,
)

class ToyUpdate(BaseModel):
    """Dados para atualização parcial de um brinquedo."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(
        default=None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
    )
    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    short_description: str | None = Field(
        default=None,
        max_length=DESCRIPTION_SHORT_MAX,
    )
    full_description: str | None = Field(default=None)
    min_age: int | None = Field(
        default=None,
        le=MIN_AGE,
    )
    max_age: int | None = Field(
        default=None,
        ge=MAX_AGE,
    )
    capacity: int | None = Field(
        default=None,
        ge=CAPACITY_MIN,
        le=CAPACITY_MAX,
    )
    is_featured: bool | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    display_order: int | None = Field(default=None)
    cover_image_id: UUID | None = Field(default=None)
    gallery_image_ids: list[UUID] | None = Field(default=None)
    video_url: str | None = Field(default=None)
    video_type: str | None = Field(default=None, pattern="^(youtube|file)$")

    @field_validator("max_age")
    @classmethod
    def validate_age_range(cls, v: int | None, info) -> int | None:
        if v is None:
            return v
        min_age = info.data.get("min_age")
        if min_age is not None and v < min_age:
            raise ValueError("A idade máxima deve ser maior ou igual à idade mínima")
        return v
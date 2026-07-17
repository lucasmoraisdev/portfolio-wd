from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.toys.constants import (
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    DESCRIPTION_SHORT_MAX,
    MAX_AGE,
    MIN_AGE,
    CAPACITY_MAX,
    CAPACITY_MIN
)

class ToyCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        description="Nome do brinquedo"
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Categoria do brinquedo",
    )

    short_description: str | None = Field(
        default=None,
        max_length=DESCRIPTION_SHORT_MAX,
        description="Descrição curta",
    )

    full_description: str | None = Field(
        default=None,
        description="Descrição completa",
    )

    min_age: int = Field(
        default=0,
        ge=0,
        description="Idade mínima recomendada",
    )

    max_age: int = Field(
        default=18,
        ge=1,
        description="Idade máxima recomendada",
    )

    capacity: int = Field(
        default=1,
        ge=CAPACITY_MIN,
        le=CAPACITY_MAX,
        description="Capacidade (quantas crianças)",
    )

    is_featured: bool = Field(default=False, description="Destaque na home")
    display_order: int = Field(default=0, description="Ordem de exibição")
    cover_image_id: UUID | None = Field(default=None, description="ID da imagem de capa")
    
    gallery_image_ids: list[UUID] = Field(
        default_factory=list,
        description="IDs das imagens da galeria",
    )

    video_url: str | None = Field(default=None, description="URL do vídeo")
    video_type: str = Field(default="youtube", pattern="^(youtube|file)$")

    @field_validator("max_age")
    @classmethod
    def validate_age_range(cls, v: int, info) -> int:
        min_age = info.data.get("min_age", 0)
        if v < min_age:
            raise ValueError("A idade máxima deve ser maior ou igual à idade mínima")
        return v
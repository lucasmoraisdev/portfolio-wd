from pydantic import BaseModel, Field


class ToyFilter(BaseModel):
    """Filtros para listagem de brinquedos."""

    search: str | None = Field(default=None, description="Busca por nome")
    category: str | None = Field(default=None, description="Filtrar por categoria")
    is_active: bool | None = Field(default=None, description="Filtrar por ativo")
    is_featured: bool | None = Field(default=None, description="Filtrar por destaque")
    min_age: int | None = Field(default=None, ge=0, le=18)
    max_age: int | None = Field(default=None, ge=0, le=18)
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    order_by: str = Field(default="display_order", pattern="^(name|display_order|created_at|category)$")
    order_direction: str = Field(default="asc", pattern="^(asc|desc)$")
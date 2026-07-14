from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class TestimonialBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class TestimonialCreate(TestimonialBase):
    name: str = Field(..., min_length=2, max_length=150, description="Nome de quem enviou o depoimento")
    city: str | None = Field(default=None, max_length=100, description="Cidade")
    company: str | None = Field(default=None, max_length=100, description="Empresa")
    testimonial: str = Field(..., min_length=5, description="Texto do depoimento")
    rating: int = Field(default=5, ge=1, le=5, description="Avaliação de 1 a 5")
    is_active: bool = Field(default=True, description="Está ativo")
    display_order: int = Field(default=0, description="Ordem de exibição")
    photo_id: UUID | None = Field(default=None, description="ID do upload da foto")

class TestimonialUpdate(TestimonialBase):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    city: str | None = Field(default=None, max_length=100)
    company: str | None = Field(default=None, max_length=100)
    testimonial: str | None = Field(default=None, min_length=5)
    rating: int | None = Field(default=None, ge=1, le=5)
    is_active: bool | None = Field(default=None)
    display_order: int | None = Field(default=None)
    photo_id: UUID | None = Field(default=None)

class TestimonialFilter(BaseModel):
    search: str | None = None
    is_active: bool | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    order_by: str = "display_order"
    order_direction: str = Field(default="asc", pattern="^(asc|desc)$")

class TestimonialResponse(TestimonialBase):
    id: UUID
    name: str
    city: str | None
    company: str | None
    testimonial: str
    rating: int
    is_active: bool
    display_order: int
    photo_id: UUID | None
    created_at: datetime
    updated_at: datetime

class TestimonialPublicResponse(TestimonialBase):
    id: UUID
    name: str
    city: str | None
    company: str | None
    testimonial: str
    rating: int
    photo_url: str | None

class TestimonialStatusResponse(TestimonialBase):
    id: UUID
    is_active: bool
    message: str

class TestimonialPositionResponse(TestimonialBase):
    id: UUID
    display_order: int
    message: str

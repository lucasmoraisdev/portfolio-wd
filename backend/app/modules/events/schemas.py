from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class EventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class EventCreate(EventBase):
    title: str = Field(..., min_length=2, max_length=200, description="Título do evento")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    client: str = Field(..., min_length=2, max_length=100, description="Nome do cliente")
    event_date: date = Field(..., description="Data do evento")
    description: str | None = Field(default=None, description="Descrição do evento")
    is_featured: bool = Field(default=False, description="Destaque na home")
    is_active: bool = Field(default=True, description="Está ativo")
    display_order: int = Field(default=0, description="Ordem de exibição")
    cover_image_id: UUID | None = Field(default=None, description="ID da imagem de capa")
    gallery_image_ids: list[UUID] = Field(default_factory=list, description="IDs das imagens da galeria")

class EventUpdate(EventBase):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    client: str | None = Field(default=None, min_length=2, max_length=100)
    event_date: date | None = Field(default=None)
    description: str | None = Field(default=None)
    is_featured: bool | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    display_order: int | None = Field(default=None)
    cover_image_id: UUID | None = Field(default=None)
    gallery_image_ids: list[UUID] | None = Field(default=None)

class EventFilter(BaseModel):
    search: str | None = None
    is_active: bool | None = None
    is_featured: bool | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    order_by: str = "display_order"
    order_direction: str = Field(default="asc", pattern="^(asc|desc)$")

class EventResponse(EventBase):
    id: UUID
    title: str
    city: str
    client: str
    event_date: date
    description: str | None
    is_featured: bool
    is_active: bool
    display_order: int
    cover_image_id: UUID | None
    gallery_image_ids: list[UUID]
    cover_image_url: str | None = None
    gallery_urls: list[str] = []
    created_at: datetime
    updated_at: datetime

class EventPublicResponse(EventBase):
    id: UUID
    title: str
    city: str
    client: str
    event_date: date
    description: str | None
    cover_image_url: str | None
    gallery_image_urls: list[str]

class EventStatusResponse(EventBase):
    id: UUID
    is_active: bool
    message: str

class EventFeaturedResponse(EventBase):
    id: UUID
    is_featured: bool
    message: str

class EventPositionResponse(EventBase):
    id: UUID
    display_order: int
    message: str

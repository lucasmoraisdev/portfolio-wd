from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class ContactCreate(ContactBase):
    name: str = Field(..., min_length=2, max_length=150, description="Nome do remetente")
    email: str = Field(..., min_length=5, max_length=255, description="E-mail de contato")
    phone: str | None = Field(default=None, max_length=30, description="Telefone de contato")
    subject: str | None = Field(default=None, max_length=200, description="Assunto da mensagem")
    message: str = Field(..., min_length=5, description="Conteúdo da mensagem")

class ContactResponse(ContactBase):
    id: UUID
    name: str
    email: str
    phone: str | None
    subject: str | None
    message: str
    is_read: bool
    created_at: datetime

class ContactFilter(BaseModel):
    search: str | None = None
    is_read: bool | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    order_by: str = "created_at"
    order_direction: str = Field(default="desc", pattern="^(asc|desc)$")

class ContactStatusResponse(ContactBase):
    id: UUID
    is_read: bool
    message: str

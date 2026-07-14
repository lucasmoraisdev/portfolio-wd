from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class FAQBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class FAQCreate(FAQBase):
    question: str = Field(..., min_length=5, max_length=300, description="Pergunta do FAQ")
    answer: str = Field(..., min_length=5, description="Resposta do FAQ")
    is_active: bool = Field(default=True, description="Está ativo")
    display_order: int = Field(default=0, description="Ordem de exibição")

class FAQUpdate(FAQBase):
    question: str | None = Field(default=None, min_length=5, max_length=300)
    answer: str | None = Field(default=None, min_length=5)
    is_active: bool | None = Field(default=None)
    display_order: int | None = Field(default=None)

class FAQFilter(BaseModel):
    search: str | None = None
    is_active: bool | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)
    order_by: str = "display_order"
    order_direction: str = Field(default="asc", pattern="^(asc|desc)$")

class FAQResponse(FAQBase):
    id: UUID
    question: str
    answer: str
    is_active: bool
    display_order: int
    created_at: datetime
    updated_at: datetime

class FAQStatusResponse(FAQBase):
    id: UUID
    is_active: bool
    message: str

class FAQPositionResponse(FAQBase):
    id: UUID
    display_order: int
    message: str

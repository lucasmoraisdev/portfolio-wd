"""
Schemas Pydantic para respostas padronizadas da API.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Schema base para todas as respostas da API.
    
    Uso:
        ApiResponse[UserResponse]  # para uma resposta com dados
        ApiResponse[None]          # para respostas sem dados (ex: delete)
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operação realizada com sucesso.",
                "data": {},
            }
        }
    )

    success: bool = True
    message: str = "Operação realizada com sucesso."
    data: T | None = None


class ApiErrorResponse(BaseModel):
    """Schema para respostas de erro (já coberto pelo handler global)."""
    success: bool = False
    error: dict[str, Any]
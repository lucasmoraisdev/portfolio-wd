"""
Módulo de respostas padronizadas da API.
"""

from .schemas import ApiResponse, ApiErrorResponse
from .helpers import (
    success_response,
    created_response,
    updated_response,
    deleted_response,
    paginated_response,
    json_success,
    json_created,
)
from .wrapper import api_response, standard_response

__all__ = [
    # Schemas
    "ApiResponse",
    "ApiErrorResponse",
    # Helpers
    "success_response",
    "created_response",
    "updated_response",
    "deleted_response",
    "paginated_response",
    "json_success",
    "json_created",
    # Decorators
    "api_response",
    "standard_response",
]
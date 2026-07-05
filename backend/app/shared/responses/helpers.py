"""
Funções helper para construir respostas padronizadas manualmente.

Use quando precisar de controle total sobre a resposta 
(ex: mensagens customizadas, dados específicos).
"""

from typing import Any

from fastapi.responses import JSONResponse

def success_response(
    data: Any = None,
    message: str = "Operação realizada com sucesso.",
    status_code: int = 200,
) -> dict[str, Any]:
    """
    Retorna um dict no formato padronizado de sucesso.
    
    Use em endpoints que retornam dict diretamente ou com JSONResponse.
    """
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def created_response(
    data: Any = None,
    message: str = "Recurso criado com sucesso.",
) -> dict[str, Any]:
    """Helper para respostas HTTP 201 Created."""
    return success_response(
        data=data,
        message=message,
        status_code=201,
    )


def updated_response(
    data: Any = None,
    message: str = "Recurso atualizado com sucesso.",
) -> dict[str, Any]:
    """Helper para respostas de atualização."""
    return success_response(
        data=data,
        message=message,
        status_code=200,
    )


def deleted_response(
    message: str = "Recurso removido com sucesso.",
) -> dict[str, Any]:
    """Helper para respostas de exclusão (sem dados)."""
    return success_response(
        data=None,
        message=message,
        status_code=200,
    )


def paginated_response(
    items: list[Any],
    total: int,
    page: int,
    per_page: int,
    message: str = "Listagem obtida com sucesso.",
) -> dict[str, Any]:
    """
    Helper para respostas paginadas.
    
    Estrutura do data:
    {
        "items": [...],
        "pagination": {
            "total": 100,
            "page": 1,
            "per_page": 20,
            "total_pages": 5
        }
    }
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return success_response(
        data={
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
            },
        },
        message=message,
    )


# ─── JSONResponse helpers (para casos especiais) ─────────────────

def json_success(
    data: Any = None,
    message: str = "Operação realizada com sucesso.",
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    """Retorna um JSONResponse no formato padronizado."""
    return JSONResponse(
        content=success_response(data, message, status_code),
        status_code=status_code,
        headers=headers,
    )


def json_created(
    data: Any = None,
    message: str = "Recurso criado com sucesso.",
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    """Retorna um JSONResponse 201 Created."""
    return json_success(data, message, 201, headers)
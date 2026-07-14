"""
Handlers globais de exceções para a aplicação.

Registra handlers para:
 - HTTPException
 - RequestValidationError
 - BusinessException
 - Exception genérica
"""

import traceback
from typing import Any
from app.core.logging import configure_logging
from structlog import get_logger

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException

from .exceptions import BusinessException

logger = get_logger(__name__)
configure_logging()

# ─── Schema de resposta padronizada ──────────────────────────────
def build_error_response(
    message: str,
    status_code: int,
    error_code: str = "ERROR",
    details: dict | list | None = None,
    path: str | None = None
) -> dict[str, Any]:
    """Constrói a resposta de erro padronizada"""
    response: dict[str, Any] = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "status_code": status_code,
        },
    }
    if details:
        response["error"]["details"] = details
    if path:
        response["error"]["path"] = path
    return response

# ─── Handler: HTTPException (Starlette) ──────────────────────────
async def http_exception_handler(
    request: Request,
    exc: StarletteHttpException
) -> Any:
    """
    Handler para HTTPException do Starlette.

    Ex: raise HTTPException(status_code=404, detail="Not found)
    """
    logger.warning(
        "HTTPException: %s | Path: %s | Method: %s",
        exc.detail,
        request.url.path,
        request.method
    )

    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", "Erro HTTP")
        details = exc.detail.get("details", {})
    else:
        message = str(exc.detail)
        details = None

    response = build_error_response(
        message=message,
        status_code=exc.status_code,
        error_code=f"HTTP_{exc.status_code}",
        details=details,
        path=request.url.path,
    )

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(response)
    )

# ─── Handler: RequestValidationError (Pydantic) ──────────────────
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> Any:
    """
    Handler para erros de validação.
    
    Ex: Campo obrigatório faltando, tipo, incorreto, etc
    """
    logger.warning(
        "ValidationError: %s | Path %s | Method: %s",
        exc.errors(),
        request.url.path,
        request.method
    )

    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": ".".join(str(loc) for loc in error.get("loc", [])),
            "message": error.get("msg", ""),
            "type": error.get("type", ""),
            "input": error.get("input")
        })
    
    response = build_error_response(
        message="Erro de validação nos dados enviados",
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        error_code="VALIDATION_ERROR",
        details=formatted_errors,
        path=request.url.path
    )

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder(response)
    )

# ─── Handler: BusinessException  ─────────────────────────────────
async def business_exception_handler(
    request: Request,
    exc: BusinessException,
) -> Any:
    """
    Handler para exceções de negócio customizadas.

    Todas as exceções que herdam de BusinessException caem aqui.
    """
    logger.info(
        "BusinessException: %s | Code: %s | Path: %s",
        exc.message,
        exc.error_code,
        request.url.path,
    )

    response = build_error_response(
        message=exc.message,
        status_code=exc.status_code,
        error_code=exc.error_code,
        details=exc.details if exc.details else None,
        path=request.url.path,
    )

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(response),
    )

# ─── Handler: Exception genérica (fallback) ──────────────────────
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> Any:
    """
    Handler de fallback para qualquer exceção não tratada.

    NUNCA expõe detalhes internos em produção.
    """
    trace = traceback.format_exc()
    logger.error(
        "Unhandled exception: %s\nTraceback:\n%s\nPath: %s | Method: %s",
        str(exc),
        trace,
        request.url.path,
        request.method,
    )

    response = build_error_response(
        message="Ocorreu um erro interno no servidor",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
        path=request.url.path,
    )

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(response),
    )

# ─── Registro dos handlers na aplicação ──────────────────────────
def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos os handlers de exceção na instância.

    Uso: from shared.exceptions.handlers import register_exception_handlers
        register_exception_handlers(app)
    """

    app.add_exception_handler(StarletteHttpException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    logger.info("Exception handlers registered successfully")
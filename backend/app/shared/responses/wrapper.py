"""
Wrapper/decorator para envolver automaticamente as respostas dos endpoints
no formato padronizado { success, message, data }.

Duas abordagens:
1. Decorator @api_response - para controle manual
2. Middleware automático - para aplicação global (opcional)
"""

from functools import wraps
from typing import Any, Callable, TypeVar

from fastapi import Request

F = TypeVar("F", bound=Callable[..., Any])


# ─── Mensagens padrão por método HTTP ────────────────────────────

DEFAULT_MESSAGES: dict[str, str] = {
    "GET": "Dados obtidos com sucesso.",
    "POST": "Recurso criado com sucesso.",
    "PUT": "Recurso atualizado com sucesso.",
    "PATCH": "Recurso atualizado com sucesso.",
    "DELETE": "Recurso removido com sucesso.",
}


def api_response(
    message: str | None = None,
    status_code: int | None = None,
    wrap_data: bool = True,
) -> Callable[[F], F]:
    """
    Decorator que envolve o retorno do endpoint no formato padronizado.
    
    Args:
        message: Mensagem customizada. Se None, usa a padrão do método HTTP.
        status_code: Status code da resposta. Se None, usa o padrão do método.
        wrap_data: Se False, retorna o valor bruto (útil para compatibilidade).
    
    Uso:
        @router.post("", response_model=ApiResponse[ToyResponse])
        @api_response(message="Toy created successfully.")
        def create_toy(...):
            return service.create(data)
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)
            return _wrap_result(result, message, status_code, kwargs)

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            return _wrap_result(result, message, status_code, kwargs)

        # Detecta se a função é async
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def _wrap_result(
    result: Any,
    message: str | None,
    status_code: int | None,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Envolve o resultado no formato padronizado."""
    
    # Se já é um dict com 'success', não wrapa de novo
    if isinstance(result, dict) and "success" in result:
        return result
    
    # Se é uma Response do FastAPI/Starlette, não wrapa
    if hasattr(result, "body") or hasattr(result, "status_code"):
        return result  # type: ignore

    # Detecta método HTTP do request (se disponível)
    request = kwargs.get("request")
    http_method = "GET"
    if isinstance(request, Request):
        http_method = request.method

    final_message = message or DEFAULT_MESSAGES.get(http_method, "Operação realizada com sucesso.")

    return {
        "success": True,
        "message": final_message,
        "data": result,
    }


# ─── Versão simplificada: decorator sem parâmetros ──────────────

def standard_response(func: F) -> F:
    """
    Decorator simplificado sem parâmetros.
    
    Uso:
        @router.get("/{id}")
        @standard_response
        def get_user(...):
            return service.get_by_id(id)
    """
    return api_response()(func)


# ─── Middleware opcional (envolve TODAS as respostas) ───────────

class StandardResponseMiddleware:
    """
    Middleware que envolve automaticamente todas as respostas JSON.
    
    ATENÇÃO: Pode conflitar com o decorator. Use um OU outro.
    """
    
    def __init__(self, app: Any):
        self.app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Intercepta a resposta
        
        async def wrapped_send(message: Any) -> None:
            print("MIddleware chamado")
            if message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    import json
                    try:
                        data = json.loads(body)
                        # Não wrapa se já está no formato ou é erro
                        if isinstance(data, dict) and "success" in data:
                            pass
                        elif isinstance(data, dict) and "error" in data:
                            pass
                        else:
                            wrapped = {
                                "success": True,
                                "message": "Operação realizada com sucesso.",
                                "data": data,
                            }
                            message["body"] = json.dumps(wrapped).encode()
                    except json.JSONDecodeError:
                        pass  # Não é JSON, deixa passar
            await send(message)

        await self.app(scope, receive, wrapped_send)
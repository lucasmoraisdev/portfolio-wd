"""
API Router do módulo de Toys.

Endpoints:
    # Públicos
    GET /public/toys              - Listar brinquedos ativos
    GET /public/toys/{slug}       - Detalhes de um brinquedo
    GET /public/toys/featured     - Listar destaques
    GET /public/toys/categories   - Listar categorias

    # Administrativos
    GET    /toys                  - Listar todos (admin)
    GET    /toys/{id}             - Detalhes (admin)
    POST   /toys                  - Criar
    PATCH  /toys/{id}             - Editar
    DELETE /toys/{id}             - Excluir
    PATCH  /toys/{id}/status      - Ativar/Desativar
    PATCH  /toys/{id}/featured    - Marcar/Remover destaque
    PATCH  /toys/{id}/position    - Alterar ordem
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.toys.constants import TOYS_PREFIX, TOYS_TAG
from app.modules.toys.service import ToyService
from app.modules.toys.repository import ToyRepository
from app.modules.toys.schemas import (
    ToyCreate,
    ToyUpdate,
    ToyFilter,
    ToyResponse,
    ToyPublicResponse,
    ToyStatusResponse,
    ToyFeaturedResponse,
    ToyPositionResponse,
)
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=TOYS_PREFIX,
    tags=[TOYS_TAG],
)

def get_toy_service(
    db: Session = Depends(get_db),
) -> ToyService:
    """Factory para ToyService."""
    repository = ToyRepository(db)
    return ToyService(repository)


# Publicos

@router.get(
    "/public",
    response_model=ApiResponse[dict],
)
@api_response(message="Brinquedos listados com sucesso.")
def list_public_toys(
    filters: ToyFilter = Depends(),
    service: ToyService = Depends(get_toy_service),
) -> dict:
    """
    Lista brinquedos ativos para o site.

    Filtros disponíveis:
        - search: busca por nome
        - category: filtra por categoria
        - min_age / max_age: faixa etária
        - page / per_page: paginação
    """
    items, total = service.list_public(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Brinquedos listados com sucesso.",
    )

@router.get(
    "/public/toys/{slug}",
    response_model=ApiResponse[ToyPublicResponse],
)
@api_response(message="Brinquedo encontrado com sucesso.")
def get_public_toy(
    slug: str,
    service: ToyService = Depends(get_toy_service),
) -> ToyPublicResponse:
    """Retorna detalhes de um brinquedo público pelo slug."""
    return service.get_by_slug(slug)

@router.get(
    "/public/toys/featured",
    response_model=ApiResponse[list[ToyPublicResponse]],
)
@api_response(message="Destaques obtidos com sucesso.")
def list_featured_toys(
    limit: int = 10,
    service: ToyService = Depends(get_toy_service),
) -> list[ToyPublicResponse]:
    """Lista brinquedos em destaque."""
    return service.list_featured(limit)

@router.get(
    "/public/toys/categories",
    response_model=ApiResponse[list[str]],
)
@api_response(message="Categorias obtidas com sucesso.")
def list_categories(
    service: ToyService = Depends(get_toy_service),
) -> list[str]:
    """Lista todas as categorias disponíveis."""
    return service.list_categories()

#ADMIN

@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="Brinquedos listados com sucesso.")
def list_admin_toys(
    filters: ToyFilter = Depends(),
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> dict:
    """
    Lista todos os brinquedos (admin).

    Inclui inativos e permite filtros completos.
    """
    items, total = service.list_admin(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Brinquedos listados com sucesso.",
    )


@router.get(
    "/{toy_id}",
    response_model=ApiResponse[ToyResponse],
)
@api_response(message="Brinquedo encontrado com sucesso.")
def get_admin_toy(
    toy_id: UUID,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyResponse:
    """Retorna detalhes completos de um brinquedo (admin)."""
    return service.get_by_id(toy_id)


@router.post(
    "",
    response_model=ApiResponse[ToyResponse],
    status_code=status.HTTP_201_CREATED,
)
@api_response(message="Brinquedo criado com sucesso.", status_code=201)
def create_toy(
    payload: ToyCreate,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyResponse:
    """Cria um novo brinquedo."""
    return service.create(payload)


@router.patch(
    "/{toy_id}",
    response_model=ApiResponse[ToyResponse],
)
@api_response(message="Brinquedo atualizado com sucesso.")
def update_toy(
    toy_id: UUID,
    payload: ToyUpdate,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyResponse:
    """Atualiza um brinquedo existente (parcial)."""
    return service.update(toy_id, payload)


@router.delete(
    "/{toy_id}",
    response_model=ApiResponse[dict],
)
@api_response(message="Brinquedo removido com sucesso.")
def delete_toy(
    toy_id: UUID,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> dict:
    """Remove um brinquedo (soft delete)."""
    service.delete(toy_id)
    return {"deleted": True, "id": str(toy_id)}


@router.patch(
    "/{toy_id}/status",
    response_model=ApiResponse[ToyStatusResponse],
)
@api_response(message="Status alterado com sucesso.")
def toggle_toy_status(
    toy_id: UUID,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyStatusResponse:
    """Ativa ou desativa um brinquedo."""
    return service.toggle_status(toy_id)


@router.patch(
    "/{toy_id}/featured",
    response_model=ApiResponse[ToyFeaturedResponse],
)
@api_response(message="Destaque alterado com sucesso.")
def toggle_toy_featured(
    toy_id: UUID,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyFeaturedResponse:
    """Marca ou remove um brinquedo dos destaques."""
    return service.toggle_featured(toy_id)


@router.patch(
    "/{toy_id}/position",
    response_model=ApiResponse[ToyPositionResponse],
)
@api_response(message="Posição alterada com sucesso.")
def update_toy_position(
    toy_id: UUID,
    new_order: int,
    service: ToyService = Depends(get_toy_service),
    current_user=Depends(get_current_user),
) -> ToyPositionResponse:
    """Altera a ordem de exibição de um brinquedo."""
    return service.update_position(toy_id, new_order)
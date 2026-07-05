from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.modules.user.repository import UserRepository
from app.modules.user.schemas import (
    UserCreate,
    UserFilter,
    UserResponse,
    UserUpdate,
    UserApiResponse
)
from app.modules.user.service import UserService
from app.modules.user.constants import USER_PREFIX, USER_TAG
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response

router = APIRouter(
    prefix=USER_PREFIX,
    tags=[USER_TAG]
)

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    repository = UserRepository(db)
    return UserService(repository=repository)

# ─── LISTAR USUÁRIOS ─────────────────────────────────────────────
@router.get(
    "",
    response_model=UserApiResponse[dict]
)
@api_response(message="Users listed successfully")
def list_users(
    filters: UserFilter = Depends(),
    service: UserService = Depends(get_user_service)
) -> dict:
    """
    Lista usuários com filtros e paginação.

    Retorna:
    {
        "success": true,
        "message": "users listed successfuly",
        "data": {
            "items": [...],
            "pagination": { "total": 10, "page": 1, "per_page": 20, "total_pages": 1}
        }
    }
    """
    items, total = service.list(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Users listed successfully"
    )

# ─── OBTER USUÁRIO POR ID ────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserApiResponse[UserResponse]
)
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.get_by_id(user_id)

# ─── CRIAR USUÁRIO ───────────────────────────────────────────────
@router.post(
    "",
    response_model=UserApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.create(payload)

# ─── ATUALIZAR USUÁRIO ───────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserApiResponse[UserResponse],
)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.update(user_id, payload)

# ─── DELETAR USUÁRIO ───────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=ApiResponse[None]
)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> Response:
    service.delete(user_id)
    return None
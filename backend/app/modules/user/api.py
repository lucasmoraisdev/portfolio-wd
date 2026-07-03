from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.modules.user.repository import UserRepository
from app.modules.user.schemas import (
    UserCreate,
    UserFilter,
    UserResponse,
    UserUpdate
)
from app.modules.user.service import UserService
from app.modules.user.constants import USER_PREFIX, USER_TAG
from app.shared.database import get_db

router = APIRouter(
    prefix=USER_PREFIX,
    tags=[USER_TAG]
)

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    repository = UserRepository(db)
    return UserService(repository=repository)

@router.get(
    "",
    response_model=list[UserResponse]
)
def list_users(
    filters: UserFilter = Depends(),
    service: UserService = Depends(get_user_service)
) -> list[UserResponse]:
    return service.list[filters]

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.get_by_id(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.create(payload)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.update(user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> Response:
    service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
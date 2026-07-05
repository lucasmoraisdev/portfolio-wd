from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.modules.auth.constants import AUTH_PREFIX, AUTH_TAG
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    LoginRequest,
    MeResponse,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthMeApiResponse,
    AuthTokenApiResponse
)
from app.modules.auth.service import AuthService
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.shared.database import get_db
from app.shared.security.dependencies import get_current_user
from app.shared.responses import api_response, ApiResponse, paginated_response

router = APIRouter(
    prefix=AUTH_PREFIX,
    tags=[AUTH_TAG]
)

def get_auth_service(
    db: Session = Depends(get_db)
) -> AuthService:
    user_repository = UserRepository(db)
    repository = AuthRepository(user_repository)

    return AuthService(repository)

# ─── LOGIN ─────────────────────────────────────────────
@router.post(
    "/login",
    response_model=AuthTokenApiResponse[TokenResponse]
)
def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return service.login(payload)

# ─── ME ─────────────────────────────────────────────
@router.get(
    "/me",
    response_model=AuthMeApiResponse[MeResponse]
)
def me(
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
) -> MeResponse:
    return service.me(current_user)

# ─── LOGOUT ─────────────────────────────────────────────
@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    service: AuthService = Depends(get_auth_service),
) -> Response:
    service.logout()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ─── FORGOT-PASSWORD ─────────────────────────────────────────────
@router.post(
    "/forgot-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def forgot_password(
    payload: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
) -> Response:
    service.forgot_password(payload)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reset_password(
    payload: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service),
) -> Response:
    service.reset_password(payload)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
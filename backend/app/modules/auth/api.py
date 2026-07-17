from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.modules.auth.constants import AUTH_PREFIX, AUTH_TAG
from app.shared.responses.wrapper import api_response
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
from app.modules.auth.schemas.token_form import TokenFormResponse
from app.modules.auth.service import AuthService
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.shared.database import get_db
from app.shared.security.dependencies import get_current_user

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

# ─── TOKEN (OAuth2 form‑urlencoded, usado pelo Swagger) ──
@router.post(
    "/token",
    response_model=TokenFormResponse,
    include_in_schema=False,
)
def token(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
) -> TokenFormResponse:
    """
    Endpoint compatível com o fluxo OAuth2 password (form‑urlencoded).
    Usado exclusivamente pelo botão **Authorize** do Swagger.
    Mapeia `username` → `email`.
    """
    # Constrói um LoginRequest a partir dos dados do form
    login_req = LoginRequest(
        email=form.username,
        password=form.password,
    )
    result = service.login(login_req)
    return TokenFormResponse(access_token=result.access_token)


# ─── LOGIN ─────────────────────────────────────────────
@router.post(
    "/login",
    response_model=AuthTokenApiResponse
)
@api_response(message="Login realizado com sucesso.")
def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    response = service.login(payload)
    return response

# ─── ME ─────────────────────────────────────────────
@router.get(
    "/me",
    response_model=AuthMeApiResponse
)
@api_response(message="Dados do usuário obtidos com sucesso.")
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
from datetime import datetime, UTC, timedelta
from secrets import token_urlsafe

from app.modules.auth.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    ExpiredTokenException
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.modules.user.models import User
from app.shared.security.jwt import create_access_token
from app.shared.security.password import (
    get_password_hash,   
    verify_password
)

class AuthService:
    def __init__(self, repository: AuthRepository):
        self._repository = repository

    def login(self, credentials: LoginRequest) -> TokenResponse:
        user = self._repository.get_by_email(credentials.email)

        if user is None or not user.is_active:
            raise InvalidCredentialsException(())
        
        if not verify_password(
            credentials.password,
            user.hashed_password
        ):
            raise InvalidCredentialsException()
        
        token = create_access_token(
            subect=str(user.id)
        )

        return TokenResponse(
            access_token=token
        )
    
    def me(self, user: User) -> User:
        return user
    
    def logout(self) -> None:
        return
    
    def forgot_password(self, payload: ForgotPasswordRequest) -> None:
        user = self._repository.get_by_email(payload.email)

        if user is None:
            return
        
        user.password_reset_token = token_urlsafe(64)
        user.password_reset_expires_at = (
            datetime.now(UTC) + timedelta(hours=1)
        )

        self._repository.save(user)

        # TODO: Enviar email

    def reset_password(self, payload: ResetPasswordRequest) -> None:
        user = self._repository.get_by_reset_token(payload.token)

        if user is None:
            raise InvalidTokenException()
        
        if (
            user.password_reset_expires_at is None
            or user.password_reset_expires_at < datetime.now(UTC)
        ):
            raise ExpiredTokenException()
        
        user.hashed_password = get_password_hash(payload.password)

        user.password_reset_token = None
        user.password_reset_expires_at = None
        
        self._repository.save(user)
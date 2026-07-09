"""
Dependências de segurança compartilhadas.

Usadas como guards em endpoints protegidos;
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.shared.database import get_db
from app.shared.security.jwt import decode_access_token
from app.shared.exceptions import (
    InvalidTokenException,
    UserInactiveException,
    UserNotFoundException
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    # 1. decodificar
    payload = decode_access_token(token)

    if not payload:
        raise InvalidTokenException()
    
    # 2. verificar o sub
    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenException("Token malformado: sub")

    #3. buscando o usuario
    user = UserRepository(db).get_by_id(user_id)

    if user is None:
        raise UserNotFoundException(user_id)
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UserInactiveException()
    
    return current_user
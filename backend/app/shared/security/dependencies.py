from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.shared.database import get_db
from app.shared.security.jwt import decode_access_token
from app.modules.auth.exceptions import InvalidCredentialsException
from app.modules.user.exceptions import UserInactiveException

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)

    user = UserRepository(db).get_by_id(payload["sub"])

    if user is None:
        raise InvalidCredentialsException()
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UserInactiveException()
    
    return current_user
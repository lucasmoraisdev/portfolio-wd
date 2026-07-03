from datetime import UTC, datetime, timedelta
from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = settings.jwt.algorithm
SECRET_KEY = settings.jwt.secret_key
ACCESS_TOKEN_EXPIRES_MINUTES = (
    settings.jwt.access_token_expire_minutes
)

def create_access_token(
    subject: str,
) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRES_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(UTC)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_access_token(
    token: str,
) -> dict:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError as e:
        raise ValueError("Invalid token.") from e
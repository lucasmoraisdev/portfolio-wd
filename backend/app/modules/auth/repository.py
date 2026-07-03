from app.modules.user.models import User
from app.modules.user.repository import UserRepository

class AuthRepository:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_by_email(self, email: str) -> User | None:
        return self._repository.get_by_email(email)
    
    def get_by_reset_token(self, token: str) -> User | None:
        return self._repository.get_by_reset_token(token)
    
    def save(self, user: User) -> User:
        return self._repository.update(user)
from uuid import UUID

from app.modules.user.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException
)
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import (
    UserCreate,
    UserFilter,
    UserUpdate,
)

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create(self, data: UserCreate) -> User:
        if self._repository.exists_by_email(data.email):
            raise UserAlreadyExistsException(email=data.email)
        
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=data.password
        )

        return self._repository.create(user)
    
    def get_by_id(self, user_id: UUID) -> User:
        user = self._repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException(user_id=user_id)
        
        return user
    
    def get_by_id(self, email: str) -> User:
        user = self._repository.get_by_email(email)

        if user is None:
            raise UserNotFoundException(email=email)
        
        return user
    
    def list(self, filters: UserFilter) -> list[User]:
        return self._repository.list(
            page=filters.page,
            page_size=filters.page_size,
            is_active=filters.is_active
        )
    
    def update(self, user_id: UUID, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)

        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = self._repository.get_by_email(update_data["email"])

            if existing and existing.id != user.id:
                raise UserAlreadyExistsException(update_data["email"])
            
        for f, v in update_data.items():
            setattr(user, "hashed_password" if f == "password" else f, v)

        return self._repository.update(user)
    
    def delete(self, user_id: UUID) -> None:
        user = self.get_by_id(user_id)
        self._repository.delete(user)
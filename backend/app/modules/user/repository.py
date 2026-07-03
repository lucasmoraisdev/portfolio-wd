from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.user.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        self._db.commit()
        self._db.refresh(user)
        return user
    
    def delete(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()

    def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self._db.scalar(stmt)
    
    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self._db.scalar(stmt)
    
    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = None
    ) -> list[User]:
        stmt = select(User) if is_active is None else select(User).where(User.is_active == is_active)

        stmt = (
            stmt
            .order_by(User.name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return list(self._db.scalars(stmt).all())
    
    def exists_by_email(self, email: str) -> bool:
        stmt = select(User.id).where(User.email == email)

        return self._db.scalar(stmt) is not None
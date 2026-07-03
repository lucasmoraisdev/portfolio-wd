from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.user.constants import USER_TABLE__NAME
from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey

class User(Base, TimestampMixin):
    __tablename__ = USER_TABLE__NAME

    id: Mapped[PrimaryKey]
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, server_default="true")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
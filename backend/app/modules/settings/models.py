from typing import Any

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from .constants import SETTINGS_TABLE_NAME

from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey

class SettingModel(Base, TimestampMixin):
    __tablename__ = SETTINGS_TABLE_NAME
    
    id: Mapped[PrimaryKey]
    key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    value: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="string")
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<Setting(id={self.id}, key={self.key}, value={self.value}, is_public={self.is_public})>"
    
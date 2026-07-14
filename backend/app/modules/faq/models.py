from sqlalchemy import Boolean, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .constants import FAQ_TABLE_NAME
from app.shared.database import Base
from app.shared.database.mixins import TimestampMixin
from app.shared.database.types import PrimaryKey

class FAQ(Base, TimestampMixin):
    __tablename__ = FAQ_TABLE_NAME

    id: Mapped[PrimaryKey]
    question: Mapped[str] = mapped_column(String(300), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)

    def __repr__(self) -> str:
        return f"<FAQ(id={self.id}, question={self.question[:30]}...)>"

from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.modules.contacts.models import ContactMessage
from app.modules.contacts.schemas import ContactFilter

class ContactRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, message: ContactMessage) -> ContactMessage:
        self._db.add(message)
        self._db.commit()
        self._db.refresh(message)
        return message

    def get_by_id(self, message_id: UUID) -> ContactMessage | None:
        stmt = select(ContactMessage).where(ContactMessage.id == message_id)
        return self._db.execute(stmt).scalar_one_or_none()

    def list_all(
        self,
        filters: ContactFilter | None = None,
    ) -> tuple[Sequence[ContactMessage], int]:
        filters = filters or ContactFilter()
        stmt = select(ContactMessage)

        # Filters
        if filters.search:
            search_term = f"%{filters.search}%"
            stmt = stmt.where(
                ContactMessage.name.ilike(search_term) |
                ContactMessage.email.ilike(search_term) |
                ContactMessage.subject.ilike(search_term) |
                ContactMessage.message.ilike(search_term)
            )

        if filters.is_read is not None:
            stmt = stmt.where(ContactMessage.is_read == filters.is_read)

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self._db.execute(count_stmt).scalar() or 0

        # Ordering
        order_column = getattr(ContactMessage, filters.order_by, ContactMessage.created_at)
        if filters.order_direction == "desc":
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column.asc())

        # Pagination
        offset = (filters.page - 1) * filters.per_page
        stmt = stmt.offset(offset).limit(filters.per_page)

        items = self._db.execute(stmt).scalars().all()
        return items, total

    def update(self, message: ContactMessage) -> ContactMessage:
        self._db.commit()
        self._db.refresh(message)
        return message

    def delete(self, message_id: UUID) -> bool:
        message = self.get_by_id(message_id)
        if not message:
            return False
        self._db.delete(message)
        self._db.commit()
        return True

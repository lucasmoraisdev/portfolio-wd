from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.modules.faq.models import FAQ
from app.modules.faq.schemas import FAQFilter

class FAQRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, faq: FAQ) -> FAQ:
        self._db.add(faq)
        self._db.commit()
        self._db.refresh(faq)
        return faq

    def get_by_id(self, faq_id: UUID) -> FAQ | None:
        stmt = select(FAQ).where(FAQ.id == faq_id)
        return self._db.execute(stmt).scalar_one_or_none()

    def list_all(
        self,
        filters: FAQFilter | None = None,
        only_active: bool = False,
    ) -> tuple[Sequence[FAQ], int]:
        filters = filters or FAQFilter()
        stmt = select(FAQ)

        # Filters
        if filters.search:
            search_term = f"%{filters.search}%"
            stmt = stmt.where(
                FAQ.question.ilike(search_term) |
                FAQ.answer.ilike(search_term)
            )

        if only_active or filters.is_active is not None:
            stmt = stmt.where(FAQ.is_active == (filters.is_active if filters.is_active is not None else True))

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self._db.execute(count_stmt).scalar() or 0

        # Ordering
        order_column = getattr(FAQ, filters.order_by, FAQ.display_order)
        if filters.order_direction == "desc":
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column.asc())

        # Pagination
        offset = (filters.page - 1) * filters.per_page
        stmt = stmt.offset(offset).limit(filters.per_page)

        items = self._db.execute(stmt).scalars().all()
        return items, total

    def update(self, faq: FAQ) -> FAQ:
        self._db.commit()
        self._db.refresh(faq)
        return faq

    def delete(self, faq_id: UUID) -> bool:
        faq = self.get_by_id(faq_id)
        if not faq:
            return False
        self._db.delete(faq)
        self._db.commit()
        return True

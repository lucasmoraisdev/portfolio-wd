from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.modules.testimonials.models import Testimonials
from app.modules.testimonials.schemas import TestimonialFilter

class TestimonialRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, testimonial: Testimonials) -> Testimonials:
        self._db.add(testimonial)
        self._db.commit()
        self._db.refresh(testimonial)
        return testimonial

    def get_by_id(self, testimonial_id: UUID) -> Testimonials | None:
        stmt = (
            select(Testimonials)
            .options(joinedload(Testimonials.photo))
            .where(Testimonials.id == testimonial_id)
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def list_all(
        self,
        filters: TestimonialFilter | None = None,
        only_active: bool = False,
    ) -> tuple[Sequence[Testimonials], int]:
        filters = filters or TestimonialFilter()
        stmt = select(Testimonials)

        # Filters
        if filters.search:
            search_term = f"%{filters.search}%"
            stmt = stmt.where(
                Testimonials.name.ilike(search_term) |
                Testimonials.testimonial.ilike(search_term)
            )

        if only_active or filters.is_active is not None:
            stmt = stmt.where(Testimonials.is_active == (filters.is_active if filters.is_active is not None else True))

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self._db.execute(count_stmt).scalar() or 0

        # Ordering
        order_column = getattr(Testimonials, filters.order_by, Testimonials.display_order)
        if filters.order_direction == "desc":
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column.asc())

        # Pagination
        offset = (filters.page - 1) * filters.per_page
        stmt = stmt.offset(offset).limit(filters.per_page)

        items = self._db.execute(stmt).scalars().all()
        return items, total

    def update(self, testimonial: Testimonials) -> Testimonials:
        self._db.commit()
        self._db.refresh(testimonial)
        return testimonial

    def delete(self, testimonial_id: UUID) -> bool:
        testimonial = self.get_by_id(testimonial_id)
        if not testimonial:
            return False
        self._db.delete(testimonial)
        self._db.commit()
        return True

from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.modules.events.models import Events
from app.modules.events.schemas import EventFilter
from app.modules.upload.models import Upload

class EventRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, event: Events) -> Events:
        self._db.add(event)
        self._db.commit()
        self._db.refresh(event)
        return event

    def get_by_id(self, event_id: UUID) -> Events | None:
        stmt = (
            select(Events)
            .options(joinedload(Events.cover_image))
            .where(Events.id == event_id)
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def list_all(
        self,
        filters: EventFilter | None = None,
        only_active: bool = False,
        only_featured: bool = False,
    ) -> tuple[Sequence[Events], int]:
        filters = filters or EventFilter()
        stmt = select(Events)

        # Filters
        if filters.search:
            search_term = f"%{filters.search}%"
            stmt = stmt.where(
                Events.title.ilike(search_term) |
                Events.city.ilike(search_term) |
                Events.client.ilike(search_term)
            )

        if only_active or filters.is_active is not None:
            stmt = stmt.where(Events.is_active == (filters.is_active if filters.is_active is not None else True))

        if only_featured or filters.is_featured is not None:
            stmt = stmt.where(Events.is_featured == (filters.is_featured if filters.is_featured is not None else True))

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self._db.execute(count_stmt).scalar() or 0

        # Ordering
        order_column = getattr(Events, filters.order_by, Events.display_order)
        if filters.order_direction == "desc":
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column.asc())

        # Pagination
        offset = (filters.page - 1) * filters.per_page
        stmt = stmt.offset(offset).limit(filters.per_page)

        items = self._db.execute(stmt).scalars().all()
        return items, total

    def list_featured(self, limit: int = 10) -> Sequence[Events]:
        stmt = (
            select(Events)
            .where(
                Events.is_featured,
                Events.is_active,
            )
            .order_by(Events.display_order.asc())
            .limit(limit)
        )
        return self._db.execute(stmt).scalars().all()

    def update(self, event: Events) -> Events:
        self._db.commit()
        self._db.refresh(event)
        return event

    def delete(self, event_id: UUID) -> bool:
        event = self.get_by_id(event_id)
        if not event:
            return False
        self._db.delete(event)
        self._db.commit()
        return True

    def resolve_image_urls(self, image_ids: list[UUID]) -> list[str]:
        if not image_ids:
            return []
        stmt = select(Upload.public_url).where(Upload.id.in_(image_ids))
        return list(self._db.execute(stmt).scalars().all())

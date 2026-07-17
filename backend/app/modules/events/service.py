import logging
from uuid import UUID

from app.modules.events.models import Events
from app.modules.events.repository import EventRepository
from app.modules.events.schemas import (
    EventCreate,
    EventUpdate,
    EventFilter,
    EventResponse,
    EventPublicResponse,
    EventStatusResponse,
    EventFeaturedResponse,
    EventPositionResponse,
)
from app.shared.exceptions import EventNotFoundException, EventDisplayOrderAlreadyExistsException

logger = logging.getLogger(__name__)

class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def _get_event_or_raise(self, event_id: UUID) -> Events:
        event = self.repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundException(str(event_id))
        return event

    def _to_public_response(self, event: Events) -> EventPublicResponse:
        cover_url = None
        if event.cover_image_id:
            from app.core.config import settings
            cover_url = f"{settings.app.base_url}{settings.app.api_prefix}/uploads/{event.cover_image_id}/file"
        gallery_urls = []
        if event.gallery_image_ids:
            gallery_urls = self.repository.resolve_image_urls(event.gallery_image_ids)

        return EventPublicResponse(
            id=event.id,
            title=event.title,
            city=event.city,
            client=event.client,
            event_date=event.event_date,
            description=event.description,
            cover_image_url=cover_url,
            gallery_image_urls=gallery_urls,
        )

    def _to_admin_response(self, event: Events) -> EventResponse:
        cover_url = None
        if event.cover_image_id:
            from app.core.config import settings
            cover_url = f"{settings.app.base_url}{settings.app.api_prefix}/uploads/{event.cover_image_id}/file"
        gallery_urls = []
        if event.gallery_image_ids:
            gallery_urls = self.repository.resolve_image_urls(event.gallery_image_ids)

        return EventResponse(
            id=event.id,
            title=event.title,
            city=event.city,
            client=event.client,
            event_date=event.event_date,
            description=event.description,
            is_featured=event.is_featured,
            is_active=event.is_active,
            display_order=event.display_order,
            cover_image_id=event.cover_image_id,
            gallery_image_ids=event.gallery_image_ids,
            created_at=event.created_at,
            updated_at=event.updated_at,
            cover_image_url=cover_url,
            gallery_urls=gallery_urls,
        )

    def create(self, data: EventCreate) -> EventResponse:
        # Check display order duplicate
        if data.display_order is not None:
            existing = self.repository.get_by_display_order(data.display_order)
            if existing:
                raise EventDisplayOrderAlreadyExistsException(data.display_order)

        event = Events(
            title=data.title,
            city=data.city,
            client=data.client,
            event_date=data.event_date,
            description=data.description,
            is_featured=data.is_featured,
            is_active=data.is_active,
            display_order=data.display_order,
            cover_image_id=data.cover_image_id,
            gallery_image_ids=data.gallery_image_ids or [],
        )
        created = self.repository.create(event)
        logger.info("Evento criado: %s", created.title)
        return self._to_admin_response(created)

    def get_by_id(self, event_id: UUID) -> EventResponse:
        event = self._get_event_or_raise(event_id)
        return self._to_admin_response(event)

    def list_admin(self, filters: EventFilter) -> tuple[list[EventResponse], int]:
        items, total = self.repository.list_all(filters)
        responses = [self._to_admin_response(x) for x in items]
        return responses, total

    def list_public(self, filters: EventFilter) -> tuple[list[EventPublicResponse], int]:
        filters.is_active = True
        items, total = self.repository.list_all(filters)
        responses = [self._to_public_response(x) for x in items]
        return responses, total

    def list_featured(self, limit: int = 10) -> list[EventPublicResponse]:
        items = self.repository.list_featured(limit)
        return [self._to_public_response(x) for x in items]

    def update(self, event_id: UUID, data: EventUpdate) -> EventResponse:
        event = self._get_event_or_raise(event_id)

        # Check display order duplicate
        if data.display_order is not None:
            existing = self.repository.get_by_display_order(data.display_order)
            if existing and existing.id != event_id:
                raise EventDisplayOrderAlreadyExistsException(data.display_order)

        update_fields = [
            "title", "city", "client", "event_date", "description",
            "is_featured", "is_active", "display_order",
            "cover_image_id", "gallery_image_ids"
        ]

        for field in update_fields:
            val = getattr(data, field)
            if val is not None:
                setattr(event, field, val)

        updated = self.repository.update(event)
        logger.info("Evento atualizado: %s", updated.id)
        return self._to_admin_response(updated)

    def delete(self, event_id: UUID) -> bool:
        self._get_event_or_raise(event_id)
        result = self.repository.delete(event_id)
        if result:
            logger.info("Evento removido: %s", event_id)
        return result

    def toggle_status(self, event_id: UUID) -> EventStatusResponse:
        event = self._get_event_or_raise(event_id)
        event.is_active = not event.is_active
        updated = self.repository.update(event)
        status_text = "ativado" if updated.is_active else "desativado"
        return EventStatusResponse(
            id=updated.id,
            is_active=updated.is_active,
            message=f"Evento {status_text} com sucesso.",
        )

    def toggle_featured(self, event_id: UUID) -> EventFeaturedResponse:
        event = self._get_event_or_raise(event_id)
        event.is_featured = not event.is_featured
        updated = self.repository.update(event)
        status_text = "marcado como destaque" if updated.is_featured else "removido dos destaques"
        return EventFeaturedResponse(
            id=updated.id,
            is_featured=updated.is_featured,
            message=f"Evento {status_text}.",
        )

    def update_position(self, event_id: UUID, new_order: int) -> EventPositionResponse:
        event = self._get_event_or_raise(event_id)
        event.display_order = new_order
        updated = self.repository.update(event)
        return EventPositionResponse(
            id=updated.id,
            display_order=updated.display_order,
            message=f"Ordem atualizada para {new_order}.",
        )

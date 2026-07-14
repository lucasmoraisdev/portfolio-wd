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
from app.shared.exceptions import EventNotFoundException

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
        cover_url = event.cover_image.public_url if event.cover_image else None
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

    def create(self, data: EventCreate) -> EventResponse:
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
        return EventResponse.model_validate(created)

    def get_by_id(self, event_id: UUID) -> EventResponse:
        event = self._get_event_or_raise(event_id)
        return EventResponse.model_validate(event)

    def list_admin(self, filters: EventFilter) -> tuple[list[EventResponse], int]:
        items, total = self.repository.list_all(filters)
        responses = [EventResponse.model_validate(x) for x in items]
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
        return EventResponse.model_validate(updated)

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

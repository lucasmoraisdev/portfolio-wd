from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.events.constants import EVENTS_PREFIX, EVENTS_TAG
from app.modules.events.service import EventService
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
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=EVENTS_PREFIX,
    tags=[EVENTS_TAG],
)

def get_event_service(
    db: Session = Depends(get_db),
) -> EventService:
    repository = EventRepository(db)
    return EventService(repository)


# Públicos

@router.get(
    "/public/events",
    response_model=ApiResponse[dict],
)
@api_response(message="Eventos listados com sucesso.")
def list_public_events(
    filters: EventFilter = Depends(),
    service: EventService = Depends(get_event_service),
) -> dict:
    items, total = service.list_public(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Eventos listados com sucesso.",
    )

@router.get(
    "/public/events/featured",
    response_model=ApiResponse[list[EventPublicResponse]],
)
@api_response(message="Eventos em destaque obtidos com sucesso.")
def list_featured_events(
    limit: int = 10,
    service: EventService = Depends(get_event_service),
) -> list[EventPublicResponse]:
    return service.list_featured(limit)

@router.get(
    "/public/events/{event_id}",
    response_model=ApiResponse[EventPublicResponse],
)
@api_response(message="Evento encontrado com sucesso.")
def get_public_event(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
) -> EventPublicResponse:
    return service._to_public_response(service._get_event_or_raise(event_id))


# Admin

@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="Eventos listados com sucesso.")
def list_admin_events(
    filters: EventFilter = Depends(),
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> dict:
    items, total = service.list_admin(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Eventos listados com sucesso.",
    )

@router.get(
    "/{event_id}",
    response_model=ApiResponse[EventResponse],
)
@api_response(message="Evento encontrado com sucesso.")
def get_admin_event(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventResponse:
    return service.get_by_id(event_id)

@router.post(
    "",
    response_model=ApiResponse[EventResponse],
    status_code=status.HTTP_201_CREATED,
)
@api_response(message="Evento criado com sucesso.", status_code=201)
def create_event(
    payload: EventCreate,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventResponse:
    return service.create(payload)

@router.patch(
    "/{event_id}",
    response_model=ApiResponse[EventResponse],
)
@api_response(message="Evento atualizado com sucesso.")
def update_event(
    event_id: UUID,
    payload: EventUpdate,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventResponse:
    return service.update(event_id, payload)

@router.delete(
    "/{event_id}",
    response_model=ApiResponse[dict],
)
@api_response(message="Evento removido com sucesso.")
def delete_event(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> dict:
    service.delete(event_id)
    return {"deleted": True, "id": str(event_id)}

@router.patch(
    "/{event_id}/status",
    response_model=ApiResponse[EventStatusResponse],
)
@api_response(message="Status alterado com sucesso.")
def toggle_event_status(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventStatusResponse:
    return service.toggle_status(event_id)

@router.patch(
    "/{event_id}/featured",
    response_model=ApiResponse[EventFeaturedResponse],
)
@api_response(message="Destaque alterado com sucesso.")
def toggle_event_featured(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventFeaturedResponse:
    return service.toggle_featured(event_id)

@router.patch(
    "/{event_id}/position",
    response_model=ApiResponse[EventPositionResponse],
)
@api_response(message="Posição alterada com sucesso.")
def update_event_position(
    event_id: UUID,
    new_order: int,
    service: EventService = Depends(get_event_service),
    current_user=Depends(get_current_user),
) -> EventPositionResponse:
    return service.update_position(event_id, new_order)

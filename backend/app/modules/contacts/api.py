from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.contacts.constants import CONTACTS_PREFIX, CONTACTS_TAG
from app.modules.contacts.service import ContactService
from app.modules.contacts.repository import ContactRepository
from app.modules.contacts.schemas import (
    ContactCreate,
    ContactResponse,
    ContactFilter,
    ContactStatusResponse,
)
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=CONTACTS_PREFIX,
    tags=[CONTACTS_TAG],
)

def get_contact_service(
    db: Session = Depends(get_db),
) -> ContactService:
    repository = ContactRepository(db)
    return ContactService(repository)


# Públicos

@router.post(
    "/public",
    response_model=ApiResponse[ContactResponse],
    status_code=status.HTTP_201_CREATED,
)
@api_response(message="Mensagem de contato enviada com sucesso.", status_code=201)
def create_public_contact(
    payload: ContactCreate,
    service: ContactService = Depends(get_contact_service),
) -> ContactResponse:
    return service.create(payload)


# Admin

@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="Mensagens de contato listadas com sucesso.")
def list_admin_contacts(
    filters: ContactFilter = Depends(),
    service: ContactService = Depends(get_contact_service),
    current_user=Depends(get_current_user),
) -> dict:
    items, total = service.list_admin(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Mensagens de contato listadas com sucesso.",
    )

@router.get(
    "/{message_id}",
    response_model=ApiResponse[ContactResponse],
)
@api_response(message="Mensagem de contato encontrada com sucesso.")
def get_admin_contact(
    message_id: UUID,
    service: ContactService = Depends(get_contact_service),
    current_user=Depends(get_current_user),
) -> ContactResponse:
    return service.get_by_id(message_id)

@router.patch(
    "/{message_id}/read",
    response_model=ApiResponse[ContactStatusResponse],
)
@api_response(message="Mensagem marcada como lida com sucesso.")
def mark_contact_read(
    message_id: UUID,
    service: ContactService = Depends(get_contact_service),
    current_user=Depends(get_current_user),
) -> ContactStatusResponse:
    return service.mark_as_read(message_id)

@router.delete(
    "/{message_id}",
    response_model=ApiResponse[dict],
)
@api_response(message="Mensagem de contato removida com sucesso.")
def delete_contact(
    message_id: UUID,
    service: ContactService = Depends(get_contact_service),
    current_user=Depends(get_current_user),
) -> dict:
    service.delete(message_id)
    return {"deleted": True, "id": str(message_id)}

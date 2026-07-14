from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.faq.constants import FAQ_PREFIX, FAQ_TAG
from app.modules.faq.service import FAQService
from app.modules.faq.repository import FAQRepository
from app.modules.faq.schemas import (
    FAQCreate,
    FAQUpdate,
    FAQFilter,
    FAQResponse,
    FAQStatusResponse,
    FAQPositionResponse,
)
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=FAQ_PREFIX,
    tags=[FAQ_TAG],
)

def get_faq_service(
    db: Session = Depends(get_db),
) -> FAQService:
    repository = FAQRepository(db)
    return FAQService(repository)


# Públicos

@router.get(
    "/public/faqs",
    response_model=ApiResponse[dict],
)
@api_response(message="FAQs listados com sucesso.")
def list_public_faqs(
    filters: FAQFilter = Depends(),
    service: FAQService = Depends(get_faq_service),
) -> dict:
    items, total = service.list_public(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="FAQs listados com sucesso.",
    )


# Admin

@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="FAQs listados com sucesso.")
def list_admin_faqs(
    filters: FAQFilter = Depends(),
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> dict:
    items, total = service.list_admin(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="FAQs listados com sucesso.",
    )

@router.get(
    "/{faq_id}",
    response_model=ApiResponse[FAQResponse],
)
@api_response(message="FAQ encontrado com sucesso.")
def get_admin_faq(
    faq_id: UUID,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> FAQResponse:
    return service.get_by_id(faq_id)

@router.post(
    "",
    response_model=ApiResponse[FAQResponse],
    status_code=status.HTTP_201_CREATED,
)
@api_response(message="FAQ criado com sucesso.", status_code=201)
def create_faq(
    payload: FAQCreate,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> FAQResponse:
    return service.create(payload)

@router.patch(
    "/{faq_id}",
    response_model=ApiResponse[FAQResponse],
)
@api_response(message="FAQ atualizado com sucesso.")
def update_faq(
    faq_id: UUID,
    payload: FAQUpdate,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> FAQResponse:
    return service.update(faq_id, payload)

@router.delete(
    "/{faq_id}",
    response_model=ApiResponse[dict],
)
@api_response(message="FAQ removido com sucesso.")
def delete_faq(
    faq_id: UUID,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> dict:
    service.delete(faq_id)
    return {"deleted": True, "id": str(faq_id)}

@router.patch(
    "/{faq_id}/status",
    response_model=ApiResponse[FAQStatusResponse],
)
@api_response(message="Status alterado com sucesso.")
def toggle_faq_status(
    faq_id: UUID,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> FAQStatusResponse:
    return service.toggle_status(faq_id)

@router.patch(
    "/{faq_id}/position",
    response_model=ApiResponse[FAQPositionResponse],
)
@api_response(message="Posição alterada com sucesso.")
def update_faq_position(
    faq_id: UUID,
    new_order: int,
    service: FAQService = Depends(get_faq_service),
    current_user=Depends(get_current_user),
) -> FAQPositionResponse:
    return service.update_position(faq_id, new_order)

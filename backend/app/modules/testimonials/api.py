from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.testimonials.constants import TESTIMONIALS_PREFIX, TESTIMONIALS_TAG
from app.modules.testimonials.service import TestimonialService
from app.modules.testimonials.repository import TestimonialRepository
from app.modules.testimonials.schemas import (
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialFilter,
    TestimonialResponse,
    TestimonialStatusResponse,
    TestimonialPositionResponse,
)
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=TESTIMONIALS_PREFIX,
    tags=[TESTIMONIALS_TAG],
)

def get_testimonial_service(
    db: Session = Depends(get_db),
) -> TestimonialService:
    repository = TestimonialRepository(db)
    return TestimonialService(repository)


# Públicos

@router.get(
    "/public/testimonials",
    response_model=ApiResponse[dict],
)
@api_response(message="Depoimentos listados com sucesso.")
def list_public_testimonials(
    filters: TestimonialFilter = Depends(),
    service: TestimonialService = Depends(get_testimonial_service),
) -> dict:
    items, total = service.list_public(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Depoimentos listados com sucesso.",
    )


# Admin

@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="Depoimentos listados com sucesso.")
def list_admin_testimonials(
    filters: TestimonialFilter = Depends(),
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> dict:
    items, total = service.list_admin(filters)
    return paginated_response(
        items=items,
        total=total,
        page=filters.page,
        per_page=filters.per_page,
        message="Depoimentos listados com sucesso.",
    )

@router.get(
    "/{testimonial_id}",
    response_model=ApiResponse[TestimonialResponse],
)
@api_response(message="Depoimento encontrado com sucesso.")
def get_admin_testimonial(
    testimonial_id: UUID,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> TestimonialResponse:
    return service.get_by_id(testimonial_id)

@router.post(
    "",
    response_model=ApiResponse[TestimonialResponse],
    status_code=status.HTTP_201_CREATED,
)
@api_response(message="Depoimento criado com sucesso.", status_code=201)
def create_testimonial(
    payload: TestimonialCreate,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> TestimonialResponse:
    return service.create(payload)

@router.patch(
    "/{testimonial_id}",
    response_model=ApiResponse[TestimonialResponse],
)
@api_response(message="Depoimento atualizado com sucesso.")
def update_testimonial(
    testimonial_id: UUID,
    payload: TestimonialUpdate,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> TestimonialResponse:
    return service.update(testimonial_id, payload)

@router.delete(
    "/{testimonial_id}",
    response_model=ApiResponse[dict],
)
@api_response(message="Depoimento removido com sucesso.")
def delete_testimonial(
    testimonial_id: UUID,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> dict:
    service.delete(testimonial_id)
    return {"deleted": True, "id": str(testimonial_id)}

@router.patch(
    "/{testimonial_id}/status",
    response_model=ApiResponse[TestimonialStatusResponse],
)
@api_response(message="Status alterado com sucesso.")
def toggle_testimonial_status(
    testimonial_id: UUID,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> TestimonialStatusResponse:
    return service.toggle_status(testimonial_id)

@router.patch(
    "/{testimonial_id}/position",
    response_model=ApiResponse[TestimonialPositionResponse],
)
@api_response(message="Posição alterada com sucesso.")
def update_testimonial_position(
    testimonial_id: UUID,
    new_order: int,
    service: TestimonialService = Depends(get_testimonial_service),
    current_user=Depends(get_current_user),
) -> TestimonialPositionResponse:
    return service.update_position(testimonial_id, new_order)

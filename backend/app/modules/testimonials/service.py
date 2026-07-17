import logging
from uuid import UUID

from app.modules.testimonials.models import Testimonials
from app.modules.testimonials.repository import TestimonialRepository
from app.modules.testimonials.schemas import (
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialFilter,
    TestimonialResponse,
    TestimonialPublicResponse,
    TestimonialStatusResponse,
    TestimonialPositionResponse,
)
from app.shared.exceptions import TestimonialNotFoundException

logger = logging.getLogger(__name__)

class TestimonialService:
    def __init__(self, repository: TestimonialRepository) -> None:
        self.repository = repository

    def _get_testimonial_or_raise(self, testimonial_id: UUID) -> Testimonials:
        testimonial = self.repository.get_by_id(testimonial_id)
        if not testimonial:
            raise TestimonialNotFoundException(str(testimonial_id))
        return testimonial

    def _to_public_response(self, testimonial: Testimonials) -> TestimonialPublicResponse:
        photo_url = None
        if testimonial.photo_id:
            from app.core.config import settings
            photo_url = f"{settings.app.base_url}{settings.app.api_prefix}/uploads/{testimonial.photo_id}/file"
        return TestimonialPublicResponse(
            id=testimonial.id,
            name=testimonial.name,
            city=testimonial.city,
            company=testimonial.company,
            testimonial=testimonial.testimonial,
            rating=testimonial.rating,
            photo_url=photo_url,
        )

    def create(self, data: TestimonialCreate) -> TestimonialResponse:
        testimonial = Testimonials(
            name=data.name,
            city=data.city,
            company=data.company,
            testimonial=data.testimonial,
            rating=data.rating,
            is_active=data.is_active,
            display_order=data.display_order,
            photo_id=data.photo_id,
        )
        created = self.repository.create(testimonial)
        logger.info("Depoimento criado: %s", created.name)
        return TestimonialResponse.model_validate(created)

    def get_by_id(self, testimonial_id: UUID) -> TestimonialResponse:
        testimonial = self._get_testimonial_or_raise(testimonial_id)
        return TestimonialResponse.model_validate(testimonial)

    def list_admin(self, filters: TestimonialFilter) -> tuple[list[TestimonialResponse], int]:
        items, total = self.repository.list_all(filters)
        responses = [TestimonialResponse.model_validate(x) for x in items]
        return responses, total

    def list_public(self, filters: TestimonialFilter) -> tuple[list[TestimonialPublicResponse], int]:
        filters.is_active = True
        items, total = self.repository.list_all(filters)
        responses = [self._to_public_response(x) for x in items]
        return responses, total

    def update(self, testimonial_id: UUID, data: TestimonialUpdate) -> TestimonialResponse:
        testimonial = self._get_testimonial_or_raise(testimonial_id)

        update_fields = [
            "name", "city", "company", "testimonial", "rating",
            "is_active", "display_order", "photo_id"
        ]

        for field in update_fields:
            val = getattr(data, field)
            if val is not None:
                setattr(testimonial, field, val)

        updated = self.repository.update(testimonial)
        logger.info("Depoimento atualizado: %s", updated.id)
        return TestimonialResponse.model_validate(updated)

    def delete(self, testimonial_id: UUID) -> bool:
        self._get_testimonial_or_raise(testimonial_id)
        result = self.repository.delete(testimonial_id)
        if result:
            logger.info("Depoimento removido: %s", testimonial_id)
        return result

    def toggle_status(self, testimonial_id: UUID) -> TestimonialStatusResponse:
        testimonial = self._get_testimonial_or_raise(testimonial_id)
        testimonial.is_active = not testimonial.is_active
        updated = self.repository.update(testimonial)
        status_text = "ativado" if updated.is_active else "desativado"
        return TestimonialStatusResponse(
            id=updated.id,
            is_active=updated.is_active,
            message=f"Depoimento {status_text} com sucesso.",
        )

    def update_position(self, testimonial_id: UUID, new_order: int) -> TestimonialPositionResponse:
        testimonial = self._get_testimonial_or_raise(testimonial_id)
        testimonial.display_order = new_order
        updated = self.repository.update(testimonial)
        return TestimonialPositionResponse(
            id=updated.id,
            display_order=updated.display_order,
            message=f"Ordem atualizada para {new_order}.",
        )

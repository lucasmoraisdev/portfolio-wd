import logging
from uuid import UUID

from app.modules.faq.models import FAQ
from app.modules.faq.repository import FAQRepository
from app.modules.faq.schemas import (
    FAQCreate,
    FAQUpdate,
    FAQFilter,
    FAQResponse,
    FAQStatusResponse,
    FAQPositionResponse,
)
from app.shared.exceptions import FAQNotFoundException

logger = logging.getLogger(__name__)

class FAQService:
    def __init__(self, repository: FAQRepository) -> None:
        self.repository = repository

    def _get_faq_or_raise(self, faq_id: UUID) -> FAQ:
        faq = self.repository.get_by_id(faq_id)
        if not faq:
            raise FAQNotFoundException(str(faq_id))
        return faq

    def create(self, data: FAQCreate) -> FAQResponse:
        faq = FAQ(
            question=data.question,
            answer=data.answer,
            is_active=data.is_active,
            display_order=data.display_order,
        )
        created = self.repository.create(faq)
        logger.info("FAQ criado: %s", created.id)
        return FAQResponse.model_validate(created)

    def get_by_id(self, faq_id: UUID) -> FAQResponse:
        faq = self._get_faq_or_raise(faq_id)
        return FAQResponse.model_validate(faq)

    def list_admin(self, filters: FAQFilter) -> tuple[list[FAQResponse], int]:
        items, total = self.repository.list_all(filters)
        responses = [FAQResponse.model_validate(x) for x in items]
        return responses, total

    def list_public(self, filters: FAQFilter) -> tuple[list[FAQResponse], int]:
        filters.is_active = True
        items, total = self.repository.list_all(filters)
        responses = [FAQResponse.model_validate(x) for x in items]
        return responses, total

    def update(self, faq_id: UUID, data: FAQUpdate) -> FAQResponse:
        faq = self._get_faq_or_raise(faq_id)

        update_fields = ["question", "answer", "is_active", "display_order"]

        for field in update_fields:
            val = getattr(data, field)
            if val is not None:
                setattr(faq, field, val)

        updated = self.repository.update(faq)
        logger.info("FAQ atualizado: %s", updated.id)
        return FAQResponse.model_validate(updated)

    def delete(self, faq_id: UUID) -> bool:
        self._get_faq_or_raise(faq_id)
        result = self.repository.delete(faq_id)
        if result:
            logger.info("FAQ removido: %s", faq_id)
        return result

    def toggle_status(self, faq_id: UUID) -> FAQStatusResponse:
        faq = self._get_faq_or_raise(faq_id)
        faq.is_active = not faq.is_active
        updated = self.repository.update(faq)
        status_text = "ativado" if updated.is_active else "desativado"
        return FAQStatusResponse(
            id=updated.id,
            is_active=updated.is_active,
            message=f"FAQ {status_text} com sucesso.",
        )

    def update_position(self, faq_id: UUID, new_order: int) -> FAQPositionResponse:
        faq = self._get_faq_or_raise(faq_id)
        faq.display_order = new_order
        updated = self.repository.update(faq)
        return FAQPositionResponse(
            id=updated.id,
            display_order=updated.display_order,
            message=f"Ordem atualizada para {new_order}.",
        )

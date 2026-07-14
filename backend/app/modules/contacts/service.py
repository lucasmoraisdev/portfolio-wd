import logging
from uuid import UUID

from app.modules.contacts.models import ContactMessage
from app.modules.contacts.repository import ContactRepository
from app.modules.contacts.schemas import (
    ContactCreate,
    ContactResponse,
    ContactFilter,
    ContactStatusResponse,
)
from app.shared.exceptions import ContactMessageNotFoundException

logger = logging.getLogger(__name__)

class ContactService:
    def __init__(self, repository: ContactRepository) -> None:
        self.repository = repository

    def _get_message_or_raise(self, message_id: UUID) -> ContactMessage:
        message = self.repository.get_by_id(message_id)
        if not message:
            raise ContactMessageNotFoundException(str(message_id))
        return message

    def create(self, data: ContactCreate) -> ContactResponse:
        message = ContactMessage(
            name=data.name,
            email=data.email,
            phone=data.phone,
            subject=data.subject,
            message=data.message,
            is_read=False,
        )
        created = self.repository.create(message)
        logger.info("Nova mensagem de contato recebida de: %s (assunto: %s)", created.name, created.subject)
        return ContactResponse.model_validate(created)

    def get_by_id(self, message_id: UUID) -> ContactResponse:
        message = self._get_message_or_raise(message_id)
        return ContactResponse.model_validate(message)

    def list_admin(self, filters: ContactFilter) -> tuple[list[ContactResponse], int]:
        items, total = self.repository.list_all(filters)
        responses = [ContactResponse.model_validate(x) for x in items]
        return responses, total

    def delete(self, message_id: UUID) -> bool:
        self._get_message_or_raise(message_id)
        result = self.repository.delete(message_id)
        if result:
            logger.info("Mensagem de contato removida: %s", message_id)
        return result

    def mark_as_read(self, message_id: UUID) -> ContactStatusResponse:
        message = self._get_message_or_raise(message_id)
        message.is_read = True
        updated = self.repository.update(message)
        return ContactStatusResponse(
            id=updated.id,
            is_read=updated.is_read,
            message="Mensagem marcada como lida com sucesso.",
        )

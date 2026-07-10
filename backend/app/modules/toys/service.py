import logging
import re
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.toys.models import Toys
from app.modules.toys.repository import ToyRepository
from app.modules.toys.schemas import (
    ToyCreate,
    ToyUpdate,
    ToyFilter,
    ToyResponse,
    ToyPublicResponse,
    ToyStatusResponse,
    ToyFeaturedResponse,
    ToyPositionResponse,
)
from app.shared.exceptions import (
    ToyNotFoundException,
    ToySlugAlreadyExistsException,
    ToyNameAlreadyExistsException,
    InvalidAgeRangeException,
)

logger = logging.getLogger(__name__)


class ToyService:
    """
    Service de brinquedos.

    Responsável por:
    - Validação de dados
    - Geração automática de slug
    - CRUD completo
    - Conversão para schemas públicos/admin
    """

    def __init__(self, repository: ToyRepository) -> None:
        self.repository = repository

    @staticmethod
    def generate_slug(name: str) -> str:
        """
        Gera um slug a partir do nome.

        Ex: "Carrinho Hot Wheels" → "carrinho-hot-wheels"
        """
        slug = name.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)  # Remove caracteres especiais
        slug = re.sub(r"[\s_]+", "-", slug)    # Espaços → hífens
        slug = re.sub(r"-+", "-", slug)         # Múltiplos hífens → um
        slug = slug.strip("-")                    # Remove hífens das pontas
        return slug[:220]  # Limita tamanho

    def _ensure_unique_slug(self, slug: str, exclude_id: UUID | None = None) -> str:
        """
        Garante que o slug seja único, adicionando sufixo numérico se necessário.

        Ex: "carrinho" → "carrinho-2" → "carrinho-3"
        """
        original_slug = slug
        counter = 2

        while self.repository.slug_exists(slug, exclude_id):
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    def _get_toy_or_raise(self, toy_id: UUID) -> Toys:
        """Busca um brinquedo ou lança exceção."""
        toy = self.repository.get_by_id(toy_id)
        if not toy or toy.deleted_at:
            raise ToyNotFoundException(str(toy_id))
        return toy

    def _to_public_response(self, toy: Toys) -> ToyPublicResponse:
        """Converte Toys para resposta pública."""
        cover_url = None
        if toy.cover_image:
            cover_url = toy.cover_image.public_url

        gallery_urls = []

        return ToyPublicResponse(
            id=toy.id,
            name=toy.name,
            slug=toy.slug,
            category=toy.category,
            short_description=toy.short_description,
            min_age=toy.min_age,
            max_age=toy.max_age,
            capacity=toy.capacity,
            cover_image_url=cover_url,
            gallery_image_urls=gallery_urls,
            video_url=toy.video_url,
        )

    def create(self, data: ToyCreate) -> ToyResponse:
        """Cria um novo brinquedo."""
        # Verifica se nome já existe
        existing = self.repository.get_by_name(data.name)
        if existing:
            raise ToyNameAlreadyExistsException(data.name)

        # Gera slug único
        slug = self.generate_slug(data.name)
        slug = self._ensure_unique_slug(slug)

        # Cria o modelo
        toy = Toys(
            name=data.name,
            slug=slug,
            category=data.category,
            short_description=data.short_description,
            full_description=data.full_description,
            min_age=data.min_age,
            max_age=data.max_age,
            capacity=data.capacity,
            is_featured=data.is_featured,
            display_order=data.display_order,
            cover_image_id=data.cover_image_id,
            gallery_image_ids=data.gallery_image_ids or [],
            video_url=data.video_url,
            video_type=data.video_type,
        )

        created = self.repository.create(toy)
        logger.info("Brinquedo criado: %s (slug: %s)", created.name, created.slug)
        return ToyResponse.model_validate(created)

    def get_by_id(self, toy_id: UUID) -> ToyResponse:
        """Busca um brinquedo pelo ID."""
        toy = self._get_toy_or_raise(toy_id)
        return ToyResponse.model_validate(toy)

    def get_by_slug(self, slug: str) -> ToyPublicResponse:
        """Busca um brinquedo público pelo slug."""
        toy = self.repository.get_by_slug(slug)
        if not toy or not toy.is_active:
            raise ToyNotFoundException(slug=slug)
        return self._to_public_response(toy)

    def list_admin(self, filters: ToyFilter) -> tuple[list[ToyResponse], int]:
        """Lista brinquedos para administração."""
        items, total = self.repository.list_all(filters)
        responses = [ToyResponse.model_validate(t) for t in items]
        return responses, total

    def list_public(self, filters: ToyFilter) -> tuple[list[ToyPublicResponse], int]:
        """Lista brinquedos públicos."""
        filters.is_active = True
        items, total = self.repository.list_all(filters)
        responses = [self._to_public_response(t) for t in items]
        return responses, total

    def list_featured(self, limit: int = 10) -> list[ToyPublicResponse]:
        """Lista brinquedos em destaque."""
        items = self.repository.list_featured(limit)
        return [self._to_public_response(t) for t in items]

    def list_categories(self) -> list[str]:
        """Lista categorias disponíveis."""
        return self.repository.list_categories()

    def update(self, toy_id: UUID, data: ToyUpdate) -> ToyResponse:
        """Atualiza um brinquedo existente."""
        toy = self._get_toy_or_raise(toy_id)

        # Verifica nome duplicado
        if data.name and data.name != toy.name:
            existing = self.repository.get_by_name(data.name)
            if existing and existing.id != toy_id:
                raise ToyNameAlreadyExistsException(data.name)

        # Atualiza slug se nome mudou
        if data.name and data.name != toy.name:
            new_slug = self.generate_slug(data.name)
            new_slug = self._ensure_unique_slug(new_slug, exclude_id=toy_id)
            toy.slug = new_slug

        # Atualiza campos
        update_fields = [
            "name", "category", "short_description", "full_description",
            "min_age", "max_age", "capacity", "is_featured", "is_active",
            "display_order", "cover_image_id", "gallery_image_ids",
            "video_url", "video_type",
        ]

        for field in update_fields:
            value = getattr(data, field)
            if value is not None:
                setattr(toy, field, value)

        updated = self.repository.update(toy)
        logger.info("Brinquedo atualizado: %s", updated.id)
        return ToyResponse.model_validate(updated)

    def delete(self, toy_id: UUID) -> bool:
        """Remove um brinquedo (soft delete)."""
        toy = self._get_toy_or_raise(toy_id)
        result = self.repository.soft_delete(toy_id)
        if result:
            logger.info("Brinquedo removido: %s", toy_id)
        return result

    def toggle_status(self, toy_id: UUID) -> ToyStatusResponse:
        """Alterna o status ativo/inativo."""
        toy = self._get_toy_or_raise(toy_id)
        toy.is_active = not toy.is_active
        updated = self.repository.update(toy)

        status_text = "ativado" if updated.is_active else "desativado"
        return ToyStatusResponse(
            id=updated.id,
            is_active=updated.is_active,
            message=f"Brinquedo {status_text} com sucesso.",
        )

    def toggle_featured(self, toy_id: UUID) -> ToyFeaturedResponse:
        """Alterna o status de destaque."""
        toy = self._get_toy_or_raise(toy_id)
        toy.is_featured = not toy.is_featured
        updated = self.repository.update(toy)

        status_text = "marcado como destaque" if updated.is_featured else "removido dos destaques"
        return ToyFeaturedResponse(
            id=updated.id,
            is_featured=updated.is_featured,
            message=f"Brinquedo {status_text}.",
        )

    def update_position(self, toy_id: UUID, new_order: int) -> ToyPositionResponse:
        """Atualiza a ordem de exibição."""
        toy = self._get_toy_or_raise(toy_id)
        toy.display_order = new_order
        updated = self.repository.update(toy)

        return ToyPositionResponse(
            id=updated.id,
            display_order=updated.display_order,
            message=f"Ordem atualizada para {new_order}.",
        )
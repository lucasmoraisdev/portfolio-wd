from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.modules.toys.models import Toys
from app.modules.toys.schemas import ToyFilter


class ToyRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, toy: Toys) -> Toys:
        """Persiste um novo brinquedo."""
        self._db.add(toy)
        self._db.commit()
        self._db.refresh(toy)
        return toy

    def get_by_id(self, toy_id: UUID) -> Toys | None:
        """Busca um brinquedo pelo ID (incluindo deletados)."""
        stmt = (
            select(Toys)
            .options(joinedload(Toys.cover_image))
            .where(Toys.id == toy_id)
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_slug(self, slug: str) -> Toys | None:
        """Busca um brinquedo pelo slug."""
        stmt = (
            select(Toys)
            .options(joinedload(Toys.cover_image))
            .where(
                Toys.slug == slug,
            )
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_name(self, name: str) -> Toys | None:
        """Busca um brinquedo pelo nome (case-insensitive)."""
        stmt = select(Toys).where(
            func.lower(Toys.name) == func.lower(name),
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_slug_excluding(self, slug: str, exclude_id: UUID) -> Toys | None:
        """Busca por slug excluindo um ID específico."""
        stmt = select(Toys).where(
            Toys.slug == slug,
            Toys.id != exclude_id,
        )
        return self._db.execute(stmt).scalar_one_or_none()

    def list_all(
        self,
        filters: ToyFilter | None = None,
        only_active: bool = False,
        only_featured: bool = False,
    ) -> tuple[Sequence[Toys], int]:
        """
        Lista brinquedos com filtros e paginação.

        Returns:
            Tuple de (items, total_count)
        """
        filters = filters or ToyFilter()

        # Query base
        stmt = select(Toys)

        # Aplicar filtros
        if filters.search:
            search_term = f"%{filters.search}%"
            stmt = stmt.where(Toys.name.ilike(search_term))

        if filters.category:
            stmt = stmt.where(Toys.category == filters.category)

        if only_active or filters.is_active is not None:
            stmt = stmt.where(Toys.is_active == (filters.is_active if filters.is_active is not None else True))

        if only_featured or filters.is_featured is not None:
            stmt = stmt.where(Toys.is_featured == (filters.is_featured if filters.is_featured is not None else True))

        if filters.min_age is not None:
            stmt = stmt.where(Toys.min_age >= filters.min_age)

        if filters.max_age is not None:
            stmt = stmt.where(Toys.max_age <= filters.max_age)

        # Contar total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self._db.execute(count_stmt).scalar() or 0

        # Ordenação
        order_column = getattr(Toys, filters.order_by, Toys.display_order)
        if filters.order_direction == "desc":
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column.asc())

        # Paginação
        offset = (filters.page - 1) * filters.per_page
        stmt = stmt.offset(offset).limit(filters.per_page)

        items = self._db.execute(stmt).scalars().all()
        return items, total

    def list_featured(self, limit: int = 10) -> Sequence[Toys]:
        """Lista brinquedos em destaque."""
        stmt = (
            select(Toys)
            .where(
                Toys.is_featured,
                Toys.is_active,
            )
            .order_by(Toys.display_order.asc())
            .limit(limit)
        )
        return self._db.execute(stmt).scalars().all()

    def list_categories(self) -> list[str]:
        """Lista todas as categorias distintas."""
        stmt = (
            select(Toys.category)
            .distinct()
            .order_by(Toys.category)
        )
        return [row[0] for row in self._db.execute(stmt).all()]

    def update(self, toy: Toys) -> Toys:
        """Atualiza um brinquedo existente."""
        self._db.commit()
        self._db.refresh(toy)
        return toy
    
    def delete(self, toy_id: UUID) -> bool:
        """Deleta o registro."""
        toy = self.get_by_id(toy_id)
        
        if not toy:
            return False
        self._db.delete(toy)
        self._db.commit()
        return True

    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        """Verifica se um slug já existe."""
        stmt = select(Toys).where(
            Toys.slug == slug,
        )
        if exclude_id:
            stmt = stmt.where(Toys.id != exclude_id)
        return self._db.execute(stmt).scalar_one_or_none() is not None

    def resolve_image_urls(self, image_ids: list[UUID]) -> list[str]:
        """Busca urls públicas a partir de uma lista de IDs de upload."""
        if not image_ids:
            return []
        from app.modules.upload.models import Upload
        stmt = select(Upload.public_url).where(Upload.id.in_(image_ids))
        return list(self._db.execute(stmt).scalars().all())
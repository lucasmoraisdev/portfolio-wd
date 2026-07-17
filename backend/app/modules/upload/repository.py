from sqlalchemy import select
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

from app.modules.upload.models import Upload
from app.modules.upload.schemas import FileInfo

from uuid import UUID, uuid4

from sqlalchemy import delete

class UploadRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, file_info: FileInfo, public_url: str) -> Upload:
        upload = Upload(
            id=uuid4(),
            original_filename=file_info.original_filename,
            stored_filename=file_info.stored_filename,
            file_path=file_info.file_path,
            public_url=public_url,
            file_size=file_info.file_size,
            mime_type=file_info.mime_type,
            extension=file_info.extension
        )
        self._db.add(upload)
        self._db.commit()
        self._db.refresh(upload)
        return upload
    
    def get_by_id(self, upload_id: UUID) -> Upload | None:
        stmt = select(Upload).where(
            Upload.id == upload_id
        )

        return self._db.scalar(stmt)
    
    def list_all(self, limit: int = 100, offset: int = 0) -> list[Upload]:
        stmt = (
            select(Upload)
            .order_by(Upload.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._db.scalars(stmt).all()
    
    def delete(self, upload_id: UUID) -> bool:
        # Clean up references in Events
        try:
            from app.modules.events.models import Events
            events = self._db.scalars(select(Events)).all()
            for event in events:
                changed = False
                if event.cover_image_id == upload_id:
                    event.cover_image_id = None
                    changed = True
                if event.gallery_image_ids and upload_id in event.gallery_image_ids:
                    event.gallery_image_ids = [gid for gid in event.gallery_image_ids if gid != upload_id]
                    changed = True
                if changed:
                    self._db.add(event)
        except Exception as e:
            logger.error("Erro ao limpar referências de uploads nos eventos: %s", e)

        # Clean up references in Toys
        try:
            from app.modules.toys.models import Toys
            toys = self._db.scalars(select(Toys)).all()
            for toy in toys:
                changed = False
                if toy.cover_image_id == upload_id:
                    toy.cover_image_id = None
                    changed = True
                if toy.gallery_image_ids and upload_id in toy.gallery_image_ids:
                    toy.gallery_image_ids = [gid for gid in toy.gallery_image_ids if gid != upload_id]
                    changed = True
                if changed:
                    self._db.add(toy)
        except Exception as e:
            logger.error("Erro ao limpar referências de uploads nos brinquedos: %s", e)

        # Commit updates to event and toy records
        self._db.commit()

        # Now get and delete Upload record if it exists
        upload = self.get_by_id(upload_id)
        if not upload:
            return False

        stmt = delete(Upload).where(Upload.id == upload_id)
        self._db.execute(stmt)
        self._db.commit()
        return True
    
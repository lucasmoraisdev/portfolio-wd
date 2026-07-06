from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status

from sqlalchemy.orm import Session

from app.modules.upload.constants import UPLOAD_PREFIX, UPLOAD_TAG
from app.modules.upload.service import UploadService
from app.modules.upload.repository import UploadRepository
from app.modules.upload.schemas import UploadResponse

from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse, paginated_response

router = APIRouter(
    prefix=UPLOAD_PREFIX,
    tags=[UPLOAD_TAG]
)

def get_upload_service(
    db: Session = Depends(get_db),
) -> UploadService:
    repository = UploadRepository(db)
    return UploadService(repository=repository)

# ─── UPLOAD ARQUIVO ─────────────────────────────────────────────
@router.post(
    "",
    response_model=ApiResponse[UploadResponse],
    status_code=status.HTTP_201_CREATED
)
@api_response(message="Arquivo enviado com sucesso.", status_code=201)
async def upload_file(
    file: UploadFile = File(
        ...,
        description="Arquivo a ser enviado"
    ),
    file_type: str = "images",
    service: UploadService = Depends(get_upload_service)
) -> UploadResponse:
    """
    Faz upload de um arquivo.

    Validações:
        - Extensão
        - Tamanho máximo
        - Nome único gerado

    O arquivo é organizado em diretórios por tipo de data:
        uploads/images/2026/07/uuid.jpg
    """
    return await service.upload(file=file, file_type=file_type)

# ─── LISTAR UPLOADS ─────────────────────────────────────────────
@router.get(
    "",
    response_model=ApiResponse[dict],
)
@api_response(message="Uploads listados com sucesso.")
def list_uploads(
    limit: int = 20,
    offset: int = 0,
    service: UploadService = Depends(get_upload_service)
) -> dict:
    items = service.list_uploads(limit=limit, offset=offset)
    return paginated_response(
        items=items,
        total=len(items),
        page=(offset // limit) + 1,
        per_page=limit,
        message="Uploads listados com sucesso."
    )

# ─── OBTER UPLOAD POR ID ─────────────────────────────────────────────
@router.get(
    "/{upload_id}",
    response_model=ApiResponse[UploadResponse]
)
@api_response(message="Upload encontrado com sucesso.")
def get_upload(
    upload_id: UUID,
    service: UploadService = Depends(get_upload_service)
) -> UploadResponse:
    return service.get_by_id(upload_id)

# ─── DELETAR UPLOAD ─────────────────────────────────────────────
@router.delete(
    "/{upload_id}",
    response_model=ApiResponse[UploadResponse]
)
@api_response(message="ARquivo removido com sucesso.")
async def delete_upload(
    upload_id: UUID,
    service: UploadService = Depends(get_upload_service)
) -> UploadResponse:
    """
    Remove um upload do storage do registro no banco de dados.

    HARD DELETE
    """
    return await service.delete(upload_id)
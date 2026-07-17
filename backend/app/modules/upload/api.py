from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse

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

from typing import Union, List

# ─── UPLOAD ARQUIVO ─────────────────────────────────────────────
@router.post(
    "",
    response_model=ApiResponse[Union[UploadResponse, List[UploadResponse]]],
    status_code=status.HTTP_201_CREATED
)
@api_response(message="Arquivo enviado com sucesso.", status_code=201)
async def upload_file(
    files: List[UploadFile] = File(
        default=None,
        description="Arquivos a serem enviados (múltiplos)"
    ),
    file: UploadFile = File(
        default=None,
        description="Arquivo a ser enviado (único)"
    ),
    file_type: str = "images",
    service: UploadService = Depends(get_upload_service)
) -> Union[UploadResponse, List[UploadResponse]]:
    """
    Faz upload de um ou múltiplos arquivos.

    Validações:
        - Extensão
        - Tamanho máximo
        - Nome único gerado
    """
    from fastapi import HTTPException
    
    uploaded_files = []
    is_multiple = False
    
    if files:
        uploaded_files = files
        is_multiple = True
    elif file:
        uploaded_files = [file]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum arquivo enviado. Use o parâmetro 'file' para um único arquivo ou 'files' para múltiplos."
        )
        
    results = []
    for f in uploaded_files:
        res = await service.upload(file=f, file_type=file_type)
        results.append(res)
        
    return results if is_multiple else results[0]

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

# ─── STREAM DE ARQUIVO ─────────────────────────────────────────────
@router.get(
    "/{upload_id}/file",
    response_class=FileResponse,
)
def get_upload_file(
    upload_id: UUID,
    service: UploadService = Depends(get_upload_service)
) -> FileResponse:
    """
    Retorna o stream do arquivo pelo ID.
    """
    upload = service.get_by_id(upload_id)
    file_path = service.storage.get_full_path(upload.file_path)
    
    if not file_path.exists():
        from app.shared.exceptions import FileNotFoundException
        raise FileNotFoundException(str(upload_id))
        
    return FileResponse(path=file_path, media_type=upload.mime_type)

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
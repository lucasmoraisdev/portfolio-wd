"""
API Router do módulo de Settings.

Endpoints:
    GET    /settings/public     - Configurações públicas (site)
    GET    /settings            - Todas as configurações (admin)
    PUT    /settings            - Atualização em lote (admin)
    PATCH  /settings            - Atualização parcial (admin)
    POST   /settings/logo       - Upload de logo (admin)
    POST   /settings/favicon    - Upload de favicon (admin)
    POST   /settings/banner     - Upload de banner (admin)
    DELETE /settings/banner/{url} - Remover banner (admin)
"""

from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from .constants import SETTINGS_PREFIX, SETTINGS_TAG
from .service import SettingsService
from .repository import SettingsRepository
from .schemas import (
    SettingPublicResponse,
    SettingAdminResponse,
    SettingBulkUpdate,
    SettingResponse
)
from app.modules.upload.service import UploadService
from app.modules.upload.repository import UploadRepository
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=SETTINGS_PREFIX,
    tags=[SETTINGS_TAG]
)

def get_settings_service(
    db: Session = Depends(get_db)
) -> SettingsService:
    repository = SettingsRepository(db)
    upload_repo = UploadRepository(db)
    upload_service = UploadService(upload_repo)
    return SettingsService(repository=repository, upload_service=upload_service)


# PÚBLICO
@router.get(
    "/public",
    response_model=ApiResponse[SettingPublicResponse]
)
@api_response(message="Configurações públicas obtida com sucesso")
def get_public_settings(
    service: SettingsService = Depends(get_settings_service)
) -> SettingPublicResponse:
    return service.get_public_settings()

# ADMINISTRATIVO
@router.get(
    "",
    response_model=ApiResponse[SettingAdminResponse]
)
@api_response(message="Configurações obtidas com sucesso.")
def get_admin_settings(
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user)
) -> SettingAdminResponse:
    return service.get_admin_settings()

@router.put(
    "",
    response_model=ApiResponse[list[SettingResponse]]
)
@api_response(message="Configurações atualizadas com sucesso.")
def update_settings(
    payload: SettingBulkUpdate,
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user) # guard
) -> list[SettingResponse]:
    return service.update_settings(payload.settings)

@router.post(
    "/logo",
    response_model=ApiResponse[SettingResponse]
)
@api_response(message="Logo enviado com sucesso.")
async def upload_logo(
    file: UploadFile = File(...),
    logo_type: str = "main",
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user)
) -> SettingResponse:
    return await service.upload_logo(file, logo_type)

@router.post(
    "/favicon",
    response_model=ApiResponse[SettingResponse]
)
@api_response(message="Favicon enviado com sucesso.")
async def upload_favicon(
    file: UploadFile = File(...),
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user)
) -> SettingResponse:
    return await service.upload_favicon(file)

@router.post(
    "/banner",
    response_model=ApiResponse[SettingResponse]
)
@api_response(message="Banner enviado com sucesso.")
async def upload_banner(
    file: UploadFile = File(...),
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user)
) -> SettingResponse:
    return await service.upload_banner(file)

@router.delete(
    "/banner/{banner_url:path}",
    response_model=ApiResponse[dict]
)
@api_response(message="Banner removido com sucesso.")
def delete_banner(
    banner_url: str,
    service: SettingsService = Depends(get_settings_service),
    current_user: Any = Depends(get_current_user)
) -> dict:
    deleted = service.delete_banner(banner_url)
    return { "deleted": deleted, "url": banner_url }
 

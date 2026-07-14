from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.hero.constants import HERO_PREFIX, HERO_TAG
from app.modules.hero.schemas import HeroResponse, HeroUpdate
from app.modules.hero.service import HeroService
from app.modules.settings.repository import SettingsRepository
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix=HERO_PREFIX,
    tags=[HERO_TAG],
)

def get_hero_service(
    db: Session = Depends(get_db),
) -> HeroService:
    repository = SettingsRepository(db)
    return HeroService(repository)


# Públicos

@router.get(
    "/public",
    response_model=ApiResponse[HeroResponse],
)
@api_response(message="Dados do hero obtidos com sucesso.")
def get_public_hero(
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    return service.get_hero()


# Admin

@router.get(
    "",
    response_model=ApiResponse[HeroResponse],
)
@api_response(message="Configurações do hero obtidas com sucesso.")
def get_admin_hero(
    service: HeroService = Depends(get_hero_service),
    current_user=Depends(get_current_user),
) -> HeroResponse:
    return service.get_hero()

@router.put(
    "",
    response_model=ApiResponse[HeroResponse],
)
@api_response(message="Hero atualizado com sucesso.")
def update_hero(
    payload: HeroUpdate,
    service: HeroService = Depends(get_hero_service),
    current_user=Depends(get_current_user),
) -> HeroResponse:
    return service.update_hero(payload)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.dashboard.schemas import DashboardStatsResponse
from app.modules.dashboard.service import DashboardService
from app.shared.database import get_db
from app.shared.responses import api_response, ApiResponse
from app.shared.security.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

def get_dashboard_service(
    db: Session = Depends(get_db),
) -> DashboardService:
    return DashboardService(db)

@router.get(
    "",
    response_model=ApiResponse[DashboardStatsResponse],
)
@api_response(message="Estatísticas do dashboard obtidas com sucesso.")
def get_dashboard_stats(
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(get_current_user),
) -> DashboardStatsResponse:
    return service.get_stats()

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import DashboardStats
from app.services import service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardStats,
    summary="Statistiques dashboard",
    description="Expose les KPIs principaux: CA facture, encaissements, devis actifs et impayes.",
    response_description="KPIs dashboard",
)
def get_dashboard(uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.dashboard(uid)

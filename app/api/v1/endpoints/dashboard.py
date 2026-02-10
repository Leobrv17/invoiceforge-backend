from __future__ import annotations

from fastapi import APIRouter

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
def get_dashboard() -> dict:
    return service.dashboard()

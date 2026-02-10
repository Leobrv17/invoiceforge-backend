from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import CompanySettings, SettingsHistoryEntry
from app.services import service

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get(
    "/company",
    response_model=CompanySettings,
    summary="Lire les parametres entreprise",
    description="Retourne les parametres legaux et fiscaux de l'entreprise.",
)
def get_company_settings(uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.get_company(uid)


@router.put(
    "/company",
    response_model=CompanySettings,
    summary="Mettre a jour les parametres entreprise",
    description="Met a jour les parametres entreprise et historise les changements de regime TVA.",
)
def update_company_settings(payload: CompanySettings, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.update_company(uid, payload.model_dump())


@router.get(
    "/history",
    response_model=List[SettingsHistoryEntry],
    summary="Historique des parametres",
    description="Retourne l'historique des periodes de regime TVA.",
)
def get_settings_history(uid: str = Depends(require_authenticated_uid)) -> list[dict]:
    return service.list_settings_history(uid)

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Retourne l'etat de disponibilite de l'API.",
    response_description="Statut applicatif",
)
def health() -> dict[str, str]:
    return {"status": "ok"}

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import InvoiceRead, QuoteCreate, QuoteRead, QuoteStatusUpdate
from app.services import service

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.get(
    "",
    response_model=List[QuoteRead],
    summary="Lister les devis",
    description="Retourne tous les devis avec leur statut metier.",
)
def list_quotes(uid: str = Depends(require_authenticated_uid)) -> list[dict]:
    return service.list_quotes(uid)


@router.post(
    "",
    response_model=QuoteRead,
    status_code=201,
    summary="Creer un devis",
    description="Creer un devis en statut Brouillon.",
)
def create_quote(payload: QuoteCreate, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.create_quote(uid, payload.model_dump())


@router.patch(
    "/{quote_id}/status",
    response_model=QuoteRead,
    summary="Mettre a jour le statut d'un devis",
    description="Met a jour le statut d'un devis existant.",
)
def patch_quote_status(quote_id: str, payload: QuoteStatusUpdate, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.update_quote_status(uid, quote_id, payload.status)


@router.post(
    "/{quote_id}/convert-to-invoice",
    response_model=InvoiceRead,
    status_code=201,
    summary="Convertir un devis en facture",
    description="Convertit un devis Accepte en facture Brouillon.",
)
def convert_quote(quote_id: str, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.convert_quote_to_invoice(uid, quote_id)

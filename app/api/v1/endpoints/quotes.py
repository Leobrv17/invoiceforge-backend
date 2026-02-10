from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.models import InvoiceRead, QuoteCreate, QuoteRead, QuoteStatusUpdate
from app.services import service

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.get(
    "",
    response_model=List[QuoteRead],
    summary="Lister les devis",
    description="Retourne tous les devis avec leur statut metier.",
)
def list_quotes() -> list[dict]:
    return service.list_quotes()


@router.post(
    "",
    response_model=QuoteRead,
    status_code=201,
    summary="Creer un devis",
    description="Creer un devis en statut Brouillon.",
)
def create_quote(payload: QuoteCreate) -> dict:
    return service.create_quote(payload.model_dump())


@router.patch(
    "/{quote_id}/status",
    response_model=QuoteRead,
    summary="Mettre a jour le statut d'un devis",
    description="Met a jour le statut d'un devis existant.",
)
def patch_quote_status(quote_id: str, payload: QuoteStatusUpdate) -> dict:
    return service.update_quote_status(quote_id, payload.status)


@router.post(
    "/{quote_id}/convert-to-invoice",
    response_model=InvoiceRead,
    status_code=201,
    summary="Convertir un devis en facture",
    description="Convertit un devis Accepte en facture Brouillon.",
)
def convert_quote(quote_id: str) -> dict:
    return service.convert_quote_to_invoice(quote_id)

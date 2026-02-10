from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import InvoiceCreate, InvoiceRead, InvoiceStatusUpdate
from app.services import service

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get(
    "",
    response_model=List[InvoiceRead],
    summary="Lister les factures",
    description="Retourne toutes les factures avec leur cycle de vie.",
)
def list_invoices(uid: str = Depends(require_authenticated_uid)) -> list[dict]:
    return service.list_invoices(uid)


@router.post(
    "",
    response_model=InvoiceRead,
    status_code=201,
    summary="Creer une facture",
    description="Creer une facture en statut Brouillon.",
)
def create_invoice(payload: InvoiceCreate, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.create_invoice(uid, payload.model_dump())


@router.patch(
    "/{invoice_id}/status",
    response_model=InvoiceRead,
    summary="Mettre a jour le statut d'une facture",
    description="Applique les regles d'immutabilite metier sur les statuts factures.",
)
def patch_invoice_status(
    invoice_id: str,
    payload: InvoiceStatusUpdate,
    uid: str = Depends(require_authenticated_uid),
) -> dict:
    return service.update_invoice_status(uid, invoice_id, payload.status)

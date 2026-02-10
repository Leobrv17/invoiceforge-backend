from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.models import CreditNoteCreate, CreditNoteRead
from app.services import service

router = APIRouter(prefix="/credit-notes", tags=["Credit Notes"])


@router.get(
    "",
    response_model=List[CreditNoteRead],
    summary="Lister les avoirs",
    description="Retourne la liste des avoirs emis.",
)
def list_credit_notes() -> list[dict]:
    return service.list_credit_notes()


@router.post(
    "",
    response_model=CreditNoteRead,
    status_code=201,
    summary="Creer un avoir",
    description="Creer un avoir rattache a une facture existante.",
)
def create_credit_note(payload: CreditNoteCreate) -> dict:
    return service.create_credit_note(payload.model_dump())

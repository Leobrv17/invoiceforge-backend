from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import CreditNoteCreate, CreditNoteRead
from app.services import service

router = APIRouter(prefix="/credit-notes", tags=["Credit Notes"])


@router.get(
    "",
    response_model=List[CreditNoteRead],
    summary="Lister les avoirs",
    description="Retourne la liste des avoirs emis.",
)
def list_credit_notes(uid: str = Depends(require_authenticated_uid)) -> list[dict]:
    return service.list_credit_notes(uid)


@router.post(
    "",
    response_model=CreditNoteRead,
    status_code=201,
    summary="Creer un avoir",
    description="Creer un avoir rattache a une facture existante.",
)
def create_credit_note(payload: CreditNoteCreate, uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.create_credit_note(uid, payload.model_dump())

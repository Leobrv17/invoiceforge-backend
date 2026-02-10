from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import require_authenticated_uid
from app.models import AccountDeletionRequestRead
from app.services import service

router = APIRouter(prefix="/account", tags=["Account"])


@router.post(
    "/deletion-request",
    response_model=AccountDeletionRequestRead,
    summary="Demander la suppression du compte",
    description="Cree une demande RGPD de suppression/anonymisation soumise a revue legale.",
)
def create_deletion_request(uid: str = Depends(require_authenticated_uid)) -> dict:
    return service.request_account_deletion(uid)

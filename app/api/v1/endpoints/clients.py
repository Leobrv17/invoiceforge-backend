from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.models import ClientCreate, ClientRead
from app.services import service

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get(
    "",
    response_model=List[ClientRead],
    summary="Lister les clients",
    description="Retourne la liste des clients en base.",
)
def list_clients() -> list[dict]:
    return service.list_clients()


@router.post(
    "",
    response_model=ClientRead,
    status_code=201,
    summary="Creer un client",
    description="Ajoute un nouveau client avec validation stricte des champs.",
)
def create_client(payload: ClientCreate) -> dict:
    return service.create_client(payload.model_dump())

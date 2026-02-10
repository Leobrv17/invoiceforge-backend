from __future__ import annotations

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.services import service

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get(
    "/ledger.json",
    summary="Exporter le ledger en JSON",
    description="Exporte le grand livre agrege (devis/factures/avoirs) au format JSON.",
)
def export_ledger_json() -> JSONResponse:
    return JSONResponse(content=service.export_ledger_json())


@router.get(
    "/ledger.csv",
    summary="Exporter le ledger en CSV",
    description="Exporte le grand livre agrege (devis/factures/avoirs) au format CSV.",
)
def export_ledger_csv() -> Response:
    csv_content = service.export_ledger_csv()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ledger.csv"},
    )


@router.get(
    "/invoices.zip",
    summary="Exporter les factures en ZIP",
    description="Genere et telecharge une archive ZIP des factures Emise/Payee en PDF.",
)
def export_invoices_zip() -> Response:
    payload = service.export_issued_invoices_zip()
    return Response(
        content=payload,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=invoices.zip"},
    )

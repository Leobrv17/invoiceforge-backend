from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import HTTPException

from app.models import InvoiceStatus, QuoteStatus
from app.services.base import BaseService
from app.storage.db import db


class InvoicesService(BaseService):
    def list_invoices(self, uid: str) -> list[dict[str, Any]]:
        return db.read(uid)["invoices"]

    def create_invoice(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            state["counters"]["invoice"] += 1
            invoice_prefix = state["company"]["invoice_prefix"]
            invoice_id = self.build_id(invoice_prefix, self.year(), state["counters"]["invoice"], 4)
            record = {
                "id": invoice_id,
                **payload,
                "status": InvoiceStatus.DRAFT.value,
                "created_at": self.iso_now(),
                "validated_at": None,
            }
            record["issued_at"] = str(record["issued_at"])
            state["invoices"].insert(0, record)
            return record

        return db.mutate(uid, _mutate)

    def update_invoice_status(self, uid: str, invoice_id: str, status: InvoiceStatus) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            invoice = next((item for item in state["invoices"] if item["id"] == invoice_id), None)
            if not invoice:
                raise HTTPException(status_code=404, detail="Invoice not found")

            current = invoice["status"]
            if current == InvoiceStatus.ISSUED.value and status == InvoiceStatus.DRAFT:
                raise HTTPException(status_code=400, detail="Issued invoice cannot return to draft")
            if current == InvoiceStatus.PAID.value and status != InvoiceStatus.PAID:
                raise HTTPException(status_code=400, detail="Paid invoice is immutable")

            invoice["status"] = status.value
            if status in (InvoiceStatus.ISSUED, InvoiceStatus.PAID):
                invoice["validated_at"] = invoice.get("validated_at") or self.iso_now()
                invoice["snapshot"] = {
                    "client": {
                        "name": invoice["client_name"],
                    },
                    "company": {
                        "company_name": state["company"]["company_name"],
                        "siret": state["company"]["siret"],
                        "address": state["company"]["address"],
                        "vat_regime": state["company"]["vat_regime"],
                        "legal_notice": state["company"]["legal_notice"],
                    },
                }
            return invoice

        return db.mutate(uid, _mutate)

    def create_invoice_from_quote(self, uid: str, quote_id: str) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            quote = next((item for item in state["quotes"] if item["id"] == quote_id), None)
            if not quote:
                raise HTTPException(status_code=404, detail="Quote not found")
            if quote["status"] != QuoteStatus.ACCEPTED.value:
                raise HTTPException(status_code=400, detail="Only accepted quotes can be converted")

            state["counters"]["invoice"] += 1
            invoice_prefix = state["company"]["invoice_prefix"]
            invoice_id = self.build_id(invoice_prefix, self.year(), state["counters"]["invoice"], 4)
            invoice = {
                "id": invoice_id,
                "client_name": quote["client_name"],
                "amount": quote["amount"],
                "issued_at": str(date.today()),
                "status": InvoiceStatus.DRAFT.value,
                "tax_rate": 0.0,
                "tax_amount": 0.0,
                "created_at": self.iso_now(),
                "validated_at": None,
                "source_quote_id": quote_id,
            }
            state["invoices"].insert(0, invoice)
            return invoice

        return db.mutate(uid, _mutate)

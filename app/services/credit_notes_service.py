from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import HTTPException

from app.services.base import BaseService
from app.storage.db import db


class CreditNotesService(BaseService):
    def list_credit_notes(self) -> list[dict[str, Any]]:
        return db.read()["credit_notes"]

    def create_credit_note(self, payload: dict[str, Any]) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            invoice = next((item for item in state["invoices"] if item["id"] == payload["invoice_id"]), None)
            if not invoice:
                raise HTTPException(status_code=404, detail="Original invoice not found")

            state["counters"]["credit_note"] += 1
            credit_id = self.build_id("AV", self.year(), state["counters"]["credit_note"], 4)
            record = {
                "id": credit_id,
                "invoice_id": payload["invoice_id"],
                "amount": payload["amount"],
                "issued_at": str(date.today()),
                "created_at": self.iso_now(),
            }
            state["credit_notes"].insert(0, record)
            return record

        return db.mutate(_mutate)

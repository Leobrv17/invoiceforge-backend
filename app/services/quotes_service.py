from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from app.models import QuoteStatus
from app.services.base import BaseService
from app.storage.db import db


class QuotesService(BaseService):
    def list_quotes(self) -> list[dict[str, Any]]:
        return db.read()["quotes"]

    def create_quote(self, payload: dict[str, Any]) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            state["counters"]["quote"] += 1
            quote_id = self.build_id("DV", self.year(), state["counters"]["quote"], 3)
            record = {
                "id": quote_id,
                **payload,
                "status": QuoteStatus.DRAFT.value,
                "created_at": self.iso_now(),
            }
            record["valid_until"] = str(record["valid_until"])
            state["quotes"].insert(0, record)
            return record

        return db.mutate(_mutate)

    def update_quote_status(self, quote_id: str, status: QuoteStatus) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            for quote in state["quotes"]:
                if quote["id"] == quote_id:
                    quote["status"] = status.value
                    return quote
            raise HTTPException(status_code=404, detail="Quote not found")

        return db.mutate(_mutate)

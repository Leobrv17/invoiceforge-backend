from __future__ import annotations

from typing import Any

from app.services.base import BaseService
from app.storage.db import db


class ClientsService(BaseService):
    def list_clients(self) -> list[dict[str, Any]]:
        return db.read()["clients"]

    def create_client(self, payload: dict[str, Any]) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            state["counters"]["client"] += 1
            record = {
                "id": f"CL-{state['counters']['client']}",
                **payload,
                "created_at": self.iso_now(),
            }
            state["clients"].insert(0, record)
            return record

        return db.mutate(_mutate)

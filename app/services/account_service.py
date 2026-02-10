from __future__ import annotations

from typing import Any

from app.services.base import BaseService
from app.storage.db import db


class AccountService(BaseService):
    def request_account_deletion(self) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            request = {
                "requested_at": self.iso_now(),
                "status": "pending_legal_review",
                "message": "Anonymisation possible, conservation des obligations fiscales requise.",
            }
            state["deletion_requests"].append(request)
            return request

        return db.mutate(_mutate)

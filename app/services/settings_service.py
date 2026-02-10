from __future__ import annotations

from datetime import date
from typing import Any

from app.storage.db import db


class SettingsService:
    def get_company(self, uid: str) -> dict[str, Any]:
        return db.read(uid)["company"]

    def update_company(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        def _mutate(state: dict[str, Any]) -> dict[str, Any]:
            previous_vat = state["company"]["vat_regime"]
            state["company"].update(payload)
            if previous_vat != payload["vat_regime"]:
                today = str(date.today())
                for entry in state["settings_history"]:
                    if entry["end_date"] is None:
                        entry["end_date"] = today
                state["counters"]["settings"] += 1
                state["settings_history"].append(
                    {
                        "id": f"SET-{state['counters']['settings']:04d}",
                        "vat_regime": payload["vat_regime"],
                        "start_date": today,
                        "end_date": None,
                    }
                )
            return state["company"]

        return db.mutate(uid, _mutate)

    def list_settings_history(self, uid: str) -> list[dict[str, Any]]:
        return db.read(uid)["settings_history"]

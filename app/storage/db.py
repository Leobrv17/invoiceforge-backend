from __future__ import annotations

import json
from datetime import date, datetime
from threading import Lock
from typing import Any

from app.core.config import DATA_DIR, DATA_FILE


class JsonDB:
    def __init__(self) -> None:
        self._lock = Lock()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            self._write(self._seed())

    def _seed(self) -> dict[str, Any]:
        now = datetime.utcnow().isoformat()
        return {
            "company": {
                "company_name": "Agence Nova",
                "siret": "901 234 567 00016",
                "address": "12 rue de la Forge, 75011 Paris",
                "vat_regime": "Franchise en base",
                "legal_notice": "TVA non applicable, article 293 B du CGI.",
                "invoice_prefix": "IF",
            },
            "settings_history": [
                {
                    "id": "SET-0001",
                    "vat_regime": "Franchise en base",
                    "start_date": date.today().isoformat(),
                    "end_date": None,
                }
            ],
            "counters": {
                "client": 1025,
                "quote": 2,
                "invoice": 22,
                "credit_note": 3,
                "settings": 1,
            },
            "clients": [
                {
                    "id": "CL-1024",
                    "name": "Studio Omena",
                    "type": "Pro",
                    "email": "contact@omena.fr",
                    "created_at": now,
                },
                {
                    "id": "CL-1025",
                    "name": "Atelier Celine",
                    "type": "Particulier",
                    "email": "celine@email.fr",
                    "created_at": now,
                },
            ],
            "quotes": [
                {
                    "id": "DV-2024-001",
                    "client_name": "Studio Omena",
                    "amount": 1840,
                    "status": "Accepte",
                    "valid_until": "2024-06-30",
                    "created_at": now,
                },
                {
                    "id": "DV-2024-002",
                    "client_name": "Atelier Celine",
                    "amount": 960,
                    "status": "Envoye",
                    "valid_until": "2024-07-12",
                    "created_at": now,
                },
            ],
            "invoices": [
                {
                    "id": "IF-2024-0021",
                    "client_name": "Studio Omena",
                    "amount": 1240,
                    "status": "Emise",
                    "issued_at": "2024-06-02",
                    "tax_rate": 0.0,
                    "tax_amount": 0.0,
                    "created_at": now,
                    "validated_at": now,
                    "source_quote_id": None,
                    "snapshot": {
                        "client": {"name": "Studio Omena"},
                        "company": {
                            "company_name": "Agence Nova",
                            "vat_regime": "Franchise en base",
                        },
                    },
                },
                {
                    "id": "IF-2024-0022",
                    "client_name": "Atelier Celine",
                    "amount": 780,
                    "status": "Payee",
                    "issued_at": "2024-06-05",
                    "tax_rate": 0.0,
                    "tax_amount": 0.0,
                    "created_at": now,
                    "validated_at": now,
                    "source_quote_id": None,
                    "snapshot": {
                        "client": {"name": "Atelier Celine"},
                        "company": {
                            "company_name": "Agence Nova",
                            "vat_regime": "Franchise en base",
                        },
                    },
                },
            ],
            "credit_notes": [
                {
                    "id": "AV-2024-0003",
                    "invoice_id": "IF-2024-0018",
                    "amount": 320,
                    "issued_at": "2024-05-21",
                    "created_at": now,
                }
            ],
            "deletion_requests": [],
        }

    def _read(self) -> dict[str, Any]:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, payload: dict[str, Any]) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    def read(self) -> dict[str, Any]:
        with self._lock:
            return self._read()

    def mutate(self, mutator):
        with self._lock:
            state = self._read()
            result = mutator(state)
            self._write(state)
            return result


db = JsonDB()

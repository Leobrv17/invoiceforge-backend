from __future__ import annotations

import json
from datetime import date, datetime
from threading import Lock
from typing import Any, Callable, TypeVar

from app.core.config import DATA_DIR, DATA_FILE, FIRESTORE_COLLECTION, STORAGE_BACKEND
from app.core.firebase import firestore_client, firestore_module

T = TypeVar("T")


class BaseDB:
    @staticmethod
    def seed() -> dict[str, Any]:
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


class JsonDB(BaseDB):
    def __init__(self) -> None:
        self._lock = Lock()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            self._write_root({"users": {}})

    def _read_raw(self) -> dict[str, Any]:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_root(self, payload: dict[str, Any]) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    def _ensure_root(self, root: dict[str, Any]) -> dict[str, Any]:
        if "users" in root and isinstance(root["users"], dict):
            return root

        # Migration legacy format: old flat root becomes default user bucket.
        return {"users": {"legacy-local": root}}

    @staticmethod
    def _ensure_user_state(root: dict[str, Any], uid: str) -> None:
        if uid not in root["users"]:
            root["users"][uid] = BaseDB.seed()

    def read(self, uid: str) -> dict[str, Any]:
        with self._lock:
            root = self._ensure_root(self._read_raw())
            self._ensure_user_state(root, uid)
            self._write_root(root)
            return root["users"][uid]

    def mutate(self, uid: str, mutator: Callable[[dict[str, Any]], T]) -> T:
        with self._lock:
            root = self._ensure_root(self._read_raw())
            self._ensure_user_state(root, uid)
            user_state = root["users"][uid]
            result = mutator(user_state)
            root["users"][uid] = user_state
            self._write_root(root)
            return result


class FirestoreDB(BaseDB):
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name

    def _doc_ref(self, uid: str):
        client = firestore_client()
        return client.collection(self.collection_name).document(uid)

    def read(self, uid: str) -> dict[str, Any]:
        doc_ref = self._doc_ref(uid)
        snapshot = doc_ref.get()
        if snapshot.exists:
            payload = snapshot.to_dict() or {}
            if payload:
                return payload

        payload = BaseDB.seed()
        doc_ref.set(payload)
        return payload

    def mutate(self, uid: str, mutator: Callable[[dict[str, Any]], T]) -> T:
        client = firestore_client()
        doc_ref = client.collection(self.collection_name).document(uid)
        firestore = firestore_module()

        @firestore.transactional
        def _mutate_transaction(transaction, reference):
            snapshot = reference.get(transaction=transaction)
            state = snapshot.to_dict() if snapshot.exists else BaseDB.seed()
            result = mutator(state)
            transaction.set(reference, state)
            return result

        transaction = client.transaction()
        return _mutate_transaction(transaction, doc_ref)


def _build_db() -> JsonDB | FirestoreDB:
    if STORAGE_BACKEND == "firestore":
        return FirestoreDB(collection_name=FIRESTORE_COLLECTION)

    return JsonDB()


db = _build_db()

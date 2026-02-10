from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class LedgerEntry(BaseModel):
    document_id: str
    document_type: str
    client_name: str
    amount: float
    status: str
    date: date

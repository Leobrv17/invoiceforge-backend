from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class CreditNoteCreate(BaseModel):
    invoice_id: str = Field(min_length=1)
    amount: float = Field(gt=0)


class CreditNoteRead(BaseModel):
    id: str
    invoice_id: str
    amount: float
    issued_at: date
    created_at: datetime

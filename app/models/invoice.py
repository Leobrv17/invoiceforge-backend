from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import InvoiceStatus


class InvoiceBase(BaseModel):
    client_name: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    issued_at: date
    tax_rate: float = 0.0
    tax_amount: float = 0.0


class InvoiceCreate(InvoiceBase):
    source_quote_id: Optional[str] = None


class InvoiceRead(InvoiceBase):
    id: str
    status: InvoiceStatus
    created_at: datetime
    validated_at: Optional[datetime] = None
    source_quote_id: Optional[str] = None


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus

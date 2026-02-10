from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.enums import QuoteStatus


class QuoteBase(BaseModel):
    client_name: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    valid_until: date


class QuoteCreate(QuoteBase):
    pass


class QuoteRead(QuoteBase):
    id: str
    status: QuoteStatus
    created_at: datetime


class QuoteStatusUpdate(BaseModel):
    status: QuoteStatus

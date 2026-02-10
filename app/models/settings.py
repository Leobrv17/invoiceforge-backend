from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel


class CompanySettings(BaseModel):
    company_name: str
    siret: str
    address: str
    vat_regime: str
    legal_notice: str
    invoice_prefix: str


class SettingsHistoryEntry(BaseModel):
    id: str
    vat_regime: str
    start_date: date
    end_date: Optional[date] = None

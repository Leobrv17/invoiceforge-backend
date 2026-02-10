from __future__ import annotations

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_invoiced: float
    total_collected: float
    active_quotes: int
    overdue_invoices: int

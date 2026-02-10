from __future__ import annotations

from typing import Any

from app.models import InvoiceStatus, QuoteStatus
from app.storage.db import db


class DashboardService:
    def dashboard(self, uid: str) -> dict[str, Any]:
        state = db.read(uid)
        invoices = state["invoices"]
        total_invoiced = round(sum(item["amount"] for item in invoices), 2)
        total_collected = round(
            sum(item["amount"] for item in invoices if item["status"] == InvoiceStatus.PAID.value), 2
        )
        active_quotes = len([item for item in state["quotes"] if item["status"] != QuoteStatus.REFUSED.value])
        overdue_invoices = len([item for item in invoices if item["status"] == InvoiceStatus.OVERDUE.value])
        return {
            "total_invoiced": total_invoiced,
            "total_collected": total_collected,
            "active_quotes": active_quotes,
            "overdue_invoices": overdue_invoices,
        }

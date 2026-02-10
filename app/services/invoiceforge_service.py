from __future__ import annotations

from typing import Any

from app.models import InvoiceStatus, QuoteStatus
from app.services.account_service import AccountService
from app.services.clients_service import ClientsService
from app.services.credit_notes_service import CreditNotesService
from app.services.dashboard_service import DashboardService
from app.services.exports_service import ExportsService
from app.services.invoices_service import InvoicesService
from app.services.quotes_service import QuotesService
from app.services.settings_service import SettingsService


class InvoiceForgeService:
    def __init__(self) -> None:
        self.clients = ClientsService()
        self.quotes = QuotesService()
        self.invoices = InvoicesService()
        self.credit_notes = CreditNotesService()
        self.dashboard_service = DashboardService()
        self.settings = SettingsService()
        self.exports = ExportsService()
        self.account = AccountService()

    def dashboard(self, uid: str) -> dict[str, Any]:
        return self.dashboard_service.dashboard(uid)

    def list_clients(self, uid: str) -> list[dict[str, Any]]:
        return self.clients.list_clients(uid)

    def create_client(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.clients.create_client(uid, payload)

    def list_quotes(self, uid: str) -> list[dict[str, Any]]:
        return self.quotes.list_quotes(uid)

    def create_quote(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.quotes.create_quote(uid, payload)

    def update_quote_status(self, uid: str, quote_id: str, status: QuoteStatus) -> dict[str, Any]:
        return self.quotes.update_quote_status(uid, quote_id, status)

    def convert_quote_to_invoice(self, uid: str, quote_id: str) -> dict[str, Any]:
        return self.invoices.create_invoice_from_quote(uid, quote_id)

    def list_invoices(self, uid: str) -> list[dict[str, Any]]:
        return self.invoices.list_invoices(uid)

    def create_invoice(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.invoices.create_invoice(uid, payload)

    def update_invoice_status(self, uid: str, invoice_id: str, status: InvoiceStatus) -> dict[str, Any]:
        return self.invoices.update_invoice_status(uid, invoice_id, status)

    def list_credit_notes(self, uid: str) -> list[dict[str, Any]]:
        return self.credit_notes.list_credit_notes(uid)

    def create_credit_note(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.credit_notes.create_credit_note(uid, payload)

    def get_company(self, uid: str) -> dict[str, Any]:
        return self.settings.get_company(uid)

    def update_company(self, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.settings.update_company(uid, payload)

    def list_settings_history(self, uid: str) -> list[dict[str, Any]]:
        return self.settings.list_settings_history(uid)

    def export_ledger_json(self, uid: str) -> list[dict[str, Any]]:
        return self.exports.export_ledger_json(uid)

    def export_ledger_csv(self, uid: str) -> str:
        return self.exports.export_ledger_csv(uid)

    def export_issued_invoices_zip(self, uid: str) -> bytes:
        return self.exports.export_issued_invoices_zip(uid)

    def request_account_deletion(self, uid: str) -> dict[str, Any]:
        return self.account.request_account_deletion(uid)


service = InvoiceForgeService()

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

    def dashboard(self) -> dict[str, Any]:
        return self.dashboard_service.dashboard()

    def list_clients(self) -> list[dict[str, Any]]:
        return self.clients.list_clients()

    def create_client(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.clients.create_client(payload)

    def list_quotes(self) -> list[dict[str, Any]]:
        return self.quotes.list_quotes()

    def create_quote(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.quotes.create_quote(payload)

    def update_quote_status(self, quote_id: str, status: QuoteStatus) -> dict[str, Any]:
        return self.quotes.update_quote_status(quote_id, status)

    def convert_quote_to_invoice(self, quote_id: str) -> dict[str, Any]:
        return self.invoices.create_invoice_from_quote(quote_id)

    def list_invoices(self) -> list[dict[str, Any]]:
        return self.invoices.list_invoices()

    def create_invoice(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.invoices.create_invoice(payload)

    def update_invoice_status(self, invoice_id: str, status: InvoiceStatus) -> dict[str, Any]:
        return self.invoices.update_invoice_status(invoice_id, status)

    def list_credit_notes(self) -> list[dict[str, Any]]:
        return self.credit_notes.list_credit_notes()

    def create_credit_note(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.credit_notes.create_credit_note(payload)

    def get_company(self) -> dict[str, Any]:
        return self.settings.get_company()

    def update_company(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.settings.update_company(payload)

    def list_settings_history(self) -> list[dict[str, Any]]:
        return self.settings.list_settings_history()

    def export_ledger_json(self) -> list[dict[str, Any]]:
        return self.exports.export_ledger_json()

    def export_ledger_csv(self) -> str:
        return self.exports.export_ledger_csv()

    def export_issued_invoices_zip(self) -> bytes:
        return self.exports.export_issued_invoices_zip()

    def request_account_deletion(self) -> dict[str, Any]:
        return self.account.request_account_deletion()


service = InvoiceForgeService()

from __future__ import annotations

import csv
from io import BytesIO, StringIO
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.core.config import PDF_DIR
from app.models import InvoiceStatus
from app.storage.db import db


class ExportsService:
    def ledger_entries(self) -> list[dict[str, Any]]:
        state = db.read()
        entries: list[dict[str, Any]] = []
        for quote in state["quotes"]:
            entries.append(
                {
                    "document_id": quote["id"],
                    "document_type": "quote",
                    "client_name": quote["client_name"],
                    "amount": quote["amount"],
                    "status": quote["status"],
                    "date": quote["valid_until"],
                }
            )
        for invoice in state["invoices"]:
            entries.append(
                {
                    "document_id": invoice["id"],
                    "document_type": "invoice",
                    "client_name": invoice["client_name"],
                    "amount": invoice["amount"],
                    "status": invoice["status"],
                    "date": invoice["issued_at"],
                }
            )
        for credit in state["credit_notes"]:
            entries.append(
                {
                    "document_id": credit["id"],
                    "document_type": "credit_note",
                    "client_name": "N/A",
                    "amount": -abs(credit["amount"]),
                    "status": "Emis",
                    "date": credit["issued_at"],
                }
            )
        return entries

    def export_ledger_json(self) -> list[dict[str, Any]]:
        return self.ledger_entries()

    def export_ledger_csv(self) -> str:
        buffer = StringIO()
        fields = ["document_id", "document_type", "client_name", "amount", "status", "date"]
        writer = csv.DictWriter(buffer, fieldnames=fields)
        writer.writeheader()
        for row in self.ledger_entries():
            writer.writerow(row)
        return buffer.getvalue()

    def render_invoice_pdf(self, invoice: dict[str, Any]) -> bytes:
        PDF_DIR.mkdir(parents=True, exist_ok=True)
        io = BytesIO()
        pdf = canvas.Canvas(io, pagesize=A4)
        pdf.setTitle(invoice["id"])
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(50, 800, f"Facture {invoice['id']}")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, 770, f"Client: {invoice['client_name']}")
        pdf.drawString(50, 750, f"Date emission: {invoice['issued_at']}")
        pdf.drawString(50, 730, f"Montant: {invoice['amount']} EUR")
        pdf.drawString(50, 710, f"Statut: {invoice['status']}")
        pdf.drawString(50, 690, "Factur-X metadata: prepared (V1 ready)")
        pdf.showPage()
        pdf.save()
        return io.getvalue()

    def export_issued_invoices_zip(self) -> bytes:
        state = db.read()
        issued = [
            invoice
            for invoice in state["invoices"]
            if invoice["status"] in (InvoiceStatus.ISSUED.value, InvoiceStatus.PAID.value)
        ]

        output = BytesIO()
        with ZipFile(output, "w", ZIP_DEFLATED) as zip_file:
            for invoice in issued:
                zip_file.writestr(f"{invoice['id']}.pdf", self.render_invoice_pdf(invoice))
        return output.getvalue()

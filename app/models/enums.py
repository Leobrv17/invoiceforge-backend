from __future__ import annotations

from enum import Enum


class ClientType(str, Enum):
    PRO = "Pro"
    INDIVIDUAL = "Particulier"


class QuoteStatus(str, Enum):
    DRAFT = "Brouillon"
    SENT = "Envoye"
    ACCEPTED = "Accepte"
    REFUSED = "Refuse"


class InvoiceStatus(str, Enum):
    DRAFT = "Brouillon"
    ISSUED = "Emise"
    PAID = "Payee"
    OVERDUE = "En retard"

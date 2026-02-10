from pathlib import Path

APP_NAME = "InvoiceForge Backend"
APP_VERSION = "1.1.0"
API_PREFIX = "/api/v1"
APP_DESCRIPTION = (
    "API backend InvoiceForge. "
    "Gestion des clients, devis, factures, avoirs, parametres entreprise et exports comptables."
)
API_CONTACT = {"name": "InvoiceForge Team", "email": "support@invoiceforge.app"}
API_TAGS = [
    {"name": "Health", "description": "Sante et disponibilite de l'API."},
    {"name": "Dashboard", "description": "KPIs business pour le tableau de bord."},
    {"name": "Clients", "description": "Gestion des fiches clients."},
    {"name": "Quotes", "description": "Cycle de vie des devis."},
    {"name": "Invoices", "description": "Cycle de vie des factures."},
    {"name": "Credit Notes", "description": "Gestion des avoirs."},
    {"name": "Settings", "description": "Configuration entreprise et historique TVA."},
    {"name": "Exports", "description": "Exports JSON, CSV et ZIP."},
    {"name": "Account", "description": "Actions compte et conformite RGPD."},
]

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILE = DATA_DIR / "db.json"
PDF_DIR = DATA_DIR / "pdf"

# InvoiceForge Backend (FastAPI)

Backend V1 pour InvoiceForge, structure de code orientee domaines metier et extensibilite.

## Stack

- Python 3.12
- FastAPI + Pydantic
- Persistance locale JSON (dev)
- Docker + docker-compose

## Architecture (pro / evolutive)

Le code est decoupe par responsabilite:

- `app/api/v1/endpoints/`: un fichier par ressource API (`clients`, `quotes`, `invoices`, etc.)
- `app/services/`: logique metier decoupee par objet domaine
- `app/models/`: schemas Pydantic separes par objet
- `app/storage/`: acces/persistance des donnees
- `app/core/`: configuration centrale (OpenAPI, chemins, constantes)

Points clefs:

- Façade `InvoiceForgeService` conservant un point d'entree stable
- Routeur principal `app/api/v1/router.py` qui compose tous les endpoints
- OpenAPI propre (tags, descriptions, summaries par endpoint)

## Fonctionnalites V1

- Clients: creation + listing
- Devis: creation, listing, changement de statut
- Conversion devis accepte -> facture brouillon
- Factures: creation, listing, changement de statut
- Immutabilite metier apres emission/paiement
- Avoirs relies a la facture d'origine
- Dashboard: CA facture, CA encaisse, devis actifs, impayes
- Parametres entreprise + historique de regime TVA
- Export ledger JSON/CSV
- Export ZIP de factures emises (PDF genere)
- Demande de suppression de compte (workflow RGPD)

## Lancer en local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: `http://localhost:8000`
Docs Swagger: `http://localhost:8000/docs`
OpenAPI JSON: `http://localhost:8000/openapi.json`

## Lancer avec Docker

```bash
docker compose up --build
```

## Endpoints principaux

- `GET /api/v1/health`
- `GET /api/v1/dashboard`
- `GET/POST /api/v1/clients`
- `GET/POST /api/v1/quotes`
- `PATCH /api/v1/quotes/{quote_id}/status`
- `POST /api/v1/quotes/{quote_id}/convert-to-invoice`
- `GET/POST /api/v1/invoices`
- `PATCH /api/v1/invoices/{invoice_id}/status`
- `GET/POST /api/v1/credit-notes`
- `GET/PUT /api/v1/settings/company`
- `GET /api/v1/settings/history`
- `GET /api/v1/exports/ledger.json`
- `GET /api/v1/exports/ledger.csv`
- `GET /api/v1/exports/invoices.zip`
- `POST /api/v1/account/deletion-request`

## Notes

- Les statuts restent normalises ASCII (`Emise`, `Payee`, `Accepte`) pour eviter les soucis d'encodage inter-systemes.
- Le stockage JSON est adapte au dev; la couche service est prete a evoluer vers une base SQL/NoSQL.

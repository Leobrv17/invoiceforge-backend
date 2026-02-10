# InvoiceForge Backend (FastAPI)

Backend V1 pour InvoiceForge, structure de code orientee domaines metier et extensibilite.

## Stack

- Python 3.9+
- FastAPI + Pydantic
- Firebase Authentication (verif des ID tokens)
- Firestore (stockage principal)
- Docker + docker-compose

## Architecture (pro / evolutive)

Le code est decoupe par responsabilite:

- `app/api/v1/endpoints/`: un fichier par ressource API (`clients`, `quotes`, `invoices`, etc.)
- `app/api/dependencies/`: dependances transverses (auth Firebase)
- `app/services/`: logique metier decoupee par objet domaine
- `app/models/`: schemas Pydantic separes par objet
- `app/storage/`: acces/persistance des donnees (Firestore ou JSON)
- `app/core/`: configuration centrale (OpenAPI, Firebase, constantes)

## Securite API (obligatoire)

Toutes les routes metier sous `/api/v1/*` (sauf `/health`) exigent un token Firebase ID:

- Header: `Authorization: Bearer <FIREBASE_ID_TOKEN>`
- Si token absent/invalide: `401`
- Si Firebase non configure: `503`

Les donnees sont isolees par utilisateur (`uid` Firebase): chaque `uid` a son propre document Firestore.

## Setup Firebase pas a pas

### 1) Creer le projet Firebase

1. Va sur [Firebase Console](https://console.firebase.google.com/)
2. Cree un projet (ou utilise un existant)
3. Active Authentication (au moins Email/Password, ou ton provider choisi)
4. Active Firestore Database en mode production ou test selon ton besoin

### 2) Creer la cle serveur (service account)

1. Firebase Console > Project settings > Service accounts
2. Clique `Generate new private key`
3. Recupere le fichier JSON

### 3) Ou mettre le fichier JSON

Dans le backend, cree ce dossier/fichier:

- `invoiceforge-backend/firebase/service-account.json`

Important:

- Ne jamais commiter ce fichier
- `.gitignore` ignore `firebase/*.json`

### 4) Variables d'environnement

Copie le template:

```bash
cp .env.example .env
```

Puis configure:

- `STORAGE_BACKEND=firestore`
- `FIREBASE_PROJECT_ID=<ton_project_id>`
- `FIREBASE_SERVICE_ACCOUNT_FILE=firebase/service-account.json`
- `FIRESTORE_COLLECTION=invoiceforge_users`

Si tu n'utilises pas de loader `.env`, exporte les variables dans ton shell:

```bash
export STORAGE_BACKEND=firestore
export FIREBASE_PROJECT_ID=your-project-id
export FIREBASE_SERVICE_ACCOUNT_FILE=firebase/service-account.json
export FIRESTORE_COLLECTION=invoiceforge_users
```

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

## Tester un endpoint protege

```bash
curl -H "Authorization: Bearer <ID_TOKEN>" http://localhost:8000/api/v1/clients
```

## Mode fallback local (sans Firestore)

Possible pour dev rapide:

- `STORAGE_BACKEND=json`

Le backend reste protege par Firebase Auth (token requis), mais stocke localement dans `data/db.json` avec isolation par `uid`.

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

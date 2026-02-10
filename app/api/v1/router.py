from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import account, clients, credit_notes, dashboard, exports, health, invoices, quotes, settings

router = APIRouter()
router.include_router(health.router)
router.include_router(dashboard.router)
router.include_router(clients.router)
router.include_router(quotes.router)
router.include_router(invoices.router)
router.include_router(credit_notes.router)
router.include_router(settings.router)
router.include_router(exports.router)
router.include_router(account.router)

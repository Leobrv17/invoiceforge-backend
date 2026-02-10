from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import HTTPException, status

from app.core.config import FIREBASE_PROJECT_ID, FIREBASE_SERVICE_ACCOUNT_FILE

try:
    import firebase_admin
    from firebase_admin import auth, credentials, firestore
except ImportError as import_error:  # pragma: no cover - defensive path
    firebase_admin = None
    auth = None
    credentials = None
    firestore = None
    FIREBASE_IMPORT_ERROR = import_error
else:
    FIREBASE_IMPORT_ERROR = None

_INIT_LOCK = Lock()


def _resolve_service_account_path() -> Path:
    path = Path(FIREBASE_SERVICE_ACCOUNT_FILE).expanduser()
    if not path.is_absolute():
        path = (Path(__file__).resolve().parents[2] / path).resolve()
    return path


def initialize_firebase() -> None:
    if FIREBASE_IMPORT_ERROR is not None:
        raise RuntimeError("Firebase SDK missing. Install requirements to use Firebase backends.") from FIREBASE_IMPORT_ERROR

    with _INIT_LOCK:
        if firebase_admin._apps:  # type: ignore[attr-defined]
            return

        service_account_path = _resolve_service_account_path()
        if not service_account_path.exists():
            raise RuntimeError(
                f"Firebase service account file not found: {service_account_path}. "
                "Configure FIREBASE_SERVICE_ACCOUNT_FILE correctly."
            )

        options: dict[str, Any] = {}
        if FIREBASE_PROJECT_ID:
            options["projectId"] = FIREBASE_PROJECT_ID

        credential = credentials.Certificate(str(service_account_path))
        firebase_admin.initialize_app(credential, options or None)


def ensure_firebase_initialized() -> None:
    try:
        initialize_firebase()
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


def verify_firebase_id_token(id_token: str) -> dict[str, Any]:
    ensure_firebase_initialized()

    try:
        return auth.verify_id_token(id_token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase ID token") from exc


def firestore_client():
    ensure_firebase_initialized()
    return firestore.client()


def firestore_module():
    ensure_firebase_initialized()
    return firestore

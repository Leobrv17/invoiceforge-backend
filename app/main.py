from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import API_CONTACT, API_PREFIX, API_TAGS, APP_DESCRIPTION, APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    contact=API_CONTACT,
    openapi_tags=API_TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=API_PREFIX)


@app.get("/", tags=["Health"], summary="Root API")
def root() -> dict[str, str]:
    return {
        "message": "InvoiceForge backend running",
        "docs": "/docs",
        "api": API_PREFIX,
    }

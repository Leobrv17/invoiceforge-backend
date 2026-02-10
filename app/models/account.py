from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AccountDeletionRequestRead(BaseModel):
    requested_at: datetime
    status: str
    message: str

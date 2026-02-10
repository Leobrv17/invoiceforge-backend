from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import ClientType


class ClientBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    type: ClientType
    email: EmailStr


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: str
    created_at: datetime

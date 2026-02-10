from __future__ import annotations

from datetime import date, datetime


class BaseService:
    @staticmethod
    def iso_now() -> str:
        return datetime.utcnow().isoformat()

    @staticmethod
    def year() -> int:
        return date.today().year

    @staticmethod
    def build_id(prefix: str, year: int, value: int, width: int) -> str:
        return f"{prefix}-{year}-{value:0{width}d}"

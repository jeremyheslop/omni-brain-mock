"""Shared helpers: envelopes, errors, auth, paging."""

from __future__ import annotations

import hmac
import os
import re
from dataclasses import dataclass
from typing import Any

from fastapi import Depends, Header, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z?)?$")


class ApiError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class Meta(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str = "ok"
    message: str = "Everything executed fine, no problems"


class Envelope(BaseModel):
    """Accelo style envelope."""

    meta: Meta
    response: Any


bearer_scheme = HTTPBearer(
    auto_error=False,
    description="Any bearer token is accepted unless the server was started with API_KEY, in which case the token must equal API_KEY.",
)


def require_auth(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_api_key: str | None = Header(default=None, include_in_schema=False),
) -> None:
    key = os.environ.get("API_KEY")
    if not key:
        return
    token = creds.credentials if creds else x_api_key
    if not token or not hmac.compare_digest(token.encode(), key.encode()):
        raise ApiError(401, "Missing or invalid credentials. Send 'Authorization: Bearer <API_KEY>'.")


def envelope(response: Any, message: str = "Everything executed fine, no problems", **extra: Any) -> dict:
    meta = {"status": "ok", "message": message}
    meta.update(extra)
    return {"meta": meta, "response": response}


@dataclass
class AcceloPage:
    limit: int
    page: int


def accelo_page(
    limit: int = Query(50, alias="_limit", ge=1, le=100, description="Page size (1 to 100). Default 50."),
    page: int = Query(0, alias="_page", ge=0, description="Zero based page number, like Accelo."),
) -> AcceloPage:
    return AcceloPage(limit, page)


def accelo_list(items: list[dict], pg: AcceloPage, what: str) -> dict:
    total = len(items)
    chunk = items[pg.page * pg.limit:(pg.page + 1) * pg.limit]
    return envelope(chunk, f"Returned {len(chunk)} of {total} {what}", total=total, page=pg.page, limit=pg.limit)


def check_date(value: str | None, name: str) -> str | None:
    if value is None:
        return None
    if not DATE_RE.match(value):
        raise ApiError(400, f"{name} must look like 2026-09-01 or 2026-09-01T12:00:00Z")
    return value


def split_csv(value: str | None) -> list[str] | None:
    return [v.strip() for v in value.split(",") if v.strip()] if value else None


def find(items: list[dict], key: str, value: int, what: str) -> dict:
    for it in items:
        if it[key] == value:
            return it
    raise ApiError(404, f"{what} {value} not found")


@dataclass
class NcPage:
    page: int
    size: int


def nc_page(
    page_number: int = Query(1, alias="pageNumber", ge=1, description="One based page number."),
    page_size: int = Query(50, alias="pageSize", ge=1, le=500, description="Page size (1 to 500). Default 50."),
) -> NcPage:
    return NcPage(page_number, page_size)


def nc_list(items: list[dict], pg: NcPage) -> dict:
    start = (pg.page - 1) * pg.size
    total = len(items)
    return {
        "data": items[start:start + pg.size], "pageNumber": pg.page, "pageSize": pg.size,
        "totalItems": total, "totalPages": max(1, -(-total // pg.size)),
    }

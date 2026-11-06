"""Omni Brain mock API: fake Accelo (PSA), fake N-central (RMM), and a Markdown knowledge base."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import accelo, kb, ncentral
from .common import ApiError, require_auth
from .generate import ANCHOR, ISSUE_TARGET, iso
from .store import content_root, store

VERSION = "1.0.0"

DESCRIPTION = """
Synthetic data and a fake API surface for the **SU GullHacks 2026 "Omni Brain"** challenge,
sponsored by OmniTechPro. **Everything here is fictional.** Companies, people, devices, and tickets are made up.

### What is in the box
* **Accelo** (`/api/v0`): a PSA with companies, contacts, tickets (issues), notes and time (activities), projects (jobs, milestones, tasks), inbound requests, and assets.
* **N-central** (`/ncentral`): an RMM with customers, sites, devices, alerts, and patch status.
* **Knowledge Base** (`/kb`): Markdown documentation files served from the `content/` folder.
* **Admin** (`/admin`): reset the data to its starting state.

### Authentication
Send `Authorization: Bearer <anything>`. Any token is accepted unless the server was started with the `API_KEY`
environment variable, in which case the token must equal that value. `/health`, `/`, and `/docs` are always open.

### Time
The data is anchored to **2026-11-07 09:00 UTC** so it looks current at the event. Writes are stamped from that anchor
plus the real seconds elapsed since the last reset.

### Accelo vs N-central conventions
Accelo style endpoints use `{"meta": {...}, "response": ...}` and `_limit` / `_page` (zero based).
N-central style endpoints use `{"data": ...}` and `pageNumber` / `pageSize` (one based).
"""

TAGS = [
    {"name": "Accelo", "description": "PSA mimic: tickets, projects, time, assets. Writes change memory only."},
    {"name": "N-central", "description": "RMM mimic: customers, devices, alerts, patching. Read only."},
    {"name": "Knowledge Base", "description": "Markdown files from the content folder."},
    {"name": "Admin", "description": "Reset and inspect the mock server."},
    {"name": "System", "description": "Health and landing page."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    minutes = float(os.environ.get("RESET_INTERVAL_MINUTES", "0") or 0)
    if minutes > 0:
        async def loop():
            while True:
                await asyncio.sleep(minutes * 60)
                await asyncio.to_thread(store.reset)
        task = asyncio.create_task(loop())
    yield
    if task:
        task.cancel()


app = FastAPI(title="Omni Brain Mock API", version=VERSION, description=DESCRIPTION, openapi_tags=TAGS,
              lifespan=lifespan, contact={"name": "OmniTechPro", "url": "https://omnitechpro.com"},
              license_info={"name": "MIT"})
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False)


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse({"meta": {"status": "failure", "message": exc.message}}, status_code=exc.status_code)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({"meta": {"status": "failure", "message": str(exc.detail)}}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errs = [f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()]
    return JSONResponse({"meta": {"status": "failure", "message": "Invalid request: " + "; ".join(errs)}}, status_code=400)


app.include_router(accelo.router)
app.include_router(ncentral.router)
app.include_router(kb.router)

admin = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_auth)])


@admin.post("/reset", summary="Reset all data")
def admin_reset(seed: int | None = Query(None, description="Optional different data seed. Omit to get the standard dataset.")):
    """Throw away every write and regenerate the dataset from the seed. Same seed gives identical data."""
    d = store.reset(seed)
    return {"meta": {"status": "ok", "message": "Data regenerated"}, "response": {"seed": store.seed, "counts": d.counts()}}


@admin.get("/stats", summary="Counts and settings")
def admin_stats():
    d = store.d
    return {"seed": store.seed, "anchor": iso(ANCHOR), "now": store.now_iso(), "resets": store.resets,
            "reset_interval_minutes": float(os.environ.get("RESET_INTERVAL_MINUTES", "0") or 0),
            "auth_mode": "api_key" if os.environ.get("API_KEY") else "any_bearer", "content_dir": str(content_root()),
            "counts": d.counts()}


app.include_router(admin)


@app.get("/health", tags=["System"], summary="Health check")
def health():
    return {"status": "ok", "version": VERSION, "issues": len(store.d.issues), "devices": len(store.d.nc_devices)}


@app.get("/", tags=["System"], include_in_schema=False, response_class=HTMLResponse)
def root():
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Omni Brain Mock API</title>
<style>body{{font-family:system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;line-height:1.5}}
code{{background:#eee;padding:.1rem .3rem;border-radius:3px}}</style></head><body>
<h1>Omni Brain Mock API</h1>
<p>Fake Accelo (PSA), fake N-central (RMM), and a Markdown knowledge base for SU GullHacks 2026.
<strong>All data is fictional.</strong> Version {VERSION}.</p>
<ul>
<li><a href="/docs">Interactive docs (Swagger)</a> and <a href="/redoc">ReDoc</a></li>
<li><a href="/openapi.json">openapi.json</a></li>
<li>Accelo: <a href="/api/v0/issues?_limit=5">/api/v0/issues</a>, <a href="/api/v0/companies">/api/v0/companies</a></li>
<li>N-central: <a href="/ncentral/devices?pageSize=5">/ncentral/devices</a>, <a href="/ncentral/alerts?active=true">/ncentral/alerts?active=true</a></li>
<li>Knowledge base: <a href="/kb/index">/kb/index</a></li>
<li><a href="/health">/health</a></li>
</ul>
<p>Send <code>Authorization: Bearer anything</code> (or your <code>API_KEY</code> if one is set).
Reset data with <code>POST /admin/reset</code>. Seeded around {ISSUE_TARGET} tickets for the week of {iso(ANCHOR)[:10]}.</p>
</body></html>"""

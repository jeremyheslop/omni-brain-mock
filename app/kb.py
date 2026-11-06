"""Knowledge base passthrough: serves Markdown files from content/."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse

from .common import ApiError, require_auth
from .store import content_root

router = APIRouter(prefix="/kb", tags=["Knowledge Base"], dependencies=[Depends(require_auth)])

MD_SUFFIXES = {".md", ".markdown"}
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")


def _title(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = HEADING.match(line)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return path.stem.replace("-", " ").replace("_", " ")


def _safe_resolve(rel: str) -> Path:
    if not rel or "\x00" in rel or "\\" in rel:
        raise ApiError(400, "Invalid path")
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise ApiError(400, "Path must be relative and stay inside content/")
    root = content_root().resolve()
    target = (root / p).resolve()
    if root != target and root not in target.parents:
        raise ApiError(400, "Path must stay inside content/")
    if target.suffix.lower() not in MD_SUFFIXES:
        raise ApiError(400, "Only Markdown files (.md) are served")
    if not target.is_file():
        raise ApiError(404, f"No such file: {rel}")
    return target


@router.get("/index", summary="List all Markdown files",
            responses={200: {"content": {"application/json": {"example": {"count": 1, "files": [{
                "path": "clients/tidewater-ledger-cpas/overview.md", "title": "Tidewater Ledger CPAs", "size": 2048}]}}}}})
def kb_index():
    """Every Markdown file under `content/` with its path, first heading as title, and size in bytes. Scanned on each call, so mounted changes show up immediately. An empty folder returns an empty list."""
    root = content_root()
    files = []
    if root.is_dir():
        resolved_root = root.resolve()
        for p in sorted(root.rglob("*")):
            if p.suffix.lower() in MD_SUFFIXES and p.is_file():
                rp = p.resolve()
                if resolved_root != rp and resolved_root not in rp.parents:
                    continue  # symlink pointing outside content/
                files.append({"path": p.relative_to(root).as_posix(), "title": _title(p), "size": p.stat().st_size})
    return {"count": len(files), "files": files}


@router.get("/file", summary="Get one Markdown file (raw)", response_class=PlainTextResponse)
def kb_file(path: str = Query(..., description="Relative path from /kb/index, e.g. clients/tidewater-ledger-cpas/overview.md")):
    """Raw Markdown as `text/markdown`. Absolute paths, `..`, and anything outside `content/` are rejected with 400."""
    target = _safe_resolve(path)
    return PlainTextResponse(target.read_text(encoding="utf-8", errors="replace"), media_type="text/markdown; charset=utf-8")

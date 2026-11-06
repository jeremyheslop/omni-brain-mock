"""In-memory state holder. Seeded data is regenerated on reset; writes live only here."""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

from .generate import ANCHOR, DEFAULT_SEED, Dataset, generate, iso

ROOT = Path(__file__).resolve().parent.parent


def seed_path() -> Path:
    return Path(os.environ.get("SEED_PATH", ROOT / "seed" / "clients.json"))


def content_root() -> Path:
    return Path(os.environ.get("CONTENT_DIR", ROOT / "content"))


class Store:
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.seed = int(os.environ.get("DATA_SEED", DEFAULT_SEED))
        self.resets = 0
        self.started = time.monotonic()
        self.d: Dataset = generate(seed_path(), self.seed)

    def reset(self, seed: int | None = None) -> Dataset:
        with self.lock:
            if seed is not None:
                self.seed = seed
            self.d = generate(seed_path(), self.seed)
            self.started = time.monotonic()
            self.resets += 1
            return self.d

    def now(self) -> datetime:
        """Mock 'current time': the anchor plus real seconds elapsed since the last reset."""
        return ANCHOR + timedelta(seconds=int(time.monotonic() - self.started))

    def now_iso(self) -> str:
        return iso(self.now()) or ""


store = Store()

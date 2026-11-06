import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402
from app.store import store  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_state(client):
    """Writes made by a test are wiped afterwards, so every test sees pristine seeded data."""
    yield
    store.reset()


@pytest.fixture()
def content_dir(tmp_path, monkeypatch):
    (tmp_path / "clients").mkdir()
    (tmp_path / "clients" / "acme.md").write_text("intro line\n\n# Acme Corp\n\nHello\n", encoding="utf-8")
    (tmp_path / "top.md").write_text("# Top Level\n", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("not markdown", encoding="utf-8")
    secret = tmp_path.parent / "secret.md"
    secret.write_text("# Secret\n", encoding="utf-8")
    monkeypatch.setenv("CONTENT_DIR", str(tmp_path))
    return tmp_path

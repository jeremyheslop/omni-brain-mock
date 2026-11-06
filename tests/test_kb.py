import pytest


def test_index_lists_markdown_with_titles(client, content_dir):
    body = client.get("/kb/index").json()
    paths = {f["path"]: f for f in body["files"]}
    assert set(paths) == {"clients/acme.md", "top.md"}
    assert paths["clients/acme.md"]["title"] == "Acme Corp"
    assert paths["top.md"]["size"] > 0
    assert body["count"] == 2


def test_empty_content_dir_ok(client, tmp_path, monkeypatch):
    monkeypatch.setenv("CONTENT_DIR", str(tmp_path / "does-not-exist"))
    assert client.get("/kb/index").json() == {"count": 0, "files": []}
    monkeypatch.setenv("CONTENT_DIR", str(tmp_path))
    assert client.get("/kb/index").json()["files"] == []


def test_file_returns_raw_markdown(client, content_dir):
    r = client.get("/kb/file", params={"path": "clients/acme.md"})
    assert r.status_code == 200 and r.text.startswith("intro line")
    assert r.headers["content-type"].startswith("text/markdown")


@pytest.mark.parametrize("bad", ["../secret.md", "clients/../../secret.md", "/etc/passwd", "..%2Fsecret.md",
                                 "clients\\..\\..\\secret.md", "....//secret.md", "notes.txt", "%00.md"])
def test_traversal_and_non_markdown_blocked(client, content_dir, bad):
    r = client.get("/kb/file", params={"path": bad})
    assert r.status_code in (400, 404)
    assert "Secret" not in r.text


def test_symlink_escape_blocked(client, content_dir):
    (content_dir / "link.md").symlink_to(content_dir.parent / "secret.md")
    assert client.get("/kb/file", params={"path": "link.md"}).status_code == 400
    assert "link.md" not in {f["path"] for f in client.get("/kb/index").json()["files"]}


def test_missing_file_404(client, content_dir):
    assert client.get("/kb/file", params={"path": "nope.md"}).status_code == 404

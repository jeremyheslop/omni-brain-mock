import pytest

ACCELO = ["/api/v0/companies", "/api/v0/companies/1001", "/api/v0/contacts", "/api/v0/issues", "/api/v0/issues/10001",
          "/api/v0/activities", "/api/v0/jobs", "/api/v0/jobs/701", "/api/v0/milestones", "/api/v0/tasks",
          "/api/v0/tasks/8001", "/api/v0/requests", "/api/v0/assets", "/api/v0/staff", "/api/v0/staff/1",
          "/api/v0/segmentations", "/api/v0/segmentations?_filters=link_type(company)", "/api/v0/companies/profiles/fields",
          "/api/v0/companies/1001/segmentations", "/api/v0/companies/1001/profiles/values"]
NCENTRAL = ["/ncentral/customers", "/ncentral/customers/5001", "/ncentral/customers/5001/devices",
            "/ncentral/customers/5001/sites", "/ncentral/devices", "/ncentral/devices/20001",
            "/ncentral/devices/20001/patch-status", "/ncentral/alerts", "/ncentral/alerts?active=true",
            "/ncentral/patch-status", "/ncentral/sites"]
OTHER = ["/health", "/", "/docs", "/openapi.json", "/kb/index", "/admin/stats"]


@pytest.mark.parametrize("url", ACCELO + NCENTRAL + OTHER)
def test_get_ok(client, url):
    assert client.get(url).status_code == 200


def test_accelo_envelope(client):
    body = client.get("/api/v0/issues?_limit=3").json()
    assert body["meta"]["status"] == "ok"
    assert len(body["response"]) == 3
    issue = body["response"][0]
    for key in ("id", "title", "description", "standing", "against_type", "against_id", "assignee", "date_submitted", "date_resolved"):
        assert key in issue
    assert issue["against_type"] == "company"


def test_ncentral_envelope(client):
    body = client.get("/ncentral/devices?pageSize=10&pageNumber=2").json()
    assert body["pageNumber"] == 2 and body["pageSize"] == 10 and len(body["data"]) == 10
    assert body["totalItems"] > 300


def test_issue_filters(client):
    all_total = client.get("/api/v0/issues").json()["meta"]["total"]
    r = client.get("/api/v0/issues?company_id=1015&status=open&_limit=100").json()
    assert r["response"] and all(i["against_id"] == 1015 and i["status"] == "open" for i in r["response"])
    r = client.get("/api/v0/issues?assignee=2&_limit=100").json()
    assert r["response"] and all(i["assignee"] == 2 for i in r["response"])
    r = client.get("/api/v0/issues?date_opened_after=2026-10-01&_limit=100").json()
    assert 0 < r["meta"]["total"] < all_total
    assert all(i["date_opened"] >= "2026-10-01" for i in r["response"])
    assert client.get("/api/v0/issues?status=bogus").status_code == 400


def test_issue_pagination(client):
    p0 = client.get("/api/v0/issues?_limit=5&_page=0").json()["response"]
    p1 = client.get("/api/v0/issues?_limit=5&_page=1").json()["response"]
    assert len(p0) == len(p1) == 5 and {i["id"] for i in p0}.isdisjoint({i["id"] for i in p1})


def test_activity_and_task_and_device_filters(client):
    acts = client.get("/api/v0/activities?against_type=issue&against_id=10001").json()["response"]
    assert all(a["against_type"] == "issue" and a["against_id"] == 10001 for a in acts)
    od = client.get("/api/v0/tasks?overdue=true&_limit=100").json()["response"]
    assert od and all(t["overdue"] and t["status"] != "complete" for t in od)
    off = client.get("/ncentral/devices?online=false&pageSize=500").json()["data"]
    assert off and all(not d["online"] for d in off)
    w10 = client.get("/ncentral/devices?os=Windows 10&pageSize=500").json()["data"]
    assert w10 and all("Windows 10" in d["os"] for d in w10)
    act = client.get("/ncentral/alerts?active=true&pageSize=500").json()["data"]
    assert act and all(a["active"] for a in act)
    c = client.get("/ncentral/alerts?customer_id=5022&pageSize=500").json()["data"]
    assert all(a["customerId"] == 5022 for a in c)


def test_assets_link_to_devices(client):
    linked = client.get("/api/v0/assets?ncentral_device_id=20001").json()["response"]
    assert len(linked) == 1 and linked[0]["title"] == client.get("/ncentral/devices/20001").json()["data"]["hostname"]


def test_not_found_and_errors(client):
    assert client.get("/api/v0/issues/999999").status_code == 404
    assert client.get("/ncentral/devices/1").status_code == 404
    assert client.get("/api/v0/issues/999999").json()["meta"]["status"] == "failure"
    assert client.post("/api/v0/issues", json={"title": "x"}).status_code == 400


def test_writes_persist_then_reset_clears(client):
    before = client.get("/api/v0/issues").json()["meta"]["total"]
    r = client.post("/api/v0/issues", json={"title": "Test ticket", "company_id": 1001, "priority": "high", "assignee": 3})
    assert r.status_code == 200
    new_id = r.json()["response"]["id"]
    assert client.get(f"/api/v0/issues/{new_id}").json()["response"]["title"] == "Test ticket"
    assert client.get("/api/v0/issues").json()["meta"]["total"] == before + 1

    u = client.put(f"/api/v0/issues/{new_id}", json={"status": "resolved", "assignee": 1}).json()["response"]
    assert u["status"] == "resolved" and u["assignee"] == 1 and u["date_resolved"]
    u = client.put(f"/api/v0/issues/{new_id}", json={"status": "open"}).json()["response"]
    assert u["date_resolved"] is None

    a = client.post("/api/v0/activities", json={"against_type": "issue", "against_id": new_id, "body": "worked on it",
                                                "time_minutes": 45, "billable": True, "owner_id": 2})
    assert a.status_code == 200 and a.json()["response"]["billable_minutes"] == 45
    listed = client.get(f"/api/v0/activities?against_type=issue&against_id={new_id}").json()["response"]
    assert len(listed) == 1

    ms = client.get("/api/v0/milestones?_limit=1").json()["response"][0]
    t = client.post("/api/v0/tasks", json={"title": "New task", "against_type": "milestone", "against_id": ms["id"],
                                           "assignee": 2, "date_due": "2026-11-20"})
    assert t.status_code == 200
    tid = t.json()["response"]["id"]
    done = client.put(f"/api/v0/tasks/{tid}", json={"complete": True}).json()["response"]
    assert done["status"] == "complete" and done["date_completed"]
    moved = client.put(f"/api/v0/tasks/{tid}", json={"status": "inprogress", "assignee": 4}).json()["response"]
    assert moved["status"] == "inprogress" and moved["assignee"] == 4

    reset = client.post("/admin/reset")
    assert reset.status_code == 200
    assert client.get("/api/v0/issues").json()["meta"]["total"] == before
    assert client.get(f"/api/v0/issues/{new_id}").status_code == 404
    assert client.get(f"/api/v0/tasks/{tid}").status_code == 404


def test_auth_default_accepts_any_bearer(client):
    assert client.get("/api/v0/staff", headers={"Authorization": "Bearer whatever"}).status_code == 200
    assert client.get("/api/v0/staff").status_code == 200


def test_auth_api_key(client, monkeypatch):
    monkeypatch.setenv("API_KEY", "s3cret")
    assert client.get("/api/v0/staff").status_code == 401
    assert client.get("/api/v0/staff", headers={"Authorization": "Bearer nope"}).status_code == 401
    assert client.get("/api/v0/staff", headers={"Authorization": "Bearer s3cret"}).status_code == 200
    assert client.get("/ncentral/customers", headers={"Authorization": "Bearer nope"}).status_code == 401
    assert client.get("/health").status_code == 200
    assert client.post("/admin/reset").status_code == 401


def test_cors_open(client):
    r = client.options("/api/v0/issues", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"})
    assert r.headers["access-control-allow-origin"] == "*"

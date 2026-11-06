from app.generate import ANCHOR, generate
from app.store import seed_path


def test_same_seed_same_data():
    a, b = generate(seed_path(), 123), generate(seed_path(), 123)
    assert a.counts() == b.counts()
    assert a.issues == b.issues
    assert a.nc_devices == b.nc_devices
    assert a.nc_alerts == b.nc_alerts
    assert a.tasks == b.tasks


def test_different_seed_differs():
    assert generate(seed_path(), 1).issues != generate(seed_path(), 2).issues


def test_scale_and_stories():
    d = generate(seed_path(), 20261107)
    c = d.counts()
    assert c["companies"] == 25 and c["staff"] == 4
    assert 1800 <= c["issues"] <= 2300
    assert 350 <= c["ncentral_devices"] <= 450
    assert c["ncentral_alerts_active"] > 20
    assert any(not x["online"] for x in d.nc_devices)
    assert any(x["warrantyExpired"] for x in d.nc_devices)
    assert any(x["os"] == "Windows 10 Pro" for x in d.nc_devices)
    # overdue onboarding tasks exist
    onboarding = {j["id"] for j in d.jobs if j["title"] == "New Client Onboarding"}
    today = ANCHOR.strftime("%Y-%m-%d")
    assert any(t["job_id"] in onboarding and t["status"] != "complete" and t["date_due"] < today for t in d.tasks)
    # a client mid onboarding
    assert any(co["status"] == "onboarding" for co in d.companies)
    # no ticket opened after the anchor
    assert max(i["date_opened"] for i in d.issues) <= "2026-11-07T09:00:00Z"

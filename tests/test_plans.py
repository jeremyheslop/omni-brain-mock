"""Service plans, industries, segmentations and company profile fields (mirrors the real Accelo structure)."""

import json
import re
from collections import Counter
from pathlib import Path

import pytest

from app.generate import INDUSTRY_TO_ACCELO, generate
from app.store import seed_path

ROOT = Path(__file__).resolve().parent.parent
SEED = json.loads(seed_path().read_text(encoding="utf-8"))
CLIENTS = {c["id"]: c for c in SEED["clients"]}
INDUSTRIES = SEED["segmentations"]["industry"]["values"]
CORE = SEED["segmentations"]["service_plans"]["core_plans"]
ADDONS = SEED["segmentations"]["service_plans"]["add_ons"]


def company(client, cid):
    return client.get(f"/api/v0/companies/{cid}").json()["response"]


def test_segmentations_list(client):
    body = client.get("/api/v0/segmentations?_filters=link_type(company)").json()
    assert body["response"] == [{"id": "1", "title": "Industry"}, {"id": "5", "title": "Service Plans"}]
    assert client.get("/api/v0/segmentations").json()["response"] == body["response"]
    assert client.get("/api/v0/segmentations?_filters=link_type(contact)").json()["response"] == []


def test_company_segmentations_shape(client):
    segs = client.get("/api/v0/companies/1024/segmentations").json()["response"]
    industry, plans = segs
    assert industry == {"id": "1", "title": "Industry", "value": "Education", "values": ["Education"]}
    assert plans["id"] == "5" and plans["title"] == "Service Plans"
    assert plans["values"][0] == "Omni+ Managed"
    assert plans["value"] == ",".join(plans["values"]) and len(plans["values"]) > 2


def test_time_and_materials_company_has_no_core_plan(client):
    c = company(client, 1015)
    assert c["core_plan"] is None and c["industry"] == "Retail"
    segs = client.get("/api/v0/companies/1017/segmentations").json()["response"]
    assert [s["title"] for s in segs] == ["Industry", "Service Plans"]
    assert segs[1]["values"] == ["Email Management"]
    bare = client.get("/api/v0/companies/1022/segmentations").json()["response"]
    assert [s["title"] for s in bare] == ["Industry"]


def test_company_has_no_service_tier_field(client):
    c = company(client, 1001)
    assert "service_tier" not in c
    assert c["core_plan"] == "Omni+ Proactive" and c["service_plans"][0] == "Omni+ Proactive"
    cust = client.get("/ncentral/customers/5001").json()["data"]
    assert "serviceTier" not in cust


def test_all_values_are_real_accelo_values(client):
    companies = client.get("/api/v0/companies?_limit=100").json()["response"]
    assert len(companies) == 25
    for c in companies:
        assert c["industry"] in INDUSTRIES
        assert len({p for p in c["service_plans"] if p in CORE}) <= 1
        assert all(p in CORE + ADDONS for p in c["service_plans"])
        assert c["core_plan"] is None or c["service_plans"][0] == c["core_plan"]
        assert "T&M" not in c["service_plans"]


def test_plan_distribution(client):
    companies = client.get("/api/v0/companies?_limit=100").json()["response"]
    counts = Counter(c["core_plan"] for c in companies)
    assert counts["Omni+ Basic"] > counts["Omni+ Proactive"] > 0
    assert counts["Omni+ Basic"] > counts["Omni+ Managed"] > 0
    assert 2 <= counts[None] <= 5
    # add-ons: security on financial/legal/health clients, servers on managed plans
    by_id = {c["id"]: c for c in companies}
    for cid in (1001, 1009, 1013, 1016):
        assert "Omni+ Advanced Security" in by_id[cid]["service_plans"]
    assert any("Hosted Website Plan" in c["service_plans"] for c in companies)
    assert any("Omni+ Passportal" in c["service_plans"] for c in companies)


def test_every_seed_industry_slug_is_mapped():
    slugs = {c["industry"] for c in SEED["clients"]}
    assert len(slugs) == 21
    assert slugs <= set(INDUSTRY_TO_ACCELO)
    assert set(INDUSTRY_TO_ACCELO.values()) <= set(INDUSTRIES)
    assert INDUSTRY_TO_ACCELO["accounting"] == INDUSTRY_TO_ACCELO["title-escrow"] == "Financial Services"
    assert INDUSTRY_TO_ACCELO["dental"] == INDUSTRY_TO_ACCELO["veterinary"] == "Healthcare"


def test_church_is_church(client):
    assert company(client, 1018)["industry"] == "Church"


def test_company_filters(client):
    tm = client.get("/api/v0/companies?service_plan=none").json()
    assert {c["id"] for c in tm["response"]} == {1015, 1017, 1022}
    managed = client.get("/api/v0/companies?service_plan=Omni%2B Managed").json()["response"]
    assert {c["id"] for c in managed} == {1008, 1009, 1013, 1016, 1024}
    email = client.get("/api/v0/companies?service_plan=email management").json()["response"]
    assert email and all("Email Management" in c["service_plans"] for c in email)
    fin = client.get("/api/v0/companies?industry=financial services").json()["response"]
    assert {c["id"] for c in fin} >= {1001, 1002, 1003, 1007, 1016, 1017}
    assert all(c["industry"] == "Financial Services" for c in fin)


def test_profile_fields(client):
    r = client.get("/api/v0/companies/profiles/fields").json()["response"]
    assert {"id": "4", "field_name": "Parent Company", "field_type": "lookup"} in r
    assert {"id": "5", "field_name": "Employee", "field_type": "integer"} in r
    assert len(r) == 2


def test_profile_values_and_parents(client):
    child = client.get("/api/v0/companies/1007/profiles/values").json()["response"]
    parent_row = next(v for v in child if v["field_name"] == "Parent Company")
    assert parent_row["field_type"] == "lookup" and parent_row["value"] == "Eastern Shore Credit Union Services"
    assert parent_row["value_type"] == "company" and parent_row["value_id"] == "1016"
    emp = next(v for v in child if v["field_name"] == "Employee")
    assert emp["value"] == "8" and emp["field_type"] == "integer"

    with_parent = []
    for cid in CLIENTS:
        rows = client.get(f"/api/v0/companies/{cid}/profiles/values").json()["response"]
        row = next(v for v in rows if v["field_name"] == "Parent Company")
        if row["value"]:
            with_parent.append((cid, row["value_id"]))
        else:
            assert row["value"] is None and row["value_id"] is None
    assert sorted(with_parent) == [(1007, "1016"), (1020, "1013")]


@pytest.mark.parametrize("path", ["segmentations", "profiles/values"])
def test_unknown_company_404(client, path):
    r = client.get(f"/api/v0/companies/999999/{path}")
    assert r.status_code == 404 and r.json()["meta"]["status"] == "failure"


def test_profiles_fields_not_shadowed_by_company_id_route(client):
    assert client.get("/api/v0/companies/profiles/fields").status_code == 200
    assert client.get("/api/v0/companies/notanumber").status_code == 400


def test_plan_drives_generation():
    d = generate(seed_path(), 20261107)
    pol = {p["patchPolicy"] for p in d.nc_patch.values() if p["patchManaged"]}
    assert pol == {"Basic - Monthly", "Proactive - Bi-Weekly", "Managed - Weekly"} | ({"Unmanaged - On Request"} & pol)
    co = {c["id"]: c for c in d.companies}
    assert co[1009]["sla_response_minutes"] == 60 and co[1015]["sla_response_minutes"] == 480
    assert co[1001]["sla_response_minutes"] == 120 and co[1002]["sla_response_minutes"] == 240


# ------------------------------------------------------------------ knowledge base consistency
def _meta(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines()[:20]:
        m = re.match(r"^([a-z_]+): (.*)$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def test_client_docs_match_seed():
    for c in SEED["clients"]:
        meta = _meta(ROOT / "content" / "clients" / f"{c['slug']}.md")
        assert meta["industry"] == c["accelo_industry"]
        assert meta["core_plan"] == (c["core_plan"] or "none (time and materials)")
        assert meta["service_plans"] == (", ".join(c["service_plans"]) or "none")
        assert "service_tier" not in meta
        text = (ROOT / "content" / "clients" / f"{c['slug']}.md").read_text(encoding="utf-8")
        assert "## Service plans and contract notes" in text


def test_content_uses_service_plan_vocabulary():
    assert (ROOT / "content" / "company" / "service-plans.md").exists()
    assert not (ROOT / "content" / "company" / "service-tiers.md").exists()
    banned = re.compile(r"managed-(essentials|pro|premier)|service[_ -]tiers?|all-tiers|\bservice tier\b", re.I)
    for f in list((ROOT / "content").rglob("*.md")) + [ROOT / "README.md"]:
        text = f.read_text(encoding="utf-8")
        assert not banned.search(text), f"old tier wording in {f}"
        assert chr(0x2014) not in text, f"em dash in {f}"


def test_service_plans_doc_has_no_prices():
    text = (ROOT / "content" / "company" / "service-plans.md").read_text(encoding="utf-8")
    assert "$" not in text and not re.search(r"\b\d+\s*(usd|dollars)\b", text, re.I)
    for name in ("Omni+ Basic", "Omni+ Proactive", "Omni+ Managed", "Omni+ Advanced Security", "Omni+ Passportal", "Hosted Cloud Server"):
        assert name in text

"""Accelo (PSA) mimic under /api/v0/."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from .common import (AcceloPage, ApiError, Envelope, accelo_list, accelo_page, check_date, envelope, find,
                     require_auth, split_csv)
from .generate import PROFILE_FIELDS, SEG_INDUSTRY_ID, SEG_PLANS_ID
from .store import store

router = APIRouter(prefix="/api/v0", tags=["Accelo"], dependencies=[Depends(require_auth)])

ISSUE_STATUSES = ("open", "inprogress", "resolved", "closed")
PRIORITIES = ("low", "normal", "high", "urgent")
TASK_STATUSES = ("pending", "inprogress", "complete")


def _ex(response: object, message: str = "Everything executed fine, no problems") -> dict:
    return {200: {"description": "Accelo style envelope", "content": {"application/json": {"example": {
        "meta": {"status": "ok", "message": message}, "response": response}}}}}


ISSUE_EXAMPLE = {
    "id": 10042, "title": "Outlook keeps asking for credentials (Dana)", "description": "Outlook on TLC-WS03 prompts for a password every few minutes.",
    "status": "inprogress", "standing": "open", "priority": "normal", "class": "Email & M365", "against_type": "company",
    "against_id": 1001, "contact_id": 3004, "assignee": 3, "assignee_name": "Jordan Blake",
    "date_opened": "2026-11-05T14:02:11Z", "date_submitted": "2026-11-05T14:02:11Z", "date_resolved": None,
    "response_minutes": 42, "resolution_minutes": None,
}


def S():
    return store.d


def _parse(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


def _staff_name(sid: int | None) -> str | None:
    if sid is None:
        return None
    return find(S().staff, "id", sid, "Staff member")["name"]


def _need_company(cid: int) -> dict:
    return find(S().companies, "id", cid, "Company")


# --------------------------------------------------------------------- reads
COMPANY_EXAMPLE = {
    "id": 1001, "name": "Tidewater Ledger CPAs", "industry": "Financial Services", "core_plan": "Omni+ Proactive",
    "service_plans": ["Omni+ Proactive", "Omni+ Advanced Security", "Omni+ Server", "Server Backup", "Email Management"],
}


@router.get("/companies", summary="List companies", response_model=Envelope, responses=_ex([COMPANY_EXAMPLE]))
def list_companies(pg: AcceloPage = Depends(accelo_page),
                   q: str | None = Query(None, description="Case insensitive name search"),
                   service_plan: str | None = Query(None, description="Only companies that have this Service Plans value, e.g. 'Omni+ Basic' or 'Email Management'. Use 'none' for companies with no core plan (time and materials)."),
                   industry: str | None = Query(None, description="Accelo Industry value, e.g. 'Financial Services' (case insensitive)")):
    """Companies (your clients). IDs match the shared seed file (1001 to 1025).

    `industry` and `service_plans` are convenience copies of the company's Accelo segmentations
    (see `/companies/{id}/segmentations`). A company with no core plan is billed time and materials (T&M).
    """
    items = S().companies
    if q:
        items = [c for c in items if q.lower() in c["name"].lower()]
    if service_plan:
        if service_plan.lower() == "none":
            items = [c for c in items if not c["core_plan"]]
        else:
            items = [c for c in items if service_plan.lower() in (p.lower() for p in c["service_plans"])]
    if industry:
        items = [c for c in items if c["industry"].lower() == industry.lower()]
    return accelo_list(items, pg, "companies")


def _segmentation_defs() -> list[dict]:
    return [{"id": str(SEG_INDUSTRY_ID), "title": "Industry"}, {"id": str(SEG_PLANS_ID), "title": "Service Plans"}]


@router.get("/segmentations", summary="List segmentations (categories)", response_model=Envelope,
            responses=_ex([{"id": "1", "title": "Industry"}, {"id": "5", "title": "Service Plans"}]))
def list_segmentations(pg: AcceloPage = Depends(accelo_page),
                       filters: str | None = Query(None, alias="_filters", description="Accelo style filter. Only `link_type(company)` is meaningful here, e.g. `_filters=link_type(company)`.")):
    """Segmentations are Accelo's custom categories. In this instance only companies use them:
    `Industry` (one value) and `Service Plans` (zero or more values)."""
    items = _segmentation_defs()
    if filters:
        m = re.search(r"link_type\(([^)]*)\)", filters)
        if m and m.group(1).strip().lower() != "company":
            items = []
    return accelo_list(items, pg, "segmentations")


def company_segmentations(c: dict) -> list[dict]:
    out = [{"id": str(SEG_INDUSTRY_ID), "title": "Industry", "value": c["industry"], "values": [c["industry"]]}]
    if c["service_plans"]:
        out.append({"id": str(SEG_PLANS_ID), "title": "Service Plans", "value": ",".join(c["service_plans"]),
                    "values": list(c["service_plans"])})
    return out


@router.get("/companies/profiles/fields", summary="List company custom profile fields", response_model=Envelope,
            responses=_ex([{"id": "4", "field_name": "Parent Company", "field_type": "lookup"},
                           {"id": "5", "field_name": "Employee", "field_type": "integer"}]))
def list_company_profile_fields(pg: AcceloPage = Depends(accelo_page)):
    """The custom profile fields defined on companies. This mock has `Parent Company` (a lookup to another company) and `Employee` (head count)."""
    return accelo_list(PROFILE_FIELDS, pg, "profile fields")


@router.get("/companies/{company_id}/segmentations", summary="Get a company's segmentations", response_model=Envelope,
            responses=_ex([{"id": "1", "title": "Industry", "value": "Education", "values": ["Education"]},
                           {"id": "5", "title": "Service Plans", "value": "Omni+ Managed,Omni+ Advanced Security,Email Management",
                            "values": ["Omni+ Managed", "Omni+ Advanced Security", "Email Management"]}]))
def get_company_segmentations(company_id: int):
    """Industry plus Service Plans for one company. Service Plans is multi-valued (`values` is the list, `value` the comma joined string).
    A company with no Service Plans (time and materials) has no `Service Plans` entry."""
    return envelope(company_segmentations(_need_company(company_id)))


@router.get("/companies/{company_id}/profiles/values", summary="Get a company's custom profile values", response_model=Envelope,
            responses=_ex([{"id": "100704", "field_id": "4", "field_name": "Parent Company", "field_type": "lookup",
                            "value": "Eastern Shore Credit Union Services", "value_type": "company", "value_id": "1016"},
                           {"id": "100705", "field_id": "5", "field_name": "Employee", "field_type": "integer",
                            "value": "8", "value_type": None, "value_id": None}]))
def get_company_profile_values(company_id: int):
    """Custom field values for one company. Every defined field is returned; `value` is null when the field is empty.
    For the `Parent Company` lookup, `value` is the parent's name and `value_id` is its company id."""
    c = _need_company(company_id)
    parent_id = S().parent_of.get(company_id)
    parent = next((x for x in S().companies if x["id"] == parent_id), None) if parent_id else None
    rows = []
    for f in PROFILE_FIELDS:
        row = {"id": f"{company_id}{int(f['id']):02d}", "company_id": company_id, "field_id": f["id"],
               "field_name": f["field_name"], "field_type": f["field_type"]}
        if f["field_name"] == "Parent Company":
            row.update(value=parent["name"] if parent else None, value_type="company" if parent else None,
                       value_id=str(parent["id"]) if parent else None)
        else:
            row.update(value=str(c["employee_count"]), value_type=None, value_id=None)
        rows.append(row)
    return envelope(rows)


@router.get("/companies/{company_id}", summary="Get one company", response_model=Envelope)
def get_company(company_id: int):
    return envelope(_need_company(company_id))


@router.get("/contacts", summary="List contacts", response_model=Envelope)
def list_contacts(pg: AcceloPage = Depends(accelo_page), company_id: int | None = None, q: str | None = None):
    """People at client companies. Emails use the pattern name@<slug>.example."""
    items = S().contacts
    if company_id is not None:
        items = [c for c in items if c["company_id"] == company_id]
    if q:
        items = [c for c in items if q.lower() in c["name"].lower() or q.lower() in c["email"].lower()]
    return accelo_list(items, pg, "contacts")


@router.get("/contacts/{contact_id}", summary="Get one contact", response_model=Envelope)
def get_contact(contact_id: int):
    return envelope(find(S().contacts, "id", contact_id, "Contact"))


@router.get("/issues", summary="List issues (tickets)", response_model=Envelope,
            responses=_ex([ISSUE_EXAMPLE]))
def list_issues(
    pg: AcceloPage = Depends(accelo_page),
    company_id: int | None = Query(None, description="Only tickets for this company"),
    status: str | None = Query(None, description="open, inprogress, resolved, closed. Comma separated list allowed."),
    standing: str | None = Query(None, description="open or closed"),
    assignee: int | None = Query(None, description="Staff id of the assigned technician"),
    priority: str | None = None,
    issue_class: str | None = Query(None, alias="class", description="e.g. Help Desk, Network, Security, Hardware, Backup, Server, Onboarding, Email & M365"),
    date_opened_after: str | None = Query(None, description="ISO date or datetime, inclusive"),
    date_opened_before: str | None = Query(None, description="ISO date or datetime, exclusive"),
    q: str | None = Query(None, description="Case insensitive search in title and description"),
):
    """Tickets, newest first. Page with `_limit` (max 100) and `_page` (zero based)."""
    items = S().issues
    if company_id is not None:
        items = [i for i in items if i["against_id"] == company_id]
    sts = split_csv(status)
    if sts:
        bad = [s for s in sts if s not in ISSUE_STATUSES]
        if bad:
            raise ApiError(400, f"Unknown status {bad}. Use one of {list(ISSUE_STATUSES)}")
        items = [i for i in items if i["status"] in sts]
    if standing:
        items = [i for i in items if i["standing"] == standing]
    if assignee is not None:
        items = [i for i in items if i["assignee"] == assignee]
    if priority:
        items = [i for i in items if i["priority"] == priority]
    if issue_class:
        items = [i for i in items if i["class"].lower() == issue_class.lower()]
    after = check_date(date_opened_after, "date_opened_after")
    before = check_date(date_opened_before, "date_opened_before")
    if after:
        items = [i for i in items if i["date_opened"] >= after]
    if before:
        items = [i for i in items if i["date_opened"] < before]
    if q:
        ql = q.lower()
        items = [i for i in items if ql in i["title"].lower() or ql in i["description"].lower()]
    items = sorted(items, key=lambda i: (i["date_opened"], i["id"]), reverse=True)
    return accelo_list(items, pg, "issues")


@router.get("/issues/{issue_id}", summary="Get one issue", response_model=Envelope)
def get_issue(issue_id: int):
    return envelope(find(S().issues, "id", issue_id, "Issue"))


@router.get("/activities", summary="List activities (notes and time entries)", response_model=Envelope)
def list_activities(
    pg: AcceloPage = Depends(accelo_page),
    against_type: Literal["issue", "job", "task", "company"] | None = Query(None, description="What the activity is logged against"),
    against_id: int | None = None,
    company_id: int | None = None,
    owner_id: int | None = Query(None, description="Staff id who logged it"),
    billable: bool | None = None,
):
    """Notes and time entries, newest first. Filter by `against_type` and `against_id` to get the history of one ticket or project."""
    items = S().activities
    if against_type:
        items = [a for a in items if a["against_type"] == against_type]
    if against_id is not None:
        items = [a for a in items if a["against_id"] == against_id]
    if company_id is not None:
        items = [a for a in items if a["company_id"] == company_id]
    if owner_id is not None:
        items = [a for a in items if a["owner_id"] == owner_id]
    if billable is not None:
        items = [a for a in items if a["billable"] == billable]
    items = sorted(items, key=lambda a: (a["date_created"], a["id"]), reverse=True)
    return accelo_list(items, pg, "activities")


def _job_view(j: dict) -> dict:
    tasks = [t for t in S().tasks if t["job_id"] == j["id"]]
    done = sum(1 for t in tasks if t["status"] == "complete")
    out = dict(j)
    out["task_count"] = len(tasks)
    out["tasks_complete"] = done
    out["percent_complete"] = round(100 * done / len(tasks)) if tasks else 0
    return out


def _milestone_view(m: dict) -> dict:
    tasks = [t for t in S().tasks if t["milestone_id"] == m["id"]]
    done = sum(1 for t in tasks if t["status"] == "complete")
    out = dict(m)
    out["status"] = "complete" if tasks and done == len(tasks) else ("pending" if not any(t["status"] != "pending" for t in tasks) else "inprogress")
    out["task_count"] = len(tasks)
    return out


def _task_view(t: dict) -> dict:
    out = dict(t)
    out["overdue"] = t["status"] != "complete" and t["date_due"] is not None and t["date_due"] < store.now().strftime("%Y-%m-%d")
    return out


@router.get("/jobs", summary="List jobs (projects)", response_model=Envelope)
def list_jobs(pg: AcceloPage = Depends(accelo_page), company_id: int | None = None,
              status: str | None = Query(None, description="active, completed, on_hold"), title: str | None = None):
    """Projects such as New Client Onboarding, Server Migration, or M365 Rollout."""
    items = S().jobs
    if company_id is not None:
        items = [j for j in items if j["company_id"] == company_id]
    if status:
        items = [j for j in items if j["status"] == status]
    if title:
        items = [j for j in items if title.lower() in j["title"].lower()]
    return accelo_list([_job_view(j) for j in items], pg, "jobs")


@router.get("/jobs/{job_id}", summary="Get one job", response_model=Envelope)
def get_job(job_id: int):
    return envelope(_job_view(find(S().jobs, "id", job_id, "Job")))


@router.get("/milestones", summary="List milestones", response_model=Envelope)
def list_milestones(pg: AcceloPage = Depends(accelo_page), job_id: int | None = None, company_id: int | None = None,
                    status: str | None = Query(None, description="pending, inprogress, complete (derived from tasks)")):
    items = S().milestones
    if job_id is not None:
        items = [m for m in items if m["job_id"] == job_id]
    if company_id is not None:
        items = [m for m in items if m["company_id"] == company_id]
    views = [_milestone_view(m) for m in items]
    if status:
        views = [m for m in views if m["status"] == status]
    return accelo_list(views, pg, "milestones")


@router.get("/tasks", summary="List tasks", response_model=Envelope)
def list_tasks(pg: AcceloPage = Depends(accelo_page), job_id: int | None = None, milestone_id: int | None = None,
               company_id: int | None = None,
               status: str | None = Query(None, description="pending, inprogress, complete. Comma separated list allowed."),
               assignee: int | None = None,
               overdue: bool | None = Query(None, description="true: past due and not complete")):
    """Project tasks. Each task includes a computed `overdue` flag."""
    items = S().tasks
    if job_id is not None:
        items = [t for t in items if t["job_id"] == job_id]
    if milestone_id is not None:
        items = [t for t in items if t["milestone_id"] == milestone_id]
    if company_id is not None:
        items = [t for t in items if t["company_id"] == company_id]
    sts = split_csv(status)
    if sts:
        bad = [s for s in sts if s not in TASK_STATUSES]
        if bad:
            raise ApiError(400, f"Unknown status {bad}. Use one of {list(TASK_STATUSES)}")
        items = [t for t in items if t["status"] in sts]
    if assignee is not None:
        items = [t for t in items if t["assignee"] == assignee]
    views = [_task_view(t) for t in items]
    if overdue is not None:
        views = [t for t in views if t["overdue"] == overdue]
    views.sort(key=lambda t: (t["date_due"] or "", t["id"]))
    return accelo_list(views, pg, "tasks")


@router.get("/tasks/{task_id}", summary="Get one task", response_model=Envelope)
def get_task(task_id: int):
    return envelope(_task_view(find(S().tasks, "id", task_id, "Task")))


@router.get("/requests", summary="List requests (inbound emails not yet ticketed)", response_model=Envelope)
def list_requests(pg: AcceloPage = Depends(accelo_page), company_id: int | None = None, status: str | None = None):
    """Emails that arrived but have not been turned into tickets. A good source for triage ideas."""
    items = S().requests
    if company_id is not None:
        items = [r for r in items if r["company_id"] == company_id]
    if status:
        items = [r for r in items if r["status"] == status]
    items = sorted(items, key=lambda r: r["date_received"], reverse=True)
    return accelo_list(items, pg, "requests")


@router.get("/assets", summary="List assets", response_model=Envelope)
def list_assets(pg: AcceloPage = Depends(accelo_page), company_id: int | None = None, asset_type: str | None = None,
                status: str | None = Query(None, description="active, retired, in_storage"),
                ncentral_device_id: int | None = Query(None, description="Find the asset linked to an N-central device")):
    """Asset records in the PSA. Many link to an N-central device through `ncentral_device_id`."""
    items = S().assets
    if company_id is not None:
        items = [a for a in items if a["company_id"] == company_id]
    if asset_type:
        items = [a for a in items if a["asset_type"].lower() == asset_type.lower()]
    if status:
        items = [a for a in items if a["status"] == status]
    if ncentral_device_id is not None:
        items = [a for a in items if a["ncentral_device_id"] == ncentral_device_id]
    return accelo_list(items, pg, "assets")


@router.get("/staff", summary="List staff (technicians)", response_model=Envelope)
def list_staff(pg: AcceloPage = Depends(accelo_page)):
    return accelo_list(S().staff, pg, "staff")


@router.get("/staff/{staff_id}", summary="Get one staff member", response_model=Envelope)
def get_staff(staff_id: int):
    return envelope(find(S().staff, "id", staff_id, "Staff member"))


# -------------------------------------------------------------------- writes
class IssueCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, json_schema_extra={"examples": [{
        "title": "Conference room display not working", "description": "HDMI shows no signal.",
        "company_id": 1001, "priority": "normal", "class": "Hardware", "assignee": 2}]})
    title: str = Field(min_length=1)
    description: str = ""
    company_id: int | None = Field(None, description="Company to log against (alias: against_id)")
    against_id: int | None = None
    against_type: Literal["company"] = "company"
    priority: Literal["low", "normal", "high", "urgent"] = "normal"
    issue_class: str = Field("Help Desk", alias="class")
    assignee: int | None = None
    contact_id: int | None = None


class IssueUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"status": "resolved", "assignee": 1}]})
    status: Literal["open", "inprogress", "resolved", "closed"] | None = None
    assignee: int | None = Field(None, description="Staff id. Send null to unassign.")
    priority: Literal["low", "normal", "high", "urgent"] | None = None
    title: str | None = None


class ActivityCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "against_type": "issue", "against_id": 10042, "body": "Reset the profile and tested login.",
        "owner_id": 3, "time_minutes": 30, "billable": False}]})
    against_type: Literal["issue", "job", "task", "company"]
    against_id: int
    subject: str | None = None
    body: str = ""
    owner_id: int | None = Field(None, description="Staff id logging the activity (default 3)")
    time_minutes: int = Field(0, ge=0, le=1440, description="0 creates a note, greater than 0 logs time")
    billable: bool = False


class TaskCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "title": "Order replacement switch", "against_type": "milestone", "against_id": 7001, "assignee": 2,
        "date_due": "2026-11-20"}]})
    title: str = Field(min_length=1)
    description: str = ""
    against_type: Literal["milestone", "job"] = "milestone"
    against_id: int
    assignee: int | None = None
    date_due: str | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"complete": True}, {"status": "inprogress", "assignee": 2}]})
    status: Literal["pending", "inprogress", "complete"] | None = None
    assignee: int | None = None
    complete: bool | None = Field(None, description="true marks complete and stamps date_completed")
    title: str | None = None
    date_due: str | None = None


@router.post("/issues", summary="Create an issue", response_model=Envelope)
def create_issue(body: IssueCreate):
    """Create a ticket. Lives in memory only until `POST /admin/reset`."""
    with store.lock:
        cid = body.company_id or body.against_id
        if cid is None:
            raise ApiError(400, "company_id is required")
        _need_company(cid)
        if body.assignee is not None:
            _staff_name(body.assignee)
        contact = None
        if body.contact_id is not None:
            contact = find(S().contacts, "id", body.contact_id, "Contact")
            if contact["company_id"] != cid:
                raise ApiError(400, "contact does not belong to that company")
        now = store.now_iso()
        row = {
            "id": S().new_id("issue"), "title": body.title, "description": body.description, "status": "open",
            "standing": "open", "priority": body.priority, "class": body.issue_class, "against_type": "company",
            "against_id": cid, "company_id": cid, "contact_id": body.contact_id,
            "contact_name": contact["name"] if contact else None, "assignee": body.assignee,
            "assignee_name": _staff_name(body.assignee), "device_hostname": None, "date_opened": now,
            "date_submitted": now, "date_resolved": None, "date_closed": None, "response_minutes": None,
            "resolution_minutes": None, "sla_response_breached": False,
        }
        S().issues.append(row)
        return envelope(row, "Issue created")


@router.put("/issues/{issue_id}", summary="Update an issue (status, assignee, priority, title)", response_model=Envelope)
def update_issue(issue_id: int, body: IssueUpdate):
    with store.lock:
        issue = find(S().issues, "id", issue_id, "Issue")
        sent = body.model_fields_set
        if "assignee" in sent:
            issue["assignee_name"] = _staff_name(body.assignee)
            issue["assignee"] = body.assignee
        if body.priority:
            issue["priority"] = body.priority
        if body.title:
            issue["title"] = body.title
        if body.status:
            now = store.now_iso()
            issue["status"] = body.status
            issue["standing"] = "open" if body.status in ("open", "inprogress") else "closed"
            if body.status in ("open", "inprogress"):
                issue["date_resolved"] = issue["date_closed"] = issue["resolution_minutes"] = None
            else:
                if not issue["date_resolved"]:
                    issue["date_resolved"] = now
                    issue["resolution_minutes"] = int((_parse(now) - _parse(issue["date_opened"])).total_seconds() // 60)
                issue["date_closed"] = now if body.status == "closed" else None
        return envelope(issue, "Issue updated")


@router.post("/activities", summary="Log a note or time entry", response_model=Envelope)
def create_activity(body: ActivityCreate):
    """Log a note (`time_minutes` 0) or a time entry against an issue, job, task, or company."""
    with store.lock:
        if body.against_type == "issue":
            company_id = find(S().issues, "id", body.against_id, "Issue")["against_id"]
        elif body.against_type == "job":
            company_id = find(S().jobs, "id", body.against_id, "Job")["company_id"]
        elif body.against_type == "task":
            company_id = find(S().tasks, "id", body.against_id, "Task")["company_id"]
        else:
            company_id = _need_company(body.against_id)["id"]
        owner = body.owner_id or 3
        name = _staff_name(owner)
        now = store.now_iso()
        text = body.body or body.subject or ""
        row = {
            "id": S().new_id("activity"), "type": "time" if body.time_minutes else "note",
            "subject": body.subject or text.split(".")[0][:80], "body": text, "against_type": body.against_type,
            "against_id": body.against_id, "company_id": company_id, "owner_type": "staff", "owner_id": owner,
            "owner_name": name, "visibility": "internal" if not body.time_minutes else "all",
            "time_minutes": body.time_minutes, "billable": body.billable,
            "billable_minutes": body.time_minutes if body.billable else 0, "date_created": now, "date_logged": now,
        }
        S().activities.append(row)
        return envelope(row, "Activity logged")


@router.post("/tasks", summary="Create a task", response_model=Envelope)
def create_task(body: TaskCreate):
    with store.lock:
        if body.against_type == "milestone":
            ms = find(S().milestones, "id", body.against_id, "Milestone")
            job_id, milestone_id, company_id = ms["job_id"], ms["id"], ms["company_id"]
        else:
            job = find(S().jobs, "id", body.against_id, "Job")
            job_id, milestone_id, company_id = job["id"], None, job["company_id"]
        due = check_date(body.date_due, "date_due")
        row = {
            "id": S().new_id("task"), "title": body.title, "description": body.description,
            "against_type": body.against_type, "against_id": body.against_id, "milestone_id": milestone_id,
            "job_id": job_id, "company_id": company_id, "assignee": body.assignee,
            "assignee_name": _staff_name(body.assignee), "status": "pending", "standing": "open",
            "date_due": due[:10] if due else None, "date_completed": None, "time_allocated_minutes": 60,
        }
        S().tasks.append(row)
        return envelope(_task_view(row), "Task created")


@router.put("/tasks/{task_id}", summary="Update a task (status, assignee, complete)", response_model=Envelope)
def update_task(task_id: int, body: TaskUpdate):
    with store.lock:
        task = find(S().tasks, "id", task_id, "Task")
        sent = body.model_fields_set
        if "assignee" in sent:
            task["assignee_name"] = _staff_name(body.assignee)
            task["assignee"] = body.assignee
        if body.title:
            task["title"] = body.title
        if body.date_due:
            task["date_due"] = check_date(body.date_due, "date_due")[:10]  # type: ignore[index]
        new_status = body.status
        if body.complete is True:
            new_status = "complete"
        elif body.complete is False and new_status is None and task["status"] == "complete":
            new_status = "pending"
        if new_status:
            task["status"] = new_status
            task["standing"] = "closed" if new_status == "complete" else "open"
            task["date_completed"] = store.now().strftime("%Y-%m-%d") if new_status == "complete" else None
        return envelope(_task_view(task), "Task updated")


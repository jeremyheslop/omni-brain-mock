# Omni Brain Mock API

A self-contained fake backend for the **SU GullHacks 2026 "Omni Brain" challenge** (November 7-8, 2026), sponsored by OmniTechPro.

Your job in the challenge is to build an internal documentation, process-plan, and dashboard app for a small managed service provider (MSP). Real MSPs keep their data in a PSA (ticketing and projects) and an RMM (device monitoring). This server pretends to be both, plus a folder of Markdown docs, so you can build against realistic data without needing any accounts or API keys.

> **Everything here is fake.** The companies, people, emails, devices, tickets, IP addresses, and incidents are synthetic. Any resemblance to a real business is a coincidence. Product names (Accelo, N-central, Microsoft, and so on) belong to their owners and are used only to describe what is being imitated. Nothing in this project talks to the real services.

## What you get

| Piece | Imitates | Base path |
|---|---|---|
| PSA | Accelo | `/api/v0` |
| RMM | N-central | `/ncentral` |
| Docs | A folder of Markdown files | `/kb` |
| Admin | Reset button | `/admin` |

The seeded data covers 25 fictional clients over the previous 12 months: about 2,000 tickets, 7,000+ notes and time entries, 400 devices, hundreds of alerts, projects with milestones and tasks, inbound requests, and assets. The data is anchored to **2026-11-07**, so it looks current on hackathon day.

## Quick start

### Docker (recommended)

```bash
docker run --rm -p 8080:8080 ghcr.io/jeremyheslop/omni-brain-mock:latest
```

Then open <http://localhost:8080> for links and <http://localhost:8080/docs> for interactive API docs. Works on Intel and Apple Silicon.

Quick check:

```bash
curl -H "Authorization: Bearer anything" "http://localhost:8080/api/v0/issues?_limit=2"
```

### Docker Compose (next to your app)

```yaml
services:
  omni-brain-mock:
    image: ghcr.io/jeremyheslop/omni-brain-mock:latest
    ports:
      - "8080:8080"

  my-app:
    build: .
    depends_on:
      - omni-brain-mock
    environment:
      OMNI_API_BASE: "http://omni-brain-mock:8080"   # container to container
    ports:
      - "3000:3000"
```

From inside your compose network use `http://omni-brain-mock:8080`. From your browser use `http://localhost:8080`. A fuller example is in `docker-compose.yml`.

### Without Docker

Python 3.12 is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8080
```

Run the tests with `pip install -r requirements-dev.txt && python -m pytest -q`.

## Authentication

Send `Authorization: Bearer <anything>`. By default **any token is accepted, and the header may even be left out**, so you can start immediately.

If an organizer or your team starts the server with `API_KEY=yoursecret`, every `/api/v0`, `/ncentral`, `/kb`, and `/admin` request must send `Authorization: Bearer yoursecret` (the header `X-API-Key: yoursecret` also works). Wrong or missing keys return 401. `/health`, `/`, and `/docs` stay open.

## Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `API_KEY` | unset | Require this bearer token |
| `RESET_INTERVAL_MINUTES` | off | Regenerate all data every N minutes (wipes writes) |
| `DATA_SEED` | `20261107` | Random seed. Same seed gives identical data |
| `CONTENT_DIR` | `/app/content` | Folder of Markdown served by `/kb` |
| `SEED_PATH` | `/app/seed/clients.json` | Client list |

To use your own Markdown instead of the bundled content, mount a folder:
`docker run -p 8080:8080 -v "$PWD/my-content:/app/content:ro" ghcr.io/jeremyheslop/omni-brain-mock:latest`

## Endpoints

Open `/docs` for parameters, schemas, and a Try it out button.

### Accelo style (`/api/v0`)

Responses look like `{"meta": {"status": "ok", "message": "...", "total": 2025, "page": 0, "limit": 50}, "response": [...]}`. Page with `_limit` (1 to 100) and `_page` (**zero based**, like Accelo). Errors use `{"meta": {"status": "failure", "message": "..."}}`.

| Method and path | Notes |
|---|---|
| `GET /companies`, `/companies/{id}` | Filters: `q`, `service_plan` (a Service Plans value, or `none` for time and materials), `industry` (an Accelo Industry value). Each company carries convenience fields `industry`, `core_plan` and `service_plans` |
| `GET /segmentations` | The company categories: `Industry` and `Service Plans`. Accepts `_filters=link_type(company)` |
| `GET /companies/{id}/segmentations` | The company's Industry (one value) and Service Plans (zero or more values) |
| `GET /companies/profiles/fields` | Custom company fields: `Parent Company` (lookup) and `Employee` (integer) |
| `GET /companies/{id}/profiles/values` | That company's custom field values. Two companies have a parent company |
| `GET /contacts`, `/contacts/{id}` | Filters: `company_id`, `q` |
| `GET /issues`, `/issues/{id}` | Tickets. Filters: `company_id`, `status` (open, inprogress, resolved, closed), `standing`, `assignee`, `priority`, `class`, `date_opened_after`, `date_opened_before`, `q` |
| `GET /activities` | Notes and time. Filters: `against_type`, `against_id`, `company_id`, `owner_id`, `billable` |
| `GET /jobs`, `/jobs/{id}` | Projects. Filters: `company_id`, `status`, `title` |
| `GET /milestones` | Filters: `job_id`, `company_id`, `status` |
| `GET /tasks`, `/tasks/{id}` | Filters: `job_id`, `milestone_id`, `company_id`, `status`, `assignee`, `overdue` |
| `GET /requests` | Inbound emails not yet turned into tickets |
| `GET /assets` | Filters: `company_id`, `asset_type`, `status`, `ncentral_device_id` |
| `GET /staff`, `/staff/{id}` | The four technicians |
| `POST /issues` | Create a ticket (JSON body) |
| `PUT /issues/{id}` | Change `status`, `assignee`, `priority`, `title` |
| `POST /activities` | Log a note, or time with `time_minutes` and `billable` |
| `POST /tasks` | Create a task under a milestone or job |
| `PUT /tasks/{id}` | Change `status` (pending, inprogress, complete), `assignee`, or send `complete: true` |

**Service plans and industry.** Like the real OmniTechPro Accelo instance, a client's plans live in the `Service Plans` segmentation (core plan `Omni+ Basic`, `Omni+ Proactive` or `Omni+ Managed`, plus add-ons such as `Omni+ Advanced Security` or `Server Backup`). A client with no core plan is time and materials (T&M) and may still have add-ons. Industry is the Accelo `Industry` value, for example `Financial Services` or `Church`. The N-central mock has no plan field, as in the real product: join through `externalId` to the Accelo company.

Request bodies are **JSON** (not form encoded like the real product). Dates are ISO 8601 strings, not Unix timestamps.

### N-central style (`/ncentral`)

Responses look like `{"data": [...], "pageNumber": 1, "pageSize": 50, "totalItems": 403, "totalPages": 9}`. Page with `pageNumber` (**one based**) and `pageSize` (1 to 500). Single items come back as `{"data": {...}}`. Fields are camelCase.

| Method and path | Notes |
|---|---|
| `GET /customers`, `/customers/{id}` | Customer ids are 5001 to 5025 |
| `GET /customers/{id}/devices` | Filters: `device_class`, `online` |
| `GET /customers/{id}/sites`, `/sites` | |
| `GET /devices`, `/devices/{id}` | Filters: `customer_id`, `device_class`, `online`, `os`, `warranty_expired`, `q` |
| `GET /devices/{id}/patch-status` | Missing patches, last scan, reboot pending |
| `GET /patch-status` | Bulk version for dashboards. Filters: `customer_id`, `status`, `reboot_pending` |
| `GET /alerts` | Filters: `customer_id`, `device_id`, `active`, `severity`, `service_name` |

### Knowledge base (`/kb`)

| Method and path | Notes |
|---|---|
| `GET /kb/index` | Every Markdown file: `path`, `title` (first heading), `size` |
| `GET /kb/file?path=sops/01-new-client-onboarding.md` | Raw Markdown. Paths outside `content/` are rejected |

### Admin and system

| Method and path | Notes |
|---|---|
| `POST /admin/reset` | Wipe all writes and regenerate. Optional `?seed=N` |
| `GET /admin/stats` | Counts and settings |
| `GET /health` | Liveness |

## Writes and reset

Writes change memory only. Restarting the container, or `POST /admin/reset`, returns everything to the starting state. New tickets, notes, and tasks get timestamps based on the 2026-11-07 anchor plus the real time since the last reset, so they sort after the seeded data. Two teams running their own containers never see each other's changes.

## How the pieces connect

* Accelo company ids (1001 to 1025) match `seed/clients.json`, the client Markdown files in `/kb` (by slug), and N-central `externalId`.
* Accelo assets point at N-central devices with `ncentral_device_id`. N-central devices point back at Accelo contacts with `assignedContactId`.
* Accelo activities, tasks, and milestones hang off issues, jobs, and milestones through `against_type` and `against_id`.
* Technician ids 1 to 4 are the same everywhere.

## Data story hints

You do not need these, but a good dashboard or assistant should be able to find them without being told:

* Some clients have a ticket queue that nobody has touched in a long time.
* A few devices have gone quiet, and one of them matters more than the others.
* Warranty dates and operating system versions tell a story about aging hardware.
* One client is in the middle of onboarding, and some of its tasks are late. Another onboarding looks finished but is not.
* Not every record links up cleanly between the two systems.
* The documentation and the live data do not always agree. Say so when they differ, and say "I don't know" when neither has the answer.

## Project layout

```
app/        FastAPI app, data generator, routers
seed/       clients.json, the shared list of fictional clients and technicians
content/    Markdown knowledge base files
tests/      pytest suite
```

## Credits and license

Built by OmniTechPro / Omni Technology Professionals, Inc. for SU GullHacks 2026. Released under the MIT License (see `LICENSE`). Have fun, and build something great.

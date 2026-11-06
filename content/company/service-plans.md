# OmniTechPro Service Plans

owner: Casey Morgan
last_reviewed: 2026-08-12
tags: company, service-plans, sla, contracts, omni-basic, omni-proactive, omni-managed, time-and-materials, add-ons

Illustrative for the hackathon. The plan names below match the names OmniTechPro uses for its real service plans (they are also the values in the Accelo "Service Plans" category), but the inclusions, response targets and tooling described here are illustrative and made up for this exercise. They are used consistently across every client file and SOP in this folder. No pricing is included on purpose.

## How service plans work

A client can have a **core plan**, plus any number of **add-ons**. Both are recorded as values of the "Service Plans" category on the client's company record in Accelo (the mock API exposes them at `/api/v0/companies/{id}/segmentations`) and in each client file under "Service plans and contract notes". A client with no core plan is billed time and materials (T&M).

The core plan decides:

- how fast we respond (first-response target, by ticket priority P1 to P4)
- whether we monitor and patch devices with N-central
- whether after-hours support is part of the deal or billed on request
- how often we are onsite
- how proactive we are (reviews, planning, vCIO conversations)

Add-ons bolt extra services onto a core plan, or onto a T&M client. Business hours are Monday to Friday, 8:00-5:00 Eastern. Holidays follow the OmniTechPro calendar posted in the shared Google Drive. Priorities are defined in `sops/27-ticket-triage-and-priorities.md`.

## Core plans at a glance

| | T&M (no core plan) | Omni+ Basic | Omni+ Proactive | Omni+ Managed |
|---|---|---|---|---|
| Who it fits | Very small shops with simple needs | Offices that want every computer patched, protected and watched | Offices that depend on IT daily and want us planning ahead | Clients who want IT fully handled, including regulated and high-uptime shops |
| Billing basis | Per ticket, hourly | Per computer | Per user | Per user |
| N-central monitoring and patching | No (agent only if agreed) | Yes | Yes | Yes |
| Antivirus / EDR | Only if bought separately | Yes | Yes | Yes |
| Remote support | Billed per ticket | Included | Included | Included, priority queue |
| After-hours | By agreement per call | By request, after-hours rate | 24x7 on-call for P1 | 24x7 for P1, extended hours for P2 |
| Onsite visits | Billed per visit | Billed per visit | Scheduled visits | Scheduled and priority onsite |
| Proactive work, vCIO, QBRs | None | None | Included | Included, most hands-on |
| Reviews | None | Annual | Semi-annual | Quarterly business review |

## T&M (no core plan)

Pay as you go. We fix things when they break and bill the time. Many clients in Accelo are T&M, and some of them still carry one or two add-ons (for example a hosted website).

- Included: nothing recurring. Each call becomes an Accelo ticket and time is billed against it.
- Response targets: P1 within 4 business hours, P2 next business day, P3 and P4 best effort.
- After-hours: only if agreed on that call. Emergency line is 410-555-0100 but there is no promise of an answer.
- Onsite: scheduled when a tech is free. Travel time is billable.
- Security: we do not manage security tools unless the client buys an add-on or a separate line item.
- Backup: we do not monitor or test backups. If a client asks us to set one up, we document it and make clear in the client file that it is "not monitored".
- Monitoring: no N-central policy. A few T&M clients have the agent installed for remote access only. Alerts for those devices are ignored.
- Typical client files: Assateague Outfitters, Blue Crab Marine Repair, Kingfisher Bookkeeping.

## Omni+ Basic

The entry managed plan, built around the computer. Every covered computer gets patching, antivirus and monitoring, with remote support included.

- Included: N-central agent on every covered computer and server, patch management on the standard schedule, endpoint protection (SentinelOne), DNS filtering (DNSFilter), unlimited remote support during business hours.
- Response targets: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- After-hours: available on request, billed at the after-hours rate. Not on-call.
- Onsite: billed per visit. One annual onsite check is offered but not guaranteed.
- Backup: not part of the plan itself. Backups come from the add-ons (Omni+ Backup, Server Backup). Where backup is in place, success is checked each morning (see `sops/08-daily-backup-check.md`).
- Reviews: annual review with Casey.

## Omni+ Proactive

Priced and scoped per user, with a more proactive relationship. For offices where an hour of downtime costs real money.

- Included: everything in Omni+ Basic, plus proactive work (firewall management and firmware updates, Microsoft 365 hardening such as MFA and conditional access basics, mailbox rule audits when an account is flagged), vCIO conversations and reviews, priority handling, and a documented onboarding for new hires and departures.
- Response targets: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- After-hours: P1 only, through the on-call rotation (Alex primary, Sam secondary, Casey escalation). Planned after-hours work is quoted separately.
- Onsite: scheduled visits (usually quarterly). Extra visits are billed.
- Backup: from the Server Backup and Omni+ Backup add-ons where the client has them. Spot restores are done periodically.
- Reviews: semi-annual.

## Omni+ Managed

IT fully handled for the client, per user. For clients with regulated data or high uptime needs (credit union services, law, healthcare, schools).

- Included: everything in Omni+ Proactive, plus a named technician and backup technician, quarterly business reviews (QBRs), quarterly documented restore tests where backup add-ons exist (see `sops/09-backup-restore-test.md`), priority onsite scheduling, change control with written approval for firewall and server changes, and audit evidence pulls on request (patch reports, access reviews, backup logs).
- Response targets: P1 15 minutes (24x7), P2 1 hour (extended hours 7:00-7:00), P3 2 business hours, P4 next business day.
- After-hours: 24x7 for P1. Extended hours coverage for P2 from 7:00 to 7:00.
- Onsite: scheduled and priority visits. A P1 that cannot be fixed remotely gets a tech onsite as soon as one can arrive.
- Reviews: quarterly.

## Add-ons

Add-ons are separate Service Plans values. They can sit on any core plan, and on a T&M client.

| Add-on | What it covers (illustrative) |
|---|---|
| Omni+ Advanced Security | Extra security services on top of the core plan: stronger endpoint and identity protection, security reviews, phishing training. Common on Omni+ Proactive and Omni+ Managed and on financial, legal and healthcare clients |
| Omni+ Backup | Backup for workstations and cloud data such as Microsoft 365 mailboxes and files |
| Omni+ Server | Monitoring and maintenance for on-premises servers |
| Server Backup | Image backup of servers, with local and cloud copies (Datto SIRIS in most client files) |
| Email Management | Mailbox administration, spam and phishing filtering, and license changes |
| Hosted Website Plan | Hosting and upkeep for the client's website |
| Hosted Cloud Server | A server hosted by OmniTechPro in the cloud for the client |
| Omni+ Passportal | Password and documentation management through Passportal |

## Things that do not change by plan

- Every request is a ticket in Accelo. No ticket, no time, no history.
- Security incidents (see `sops/10-phishing-email-response.md`, `sops/11-suspected-compromised-account.md`, `sops/34-ransomware-response.md`) are treated as P1 on every monitored client. For T&M clients we still respond, but the target is "as soon as we see it".
- Password references are stored as vault paths only, never in tickets or documents.
- CPA clients get a tax-season change freeze from January 15 through April 18 regardless of plan. See `sops/31-cpa-tax-season-software-prep.md`.

## Known mismatches (internal)

- A few older contracts still use the phrase "Total Care" instead of Omni+ Managed. Treat it as Omni+ Managed.
- Some Omni+ Basic clients have a Datto appliance installed before the plans were reworked. Leave it alone, but note it in the client file.
- The Accelo contract name sometimes says "Managed Pro" while the client file says Omni+ Basic. When they disagree, the Accelo Service Plans category and the contract win, and fix the client file.

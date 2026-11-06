# Ticket Triage and Priority Definitions

owner: Jordan Blake
last_reviewed: 2026-09-15
applies_to: all-plans
tags: triage, priorities, accelo, sla, help-desk

## Purpose
Give every incoming request a priority, a category, and an owner within a few minutes, so the right thing gets worked first and the client gets a first response inside their plan's target.

## When to use
Every new ticket in Accelo, whether it came from email, phone, the portal, or an N-central alert. Whoever is on help desk (usually Jordan) triages. If Jordan is out, Alex does it.

## Before you start
- Open the Accelo queue view "Unassigned and New".
- Have the N-central alert list open in a second tab.
- Know the client's service plans. They are on the Accelo contract and in the client file.

## Priority definitions

| Priority | Name | Meaning | Examples |
|---|---|---|---|
| P1 | Critical | Business is down, a security incident is in progress, or data loss is likely | Server down, ransomware suspected, internet down at the only site, phishing with money movement, compromised admin account |
| P2 | High | Major impairment, several users affected, a key application is down or crawling | Line-of-business app unavailable for a department, email down for one person who is the owner, backup failing for 2 nights, VPN down |
| P3 | Normal | One user or one device affected, work can continue some other way | Laptop will not boot, printer not printing for one person, password reset, cannot open a shared folder |
| P4 | Low | A request, a how-to, cosmetic, or project work | New user setup with a future date, add a shortcut, license change, "how do I do X" |

When in doubt between two levels, pick the higher one and adjust after talking to the client. Do not downgrade a security incident.

## First response targets by core plan

| Core plan | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| T&M | 4 business hours | Next business day | Best effort | Best effort |
| Omni+ Basic | 1 business hour | 4 business hours | Next business day | 2 business days |
| Omni+ Proactive | 30 minutes (24x7 on-call) | 2 business hours | 4 business hours | Next business day |
| Omni+ Managed | 15 minutes (24x7) | 1 hour (extended hours 7:00-7:00) | 2 business hours | Next business day |

First response means a real human message or phone call to the client, not the auto-acknowledgement.

## Steps
1. Open the ticket. Read the subject, the body, and the client name. Check the core plan.
   Check: you can say who is affected and what they cannot do.
2. Look in N-central for alerts on the affected client or device in the last 24 hours.
   Check: you know whether this is a known alert, a new alert, or nothing in monitoring.
3. Assign a priority using the table above. Set it in Accelo.
   Check: the SLA clock in Accelo shows the right target for the core plan.
4. Set the category: Help Desk, Security Incident, Backup, Network, New User, Offboarding, Hardware, Project, Billing question, or Other. If it is a security incident, use "Security Incident" and notify Alex.
   Check: category is not left on "General".
5. Assign an owner:
   - Password reset, license, printer, how-to: Jordan.
   - Server, network, firewall, backups, security: Alex.
   - Onsite hardware, cabling, printers that need a visit: Sam.
   - Contract, billing, vendor, serious incident: Casey.
   Check: ticket has exactly one assignee.
6. Send a first response if you are not the owner and the owner cannot reply right away. Tell the client the priority, who has it, and when to expect the next update.
   Check: the response is logged in the ticket.
7. For P1: call the client's primary contact. Do not rely on email. If it is after hours, follow `26-after-hours-emergency-call.md`.
   Check: you spoke to a person or left a voicemail and logged it.
8. Link duplicates. If five people at one client open tickets about the same outage, merge them or link them to one parent ticket.
   Check: parent ticket shows the linked tickets.
9. Check the ticket again at half the response target time if it has not been picked up.

## Gotchas
- N-central alerts auto-create tickets as P3 by default. A Critical alert on a server should be P2 at least. Fix the priority by hand, and tell Alex if the alert rule needs tuning.
- A request from the owner of a business is not automatically higher priority, but we do treat it as P2 when it blocks them from running the business that day.
- "Nothing works" almost always means "something does not work for me". Ask who else is affected before you set P1.
- Tickets from T&M clients still get triaged the same way. The target is different, not the process.
- Phone calls come first, ticket second. Open the ticket while the person is still on the line.
- Do not close a ticket just because the user stopped replying. See the closing rule in `28-time-entry-standards.md`.

## Escalate when
- P1 and nobody has acknowledged within 10 minutes: call Alex, then Casey.
- The client disputes the priority: pass to Casey.
- A ticket mentions law enforcement, regulators, a data breach, or a lawsuit: Casey immediately.

## Documentation and time
- Triage time is usually part of the ticket's first time entry (5 minutes is normal). Do not leave it off.
- Record the priority change reason in the ticket if you changed it after triage.
- Add the category before closing. Reports rely on it.

## Related
- `26-after-hours-emergency-call.md`
- `28-time-entry-standards.md`
- `30-vendor-escalation.md`
- `10-phishing-email-response.md`

# Time Entry Standards

owner: Casey Morgan
last_reviewed: 2026-07-08
applies_to: all-plans
tags: time-entry, accelo, billing, tickets, contracts, reporting

## Purpose
Make every time entry in Accelo clear enough that billing, contract reviews, and client questions can be answered without asking the tech what they meant.

## When to use
Every time you work on something for a client, including phone calls and travel. Also used when you close a ticket, and by Casey on the billing run.

## Before you start
- Time goes against a ticket or a project task, never against the client with no ticket.
- Know the contract type for the client: a managed plan (flat fee plus project hours), T&M (hourly), or block hours. It is on the Accelo contract.
- Have the Accelo timer running or write the time in as soon as you finish. Do not wait until Friday.

## Steps
1. Start from a ticket. If there is no ticket for the work, create one, even for a 5-minute call.
   Check: the ticket has a client, category, and priority.
2. Log time in 0.25 hr increments. Under 8 minutes can round up to 0.25 if it is a separate contact. Do not log 0.1 on twenty tickets.
   Check: the entry shows a rounded duration.
3. Choose the activity type: Help Desk, Network, Server, Security, Backup, Onsite, Travel, Project, Admin (non-billable), or After-Hours. Pick one per entry.
   Check: the type matches the work. After-hours work uses After-Hours even if the task is a password reset.
4. Write a short note that says what you did and the result. Good: "Reset password, cleared cached credentials in Outlook, user confirmed sign-in." Bad: "worked on issue".
   Check: someone who was not there can tell what happened.
5. Mark billable status correctly. Billable: client-requested work, onsite visits, after-hours calls, project work. Non-billable: our own mistake, internal training, tool maintenance, fixing alerts that our own rule caused.
   Check: no non-billable work is marked billable by default.
6. Log travel as a separate Travel entry, round trip, against the onsite ticket. Onsite visits included in a contract (Omni+ Proactive and above) are still logged, with the contract box ticked so reporting shows usage.
7. Closing a ticket: confirm the issue is fixed, add the final note and category, and set the status to Resolved. Wait 2 business days for the client reply before Closed. If the client does not reply after two follow-ups, close it with a note saying so. Do not close because they went quiet after one email.
   Check: status is Resolved or Closed, with a final note.
8. End of day: open "My time" in Accelo and check for tickets with a running timer, or a day with fewer hours than you worked.

## Gotchas
- Alerts that become tickets: time spent investigating an N-central alert goes under the ticket the alert created. If there is none, make one. Do not use "Internal".
- One ticket for several clients is not allowed. Split it.
- Project tasks bill differently from tickets. Do not log project time on a help desk ticket "because it was easier".
- A call that turns into a 2 hour fix: change the priority and category if it is no longer what the ticket says.
- Omni+ Managed QBR prep time is non-billable but must still be logged under the QBR ticket. We use it to judge the contract.
- Editing someone else's entry is not allowed. Ask them or Casey. The billing run locks on the last business day of the month.
- This changed in 2026: After-Hours is now its own activity type. Older entries tagged "Help Desk, after-hours" in the note will not appear in the after-hours report.

## Escalate when
- You think you worked more time than the client will accept: tell Casey before the billing run, not after the invoice.
- A client disputes time: Casey handles it with the ticket history.
- Your entries are being rejected or a contract shows over its limit: Casey.

## Documentation and time
- Ticket notes are customer-facing by default in the portal. Mark internal notes as Internal. No passwords, no frustration.
- Review weekly. Jordan runs a quick report of tickets with no time or no category every Friday.

## Related
- `27-ticket-triage-and-priorities.md`
- `30-vendor-escalation.md`
- `33-onsite-visit-checklist.md`
- `29-client-offboarding.md`

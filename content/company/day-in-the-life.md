# A Day in the Life of an OmniTechPro Tech

owner: Alex Rivera
last_reviewed: 2026-06-30
tags: company, culture, workflow, knowledge, accelo, n-central, passportal

This is one realistic Tuesday for Alex Rivera, the lead tech. It is here so you can see where knowledge actually lives today, and where it goes missing. Everything in it is fictional.

## 6:50 AM: before the first coffee

Alex checks the phone. One text from N-central overnight: a Critical alert on a file server at a client (disk at 94 percent). It was already auto-ticketed in Accelo as a P3. Alex bumps it to P2 because the nightly backup runs on that disk, and leaves a note in the ticket. Knowledge used: which server holds the backup staging folder. That fact is in Alex's head and in a two-year-old Passportal note.

## 7:30 AM: the morning check

The daily routine from `sops/08-daily-backup-check.md`:

1. Open the Datto portal and the Cove console. Look for red or yellow.
2. Open N-central. Sort alerts by severity. Anything Critical not already ticketed gets a ticket.
3. Look at the Accelo queue. Jordan (help desk) has already picked up three password resets. Two tickets are unassigned from overnight.

Two backups failed. One is a known issue (the client turns off their PC at night). One is new. Alex opens a ticket, and spends ten minutes finding the client's backup notes in a Google Doc that Casey wrote in 2024.

## 8:15 AM: the interruptions begin

Jordan messages: a CPA client says scan-to-email stopped working. Alex knows the printer uses an SMTP relay on a nonstandard port because of how the firewall was set up in 2023. That is not written down anywhere except in Alex's memory and a line in an old ticket. Alex tells Jordan the port and the vault path for the relay account.

Then the phone rings: a dental office cannot open the imaging software on one workstation. Alex remotes in through N-central, finds the sensor driver updated overnight, rolls it back. Time entry: 25 minutes, ticket updated.

## 10:00 AM: planned work

Alex has a firewall rule change request for a law firm. The process in `sops/18-firewall-rule-change-request.md` says to get written approval first. The approval is in an email thread, not in the ticket. Alex copies it into Accelo so the next person can see it. Omni+ Managed clients need that paper trail.

## 12:00 PM: lunch, sort of

Casey stops by with a billing question: why did a T&M client get 4.5 hours billed last month? Alex remembers the visit but not the details. Time entries in Accelo have one-line notes ("fixed printer"). Not enough to answer. Alex digs through two tickets and a sticky note.

## 1:00 PM: onsite

Sam Okafor (field tech) is already at a client replacing a switch. He calls Alex because the new switch needs the same VLAN setup as the old one, and the old config backup is not where the notes say. Alex finds it in the UniFi controller export. Sam would have found it faster if the client's page had a "network config backup" link.

Meanwhile a new-hire onboarding comes in from a title company: new user starting Monday. Jordan works from the checklist in `sops/02-new-user-onboarding.md`, but the title company has a wire-fraud training step that is not on the generic checklist. Jordan asks Alex. Alex remembers.

## 3:30 PM: a real problem

A Omni+ Proactive client reports a strange email: a vendor asking to change bank details. This is the kind of thing that costs real money. Alex follows `sops/10-phishing-email-response.md`: pull the message headers, search the tenant for similar messages, block the sender, check for forwarding rules, and call the client (not email) to confirm. This turns into a P1 for an hour. All other work pauses.

## 5:00 PM: wrap up

Alex closes out time entries. Each ticket needs a category, a resolution note, and the time. He writes the phishing incident summary into the Accelo ticket. He also adds a line to the client's page in Passportal about the vendor bank change process, because the next tech should know to call first.

## Where knowledge lives today

| Place | What is in it | Problem |
|---|---|---|
| Accelo | Tickets, time, contracts, client records | Great history, impossible to search by meaning. Notes are terse. |
| N-central | Device inventory, alerts, patch status | Tells you what is wrong, not why or what to do. |
| Passportal | Client documentation and passwords | Stale in places. Gets updated only when someone remembers. |
| Google Drive | SOPs, spreadsheets, one-off notes | Duplicates, old versions, names like "Final FINAL v3". |
| People's heads | Quirks, history, who to call, why a thing was set up that way | The biggest store, and the one that walks out the door. |

## What would help

- A place where a tech can ask "why does scan-to-email use port 465 at this client" and get an answer with a source.
- A clear "I don't know" when nobody wrote it down, so a tech knows to ask a person and then document it.
- Step-by-step plans (like onboarding) that can be checked off, assigned to people, and show up on a dashboard.
- A dashboard that shows stale docs, open onboarding plans, and clients with no recent review.

## Notes for the hackathon

- Not every client has a great page. That is realistic. Some pages are thin or out of date on purpose.
- Contradictions exist between a few documents. A good tool should show both and cite them rather than pick one silently.
- Accelo and N-central data in the mock APIs is separate from these documents. The best answers will combine both.

# Vendor Escalation

owner: Casey Morgan
last_reviewed: 2026-05-27
applies_to: all-plans
tags: vendors, escalation, isp, support, accounts, sla

## Purpose
Know when to open a case with a vendor (ISP, software, hardware, distributor), how to do it so they actually respond, and when to escalate beyond the first support line.

## When to use
- We have done the basic troubleshooting and the fault is in the vendor's product or service (circuit down, bug, license problem, RMA).
- A vendor missed their own response commitment.
- A client's line-of-business vendor (tax, dental, legal, practice management) needs to look at something on their side.

## Before you start
- Check the client file under Vendor contacts and Internet and circuits. It lists account numbers, support phone numbers, and the rep.
- Know who is authorized. ISPs and some software vendors only talk to the account holder. Some clients added us as technical contact, some did not. The client file notes which.
- Have the evidence ready: device names, error text, screenshots, time it started, what you tried.
- Vendor portal logins: `Vault: <client-slug>/isp-portal` or `Vault: <client-slug>/lob-app-admin`. Our reseller accounts: `Vault: omnitechpro/<vendor>`.

## Steps
1. Open or find the Accelo ticket. Add a sub-task "Vendor case" so the open vendor case is visible and the clock is tracked.
   Check: the ticket has a vendor name and a placeholder for the case number.
2. Open the vendor case by their fastest working channel (phone for outages, portal for everything else). Give: client name, account number, site address, a short fault description, what you tested, and the priority you want.
   Check: you have a case or reference number. Write it in the ticket right away.
3. Tell the client what you did and when to expect an update. If the vendor says 4 hours, say 4 hours and check at 3.
   Check: the update is logged in the ticket as visible to the client.
4. Follow up on a schedule: P1 every 30 minutes, P2 every 2 hours, P3 daily. Log every call.
   Check: each follow-up shows in the ticket history with a name and time.
5. Escalate inside the vendor if they miss their promise. Ask for a supervisor or the "duty manager". Use the escalation numbers in the client file or Drive > Vendors > Escalation list. Quote the case number and the time you first called.
   Check: you have a name for the escalation contact.
6. For hardware RMAs: get the serial number, warranty status, shipping address, and a swap-ahead option if the device is critical (switches, firewalls, Datto appliances). Label the box with the case number.
7. When resolved, test from our side, not just the vendor's "it's fixed". Confirm with the client. Record the root cause and what the vendor did.
8. If the vendor failed the client, note it for Casey. We keep a short vendor scorecard and use it at contract renewals.

## Gotchas
- ISPs often say "we see no problem" and close the case. Ask for a line test or a dispatch, and keep the case open. Have a screenshot of a failed ping to the ISP's gateway.
- Vendors ask you to reboot everything. Do it only if it is safe, and say you already did when you called.
- Do not give the vendor remote access to a server without Alex or Casey approving it, and without checking that the vendor is who they say.
- Distributors (the people we buy hardware from) can often escalate to a manufacturer faster than we can. Ask the rep.
- Case numbers are easy to lose in email. Put them in the ticket title for P1 and P2.
- Some line-of-business vendors only support during hours that differ from ours. Tax software vendors are overloaded around the filing deadlines (March and April). Open the case earlier than you think.

## Escalate when
- A P1 vendor case has no engineer assigned in 1 hour: Casey calls the vendor account rep.
- The vendor wants a change we have not authorized (a configuration change, a firmware update, a payment): stop, Alex.
- The vendor is blaming our setup and we are not sure: ask Alex to review before replying.
- A vendor breach or security notice affects a client: Casey and Alex, treat as a security incident, see `34-ransomware-response.md` if ransomware is involved.

## Documentation and time
- Ticket: vendor, case number, who you spoke to, times, outcome.
- Time: waiting on hold counts. Log it as the issue category, and write "vendor call" in the note.
- Update the client file vendor table if the rep or phone changed.

## Related
- `35-isp-outage-troubleshooting.md`
- `27-ticket-triage-and-priorities.md`
- `28-time-entry-standards.md`
- `31-cpa-tax-season-software-prep.md`

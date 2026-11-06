# After-Hours Emergency Call

owner: Alex Rivera
last_reviewed: 2026-08-03
applies_to: Omni+ Proactive, Omni+ Managed (P1 only); Omni+ Basic and T&M by request
tags: on-call, after-hours, emergency, p1, escalation

## Purpose
Say who picks up the emergency line, what counts as an emergency, and what to do in the first 15 minutes so a P1 after hours is handled the same way every time.

## When to use
Any call, text, or N-central alert outside Monday to Friday 8:00-5:00 Eastern, on weekends, or on company holidays.

## Before you start
- On-call rotation: Alex is primary, Sam is secondary, Casey is escalation. The schedule lives in the shared calendar named "OmniTechPro On-Call".
- The emergency line is 410-555-0100. It forwards to the primary's phone. If it rings out after 5 rings it forwards to the secondary.
- Have the laptop, the vault, and Accelo open before you answer if you can.
- Know the client's core plan. Only Omni+ Proactive and Omni+ Managed include after-hours P1. Others are billed at the after-hours rate and only if the client agrees on the call.

## Steps
1. Answer with "OmniTechPro emergency line, this is [name]." Get the caller's name, company, and callback number.
   Check: you wrote them down before anything else.
2. Ask: "What can you not do, and who else is affected?" Decide if it is a P1 using `27-ticket-triage-and-priorities.md`. Business down, security incident, data loss risk, or all staff cannot work counts.
   Check: you can say in one sentence what is broken.
3. If it is not a P1 (one user, a printer, a how-to), open a P3 ticket, tell the caller it will be handled next business day, and end the call politely.
   Check: the ticket exists and has the caller's name.
4. Look up the client in Accelo and confirm their plan. If the plan is T&M or Omni+ Basic, say that after-hours work is billed at the after-hours rate and get a yes before starting.
   Check: the yes is written in the ticket.
5. Open the Accelo ticket as P1. Category depends on the cause. Put the time of the call in the first note.
6. Check N-central for alerts on that client in the last 2 hours.
   Check: you know if monitoring saw it too.
7. Start remote work. If you cannot connect, ask the caller to check power, the internet modem lights, and whether the firewall is on.
   Check: you have a first diagnosis within 15 minutes (Omni+ Managed) or 30 minutes (Omni+ Proactive).
8. If it looks like a security incident, switch to `34-ransomware-response.md` or `11-suspected-compromised-account.md`. Tell Casey right away.
9. If you need hands onsite, call Sam. If Sam is unavailable, call Casey.
10. Every 30 minutes, send a short update to the client contact. "Still working, here is what we know."
11. When service is back, confirm with the caller that work can resume. Check at least one real task (open the tax database, open a patient chart, print).
12. Write a summary in the ticket: cause, fix, what is still open, and time spent.

## Gotchas
- Callers sometimes say "emergency" when they mean "annoyed". Ask the question in step 2 before you start billing.
- If the ISP is down, you will not reach the site. Check the ISP outage page and call the ISP from your end if you are on the account contact list. See `35-isp-outage-troubleshooting.md`.
- Some clients give out the emergency number to staff who then call at 11 PM about passwords. Remind the client contact it is for outages and security only.
- Do not make big changes alone at 2 AM when a fix can wait until morning. Stabilize first.
- A text message from N-central is not an emergency call. Check it, but do not call the client until you know what it is.

## Escalate when
- You cannot reach the client contact after two tries and the issue is a P1: call the after-hours contact listed in the client file.
- You are not making progress after 45 minutes: call Alex (if you are Sam) or Casey.
- The issue involves a breach, law enforcement, or regulator: Casey immediately.
- A vendor outage (ISP, Microsoft, LOB vendor) is the cause: use `30-vendor-escalation.md`.

## Documentation and time
- Time entries: after-hours work on Omni+ Proactive and Omni+ Managed P1s is logged as "After-hours P1" so reports can count it. Use the actual minutes, rounding up to the nearest 15.
- For Omni+ Basic and T&M, log it as billable "After-hours" with the approval noted.
- If you changed anything on the client's network, add a change log line in the client file the next business day.

## Related
- `27-ticket-triage-and-priorities.md`
- `30-vendor-escalation.md`
- `34-ransomware-response.md`
- `35-isp-outage-troubleshooting.md`

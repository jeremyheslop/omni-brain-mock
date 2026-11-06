# New Client Onboarding

owner: Casey Morgan
last_reviewed: 2026-09-08
applies_to: all-plans
tags: onboarding, new-client, accelo, n-central, documentation

## Purpose
Bring a new client from signed agreement to a fully monitored, documented, supported environment. This is the generic version. CPA firms use the longer plan in `process-plans/new-client-onboarding-cpa.md`.

## When to use
Whenever a signed agreement is received. T&M clients get a shorter version (skip monitoring steps unless purchased).

## Before you start
- Signed agreement and the plan decision from Casey.
- Access: Accelo, N-central, the vault, and Microsoft 365 admin center.
- A calendar slot for a site walk with the client's office manager.
- Do not start between January 15 and April 18 if the client is a CPA firm unless Casey says so.

## Steps
1. In Accelo, create the client record and contract. Set the service plans, contacts (primary, billing, after-hours), and billing start date.
   Check: contract shows the right plans and renewal date.
2. Create an onboarding project (P-xxxx) from the standard template. Add tasks and due dates.
   Check: project has an owner and every task has a due date.
3. Send the welcome email with the ticket address, emergency number 410-555-0100, and a short "how to ask for help" note.
   Check: the client replied or confirmed receipt.
4. Hold the kickoff call. Ask about busy seasons, key people, and what has gone wrong in the past. Ask who can authorize changes and spending.
   Check: you have written down the names of authorized contacts in Accelo.
5. Do the site walk. Photograph the network closet, label ports, count devices, and note ISP, router, firewall, switch, Wi-Fi, servers, printers, scanners, and phones.
   Check: you have a device list with serial numbers where possible.
6. Create the client page using the client file format: overview, service plans, contacts, sites, internet, network, servers and apps, M365 or Google notes, backup, printers, vendors, gotchas, vault references, change log.
   Check: the page has no passwords. Passwords are vault references only.
7. In N-central, create the customer and site. Deploy the agent to every workstation and server. Confirm each device appears with the right name.
   Check: device count in N-central matches the inventory (within 2).
8. Deploy EDR (SentinelOne) and DNS filtering (DNSFilter) as the core plan requires.
   Check: EDR console shows all devices healthy.
9. Set up backup per plan and add-on (Omni+ Backup, Server Backup): Cove for Omni+ Basic, Datto SIRIS plus M365 backup for Omni+ Proactive and Omni+ Managed. Run the first backup.
   Check: first full backup complete, and a file restore tested.
10. Review Microsoft 365: license assignments, admin roles, MFA, mail flow, forwarding rules, shared mailboxes. Enable MFA for all users.
    Check: MFA report shows every user registered.
11. Set the patch policy and reboot window in N-central. Agree the window with the client.
    Check: policy name and window are written in the client page.
12. Add the client to the daily backup check list and the monthly maintenance plan.
    Check: both show the new client.
13. 30-day review with the client contact. Close the project.

## Gotchas
- Clients often forget about the second office, the home office of a partner, or the old server in the closet. Ask three times.
- The ISP account is often in the name of a former employee. Get it changed to a current contact early, you will need it at 2 AM.
- A "managed" client with an unsupported Windows or a switch that cannot be updated needs a written plan, not a quiet assumption.
- Some clients have personal Microsoft accounts logged in on work PCs. Find them in step 10.
- Do not rotate every password on day one if staff rely on shared logins. Plan it with the client.

## Escalate when
- The client has no working backup at all: Alex and Casey, same day.
- Evidence of a prior breach (strange forwarding rules, unknown admins): treat it as `11-suspected-compromised-account.md`.
- The client wants to change plans mid-onboarding: Casey.

## Documentation and time
- Time entries go against the onboarding project tasks, not against the client's general bucket.
- Before closing the project, a second tech reviews the client page.

## Related
- `process-plans/new-client-onboarding-cpa.md`
- `02-new-user-onboarding.md`
- `08-daily-backup-check.md`
- `31-cpa-tax-season-software-prep.md`
- `33-onsite-visit-checklist.md`

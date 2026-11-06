# Microsoft 365 License Changes

owner: Jordan Blake
last_reviewed: 2026-04-17
applies_to: all-plans
tags: m365, licensing, billing, csp, users

## Purpose
Add, remove, or change Microsoft 365 licenses for a client's users and keep our billing and the client's bill in agreement.

## When to use
New hire needing a license, a role change (e.g. Business Basic to Business Premium), an offboarded user, a shared mailbox that needs a license, or a client asking for more seats. Licenses are billed through our Microsoft CSP account, so every change touches billing.

## Before you start
- Written request from an authorized contact (client file). Email is fine for adds. For removals, check that the user is really gone, see `03-employee-offboarding.md`.
- Microsoft 365 admin center > Billing > Licenses open for the client's tenant. Partner Center for the CSP side.
- Know the license type. Standard on our managed clients is Business Premium. Some older tenants have Business Standard or Basic, and a few have E3.
- Open an Accelo ticket, category Billing question or New User, priority P4.

## Steps
1. Check what is in the tenant: Billing > Licenses. Note total, assigned, and available for each SKU.
   Check: you can say how many seats are free.
2. If a seat is free, assign it: Users > Active users > (user) > Licenses and apps > tick the license > Save. Leave default apps on.
   Check: license shows under the user and the mailbox appears in about 15 minutes.
3. If no seat is free, ask Casey to add a seat in Partner Center. Do not buy licenses yourself. Wait for confirmation before you assign.
   Check: Billing > Licenses shows total increased.
4. For downgrades or role changes, check what the user loses. Going from Business Premium to Basic drops desktop apps, Defender, and Intune. Confirm the client understands and the device is not enrolled in something that needs the old license.
   Check: ticket shows the client's OK in writing.
5. For removals, convert to a shared mailbox first if mail must be kept (see `15-shared-mailbox-setup.md`). Then remove the license. Do not delete a user before checking OneDrive retention.
   Check: mailbox is shared type before the license goes.
6. Check the backup side. Datto SaaS Protection needs the seat added or removed too (Omni+ Proactive and Omni+ Managed). Cove Omni+ Basic clients are billed per device so no change.
   Check: the Datto SaaS dashboard shows the user protected.
7. Check the security side. SentinelOne and DNSFilter seats on managed plans follow device count, not user count, but verify the new device is covered.
8. Tell Casey the final count so the monthly invoice matches. Casey adjusts in Accelo (contract line items).
   Check: the Accelo contract shows the new seat count.
9. Update the user list and license count in the client file. Close the ticket.

## Gotchas
- Monthly CSP terms vs annual terms: an annual commitment cannot be reduced mid-term. Check the subscription term in Partner Center before you promise a refund or credit.
- Removing a license from a mailbox over 50 GB (or with an archive or litigation hold) can delete it after 30 days. Convert or keep a license.
- Shared mailboxes do not need a license unless they pass 50 GB or need an archive. Many clients still ask for one.
- A trial license left from a past project sometimes sits in the tenant. Leave it alone unless Casey says remove it.
- As of 2026, the Billing > Your products page was rearranged. If you cannot find Licenses, use Billing > Licenses from the left menu.
- Never assign a license to a service account that Alex created without checking with Alex. Some are intentionally unlicensed.
- Do not assign Business Premium to a user in a tenant that has unused E3 seats. Use what the client already pays for.

## Escalate when
- The client wants a different plan or wants to move to E3 or E5: Casey, quote needed.
- The seat count in Partner Center and in the tenant disagree: Casey.
- Pricing questions or credits: Casey.
- Licenses are missing and a user is blocked (P2 for an owner): Alex or Casey to approve a quick seat add.

## Documentation and time
- Ticket should show who requested it, what changed, and the new seat count.
- Time: 10 to 15 minutes for a simple add. Log under the ticket.
- Update the client file license section and the Accelo contract line items.

## Related
- `02-new-user-onboarding.md`
- `03-employee-offboarding.md`
- `15-shared-mailbox-setup.md`
- `08-daily-backup-check.md`

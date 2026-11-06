# New User Onboarding

owner: Jordan Blake
last_reviewed: 2026-06-10
applies_to: all-plans
tags: new-user, onboarding, m365, accounts, help-desk

## Purpose
Create a new employee's accounts and get their equipment ready so they can work on day one.

## When to use
When an authorized client contact asks for a new user. For the hardware side see `process-plans/new-hire-workstation.md`.

## Before you start
- Authorization from a contact listed in the client file. If the sender is not listed, call the primary contact before doing anything.
- Start date, full name, job title, manager, and a "copy permissions from" user.
- Check license availability in Microsoft 365 admin center under Billing > Licenses.
- Ask whether the role needs line-of-business apps (tax software, Dentrix, Clio, Procore, AutoCAD).

## Steps
1. Open an Accelo ticket (category: New User). Paste the request and the approval.
   Check: the ticket names the approver and the start date.
2. In Microsoft 365 admin center > Users > Active users > Add a user. Use the client's naming rule (first.last, flast, or other: check the client file). Assign the license that matches the role.
   Check: the user shows "Licensed" and a mailbox appears within about 15 minutes.
3. Set a one-time password and force change at first sign-in. Store it in the vault temporarily. Do not put it in the ticket.
   Check: the vault entry exists with the correct client path.
4. Add the user to security groups, distribution lists, and shared mailboxes by copying a peer. Do not copy admin roles.
   Check: group list matches the peer minus admin roles.
5. Create accounts in line-of-business apps. For CPA firms: tax software and portals. For dental: Dentrix user and chart permissions. For legal: Clio and document management.
   Check: login tested with the user's role.
6. If a workstation is needed, create the sub-task for Sam or follow `04-new-workstation-setup.md`.
7. Send MFA setup instructions. On day one, sit with the user (or on the phone) and register the authenticator app and a backup method. See `12-mfa-reset.md` if something goes wrong.
   Check: the user can sign in from a private window with MFA.
8. Set up printers, scanners, and shared drives. Test print and test scan.
9. Add the user to the client's user list in the client file. Add their device to the asset list.
10. Day +1 check-in with the user. Close the ticket after the manager confirms.

## Gotchas
- Names matter in email. Confirm spelling and the preferred name before you create the account. Changing it later breaks calendar shares.
- A new hire at a CPA firm during tax season cannot wait for the freeze. Do the user and mailbox, but do not touch the tax server in production without Alex.
- Title and real estate clients: new users must get the wire-fraud briefing from the client before they have access to wire instructions.
- Some clients use a shared mailbox for scanning. Add the new user as a member with "send as" only if the manager asks.
- Healthcare: no access to the EMR until the client says HIPAA training is done.

## Escalate when
- The request includes admin rights: Alex and the client owner must both approve.
- The licence count is short: Casey.
- The person's name matches a former employee with a retained mailbox: ask before reusing the address.

## Documentation and time
- Time entries: account work under the ticket. Hardware under the workstation sub-task.
- Update the client file user list and licence count.

## Related
- `04-new-workstation-setup.md`
- `14-m365-license-changes.md`
- `12-mfa-reset.md`
- `process-plans/new-hire-workstation.md`

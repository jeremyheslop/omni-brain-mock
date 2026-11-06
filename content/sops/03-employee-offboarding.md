# Employee Offboarding

owner: Jordan Blake
last_reviewed: 2026-07-22
applies_to: all-plans
tags: offboarding, security, accounts, m365, data-retention

## Purpose
Remove a departing employee's access safely, keep the business data that must be kept, and recover equipment. The full checklist is `process-plans/employee-offboarding.md`. This SOP is the short version for the person doing the work.

## When to use
When an authorized contact reports that someone is leaving, or has left.

## Before you start
- Confirm the requester is an authorized contact for the client.
- Get answers in writing: who gets the mailbox, who gets the files, forwarding needed or not, retention time.
- Know the cutoff time. For a firing or hostile exit, do the cutoff first and ask questions after.

## Steps
1. Open an Accelo ticket (category: Offboarding). Record the cutoff date and time.
   Check: ticket contains the written data-handling choices.
2. At the cutoff time, reset the user's password and sign out all sessions (Entra ID > Users > Revoke sessions).
   Check: user shows as signed out and password reset in the audit log.
3. Block sign-in (Microsoft 365 admin center > Users > Block sign-in).
   Check: status shows "Sign-in blocked".
4. Remove MFA methods, remove VPN access, and disable line-of-business app logins.
   Check: you tested that the user cannot sign in to each.
5. Handle the mailbox as approved:
   - Convert to shared mailbox (no licence needed under 50 GB) and give the manager access, or
   - Set forwarding for the approved time, or
   - Keep the licence for 30 days if a conversion is not possible.
   Check: manager can open the mailbox.
6. Move or share the user's OneDrive with the manager.
   Check: manager sees the files.
7. Collect equipment. Mark it unassigned in the asset list. For laptops: back up anything needed, then wipe (Windows Reset or reimage) before reissue.
8. Change shared passwords the person knew (shared logins, copier admin, Wi-Fi). Store the new ones in the vault.
   Check: vault entries updated with today's date in the notes.
9. After 30 days, remove the licence and, if approved in writing, delete the account.
10. Update the client file and Accelo, close the ticket.

## Gotchas
- Do not delete the account on the last day. Deleted mailboxes are hard to get back after 30 days.
- Devices with Outlook still signed in will keep trying. Revoke sessions, do not rely on password reset alone.
- Auto-forwarding to the former employee's personal address is a liability. Do not do it unless the client owner asks in writing.
- A person who also owned a domain, social account, or vendor portal login in their own name is a recurring problem. Ask.
- Some clients give departing staff a week of "read only". Plan it as a separate step, not a loose end.

## Escalate when
- The departing person had admin rights or access to payments: Alex and Casey.
- The client wants emails preserved for legal reasons: Casey (legal hold needs a licence and a decision).
- Any sign that data was copied out in the last week: treat as `11-suspected-compromised-account.md`.

## Documentation and time
- Log time on the ticket. Write what was kept, what was deleted, and who approved.
- Update the licence count on the Accelo contract for billing.

## Related
- `process-plans/employee-offboarding.md`
- `14-m365-license-changes.md`
- `15-shared-mailbox-setup.md`
- `13-password-reset-policy.md`

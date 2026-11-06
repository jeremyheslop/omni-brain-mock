# Password Reset Policy

owner: Casey Morgan
last_reviewed: 2025-04-09
applies_to: all-plans
tags: password, policy, reset, identity, help-desk, security

## Purpose
Say who we reset passwords for, how we verify them, and how we hand the new password over, so a reset never turns into a break-in.

## When to use
Any request to reset a password for Microsoft 365, Active Directory, a line-of-business app we manage, or a VPN account. This is a policy page. For the account compromise case use `11-suspected-compromised-account.md`.

## Before you start
- Open an Accelo ticket, category Help Desk, priority P3. For a locked-out owner, P2.
- The client file with the list of authorized contacts and any special rules (some clients require manager approval for every reset).
- Admin access to Microsoft 365 admin center or the client's AD (via N-central remote or the client's DC).

## Steps
1. Find out who is asking and for which account. Compare against the user list in the client file.
   Check: requester and target account are both known.
2. Verify the requester.
   - If the requester is the account owner: call them back at the number in the client file. If they are on the phone with you already, ask a verification question.
   - If the requester is someone else: get approval from the account owner's manager or a listed contact by phone.
   Check: ticket says how verification was done.
3. Self-service first. If the client has Self-Service Password Reset (SSPR) turned on, send the user to aka.ms/sspr. Only do the reset yourself if SSPR is not set up or does not work.
   Check: user either resets it themselves or you move on to step 4.
4. In Microsoft 365 admin center > Users > Active users > (user) > Reset password. Choose "Automatically create a password" and "Require this user to change their password when they first sign in". For AD, use `Set-ADAccountPassword` and `Set-ADUser -ChangePasswordAtLogon $true`.
   Check: the user shows no error, and the sign-in log shows a change at next login.
5. Deliver the password by phone only. Read it slowly, spelled out if needed. Never send it in email or the ticket, and never over text.
   Check: user confirms they have it.
6. Stay on the phone until the user signs in and sets their new one. Remind them: at least 14 characters, a passphrase is best, not reused from other sites.
   Check: sign-in works and email opens.
7. If the user uses saved passwords in Outlook, Teams, or mapped drives on other devices, tell them to update those, otherwise the account will lock out again.
8. If the account was locked out (not forgotten), find the cause. In AD: `Get-ADUser <name> -Properties LockedOut`, then check the Event ID 4740 on the DC for the source device.
   Check: you know which device keeps sending the old password.
9. Close the ticket with the verification method.

## Policy rules
- Minimum length 14 characters. No forced rotation unless the client's insurer or auditor requires it (credit unions and some healthcare clients do; see client file).
- Temporary passwords are random, one-time use, and expire at first login.
- MFA must be on for every cloud account. A reset does not remove MFA. If MFA is the problem, go to `12-mfa-reset.md`.
- Shared passwords go in the vault, never in a spreadsheet. Vault path format: `Vault: <client-slug>/<item>`.
- We do not reset passwords for ex-employees on request. See `03-employee-offboarding.md`.
- Service accounts are changed only by Alex, with a ticket and a change window.

## Gotchas
- A user who "forgot their password" three times in a week may be getting phished. Ask what they have clicked.
- Resetting an AD password does not always sync to Microsoft 365 right away if Entra Connect is on a 30 minute cycle. Tell the user to wait or force a sync (`Start-ADSyncSyncCycle -PolicyType Delta`).
- Don't reset passwords from a text message claiming to be the owner. Ever.
- Resets for client owners and partners get extra care. They are the highest-value targets.
- Old note: some clients still have 90-day expiry set in AD from before 2023. If a client complains about it, tell Alex and check what the insurer asks for before changing it.

## Escalate when
- You cannot verify identity: stop and tell Alex.
- Request is for an admin or service account: Alex.
- The client wants an exception to this policy: Casey decides, and writes it in the client file.
- You suspect the request is social engineering: Alex, then Casey.

## Documentation and time
- Record who asked, who was verified, how, and when. No passwords in notes.
- Time: 10 to 20 minutes. Log under the ticket.
- Update the client file if the client gave a new authorized contact.

## Related
- `12-mfa-reset.md`
- `11-suspected-compromised-account.md`
- `03-employee-offboarding.md`
- `02-new-user-onboarding.md`

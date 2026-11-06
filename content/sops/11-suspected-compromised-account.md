# Suspected Compromised Account

owner: Alex Rivera
last_reviewed: 2026-05-30
applies_to: all-plans
tags: security, compromise, incident, m365, entra, mailbox-rules

## Purpose
Contain a Microsoft 365 account that may be in someone else's hands, find out what they did, and give the user back a clean account.

## When to use
User reports odd sign-in prompts, sent mail they did not write, or a phish where they typed a password. Entra flags a risky sign-in. Clients get "you sent me something strange" replies. A forwarding rule appears. This is P1 if money movement, an admin account, or sensitive data is involved, otherwise P2.

## Before you start
- Open an Accelo ticket, category Security Incident. Tell Alex and Casey. Alex owns it.
- Global admin or Security Administrator access to the tenant. Break-glass: `Vault: <client-slug>/m365-global-admin-breakglass`.
- Do not email the user's own address to tell them what is going on. Call them.
- Write down timestamps as you go. They matter later.

## Steps
1. Call the user on a phone. Confirm they are who they say they are and ask what happened. Do not reset anything until you have notes.
   Check: ticket has the user's account of events with a time.
2. Block sign-in right now: Microsoft 365 admin center > Users > Active users > (user) > Block this user, or Entra admin center > Users > Properties > Account enabled = No.
   Check: the user's status shows "Sign-in blocked".
3. Revoke sessions: Entra > Users > (user) > Revoke sessions. Or in PowerShell: `Revoke-MgUserSignInSession -UserId user@clientdomain.example`.
   Check: the command returns True.
4. Reset the password (see `13-password-reset-policy.md`) and remove all registered MFA methods under Authentication methods. The attacker may have added their own.
   Check: the user shows no unknown authenticator apps or phone numbers.
5. Review sign-in logs for the past 30 days (Entra > Users > Sign-in logs). Note unfamiliar IPs, countries, and apps.
   Check: you can name the first suspicious sign-in time.
6. Check inbox rules and forwarding. Exchange admin center > Recipients > Mailboxes > (user) > Mail flow settings, plus in PowerShell: `Get-InboxRule -Mailbox user@clientdomain.example | fl Name,Enabled,ForwardTo,RedirectTo,DeleteMessage`. Delete rules that forward, redirect, or move mail to RSS or Archive.
   Check: no suspicious rules left, and `Get-Mailbox | fl ForwardingSmtpAddress` is blank.
7. Check OAuth apps: Entra > Enterprise applications > filter by user consent. Remove unknown consents.
   Check: only known apps remain.
8. Search the Unified Audit Log in Purview for what the attacker did (mail sent, files shared, MailItemsAccessed). Export to the ticket.
   Check: you can say whether they only logged in or sent mail or downloaded files.
9. Pull back what was sent. Use Defender Explorer to find the phishing mail the account sent and remove it from other mailboxes. Tell affected recipients, via the client contact.
10. Re-enable the account, have the user sign in with a new password, and re-register MFA with you on the phone.
    Check: sign-in logs show the user's normal device and location.
11. Scan the user's PC with SentinelOne. Reimage if S1 finds anything.
12. Watch the account for 7 days. Set a reminder in the Accelo ticket for day 2 and day 7.

## Gotchas
- Resetting the password without revoking sessions leaves the attacker logged in. Do both.
- Attackers love inbox rules that hide replies from banks and customers. Check for rules with odd names like "." or a blank name.
- Legacy auth (IMAP/POP) can bypass MFA. If the tenant allows it, turn it off after the incident. We now block legacy auth at onboarding, but older tenants were missed.
- An attacker in a CPA partner's mailbox may have seen client tax documents. This can be a reportable event. Casey decides who is told. Do not speculate in writing to the client.
- Do not delete the mailbox or the logs. Audit logs are kept 180 days on Business Premium. Export early.
- If the user's account is also a vault, VPN, or tax portal login, change those too.

## Escalate when
- Admin account involved: Alex and Casey now, assume tenant-wide risk.
- Money was sent or wire info was changed: Casey calls the client and their bank contact.
- Data of regulated type (health, financial customer records) was accessed: Casey, for the legal and notification decision.
- More than one account shows the same attacker IP: treat as a tenant compromise.
- Anything that looks like ransomware: `34-ransomware-response.md`.

## Documentation and time
- Keep a running timeline in the ticket with exact times. Attach exports from Entra and Purview.
- Time: expect 2 to 4 hours for a simple case, more if mail was sent from the account.
- After closing, write a short summary for the client and add a note to the client file.
- If the cause was a weak or reused password or missing MFA, add a recommendation to the next quarterly review.

## Related
- `10-phishing-email-response.md`
- `12-mfa-reset.md`
- `13-password-reset-policy.md`
- `34-ransomware-response.md`

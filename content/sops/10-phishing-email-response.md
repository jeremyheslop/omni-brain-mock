# Phishing Email Response

owner: Jordan Blake
last_reviewed: 2026-09-22
applies_to: all-plans
tags: security, phishing, email, m365, defender, incident

## Purpose
Handle a reported phishing or suspicious email: find out who got it, whether anyone clicked, remove it, and close the hole.

## When to use
A user forwards or reports a suspicious email, or a user says they clicked a link or opened an attachment. Also when Defender or Proofpoint flags a campaign. If a user entered a password or approved an MFA prompt, switch to `11-suspected-compromised-account.md` right away. If money movement is involved, treat as P1.

## Before you start
- Microsoft 365 admin access for the client (Defender portal at security.microsoft.com, Exchange admin center). Break-glass is `Vault: <client-slug>/m365-global-admin-breakglass`, use it only if normal admin access is gone.
- Ask the user to not delete the email. We need the original.
- Open an Accelo ticket, category Security Incident. Priority P2 by default, P1 if someone clicked and entered credentials or if wire/payment instructions are involved.
- Tell Alex.

## Steps
1. Ask the reporter three questions: Did you click anything? Did you open an attachment? Did you type a password or approve a prompt? Record the answers in the ticket.
   Check: the ticket has all three answers in the user's words.
2. Get the message. Have the user use "Report message" in Outlook, or forward as attachment to the helpdesk address. Save the .eml in the ticket.
   Check: you can see full headers (sender, return-path, SPF/DKIM results).
3. Find everyone else who got it. In Defender portal > Email & collaboration > Explorer (or Threat Explorer) search by sender, subject, or URL for the last 7 days.
   Check: you have a count of recipients and whether anyone clicked.
4. Remove it. In Explorer select the messages > Take action > Move to junk, or Soft delete. Use Hard delete only if Alex agrees.
   Check: a second search shows the message is gone from mailboxes.
5. Block the sender and URL. Add the domain to Tenant Allow/Block List > Block. If the client has Proofpoint Essentials (Omni+ Managed), add the sender there as well.
   Check: the entry appears in the block list.
6. If someone clicked: check their sign-in logs in Entra admin center > Users > (user) > Sign-in logs for the last 24 hours. Look for new locations or apps.
   Check: no sign-ins from unexpected countries or unknown devices. If there are, go to `11-suspected-compromised-account.md`.
7. If someone opened an attachment: check the device in N-central and SentinelOne for detections. Ask Alex to run a full scan or isolate the device if it flags anything.
   Check: S1 shows no threats, or the device is isolated.
8. Send a short message to the reporter and, if several people got it, to the client contact. Plain language: what it was, what we did, what to look for next time.
9. Offer the user a reminder of how to spot it. Do not scold. People who report quickly are the good ones.
10. Close the ticket after 24 hours of no further activity.

## Gotchas
- Invoice and "shared document" phish from a real compromised vendor look very real. The sender domain can be legit. Check the reply-to and the link, not just the From name.
- Reporting from a phone often strips headers. Ask the user to forward as attachment from a PC.
- CPA clients get fake IRS and client-document phish all year, spiking in February and March. Expect volume.
- Title and real estate clients: any email asking to change wire instructions is wire fraud until proven otherwise. Call the sender on a known number.
- Do not click the link yourself on your daily machine to "see what it does". Use the sandbox in Defender (URL detonation) or the lab VM.
- Users often send the same phish to Jordan, Alex, and Casey at once. Pick one owner in the ticket so work is not duplicated.
- A quarantine release by the user can put the message right back. Check Quarantine in Defender.

## Escalate when
- A user entered credentials, approved MFA, or ran an attachment: Alex, and switch to `11-suspected-compromised-account.md`.
- Wire, payment, or payroll change was requested or sent: P1, Casey calls the client now.
- More than 5 mailboxes got it with a click-through: Alex.
- Regulated client (healthcare, credit union): Casey decides on any notification. Do not write "breach" in client emails yourself.

## Documentation and time
- Ticket: category Security Incident, with the .eml, the list of recipients, and what was removed.
- Time: 30 to 60 minutes for a simple report, more if clicked. Log under the ticket.
- If a pattern repeats (same user, third time), note it in the client file and mention it at the quarterly review.

## Related
- `11-suspected-compromised-account.md`
- `12-mfa-reset.md`
- `13-password-reset-policy.md`
- `34-ransomware-response.md`

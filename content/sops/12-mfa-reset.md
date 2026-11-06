# MFA Reset

owner: Jordan Blake
last_reviewed: 2026-10-11
applies_to: all-plans
tags: mfa, authentication, m365, entra, help-desk, identity

## Purpose
Reset or re-register a user's multi-factor authentication when they lose access to their authenticator, without handing an attacker a way in.

## When to use
A user says "I got a new phone", "my authenticator stopped working", or "it keeps asking for a code I don't have". Not for a planned phone swap where the user still has the old phone: see `32-new-phone-mfa-device-swap.md`. If the request looks odd, treat it as a possible takeover and read `11-suspected-compromised-account.md`.

## Before you start
- Verify identity. This is the whole point. Do not reset MFA based on an email alone.
- Know the client's approved contacts list in the client file. If the request comes from someone other than the user, the user's manager or a listed contact must approve.
- Admin access: Entra admin center (User Administrator or Authentication Administrator role).
- Open an Accelo ticket, category Help Desk, priority P3. Priority goes to P2 if the user is an owner or partner and cannot work.

## Steps
1. Verify the user. Call them back on the phone number in the client file, not the number in the email. Ask a question only they would know (manager name, last project, or a code word if the client set one up).
   Check: you spoke to the person, and you note "verified by callback" in the ticket.
2. If the request came by email or chat and the person is not known to you, also get approval from the client's primary contact by phone.
   Check: approval is written in the ticket with a name and time.
3. In Entra admin center, go to Users > (user) > Authentication methods. Look at what is registered and the last used date.
   Check: you can see the old device or method listed.
4. Click "Require re-register multifactor authentication", then delete the lost method (Microsoft Authenticator, phone, or others). Also click "Revoke multifactor authentication sessions".
   Check: the user's methods list is empty or only shows methods the user confirms.
5. Issue a Temporary Access Pass: Authentication methods > Add authentication method > Temporary Access Pass. Set one-time use, 60 minutes.
   Check: the TAP is shown once on screen. Do not paste it into the ticket or an email.
6. Read the TAP to the user over the phone. Have them go to mysignins.microsoft.com/security-info in a private window and sign in with the TAP.
   Check: they land on the Security info page.
7. Have the user add Microsoft Authenticator and a backup method (a phone number for text or call). Walk them through the number-matching prompt.
   Check: they approve a test prompt on the new device.
8. Have them sign out and back in to Outlook and Teams on their PC and phone.
   Check: no more MFA loops and email loads.
9. Tell them to remove the old phone entry in Authenticator if the phone still exists.
10. Close the ticket with a note of who verified, how, and the date.

## Gotchas
- MFA reset is the most common attacker social-engineering request. Never skip the callback, even for an owner you know. An email saying "I'm in a rush, just reset it" is a warning sign, not a reason to hurry.
- The Authenticator app has a cloud backup on iPhone (iCloud) and Android (Microsoft account). Some users can restore it themselves. Ask first.
- If the tenant uses per-user MFA instead of Conditional Access, the options in Entra look different. Older tenants were set up this way. Check Security > Conditional Access first.
- A TAP is not allowed in some tenants until the method is enabled under Authentication methods > Policies > Temporary Access Pass.
- If the user is traveling, Conditional Access may block sign-in from another country even with a valid TAP. Look at the sign-in log failure reason.
- Admin accounts: do not use a TAP for a global admin without Alex.

## Escalate when
- You cannot verify the person: stop. Tell Alex. Do not "try later".
- The user says they did not request the reset, or they see prompts they did not trigger: `11-suspected-compromised-account.md`, P1 handling.
- The account is a global admin or the client owner's break-glass account: Alex.
- TAP is disabled and the tenant policy needs to change: Alex.

## Documentation and time
- Ticket must show: who asked, how identity was verified, who approved if needed, what was removed and added.
- Time: 15 to 30 minutes. Log under the ticket.
- If the client has a recurring problem (many resets), note it for the quarterly review and suggest a number-matching rollout or password-less sign-in.

## Related
- `32-new-phone-mfa-device-swap.md`
- `13-password-reset-policy.md`
- `11-suspected-compromised-account.md`
- `02-new-user-onboarding.md`

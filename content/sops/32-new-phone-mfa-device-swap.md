# New Phone: MFA Device Swap

owner: Jordan Blake
last_reviewed: 2026-08-03
applies_to: all-plans
tags: mfa, authenticator, phone, entra, m365, help-desk, identity

## Purpose
Move a user's multi-factor sign-in from an old phone to a new one without locking them out, and without letting a social engineer take over an account.

## When to use
A user is getting a new phone, has lost or reset the old one, or wants to switch authenticator apps. If the old phone is still working this is a quick move. If it is lost or wiped, it is an MFA reset, see `12-mfa-reset.md`.

## Before you start
- Confirm who is calling. Call back on a number from the client file (not the one in the email). For a change request that came by email, phone the user.
- Ask: is the old phone still in their hand and signed in to the authenticator app? That decides the path below.
- Know the client's MFA method. Most are Microsoft Authenticator through Entra ID. A few use Duo or FortiToken for VPN. Check the client file.
- Have the admin center ready: Entra admin center > Users > select user > Authentication methods.

## Steps
1. Open an Accelo ticket (category: Help Desk, priority P3). If the user is locked out and cannot work, make it P2.
   Check: the ticket records how you verified the caller.
2. Path A, old phone still works. Tell the user to install Microsoft Authenticator on the new phone first, but not sign out of the old one. On the new phone: add account > Work or school > sign in. The old phone approves the new sign-in.
   Check: the new phone shows the account with a 6-digit code ticking.
3. Have the user turn on phone sign-in (Microsoft Authenticator cloud backup is also an option on iPhone and Android, but it is the user's personal account, not ours). Set the new device as default.
4. In Entra > Authentication methods, check that the new device appears and the old device is listed. Delete the old device only after the new one works for a real sign-in.
   Check: the user signs in from a private browser window with the new phone.
5. Path B, old phone gone or wiped. Verify the user using the client's approved method (manager confirmation by phone for a high-risk role). In Entra, go to the user's Authentication methods > Require re-register multifactor authentication. Or issue a Temporary Access Pass (Add authentication method > Temporary Access Pass, one-time, 1 hour).
   Check: the TAP is delivered by phone or in person, never by email or in the ticket.
6. Walk the user through registering the new phone with the TAP at https://aka.ms/mysecurityinfo. Add two methods: authenticator app and a backup (text to the new number, or a second device).
   Check: the security info page lists two methods.
7. Revoke old sessions: Entra > user > Revoke sessions. This signs the old phone out of everything.
8. Fix other apps that use their own tokens: password manager, client VPN token, bank or tax portals with their own MFA. Remind the user.
9. Tell the user to wipe or trade in the old phone only after everything works. Give it 24 hours.

## Gotchas
- The user trades in the old phone before the move. This is the number one cause of this ticket. Ask during onboarding and put a note in the user's welcome mail.
- Authenticator backup on iCloud or Google restores the app, but not always the work account. Test it.
- A new number with the same old text-message method only works if the number in Entra is updated.
- Do not read a Temporary Access Pass over the phone if the user is on speaker in an open office. Ask them to go somewhere private.
- Executives and anyone with finance or wire access: use the manager confirmation step every time. Fake "new phone" requests are a common attack.
- Conditional access with "compliant device" requirements may block the new phone's Authenticator sign-in until the device is enrolled in Intune. Alex can check the policy.

## Escalate when
- The user cannot be verified: stop and tell Casey or the client primary contact. Do not reset.
- Several users report new-phone requests on the same day: possible attack, tell Alex, see `11-suspected-compromised-account.md`.
- The user has Global Admin or another admin role: Alex does it.

## Documentation and time
- Ticket: caller verification method, path used (A or B), methods registered, old sessions revoked.
- Time: 0.25-0.5 hr for Path A, 0.5-0.75 hr for Path B.
- Do not paste codes or TAP values into any note.

## Related
- `12-mfa-reset.md`
- `11-suspected-compromised-account.md`
- `13-password-reset-policy.md`
- `02-new-user-onboarding.md`

# Process Plan: Employee Offboarding

owner: Jordan Blake
last_reviewed: 2026-07-22
tags: process-plan, offboarding, security, m365, accounts
plan_id: employee-offboarding
applies_to: all-plans (managed plans do the full plan; T&M does what the client asks and pays for)
duration: Day -2 to Day +30
related: sops/03-employee-offboarding.md, sops/14-m365-license-changes.md, sops/15-shared-mailbox-setup.md

How to use: open an Accelo ticket (category: Offboarding) the moment the client tells us someone is leaving. Make one task per checkbox. The client's authorized contact (see the client file) must approve the data handling choices in Phase 1. If the departure is hostile or sudden, jump to Phase 3 first and run it as P1.

Owner roles: Help Desk (Jordan Blake), Lead Tech (Alex Rivera), Field Tech (Sam Okafor), Owner (Casey Morgan), Client Contact.

## Phase 1: Planning (Day -2 to Day 0)

Owner role: Help Desk

- [ ] Ticket opened with last day, last hour, and requester name | Day -2 | Help Desk
- [ ] Confirm requester is an authorized contact for this client | Day -2 | Help Desk
- [ ] Ask: who gets the mailbox? who gets the files? should email be forwarded and for how long? | Day -2 | Help Desk
- [ ] Ask: is a company phone, laptop, or token to be returned? | Day -2 | Help Desk
- [ ] Ask: does the person use line-of-business apps with their own accounts (CCH, Dentrix, Clio, Procore)? | Day -1 | Help Desk
- [ ] Ask: is there a voicemail box or desk phone to reassign? | Day -1 | Help Desk
- [ ] Written approval from the client contact stored in the ticket | Day -1 | Help Desk

## Phase 2: Pre-departure (Day -1 to Day 0)

Owner role: Help Desk

- [ ] List groups, shared mailboxes, shared drives, and Teams the user belongs to | Day -1 | Help Desk
- [ ] List devices assigned (N-central device list) | Day -1 | Help Desk
- [ ] Check for personal files on the laptop that should be copied | Day -1 | Help Desk
- [ ] Check for mail rules or forwarding already in place | Day -1 | Help Desk
- [ ] Schedule the account change for the end of the last working day | Day 0 | Help Desk

## Phase 3: Cutoff (Day 0, at the agreed time)

Owner role: Help Desk, with Lead Tech on call

- [ ] Reset the password (do not tell the user) | Day 0 | Help Desk
- [ ] Sign out all sessions and revoke refresh tokens | Day 0 | Help Desk
- [ ] Block sign-in in Entra ID (or suspend in Google Workspace) | Day 0 | Help Desk
- [ ] Remove the user from MFA methods or delete authentication methods | Day 0 | Help Desk
- [ ] Remove VPN access | Day 0 | Help Desk
- [ ] Disable or reassign line-of-business app logins | Day 0 | Help Desk
- [ ] Convert mailbox to shared (if retained) or set up forwarding as approved | Day 0 | Help Desk
- [ ] Set an out-of-office reply if approved | Day 0 | Help Desk
- [ ] Remove from distribution lists and shared mailboxes (or keep as approved) | Day 0 | Help Desk
- [ ] Wipe or remove company data from the user's mobile device (if managed) | Day 0 | Help Desk
- [ ] Collect laptop, badge, keys, token, phone | Day 0 | Client Contact

## Phase 4: Data and equipment (Day +1 to Day +7)

Owner role: Field Tech and Help Desk

- [ ] Home folder, OneDrive, and mail archived to the agreed location | Day +2 | Help Desk
- [ ] Ownership of OneDrive files transferred to the manager | Day +2 | Help Desk
- [ ] Laptop collected and checked in; device marked "unassigned" in the asset list | Day +3 | Field Tech
- [ ] Laptop either wiped and put back in the spare pool, or sent to refresh | Day +5 | Field Tech
- [ ] Desk phone or softphone license reassigned | Day +3 | Help Desk
- [ ] Remove from N-central device ownership notes | Day +3 | Help Desk
- [ ] Remove saved Wi-Fi and cached credentials on devices that stay | Day +5 | Field Tech
- [ ] Printers or scanners with the user's name or scan-to-email address updated | Day +5 | Field Tech

## Phase 5: Licenses and cleanup (Day +7 to Day +30)

Owner role: Help Desk and Owner

- [ ] After the retention period (default 30 days), remove the Microsoft 365 license if the mailbox is not retained | Day +30 | Help Desk
- [ ] Confirm the shared mailbox does not need a license (under 50 GB, no archive) | Day +7 | Help Desk
- [ ] Delete the account only if the client approved in writing | Day +30 | Help Desk
- [ ] Update the license count on the client record for billing | Day +30 | Owner
- [ ] Change shared passwords that the user knew (copier admin, Wi-Fi, shared accounts) | Day +7 | Lead Tech
- [ ] Remove from third-party portals (tax portal, bank portals) with client contact | Day +7 | Client Contact
- [ ] Update the client file contacts and user list | Day +7 | Help Desk

## Phase 6: Close out (Day +30)

Owner role: Help Desk

- [ ] Time entries added to the ticket | Day +30 | Help Desk
- [ ] Final note in ticket: what was kept, what was deleted, who approved | Day +30 | Help Desk
- [ ] Ticket closed | Day +30 | Help Desk

## Notes

- If the person is a partner or owner of the business, or holds admin rights, involve Alex and Casey. Review all admin roles and shared passwords.
- If the person had access to client money or wire instructions (title, CPA, real estate), tell Casey. Consider a mailbox rules audit.
- Never delete a mailbox on the last day. Hold it for at least 30 days.

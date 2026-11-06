# Process Plan: New Hire Workstation

owner: Sam Okafor
last_reviewed: 2026-02-27
tags: process-plan, workstation, new-hire, onboarding, hardware
plan_id: new-hire-workstation
applies_to: all-plans
duration: Day -10 to Day +7
related: sops/02-new-user-onboarding.md, sops/04-new-workstation-setup.md, sops/05-laptop-refresh.md, sops/24-windows-10-to-11-upgrade.md

How to use: open an Accelo ticket (category: New User) when the client tells us about a hire. One task per checkbox. The best case is ten business days of notice. Most clients give three. Compress by keeping the order; skip nothing that touches security.

Owner roles: Help Desk (Jordan Blake), Field Tech (Sam Okafor), Lead Tech (Alex Rivera), Client Contact.

## Phase 1: Request intake (Day -10 to Day -7)

Owner role: Help Desk

- [ ] Request ticket opened with start date, name, job title, manager | Day -10 | Help Desk
- [ ] Approval from the authorized contact stored in the ticket | Day -10 | Help Desk
- [ ] Ask: laptop or desktop? new purchase or spare from stock? | Day -9 | Help Desk
- [ ] Ask: which apps (tax software, Dentrix, Clio, AutoCAD, QuickBooks)? | Day -9 | Help Desk
- [ ] Ask: which mailboxes, shared drives, groups, printers? | Day -9 | Help Desk
- [ ] Ask: a copy of which existing user's access (role template)? | Day -9 | Help Desk
- [ ] Ask: phone number, desk phone, softphone, or mobile device? | Day -9 | Help Desk
- [ ] License availability confirmed (M365, LOB app seats) | Day -8 | Help Desk

## Phase 2: Procurement (Day -8 to Day -5)

Owner role: Field Tech

- [ ] Stock checked: any imaged spare laptop that fits? | Day -8 | Field Tech
- [ ] If buying: quote approved by client contact | Day -8 | Help Desk
- [ ] Order placed; delivery date recorded | Day -7 | Field Tech
- [ ] Monitor, dock, keyboard, mouse, headset needs confirmed | Day -7 | Field Tech
- [ ] Asset tag printed | Day -6 | Field Tech

## Phase 3: Build and image (Day -5 to Day -2)

Owner role: Field Tech

- [ ] Device unboxed; BIOS or firmware updated; Windows updated | Day -5 | Field Tech
- [ ] Windows 11 Pro installed or confirmed; TPM and Secure Boot on | Day -5 | Field Tech
- [ ] Device renamed using the client prefix (e.g. TLC-WS-021) | Day -4 | Field Tech
- [ ] Device joined to the domain or Entra ID | Day -4 | Field Tech
- [ ] N-central agent installed; device appears in the right customer and site | Day -4 | Field Tech
- [ ] EDR (SentinelOne) installed; confirmed healthy in the console | Day -4 | Field Tech
- [ ] BitLocker enabled; recovery key escrowed to Entra ID or AD | Day -4 | Field Tech
- [ ] Standard apps installed: Office, Teams, Adobe Reader, Chrome or Edge, 7-Zip | Day -3 | Field Tech
- [ ] LOB apps installed and tested against a test login | Day -3 | Field Tech
- [ ] Printers and scanners mapped | Day -3 | Field Tech
- [ ] Local admin account removed or set to LAPS | Day -3 | Field Tech
- [ ] Power plan, sleep settings, and Windows Update policy set to client standard | Day -3 | Field Tech
- [ ] Final patch run; reboot; no pending updates | Day -2 | Field Tech
- [ ] Asset record added to the client file | Day -2 | Field Tech

## Phase 4: Accounts (Day -3 to Day -1)

Owner role: Help Desk

- [ ] M365 user created; license assigned | Day -3 | Help Desk
- [ ] Mailbox created; aliases set | Day -3 | Help Desk
- [ ] Group and shared mailbox memberships added | Day -3 | Help Desk
- [ ] MFA registration link prepared (not enrolled yet) | Day -2 | Help Desk
- [ ] LOB app account created | Day -2 | Help Desk
- [ ] VPN access added if requested and approved | Day -2 | Help Desk
- [ ] Temporary password stored in the vault; delivery method agreed with the manager | Day -1 | Help Desk
- [ ] Welcome sheet prepared with Wi-Fi guidance, help desk number, ticket email | Day -1 | Help Desk

## Phase 5: Delivery and first day (Day 0)

Owner role: Field Tech or Help Desk

- [ ] Equipment delivered to the desk and tested | Day 0 | Field Tech
- [ ] User signs in; password changed | Day 0 | Help Desk
- [ ] MFA enrolled on the user's phone with a second method added | Day 0 | Help Desk
- [ ] Outlook, Teams, OneDrive signed in and working | Day 0 | Help Desk
- [ ] Test print and test scan | Day 0 | Field Tech
- [ ] LOB app tested with real work | Day 0 | Help Desk
- [ ] Short walkthrough: how to open a ticket, who to call | Day 0 | Help Desk

## Phase 6: Follow-up (Day +1 to Day +7)

Owner role: Help Desk

- [ ] Day +1 check-in call or email | Day +1 | Help Desk
- [ ] Any missing access fixed | Day +2 | Help Desk
- [ ] Client contact confirms everything works | Day +5 | Help Desk
- [ ] Time entries added; ticket closed | Day +7 | Help Desk
- [ ] Client file user list and asset list updated | Day +7 | Help Desk

## Notes

- If the new hire is a partner, manager, or has access to money (wires, trust accounts, payroll), tell Alex and review permissions before day one.
- Do not skip BitLocker. We have had a stolen laptop with no encryption and it is a bad phone call.
- Clients on T&M: do the same build, but confirm in writing what they want us to install and that the time is billable.

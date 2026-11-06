# Process Plan: New Client Onboarding (CPA Firm)

owner: Casey Morgan
last_reviewed: 2026-09-08
tags: process-plan, onboarding, cpa, accounting, new-client
plan_id: new-client-onboarding-cpa
applies_to: Omni+ Proactive, Omni+ Managed, Omni+ Basic (CPA and tax firms)
duration: about 30 days
related: sops/01-new-client-onboarding.md, sops/31-cpa-tax-season-software-prep.md, sops/08-daily-backup-check.md

How to use: this plan is meant to be digitized. Each phase has a due offset from Day 0 (contract signed), an owner role, and checkbox tasks. Owner roles: Owner (Casey Morgan), Lead Tech (Alex Rivera), Field Tech (Sam Okafor), Help Desk (Jordan Blake). Create the Accelo project (P-xxxx) with one task per checkbox. Do not start a CPA onboarding between January 15 and April 18 unless the client is in trouble. If you must, skip all changes to production systems until after April 18.

## Phase 1: Paperwork and kickoff (Day 0 to Day +2)

Owner role: Owner

- [ ] Signed agreement received and contract created in Accelo (service plans set) | Day 0 | Owner
- [ ] Accelo client record complete: billing contact, primary contact, after-hours contact | Day 0 | Owner
- [ ] Create Accelo onboarding project and tasks from this plan | Day 0 | Owner
- [ ] Welcome email sent with emergency line 410-555-0100 and ticket instructions | Day +1 | Help Desk
- [ ] Kickoff call held: goals, busy season dates, who approves changes | Day +2 | Owner
- [ ] Ask about tax-season freeze dates and any extended deadlines (extension season to October 15) | Day +2 | Owner
- [ ] Get written approval to access the client's systems | Day +2 | Owner

## Phase 2: Discovery (Day +2 to Day +7)

Owner role: Lead Tech, with Field Tech onsite

- [ ] Site walk scheduled with the office manager | Day +3 | Field Tech
- [ ] Inventory every workstation, server, laptop, printer, scanner, firewall, switch, AP | Day +5 | Field Tech
- [ ] Photograph the network closet and label ports | Day +5 | Field Tech
- [ ] Record ISP, circuit type, account number reference, static IP | Day +5 | Field Tech
- [ ] List line-of-business apps: tax software (CCH Axcess, CCH ProSystem fx, Drake, UltraTax CS), accounting (QuickBooks), document portal, e-sign, scanning workflow | Day +5 | Lead Tech
- [ ] Record software versions, licensing, and who holds the license keys | Day +6 | Lead Tech
- [ ] Review the Microsoft 365 or Google tenant: users, admins, MFA state, mail flow, domain | Day +6 | Lead Tech
- [ ] Review current backups: what, where, how often, last successful restore | Day +6 | Lead Tech
- [ ] Review the firewall and Wi-Fi: firmware, rules, guest network | Day +6 | Lead Tech
- [ ] Ask about tribal knowledge: scanner quirks, partners who work remote, special hardware | Day +7 | Lead Tech
- [ ] Draft the client file in the documentation platform | Day +7 | Lead Tech

## Phase 3: Risk review and plan (Day +7 to Day +10)

Owner role: Lead Tech and Owner

- [ ] Gap list written: end-of-life hardware, unsupported Windows, no MFA, no backup test, flat network | Day +8 | Lead Tech
- [ ] Gap list reviewed with the client; priorities agreed | Day +10 | Owner
- [ ] Quote any needed hardware or projects | Day +10 | Owner
- [ ] Decide what must be done before the next tax-season freeze | Day +10 | Owner

## Phase 4: Stand up monitoring and protection (Day +10 to Day +18)

Owner role: Lead Tech

- [ ] Create the customer and site in N-central | Day +10 | Lead Tech
- [ ] Deploy N-central agent to every workstation and server | Day +12 | Help Desk
- [ ] Confirm each device appears under the right customer and site | Day +12 | Lead Tech
- [ ] Deploy EDR (SentinelOne) to every device | Day +12 | Help Desk
- [ ] Enable DNS filtering at the firewall or via agent | Day +14 | Lead Tech
- [ ] Apply the standard patch policy; set reboot window outside business hours | Day +14 | Lead Tech
- [ ] Import or create vault entries; confirm vault paths follow `Vault: <slug>/<item>` | Day +14 | Lead Tech
- [ ] Rotate shared admin and firewall passwords to new vault entries | Day +15 | Lead Tech
- [ ] Tune N-central alert thresholds to avoid noise (disk, offline, service) | Day +16 | Lead Tech
- [ ] Confirm alerts create Accelo tickets for this client | Day +16 | Lead Tech

## Phase 5: Backup and recovery (Day +14 to Day +21)

Owner role: Lead Tech

- [ ] Install Datto appliance or configure Cove, matching the plan | Day +14 | Lead Tech
- [ ] First full backup completed | Day +16 | Lead Tech
- [ ] Add M365 backup (Omni+ Proactive and Omni+ Managed) | Day +16 | Lead Tech
- [ ] Add the client to the daily backup check list | Day +17 | Help Desk
- [ ] Test restore of one file and one server (or VM) | Day +20 | Lead Tech
- [ ] Record the restore test result in the client file | Day +21 | Lead Tech

## Phase 6: Users and security (Day +14 to Day +25)

Owner role: Help Desk

- [ ] Verify every user has a Microsoft 365 license that matches what they use | Day +18 | Help Desk
- [ ] Turn on MFA for every user; enroll phones or authenticator apps | Day +20 | Help Desk
- [ ] Enable conditional access baseline (block legacy auth) | Day +21 | Lead Tech
- [ ] Remove unused accounts and old admins | Day +21 | Lead Tech
- [ ] Set up the break-glass admin account with a vault reference | Day +21 | Lead Tech
- [ ] Short security tip sheet delivered to staff | Day +25 | Help Desk
- [ ] Phishing reporting button or process explained | Day +25 | Help Desk

## Phase 7: Office and equipment (Day +10 to Day +25)

Owner role: Field Tech

- [ ] Label all devices in the office with asset tags | Day +14 | Field Tech
- [ ] Fix known cabling problems | Day +18 | Field Tech
- [ ] Document the scanner workflow and scan-to-email or scan-to-folder settings | Day +20 | Field Tech
- [ ] Printer queues cleaned up, static IPs set for printers | Day +20 | Field Tech
- [ ] Wi-Fi: separate guest network, SSID and password reference recorded | Day +22 | Field Tech
- [ ] UPS tested; battery age recorded | Day +22 | Field Tech
- [ ] Update photos in the client file | Day +25 | Field Tech

## Phase 8: Handoff and review (Day +25 to Day +30)

Owner role: Owner

- [ ] Client file reviewed by a second tech (not the author) | Day +26 | Lead Tech
- [ ] Training call: how to open a ticket, how to reach the emergency line | Day +27 | Help Desk
- [ ] 30-day review meeting: what went well, what is still open | Day +30 | Owner
- [ ] Create recurring tasks in Accelo: monthly patch review, daily backup check, quarterly review | Day +30 | Owner
- [ ] Close the onboarding project | Day +30 | Owner

## Notes

- A CPA client's most sensitive moment is January to April. Even a good onboarding can go sideways if you touch the scanner or the tax database during that time.
- Common surprises: tax software license tied to one machine, a partner working from a home computer, QuickBooks running on a workstation that is never backed up, a scanner that only talks to one old PC.
- If any phase slips more than three days, tell Casey in the project.

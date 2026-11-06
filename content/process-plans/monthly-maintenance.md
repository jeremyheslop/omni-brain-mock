# Process Plan: Monthly Maintenance

owner: Alex Rivera
last_reviewed: 2026-04-02
tags: process-plan, maintenance, patching, backups, monthly
plan_id: monthly-maintenance
applies_to: Omni+ Basic, Omni+ Proactive, Omni+ Managed
duration: one calendar month, per client
related: sops/06-monthly-patch-review.md, sops/07-failed-patch-remediation.md, sops/08-daily-backup-check.md, sops/09-backup-restore-test.md, sops/25-server-reboot-window.md

How to use: create one Accelo recurring project per client on the first business day of each month, with one task per checkbox. Day offsets count from the first business day (Day 0). CPA clients: during the freeze (January 15 to April 18), do reviews only. No patch deployments to servers. Sam handles anything onsite. Jordan handles anything that is mostly ticket and report work.

Owner roles: Help Desk (Jordan Blake), Lead Tech (Alex Rivera), Field Tech (Sam Okafor), Owner (Casey Morgan).

## Phase 1: Month start review (Day 0 to Day +2)

Owner role: Help Desk

- [ ] Last month's closed tickets scanned for repeat issues | Day 0 | Help Desk
- [ ] Open tickets older than 14 days reviewed; stale ones updated or closed | Day +1 | Help Desk
- [ ] N-central: list of devices offline more than 14 days reviewed; retire or fix | Day +1 | Help Desk
- [ ] N-central: devices with no recent check-in reported to the Lead Tech | Day +1 | Help Desk
- [ ] Client contacts confirmed current (any new hires or departures not yet processed) | Day +2 | Help Desk

## Phase 2: Patch review and approval (Day +2 to Day +6)

Owner role: Lead Tech

- [ ] Microsoft patch Tuesday updates reviewed (second Tuesday) | Day +2 | Lead Tech
- [ ] Known bad updates flagged from vendor notices and community reports | Day +2 | Lead Tech
- [ ] Approve patches for pilot group (internal and one friendly client) | Day +3 | Lead Tech
- [ ] Pilot group checked after 48 hours | Day +5 | Lead Tech
- [ ] Approve patches for the rest of the clients, excluding hold clients | Day +6 | Lead Tech
- [ ] Third-party patching (browsers, Adobe, Java, Zoom) approved | Day +6 | Lead Tech
- [ ] Confirm reboot windows are set per client (see client files) | Day +6 | Lead Tech

## Phase 3: Patch deployment and follow-up (Day +7 to Day +14)

Owner role: Help Desk with Lead Tech

- [ ] Servers patched in the agreed window | Day +7 | Lead Tech
- [ ] Workstation patching completed | Day +8 | Help Desk
- [ ] Failed patches listed with device names | Day +10 | Help Desk
- [ ] Failed patches remediated or ticketed per the failed patch SOP | Day +12 | Help Desk
- [ ] Devices still pending reboot nudged via ticket or reminder to user | Day +12 | Help Desk
- [ ] Patch compliance report exported (target 95 percent or better) | Day +14 | Lead Tech
- [ ] Exceptions recorded in the client file (devices excluded and why) | Day +14 | Lead Tech

## Phase 4: Backup and recovery review (Day +3 to Day +20)

Owner role: Lead Tech

- [ ] Backup success rate reviewed for the previous 30 days | Day +3 | Lead Tech
- [ ] Any client with two or more failures in the month flagged | Day +3 | Lead Tech
- [ ] Retention and storage usage checked on each appliance | Day +5 | Lead Tech
- [ ] Spot-restore one file per Omni+ Proactive client | Day +10 | Help Desk
- [ ] For Omni+ Managed clients: schedule the quarterly restore test if this is a quarter-end month | Day +10 | Lead Tech
- [ ] M365 backup job status confirmed | Day +10 | Help Desk
- [ ] Results written to the client files | Day +15 | Help Desk

## Phase 5: Security hygiene (Day +10 to Day +20)

Owner role: Lead Tech

- [ ] EDR console: any unresolved threats or devices without an agent | Day +10 | Lead Tech
- [ ] DNS filtering: top blocked categories scanned for oddities | Day +10 | Help Desk
- [ ] Microsoft 365: sign-in risk report, new admin roles, new forwarding rules | Day +12 | Lead Tech
- [ ] MFA status report: users without MFA | Day +12 | Help Desk
- [ ] Guest and external sharing review (Omni+ Proactive and Omni+ Managed) | Day +14 | Lead Tech
- [ ] Disabled accounts older than 90 days listed for cleanup | Day +14 | Help Desk
- [ ] Admin account list reviewed (quarterly months only) | Day +14 | Lead Tech

## Phase 6: Infrastructure and onsite (Day +10 to Day +25)

Owner role: Field Tech

- [ ] Firewall firmware check; schedule updates | Day +10 | Lead Tech
- [ ] Switch and AP firmware check | Day +12 | Field Tech
- [ ] UPS battery status from N-central or unit display | Day +15 | Field Tech
- [ ] Disk space on servers: any volume above 80 percent ticketed | Day +10 | Help Desk
- [ ] Warranty and end-of-life list updated (workstations over five years) | Day +15 | Field Tech
- [ ] Scheduled onsite visit (Omni+ Proactive and Omni+ Managed) using onsite checklist | Day +20 | Field Tech
- [ ] SSL and domain expiry check | Day +15 | Help Desk

## Phase 7: Reporting and billing (Day +20 to Day +25)

Owner role: Owner

- [ ] License counts compared to the actual M365 and software users | Day +20 | Help Desk
- [ ] Time entries reviewed for missing or vague notes | Day +22 | Help Desk
- [ ] Monthly summary written for Omni+ Managed clients (one paragraph, in Accelo) | Day +24 | Lead Tech
- [ ] Invoices checked against contracts | Day +25 | Owner
- [ ] Any client at risk (late invoices, unresolved P2s) raised to Casey | Day +25 | Owner

## Phase 8: Documentation upkeep (Day +25 to Day +30)

Owner role: Help Desk

- [ ] Each client file touched this month has a change log entry | Day +26 | Help Desk
- [ ] Any file with last_reviewed over 12 months reviewed or flagged | Day +28 | Lead Tech
- [ ] New quirks learned this month added to "Gotchas" sections | Day +28 | Help Desk
- [ ] Next month's project created | Day +30 | Help Desk

## Notes

- A patch cycle that slips past Day +14 puts clients out of compliance targets. Tell Casey.
- Some clients have patch holds or special reboot windows. Read the client file (Gotchas section) before approving patches for a client you do not know well.

# Shorepoint Wealth Partners

owner: Casey Morgan
last_reviewed: 2026-04-02
tags: financial-advisory, wealth-management, orion, redtail, compliance, email-archiving, omni-proactive, easton
client_id: 1003
slug: shorepoint-wealth-partners
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Advanced Security, Omni+ Server, Email Management, Omni+ Passportal
industry: Financial Services
employees: 11

## Overview
Shorepoint Wealth Partners is an 11-person registered investment advisory (RIA) firm in Easton, MD. Four advisors (two principals), three client service associates, one paraplanner, one compliance officer who is also the COO, one operations/admin, one receptionist.

Core systems: Orion (portfolio management and reporting), Redtail CRM, Schwab Advisor Center (custodian portal, browser only), and eMoney for financial planning. All cloud. The IT footprint is mostly laptops, M365, a firewall, and compliance tooling.

What makes this client different from the CPA firms: **everything has to be retained and provable.** Email is archived under SEC and state rules. Any change to mail flow, retention, or archiving needs Casey Morgan's sign off and a heads-up to their compliance officer first. See Gotchas.

Client since 2023. Casey owns the relationship directly.

## Service plans and contract notes
- Core plan: Omni+ Proactive. First response: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Email Management, Omni+ Passportal.
- Contract renews April 1. Casey handles renewal in February.
- Onsite visit included: one scheduled visit per quarter (Sam Okafor). Easton is about 45 minutes from Salisbury, schedule at least a week out.
- Includes N-central monitoring and patching, SentinelOne, DNSFilter, Datto SIRIS (small appliance), Datto SaaS Protection for M365, help desk.
- Not included: Smarsh archive subscription (client pays Smarsh directly), Orion and Redtail support (vendors).
- Client asked for an annual written summary of security controls for their regulator exam binder. Casey produces it in March. Alex Rivera supplies the technical details.
- Monthly patch reports are sent to the COO, Beatrice Okonkwo-Hale, on the first business day (see `sops/06-monthly-patch-review.md`).

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary (managing principal) | Grant Ellsworth-Pierce | 410-555-0141 | grant@shorepointwealth.example |
| Billing | Naomi Castellano (operations) | 410-555-0142 | naomi@shorepointwealth.example |
| After-hours | Beatrice Okonkwo-Hale (COO / compliance) | 302-555-0169 | beatrice@shorepointwealth.example |
| Compliance officer | Beatrice Okonkwo-Hale | 302-555-0169 | beatrice@shorepointwealth.example |
| Receptionist | Tyrell Vance | 302-555-0170 | frontdesk@shorepointwealth.example |
| Senior CSA (key user) | Imogen Farrow | 410-555-0144 | imogen@shorepointwealth.example |

- For anything involving email retention, archiving, or a possible data incident, call Beatrice before anyone else. She has a regulatory notification clock to think about.

## Sites and addresses
- Main office: 7 Goldsborough Street, Suite 2B, Easton, MD 21601 (fictional). Second floor over a coffee shop.
- Hours: Mon-Fri 8:30-5:30. Advisors often work from home on Fridays.
- Access: keypad door to the suite, code in the vault note under `lob-app-admin` (yes, it's a strange place, ask Casey). Elevator is slow, stairs are fine.
- Network closet: small locked cabinet in the file room. Key is with Naomi.

## Internet and circuits
- ISP: Delmarva Link Fiber, 300/300 Mbps business fiber. Account ref DLF-51877-3 (fictional).
- Static IP: 203.0.113.118. Single static, assigned to the UniFi gateway.
- Backup: LTE failover through a Ubiquiti UniFi LTE Backup unit (carrier SIM billed to us). Tested in October 2025.
- Outage procedure: `sops/35-isp-outage-troubleshooting.md`.

## Network
- Gateway: Ubiquiti UniFi Cloud Gateway (SHW-GW01), threat management on, geo-blocking set to block non-US inbound.
- Switch: one UniFi 24-port PoE switch (SHW-SW01).
- Wi-Fi: three UniFi U6 Pro access points. SSID `ShorepointStaff` (WPA3), `ShorepointGuest` (isolated, 8 hour captive portal).

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 1 | Default/Management | 10.30.1.0/24 | Network gear |
| 10 | Staff | 10.30.10.0/24 | Laptops, printers |
| 20 | Conference | 10.30.20.0/24 | Conference room AV |
| 30 | Guest | 10.30.30.0/24 | Guest Wi-Fi |

- DHCP from the UniFi gateway. Staff scope 10.30.10.50-10.30.10.200. DNS goes to DNSFilter.
- No on-prem servers, no domain controller. Laptops are Entra ID joined.
- VPN: none needed. All apps are cloud.

## Servers and line-of-business apps
- No servers. Small Datto SIRIS appliance exists only for the shared network drive on a NAS (SHW-NAS01, Synology, 10.30.10.8). The NAS holds scanned client onboarding paperwork and compliance folders.
- Orion: cloud portfolio platform, SSO through M365 for most users.
- Redtail CRM: cloud, each user has their own login. The Redtail desktop sync tool (Redtail Speed) is installed on 5 laptops, and it fails to sync after Outlook updates. See Gotchas.
- eMoney Advisor and Schwab Advisor Center: cloud. Schwab hardware tokens are held by advisors, we do not manage them.
- Smarsh archive (email and text archiving): journaling from Exchange Online to the vendor. We do not touch the journal rule.

## Microsoft 365 / Google tenant notes
- Tenant: shorepointwealth.example on Microsoft 365 Business Premium. 11 licenses plus 1 shared mailbox (`clientservice@`).
- Exchange Online journaling rule sends a copy of all internal and external mail to the Smarsh archive address. **Do not disable, edit, or reorder this rule.** If a mail flow issue looks related, open a ticket and call Casey.
- Retention policies: litigation hold on all mailboxes (compliance requirement). Do not delete mailboxes for departed employees. Convert to shared and keep the hold.
- Departing user offboarding follows `sops/03-employee-offboarding.md` plus an extra step: confirm archive coverage with Beatrice before license removal.
- MFA is enforced with Authenticator. Conditional Access blocks sign-in from outside the US.
- Teams chats are captured by Smarsh. Personal texting apps are against firm policy.

## Backup
- Datto SIRIS (SHW-BK01) protects the Synology NAS shares via agentless backup. Hourly during business hours, cloud replication nightly.
- Datto SaaS Protection for M365 covers all 12 mailboxes, OneDrive, SharePoint and Teams chats. Three backups a day.
- Retention: Datto cloud 7 years for the NAS share (client requirement, billed). M365 backup retained 1 year. Needs verification whether the M365 retention was extended to match.
- Restore test: last full test 2026-02-11 (T-25107), passed. Daily check follows `sops/08-daily-backup-check.md`.
- Laptops are not backed up. Compliance bans local storage of client records and checks this themselves.

## Printers, scanners, and other devices
| Device | Model | Address | Notes |
|---|---|---|---|
| SHW-PR01 | Xerox VersaLink C415 | 10.30.10.20 | Main printer, scan to email |
| SHW-SC01 | Fujitsu ScanSnap iX1600 | Wi-Fi | Imogen's desk, scans to NAS |
| SHW-AV01 | Logitech Rally Bar | 10.30.20.11 | Large conference room |

- Office phones are cell phones plus a Zoom Phone line for the receptionist. We do not manage Zoom.

## Vendor contacts
| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Support desk | 410-555-0150 | Primary circuit |
| Smarsh (archive) | Account rep Colleen Marsh | 410-555-0147 | Billing is client's |
| Easton Office Systems | Jerome Tull | 410-555-0148 | Xerox service |

## Gotchas / tribal knowledge
1. **Never touch the Exchange journaling rule or the Smarsh connector.** A broken journal can create a compliance gap that the firm has to report. If mail to the archive looks stuck, call Beatrice and Casey, not the vendor.
2. Redtail Speed loses sync after Outlook updates. Fix: sign out, reinstall Redtail Speed, re-authorize. It takes 10 minutes per laptop. Warn Imogen first, she watches the calendar sync.
3. The coffee shop downstairs once tripped a breaker shared with the closet cabinet. Sam moved the gear to a separate circuit in 2025.
4. Beatrice wants changes on a Wednesday after 5:30 PM or Friday after 2 PM. Not Monday mornings, advisors are on client calls.
5. If the large conference display goes blank at a client meeting, power cycle the Rally Bar hub, not the display.
6. Advisors travel. Conditional Access blocks non-US sign-in. For travel abroad, ask 5 business days ahead so Casey can approve a temporary country exception, then remove it.

## Credential references (vault paths only)
- Vault: shorepoint-wealth-partners/firewall-admin
- Vault: shorepoint-wealth-partners/switch-admin
- Vault: shorepoint-wealth-partners/wifi-psk
- Vault: shorepoint-wealth-partners/domain-registrar
- Vault: shorepoint-wealth-partners/m365-global-admin-breakglass
- Vault: shorepoint-wealth-partners/isp-portal
- Vault: shorepoint-wealth-partners/backup-appliance
- Vault: shorepoint-wealth-partners/lob-app-admin (door code note and Redtail admin)
- Vault: shorepoint-wealth-partners/printer-admin

## Change log
- 2026-04-02 Casey Morgan: Annual review and renewal prep. Updated retention notes (T-25214).
- 2026-02-11 Alex Rivera: Full restore test of NAS share, passed (T-25107).
- 2025-10-21 Sam Okafor: Tested LTE failover, passed.
- 2025-06-09 Jordan Blake: Offboarded advisor, converted mailbox to shared with hold kept (T-23788).
- 2025-01-15 Alex Rivera: Enabled geo-blocking and Conditional Access country restriction.
- 2023-04-03 Casey Morgan: Initial onboarding via `sops/01-new-client-onboarding.md`.

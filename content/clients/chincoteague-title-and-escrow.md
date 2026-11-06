# Chincoteague Title & Escrow

owner: Alex Rivera
last_reviewed: 2026-09-30
tags: title-escrow, softpro, wire-fraud, ron, omni-basic, snow-hill
client_id: 1007
slug: chincoteague-title-and-escrow
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Advanced Security, Omni+ Server, Server Backup, Omni+ Backup, Email Management
industry: Financial Services
parent_company: Eastern Shore Credit Union Services (1016)
employees: 8

## Overview
Small title and escrow company in Snow Hill, MD. 8 staff: owner/attorney, 3 closers/settlement agents, 2 processors, 1 title examiner, 1 office manager. Handles residential closings across Worcester and Wicomico counties, plus some commercial. Closings are the whole business: Thursday and Friday, and the last 3 business days of each month, are the busiest.

Main systems: SoftPro Select for order and closing management, a scanner-heavy paper workflow, and a remote online notarization (RON) platform used for about a third of closings. Money moves by wire, so email security and the wire-fraud policy matter more here than at most clients.

Treat any report of a suspicious email as a P1 until proven otherwise (see wire-fraud section below).

Related company: this title agency is a subsidiary of Eastern Shore Credit Union Services (client 1016, credit union service organization). It is a separate company with its own contract and its own IT. In Accelo the link is the Parent Company field on the company profile.

## Service plans and contract notes
- Core plan: Omni+ Basic. N-central agent on all devices, SentinelOne, DNSFilter. Backup comes from the Server Backup and Omni+ Backup add-ons: Datto SIRIS appliance and Datto SaaS Protection for M365.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Omni+ Backup, Email Management.
- Response targets: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Onsite visit by agreement at a quarterly interval, usually the first Tuesday of the quarter, billed per visit. Never on closing days.
- They carry cyber insurance and send us the renewal questionnaire every September. Casey Morgan handles it, Alex fills in the technical answers.
- Contract renews in July. Last renewal 2026-07, no changes.
- Email gateway (Proofpoint Essentials) is NOT part of the Email Management add-on here. Owner asked about it in 2026, quote is in Accelo as a pending project (P-0412).

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Rhonda Whitaker (Office Manager) | 410-555-0139 | rhonda@chincoteaguetitle.example |
| Billing | Rhonda Whitaker | 410-555-0139 | billing@chincoteaguetitle.example |
| After-hours | Gordon Satterfield (Owner/Attorney) | 410-555-0145 | gordon@chincoteaguetitle.example |
| Lead closer | Alicia Dunmore | 410-555-0146 | alicia@chincoteaguetitle.example |
| Title examiner | Wendell Parrish | 410-555-0149 | wendell@chincoteaguetitle.example |

Main line: 410-555-0140. Rhonda is the day-to-day contact for everything. Gordon only gets called for incidents involving money or client data.

## Sites and addresses
- Main office: 6 Market Street, Suite B, Snow Hill, MD 21863
- Hours: Mon-Fri 8:30-5:00. Closings run until 6:00 or later.
- Access: front door is keyed, after-hours alarm panel needs a code held by Rhonda. Sam has a keyholder agreement on file.
- Network closet is a small locked cabinet in the file room, behind the shredding bin.
- Offsite closings: closers carry laptops and a portable scanner to bank and attorney offices. They tether to phone hotspots.

## Internet and circuits
- ISP: Delmarva Link Fiber, 500/500 symmetric business fiber.
- Static IP: 203.0.113.74.
- Account ref: DLF-77402 (fake). Portal: `Vault: chincoteague-title-and-escrow/isp-portal`.
- ONT is in the file room, ISP-owned, powered from a small UPS shared with the firewall.
- Secondary: Gordon's office has a cellular hotspot (not managed by us). No automatic failover. If fiber is down on a closing day, closers use hotspots and SoftPro on the server still works internally.
- See `sops/35-isp-outage-troubleshooting.md`.

## Network
- Firewall: Fortinet FortiGate 60F (CTE-FW01), FortiOS updates scheduled by Alex only after hours.
- Switch: one Aruba Instant On 1930 24-port PoE (CTE-SW01).
- Wi-Fi: 2 Aruba Instant On AP22. Staff SSID, and a guest SSID with captive terms used in the conference room.
- DHCP on the FortiGate. Internal DNS from CTE-SRV01 for the AD domain.
- VPN: FortiClient SSL VPN for the owner and two closers, MFA required. Setup per `sops/19-vpn-user-setup.md`.

| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 1 | Staff | 10.40.10.0/24 | Workstations, server, printers |
| 20 | Guest | 10.40.20.0/24 | Internet only, isolated |
| 30 | VoIP | 10.40.30.0/24 | Desk phones |

DHCP on Staff: 10.40.10.100-10.40.10.199. Server at 10.40.10.5, printers and scanners 10.40.10.20-10.40.10.30.

## Servers and line-of-business apps
- CTE-SRV01: Windows Server 2022, physical Dell T350. Active Directory, file shares, SoftPro database (SQL Server Standard), print server. 32 GB RAM.
- SoftPro Select: order entry, title commitments, settlement statements, policy production. Client install on every PC. SoftPro database lives on CTE-SRV01. Vendor support covers upgrades, we only do the server side.
- RON platform (NotaryBridge, fictional vendor): browser based, runs on the closers' laptops with a webcam and a second monitor. Credential verification and e-seal handled on their side. Recorded sessions stay in their cloud for the required retention period, not on our server.
- Wire and escrow accounts are in the bank's online portal. We never touch those credentials. Positive pay is configured by the bank.
- Document imaging: scanned closing packages saved to `\\CTE-SRV01\Closings\<year>\<file number>`. Keep the folder structure. SoftPro document links point at those paths.
- QuickBooks Desktop (escrow reconciliation) runs on Rhonda's PC, not the server.

## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 8 licenses plus a shared mailbox (closings@).
- Tenant domain: chincoteaguetitle.example. MFA enforced for all users, number matching, no SMS.
- Conditional Access: sign-ins blocked from outside the US. Closers who travel have to tell Rhonda who opens a ticket first (this one is a pain, see gotchas).
- External email banner is on for all inbound messages. Auto-forwarding to external addresses is disabled in the transport rules. Any new inbox rule that forwards or deletes triggers an alert to Alex.
- Datto SaaS Protection backs up mailboxes, OneDrive and SharePoint daily.
- Break-glass admin exists, see credential references.

## Backup
- Datto SIRIS appliance (CTE-BKP01) on the Staff VLAN, image backups of CTE-SRV01 every hour during business hours, nightly offsite replication to Datto cloud.
- Retention: local 30 days, cloud 1 year. Closing documents kept longer under the firm's own retention schedule (7 years), done by Rhonda via an archive folder on the server.
- Datto SaaS Protection for M365 as above.
- Daily check by help desk per `sops/08-daily-backup-check.md`.
- Restore test: not part of Omni+ Basic, but Alex does one in January each year. Last: 2026-01-14, restored SoftPro SQL backup to a test VM, passed.
- Cyber insurance form asks for proof of backups. Pull the report from the Datto portal each September.

## Printers, scanners, and other devices
- Konica Minolta bizhub C300i copier (CTE-PR01), static 10.40.10.21, scan-to-email through the M365 SMTP relay. See `sops/17-scan-to-email-troubleshooting.md`.
- Two Fujitsu fi-7160 desktop scanners at closer desks, USB.
- Portable Brother scanners for offsite closings, 3 units, kept in a cabinet labeled by name.
- Docusign-style signing pads are used at closing tables. Wired USB, driver version matters.
- 8 workstations (CTE-WS-001 to CTE-WS-008), plus 3 laptops for closers (CTE-LT-01 to -03).
- Desk phones are a hosted VoIP system, VLAN 30.

## Vendor contacts
| Vendor | Rep | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Support line | 410-555-0181 | Account DLF-77402 (fake) |
| SoftPro support | Marcy Eckhart | 410-555-0182 | Needs the license ID from the vault note |
| NotaryBridge (RON) | Tier 2 support | 410-555-0183 | Webcam and browser issues |
| Hosted phone provider | Chesapeake Voice Co. | 410-555-0175 | Handsets, forwarding |
| Cyber insurance broker | Gareth Lowry | 410-555-0184 | Renewal questionnaire |

## Gotchas / tribal knowledge
- Wire-fraud policy. Written policy is on the firm's SharePoint, a summary is here: no change to wire instructions is accepted by email; every outbound wire gets a callback to a phone number already on file, never one from the email; wires over $10,000 need two people. IT's part: protect the mailboxes. Any report of a spoofed or "changed instructions" email gets a P1, loop in Casey Morgan, and follow `sops/11-suspected-compromised-account.md` and `sops/10-phishing-email-response.md`. Do not rely on the closer's judgment alone.
- If a mailbox is suspected compromised, tell Gordon by phone, not by email. The attacker may be reading the thread.
- Never touch the closing workstations during a scheduled closing. Ask Rhonda for the calendar first. Reboots and patch windows are Sunday evening only.
- SoftPro client updates must be done on all PCs at the same version. When the vendor pushes a new build, version mismatch gives a cryptic "database schema" error. Get the install files from SoftPro, do the server first.
- The RON webcams must be the Logitech model the platform approved. Substituting a different webcam fails the identity check, learned this the hard way in 2025.
- The geo-block in Conditional Access catches closers using VPNs on hotel Wi-Fi. Add a temporary exception, set an expiry date, and remove it after the trip.
- The copier scan-to-email stops working whenever the shared mailbox password rotates. It uses an app-specific SMTP credential, not the mailbox password (check the vault note).
- Two PCs share a desk with a signing pad. Pad driver installs on one PC only, the other gets the plain USB port.
- Rhonda keeps a paper binder of closings by file number. Do not delete old folders from the server, she checks them for audits.
- Snow Hill has frequent short power flickers. The UPS in the file room was replaced in 2026 after it failed during one, battery replacement is every 3 years.

## Credential references
- `Vault: chincoteague-title-and-escrow/firewall-admin`
- `Vault: chincoteague-title-and-escrow/switch-admin`
- `Vault: chincoteague-title-and-escrow/wifi-psk`
- `Vault: chincoteague-title-and-escrow/isp-portal`
- `Vault: chincoteague-title-and-escrow/domain-registrar`
- `Vault: chincoteague-title-and-escrow/m365-global-admin-breakglass`
- `Vault: chincoteague-title-and-escrow/backup-appliance`
- `Vault: chincoteague-title-and-escrow/lob-app-admin` (SoftPro server and SQL admin)
- `Vault: chincoteague-title-and-escrow/printer-admin`

## Change log
- 2026-09-30: Cyber insurance questionnaire technical answers submitted. (Alex Rivera, T-25503)
- 2026-07-22: Annual review. Updated contacts and renewal date. (Alex Rivera)
- 2026-05-06: Replaced file room UPS after power flicker outage. (Sam Okafor, T-24850)
- 2026-03-11: Added forward/delete inbox rule alerts after near-miss spoof attempt. (Alex Rivera, T-24688)
- 2026-01-14: Annual restore test of SoftPro SQL backup, passed. (Alex Rivera, T-24402)
- 2025-10-02: Onboarded NotaryBridge webcams and second monitors for 3 closers. (Jordan Blake, T-23977)

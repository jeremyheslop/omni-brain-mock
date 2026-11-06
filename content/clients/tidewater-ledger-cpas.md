# Tidewater Ledger CPAs

owner: Alex Rivera
last_reviewed: 2026-09-18
tags: cpa, accounting, tax-season-freeze, cch-axcess, quickbooks, omni-proactive, salisbury
client_id: 1001
slug: tidewater-ledger-cpas
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management
industry: Financial Services
employees: 14

## Overview

Tidewater Ledger CPAs is a 14-person CPA firm in Salisbury, MD. Three partners, four seniors, five staff accountants/preparers, one office manager, one receptionist. Mix of individual and small business tax, audit/review work, and about 30 bookkeeping clients that live in QuickBooks Online.

Main practice software is CCH Axcess (Tax, Workstream, Document) in the cloud, plus CCH ProSystem fx Engagement for a few legacy audit files that Marcus Whitlock (partner) refuses to migrate. A few client files for QuickBooks Desktop Enterprise live on the local server.

One onsite server (TLC-SRV01), one Datto SIRIS appliance, one FortiGate. 14 workstations, most with dual monitors. This is one of our busiest accounts from Jan 20 to Apr 20 and again around Oct 15 (extension deadline). See the freeze rules in Gotchas.

Client since 2021. Moved from time and materials to Omni+ Proactive in March 2023 after the January 2023 server failure (T-19302).

## Service plans and contract notes

- Core plan: Omni+ Proactive. First response: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management.
- Contract renews every January 1. Casey Morgan handles renewal, usually in November.
- Onsite visit included: one scheduled visit per quarter (Sam Okafor). Extra onsite is billed at the standard onsite rate. Pre-season visit is always in the first week of January.
- Busy-season addendum (signed 2024): partners get a direct line to Alex during Jan 20 to Apr 20 and P3 tickets from preparers are treated as P2 for response time. Do not downgrade these on triage. Ask Casey if unsure.
- After-hours during busy season is covered at no extra charge for P1 and P2 only. Everything else after hours is billed at the after-hours rate.
- Included: N-central monitoring, patching, SentinelOne, DNSFilter, Datto SIRIS plus SaaS Protection for M365, help desk.
- Not included: CCH Axcess application support (call CCH), project work (new server, Windows 11 upgrades are quoted separately).
- Billing contact wants a single itemized invoice by the 3rd of the month. Accelo time entries need to say which user and device.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary (managing partner) | Diane Whitlock-Ames | 302-555-0171 | diane@tidewaterledger.example |
| Billing | Priya Nandakumar (office manager) | 302-555-0172 | priya@tidewaterledger.example |
| After-hours | Marcus Whitlock (partner) | 302-555-0173 | marcus@tidewaterledger.example |
| Office manager / day-to-day | Priya Nandakumar | 302-555-0172 | priya@tidewaterledger.example |
| Receptionist | Tomas Ferreira | 410-555-0120 | frontdesk@tidewaterledger.example |
| Senior preparer (key user) | Gloria Esposito | 302-555-0174 | gloria@tidewaterledger.example |

- Diane is the decision maker for spend. Priya can approve anything under $250 without asking Diane.
- Marcus answers his cell after hours but is bad about voicemail. Text first, then call.
- Gloria is the unofficial super-user. If a preparer has a CCH Axcess problem, she has usually already seen it.

## Sites and addresses

- Main office: 218 Camden Avenue, Suite 300, Salisbury, MD 21801 (fictional). Second floor of a three-story brick building shared with a dentist and an insurance agent.
- Hours: Mon-Fri 8:00-5:00. Busy season: Mon-Sat 8:00-7:00 and Sundays 12:00-5:00 from about Feb 15.
- Access: front door code changes in January, ask Priya. Server closet is inside the supply room behind reception. The key hangs inside the supply room door frame, top left.
- Parking: client lot behind the building. Visitors should not use the dentist spaces (they tow).
- No second site. Two partners work from home some days using the VPN, see Network.

## Internet and circuits

- Primary: Delmarva Link Fiber, 500/500 Mbps business fiber. Account ref DLF-48213-0 (fictional).
- Static IP: 203.0.113.42/29 (usable range .41 to .46). FortiGate WAN1 uses .42. .43 is reserved, do not assign.
- Secondary: Bayline Broadband business cable, 300/30 Mbps, dynamic IP, WAN2 on the FortiGate. Used for failover only. Added after the 2024 fiber cut (T-22640).
- ONT for the fiber is in the server closet, top shelf, left of the UPS. The fiber provider's ONT has a battery backup that beeps every 10 minutes when it is dying. Replace through Delmarva Link, not us.
- Cable modem is in the same closet. It is the bridge-mode type, do not let anyone turn on its Wi-Fi.
- Delmarva Link support: 410-555-0150. Bayline Broadband support: 410-555-0151. See Vendor contacts.
- ISP portal login is in the vault, see Credential references.

## Network

- Firewall: FortiGate 60F (TLC-FW01), FortiOS 7.4.x. Active on WAN1 (fiber), WAN2 (cable) in failover. Firmware updates by Alex only, after hours, never in busy season.
- Switching: two Ubiquiti UniFi 24-port PoE switches (TLC-SW01 in closet, TLC-SW02 in the partners' wing). Uplink between them on ports 23-24 (LAG).
- Wi-Fi: three UniFi U6 Pro access points (reception, open bullpen, partner offices). SSID `TidewaterStaff` (WPA2/WPA3) and `TidewaterGuest` (isolated, captive portal, 4 hour limit).
- UniFi controller runs as a hosted network application on TLC-SRV01. If the server is down, APs keep working but you can't adopt or change settings.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 1 | Default/Management | 10.20.1.0/24 | Switches, APs, firewall |
| 10 | Staff | 10.20.10.0/24 | Workstations, server |
| 20 | Printers | 10.20.20.0/24 | Copiers, scanners |
| 30 | Guest | 10.20.30.0/24 | Guest Wi-Fi, internet only |
| 40 | VoIP | 10.20.40.0/24 | Desk phones (hosted VoIP) |

- DHCP: FortiGate serves DHCP on VLANs 10, 20, 30, 40. Staff scope 10.20.10.100-10.20.10.220. Server is static at 10.20.10.5. Reservations for scanners are on VLAN 20, see Gotchas.
- DNS: TLC-SRV01 is the domain controller and DNS server (10.20.10.5). FortiGate forwards upstream to DNSFilter resolvers. Internal domain is `tidewater.local`.
- VPN: FortiClient SSL VPN for the two partners and Gloria (works from home during crunch). MFA through FortiToken Mobile. Setup steps in `sops/19-vpn-user-setup.md`. Split tunnel is on, so CCH Axcess traffic goes direct to the internet.
- Firewall changes go through `sops/18-firewall-rule-change-request.md`. Diane must approve in writing for anything that opens an inbound port. There are none today.

## Servers and line-of-business apps

| Device | Role | OS | Notes |
|---|---|---|---|
| TLC-SRV01 | DC, file server, QuickBooks Desktop host, UniFi app | Windows Server 2019 | Dell PowerEdge T350, 64 GB RAM, RAID 10 |
| TLC-BK01 | Datto SIRIS appliance | Datto OS | In closet, see Backup |

- CCH Axcess: cloud. Users sign in through a browser plus the Axcess Tax local client on workstations. Staff run the Axcess Document desktop uploader for the scanners.
- CCH ProSystem fx Engagement: one legacy audit database on TLC-SRV01 in `D:\Apps\Engagement`. Marcus and one senior use it. Do not move it without a ticket and a restore test.
- QuickBooks Desktop Enterprise 23: company files for six bookkeeping clients in `D:\QB\Clients`. Hosted from the server, multi-user mode. The QuickBooks Database Server Manager service must be running. If a QB client can't open a file in multi-user mode, restart that service first.
- QuickBooks Online: accessed by browser for the rest of the bookkeeping clients. Accountant-invite model, nothing for us to manage.
- Document portal: SafeSend (returns) and TaxCaddy (client uploads). Browser based. Nothing local.
- Shared drives: `S:\Clients` (client folders, about 1.4 TB), `T:\Templates`, `P:\Partners` (restricted to partners).
- Server reboots follow `sops/25-server-reboot-window.md`. Window is Sunday 6:00 AM outside busy season. In busy season only with Diane's OK.

## Microsoft 365 / Google tenant notes

- Tenant: tidewaterledger.example on Microsoft 365 Business Premium. 15 licenses (14 users plus one shared mailbox converted to licensed for the scanner relay, see Gotchas).
- Email domain: tidewaterledger.example. MX points to Exchange Online. SPF, DKIM, DMARC set to quarantine. DNS is hosted at the registrar, see `sops/21-domain-dns-change.md`.
- MFA is enforced via Conditional Access (security defaults are off). Authenticator app preferred. Phone swaps follow `sops/32-new-phone-mfa-device-swap.md`.
- Shared mailboxes: `info@`, `taxdocs@` (client document drop, 5 users have access), `payroll@` (partners and Priya only).
- OneDrive Known Folder Move is on for Desktop and Documents on laptops only. Desktops use the server shares.
- Break-glass global admin account exists and is excluded from Conditional Access. Credentials in the vault.
- License changes via `sops/14-m365-license-changes.md`. Seasonal staff: Diane usually adds two temp preparers in late January. Ask for names by January 10.

## Backup

- Datto SIRIS (TLC-BK01) backs up TLC-SRV01 every 1 hour during the day, nightly full verification. Cloud replication to Datto cloud.
- Datto SaaS Protection covers all 15 M365 mailboxes plus OneDrive and the `taxdocs@` shared mailbox. Three backups a day.
- Retention: local 30 days, cloud 1 year. The IRS wants 3 years for returns but the actual returns live in CCH Axcess, which has its own retention. Don't promise Diane anything about 7-year retention without checking with Casey.
- Daily check per `sops/08-daily-backup-check.md`. Restore tests: Omni+ Proactive does these semi-annually. Last full restore test was 2026-06-10 (T-25388), file-level only. A full virtualization test has not been done since 2025.
- QuickBooks files are backed up with the server image. Priya also makes manual `.qbb` backups on Fridays to a USB drive in the safe. Don't trust those. They are not scheduled and the drive is old.
- Workstations are not backed up. Staff are told to save to the server. Laptop users with OneDrive KFM are covered by OneDrive only.

## Printers, scanners, and other devices

| Device | Model | Location | Address | Notes |
|---|---|---|---|---|
| TLC-PR01 | Ricoh MP C3004 copier | Bullpen | 10.20.20.11 | Main printer, scan to folder and email |
| TLC-PR02 | HP LaserJet Pro M404dn | Partners' wing | 10.20.20.12 | Partners only |
| TLC-SC01 | Fujitsu fi-7160 | Bullpen | USB to TLC-WS-004 | Tax doc scanning, PaperStream Capture |
| TLC-SC02 | Fujitsu fi-7160 | Front desk | USB to TLC-WS-001 | Receptionist uses it for intake |
| TLC-SC03 | Fujitsu fi-7600 | Supply room | 10.20.20.15 | High volume, only used Mar-Apr |

- 14 workstations named TLC-WS-001 through TLC-WS-014, mostly Dell OptiPlex Micro with two 24 inch monitors. Laptops: TLC-WS-011 through 014 (partners and Gloria).
- Desk phones: hosted VoIP from a provider the firm manages directly. We only provide the VLAN. Phone problems go to the VoIP vendor first.
- UPS: APC Smart-UPS 1500 in closet, battery replaced 2025-11. Sam checks it each quarter.

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Support desk | 410-555-0150 | Primary circuit |
| Bayline Broadband | Support desk | 410-555-0151 | Failover cable |
| CCH Axcess support | Tax support line | 800 number on account page | Ask for Tier 2 for rendering bugs |
| Datto | Partner support | via N-central or portal | Open case through the partner portal |
| Coastline Voice (hosted VoIP) | Renee Dalton | 410-555-0153 | Firm contracts directly |
| Keystone Copier Services | Walt Bryner | 410-555-0154 | Ricoh service contract |

## Gotchas / tribal knowledge

1. **Tax-season freeze: Jan 20 to Apr 20, and again Oct 1 to Oct 20.** No server reboots, no Windows feature updates, no firewall firmware, no driver pushes, no new software installs without Diane's approval. N-central patch policy for this client is set to "security only, deferred" during these windows. Follow `sops/31-cpa-tax-season-software-prep.md` before January 10 every year.
2. The scanner fi-7600 only works through the SMTP relay on port 465 with the dedicated account. Port 587 fails silently. The scan-to-email failures were traced in T-23915. See `sops/17-scan-to-email-troubleshooting.md`.
3. Gloria's laptop (TLC-WS-013) loses the mapped `S:` drive after sleep. It is a known issue with the VPN auto-connect order. Fix is `net use S: /delete` then remap. Real fix is on the Windows 11 refresh list.
4. CCH Axcess Tax is picky about browser extensions. If the Tax return screen goes white, disable all extensions first, then clear cache, then call CCH.
5. QuickBooks Database Server Manager will stop if the server is rebooted without a clean shutdown. Check the service first thing after any server restart or the bookkeeping users will call within five minutes.
6. Never reboot TLC-SRV01 between 8:00 and 6:00 in busy season, even for a Critical alert, without calling Diane or Marcus. A forced reboot during a 2023 e-file run cost them half a day (T-20877).
7. The fiber ONT beeping is not our problem. Call Delmarva Link. Do not unplug it.
8. Two temp preparers get shared Windows logins every year because the firm insists. Push back, create real accounts. Jordan has this on the onboarding checklist now.
9. Priya forwards phishing "invoice" emails to us all the time. That is good. Treat each as `sops/10-phishing-email-response.md`, even when it is obvious, because Diane wants a ticket trail.
10. The Sunday busy-season staff run the Ricoh copier alone. If it jams and they text Alex, tell them to call Keystone Copier first. Alex is not the printer guy on weekends.
11. Do not use the partners' wing switch ports 19-22 for anything. They are wired to old wall jacks that carry a ground loop and flap.

## Credential references (vault paths only)

- Vault: tidewater-ledger-cpas/firewall-admin
- Vault: tidewater-ledger-cpas/switch-admin
- Vault: tidewater-ledger-cpas/wifi-psk
- Vault: tidewater-ledger-cpas/domain-registrar
- Vault: tidewater-ledger-cpas/m365-global-admin-breakglass
- Vault: tidewater-ledger-cpas/isp-portal
- Vault: tidewater-ledger-cpas/backup-appliance
- Vault: tidewater-ledger-cpas/lob-app-admin (QuickBooks admin and Engagement admin)
- Vault: tidewater-ledger-cpas/printer-admin
- Vault: tidewater-ledger-cpas/scanner-relay-account

## Change log

- 2026-09-18 Alex Rivera: Reviewed doc. Added Oct 1-20 extension freeze, confirmed fi-7600 relay account (T-25611).
- 2026-06-10 Sam Okafor: Quarterly onsite. UPS self-test passed, labeled switch ports in closet. File-level restore test completed (T-25388).
- 2026-01-07 Sam Okafor: Pre-season visit. Replaced failing fan in TLC-SRV01, cleaned dust from closet, verified failover to cable (T-24980).
- 2025-11-14 Sam Okafor: Replaced UPS battery.
- 2025-03-04 Alex Rivera: Updated FortiOS to 7.4.x after the season. Re-enabled patch policy to normal.
- 2024-08-19 Alex Rivera: Added WAN2 cable failover after the fiber cut (T-22640).
- 2023-03-02 Casey Morgan: Moved from time and materials to Omni+ Proactive. Initial onboarding via `sops/01-new-client-onboarding.md`.

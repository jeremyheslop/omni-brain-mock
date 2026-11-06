# Pocomoke Bay Tax & Advisory

owner: Jordan Blake
last_reviewed: 2025-06-12
tags: cpa, tax, drake-tax, omni-basic, pocomoke-city, small-office, cove-backup
client_id: 1002
slug: pocomoke-bay-tax-and-advisory
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Advanced Security, Omni+ Backup
industry: Financial Services
employees: 9

## Overview
Small tax and advisory practice in Pocomoke City, MD. Nine people: owner/EA (Enrolled Agent) Lorraine Tilghman-Reese, one CPA, four tax preparers, a bookkeeper, an admin, and a part-time seasonal helper counted in the headcount. Mostly individual returns, small business returns, and payroll for a handful of local businesses.

Main software is Drake Tax (installed, network version) and QuickBooks Online for the bookkeeping side. No domain controller. Workstations are joined to Entra ID (cloud only) and the Drake data lives on a small NAS-style file share on one PC.

This client is lighter weight than Tidewater Ledger CPAs. Much less structure, no partner group, decisions are all Lorraine. Last full review of this doc was June 2025, so check anything marked "needs verification".

Client since 2022.

## Service plans and contract notes
- Core plan: Omni+ Basic. First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Add-ons: Omni+ Advanced Security, Omni+ Backup.
- After-hours support by request only, billed at the after-hours rate. Lorraine knows this and still calls on Sundays in February. Log it, bill it.
- No scheduled onsite visits are included. Onsite is billed as needed. Sam Okafor does most of it, about a 50 minute drive from Salisbury.
- Includes N-central monitoring, patching, SentinelOne, DNSFilter, Cove Data Protection (cloud only) for the file server PC, help desk.
- Does not include Datto SaaS Protection for M365. Lorraine declined it in the 2024 renewal. Casey Morgan has the signed note. Needs verification whether this was revisited at the 2025 renewal.
- Contract renews July 1. Casey handles renewal in May.
- Tax-season freeze applies, see Gotchas. Same general rules as `sops/31-cpa-tax-season-software-prep.md`.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary (owner/EA) | Lorraine Tilghman-Reese | 302-555-0159 | lorraine@pocomokebaytax.example |
| Billing | Odell Pruitt (bookkeeper) | 302-555-0160 | odell@pocomokebaytax.example |
| After-hours | Lorraine Tilghman-Reese (cell) | 302-555-0161 | lorraine@pocomokebaytax.example |
| Admin / front desk | Keisha Warrington | 302-555-0162 | office@pocomokebaytax.example |
| CPA on staff | Hollis Greer | 302-555-0163 | hollis@pocomokebaytax.example |

- Keisha opens most tickets by phone. Ask her for the computer name on the sticker. Only Lorraine approves new spend.

## Sites and addresses
- One office: 41 Market Street, Pocomoke City, MD 21851 (fictional). Street-level storefront with a back office and a small supply room.
- Hours: Mon-Fri 9:00-5:00, plus Saturdays 9:00-2:00 from Feb 1 to Apr 15.
- Access: front door key only. Keisha has a key and opens at 8:30. Spare key at the hardware shop next door (owner knows us, call Keisha first).
- Network gear is on a shelf in the supply room. Needs verification: may have moved to a wall cabinet.

## Internet and circuits
- ISP: Bayline Broadband, business cable 200/20 Mbps. Account ref BB-77402 (fictional).
- Static IP: 198.51.100.77 (single static). Not currently used for any inbound rules.
- Modem: Bayline-supplied cable modem, set to bridge mode. Sits next to the UniFi gateway.
- No failover circuit. If cable goes down, staff tether to phones. See `sops/35-isp-outage-troubleshooting.md`.

## Network
- Gateway: Ubiquiti UniFi Dream Machine (UDM) acting as router, firewall, and UniFi controller. Name POKE-GW01.
- Switch: one Ubiquiti UniFi 16-port PoE switch (POKE-SW01).
- Wi-Fi: two UniFi U6 Lite access points. SSID `PocomokeBay` for staff and `PocomokeBay-Guest` for guests (isolated).
- Internal subnet for staff is 192.168.40.0/24. Needs verification: older notes say 192.168.1.0/24 before the 2024 gateway swap.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 1 | Default | 192.168.40.0/24 | Staff, printer, file share PC |
| 20 | Guest | 192.168.41.0/24 | Guest Wi-Fi, internet only |

- DHCP is handled by the UDM. Scope 192.168.40.100-192.168.40.200. The file share PC and printer have static assignments below .100.
- DNS: UDM forwards to DNSFilter resolvers. No internal DNS zone.
- VPN: none. Lorraine remotes into her office PC through N-central remote control. Needs verification.

## Servers and line-of-business apps
There is no server. The Drake Tax network data lives on a shared folder on a regular workstation.

| Device | Role | Notes |
|---|---|---|
| POKE-WS-01 | Drake Tax data host (shared folder `C:\DrakeData`) | Dell OptiPlex, 32 GB RAM, 1 TB NVMe plus 2 TB data drive. Never power off during the day. |
| POKE-WS-02 to POKE-WS-09 | Preparer and staff workstations | Windows 11 Pro, mostly refreshed in 2024 |

- Drake Tax: network install, data folder on POKE-WS-01, clients map to `\\POKE-WS-01\DrakeData`. Updates come from Drake in January and are installed by the staff with our help. Support: Drake support line.
- Drake Documents, Drake Portal, QuickBooks Online: cloud, no local footprint.
- Check scanner: Epson DS-530 II at front desk, TWAIN driver on POKE-WS-09.
- Needs verification: whether a separate e-file transmitter machine still exists.

## Microsoft 365 / Google tenant notes
- Tenant: pocomokebaytax.example on Microsoft 365 Business Premium. 9 licenses.
- Workstations are Entra ID joined, managed with Intune basic policies. No on-prem AD.
- MFA is enforced for all users with the Authenticator app. Lorraine uses SMS as a fallback. Not ideal, see `sops/12-mfa-reset.md`.
- Email: Exchange Online. SPF set, DKIM enabled, DMARC at `p=none`. Needs verification and tightening, tracked as a P4 task.
- Shared mailbox: `office@` (Keisha, Odell, Lorraine). Break-glass admin in the vault.

## Backup
- Cove Data Protection (cloud only) backs up POKE-WS-01 (the Drake data folder and Documents) nightly at 11:00 PM. Retention 28 days in cloud.
- No local copy, no Datto appliance on this plan. M365 and other workstations are not backed up (see contract notes).
- Daily check per `sops/08-daily-backup-check.md`. Restore testing is not part of this plan. Jordan did an informal file restore on 2025-04-22 (T-23211) after Keisha deleted a client folder.

## Printers, scanners, and other devices
| Device | Model | Address | Notes |
|---|---|---|---|
| POKE-PR01 | Brother MFC-L8900CDW | 192.168.40.20 | Main printer and scanner, scan to email works |
| POKE-PR02 | HP LaserJet Pro M404n | 192.168.40.21 | Back office, Hollis uses it |

- Scan-to-email troubleshooting: `sops/17-scan-to-email-troubleshooting.md`.
- Phones are cell phones plus one analog fax line that Lorraine will not give up. Not our problem.

## Vendor contacts
| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Bayline Broadband | Business support | 410-555-0151 | Cable circuit |
| Drake Software | Support line | on Drake account page | Call for e-file rejects |
| Chesapeake Copy & Print | Dale Hutchins | 410-555-0138 | Brother toner and service |

## Gotchas / tribal knowledge
1. **Never power off or restart POKE-WS-01 during business hours.** It is a regular PC acting as the Drake data host. If it reboots, everyone's Drake session drops and some data files lock for a few minutes after. Patches for it are scheduled in N-central for Sunday 6:00 AM.
2. Tax-season freeze: Jan 15 to Apr 20 (and Sept 15 to Oct 15 for extensions). No feature updates, no driver pushes, no software installs unless Drake needs it. Ask Lorraine before touching POKE-WS-01 in these windows.
3. Drake needs an exclusion in SentinelOne for the data folder, or the first open each morning is very slow. The exclusion is in place. Don't remove it when cleaning up policies.
4. Keisha's PC (POKE-WS-09) has the check scanner TWAIN driver and will crash the Drake client if Windows decides to update the driver. If Drake closes by itself on that PC, check the scanner driver version first.
5. Hollis prints to POKE-PR02 and sometimes it falls off the network. The printer's DHCP lease was fixed with a static address, but the problem returned once after the 2024 UDM swap. Needs verification that it is still static.

## Credential references (vault paths only)
- Vault: pocomoke-bay-tax-and-advisory/firewall-admin (UDM and UniFi controller)
- Vault: pocomoke-bay-tax-and-advisory/switch-admin
- Vault: pocomoke-bay-tax-and-advisory/wifi-psk
- Vault: pocomoke-bay-tax-and-advisory/domain-registrar
- Vault: pocomoke-bay-tax-and-advisory/m365-global-admin-breakglass
- Vault: pocomoke-bay-tax-and-advisory/isp-portal
- Vault: pocomoke-bay-tax-and-advisory/backup-appliance (Cove console login, not an appliance)
- Vault: pocomoke-bay-tax-and-advisory/lob-app-admin (Drake EFIN admin)
- Vault: pocomoke-bay-tax-and-advisory/printer-admin

## Change log
- 2025-06-12 Jordan Blake: Reviewed doc, added "needs verification" markers where info is old (T-23902).
- 2025-04-22 Jordan Blake: Restored deleted client folder from Cove for Keisha (T-23211).
- 2025-01-09 Sam Okafor: Pre-season check. Cleaned up POKE-WS-01 disk, confirmed Cove job ran (T-22987).
- 2024-09-17 Alex Rivera: Replaced old gateway with UniFi Dream Machine. Changed internal subnet (T-22244).
- 2022-07-12 Casey Morgan: Initial onboarding via `sops/01-new-client-onboarding.md`.

# Nanticoke Mechanical Services

owner: Jordan Blake
last_reviewed: 2025-05-19
tags: hvac, trades, field-tablets, servicetitan, omni-basic, delmar-de, needs-review
client_id: 1010
slug: nanticoke-mechanical-services
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Server, Server Backup, Hosted Website Plan
industry: Plumbing
employees: 34

## Overview
HVAC and plumbing contractor in Delmar, DE. About 20 field techs and installers, plus dispatch, estimators, accounting and managers. Techs run service calls from company field tablets. Main systems: a ServiceTitan-style field service app (cloud), QuickBooks Desktop on a small office server, and a flat office network. This file has not been fully reviewed in a while. Check anything marked "needs verification" with Dale before relying on it.

## Service plans and contract notes
- Core plan: Omni+ Basic. N-central agent on office PCs and the server. Response targets: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Add-ons: Omni+ Server, Server Backup, Hosted Website Plan.
- Scheduled onsite visits by agreement: semiannual. Date of last visit needs verification.
- Contract renewal date: needs verification (believed spring).
- Dispatch cannot be down during the first cold snap or first heat wave of the year.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dale Hutchins (Operations Manager) | 302-555-0121 | dale@nanticokemech.example |
| Billing | Sherry Lund (Accounting) | 302-555-0122 | sherry@nanticokemech.example |
| After-hours | Dale Hutchins (cell) | 302-555-0123 | dale@nanticokemech.example |
| Dispatch lead | Rob Tilghman | 302-555-0124 | dispatch@nanticokemech.example |

Main line: 302-555-0120.

## Sites and addresses
- Shop and office: 910 Industrial Park Road, Delmar, DE 19940. Office Mon-Fri 7:00-4:30, dispatch by rotation 7 days. Techs start at the yard at 6:30.
- Access: keypad door, code held by Dale. Network rack is in the parts room.
- Yard Wi-Fi: needs verification (unknown whether the yard AP was ever installed).

## Internet and circuits
- ISP: Delmarva Link Fiber, 300/300 business fiber. Static IP 203.0.113.140. Account ref: needs verification.
- Portal: `Vault: nanticoke-mechanical-services/isp-portal`. Backup circuit: none documented.

## Network
- Firewall: SonicWall TZ370 (bought before our contract). Firmware status needs verification.
- Switch: one 24-port switch in the parts room, model not documented yet. APs: needs verification (believed 2 UniFi).
- DHCP and DNS on the SonicWall, range 192.168.1.100-192.168.1.199. Believed flat network on 192.168.1.0/24, no VLANs documented. Guest Wi-Fi isolation needs verification.
- VPN: SonicWall Global VPN for dispatch from home. User count needs verification.

## Servers and line-of-business apps
- NMS-SRV01: Windows Server (2016, believed), 192.168.1.10. QuickBooks Desktop Enterprise company file, estimating spreadsheets, scanned work orders.
- Field service app: cloud, used on tablets and dispatch PCs. Vendor admin contact not documented yet, Dale holds the login.
- About 20 rugged Samsung Galaxy Tab Active tablets with a mobile card reader. MDM method not documented yet.

## Microsoft 365 / Google tenant notes
- Believed Microsoft 365 Business Standard for office staff, field techs on shared or no mailboxes. Needs verification.
- Tenant domain: nanticokemech.example. MFA enforcement is partial, needs verification.

## Backup
- The Server Backup add-on normally means a Datto SIRIS appliance. Whether one is installed here needs verification (check N-central and the Datto portal).
- Schedule, retention and last restore test: not documented yet.

## Printers, scanners, and other devices
- Ricoh copier on lease. Model and IP not documented yet. Scans go to a folder on NMS-SRV01.
- About 9 office PCs (NMS-WS-001 to NMS-WS-009 believed).

## Vendor contacts
- Delmarva Link Fiber: business support 302-555-0191.
- Copier vendor (Peninsula Print Partners): 302-555-0194, lease contract.
- Field service app vendor: not documented yet.

## Gotchas / tribal knowledge
- Maintenance only after 7:00 PM or on a Sunday, and ask Rob first.
- Do not update SonicWall firmware without a config export. The 2024 attempt dropped VPN users for a morning.
- Tablets lose sync when the shop Wi-Fi password changes. Update the tablets at the same time.
- The server UPS battery was flagged for replacement. Not verified whether it was done.
- Dale rarely replies to tickets. Call him.

## Credential references
- `Vault: nanticoke-mechanical-services/firewall-admin`
- `Vault: nanticoke-mechanical-services/wifi-psk`
- `Vault: nanticoke-mechanical-services/isp-portal`
- `Vault: nanticoke-mechanical-services/m365-global-admin-breakglass`
- `Vault: nanticoke-mechanical-services/lob-app-admin` (QuickBooks, server admin)

## Change log
- 2025-05-19: Partial review, marked missing items. (Jordan Blake)
- 2025-02-06: Updated copier vendor contact. (Jordan Blake, T-22488)
- 2024-11-12: SonicWall firmware update attempt, rolled back. (Alex Rivera, T-21970)

# Kingfisher Bookkeeping

owner: Jordan Blake
last_reviewed: 2026-03-11
tags: accounting, bookkeeping, quickbooks-online, small-office, home-office, time-and-materials
client_id: 1017
slug: kingfisher-bookkeeping
core_plan: none (time and materials)
service_plans: Email Management
industry: Financial Services
employees: 4

## Overview
Four-person bookkeeping shop run out of the owner's house in Hebron. The office is a converted garage with its own entrance. No server. Everything is cloud: QuickBooks Online (client books), Microsoft 365, and a shared Dropbox-style folder that clients use to drop receipts (the client's own account, not ours). Small, low drama, but the owner (Brenda) is very particular about not losing client data.

## Service plans and contract notes
- Core plan: none (time and materials).
- Add-ons: Email Management.
- First response: P1 4 business hours, P2 next business day, P3 and P4 best effort.
- After-hours by request only, billed at the after-hours rate. Brenda knows this and rarely asks.
- No onsite visits included. Sam goes out when needed, billed hourly. Travel from Salisbury is about 25 minutes.
- Busiest times: end of each month (client closes) and the week of quarterly payroll filings.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Brenda Kowalczyk (Owner) | 410-555-0198 | brenda@kingfisherbooks.example |
| Billing | Brenda Kowalczyk | 410-555-0198 | brenda@kingfisherbooks.example |
| After-hours | Brenda (cell) | 410-555-0199 | brenda@kingfisherbooks.example |
| Staff / daily user | Tomasz Reilly (Senior Bookkeeper) | 302-555-0128 | tomasz@kingfisherbooks.example |

## Sites and addresses
- One site: 7 Heron Lane, Hebron, MD 21830 (owner's property, garage office). Hours roughly Mon-Fri 8:30-4:30, flexible.
- Dog in the yard. Call before arriving. Park in the gravel by the side door, not the driveway.
- Not documented yet: alarm / access notes for after-hours entry.

## Internet and circuits
- ISP: Bayline Broadband residential-business cable plan, about 200/20. Account ref BB-71204.
- Static IP: none. Dynamic address, so no VPN or inbound rules.
- Modem/router combo is ISP-supplied, in the house utility closet. The office gets its network through a cable run to the garage.
- Needs verification: whether the ISP gateway is still the only router, or if Brenda added her own.

## Network
- Ubiquiti UniFi Cloud Gateway Lite plus one UniFi AP in the garage. Flat network 192.168.10.0/24, DHCP from the gateway.
- Wi-Fi SSIDs: `Kingfisher` (staff) and `Kingfisher-Guest` (isolated, rarely used).
- No VLANs, no VPN. Staff work remotely from home occasionally, all apps are cloud so it doesn't matter.
- Network diagram: not documented yet.

## Servers and line-of-business apps
- No servers.
- QuickBooks Online Accountant (Brenda is the accountant user, client books accessed through it). No desktop QuickBooks anymore, retired in 2024.
- Gusto-style payroll portal for two of their clients, logins are client-owned.
- Adobe Acrobat on all four PCs. Brenda's license is from us, the rest are subscription under her account.
- 4 workstations: `KFB-WS-01` to `KFB-WS-04` (3 desktops, 1 laptop). N-central agent installed for remote access only.

## Microsoft 365 / Google tenant notes
- Tenant `kingfisherbooks.example`, 4 Business Standard licenses. No Defender add-on, not on Business Premium.
- MFA is on for everyone via Authenticator. Brenda has a hardware key as a backup.
- Not documented yet: whether any shared mailbox exists. Brenda mentioned an `info@` alias once.

## Backup
- Cove Data Protection on the 4 workstations, set up at Brenda's request (cloud only, no appliance). Daily at 11:00 PM. We do not monitor it.
- No M365 backup (not part of the Email Management add-on). Brenda was offered it, said no. Mentioned in the 2025 review.
- Restore test: not done recently. Last known restore was a one-file request in late 2025.

## Printers, scanners, and other devices
- One HP LaserJet-class printer/scanner on Wi-Fi, static reservation on the gateway. Scan-to-email not set up, they scan to USB.
- Desk scanner: small Fujitsu ScanSnap, USB, Tomasz's PC.

## Vendor contacts
- Bayline Broadband business support: 410-555-0172 (account holder is Brenda, they will not talk to us without her).
- Intuit support: client-owned, Brenda calls them.

## Gotchas / tribal knowledge
1. Brenda's husband's work laptop sometimes joins the staff Wi-Fi. It's not ours. Ignore the unknown device alerts for hostname `LAPTOP-HM01`.
2. Tomasz's PC loses the ScanSnap after sleep. Unplug and replug USB, or reboot. Haven't found a better fix.
3. The garage gets hot in summer. Brenda's PC has shut down on heat twice. Check that first on a "random shutdown" ticket.
4. Month-end close: do not schedule patching reboots in the last 3 business days of the month.
5. Brenda prefers phone calls to email for anything urgent.

## Credential references
- Vault: kingfisher-bookkeeping/wifi-psk
- Vault: kingfisher-bookkeeping/m365-global-admin-breakglass
- Vault: kingfisher-bookkeeping/domain-registrar
- Vault: kingfisher-bookkeeping/isp-portal (needs verification, may be Brenda's personal login)
- Vault: kingfisher-bookkeeping/firewall-admin (UniFi cloud console)

## Change log
- 2026-03-11 (Jordan Blake): Light review, added backup and device notes.
- 2025-11-04 (Sam Okafor): Replaced garage AP after it died, adopted new one in UniFi. T-23761.
- 2025-06-19 (Jordan Blake): Onboarded Tomasz's new PC `KFB-WS-04`. T-23102.
- 2025-03-20 (Alex Rivera): Moved from old SonicWall to UniFi gateway. T-22618.

# Blue Crab Marine Repair
owner: Sam Okafor
last_reviewed: 2025-11-18
tags: marine, time-and-materials, rugged-laptops, shop-pcs, crisfield-md
client_id: 1022
slug: blue-crab-marine-repair
core_plan: none (time and materials)
service_plans: none
industry: Retail
employees: 13
## Overview
Boat engine and hull repair shop on the water in Crisfield, MD. 13 people: owner, shop foreman, 7 mechanics, parts counter, office manager, part-time bookkeeper. T&M customer: no monitoring, no N-central agent, no scheduled patching. We show up when they call and bill hourly. Do not look for them in N-central.
## Service plans and contract notes
- T&M (time and materials), hourly rate agreement, no monthly fee. Signed 2022.
- Add-ons: none.
- P1 first response 4 business hours, P2 next business day, P3/P4 best effort. After-hours only if Casey agrees per call (usually yes in October haul-out and April commissioning).
- Onsite trip charge applies (long drive from Salisbury). Batch fixes. Quote required before hardware over a few hundred dollars, call Dale.
- Offer Omni+ Basic once a year. Dale says no every year.
## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dale Tilghman (Owner) | 410-555-0112 | dale@bluecrabmarine.example |
| Billing | Pam Evans (Office Manager) | 410-555-0113 | pam@bluecrabmarine.example |
| After-hours | Dale Tilghman (cell) | 410-555-0114 | dale@bluecrabmarine.example |
| Shop foreman | Ricky Sterling | 410-555-0115 | ricky@bluecrabmarine.example |
## Sites and addresses
- Shop and office: 77 Somers Wharf Road, Crisfield, MD 21817. Mon-Fri 7:00-4:00, Sat 7:00-12:00. Metal building on the dock, office upstairs. Pam opens at 7. Closed-toe shoes in the shop.
## Internet and circuits
- Bayline Broadband business cable. Speed and account number: not documented yet. Dynamic IP. Modem in the office closet, ISP-owned. The old DSL line was removed in 2023.
## Network
- Consumer router from the ISP, not managed by us. Model needs verification. Flat network, probably 192.168.1.0/24. No VLANs, no VPN.
- Office Wi-Fi from the router, plus an old Netgear AP on a beam in the shop. Poor coverage at the back of the shop.
## Servers and line-of-business apps
- No server. QuickBooks Desktop Pro on Pam's PC (company file local, not shared). Parts catalog sites are web based.
- Engine diagnostic software (brand-specific) on the rugged laptops. Versions and dongles need verification.
## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Basic, 6 licenses. Mechanics have no email. Domain `bluecrabmarine.example`; registrar is Dale's personal login (needs verification). No MFA enforced, we have recommended it.
## Backup
- Not documented yet. Probably nothing. Pam copies QuickBooks to a USB stick on Fridays. Offer Cove Data Protection if Dale ever agrees.
## Printers, scanners, and other devices
- HP LaserJet in the office (shared via Pam's PC, needs verification). Zebra label printer at the parts counter, USB.
- 4 rugged laptops (Panasonic Toughbook class, Windows 10) for boat diagnostics. Weak batteries, not Windows 11 capable.
- 3 shop PCs (hand-me-down desktops, Windows 10) for parts lookup and timekeeping. All past Windows 10 support. Dale has been told. See `sops/23-end-of-life-hardware.md` and `sops/24-windows-10-to-11-upgrade.md`.
## Vendor contacts
- Bayline Broadband: 410-555-0172 (account number not recorded). Diagnostic software vendor: not documented. Everything else: ask Pam.
## Gotchas / tribal knowledge
1. Salt air and sawdust kill things. Keep spare mice and keyboards in the truck.
2. The Toughbooks are shared. Nobody knows which has which diagnostic license. Label them if you get the chance.
3. The shop AP Wi-Fi password is on a sticky note on the router. Do not copy it into a ticket.
4. October and April are busy. They will not wait for a P3.
5. Pam's PC is the only place the QuickBooks file lives. If it dies, the company file is gone. Raised many times.
## Credential references
- Router admin: `Vault: blue-crab-marine-repair/firewall-admin` (may not exist yet)
- Wi-Fi PSK: `Vault: blue-crab-marine-repair/wifi-psk`
- M365 admin: `Vault: blue-crab-marine-repair/m365-global-admin-breakglass`
- Domain registrar: not in the vault.
## Change log
- 2025-11-18 (Sam Okafor): Cleaned up notes after October visit. Replaced two Toughbook batteries. T-24102.
- 2025-04-22 (Jordan Blake): Reset Pam's M365 password, rebuilt Outlook profile.
- 2024-10-09 (Sam Okafor): Replaced shop AP.
- 2023-06-14 (Alex Rivera): Removed DSL line, cable only.

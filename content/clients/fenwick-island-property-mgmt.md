# Fenwick Island Property Mgmt
owner: Sam Okafor
last_reviewed: 2026-03-02
tags: property-management, appfolio, multi-site, vacation-rentals, omni-proactive, fortinet, unifi, seasonal
client_id: 1025
slug: fenwick-island-property-mgmt
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Server, Server Backup, Email Management, Omni+ Backup
industry: Real Estate
employees: 14
## Overview
Property management company on the Delaware coast. Manages about 160 vacation rentals and 40 long-term rentals across Fenwick Island, Bethany Beach and Ocean View. 14 staff: owner, 2 property managers, 4 leasing/guest services, 5 maintenance and housekeeping leads, 1 bookkeeper, 1 office admin. Main office plus three small satellite sites. Most work happens in AppFolio (cloud). Email and files are all Microsoft 365.
High season is Memorial Day to Labor Day. Saturday is changeover day (guests out by 10 AM, in after 4 PM) and the office runs on tablets and phones. N-central device prefix: `FIP-` (e.g. `FIP-FW01`, `FIP-WS-003`).
## Service plans and contract notes
- Omni+ Proactive, renewed 2025-12-01 for 12 months.
- Add-ons: Omni+ Server, Server Backup, Email Management, Omni+ Backup.
- P1 30 minutes (24x7), P2 2 business hours, P3 4 business hours, P4 next business day.
- Onsite included: main office monthly in the off-season, every other week June-August. Satellite sites by ticket only.
- Summer rule: nothing disruptive on Fridays or Saturdays from Memorial Day to Labor Day.
- Not covered: AppFolio itself, the door-code vendor portal, the phone carrier. We help with access and networking only.
- Renata wants a "what's broken at which site" summary at the monthly check-in. Use the N-central site view.
## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Renata Kowalczyk (Owner) | 302-555-0109 | renata@fenwickislandpm.example |
| Billing | Marcus Delaney (Bookkeeper) | 302-555-0110 | marcus@fenwickislandpm.example |
| After-hours | Tomas Reyes (Maintenance Director) | 302-555-0111 | tomas@fenwickislandpm.example |
| Office admin | Gwen Pettibone | 302-555-0112 | gwen@fenwickislandpm.example |
| Guest services lead | Dana Whitaker | 302-555-0113 | dana@fenwickislandpm.example |
Renata approves all spending. Gwen is the first call for users. Tomas is the only one with keys to every satellite in the off-season.
## Sites and addresses
| Site | Address | Hours | Notes |
|---|---|---|---|
| Main office | 1180 Coastal Highway, Suite 4, Fenwick Island, DE 19944 | Mon-Fri 8:30-5, summer weekends 9-3 | FortiGate, switch, Synology |
| Bethany satellite | 28 Pinecrest Court, Bethany Beach, DE 19930 | June-Aug | Leasing counter in a condo clubhouse |
| Maintenance yard | 5602 Hollow Road, Ocean View, DE 19970 | Mon-Sat 7-4 | Work-order PC, parts shelves |
| Ocean View long-term office | 330 Atlantic Terrace, Ocean View, DE 19970 | Mon-Fri 9-4 | Two staff, landlord router |
Access: the main office has a keypad. Satellite access codes live in the door-code system and are NOT documented here (see "Door and key system"). Ask Gwen or Tomas to let you in.
## Internet and circuits
| Site | ISP / circuit | Public IP | Notes |
|---|---|---|---|
| Main | Delmarva Link Fiber 300 Mbps, DLF-ACC-0072941 (fake) | 198.51.100.130 (static) | Portal: `Vault: fenwick-island-property-mgmt/isp-portal` |
| Bethany | Bayline Broadband cable 200/20 | 192.0.2.88 (dynamic) | Suspended Oct-Apr, reactivated each May |
| Yard | Bayline Broadband cable 100/10 | Dynamic | UniFi Cloud Gateway |
| Ocean View | Landlord-provided, shared | Unknown | Behind landlord router |
- Casey keeps the Bethany reactivation date in the Accelo contract. If it is dead in May, call Bayline before the visit.
- Main office outage: staff use phone hotspots (AppFolio works fine on a phone). Phones are cloud-hosted.
## Network
- Main: FortiGate 40F (`FIP-FW01`), UniFi Switch 16 PoE, 3x U6 Lite. Satellites: UniFi Cloud Gateway Ultra at Bethany and the yard, IPsec back to `FIP-FW01`. SSIDs `FIPM-Staff`, `FIPM-Guest`.
| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 1 | Staff | 10.60.1.0/24 | Workstations, printers |
| 20 | Guest | 10.60.20.0/24 | Visitors |
| 30 | Phones | 10.60.30.0/24 | Cloud phones, QoS on |
- Satellites are flat: Bethany 10.60.41.0/24, Yard 10.60.42.0/24. DHCP from the FortiGate or each UniFi gateway. No internal AD, PCs are Entra-joined, DNS via DNSFilter.
- Remote staff (4) use FortiClient VPN. See `sops/19-vpn-user-setup.md`.
## Servers and line-of-business apps
- No on-prem server. `FIP-SRV01` was retired in 2024, files are in SharePoint/OneDrive.
- `FIP-NAS01` (Synology, main): old camera footage and scan archives only, not backed up.
- AppFolio Property Manager (leases, accounting, owner statements, work orders) and the AppFolio Maintenance app on the yard and housekeeping tablets.
- Channel manager for bookings (cloud, guest services). QuickBooks Online (Marcus). DocuSign for leases.
- 12 staff PCs, mixed Dell OptiPlex/Latitude, all Windows 11 since 2026-02.
## Door and key system
Fenwick runs a hosted smart lock and lockbox system for rental units (guest, cleaner and master codes). We do NOT store or document codes. This file only points to where things live.
- Vendor portal: `Vault: fenwick-island-property-mgmt/door-code-system-admin`.
- Lock hub Wi-Fi (one small hub per building): `Vault: fenwick-island-property-mgmt/lock-hub-wifi`.
- Adding locks, rotating codes and guest schedules are done by Tomas or Gwen in the portal. A bad lock goes to the lock vendor, not us.
- Not documented here: hub models, unit-by-unit lock inventory, lockbox master codes. Ask Tomas.
## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 14 licenses, plus 5 F3 licenses for housekeeping leads (Outlook web and Teams on tablets). Domain `fenwickislandpm.example`.
- Shared mailboxes `reservations@`, `maintenance@`, `owners@` (`sops/15-shared-mailbox-setup.md`).
- MFA via Authenticator. Housekeeping MFA resets are common (wet phones). See `sops/12-mfa-reset.md` and `sops/32-new-phone-mfa-device-swap.md`.
- Break glass: `Vault: fenwick-island-property-mgmt/m365-global-admin-breakglass`.
- If AppFolio owner statements land in junk, check the SPF record before blaming M365 (`sops/21-domain-dns-change.md`).
## Backup
- Datto SaaS Protection for M365 only. No server, so no SIRIS. Laptops are not imaged, AppFolio data is vendor-hosted.
- `FIP-NAS01` has no backup. Renata accepted the risk in writing (T-23880).
- Daily check per `sops/08-daily-backup-check.md`.
## Printers, scanners, and other devices
- Main: Brother MFC-L8900CDW (scan to email), Epson label printer at guest services. Yard: HP LaserJet, USB to the work-order PC.
- 8 housekeeping iPads with an app and Wi-Fi profile in Intune. 6 consumer cameras at the yard owned by Tomas, not ours. Poly desk phones on VLAN 30.
## Vendor contacts
- Delmarva Link Fiber: 302-555-0141. Bayline Broadband: 410-555-0172 (Bethany and yard).
- Seabird Voice (cloud phones), Kyle Ostrander: 302-555-0114.
- AppFolio support: Gwen and Marcus only. Lock vendor: Tomas has the relationship.
## Gotchas / tribal knowledge
1. Summer Fridays and Saturdays are changeover. No reboots, no patches, no network changes.
2. The Ocean View office sits behind a landlord router we cannot log in to, so no VPN there. Staff use FortiClient from laptops. Ask Renata about bridge mode (open since 2024).
3. The Bethany tunnel uses a DDNS name because the IP is dynamic. If it is down after the cable returns in May, restart the gateway before debugging.
4. Housekeeping iPads get dropped in sinks. A spare loaner iPad is in the main office cabinet (Gwen has the key).
5. Scan-to-email on the Brother needs the SMTP relay on 587 with a relay user. It broke when SMTP AUTH was turned off tenant-wide (`sops/17-scan-to-email-troubleshooting.md`).
6. The yard PC `FIP-WS-011` auto-logs in. Don't change it. It has no sensitive data.
7. If AppFolio is slow, check main office upload first. The camera NAS used to upload nightly and clog the fiber. Disabled now.
8. Gwen resets Microsoft passwords herself. Make sure she never resets Renata's or an admin account.
9. The conference room TV switches inputs by itself. Turn off HDMI-CEC in the TV menu.
10. `FIP-WS-014` shows offline in N-central most of the time. It is a spare laptop in a drawer. Don't ticket it.
## Credential references
- Firewall: `Vault: fenwick-island-property-mgmt/firewall-admin`
- Satellite gateways: `Vault: fenwick-island-property-mgmt/switch-admin`
- Wi-Fi PSK: `Vault: fenwick-island-property-mgmt/wifi-psk`
- Lock hub Wi-Fi: `Vault: fenwick-island-property-mgmt/lock-hub-wifi`
- Door code system admin: `Vault: fenwick-island-property-mgmt/door-code-system-admin`
- Domain registrar: `Vault: fenwick-island-property-mgmt/domain-registrar`
- Printer admin: `Vault: fenwick-island-property-mgmt/printer-admin`
- AppFolio admin (owner only): `Vault: fenwick-island-property-mgmt/lob-app-admin`
## Change log
- 2026-03-02 (Sam Okafor): Review. Added door and key system section, noted we hold no codes. T-24477.
- 2026-02-10 (Jordan Blake): Windows 11 upgrade completed on last 3 PCs. T-24398.
- 2025-12-01 (Casey Morgan): Contract renewed.
- 2025-10-06 (Sam Okafor): Suspended Bethany cable for the season, saved tunnel config.
- 2025-06-02 (Alex Rivera): Reactivated Bethany, rebuilt IPsec tunnel with DDNS.
- 2025-04-15 (Sam Okafor): Replaced Brother printer at main office, updated relay settings.
- 2024-09-20 (Alex Rivera): Retired `FIP-SRV01`, moved files to SharePoint. P-0310.

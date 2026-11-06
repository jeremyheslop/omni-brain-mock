# Willards Ridge Orchards
owner: Jordan Blake
last_reviewed: 2025-04-22
tags: agriculture, orchard, seasonal, farm-stand, square-pos, rural-wireless, omni-basic, stale
client_id: 1023
slug: willards-ridge-orchards
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Email Management
industry: Manufacturing
employees: 11
## Overview
Family orchard and farm stand outside Willards, MD. Apples, peaches, pumpkins, cider. 11 year-round staff. From August to November they add about 25 seasonal workers (pickers, stand staff) who do not use company computers except the stand iPads.
This doc was last reviewed April 2025, before the 2025 harvest. Check everything here before trusting it, especially network and stand setup.
## Service plans and contract notes
- Omni+ Basic, signed 2024. Renewal date needs verification.
- Add-ons: Email Management.
- P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days. After-hours by request, billed at after-hours rate.
- Cove Data Protection (cloud) on the office PC. N-central agent, SentinelOne and DNSFilter on managed devices. Whether the stand iPads count as managed: not documented yet.
- Busy period Sept to mid-Nov. Do not schedule projects then.
## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Harlan Voss (Owner) | 410-555-0116 | harlan@willardsridge.example |
| Billing | Beth Voss (Office Manager) | 410-555-0117 | beth@willardsridge.example |
| After-hours | Harlan Voss (cell) | 410-555-0118 | harlan@willardsridge.example |
| Farm stand manager | Tasha Greer | not documented yet | stand@willardsridge.example |
## Sites and addresses
- Farm office and packing house: 9120 Ridge Road, Willards, MD 21874. Mon-Fri 7-4, office above the packing house. Ring the farm bell if nobody is in.
- Farm stand: 9118 Ridge Road, Willards, MD 21874. Sept-Nov, daily 9-6. Wooden stand by the road, no wired network.
## Internet and circuits
- Shoreline Wireless (rural fixed wireless), about 25/5 as of 2025 (needs verification). Static IP and account number: not documented yet.
- Antenna on the packing house roof, PoE injector in the office closet. If internet drops, power cycle the injector first.
## Network
- Router model: needs verification. How Wi-Fi reaches the stand (point-to-point or outdoor AP): not documented yet. No VLANs known, no VPN.
## Servers and line-of-business apps
- No server. QuickBooks Desktop on Beth's PC `WRO-WS-001`, company file local.
- Square Register on two iPads at the stand with a Square Reader. Square account is Harlan's. If stand Wi-Fi fails, Square uses offline mode.
## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Basic, 5 licenses. Domain `willardsridge.example`. Seasonal staff have no accounts. Tasha uses the `stand@` shared mailbox. MFA status needs verification.
## Backup
- Cove Data Protection on `WRO-WS-001` (QuickBooks file and Documents). Last verified restore: not documented yet. Nothing else is backed up.
## Printers, scanners, and other devices
- HP OfficeJet in the office on Wi-Fi (model needs verification). Star receipt printer at the stand, Bluetooth to the iPad. 2 stand iPads, 1 spare iPad, 1 laptop for Tasha.
## Vendor contacts
- Shoreline Wireless: 410-555-0119 (support), account number not recorded. Square: Harlan manages. Everything else: ask Beth.
## Gotchas / tribal knowledge
1. The stand opens in late August. Check stand Wi-Fi and the Square iPads the week before, not the day of.
2. Seasonal workers do not get Wi-Fi without asking Beth. She wants a guest password changed each season.
3. The roof antenna has been hit by lightning once. Cycle the PoE injector before calling the ISP.
4. Needs verification: where the router is, and whether the cider press scale (serial port) connects to anything.
## Credential references
- Router admin: `Vault: willards-ridge-orchards/firewall-admin` (not verified)
- Wi-Fi PSK: `Vault: willards-ridge-orchards/wifi-psk`
- M365 break glass: `Vault: willards-ridge-orchards/m365-global-admin-breakglass`
- Square admin: not ours, Harlan owns it.
## Change log
- 2025-04-22 (Jordan Blake): Added N-central agent to `WRO-WS-001`, noted Cove backup. T-23904.
- 2025-03-04 (Jordan Blake): Initial doc after onboarding.
- 2024-09-17 (Sam Okafor): Onsite assessment, checked antenna and stand Wi-Fi.

# Old Mill Grain & Supply

owner: Sam Okafor
last_reviewed: 2025-06-09
tags: agriculture, grain, omni-basic, quickbooks, rural-wireless, scale-software, princess-anne-md
client_id: 1014
slug: old-mill-grain-and-supply
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Server, Server Backup
industry: Retail
employees: 15

## Overview

Family-owned grain elevator and farm supply store outside Princess Anne. 15 people: 4 in the office (owner, bookkeeper, scale/ticket clerk, store manager), 3 at the retail counter, 8 yard and warehouse staff. Only the office and counter people use computers daily. Two shared PCs in the scale house and one in the warehouse office.

Busiest times: wheat harvest (late June to mid July) and corn/soy harvest (mid September to early November). During harvest the scale house runs 6:00 am to 9:00 pm. Do not schedule anything then.

Apps: grain scale and ticketing software (GrainTrak-style, called "the scale program"), QuickBooks Desktop Enterprise for accounting, and a farm supply POS module that talks to QuickBooks.

Note: this file was last fully reviewed in June 2025. Some details (staff, scale hardware) may have changed. Needs verification before relying on it.

## Service plans and contract notes

- Core plan: Omni+ Basic. Accelo contract C-1014-A.
- Add-ons: Omni+ Server, Server Backup.
- First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- After-hours is by request and billed at the after-hours rate. During harvest Dale Hartsock (owner) has pre-approved after-hours for scale house outages only. This is noted on the contract.
- Backup is Cove Data Protection (cloud only) for the server. No Datto.
- Casey Morgan has the pricing notes. Do not quote.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dale Hartsock (Owner) | 302-555-0137 | dale.hartsock@oldmillgrain.example |
| Billing | Ruth Ann Doyle (Bookkeeper) | 302-555-0138 | ruthann.doyle@oldmillgrain.example |
| After-hours | Dale Hartsock (cell) | 302-555-0139 | same as above |
| Scale house clerk | Tommy Pruitt | 302-555-0140 | tommy.pruitt@oldmillgrain.example |
| Store manager | Carol Everett | 302-555-0148 | carol.everett@oldmillgrain.example |

- Ruth Ann is the best first call during business hours. Dale answers his cell if it is a scale outage.
- Tommy runs the scale program. He is on the phone constantly during harvest, text him instead.

## Sites and addresses

| Site | Address | Notes |
|---|---|---|
| Main elevator and store | 9104 Old Mill Road, Princess Anne, MD 21853 | Office, scale house, store, warehouse. |
| Satellite seed barn | 2250 Deal Island Road, Princess Anne, MD 21853 | No network. Seasonal. |

- Office hours Mon-Fri 7:00-5:00, Sat 7:00-12:00. Scale house hours vary by season.
- Server and network gear are in the small closet behind the store counter. Door sticks, lift while turning.
- Gravel lot. Park by the office, not by the scale, trucks come through.

## Internet and circuits

- ISP: Chesapeake Prairie Wireless (fixed rural wireless), 50/10 plan. Account ref CPW-4471 (fictional). Support 410-555-0190.
- Radio is on a pole by the office. It is a Ubiquiti-style dish with PoE injector in the closet. IP is dynamic, no static. Last time we checked, the provider can supply a static for a monthly fee, client has declined.
- The signal drops in heavy rain or snow. This is normal. If it is down in storms, wait an hour before calling the ISP.
- There is no backup circuit. A cellular failover has been proposed twice (T-23611), client has not approved. Needs verification if this changed.
- Latency to the ISP is 40-60 ms. Do not bother testing speed from the scale house, Wi-Fi there is weak.

## Network

- Firewall/router: SonicWall TZ370 (older, bought 2022). Hostname `OMG-FW01`. Firmware is old, needs verification. Management from LAN only.
- Switch: one Netgear 24-port unmanaged in the closet and a small 8-port in the scale house.
- Wi-Fi: 2 Ubiquiti UniFi AC Lite APs (office and store). Scale house gets a UniFi AP in a weatherproof box, signal is weak across the yard. SSID `OldMill-Staff`. Guest SSID: none.
- Single flat LAN, 192.168.1.0/24. Gateway 192.168.1.1. DHCP scope .100-.200. Server at 192.168.1.10.
- No VLANs.
- VPN: SonicWall SSL VPN available for the bookkeeper to use at home. Rarely used.

## Servers and line-of-business apps

| Device | Role | Notes |
|---|---|---|
| OMG-SRV01 | File server, QuickBooks hosting, scale program database | Windows Server 2016, Dell PowerEdge T140. End of life January 2027, see Gotchas. |

- Grain scale software (the scale program): client/server. Server component runs on OMG-SRV01. The scale house PC `OMG-WS-SCALE1` talks to the weighbridge indicator over a serial-to-ethernet adapter at 192.168.1.40. The vendor is Plainfield Scale Systems (fictional).
- QuickBooks Desktop Enterprise: company file on OMG-SRV01 (`D:\QB`). Used by Ruth Ann and Carol. Multi-user mode.
- Farm supply POS: runs inside QuickBooks via a plugin, with a barcode scanner and receipt printer at the counter.
- Microsoft Office: Office 2019 on most PCs, not on M365. Needs verification.
- Weather and futures price screens run in a browser on the scale house PC. Tommy keeps them open all day.

## Microsoft 365 / Google tenant notes

- Email is Microsoft 365 Exchange Online only (Business Basic, 10 licenses). The rest of the staff share mailboxes or have no email.
- Tenant: oldmillgrain.onmicrosoft.com. Primary domain oldmillgrain.example.
- MFA: on for Dale and Ruth Ann. Others not enforced. Needs verification.
- No Intune. No Conditional Access.
- Domain registrar is under Dale's own account. We have DNS access via a delegate login, see vault.

## Backup

- Cove Data Protection on OMG-SRV01: nightly, 30 day retention, cloud only. No local copy.
- Last confirmed restore test: not documented. Need to run one before next harvest.
- QuickBooks company file backups also go to a USB drive each Friday, handled by Ruth Ann. We have no visibility into that.
- Workstations: not backed up. Files should be on the server.
- Scale program has its own nightly export to `D:\ScaleExports`, picked up by the Cove job.

## Printers, scanners, and other devices

| Device | Location | IP | Notes |
|---|---|---|---|
| Brother MFC-L8900 | Office | 192.168.1.50 | Scan to email via the server relay. Often flaky. |
| Epson TM-T88 receipt printer | Store counter | USB | Tied to the POS PC. |
| Zebra ticket printer | Scale house | 192.168.1.41 | Prints scale tickets, labels. Do not change the IP. |
| Weighbridge indicator | Scale house | 192.168.1.40 | Vendor managed. Never touch. |
| Barcode scanner | Store | USB | Standard, wired. |

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Chesapeake Prairie Wireless | Support | 410-555-0190 | Account holder is Dale. |
| Plainfield Scale Systems | Marty Voss | 410-555-0191 | Scale program and indicator. Phone support only, they will not remote in without Tommy there. |
| Intuit reseller | Through Ruth Ann | n/a | QuickBooks annual renewal. |
| Scale calibration inspector | State weights and measures office | n/a | Annual certification. Not ours. |

## Gotchas / tribal knowledge

1. Never reboot OMG-SRV01 during harvest or when the scale house is open. If a ticket is being weighed it breaks the ticket sequence and Tommy has to rebuild it by hand.
2. The scale program stops if the server IP changes. Server is fixed at 192.168.1.10. If DHCP ever hands out something else, the weigh station PC loses the database.
3. QuickBooks company file gets "unable to open" if Windows search indexing runs on `D:\QB`. Index is disabled, do not re-enable.
4. Scale house PC has an old serial adapter driver. Do not let Windows Update replace it.
5. The Brother scanner only sends mail on port 465 to our SMTP relay. Standard 587 is blocked by the SonicWall rule.
6. The ISP radio loses sync in a thunderstorm. Rebooting the PoE injector helps maybe half the time.
7. Dale likes to be called, not emailed, for anything he has to approve.
8. Server is old and Windows Server 2016 is near end of life. A replacement quote is on Casey's list.

## Credential references (vault paths only)

- Vault: old-mill-grain-and-supply/firewall-admin
- Vault: old-mill-grain-and-supply/wifi-psk
- Vault: old-mill-grain-and-supply/domain-registrar
- Vault: old-mill-grain-and-supply/isp-portal
- Vault: old-mill-grain-and-supply/m365-global-admin-breakglass
- Vault: old-mill-grain-and-supply/backup-appliance (Cove console)
- Vault: old-mill-grain-and-supply/lob-app-admin (scale program admin, QuickBooks admin)
- Vault: old-mill-grain-and-supply/printer-admin

## Change log

- 2025-06-09: Reviewed doc, added Gotchas 5 and 6, confirmed server IP. Sam Okafor. T-24188.
- 2025-03-18: Replaced scale house AP, moved to weatherproof enclosure. Sam Okafor. T-23895.
- 2024-12-02: Proposed cellular failover, client declined. Casey Morgan. T-23611.
- 2024-09-10: Added Cove job for D:\ScaleExports. Alex Rivera. T-23402.
- 2024-04-22: Initial onboarding doc written. Sam Okafor. P-0301.

# Assateague Outfitters

owner: Sam Okafor
last_reviewed: 2025-03-27
tags: retail, time-and-materials, pos, berlin-md, no-monitoring, stale
client_id: 1015
slug: assateague-outfitters
core_plan: none (time and materials)
service_plans: Hosted Website Plan
industry: Retail
employees: 10

## Overview

Outdoor and fishing gear shop in downtown Berlin. 10 people: owner, store manager, 7 sales staff (mix of full and part time), and a seasonal stock person. One storefront, no server. Busiest from May through October and the week before Thanksgiving.

Tools: Lightspeed-style cloud POS on two registers, QuickBooks Online (owner and bookkeeper, done from the owner's own laptop), and a back office PC for inventory and ordering.

This file is thin on purpose, we only see them when something breaks. Needs verification on almost everything below.

## Service plans and contract notes

- Core plan: none (time and materials). No monthly fee, billed per Accelo ticket.
- Add-ons: Hosted Website Plan.
- First response: P1 4 business hours, P2 next business day, P3/P4 best effort.
- No monitoring, no patch management, no after-hours unless Casey Morgan agrees per call.
- N-central agent is installed on only some machines (back office PC and one register). The owner's laptop and the second register were never enrolled. Which ones have the agent: needs verification, check N-central device list for `AO-` names.
- Client declines managed upgrades every year. Casey has the last quote.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Walt Brennerman (Owner) | 410-555-0101 | walt@assateagueoutfitters.example |
| Billing | Walt Brennerman | 410-555-0101 | same |
| After-hours | not documented yet | | |
| Store manager | Kayla Dempsey | 410-555-0126 | kayla@assateagueoutfitters.example |

## Sites and addresses

- Store: 14 Main Street, Berlin, MD 21811.
- Hours: Mon-Sat 9:00-6:00, Sun 10:00-4:00, summer hours extend to 8:00 pm Fri and Sat.
- Access: front door during business hours. Back door for deliveries. Alarm code is with Walt, ask him. Not documented.

## Internet and circuits

- ISP: Bayline Broadband business cable, 100/10. Account number not documented yet.
- Static IP: none.
- Modem is in the back stock room next to the router. Powered via a power strip that also runs the stock room fridge. Check if someone has pulled the plug.

## Network

- Router: consumer Wi-Fi router (brand needs verification), not managed by us. Admin password is Walt's. We do not hold it.
- Wi-Fi SSID `AssateagueStore`, one network for everything including the POS. Needs verification of PSK location.
- No VLANs, no VPN.
- The two POS registers connect to Wi-Fi, not wired.

## Servers and line-of-business apps

- No servers.
- POS: cloud POS service with card reader hardware (vendor supplied). The vendor owns the terminal firmware and support. Do not touch.
- QuickBooks Online: cloud, runs in a browser.
- Back office PC `AO-WS-BACK` runs inventory spreadsheets, vendor ordering sites, and label printing.

## Microsoft 365 / Google tenant notes

- Email: Walt uses a Google Workspace Business Starter account at his own domain. We have no admin access. Not documented further.
- No M365 tenant that we know of. Needs verification.

## Backup

- None provided by us.
- Walt says he backs up the back office PC to a USB drive "sometimes." Treat as no backup.

## Printers, scanners, and other devices

- Dymo label printer and a Brother laser printer at the back office PC. IPs and drivers not documented.
- Receipt printers at the registers belong to the POS vendor kit.
- Security cameras: installed by someone else, not ours.

## Vendor contacts

- Bayline Broadband: 410-555-0163.
- POS vendor support: number on a sticker on each register.
- Everything else: not documented yet.

## Gotchas / tribal knowledge

- Walt will call and say "the internet is down." Nine times out of ten the modem power strip is switched off. Ask first.
- Register 2 drops off Wi-Fi at the far end of the store when the dehumidifier is on.
- Never leave the store with a ticket open without telling Kayla.
- Pay by check or card on file only, bill after the visit.

## Credential references (vault paths only)

- Vault: assateague-outfitters/wifi-psk (may not exist)
- Vault: assateague-outfitters/isp-portal (may be out of date)
- Router admin: not in the vault, owned by client

## Change log

- 2025-03-27: Reviewed after replacing the back office PC. Sam Okafor. T-24002.
- 2024-10-14: Register 2 Wi-Fi fix, moved AP closer. Sam Okafor. T-23455.
- 2024-05-06: Initial doc created. Jordan Blake.

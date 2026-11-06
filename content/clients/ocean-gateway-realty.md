# Ocean Gateway Realty

owner: Jordan Blake
last_reviewed: 2025-04-22
tags: real-estate, omni-basic, byod, ocean-city-md, stale
client_id: 1012
slug: ocean-gateway-realty
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Email Management, Hosted Website Plan
industry: Real Estate
employees: 19

## Overview

Residential and vacation rental sales brokerage on the boardwalk end of Ocean City. 19 people: broker/owner, 2 office staff, 16 agents. Agents are independent contractors and mostly use their own laptops, phones, and tablets (see Gotchas). Office staff have company PCs. Busy season is May to September, slow in winter.

Tools: MLS portal (browser), dotloop for contracts, Canva, M365 for email only. No server.

Needs verification: employee count was 17 in the original onboarding, 19 per the 2026 contract renewal.

## Service plans and contract notes

- Core plan: Omni+ Basic. Accelo contract C-1012-A.
- Add-ons: Email Management, Hosted Website Plan.
- First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Only company-owned devices are covered (2 office PCs, 1 conference room PC, router). Agent personal devices are NOT covered by the agreement. Jordan has been helping with them anyway as a courtesy. Check with Casey Morgan before spending more than 15 minutes on one.
- Cove Data Protection (cloud only) on the office PCs. No Datto.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Denise Carlisle (Broker/Owner) | 302-555-0134 | denise.carlisle@oceangatewayrealty.example |
| Billing | Denise Carlisle | 302-555-0134 | same as above |
| After-hours | Denise Carlisle (cell) | 302-555-0135 | not documented yet, confirm |
| Office manager | Trish Navarro | 302-555-0136 | trish.navarro@oceangatewayrealty.example |

## Sites and addresses

- Main office: 2201 Baltimore Avenue, Suite 3, Ocean City, MD 21842.
- Hours: Mon-Sat 9:00-5:00 in season, Mon-Fri 9:00-4:00 off season.
- Access: ground floor suite. Landlord controls the building door. Access notes: not documented yet.

## Internet and circuits

- ISP: Bayline Broadband business cable, 200/20. Account number not documented yet.
- Static IP: none, dynamic.
- Modem in the supply closet behind the copier. Router is a consumer-grade Wi-Fi router the landlord provided? Needs verification, we may have replaced it.

## Network

- Firewall: not documented yet. Possibly a UniFi Dream Machine (needs verification).
- Wi-Fi: one SSID for staff `OGR-Office`, one for guests/agents `OGR-Agents` (open to anyone with the PSK). Both are on the same flat network as far as we know.
- VLANs: none documented.
- DHCP: router. Scope not documented yet.
- VPN: none.

## Servers and line-of-business apps

- Servers: none.
- Agent tools: MLS (browser), dotloop, ShowingTime, DocuSign. All cloud, none managed by us.
- Office staff use QuickBooks Online (cloud) through Trish.
- Shared files are in OneDrive/SharePoint. Folder structure is a mess, ask Trish.

## Microsoft 365 / Google tenant notes

- M365 tenant: oceangatewayrealty.onmicrosoft.com. 6 Business Basic licenses (broker, office staff, shared). Agents use their own personal or brokerage email, NOT M365.
- Agents at oceangatewayrealty.example addresses: some are on Gmail forwarding. Needs verification.
- MFA: on for admin accounts only. Others not documented.

## Backup

- Cove Data Protection on the 2 office PCs (Trish and front desk). Last verified restore: never tested.
- M365 backup: none. No Datto SaaS Protection (Omni+ Basic does not include it).

## Printers, scanners, and other devices

- One Canon imageRunner copier (front office). Scan to email is flaky, see Gotchas.
- Printer IP not documented yet.

## Vendor contacts

- Bayline Broadband: support desk 410-555-0174. Account PIN not on file.
- Canon dealer: Chesapeake Office Systems, 800-555-0197.
- Everything else: not documented yet.

## Gotchas / tribal knowledge

- Agents bring their own laptops and phones and ask us to "just connect them." They are not enrolled in anything. N-central agent is on company PCs only. We have no visibility into agent devices.
- Two agents had SentinelOne installed by mistake in 2024 (someone ran the wrong installer). Check N-central before assuming a personal laptop is managed.
- Copier scan-to-email breaks every time Denise changes her M365 password.
- Summer: do not schedule any work Fri-Sun of July and August. Call Denise first.

## Credential references (vault paths only)

- Vault: ocean-gateway-realty/m365-global-admin-breakglass
- Vault: ocean-gateway-realty/isp-portal (may be out of date)
- Vault: ocean-gateway-realty/wifi-psk
- Vault: ocean-gateway-realty/printer-admin
- Firewall/router admin: not in the vault yet

## Change log

- 2025-04-22: Added Trish as office contact, updated agent device notes. Jordan Blake. T-24016.
- 2025-01-15: Replaced front desk PC. Sam Okafor. T-23771.
- 2024-06-03: Initial onboarding doc written from Passportal export. Jordan Blake.

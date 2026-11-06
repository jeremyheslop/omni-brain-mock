# Heron Neck Insurance Group

owner: Alex Rivera
last_reviewed: 2025-10-14
tags: insurance, agency-management, applied-epic, two-sites, two-phone-systems, ringcentral, mitel, omni-proactive, berlin
client_id: 1004
slug: heron-neck-insurance-group
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management
industry: Insurance
employees: 22

## Overview

Heron Neck Insurance Group is an independent insurance agency with 22 staff, headquartered in Berlin, MD. Personal lines, commercial lines, a small benefits book, and a flood/wind specialty desk that gets very busy before and after storm season. 17 people sit in the Berlin main office and 5 sit in a satellite office in Snow Hill, MD that came with the 2022 purchase of Kellam Insurance Services.

Because of that acquisition, the firm runs **two phone systems**: RingCentral (cloud) in Berlin, and a legacy Mitel MiVoice Business on-prem system in Snow Hill. They talk to each other only through the public phone network. Extension dialing between sites does not work. Leadership has talked about merging them since 2023. Nothing is scheduled.

Agency management system is Applied Epic, hosted by Applied. Quoting uses EZLynx. Carriers are accessed by web portals and by Applied's download/upload interface. Almost nothing runs locally besides file shares and scan workflows.

Client since 2020. Moved to Omni+ Proactive in January 2022 right before the acquisition.

## Service plans and contract notes

- Core plan: Omni+ Proactive. First response: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management.
- Contract renews January 1. Casey Morgan handles renewal in October.
- Onsite: one scheduled visit per quarter, alternating Berlin and Snow Hill. Sam Okafor owns this. Extra onsite visits are billed.
- Includes N-central monitoring and patching, SentinelOne, DNSFilter, Datto SIRIS and SaaS Protection, help desk.
- Phones are NOT in scope. We manage the network and VLANs. RingCentral and the Mitel are managed by their vendors (see Vendor contacts). We do handle the "is it the network or the phone" triage.
- Applied Epic issues go to Applied support. We cover connectivity and the local client.
- Storm season (June 1 to Nov 30) tickets: the client expects fast P1 and P2 handling when the flood desk is slammed. Treat Epic or internet outage as P1 any time a named storm is within 3 days.
- Billing contact wants a PO number on every invoice. Naomi in accounting sets the number, we put it in the Accelo contract notes.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary (agency principal) | Walter Kellerman | 410-555-0192 | walter@heronneckinsurance.example |
| Billing | Tamsin Rowe (accounting) | 410-555-0193 | tamsin@heronneckinsurance.example |
| After-hours | Walter Kellerman (cell) | 410-555-0194 | walter@heronneckinsurance.example |
| Office manager (Berlin) | Fatima Abdullahi | 410-555-0195 | fatima@heronneckinsurance.example |
| Snow Hill branch lead | Dennis Pruett-Kellam | 410-555-0196 | dennis@heronneckinsurance.example |
| Account manager (key user) | Lucinda Vasquez | 410-555-0197 | lucinda@heronneckinsurance.example |

- Fatima handles everyday requests and is the best first call. She knows the network closet layout.
- Dennis is the only person at Snow Hill who will touch the Mitel handset programming and he does it wrong sometimes. Do not let him reset the voicemail PINs without a ticket.
- Walter wants an email summary for any outage longer than one hour. Casey sends it.

## Sites and addresses

- Berlin HQ: 112 Harrison Avenue, Suite A, Berlin, MD 21811 (fictional). Single-story building, ground floor. 17 staff, a reception area, a small conference room.
- Berlin hours: Mon-Fri 8:30-5:00. Storm days: office closes, calls forward to cell phones through RingCentral.
- Snow Hill branch: 38 Green Street, Snow Hill, MD 21863 (fictional). Two rooms and a back closet. 5 staff.
- Snow Hill hours: Mon-Fri 9:00-4:30.
- Access, Berlin: front door unlocked in business hours, after hours key from Fatima. Network rack is in the back utility room, next to the water heater (see Gotchas).
- Access, Snow Hill: a keypad door. Dennis has the code. Closet is behind the copier.

## Internet and circuits

| Site | ISP | Circuit | Static IP | Notes |
|---|---|---|---|---|
| Berlin | Delmarva Link Fiber | 500/500 fiber | 192.0.2.61/29 | Account ref DLF-39140-2 (fictional) |
| Berlin | Bayline Broadband | 200/20 cable | dynamic | Failover on WAN2 |
| Snow Hill | Bayline Broadband | 150/15 cable | 198.51.100.140 | Account ref BB-80915 (fictional) |

- Berlin ONT is in the utility room, mounted high on the left wall. Cable modem is on the shelf below.
- Snow Hill has no failover circuit. Dennis is told to use phone hotspots if it drops. Needs verification: a quote for LTE failover was sent in 2025, outcome unknown.
- Circuit outage procedure is `sops/35-isp-outage-troubleshooting.md`. For Berlin, check failover status in FortiGate first, then call Delmarva Link.
- ISP portals are in the vault.

## Network

- Berlin firewall: FortiGate 70F (HNIG-FW01), FortiOS 7.2.x. Dual WAN failover.
- Snow Hill firewall: FortiGate 40F (HNIG-FW02), FortiOS 7.2.x.
- Site-to-site: IPsec VPN tunnel between HNIG-FW01 and HNIG-FW02. Snow Hill staff reach the file server and printers over the tunnel. If the tunnel drops they can't open scanned documents but Epic keeps working (cloud).
- Switching, Berlin: two UniFi 24-port PoE switches (HNIG-SW01, HNIG-SW02). Snow Hill: one UniFi 8-port PoE switch (HNIG-SW03).
- Wi-Fi: Berlin has three UniFi U6 Lite APs. Snow Hill has one. SSID `HeronNeckStaff` (WPA2/WPA3) and `HeronNeckGuest` (isolated).

| VLAN | Name | Subnet | Site | Purpose |
|---|---|---|---|---|
| 1 | Management | 10.40.1.0/24 | Berlin | Network gear |
| 10 | Staff | 10.40.10.0/24 | Berlin | Workstations, server |
| 20 | Voice (RingCentral) | 10.40.20.0/24 | Berlin | RingCentral desk phones, QoS tagged |
| 30 | Guest | 10.40.30.0/24 | Berlin | Guest Wi-Fi |
| 50 | Staff | 10.41.10.0/24 | Snow Hill | Workstations, printer |
| 60 | Voice (Mitel) | 10.41.60.0/24 | Snow Hill | Mitel IP phones and PBX |

- DHCP from each FortiGate. Berlin staff scope 10.40.10.100-10.40.10.220. Snow Hill staff scope 10.41.10.100-10.41.10.160.
- DNS: HNIG-SRV01 (10.40.10.5) is the domain controller and DNS server. The Snow Hill clients also use it over the tunnel. Internal domain `heronneck.local`.
- Client VPN: FortiClient IPsec for the principal and two producers who work from home. MFA through FortiToken Mobile. See `sops/19-vpn-user-setup.md`.
- Firewall rule requests per `sops/18-firewall-rule-change-request.md`. SIP ALG is OFF on both FortiGates. Do not turn it on. See Gotchas.

## Servers and line-of-business apps

| Device | Role | OS | Notes |
|---|---|---|---|
| HNIG-SRV01 | DC, DNS, file server, print server | Windows Server 2022 | Dell PowerEdge T350, 32 GB RAM |
| HNIG-SRV02 | Scan-to-folder and document import host | Windows Server 2019 VM | Hyper-V guest on SRV01 |

- Applied Epic: hosted by Applied. Staff use the Epic desktop client installed on every PC plus the Outlook add-in. Connectivity depends on the firewall allowing Applied's cloud endpoints. Epic client updates are pushed by Applied automatically; do not block them.
- EZLynx: browser based comparative rater. Nothing local.
- Carrier portals: browser, with shared and personal logins managed by the agency. Bookmarks are pushed through Edge policy.
- Document workflow: scanners at both sites drop PDFs into `\\HNIG-SRV01\Scans`. SRV02 runs a watch script that imports files to Epic attachments through the Epic scan folder. If attachments stop appearing in Epic, check SRV02's scheduled task `EpicScanImport` first.
- Shared drives: `K:\Agency` (forms, templates, ACORD PDFs), `L:\Accounting` (restricted to Tamsin and Walter).
- DocuSign and Adobe Sign: used heavily, cloud.
- Reboots follow `sops/25-server-reboot-window.md`. Window is Sunday 6:00 AM. Not during storm events.

## Microsoft 365 / Google tenant notes

- Tenant: heronneckinsurance.example on Microsoft 365 Business Premium. 23 licenses (22 users plus a shared mailbox `claims@` with a license for a mobile device).
- MFA via Conditional Access with Authenticator. Producers use number matching on personal phones. Phone swaps per `sops/32-new-phone-mfa-device-swap.md`.
- Shared mailboxes: `service@`, `certificates@` (certificates of insurance requests, high volume), `claims@`. Auto-reply on `certificates@` is customized, do not overwrite it.
- Outlook for Mac is used by one producer (Wes Dunleavy). The only Mac in the firm. N-central does not manage it fully; SentinelOne is installed. Needs verification of macOS version and update status.
- Retention: 7 year retention on `service@` and `certificates@`. The agency's E&O carrier asks about it every year.
- License changes via `sops/14-m365-license-changes.md`.

## Backup

- Datto SIRIS (HNIG-BK01) backs up SRV01 and the SRV02 VM. Hourly in business hours, nightly verified screenshot. Cloud replication nightly.
- Datto SaaS Protection covers all M365 mailboxes, OneDrive, and shared mailboxes.
- Retention: local 30 days, cloud 1 year. The firm keeps client records in Epic, so local retention was scoped to just file shares and scan input.
- Daily check per `sops/08-daily-backup-check.md`. Last restore test: 2025-09-02 (T-24160) file-level plus VM boot test.
- Snow Hill has no local server or backup. Its endpoints are not backed up.
- Needs verification: whether the ACORD template folder on a partner's laptop is backed up anywhere.

## Printers, scanners, and other devices

| Device | Model | Address | Notes |
|---|---|---|---|
| HNIG-PR01 | Canon imageRUNNER ADVANCE C3926i | 10.40.10.21 | Berlin main copier, scan to folder |
| HNIG-PR02 | HP LaserJet Pro M479fdw | 10.40.10.22 | Berlin back office |
| HNIG-PR03 | Canon imageRUNNER 2745i | 10.41.10.20 | Snow Hill, scans over the tunnel |
| HNIG-SC01 | Fujitsu fi-7160 | USB to HNIG-WS-009 | Certificates desk |

- Phone hardware: Berlin uses Poly VVX desk phones with RingCentral. Snow Hill uses Mitel 6900 series phones. Do not swap handsets between sites.
- Workstations named HNIG-WS-001 through HNIG-WS-022, laptops HNIG-LT-001 through 004 for producers.
- Berlin UPS: APC Smart-UPS 1500 in the rack. Snow Hill has a small APC Back-UPS for modem and firewall only. The Mitel PBX is on its own UPS.

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Support desk | 410-555-0150 | Berlin primary |
| Bayline Broadband | Business support | 410-555-0151 | Berlin failover and Snow Hill |
| RingCentral | Business support | on account portal | Berlin phones |
| Shoreline Telecom (Mitel dealer) | Hank Dufresne | 410-555-0168 | Snow Hill Mitel service |
| Applied Systems | Epic support | on client portal | Ask for "Hosted Epic" |
| Eastside Copy Solutions | Paula Marchetti | 410-555-0169 | Canon service |

## Gotchas / tribal knowledge

1. **Two phone systems, two different owners.** If Snow Hill says "phones are down", call Hank at Shoreline Telecom after confirming the switch and VLAN 60 are up. If Berlin says it, check VLAN 20 and the RingCentral status page first. A network problem looks the same as a phone problem to staff.
2. Extension dialing between Berlin and Snow Hill does not work. Staff dial the 10-digit number. Do not promise to fix this, it needs the merge project.
3. SIP ALG must stay off on both FortiGates. When it was on in 2023 RingCentral calls dropped audio after 30 seconds (T-21894). Firmware updates can reset it, so check after any FortiOS upgrade.
4. RingCentral E911 is registered by address. The Berlin phones have the Harrison Avenue address. If anyone moves a handset to the Snow Hill office, E911 will be wrong. Tell Fatima.
5. The Berlin network rack is next to the water heater. It trips the utility room breaker occasionally. If the whole rack is dead, check the breaker panel in the hallway before dispatching Sam.
6. Do not reboot HNIG-SRV01 between 9:00 and 11:00 or 1:00 and 3:00. Policy renewal batches run then and the scan import fails halfway.
7. Month-end (last 3 business days) is renewal crunch. Avoid changes. Tamsin will escalate fast if the printers go down.
8. Storm season runbook: when a named storm is forecast, Sam confirms UPS status and the Datto cloud sync, Alex checks on-call coverage. Walter forwards the office phones. Casey sends a short status note on day 1 and day 2.
9. The Snow Hill copier scans over the tunnel. If scans fail and the tunnel is up, check the Snow Hill FortiGate's local-in policy for SMB. It was blocked once after a firmware change.
10. Wes (the Mac user) forgets his MFA phone at home. He's the most frequent `sops/12-mfa-reset.md` ticket. Be nice.
11. The `certificates@` mailbox gets 150 emails on a bad day. Do not enable aggressive spam filtering on it without asking Lucinda, real COI requests will be quarantined.

## Credential references (vault paths only)

- Vault: heron-neck-insurance-group/firewall-admin (Berlin FortiGate)
- Vault: heron-neck-insurance-group/firewall-admin-snowhill
- Vault: heron-neck-insurance-group/switch-admin
- Vault: heron-neck-insurance-group/wifi-psk
- Vault: heron-neck-insurance-group/domain-registrar
- Vault: heron-neck-insurance-group/m365-global-admin-breakglass
- Vault: heron-neck-insurance-group/isp-portal (both ISPs)
- Vault: heron-neck-insurance-group/backup-appliance
- Vault: heron-neck-insurance-group/lob-app-admin (Epic admin contact is Fatima, no local admin account)
- Vault: heron-neck-insurance-group/printer-admin
- Vault: heron-neck-insurance-group/mitel-admin

## Change log

- 2025-10-14 Alex Rivera: Reviewed doc. Added storm runbook and SIP ALG note (T-24470).
- 2025-09-02 Sam Okafor: Quarterly visit at Berlin. Restore test with Alex (T-24160).
- 2025-06-17 Sam Okafor: Moved Berlin switch ports for new conference room drop.
- 2025-03-11 Alex Rivera: FortiOS 7.2 update on both firewalls. Re-checked SIP ALG (T-23544).
- 2023-09-20 Alex Rivera: Fixed RingCentral audio drop by disabling SIP ALG (T-21894).
- 2022-02-07 Casey Morgan: Added Snow Hill after acquisition, built IPsec tunnel with Alex (P-0412).
- 2022-01-03 Casey Morgan: Upgraded contract to Omni+ Proactive.

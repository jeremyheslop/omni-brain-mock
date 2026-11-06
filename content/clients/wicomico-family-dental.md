# Wicomico Family Dental

owner: Sam Okafor
last_reviewed: 2026-08-27
tags: dental, hipaa, dentrix, dexis, imaging, xray, pano, omni-proactive, salisbury, baa
client_id: 1005
slug: wicomico-family-dental
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Advanced Security, Omni+ Server, Server Backup
industry: Healthcare
employees: 18

## Overview

Wicomico Family Dental is a general dentistry practice in Salisbury, MD with 18 staff: 2 dentists, 4 hygienists, 5 dental assistants, 3 front desk, 1 billing/insurance coordinator, 1 office manager, 2 part-timers on the sterilization and scheduling side (counted in headcount). 10 operatories (8 in use daily, 2 for the second dentist's overflow days).

The practice runs Dentrix (G-series, on-prem) with an SQL database on the local server, Dexis imaging software and sensors, a panoramic X-ray unit, and a handful of dedicated "X-ray PCs" that sit in the operatories. HIPAA applies. OmniTechPro signed a Business Associate Agreement (BAA) with the practice in 2023. The BAA is stored in Accelo under the client record, not in this doc.

This is a hardware-heavy client. Sam Okafor does most of the visits. The server is the most important device in the building: if it is down, nobody can see the schedule, chart, or images.

Client since 2021. Moved from time and materials to Omni+ Proactive in 2023 when they added the second dentist.

## Service plans and contract notes

- Core plan: Omni+ Proactive. First response: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup.
- Clinical downtime counts as P1: if Dentrix, the server, or imaging is unavailable and patients are in chairs, open it as P1 even if the caller says "just slow".
- Contract renews September 1. Casey Morgan handles renewal in July.
- Onsite visit included: one scheduled visit per quarter (Sam). Scheduled on Fridays when the office is open but half-booked, or on a Wednesday afternoon when the office is closed (see hours).
- Includes N-central monitoring, patching, SentinelOne, DNSFilter, Datto SIRIS plus SaaS Protection, help desk.
- Not included: Dentrix support (Henry Schein One / vendor line), Dexis support (vendor), sensor replacement, X-ray equipment service.
- HIPAA: the practice does its own annual risk assessment. We provide a technical controls summary each April (Alex Rivera drafts, Casey signs).
- Incident rule: anything that might expose patient data (lost laptop, wrong email recipient, suspected ransomware) goes to Casey Morgan immediately and to the office manager. See `sops/34-ransomware-response.md` and `sops/11-suspected-compromised-account.md`.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary (office manager) | Rosalind Chambers | 302-555-0175 | rosalind@wicomicodental.example |
| Billing | Marisol Dutton (insurance/billing) | 302-555-0176 | marisol@wicomicodental.example |
| After-hours | Dr. Elias Brandt (owner dentist) | 302-555-0177 | dr.brandt@wicomicodental.example |
| Dentist (associate) | Dr. Priyanka Venkataraman | 302-555-0178 | dr.venkat@wicomicodental.example |
| Front desk | Front office line | 410-555-0170 | frontdesk@wicomicodental.example |
| Lead assistant (imaging super-user) | Tobias Greenleaf | 302-555-0179 | tobias@wicomicodental.example |

- Rosalind is the best first call for anything non-emergency. Dr. Brandt only wants calls for downtime that affects patients.
- Tobias knows more about the sensors than anyone. Ask him which operatory and which sensor serial.

## Sites and addresses

- Single office: 906 Riverside Drive, Suite 110, Salisbury, MD 21801 (fictional). Ground-floor suite in a medical office building.
- Hours: Mon, Tue, Thu 7:30-4:30. Wed 7:30-12:30. Fri 7:30-3:00. Closed weekends. The office is closed Wednesday afternoon, so that is the preferred time for server work.
- Access: front door by key. After-hours entry requires Rosalind or Dr. Brandt (alarm code). Do not ask for the alarm code in an email.
- Server closet: a locked cabinet in the sterilization hallway. Key on Rosalind's ring, spare in the office manager's desk.
- Parking: shared lot. Sam parks in the loading spot by the side door with a note in the window.

## Internet and circuits

- Primary: Delmarva Link Fiber, 300/300 Mbps business fiber. Account ref DLF-42906-1 (fictional).
- Static IP: 192.0.2.87/30 on the FortiGate WAN1.
- Backup: Bayline Broadband business cable, 100/10 Mbps, dynamic IP, WAN2 failover. Added 2024 after a fiber outage during a full schedule (T-22013).
- ONT and cable modem are in the same locked cabinet as the server, top shelf.
- Outage procedure is `sops/35-isp-outage-troubleshooting.md`. Dentrix is on-prem so a short internet outage is survivable. E-claims, patient texting, and the phone system are not.

## Network

- Firewall: FortiGate 60F (WFD-FW01), FortiOS 7.4.x, dual WAN failover.
- Switching: Ubiquiti UniFi 48-port PoE switch (WFD-SW01) in the cabinet, plus four small 8-port UniFi switches in operatory clusters (WFD-SW02 through WFD-SW05).
- Wi-Fi: four UniFi U6 Lite APs. SSID `WicomicoStaff` (WPA2/WPA3), `WicomicoGuest` (waiting room, isolated, 4 hour captive portal).
- VLANs are segmented on purpose. Imaging devices are not allowed on the staff VLAN.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 1 | Management | 10.50.1.0/24 | Network gear |
| 10 | Staff | 10.50.10.0/24 | Front desk, back office, server |
| 20 | Clinical | 10.50.20.0/24 | Operatory PCs, X-ray PCs, imaging |
| 30 | Guest | 10.50.30.0/24 | Waiting room Wi-Fi |
| 40 | VoIP | 10.50.40.0/24 | Desk phones |
| 99 | Legacy | 10.50.99.0/28 | Pano PC only, no internet |

- DHCP: FortiGate. Staff scope 10.50.10.100-10.50.10.200. Clinical scope 10.50.20.100-10.50.20.200. Server and imaging devices have reservations or static IPs below .100.
- DNS: WFD-SRV01 (10.50.10.5) is the domain controller and DNS. Internal domain `wicomicodental.local`. Forwarders to DNSFilter.
- VPN: FortiClient SSL VPN for Dr. Brandt and Rosalind only (chart review after hours). MFA via FortiToken Mobile.
- Firewall changes per `sops/18-firewall-rule-change-request.md`. Rosalind approves.

## Servers and line-of-business apps

| Device | Role | OS | Notes |
|---|---|---|---|
| WFD-SRV01 | DC, Dentrix SQL host, file server | Windows Server 2019 | Dell PowerEdge T350, 64 GB RAM, RAID 10 SSD |
| WFD-IMG01 | Imaging storage (Dexis database and image store) | Windows Server 2016 | Older Dell T340, 8 TB RAID 5, due for replacement 2027 |

- Dentrix G-series: client installed on all front desk and operatory PCs. Database on WFD-SRV01. Dentrix services must be up for the schedule to load. Updates come from the vendor and are applied by their installer tech or by Alex on a Wednesday afternoon.
- Dexis: imaging software on operatory PCs, X-ray PCs, and the front desk. Images stored on WFD-IMG01 under `\\WFD-IMG01\DexisImages`. The Dexis database is a separate SQL instance on WFD-IMG01.
- Dentrix/Dexis bridge: images show up in the Dentrix chart via a bridge. If images vanish from Dentrix but are still in Dexis, restart the bridge service on the operatory PC.
- Patient forms: tablets at the front desk (iPad check-in app). Cloud, vendor managed.
- E-claims: Dentrix e-claims through the vendor clearinghouse. Marisol uses it daily.
- Reboots follow `sops/25-server-reboot-window.md`. Window is Wednesday after 1:00 PM. Never during patient hours.

## Microsoft 365 / Google tenant notes

- Tenant: wicomicodental.example on Microsoft 365 Business Premium. 16 licenses. The sterilization and scheduling part-timers share two kiosk-style accounts without email.
- Exchange Online. Email encryption: message-level encryption is enabled for outbound mail containing PHI keywords (e.g. "SSN", "date of birth"). Do not turn this off.
- MFA via Conditional Access. Dentists use Authenticator. Front desk uses Authenticator too, with a registered second phone for Rosalind in case of a lost device.
- Shared mailbox: `frontdesk@` (3 front desk staff, Rosalind, Marisol).
- Teams is not used. Staff communicate with an intercom message system on the Dentrix client.
- Break-glass admin in the vault.

## Backup

- Datto SIRIS (WFD-BK01) backs up WFD-SRV01 and WFD-IMG01. Hourly in clinic hours, with a nightly verified screenshot. Cloud replication nightly. Image backups run slow because the Dexis store is big (about 2.1 TB).
- Datto SaaS Protection covers all M365 mailboxes and OneDrive.
- Retention: local 30 days, cloud 1 year. HIPAA requires 6 years for some records, but the clinical records live in Dentrix, which has its own export schedule. Needs verification with Rosalind on who exports.
- Restore tests: last full virtualization test 2026-03-18 (T-25062), Dentrix schedule opened. Image restore tested 2026-08-12 (T-25598). Daily check per `sops/08-daily-backup-check.md`.
- Dentrix also runs its own database backup nightly to `D:\DentrixBackups` on SRV01. Datto picks this up. This is the one Rosalind can restore from without us if the chart looks wrong.
- Workstations are not backed up. Nothing important should be local. Dexis image caches on operatory PCs do get deleted and rebuilt, so don't be surprised.

## Printers, scanners, and other devices

| Device | Model | Location | Address / connection | Notes |
|---|---|---|---|---|
| WFD-PR01 | HP LaserJet Pro M479fdw | Front desk | 10.50.10.21 | Insurance forms, scan to folder |
| WFD-PR02 | Brother HL-L8360CDW | Back office | 10.50.10.22 | Billing statements |
| WFD-PR03 | Zebra ZD421 | Front desk | USB to WFD-WS-002 | Label printer |
| Sensors | Dexis Titanium (8) | Operatories 1-8 | USB 3.0 to X-ray PC | One sensor per operatory |
| Pano | Planmeca ProMax | Room 9 | Network to WFD-XR-PANO | Legacy PC, see Gotchas |
| Intraoral cameras | USB cameras | Operatories 1-8 | USB to operatory PC | Cheap ones, replace every 3 years |

- X-ray PCs: WFD-XR-01 through WFD-XR-08 (one per operatory, each mounted on an arm, Windows 11 Pro, small form factor). WFD-XR-PANO is the pano PC. These are not the same machines as the operatory chairside workstations (WFD-OP-01 through 08).
- Front desk and office PCs: WFD-WS-001 to WFD-WS-005.
- UPS: APC Smart-UPS 1500 for server and imaging server. Individual small UPS units at the front desk. Sam tests each quarter.

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Support desk | 410-555-0150 | Primary circuit |
| Bayline Broadband | Business support | 410-555-0151 | Failover cable |
| Dentrix vendor support | Support line | on account page | Needs the practice ID, Rosalind has it |
| Dexis support | Support line | on account page | Sensor and software issues |
| Planmeca service | Field engineer Harlan Voss | 410-555-0179 | Pano service, calibrations |
| Seaboard Cloud Voice | Support desk | 410-555-0178 | Hosted phones |

## Gotchas / tribal knowledge

1. **Windows updates can break the Dexis sensor drivers.** On X-ray PCs the N-central patch policy is set to "security only, deferred 14 days, manual approval". Sam tests on WFD-XR-08 (the least used) before approving the rest. If a sensor stops being detected after a patch, uninstall the USB device in Device Manager and reconnect it, then restart the Dexis service.
2. The pano PC WFD-XR-PANO runs Windows 10 (the vendor will not certify later) and is on VLAN 99 with no internet. SentinelOne is installed with a locked-down policy that cannot call home, so alerts only appear when someone checks the console. It is on the EOL hardware list, see `sops/23-end-of-life-hardware.md`. Don't plug it into the staff VLAN to "just update it".
3. USB 3.0 sensors only work reliably on the rear USB ports of the X-ray PCs. Front ports cause intermittent captures. Tobias has put tape over the front ports. Leave the tape.
4. Never reboot WFD-SRV01 or WFD-IMG01 before 1:00 PM on a Wednesday. Even a "quick" reboot of the imaging server kills the Dexis acquisition session mid-patient and images may need retaking. That means more X-ray radiation for the patient, and the dentists take it seriously.
5. When Dentrix says "Cannot connect to database" the first suspect is the Dentrix SQL service on SRV01, not the network. Check `Services.msc` for the Dentrix SQL instance.
6. The waiting room TV uses the guest Wi-Fi. Once it loops on a dead stream and chews bandwidth. If the guest VLAN looks busy, check it.
7. Hygienists save appointment notes by habit to the local Desktop on the operatory PC. Those files are lost on a re-image. Warn Rosalind before any refresh and look for a stray Notes folder.
8. Rosalind will say "the computer is slow". Ask which room. Operatory 4's PC has a failing SSD (T-25601 open as of this review). Everything else is usually Dentrix indexing after hours.
9. The sterilization room has a small PC logging autoclave cycles for the state inspection. It is not on the list of managed devices. Don't wipe it. Treat as needs verification, and ask Rosalind who set it up.
10. HIPAA training attestation: Rosalind sometimes asks us to prove staff completed security training. We use a separate training platform; the report comes from there, not Accelo.

## Credential references (vault paths only)

- Vault: wicomico-family-dental/firewall-admin
- Vault: wicomico-family-dental/switch-admin
- Vault: wicomico-family-dental/wifi-psk
- Vault: wicomico-family-dental/domain-registrar
- Vault: wicomico-family-dental/m365-global-admin-breakglass
- Vault: wicomico-family-dental/isp-portal
- Vault: wicomico-family-dental/backup-appliance
- Vault: wicomico-family-dental/lob-app-admin (Dentrix SQL and Dexis admin)
- Vault: wicomico-family-dental/printer-admin
- Vault: wicomico-family-dental/pano-pc-local-admin

## Change log

- 2026-08-27 Sam Okafor: Reviewed doc. Added Operatory 4 SSD note, recorded image restore test (T-25598).
- 2026-03-18 Alex Rivera: Full virtualization test of SRV01, Dentrix opened fine (T-25062).
- 2025-11-05 Sam Okafor: Replaced X-ray PC WFD-XR-03 after sensor errors (T-24733).
- 2025-07-23 Alex Rivera: Added VLAN 99 for the pano PC and moved it off the clinical VLAN (T-24301).
- 2024-06-11 Alex Rivera: Added cable failover on WAN2 (T-22013).
- 2023-09-08 Casey Morgan: Upgraded to Omni+ Proactive, signed BAA.
- 2021-10-04 Casey Morgan: Initial onboarding.

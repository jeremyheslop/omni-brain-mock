# Sandpiper Physical Therapy

owner: Sam Okafor
last_reviewed: 2026-05-06
tags: healthcare, physical-therapy, hipaa, emr, webpt, baa, ocean-pines, omni-basic
client_id: 1020
slug: sandpiper-physical-therapy
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Advanced Security, Server Backup, Omni+ Backup
industry: Healthcare
parent_company: Bayside Pediatric Therapy (1013)
employees: 17

## Overview
Outpatient physical therapy clinic in Ocean Pines, MD. 17 staff: 8 therapists, 3 PT assistants, 4 front desk and billing, 1 clinic director, 1 office manager. One location, one open gym floor, 6 treatment rooms with a workstation in each. The EMR is cloud based, so there is no server on site. Patient data lives in the EMR, in M365, and on a few exercise equipment PCs.

HIPAA applies. We have a signed BAA with Sandpiper (Casey holds the copy, filed in Accelo under the client record). Treat any request involving patient data, lost devices, or emailed PHI as a possible incident and follow the escalation notes below.

Related company: Sandpiper is a subsidiary of Bayside Pediatric Therapy (client 1013) and lists it as the Parent Company in Accelo. Contracts, networks and contacts are separate.

## Service plans and contract notes
- Core plan: Omni+ Basic. Accelo contract "Sandpiper Omni+ Basic Services".
- Add-ons: Omni+ Advanced Security, Server Backup, Omni+ Backup.
- First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Onsite visit by agreement twice a year (Sam, usually March and September), billed per visit.
- BAA renewal and HIPAA risk assessment: annual, done each spring. The last one was April 2026. Casey sends the completed report to Dr. Okonkwo.
- Contract renews April 1.
- The clinic is closed weekends. After-hours support is by request, at the after-hours rate, and in practice only for P1 (EMR login failures on a Monday morning count, so check Sunday evening if a patch went out).

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dr. Imani Okonkwo (Clinic Director) | 302-555-0165 | imani.okonkwo@sandpiperpt.example |
| Billing | Rhonda Scully (Billing Lead) | 302-555-0166 | rhonda.scully@sandpiperpt.example |
| After-hours | Dr. Imani Okonkwo (cell) | 302-555-0167 | imani.okonkwo@sandpiperpt.example |
| Office manager | Tess Alvarado | 302-555-0168 | tess.alvarado@sandpiperpt.example |
| HIPAA privacy officer | Tess Alvarado | 302-555-0168 | privacy@sandpiperpt.example |
| Lead therapist / EMR super user | Colin Dray, PT | 410-555-0125 | colin.dray@sandpiperpt.example |

Tess is the first call for day-to-day IT. Dr. Okonkwo for anything involving patient data exposure.

## Sites and addresses
- Single site: 11224 Coastal Highway, Suite 6, Ocean Pines, MD 21811. Hours Mon-Thu 7:00-6:00, Fri 7:00-3:00. Closed weekends.
- Strip-center unit. Customer parking in front, back door by the dumpsters is open to staff only 6:30 AM onward. Tess has a key, Sam has a key.
- Network closet is a locked cabinet in the supply room off the open gym. The cabinet key is on Tess's ring.
- Landlord is separate. Don't use the shared telecom room at the end of the building.

## Internet and circuits
| Item | Primary | Backup |
|---|---|---|
| ISP | Bayline Broadband | none |
| Type | 300/30 business cable | n/a |
| Static IP | 198.51.100.130/29 (firewall on .131) | n/a |
| Account ref | BB-77045 | n/a |

- Modem is in the supply room, mounted on the wall above the cabinet.
- No backup circuit. Quoted a cellular failover in 2025, Dr. Okonkwo declined. If the cable goes down, the EMR is unreachable and they have to chart on paper. See gotchas.
- Outage SOP: `sops/35-isp-outage-troubleshooting.md`.

## Network
- Firewall: Fortinet FortiGate 40F `SPT-FW01`. IPS and web filtering on. Logging kept 12 months for HIPAA.
- Switch: Ubiquiti UniFi 24-port PoE `SPT-SW01` plus an 8-port in the open gym. APs: UniFi U6 Pro x2 (staff and guest).
- VLANs below. Medical equipment PCs (e.g. the balance platform and the biofeedback unit) sit on the Devices VLAN with no internet except to the vendors' update sites.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 10 | Clinical | 10.70.10.0/24 | Therapist and front desk PCs, printers |
| 20 | Devices | 10.70.20.0/27 | Equipment PCs, limited internet |
| 30 | Voice | 10.70.30.0/26 | Desk phones |
| 40 | Guest | 10.70.40.0/24 | Patient and visitor Wi-Fi, isolated |
| 99 | Mgmt | 10.70.99.0/28 | Switch and AP management |

- DHCP from the FortiGate. DNS to DNSFilter. No domain controller, workstations are Entra joined and managed through Intune with N-central on top.
- Wi-Fi: `Sandpiper-Staff` (WPA2 PSK, clinical VLAN), `Sandpiper-Guest` (isolated, captive splash with terms). Guest SOP is `sops/20-wifi-guest-network.md`.
- VPN: FortiClient for the clinic director and billing lead only (2 users).

## Servers and line-of-business apps
- No servers.
- EMR: WebPT-style cloud EMR (documentation, scheduling, billing). Web only, browser must be Chrome or Edge. Colin is the super user and creates new accounts. We reset MFA only through `sops/12-mfa-reset.md`, with Tess approving by email.
- Billing clearinghouse: a web portal inside the EMR. Rhonda handles it. We do not.
- E-fax: cloud fax service tied to a shared mailbox `fax@sandpiperpt.example`.
- Exercise software: a patient home-exercise program web app, therapist logins only.
- 17 user PCs `SPT-WS-001` to `SPT-WS-017` (8 laptops, 9 desktops). Equipment PCs `SPT-EQ-01` to `SPT-EQ-03`.
- Screen privacy filters on the front desk monitors. Please don't remove them during hardware swaps.

## Microsoft 365 / Google tenant notes
- Tenant `sandpiperpt.example`, 17 Business Premium licenses, 2 shared mailboxes (`fax@`, `frontdesk@`).
- MFA required for all. Conditional Access blocks sign-in outside the US and blocks unmanaged devices from downloading from SharePoint.
- Email encryption: Office Message Encryption rule triggers on the word "[secure]" in the subject. Staff know to use it. Remind new hires.
- Datto SaaS Protection on all mailboxes and OneDrive/SharePoint.
- No PHI should be in Teams chats. Retention policy is on, but remind staff anyway.

## Backup
- Datto SIRIS appliance protects the three equipment PCs and the front desk PC image (the old scan station). Cloud-replicated.
- SaaS Protection covers M365.
- The EMR vendor handles its own backups. Our BAA language says so. Don't promise to restore EMR data.
- Daily check per `sops/08-daily-backup-check.md`. Restore test twice a year, last was 2026-03-24 (a OneDrive folder, passed).

## Printers, scanners, and other devices
- Brother-style color laser MFP at the front desk, scan-to-email via relay. Static IP 10.70.10.20.
- Second printer in the therapist workroom (mono laser), static 10.70.10.21.
- Label printer for patient wristband-style home program sheets, USB at the front desk.
- Signature pads (3) at check-in, USB, driver in the EMR's plugin. Needs the browser plugin reinstalled after Chrome major updates.
- Desk phones: 14 handsets from Tidewater Voice (fictional hosted VoIP), VLAN 30.
- Equipment PCs: `SPT-EQ-01` (balance platform), `SPT-EQ-02` (biofeedback), `SPT-EQ-03` (gait treadmill display). Vendor-supplied, do not install our software beyond the N-central agent without asking the vendor.

## Vendor contacts
| Vendor | What | Contact | Phone |
|---|---|---|---|
| Rapidstride Systems (WebPT-style EMR, fictional) | EMR | Support, ask for Yuki | 410-555-0131 |
| Bayline Broadband | Circuit | Business support | 410-555-0172 |
| Tidewater Voice | Phones | Support | 410-555-0177 |
| BalanceWorks | Balance platform | Technician line | 410-555-0132 |
| Datto | SIRIS / SaaS | Partner portal | n/a |

## Gotchas / tribal knowledge
1. If the internet drops, therapists chart on paper forms in the clipboard bin at the front desk. Do not tell Dr. Okonkwo "it will be back soon". Give a real ETA or say you don't know.
2. The signature pad plugin breaks after Chrome updates. Reinstall it from the EMR admin page (Colin knows where). Not a driver issue.
3. Front desk PC `SPT-WS-001` sleeps through the night and sometimes doesn't wake the scan station. Reboot fixes it.
4. Do not do patching reboots between 7:00 AM and 6:00 PM. The N-central window is Friday 3:30 PM, after close.
5. Anything where a patient name, DOB, or diagnosis shows up in a ticket or screenshot: strip it before saving. Our tickets are not a PHI system.
6. Lost or stolen laptop: lock via Intune, remote wipe, tell Casey right away, and Dr. Okonkwo gets a call within the hour. HIPAA clock is real. See `sops/34-ransomware-response.md` for the overall incident flow, but use the lost-device note in the client file first.
7. Balance platform PC `SPT-EQ-01` runs an old OS. It is on VLAN 20 and cannot be upgraded. Marked end-of-life in N-central. See `sops/23-end-of-life-hardware.md`.
8. Colin sometimes says "the EMR is down" when his personal login got locked. Check another user first.

## Credential references
- Vault: sandpiper-physical-therapy/firewall-admin
- Vault: sandpiper-physical-therapy/switch-admin (UniFi controller)
- Vault: sandpiper-physical-therapy/wifi-psk
- Vault: sandpiper-physical-therapy/m365-global-admin-breakglass
- Vault: sandpiper-physical-therapy/domain-registrar
- Vault: sandpiper-physical-therapy/isp-portal
- Vault: sandpiper-physical-therapy/backup-appliance
- Vault: sandpiper-physical-therapy/lob-app-admin (EMR admin, held by Colin, ours is read-only)
- Vault: sandpiper-physical-therapy/printer-admin

## Change log
- 2026-05-06 (Sam Okafor): Annual review after HIPAA risk assessment. T-24650.
- 2026-04-15 (Casey Morgan): BAA renewed, copy filed in Accelo.
- 2026-03-24 (Jordan Blake): Restore test, OneDrive folder, passed. T-24412.
- 2026-03-10 (Sam Okafor): Semiannual onsite. Replaced a front desk UPS. T-24380.
- 2025-11-18 (Alex Rivera): Added Devices VLAN rule to block equipment PCs from general internet. T-23820.
- 2025-09-09 (Sam Okafor): Semiannual onsite, moved cabinet into locked supply room.

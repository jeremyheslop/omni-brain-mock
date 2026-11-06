# Saltmarsh Law Group

owner: Casey Morgan
last_reviewed: 2026-10-06
tags: legal, clio, netdocuments, ethical-walls, conflicts, omni-managed, salisbury, confidential
client_id: 1009
slug: saltmarsh-law-group
core_plan: Omni+ Managed
service_plans: Omni+ Managed, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Omni+ Passportal
industry: Professional Service
employees: 16

## Overview
Mid-small law firm in downtown Salisbury, MD. 16 staff: 5 attorneys (3 partners, 2 associates), 3 paralegals, 3 legal assistants, 2 billing/accounting staff, 1 firm administrator, 1 receptionist, 1 records clerk. Practice areas: family law, estate and probate, real estate litigation, and a small business transactional group. Some matters involve opposing parties who are also current or former clients, so the firm keeps strict ethical walls.

Main systems: Clio Manage (matters, time, billing, conflicts), NetDocuments (document management), Microsoft 365, and a modest on-prem footprint (one small server for scanning and print).

Confidentiality rules here are stricter than at most clients. Read the ethical wall section before touching anything related to documents, mailboxes or permissions. When in doubt, ask Margaret (Firm Administrator) before you open a file.

## Service plans and contract notes
- Core plan: Omni+ Managed. N-central agent, SentinelOne, DNSFilter, Proofpoint Essentials, Datto SIRIS with cloud replication, Datto SaaS Protection for M365.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Omni+ Passportal.
- Response targets: P1 15 minutes (24x7), P2 1 hour (extended hours 7:00-7:00), P3 2 business hours, P4 next business day.
- Quarterly business review: held the first Thursday of the quarter at the firm, with Margaret and one partner (Thomas Ashby). Casey Morgan owns the relationship.
- Quarterly restore tests: required, see backup section and `sops/09-backup-restore-test.md`.
- Priority onsite. Sam can be onsite same day for P1 and P2.
- Contract renews in October. The 2026 renewal was signed 2026-10-01 with a 3 percent increase.
- The firm's malpractice carrier requires proof of security controls annually. Casey submits the annual attestation in November, Alex supplies the technical details.
- Technicians have signed the firm's confidentiality agreement. Do not open client documents. If a document needs to be opened for troubleshooting, ask a paralegal to share their screen instead.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Margaret Oyelaran (Firm Administrator) | 410-555-0161 | margaret.oyelaran@saltmarshlaw.example |
| Billing | Priya Chaudhary (Billing Manager) | 410-555-0162 | billing@saltmarshlaw.example |
| After-hours | Thomas Ashby (Managing Partner) | 302-555-0164 | thomas.ashby@saltmarshlaw.example |
| Backup after-hours | Margaret Oyelaran (cell) | 410-555-0164 | margaret.oyelaran@saltmarshlaw.example |
| Records manager (NetDocuments admin) | Louis Beaumont | 410-555-0165 | louis.beaumont@saltmarshlaw.example |
| Receptionist | Janelle Pruitt | 410-555-0160 | frontdesk@saltmarshlaw.example |

Main line: 410-555-0160. Louis is the only person who may grant or change NetDocuments access. Never take permission requests from attorneys directly, route them to Louis.

## Sites and addresses
- Main office: 55 Division Street, Suite 300, Salisbury, MD 21801
- Hours: Mon-Fri 8:30-5:30. Partners are often in earlier or later. Court days (Tuesday and Wednesday) often have attorneys out.
- Access: building lobby is open 7:00-6:00, suite door needs a badge. Sam has a visitor badge on file at the front desk. Use the badge system in the lobby after hours (call Margaret).
- Network closet: locked closet next to the conference room. Shared with the building's cable provider box, do not touch the provider's gear.
- Documents are not stored on paper offsite. Boxes of closed files are in the basement storage unit, not our concern.

## Internet and circuits
- Primary: Bayline Broadband business fiber, 500/500. Static block 198.51.100.130/29, firewall at 198.51.100.131.
- Secondary: Delmarva Link Fiber cellular-backed fixed wireless 100/20 as automatic failover, dynamic IP.
- Account refs: BB-0082250 (primary), DLF-61188 (secondary) (both fake).
- Portals: `Vault: saltmarsh-law-group/isp-portal`.
- Provider gear is in the building telecom room on the first floor, not in the suite. The fiber ONT lives there. Building management can unlock it, call Casey first to set up.
- Failover is automatic. A status alert from N-central goes to Alex, who confirms with Margaret.
- See `sops/35-isp-outage-troubleshooting.md`.

## Network
- Firewall: Fortinet FortiGate 80F (SLG-FW01) with FortiGuard web filter and IPS enabled.
- Switches: 2 Ubiquiti UniFi 24-port PoE (SLG-SW01, SLG-SW02), one in the closet, one in the conference room cabinet.
- Wi-Fi: 4 UniFi U6 APs. Staff SSID (WPA2 Enterprise via Entra), Guest SSID, and a "Conf-Room" SSID with an hourly code for clients.
- DHCP and DNS: FortiGate for DHCP, internal DNS from SLG-SRV01.
- VPN: FortiClient with MFA for attorneys working remotely. Under Omni+ Managed, new VPN users require Casey's approval since access to NetDocuments is browser-based anyway.

| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 10 | Staff | 10.60.10.0/24 | Workstations, laptops, printers |
| 20 | Servers/Backup | 10.60.20.0/24 | SLG-SRV01 and the Datto appliance |
| 30 | Guest | 10.60.30.0/24 | Isolated, internet only |
| 40 | Conference | 10.60.40.0/24 | Conference room display, Teams Room device, client Wi-Fi |
| 50 | VoIP | 10.60.50.0/24 | Phones |

Reserved: .1 gateway, .5 server, .20-.40 printers and scanners.

## Servers and line-of-business apps
- SLG-SRV01: Windows Server 2022 (virtual, on a small Dell host SLG-HV01). Roles: file share for scans, print server, DNS. Not a domain controller, devices are Entra joined.
- Clio Manage: cloud. Matters, contacts, calendar, time and billing, conflict checks. Integrated with Microsoft 365 calendar and NetDocuments (via Clio's NetDocuments integration). The integration login must be the service account, not a person's.
- NetDocuments: cloud DMS. All firm documents live in NetDocuments workspaces, one workspace per matter. ndOffice is installed on all workstations for Outlook and Word integration. Cabinets: Active Matters, Closed Matters, Firm Admin.
- Court e-filing: attorneys use the Maryland MDEC portal and federal PACER. No integration to our systems. Paralegals have a shared Adobe Acrobat Pro license for stamping.
- Billing: Clio Payments plus QuickBooks Online maintained by Priya. Not ours.
- Scanning: Fujitsu fi-7600 production scanner (records) saves to a folder on SLG-SRV01. A scheduled job moves scanned PDFs into NetDocuments inbox. If the job fails, scans pile up. See gotchas.

## Ethical walls and conflict handling
Why it matters: the firm has more than one matter where opposing parties were clients of different attorneys. Violations of an ethical wall can mean disqualification. Treat access like a security incident.
- Walls are implemented in NetDocuments by workspace security: only named attorneys and staff have access, everyone else is explicitly excluded. Walls are listed in a spreadsheet kept by Louis.
- Clio mirrors the wall with matter permissions ("Restricted matter" setting). Clio conflict check runs at intake. Conflicts are reviewed by the managing partner.
- Technicians must never be added to a walled workspace, even temporarily. Our admin accounts are excluded from restricted workspaces on purpose. If troubleshooting needs document-level access, a staff member shares their screen.
- Shared mailboxes for restricted matters (for example matter-specific inboxes) are limited to named users. Do not add technicians to mailbox permissions. Use message trace if needed, which only shows metadata.
- When an employee leaves or changes roles, route access removal through Louis and Margaret before we disable anything. The offboarding checklist `sops/03-employee-offboarding.md` has a legal-hold step, follow that. No deleting mailboxes or OneDrive content without written approval from Thomas Ashby.
- Litigation hold: placed in Purview by Alex only on written request from Thomas or Margaret. Keep the request email attached to the Accelo ticket.
- Audit logs: Purview audit retention is set to 1 year. Louis runs the NetDocuments activity report every quarter. We do not.
- If anyone asks us to look at "who opened this file", the answer is yes we can pull audit logs, but get written approval from a partner first.

## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 16 licenses plus 2 shared mailboxes (intake@, billing@) and 1 room mailbox (Conf-Room).
- Tenant domain: saltmarshlaw.example. MFA enforced with Authenticator number matching, no SMS. Conditional Access requires Entra joined or compliant device.
- Devices are Intune enrolled, BitLocker keys escrowed in Entra. Laptops leaving the building must be encrypted. Check compliance before issuing.
- Proofpoint Essentials is in front of the mailboxes. Extra rule: outbound emails with attachments to non-firm domains get a "Confidential" footer. The footer text was approved by Thomas, do not edit it.
- Mailbox auditing is on for everyone. Mail forwarding to external addresses is blocked.
- Retention: 7-year mail retention policy via Purview. Closed matter mail is exported by Louis to NetDocuments, then the mailbox folder is cleaned up by the user.
- Datto SaaS Protection covers mailboxes, OneDrive and SharePoint. Restore requests go through Alex.
- Break-glass account exists, see credential references.

## Backup
- Datto SIRIS appliance (SLG-BKP01) protects SLG-SRV01 and SLG-HV01. Hourly during business hours, nightly cloud replication. Local retention 30 days, cloud 1 year.
- NetDocuments and Clio are cloud systems. Their data is not in our backup. The vendors keep their own copies, but the firm asked in 2025 for a monthly export of the Clio data to a separate encrypted store. Louis runs the export from Clio and hands it to Alex, who stores it in the encrypted Datto cloud folder. Alex owns the schedule. This is manual and is the weakest point.
- Datto SaaS Protection for M365 daily.
- Quarterly restore test: restore SLG-SRV01 scan folder to a lab VM, confirm PDFs open. Also restore one mailbox item from SaaS Protection. Last done 2026-09-23, passed.
- Daily check per `sops/08-daily-backup-check.md`.
- Omni+ Managed includes disaster recovery planning. A written DR plan exists in Google Drive under the client folder, last updated 2026-03.

## Printers, scanners, and other devices
- Xerox VersaLink C7130 in the main hallway (SLG-PR01), static 10.60.10.21. Scan to email through the M365 relay. Secure print release enabled (PIN).
- Brother MFC-L9570CDW at the receptionist desk, static 10.60.10.22.
- Fujitsu fi-7600 in the records room, USB to SLG-WS-012.
- Conference room: 85-inch display, Teams Room device. Calendar integrates with the room mailbox.
- 16 Windows laptops/docking stations (SLG-LT-01 to SLG-LT-16), Dell Latitudes, 3-year refresh cycle. Each user has dual monitors.
- Desk phones are a hosted VoIP system (VLAN 50). Voicemail transcriptions may include client information, treat them as confidential.
- Shredding is a vendor service, not IT.

## Vendor contacts
| Vendor | Rep | Phone | Notes |
|---|---|---|---|
| Bayline Broadband | Business support | 410-555-0176 | Account BB-0082250 (fake) |
| Delmarva Link Fiber | Wireless support | 410-555-0177 | Account DLF-61188 (fake) |
| Clio support | Tier 2 | 410-555-0185 | Account admin: Margaret |
| NetDocuments support | Customer success manager Ellis Park | 410-555-0186 | Only Louis may open admin tickets |
| Chesapeake Voice Co. | Dispatch | 410-555-0175 | Phones, voicemail transcription |
| Malpractice carrier broker | Denise Kowal | 410-555-0187 | Annual security attestation |
| Building manager | Salisbury Plaza management | 410-555-0188 | Lobby and telecom room access |

## Gotchas / tribal knowledge
- Never open a client document to troubleshoot. If an Outlook or Word add-in fails, ask the user to share their screen and do not click into files.
- NetDocuments ndOffice crashes Word after Office updates. Fix: repair the Office install, then reinstall ndOffice from the NetDocuments portal, not from a stored installer. Run the repair on a test laptop first. Attorneys notice when Word hangs.
- The scan-to-NetDocuments job on SLG-SRV01 fails when the scanner folder has a file with a trailing space in the name. Move that file into a quarantine folder and re-run. Louis names files by hand sometimes.
- Court days: Tuesday and Wednesday mornings have attorneys at hearings and relying on laptops, hotspots and phones. Do not push updates to laptops those mornings. Patch windows are Thursday after 6:00 PM.
- Partners expect a same-day callback even for P4. This is not in the SLA but it matters to the relationship. Call and say it is scheduled.
- The conference room Teams device loses its calendar after a password rotation on the room mailbox. Re-sign in with the room account in the device's admin menu. This has happened three times.
- Priya's QuickBooks Online and Clio billing export use a CSV that breaks if Excel auto-converts the matter number to a date. Tell her to import as text.
- Firm Word templates live in the NetDocuments Firm Admin cabinet. Do not edit them, even to fix a style problem. Tell Louis.
- Partner Thomas Ashby uses a personal iPad with Outlook. It is enrolled with app protection only, not full MDM. This was a negotiated exception, noted in Accelo.
- When a new attorney is onboarded, do not copy permissions from another attorney. Louis builds the NetDocuments access from the conflict-checked matter list, then Margaret signs off.
- Voicemail to email is turned off for the family law group. They asked for it in 2025.

## Credential references
- `Vault: saltmarsh-law-group/firewall-admin`
- `Vault: saltmarsh-law-group/switch-admin`
- `Vault: saltmarsh-law-group/wifi-psk`
- `Vault: saltmarsh-law-group/isp-portal`
- `Vault: saltmarsh-law-group/domain-registrar`
- `Vault: saltmarsh-law-group/m365-global-admin-breakglass`
- `Vault: saltmarsh-law-group/backup-appliance`
- `Vault: saltmarsh-law-group/lob-app-admin` (Clio service account and Proofpoint admin; NetDocuments admin is held by Louis only)
- `Vault: saltmarsh-law-group/printer-admin`

## Change log
- 2026-10-06: Review after renewal. Updated contract date, added ethical wall section. (Casey Morgan)
- 2026-09-23: Q3 restore test passed (scan folder and one mailbox item). (Alex Rivera, T-25390)
- 2026-07-15: Replaced Teams Room device after repeated calendar failures. (Sam Okafor, T-25140)
- 2026-05-12: Moved patch window from Wednesday to Thursday after 6:00 PM due to court schedule. (Casey Morgan, T-24881)
- 2026-03-04: Updated DR plan in Google Drive. (Alex Rivera, T-24577)
- 2025-12-09: Added monthly Clio export to encrypted Datto folder. (Alex Rivera, T-24233)
- 2025-09-17: Entra join and Intune enrollment finished for last 3 laptops. (Jordan Blake, T-23802)

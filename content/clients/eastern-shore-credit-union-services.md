# Eastern Shore Credit Union Services

owner: Alex Rivera
last_reviewed: 2026-10-02
tags: financial-services, credit-union, core-banking, segmented-network, change-control, audit, omni-managed, ffiec
client_id: 1016
slug: eastern-shore-credit-union-services
core_plan: Omni+ Managed
service_plans: Omni+ Managed, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Omni+ Passportal
industry: Financial Services
employees: 38

## Overview
Eastern Shore Credit Union Services (ESCUS, say "ess-cus") is the shared-services and back-office arm for a small group of member credit unions on the Shore. They run member support, loan processing, card dispute handling, and the connection to the core banking processor. 38 users, one main office in Salisbury and a small disaster recovery room at a second site in Fruitland. No member branches are managed by us. Branch networks belong to the individual credit unions.

This is our most regulated client. They get examined (NCUA-style exam plus an annual third-party IT audit modeled on FFIEC guidance), so anything we touch needs a ticket, a change record, and evidence. If you are unsure whether something is a "change", it is. Open the ticket first.

Key facts to remember:
- Core banking runs at the processor, not here. We only maintain the connection (site-to-site VPN plus a terminal emulator app on about 22 workstations).
- Network is segmented on purpose. Do not "simplify" VLANs, ever.
- Change control is strict. No firewall, GPO, or server changes without an approved change ticket.
- Audit evidence is collected quarterly and handed over by Casey. See the audit section below.

Related company: Chincoteague Title & Escrow (client 1007) is a subsidiary and lists this company as its Parent Company in Accelo. The two have separate contracts, networks and contacts.

## Service plans and contract notes
- Core plan: Omni+ Managed. Contract renews every January 1. Accelo contract: "ESCUS Omni+ Managed Managed Services".
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Omni+ Passportal.
- First response: P1 15 minutes (24x7), P2 1 hour (extended hours 7:00-7:00), P3 2 business hours, P4 next business day.
- Quarterly business review (QBR) is with Dana Whitfield (COO) and Priya Raman (IT/compliance). Casey runs it, Alex preps the numbers from N-central and Accelo.
- Quarterly restore tests are in the contract and are an audit item. See SOP `sops/09-backup-restore-test.md`. Results go to Priya the same week.
- Priority onsite: Sam can be there within 4 business hours for P1/P2. Onsite visits are not billed against the monthly hour block.
- Contract includes security awareness training seats (38) and Proofpoint Essentials. It does not include the core processor's own support, or the terminal emulator license.
- Change windows: Tuesday and Thursday 6:00 PM to 10:00 PM Eastern, plus emergency changes with Priya's written OK. Core processor maintenance happens the first Sunday of the month, do not schedule anything that weekend.
- Month-end and quarter-end: change freeze from the 28th through the 3rd. Exceptions need Dana's sign-off.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Priya Raman (IT and Compliance Manager) | 410-555-0152 | priya.raman@escus.example |
| Billing | Marcus Delaney (Finance Manager) | 410-555-0155 | marcus.delaney@escus.example |
| After-hours | Priya Raman (cell) | 410-555-0156 | priya.raman@escus.example |
| Executive sponsor | Dana Whitfield (COO) | 410-555-0157 | dana.whitfield@escus.example |
| Office manager | Gloria Fenn | 410-555-0158 | gloria.fenn@escus.example |
| Member support lead | Terrence Boyd | 410-555-0166 | terrence.boyd@escus.example |
| Facilities / building access | Harlan Pruitt | 410-555-0167 | harlan.pruitt@escus.example |

Notes: Call Priya first for anything security related. Call Dana only if Priya is unreachable for a P1. Casey owns the relationship, so tell Casey before any call to Dana.

## Sites and addresses
| Site | Address | Hours | Notes |
|---|---|---|---|
| Main office (HQ) | 2210 Riverside Commerce Way, Suite 300, Salisbury, MD 21801 | Mon-Fri 8:00-5:30, Sat 9:00-1:00 (member support only) | Badge entry. Sign in at front desk, wear visitor badge. |
| DR room | 418 Railroad Ave, Unit B, Fruitland, MD 21826 | Unattended, access by appointment | Call Harlan 24 hours ahead. Alarm code is held by Priya, not in the vault. |

- Server room at HQ is on the third floor behind the break room. Door has a keypad plus badge. Sam has a badge, Alex has a badge, Jordan does not.
- Parking for service vehicles is in the rear lot. Loading dock is shared with another tenant, do not block it.
- Visitors to the server room must be escorted and logged on the paper log inside the door. Auditors check that log.

## Internet and circuits
| Item | Primary | Secondary |
|---|---|---|
| ISP | Delmarva Link Fiber | Bayline Broadband |
| Type | 500/500 dedicated fiber (DIA) | 300/30 business cable |
| Static IP | 203.0.113.40/29 (usable .41-.45, firewall on .41) | 198.51.100.74/30 (firewall on .74) |
| Account ref | DLF-ESCUS-0042 | BB-88317 |
| Handoff | Fiber ONT in telecom closet, 1st floor | Cable modem in server room, rack 1 |
| Support | 410-555-0171 (Delmarva Link NOC) | 410-555-0172 |

- Failover is automatic on the FortiGate (SD-WAN rule, health check to the processor VPN peer, not to the internet). If the primary link is up but the processor VPN is down, failover still triggers. This is by design.
- The cable modem is in bridge mode. Do not factory reset it, Bayline has to re-provision it and that takes two days.
- Delmarva Link NOC will only talk to the account contact (Priya) for outages. Casey is added as an authorized contact. Jordan and Sam are not, so give them the account ref and let Casey open the case if Priya is out.
- Circuit outage SOP is `sops/35-isp-outage-troubleshooting.md`. Always check the secondary before calling the ISP.

## Network
- Firewall: FortiGate 100F pair in HA (active/passive), FortiOS 7.2. HQ cluster named `ESCUS-FW01` and `ESCUS-FW02`. DR room has a FortiGate 60F `ESCUS-DR-FW01`.
- Core switch: Aruba CX 6300M `ESCUS-SW-CORE`. Access switches: Aruba CX 6100 x3 (`ESCUS-SW-A1` to `A3`). Wi-Fi: Aruba AP-515 x6 managed by a controller-less Instant setup, SSIDs below.
- Site-to-site: IPsec to the core processor (peer 198.51.100.200), IPsec to DR room, and a small client VPN (FortiClient, MFA via Entra) for 6 remote-eligible staff.
- Firewall changes follow `sops/18-firewall-rule-change-request.md` plus ESCUS's own change form. Priya signs, Alex implements, Casey files the evidence.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 10 | Corp-Users | 10.40.10.0/24 | Normal staff workstations |
| 20 | Core-Access | 10.40.20.0/26 | The 22 workstations allowed to reach the core processor |
| 30 | Servers | 10.40.30.0/24 | AD, file, backup, print |
| 40 | Voice | 10.40.40.0/24 | Phones (hosted VoIP, QoS tagged) |
| 50 | Guest | 10.40.50.0/24 | Guest Wi-Fi, internet only, isolated |
| 60 | Mgmt | 10.40.60.0/28 | Switch, AP, firewall management |
| 70 | Card-Ops | 10.40.70.0/27 | Card dispute team, extra restrictions |

- DHCP: served by the two domain controllers (split scope 50/50) for VLANs 10, 20, 70. Voice and guest DHCP are on the firewall. Servers and Mgmt are static.
- DNS: internal AD DNS. Forwarders go to DNSFilter on the firewall. Do not point workstations at public DNS.
- A workstation moves between VLAN 10 and VLAN 20 by switch port profile plus an AD group (`ESCUS-CoreAccess`). Both must change, and the change needs a ticket and Priya's approval. Member Support is the only team that normally has VLAN 20.
- Wi-Fi: `ESCUS-Staff` (WPA2-Enterprise, Entra-backed RADIUS on the NPS server), `ESCUS-Guest` (PSK, rotated quarterly by Jordan). Guest SOP: `sops/20-wifi-guest-network.md`.
- No inter-VLAN routing from Guest to anything. Auditors test this. Leave it alone.

## Servers and line-of-business apps
| Name | Role | OS | Notes |
|---|---|---|---|
| ESCUS-DC01 | Domain controller, DHCP | Windows Server 2022 | Physical Dell R450 |
| ESCUS-DC02 | Domain controller, DHCP, NPS | Windows Server 2022 | VM on host below |
| ESCUS-HV01 | Hyper-V host | Windows Server 2022 | Dell R650, hosts DC02, FS01, APP01, PRT01 |
| ESCUS-FS01 | File server | Windows Server 2022 | Member docs, loan files, restricted shares |
| ESCUS-APP01 | App server | Windows Server 2019 | Loan origination web app and doc imaging |
| ESCUS-PRT01 | Print server | Windows Server 2022 | All queues, secure release printing |
| ESCUS-DR01 | DR replica host | Windows Server 2022 | In Fruitland, receives Datto replication |

- Core banking: hosted at the processor, reached through a terminal emulator (a Citrix-style published app) over the IPsec tunnel. Only VLAN 20 can reach it. If the tunnel is down the emulator shows "host unreachable". See gotchas.
- Loan origination: a vendor web app on APP01 plus a document imaging client. The vendor patches it themselves, we only patch the OS.
- Secure printing: PaperCut-style release stations. Print queues are tied to AD groups.
- Server patching goes through N-central, approved monthly, installed during the Tuesday change window. See `sops/06-monthly-patch-review.md` and `sops/25-server-reboot-window.md`. Every server reboot gets a change ticket.
- Endpoint count in N-central: 38 workstations/laptops, 7 servers, 3 firewalls, 4 switches. Device naming `ESCUS-WS-0xx` and `ESCUS-LT-0xx`.

## Microsoft 365 / Google tenant notes
- Tenant: `escus.example` (Microsoft 365 Business Premium for 36 users, 2 Exchange Online shared mailboxes unlicensed, 1 service account). Two seats are Business Premium + Exchange archiving add-on for the compliance team.
- Conditional Access: block legacy auth, require MFA everywhere, block sign-in from outside the US, require compliant device for admin roles. Policy changes need a change ticket.
- Proofpoint Essentials sits in front of Exchange Online (MX points to Proofpoint). Quarantine digest goes to users daily at 7:00 AM. Release requests for anything with an attachment from an unknown sender go to Priya.
- Email retention: 7 years via retention policy plus litigation hold on 5 named mailboxes. Do not remove a licensed user without checking hold status. Offboarding SOP is `sops/03-employee-offboarding.md` and the process plan is `process-plans/employee-offboarding.md`.
- Break-glass admin: two accounts, excluded from Conditional Access, alerts to Priya and Casey on any sign-in. Reference in the vault section.
- Shared mailboxes: `memberservices@escus.example`, `disputes@escus.example`. Setup standard is `sops/15-shared-mailbox-setup.md`.
- Datto SaaS Protection covers all mailboxes, OneDrive, and SharePoint. 7-year retention is on the backup side too, because an auditor asked.

## Backup
- Server and image backup: Datto SIRIS appliance at HQ (`ESCUS-BDR01`), 15-minute snapshots on FS01 and APP01, hourly on the rest. Cloud replication to Datto cloud plus local replication to the DR room hardware (ESCUS-DR01).
- M365: Datto SaaS Protection, 3 backups a day.
- Daily check per `sops/08-daily-backup-check.md`. Jordan does it, Alex reviews failures. Failures on FS01 or APP01 are a P2 here, not P3.
- Quarterly restore test per `sops/09-backup-restore-test.md`: one file-level restore, one full VM virtualization test of APP01, one mailbox item restore. Evidence (screenshots, timestamps, who approved) is saved to `ESCUS Audit Evidence/Restore Tests/<year>-Q#` in the secured Google Drive folder, and linked in the Accelo ticket.
- Last restore test: 2026-09-18, passed. APP01 virtualized in 11 minutes. Next due by 2026-12-18.
- Retention: 30 days local, 7 years cloud for FS01 (yes, expensive, Marcus knows).

## Audit evidence
Annual IT audit is in March, with quarterly self-assessment packets. Priya asks for the same things every time:
- Patch compliance report from N-central (monthly, PDF, all devices, showing exceptions with reasons).
- List of approved change tickets for the quarter, exported from Accelo with approver names and timestamps.
- Firewall rule review, signed by Priya, twice a year (June and December). Alex does the export and walks through it.
- User access review: AD group membership export for `ESCUS-CoreAccess`, `ESCUS-Admins`, `ESCUS-LoanRestricted`, Entra admin role list. Done quarterly.
- Restore test evidence (above).
- Offboarding evidence: for each departure, disabled date, mailbox handling, device wiped date. Keep in the ticket.
- Security awareness training completion, pulled by Jordan from the training portal.
- Visitor log scans from the server room.
Where it all goes: `ESCUS Audit Evidence/<year>/` in the restricted Google Drive folder (Casey and Alex only). Do not email evidence, use the Drive link.

## Printers, scanners, and other devices
| Device | Model | Location | Notes |
|---|---|---|---|
| ESCUS-PRT-MFP1 | Ricoh-style color MFP | 3rd floor hall | Secure release, scan to email via relay |
| ESCUS-PRT-MFP2 | Ricoh-style color MFP | Member support | Secure release |
| ESCUS-PRT-CARD | Check/card label printer | Card-Ops room | USB on one fixed PC (`ESCUS-WS-031`), not network |
| Check scanners | Panini-style desktop x6 | Loan processing | Driver is picky, see gotchas |
| Door/badge system | Cloud badge reader controller | HQ entry, server room | Facilities owns it, not us |
| Cameras | 8-camera NVR | HQ | VLAN 60, facilities owns it, we only keep it patched |
| Phones | Hosted VoIP, 38 desk phones | All | Vendor: Tidewater Voice (fictional), VLAN 40 |

Scan-to-email uses the printers' static IPs and an SMTP relay with an allowed IP list. See `sops/17-scan-to-email-troubleshooting.md` and `sops/16-printer-scanner-setup.md`.

## Vendor contacts
| Vendor | What | Contact | Phone |
|---|---|---|---|
| Harborline Core Systems (core processor) | Core banking, tunnel peer | Nolan Teague (account mgr) | 410-555-0174 |
| Harborline Core Systems | Tunnel / network support | Support desk | 800-555-0198 |
| Delmarva Link Fiber | Primary circuit | NOC | 410-555-0171 |
| Bayline Broadband | Backup circuit | Business support | 410-555-0172 |
| LoanBridge Software | Loan origination app | Renata Voss | 410-555-0176 |
| Tidewater Voice | Hosted phones | Support | 410-555-0177 |
| Datto | SIRIS and SaaS Protection | Via partner portal | n/a |
| Fortinet | FortiGate support (FortiCare) | Via partner portal, contract FC-ESCUS | n/a |
Vendor escalation process is `sops/30-vendor-escalation.md`. For the core processor tunnel, call their support desk first, then Nolan, and keep Priya copied.

## Gotchas / tribal knowledge
1. Never reboot ESCUS-HV01 or either firewall outside a change window, even if it "looks hung". The core tunnel takes about 6 minutes to renegotiate, and member support is watching it in real time.
2. The terminal emulator app only works on VLAN 20 machines. If a user says "core is down" and they are on VLAN 10, they are probably on the wrong port or the AD group got removed. Check `ESCUS-CoreAccess` before anything else.
3. The check scanners need the old 32-bit driver. Windows 11 feature updates break it about once a year. Test one machine before approving the feature update ring in N-central.
4. The processor's tunnel peer drops idle IPsec sessions at exactly 8 hours. The FortiGate has a keepalive ping set to the peer for this reason. If someone "cleans up" firewall policies and removes it, core drops every morning at about 3:00 AM.
5. Secure print release cards are programmed by Gloria. Jordan cannot reissue them. Don't promise a same-day card replacement.
6. Terrence's team prints disputes in bulk at month end. Leave the print server alone from the 28th to the 3rd.
7. Card-Ops (VLAN 70) can't reach the file server on SMB except one share. If a new hire there "can't open files", it is almost never a bug. Check the ticket for the approved share list.
8. The Saturday member support shift (9:00-1:00) is two people on laptops. If the Wi-Fi goes down Saturday, Priya wants a call, not a ticket.
9. Auditors ask for screenshots with visible timestamps and the tech's name. Put your name in the ticket notes, not just "done".
10. The DR room has no staff. Rack temperature alerts from N-central go to Sam as well as Alex. Last summer the AC tripped and nobody noticed for a day.
11. Do not use remote control on VLAN 70 or 20 machines without telling Priya in the ticket first. It is allowed, but she wants a note, and N-central session logs are part of the evidence.
12. The two Exchange shared mailboxes have auto-reply text approved by compliance. Don't edit it without a ticket.

## Credential references
- Vault: eastern-shore-credit-union-services/firewall-admin
- Vault: eastern-shore-credit-union-services/firewall-dr-admin
- Vault: eastern-shore-credit-union-services/switch-admin
- Vault: eastern-shore-credit-union-services/wifi-psk (guest only)
- Vault: eastern-shore-credit-union-services/m365-global-admin-breakglass
- Vault: eastern-shore-credit-union-services/domain-registrar
- Vault: eastern-shore-credit-union-services/isp-portal
- Vault: eastern-shore-credit-union-services/backup-appliance
- Vault: eastern-shore-credit-union-services/lob-app-admin (LoanBridge)
- Vault: eastern-shore-credit-union-services/core-tunnel-psk (held jointly with the processor, rotate by change ticket only)
- Vault: eastern-shore-credit-union-services/printer-admin

## Change log
- 2026-10-02 (Alex Rivera): Annual doc review. Updated VLAN 70 notes and audit evidence list.
- 2026-09-18 (Alex Rivera, Jordan Blake): Q3 restore test passed. Evidence filed. T-25102.
- 2026-08-12 (Alex Rivera): FortiOS upgrade to 7.2 latest patch on HA pair, Tuesday window, no tunnel drop beyond 40 seconds. T-24977.
- 2026-06-17 (Alex Rivera): Semiannual firewall rule review, signed by Priya. Removed 4 stale rules. T-24610.
- 2026-04-08 (Sam Okafor): Replaced failed PSU in ESCUS-DR01. T-24388.
- 2026-02-24 (Casey Morgan): Added Dana's assistant as authorized contact on Delmarva Link account.
- 2026-01-13 (Alex Rivera): Moved Card-Ops team to new VLAN 70 after audit finding. T-24102.

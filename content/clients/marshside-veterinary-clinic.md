# Marshside Veterinary Clinic

owner: Sam Okafor
last_reviewed: 2026-04-14
tags: veterinary, avimark, idexx, digital-xray, omni-basic, fruitland
client_id: 1006
slug: marshside-veterinary-clinic
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Backup, Hosted Website Plan
industry: Healthcare
employees: 12

## Overview
Small-animal vet clinic in Fruitland, MD. 12 staff: 3 veterinarians, 5 technicians/assistants, 3 front desk, 1 practice manager. Single site. Busy all day, walk-ins and surgery drop-offs start at 7:30, so there is no quiet window for work during the day.

Main systems: AVImark (practice management), an IDEXX in-house lab (VetLab Station plus analyzers), and a digital X-ray setup in the treatment area. The clinic is not very tech-minded, the practice manager (Denise Harlow) is the one person who gets it. Always go through her unless it is an emergency.

Dr. Pruitt (owner vet) is hands-off but approves anything that costs money.

## Service plans and contract notes
- Core plan: Omni+ Basic. N-central agent on all workstations and the AVImark server, SentinelOne EDR, DNSFilter, patching on the monthly cycle (see `sops/06-monthly-patch-review.md`).
- Add-ons: Omni+ Backup, Hosted Website Plan.
- Response targets: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days. After-hours by request only, billed at after-hours rate.
- Backup is Cove Data Protection (cloud only), no local appliance. No Datto SaaS Protection on M365, that is a Omni+ Proactive or Omni+ Managed feature. Dr. Pruitt was quoted an upgrade in Feb 2026 and passed.
- Contract renews every January. Billing goes through Accelo contract, ask Casey Morgan for changes.
- Onsite visits are billed time and materials. Sam does hardware visits, schedule at least 2 days out and avoid Tuesday and Thursday (surgery days).
- Switches, APs and the gateway are covered for monitoring only. Hardware replacement is quoted separately.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Denise Harlow (Practice Manager) | 302-555-0129 | denise.harlow@marshsidevet.example |
| Billing | Marcus Pruitt (Owner, DVM) | 302-555-0130 | dr.pruitt@marshsidevet.example |
| After-hours | Denise Harlow (cell) | 302-555-0131 | denise.harlow@marshsidevet.example |
| Front desk lead | Tonya Reyes | 302-555-0132 | frontdesk@marshsidevet.example |
| Lead vet tech (X-ray, analyzers) | Kyle Brandt | 302-555-0133 | kyle.brandt@marshsidevet.example |

Main clinic line: 410-555-0130. If Denise does not answer after-hours, try Tonya, then Dr. Pruitt as last resort.

## Sites and addresses
- Main clinic: 118 Mill Pond Road, Fruitland, MD 21826
- Hours: Mon-Fri 7:30-6:00, Sat 8:00-12:00, closed Sun (emergency referrals go to an outside ER clinic).
- Access: front door code is held by Denise, do not write it down in Accelo. Side door by the kennels is used for deliveries. Park in the back.
- Server and network gear are in the supply closet behind the pharmacy. Keep the door closed, the dogs bark at the fan noise otherwise (really).

## Internet and circuits
- ISP: Bayline Broadband, business cable, 300/30 Mbps.
- Static IP: 198.51.100.68 (single static, /29 not purchased).
- Account ref: BB-0048213 (fake). Portal login: `Vault: marshside-veterinary-clinic/isp-portal`.
- Cable modem sits in the supply closet next to the UPS. It is ISP-owned, do not swap it ourselves.
- No backup circuit. When cable is down the clinic runs AVImark locally on the server but cloud lab results and VetConnect PLUS stop. Phone lines are on a separate carrier so the front desk can still take calls.
- See `sops/35-isp-outage-troubleshooting.md`.

## Network
- Gateway: Ubiquiti UniFi Dream Machine Pro (MVC-GW01), firmware auto-update turned OFF, update by hand after hours.
- Switch: one UniFi 24-port PoE (MVC-SW01) in the closet, one 8-port in the treatment room (MVC-SW02) for the X-ray capture PC and analyzers.
- Wi-Fi: 3 UniFi U6 access points (lobby, exam hall, kennel area). Staff SSID and guest SSID.
- DHCP and DNS: the UDM-Pro hands out DHCP. Clients use the gateway as DNS, which forwards to DNSFilter. MVC-SRV01 does not run DNS or DHCP.
- VPN: none. Dr. Pruitt checks lab results from home through VetConnect PLUS in the browser.

| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 1 | Staff | 192.168.60.0/24 | Workstations, printers, server |
| 20 | Lab/Imaging | 192.168.62.0/24 | Analyzers, X-ray capture PC, VetLab Station |
| 30 | Guest | 192.168.63.0/24 | Client isolation on, internet only |

DHCP range on Staff: .100-.199. Server and printers sit on static addresses below .50.

## Servers and line-of-business apps
- MVC-SRV01: Windows Server 2019 on a single Dell tower, 16 GB RAM, hosts AVImark database and file shares. Static 192.168.60.10. No virtualization and no Active Directory domain, the clinic runs a workgroup with local accounts and M365 sign-in on workstations.
- AVImark (practice management): runs on the server, workstations use the client install mapped to `\\MVC-SRV01\AVImark`. Support from the AVImark vendor, see vendor contacts.
- IDEXX VetLab Station (MVC-LAB01): small PC in the lab. Connects the in-house analyzers (chemistry, hematology, and a urine analyzer) and pushes results to AVImark through the IDEXX interface. Analyzers are static IPs on VLAN 20.
- Digital X-ray: DR panel with a capture workstation (MVC-XR01) in the treatment room. Images get stored locally and exported to AVImark. Radiograph archive is on a separate 4 TB drive in MVC-SRV01.
- Do not install Windows feature updates on MVC-LAB01 or MVC-XR01 without checking with the vendor first, past updates have broken the analyzer drivers.
- Other: QuickBooks Desktop Pro on one front desk PC (Denise). Not shared.

## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 12 licenses plus 2 shared mailboxes (frontdesk@, labresults@).
- Tenant domain: marshsidevet.example. MFA enforced via Conditional Access, Authenticator app, except two kennel-area shared tablets that use a legacy flow (see gotchas).
- Break-glass account exists, see credential references. Do not use for daily admin.
- Email is hosted in M365 only. No third-party gateway (Proofpoint Essentials is Omni+ Managed-only).
- No Datto SaaS Protection. Deleted items restore is limited to the M365 retention window, tell the client that if they ask about recovering old mail.

## Backup
- Cove Data Protection (cloud only) on MVC-SRV01. Daily at 10:00 PM, retention 28 days in the cloud plus monthly fulls kept 12 months.
- Backup selection includes the AVImark database, the radiograph archive drive, and the QuickBooks company file.
- Workstations are not backed up. Documents live on the server.
- Daily check: see `sops/08-daily-backup-check.md`. Failures raise a N-central alert and an Accelo ticket.
- Restore tests are not part of Omni+ Basic. Do an informal test once a year if time allows. Last one was 2025-11, restored one AVImark backup file to a lab VM without issue.
- Radiographs: 4 TB drive is about 70 percent full. Flag to Denise when it hits 85 percent, the plan is a larger drive.

## Printers, scanners, and other devices
- Front desk: Brother MFC-L8900CDW color laser multifunction, static 192.168.60.21.
- Treatment room label printer for pharmacy labels (Zebra), USB to MVC-WS-004 only.
- Fujitsu ScanSnap iX1600 at front desk for scanning records into AVImark.
- Credit card terminals are on a dedicated processor network, not ours. Do not touch.
- Two kennel-area tablets (iPad) show the daily treatment board.
- Phones are a hosted VoIP system from the phone vendor, handsets on VLAN 1.
- 8 workstations (MVC-WS-001 to MVC-WS-008), mostly Dell OptiPlex from 2021, check `sops/23-end-of-life-hardware.md` for Win 10 items.

## Vendor contacts
| Vendor | Rep | Phone | Notes |
|---|---|---|---|
| Bayline Broadband | Support desk | 410-555-0172 | Account BB-0048213 (fake) |
| AVImark support | Gina Voss | 800-555-0199 | Needs the clinic's customer number, in the vault note |
| IDEXX service | Local tech Ron Lefler | 410-555-0173 | Analyzer repair and VetLab Station updates |
| X-ray vendor (Tidal Imaging Supply) | Priya Nandakumar | 410-555-0174 | DR panel calibration and software |
| Hosted phone provider | Chesapeake Voice Co. | 410-555-0175 | Handsets, call routing |

## Gotchas / tribal knowledge
- Surgery days are Tuesday and Thursday. No reboots, no remote sessions on the front desk PCs before 2:00 PM on those days.
- AVImark must be fully closed on every workstation before the nightly backup window (10:00 PM) or the backup can skip the database. Kyle sometimes leaves it open in the treatment room. Check the N-central alert for MVC-SRV01 if backup warnings appear on Wednesday and Friday mornings.
- After any power blip, the analyzers do not come back on the right IP until the VetLab Station is restarted last. Order is: switch, analyzers, then MVC-LAB01.
- The pharmacy label printer is USB only. If the label shows the wrong drug name, it is an AVImark template issue, not the printer. Hand it to Gina at AVImark support.
- X-ray capture software license is tied to MVC-XR01's hardware. If the PC is replaced, the vendor has to re-issue the license, give them 3 business days.
- The kennel tablets cannot do the Authenticator prompt. They use a dedicated account (kennelboard@) with a scoped Conditional Access exclusion for the clinic's static IP only.
- The cable modem has a failing power brick (see change log). Keep a spare on the shelf.
- Denise reads email on her phone and will click anything. She has had two phishing near-misses. Use `sops/10-phishing-email-response.md` and check her mail rules after any report.
- Wi-Fi in the kennel area drops when the large dryer runs. Moved AP to the hallway in 2025, it is mostly better.
- Do not use the front desk PC's USB ports for anything, the label printer is on that bus and unplugging it kills the pharmacy workflow for the day.

## Credential references
- `Vault: marshside-veterinary-clinic/firewall-admin`
- `Vault: marshside-veterinary-clinic/switch-admin`
- `Vault: marshside-veterinary-clinic/wifi-psk`
- `Vault: marshside-veterinary-clinic/isp-portal`
- `Vault: marshside-veterinary-clinic/domain-registrar`
- `Vault: marshside-veterinary-clinic/m365-global-admin-breakglass`
- `Vault: marshside-veterinary-clinic/backup-appliance` (Cove portal login)
- `Vault: marshside-veterinary-clinic/lob-app-admin` (AVImark admin)

## Change log
- 2026-04-14: Documentation review, updated contacts and VLAN table. (Sam Okafor)
- 2026-02-09: Quoted Omni+ Proactive upgrade to Dr. Pruitt, declined. Noted in Accelo. (Casey Morgan)
- 2025-11-18: Annual restore test of AVImark backup to lab VM, passed. (Alex Rivera, T-24108)
- 2025-09-04: Replaced cable modem power brick, ISP dispatched (Sam Okafor, T-23740)
- 2025-06-12: Moved kennel AP to hallway after dryer interference. (Sam Okafor, T-23188)
- 2025-03-20: Moved X-ray capture PC and analyzers onto VLAN 20. (Alex Rivera, T-22764)

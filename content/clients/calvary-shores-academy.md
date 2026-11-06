# Calvary Shores Academy

owner: Alex Rivera
last_reviewed: 2026-10-09
tags: education, k-12, omni-managed, google-workspace, chromebooks, fortinet, unifi, student-vlan, content-filter, e-rate, datto
client_id: 1024
slug: calvary-shores-academy
core_plan: Omni+ Managed
service_plans: Omni+ Managed, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Hosted Website Plan, Omni+ Backup
industry: Education
employees: 45

## Overview
Private K-8 school in Salisbury, MD. 45 staff (teachers, aides, admin office, facilities). Roughly 380 students. Staff and students live in Google Workspace for Education. The admin office (front office, business manager, head of school) also has a small Microsoft 365 Business Premium tenant for Excel-heavy finance work and Outlook. Yes, two tenants. It is on purpose, see gotchas.

Fleet: about 400 Chromebooks (student carts plus staff), 38 Windows PCs (admin office, labs, teacher desks), 12 iPads (kindergarten cart), 6 classroom smartboards. Everything on one campus, two buildings.

Biggest rules: student devices never touch the staff network, the content filter must stay on, and nothing disruptive happens between the first bell in late August and the last day in May. Big changes wait for the summer maintenance window.

N-central device prefix: `CSA-` (e.g. `CSA-HV01`, `CSA-WS-007`). Chromebooks are NOT in N-central, they live in the Google Admin console.

## Service plans and contract notes
- Core plan: Omni+ Managed. Agreement renewed 2026-07-01 for 12 months, auto-renews. Casey owns the contract.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management, Hosted Website Plan, Omni+ Backup.
- Response targets: P1 15 minutes (24x7), P2 1 hour (7:00-7:00), P3 2 business hours, P4 next business day.
- Quarterly business review (QBR) with head of school and business manager. Next one: January 2027 (they asked for it after winter break, not the first week).
- Quarterly restore tests required. Results go in the QBR deck. See `sops/09-backup-restore-test.md`.
- Priority onsite: Sam is onsite every other Tuesday during the school year, every Tuesday and Thursday in the summer window.
- Includes Proofpoint Essentials on the M365 tenant only. The Google tenant relies on Google's own mail filtering (see Google section).
- Not covered: the SIS (PowerSchool, hosted), the copier lease (Ricoh dealer), and the school's door access and fire panel. Do not touch those even if asked nicely.
- After-hours: school events (evening concerts, Friday night games, the spring auction) are scheduled. Casey agrees an event support window in advance. Otherwise standard on-call applies.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Marguerite Dalloway (Business Manager) | 410-555-0102 | m.dalloway@calvaryshores.example |
| Billing | Teresa Quillen (Accounts Payable) | 410-555-0103 | t.quillen@calvaryshores.example |
| After-hours | Dennis Harkins (Facilities Director) | 410-555-0104 | d.harkins@calvaryshores.example |
| Head of School | Rev. Allan Pruitt | 410-555-0105 | head@calvaryshores.example |
| Front office / first call | Joanne Baptiste (Office Manager) | 410-555-0106 | office@calvaryshores.example |
| Teacher tech liaison | Priya Venkataraman (7th grade science) | 410-555-0107 | p.venkataraman@calvaryshores.example |
| Registrar (SIS admin) | Colleen Mattingly | 410-555-0108 | registrar@calvaryshores.example |

Notes: Marguerite approves anything that costs money or touches the network. Joanne knows everything about who is where, call her first for onsite access. Dennis has the building keys and the alarm code, so he is also who you call if you are locked out at night. Priya is the unofficial teacher liaison and tests changes with her class before we roll them to everyone.

## Sites and addresses
| Site | Address | Notes |
|---|---|---|
| Main campus, Hartwell Building | 2200 Westbrook Lane, Salisbury, MD 21801 | Admin office, grades 3-8, MDF/server room (ground floor, behind the copy room) |
| Lower school, Pelican Wing | 2214 Westbrook Lane, Salisbury, MD 21801 | K-2, gym, cafeteria. Connected to Hartwell by fiber, IDF-2 in the janitor closet |

Hours: students 8:15-3:15 Mon-Fri, staff 7:30-4:30. Aftercare runs to 5:30 in the Pelican Wing, that room has a sign-in laptop. Building is locked outside those hours.

Access: check in at the front office (Hartwell). Sam keeps a visitor badge. Server room key is on the hook in the office manager's desk (ask Joanne) and Dennis has a spare. Server room has a small portable AC unit; if it trips, the room hits 90F in about an hour. Check it on every visit.

Closed: Christmas break, spring break, and all of July. Building is open for facilities staff only in July (HVAC and floors).

## Internet and circuits
| Item | Detail |
|---|---|
| Primary | Delmarva Link Fiber, 1 Gbps symmetric dedicated, E-rate funded (category 1) |
| Primary account ref | DLF-ACC-0048210 (fake ref, portal in vault) |
| Primary static block | 203.0.113.96/29 (usable .98 to .102, firewall WAN1 on .98) |
| Secondary | Bayline Broadband business cable, 500/50, DHCP |
| Secondary account ref | BBL-5521907 |
| Demarc | Hartwell MDF, ONT on the wall above the rack, Delmarva owns the ONT |
| Public DNS records | school website is hosted off-site (web host), only mail and a few records matter here |

- The firewall does WAN failover. Fiber is primary, cable is backup. Failover takes about 40 seconds, Google Meet calls will drop.
- Do NOT unplug or reset the ONT. If fiber is down, call Delmarva (see vendors) before touching anything. They need a ticket opened before dispatch.
- E-rate funded service: keep copies of every Delmarva invoice and service change. Marguerite files the forms with the school's E-rate consultant. We just give her the circuit details when she asks.
- Login for both ISP portals: `Vault: calvary-shores-academy/isp-portal`.
- Bandwidth is fine until state testing weeks (April), when every Chromebook is online at once. During testing, the cable backup is used for guest traffic only. Do not change this without asking Alex.

## Network
Firewall and core:
- Firewall: FortiGate 100F, HA pair (active/passive), `CSA-FW01` and `CSA-FW02`. Managed in the FortiGate GUI and FortiCloud. Firmware updates only in the summer window.
- Core switch: UniFi Switch Pro 48 PoE in Hartwell MDF. Access switches: UniFi Pro 24 PoE in IDF-1 (Hartwell second floor), IDF-2 (Pelican Wing). Fiber trunk between Hartwell and Pelican.
- Wi-Fi: UniFi U6 Pro APs, one per classroom (about 28 total) plus U6 Mesh in the gym and cafeteria. Controller runs on `CSA-HV01` as a VM (UniFi Network Application).
- Wi-Fi SSIDs: `CSA-Staff` (WPA2/WPA3 enterprise-ish, actually PSK, see gotchas), `CSA-Students` (student VLAN, Chromebooks only), `CSA-Guest` (isolated, captive portal, parent events).
- VPN: FortiClient SSL VPN for the admin office (3 users: Marguerite, Teresa, Colleen). Everyone else uses cloud tools. IPsec site-to-site is not in use. Check `sops/19-vpn-user-setup.md`.

VLANs:
| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 10 | Staff | 10.40.10.0/24 | Staff laptops and PCs, wired and Wi-Fi |
| 20 | Students | 10.40.20.0/22 | Chromebooks, iPads. Internet only, filtered. 1022 hosts is enough |
| 30 | Guest | 10.40.30.0/24 | Isolated, captive portal, 4 hour lease |
| 40 | VoIP | 10.40.40.0/24 | Desk phones, hosted PBX |
| 50 | Cameras | 10.40.50.0/24 | UniFi Protect NVR and cameras, no internet |
| 60 | Servers/Mgmt | 10.40.60.0/24 | Hyper-V host, VMs, switch and AP management, Datto |
| 70 | Printers | 10.40.70.0/24 | Copiers and label printers, static only |

DHCP and DNS:
- Staff, VoIP, printers: DHCP from `CSA-DC01` (staff and VoIP) and static for printers. Students, guests: DHCP from the FortiGate.
- DNS: internal AD DNS on `CSA-DC01` (10.40.60.10) for staff and servers. Student VLAN uses DNSFilter resolvers via the FortiGate, with Securly in the Chromebook extension on top. That is two filters on purpose.
- Student VLAN rules: internet only (TCP 80/443, DNS, NTP). No access to any other VLAN. The one exception is the Pelican library printer, reachable on port 9100 from VLAN 20 only (ask Alex before changing).
- Rule changes: submit per `sops/18-firewall-rule-change-request.md`. Marguerite signs off on anything that opens student traffic.

## Servers and line-of-business apps
| Name | Role | Notes |
|---|---|---|
| `CSA-HV01` | Hyper-V host (Dell PowerEdge R450, 2022 purchase) | Hosts all VMs below |
| `CSA-DC01` | Domain controller, DHCP, DNS (Windows Server 2022) | 10.40.60.10 |
| `CSA-FS01` | File server (Windows Server 2022) | Admin office shares, finance shares, scan folders |
| `CSA-UNIFI` | UniFi controller VM (Ubuntu) | Also hosts Protect NVR config backup |
| `CSA-WS-001` to `CSA-WS-038` | Windows PCs | Admin office, labs, aftercare |

Apps:
- PowerSchool (SIS), hosted by vendor. Registrar manages accounts. We only help with browser and SSO issues.
- FACTS tuition billing, cloud. Teresa and Marguerite use it.
- QuickBooks Desktop Pro on two admin PCs (`CSA-WS-003` for Marguerite, `CSA-WS-004` for Teresa), company file on `CSA-FS01\Finance`. Only one user in multi-user mode at a time.
- Securly (student web filter and classroom view), console owned by Alex.
- GoGuardian Teacher is licensed but only the 7th and 8th grade teachers use it. Priya will tell you if it breaks.
- Google Workspace for Education, see below.
- Hosted VoIP PBX (Harborline Voice). Phones are on VLAN 40, we only manage the network side.
- Library catalog (Follett Destiny) is cloud. Nothing local.
- Windows PCs are the only machines with N-central, SentinelOne and DNSFilter agents. Chromebooks use Google policy plus Securly.

## Microsoft 365 / Google tenant notes
Google Workspace for Education (primary tenant):
- Domain `calvaryshores.example`. Education Plus licenses for staff, Education Fundamentals for students.
- Student accounts: `firstname.lastname.YY@students.calvaryshores.example` where YY is graduating year. Provisioned from SIS export by the registrar on the first week of August.
- Org units: `/Staff`, `/Students/K-2`, `/Students/3-5`, `/Students/6-8`, `/Chromebooks/Carts`, `/Chromebooks/Loaners`. Policies (apps, extensions, forced re-enrollment, sign-in restriction to domain) are set per OU. Do not move a device out of its OU without writing it down.
- Chromebooks are enrolled with forced re-enrollment. Wiped devices re-enroll to `/Chromebooks/Loaners` until Jordan moves them.
- Student email can only send to and receive from `calvaryshores.example` and an allow list of parent domains. Allow list is in Admin console > Apps > Gmail > Compliance.
- Super admin accounts: two named admins (Alex, Casey) plus break glass. `Vault: calvary-shores-academy/google-super-admin-breakglass`.
- Graduation: the 8th grade class is suspended (not deleted) on June 30. Deletion is Casey's call after 90 days.

Microsoft 365 Business Premium (small tenant):
- Tenant uses the sub-domain `office.calvaryshores.example` for mail, because the main `calvaryshores.example` domain mail is on Google. Only 6 finance and admin users use Outlook. Confusing, see gotchas.
- 8 licenses (6 admin, 1 spare, 1 shared). MFA via Microsoft Authenticator, conditional access baseline on.
- Break glass: `Vault: calvary-shores-academy/m365-global-admin-breakglass`.
- Proofpoint Essentials covers this tenant only. License changes per `sops/14-m365-license-changes.md`.

## Backup
- Datto SIRIS appliance (`CSA-BDR01`, rack in Hartwell MDF) backs up `CSA-HV01`, `CSA-DC01`, `CSA-FS01`, `CSA-UNIFI`. Image-based, cloud replication on. Retention per Datto default plus 1 year on finance share.
- Datto SaaS Protection covers both the Google Workspace tenant (Gmail, Drive, shared drives for staff only) and the M365 tenant. Student accounts are NOT backed up. The school knows. Signed off by Marguerite in 2025.
- Daily check by whoever is on help desk, see `sops/08-daily-backup-check.md`.
- Quarterly restore test: pick one VM, one file share restore, one Google Drive item. Log results in the Accelo ticket and send to Marguerite. Last done: 2026-09-23 (passed, file restore took 40 min because someone picked the wrong snapshot).
- Chromebook data lives in Google. There is no local backup of Chromebooks.

## Printers, scanners, and other devices
- Ricoh MP C3004 copiers (3): Hartwell front office, Hartwell second floor workroom, Pelican Wing. Leased through a Ricoh dealer. Scan-to-email uses SMTP relay (see gotchas). Static IPs in 10.40.70.21-23.
- HP LaserJet Pro M404 in the business manager's office (10.40.70.40).
- Brother QL label printers (2) at the front office and library, USB to the PCs only.
- Pelican library: Brother laser reachable from the student VLAN on port 9100 only.
- 6 smartboards (Promethean), each with a small OPS PC that is NOT domain joined. Teachers log in with Google.
- 2 Chromebook charging carts per grade level. Cart numbers are on the white labels. Tracking sheet is in the shared drive `IT > Chromebook Inventory`.
- Door access system: managed by the alarm vendor, not by us.
- UniFi Protect cameras (about 24) on VLAN 50. Footage retention 30 days on the NVR. Dennis can pull footage, not us unless Marguerite asks.

## Vendor contacts
| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | NOC desk (ask for Brandon Teague, account rep) | 302-555-0141 | Circuit ID DLF-ACC-0048210, say E-rate site |
| Bayline Broadband | Support line | 410-555-0172 | Backup cable, account BBL-5521907 |
| Harborline Voice | Support, rep Nina Castellano | 410-555-0109 | Hosted PBX and desk phones |
| Chesapeake Copier Co. (Ricoh dealer) | Service line | 410-555-0110 | Copier lease and toner |
| Securly | Support portal | n/a | Alex owns the admin console |
| PowerSchool | Support portal | n/a | Registrar opens tickets |
| E-rate consultant (Wexford Education Funding) | Gil Ramsay | 410-555-0111 | Marguerite's contact, not ours |
| Dell ProSupport | Portal | n/a | R450 service tag in the server room label |

## Gotchas / tribal knowledge
1. Never reboot or patch anything in the first two weeks of school or during state testing (April). If a patch is critical, call Marguerite and Joanne first.
2. The summer maintenance window is the last week of June through mid-July. Sam is onsite. Firmware, Windows feature updates, switch firmware, Chromebook OS pinning changes, and the Hyper-V host patch all happen then. Plan it in May.
3. Chromebook carts: if a whole cart fails to join Wi-Fi, check the cart's charger first. A loose power strip once took down 30 machines' charge and they all lost the Wi-Fi profile after a policy refresh.
4. The scanners on the Ricoh copiers only send mail through the SMTP relay on port 465 with a dedicated relay account (not port 587). Moving the relay broke scan-to-email for a week in 2025. See `sops/17-scan-to-email-troubleshooting.md`.
5. The `CSA-Staff` SSID uses a shared passphrase, not 802.1X. Rotate it each summer and hand out the new one at the August staff meeting. `Vault: calvary-shores-academy/wifi-psk`.
6. Two tenants (Google primary, M365 for finance). When someone says "my email is broken", ask which one. Marguerite's mail is in Outlook, Joanne's is in Gmail.
7. Student VLAN is a /22. If DHCP runs out in the Pelican Wing (all K-2 iPads wake up at once), look for stale leases from the summer and shorten the lease to 4 hours.
8. Securly sometimes blocks a teacher's legit video site on a Monday after a category update. Priya or the teacher emails Alex, Alex whitelists in the Securly console. Do not disable the filter to "test".
9. The server room portable AC trips on the same circuit as the copy machine. If the copier is running a big job and the AC dies, the Hyper-V host alarms with an overheat warning. Keep the door propped and call Dennis.
10. Datto SIRIS is plugged in below the switch on the same UPS as the host. The UPS battery is replaced every 3 years (due in the 2027 summer window).
11. Teacher laptops (Windows) sometimes lose the mapped `S:` drive after sleep. Known issue, fix is a GPO tweak in the Staff OU plus a reboot. Documented in T-24390 but not fixed for 3 laptops.
12. Fire marshal rules: do not cable through the stairwell. Sam learned this the hard way.
13. School events: the cafeteria projector and the mic mixer are on the guest VLAN by accident. Leave it, the events team likes it that way.

## Credential references
- Firewall: `Vault: calvary-shores-academy/firewall-admin`
- Switch/AP controller: `Vault: calvary-shores-academy/switch-admin`
- Wi-Fi staff PSK: `Vault: calvary-shores-academy/wifi-psk`
- Wi-Fi guest portal admin: `Vault: calvary-shores-academy/wifi-guest-admin`
- Google super admin break glass: `Vault: calvary-shores-academy/google-super-admin-breakglass`
- M365 global admin break glass: `Vault: calvary-shores-academy/m365-global-admin-breakglass`
- Domain registrar: `Vault: calvary-shores-academy/domain-registrar`
- ISP portals: `Vault: calvary-shores-academy/isp-portal`
- Datto BDR: `Vault: calvary-shores-academy/backup-appliance`
- Copier admin: `Vault: calvary-shores-academy/printer-admin`
- Securly console: `Vault: calvary-shores-academy/securly-admin`
- Domain admin (CSA-DC01): `Vault: calvary-shores-academy/ad-domain-admin`

## Change log
- 2026-10-09 (Alex Rivera): Annual review. Updated contacts after Teresa Quillen took over AP. Confirmed backup scope with Marguerite. T-25203.
- 2026-09-23 (Jordan Blake): Quarterly restore test passed (VM, file share, Drive item). Results sent to Marguerite.
- 2026-07-08 (Alex Rivera, Sam Okafor): Summer window complete. FortiGate firmware upgraded, UniFi switch firmware updated, Hyper-V host patched. WiFi PSK rotated. T-24980.
- 2026-06-30 (Jordan Blake): 8th grade Google accounts suspended. Loaner OU cleaned.
- 2026-04-14 (Alex Rivera): Added cable backup rule so guest traffic only during state testing.
- 2026-02-17 (Sam Okafor): Replaced two failed U6 Pro APs in Pelican Wing, relabeled all APs with room numbers.
- 2025-11-04 (Casey Morgan): Added GoGuardian note after teacher complaint. Omni+ Managed renewal notes moved to Accelo contract.
- 2025-08-12 (Alex Rivera): Student VLAN grown from /23 to /22 after the Pelican iPads ran out of leases.

# Cypress Swamp Builders

owner: Alex Rivera
last_reviewed: 2026-09-14
tags: construction, omni-basic, procore, bluebeam, job-trailers, fortigate, selbyville-de, sage-300-cre
client_id: 1011
slug: cypress-swamp-builders
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Omni+ Server, Server Backup, Omni+ Backup, Email Management
industry: Construction
employees: 41

## Overview

General contractor doing light commercial and multifamily work in southern Delaware and the Maryland line. 41 users total: about 14 in the Selbyville office (owners, estimating, accounting, project managers, admin) and about 27 field staff (superintendents, assistant supers, foremen with company tablets). Most field people use a phone or an iPad and rarely touch a PC. Superintendents each have a laptop that lives in a job trailer.

The business runs on Procore (project management, RFIs, submittals, daily logs), Bluebeam Revu (plan markup and takeoffs), and Sage 300 CRE for job cost and accounting. Estimating also uses On-Screen Takeoff on two workstations.

Office is a single building. Active job sites change every few months. At the time of the last review there were three active trailers (see Sites). The owner, Dale Whitcomb (fictional), cares most about two things: the superintendents can get on the internet at a new site fast, and plans open quickly on the tablets.

Related docs: `sops/01-new-client-onboarding.md`, `sops/35-isp-outage-troubleshooting.md`, `sops/19-vpn-user-setup.md`, `sops/33-onsite-visit-checklist.md`.

## Service plans and contract notes

- Core plan: Omni+ Basic (Accelo contract C-1011-A, renews each January 1).
- Add-ons: Omni+ Server, Server Backup, Omni+ Backup, Email Management.
- First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Onsite visit on a scheduled interval by agreement: first Tuesday of every other month (Feb, Apr, Jun, Aug, Oct, Dec). Sam Okafor does these. Extra visits are billed at the standard onsite rate.
- Job trailer setup is NOT included in the monthly fee. It is a project (4 hours flat, billed under a P-0xxx project per site). Equipment (router, cellular plan) is billed to Cypress at cost plus 10 percent.
- Datto SaaS Protection for M365 (Omni+ Backup add-on) and the Datto SIRIS appliance in the server closet (Server Backup add-on) are covered under the add-ons.
- 41 seats billed. Seasonal laborers do not get seats. If Dale asks for a "temporary user," check with Casey first, it is billed per seat per month, no proration.
- Casey Morgan handles contract and billing questions. Do not quote prices at the client.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dale Whitcomb (Owner / President) | 302-555-0117 | dale.whitcomb@cypressswamp.example |
| Billing | Marlene Pruitt (Controller) | 302-555-0118 | marlene.pruitt@cypressswamp.example |
| After-hours | Tyrell Banks (Operations Manager) | 302-555-0119 | tyrell.banks@cypressswamp.example |
| Office manager | Gwen Alder | 302-555-0125 | gwen.alder@cypressswamp.example |
| Lead estimator | Rob Hastings | 302-555-0126 | rob.hastings@cypressswamp.example |
| Senior superintendent | Luis Ferrer | 302-555-0127 | luis.ferrer@cypressswamp.example |

Notes:
- Tyrell answers after-hours calls for outages. Do not call Dale at night unless Tyrell says to.
- Gwen is the day to day contact for new hires and equipment. She approves new user requests, Marlene signs off on anything that costs money.
- Luis is the person to ask when a job site is down. Superintendents will text him before they call us.

## Sites and addresses

| Site | Address | Notes |
|---|---|---|
| Main office | 1180 Coastal Highway Suite B, Selbyville, DE 19975 | Server closet in the back hall. Hours 7:00-4:30 Mon-Fri. Key code on file in Accelo (client record > Access notes). |
| Yard / shop | 412 Pump Station Road, Selbyville, DE 19975 | Equipment storage, no network, one cellular camera. Not covered by us. |
| Job trailer: Harbor Pines (multifamily) | Lot 6 Ridge Lane, Millsboro, DE 19966 | Active. Superintendent Luis Ferrer. Cellular router. |
| Job trailer: Route 54 Retail | 20 Bayard Road, Frankford, DE 19945 | Active. Superintendent Nina Okoye. Cellular router. |
| Job trailer: Dagsboro Medical Office | 88 Clayton Street, Dagsboro, DE 19939 | Active. Superintendent Pete Wallace. Wired internet from site utility trailer, see below. |

Access notes:
- Office: front door is unlocked 7:00-4:30. After hours call Tyrell to get someone to let you in. Alarm panel is by the back door, code is in Accelo access notes only.
- Trailers: locked with a combination padlock. Superintendent has the combo. Do not ask the office, they do not have it.
- Hard hats and safety vest required on any job site. Sam keeps a set in the truck. Remote tech work never needs a site visit if the router is up.

## Internet and circuits

Main office:
- ISP: Delmarva Link Fiber, 500/500 symmetrical fiber, business class.
- Account ref: DLF-88-20417 (fictional). Support: 302-555-0150.
- Static IP block: single static 203.0.113.41 on the FortiGate WAN1.
- ONT is in the server closet on the left wall, powered from its own wall wart. Do not unplug the power strip next to it, it also feeds the Datto.
- Backup circuit: Bayline Broadband business cable, 300/30, WAN2, dynamic IP, account BB-5521907. Failover is automatic (FortiGate SD-WAN rule, health check to 198.51.100.10 and 198.51.100.11).
- Bayline cable modem sits on the shelf above the Datto. If WAN2 shows down in N-central, power cycle the modem first.

Job trailers (this is the part people forget):
- Each trailer gets a Cradlepoint-style cellular router (R-series) with a business data plan on a carrier pooled account. Carrier account is in the vault, see below. Pool is 600 GB per month shared across all trailers.
- Router naming: CSB-TRL-HP (Harbor Pines), CSB-TRL-R54 (Route 54), CSB-TRL-DMO (Dagsboro). The router is monitored by SNMP ping from N-central, but it does NOT run an agent.
- Each trailer router broadcasts one SSID, `CSB-Trailer-<site code>`. Superintendents and the trailer plotter/printer connect to it. The PSK is the same for all trailers and is rotated yearly.
- Dagsboro has a wired drop from the site utility trailer provided by the general site owner. It is dirty: DHCP only, often slow, sometimes blocks VPN. The cellular router is still there as backup, plugged into WAN2.
- Typical throughput on LTE is 20-60 Mbps down. Procore and Bluebeam Studio are fine. Large PDF sets (over 150 MB) are slow, tell supers to sync the project folder before they leave the office.
- Trailer routers use a VPN back to the office FortiGate for file share access (IPsec, site-to-site, one tunnel per trailer). If the tunnel is down but the internet works, Procore and M365 still work, only the S: drive does not.

## Network

Firewall:
- FortiGate 60F, hostname `CSB-FW01`, FortiOS 7.2.x (check version before touching, we were on 7.2.8 at last review).
- LAN gateway 192.168.20.1.
- Management only from the LAN VLAN 20 and from our RMM jump host. WAN admin is disabled.
- Config backup runs weekly via N-central script to the Datto share. Last known good backup is from the monthly review.

Switching and Wi-Fi:
- Core switch: Ubiquiti UniFi USW-24-PoE in the server closet (`CSB-SW01`).
- Access switch in the estimating room: UniFi USW-Lite-8-PoE (`CSB-SW02`).
- APs: 3x UniFi U6-Pro (front office, estimating, back hall). Controller is the UniFi Network app running on CSB-SRV01.
- Wi-Fi SSIDs: `CSB-Corp` (WPA2/WPA3, VLAN 20), `CSB-Guest` (isolated, VLAN 40, captive portal off, rotating PSK).

VLANs:

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 20 | Corp | 192.168.20.0/24 | Workstations, server, printers |
| 30 | Devices | 192.168.30.0/24 | Cameras, plotter, time clock |
| 40 | Guest | 192.168.40.0/24 | Visitors, subcontractors in the office |
| 99 | Mgmt | 192.168.99.0/24 | Switches, APs, FortiGate |

DHCP and DNS:
- DHCP is served by the FortiGate, scope 192.168.20.100-192.168.20.230 on VLAN 20.
- Static range 192.168.20.2-192.168.20.99 (server .10, printers .50-.59, Datto .30).
- Internal DNS is CSB-SRV01 (AD DNS). Forwarders go to DNSFilter resolvers.
- AD domain: `cypressswamp.local` (old naming, do not rename it, accounting software license is tied to it).

VPN:
- FortiClient SSL VPN for the five office staff who work from home. Group `VPN-Users` in AD.
- MFA via FortiToken Mobile. If someone swaps phones see `sops/32-new-phone-mfa-device-swap.md`.
- Site-to-site IPsec to each trailer router (see Internet).

## Servers and line-of-business apps

| Device | Role | Notes |
|---|---|---|
| CSB-SRV01 | Domain controller, file server, UniFi controller | Windows Server 2019, Dell PowerEdge T350, 64 GB RAM. |
| CSB-SRV02 | Sage 300 CRE, SQL | Windows Server 2022 VM on a separate small host. Do not install anything else on it. |
| CSB-DATTO01 | Datto SIRIS | Image backup and local virtualization. |

Line of business:
- Sage 300 CRE (accounting, job cost, payroll). Marlene and two accounting staff use it. Month-end close is the 5th-8th of each month, no maintenance those days.
- Procore: cloud, SSO is not enabled. Users have their own logins tied to cypressswamp.example addresses. Procore admin is Gwen. If a super says "Procore won't send RFIs," it is almost always the mailbox rule, not Procore.
- Bluebeam Revu 21: licensed per seat, 14 seats (estimators and PMs). License admin is Rob Hastings. Studio Projects are on Bluebeam's cloud, not our server.
- On-Screen Takeoff: 2 seats on CSB-WS-006 and CSB-WS-007 (estimating). USB dongle license on CSB-WS-006, do not lose it.
- Adobe Acrobat Pro: 6 seats.
- Plan files live on `S:\Projects` (CSB-SRV01). Roughly 1.4 TB. Drawings are big, so expect slow first-opens over VPN.
- Field tablets: 18 iPads managed with Intune (see M365). They run Procore, Bluebeam, and Teams.

Device naming: workstations `CSB-WS-001` through `CSB-WS-0xx`, super laptops `CSB-LT-<name>`, e.g. `CSB-LT-FERRER`.

## Microsoft 365 / Google tenant notes

- Tenant: cypressswamp.onmicrosoft.com. Primary domain cypressswamp.example.
- Licenses: 41 Microsoft 365 Business Premium (all users), plus 4 Exchange Online shared mailbox (free) for `estimating@`, `ap@`, `info@`, `safety@`.
- Defender for Business is on. SentinelOne is the EDR on Windows endpoints, installed by N-central policy.
- MFA enforced for everyone via Conditional Access. Exception: two shared tablets in the Harbor Pines trailer sign in with a device-based policy, no user MFA prompt.
- Intune enrolls the iPads. Supervised mode, Procore and Bluebeam pushed as required apps.
- Global admin accounts: two named (Alex and Casey). Breakglass account exists, never used.
- Domain registrar: managed under Casey, see vault.
- DKIM and SPF are set. DMARC is at p=quarantine. Do not move to reject without asking Gwen, a lot of vendors send as the company.
- Datto SaaS Protection covers Exchange, OneDrive, SharePoint, and Teams.

## Backup

- Datto SIRIS (`CSB-DATTO01`) backs up CSB-SRV01 and CSB-SRV02 every hour. Daily offsite replication to Datto cloud.
- Retention: local 30 days, cloud 1 year (standard Server Backup settings).
- Datto SaaS Protection backs up M365 mailboxes and OneDrive daily.
- Daily backup check per `sops/08-daily-backup-check.md`. Failures in N-central come in as Warning, two missed in a row is Critical.
- Restore test is run twice a year (not quarterly, that is Omni+ Managed only). Last one was done by Alex in April.
- Workstations are NOT backed up. Users are told to save to S: or OneDrive. Superintendent laptops have OneDrive Known Folder Move turned on so Desktop and Documents sync.
- Datto is plugged into a UPS (APC 1500). Battery was replaced in 2025.

## Printers, scanners, and other devices

| Device | Location | IP | Notes |
|---|---|---|---|
| Ricoh MP C3004 | Front office | 192.168.20.50 | Scan to email via M365 SMTP relay on 587. Admin in vault. |
| HP LaserJet M507 | Accounting | 192.168.20.51 | Checks. Uses MICR toner cartridge, do not swap in a standard cart. |
| HP DesignJet T850 plotter | Estimating | 192.168.30.20 | 36 inch. Plots from Bluebeam. Driver issues after Windows updates. |
| HP DesignJet T650 | Harbor Pines trailer | DHCP from trailer router | Pinned by MAC on router. |
| Brother MFC | Reception | 192.168.20.52 | Fax line is VoIP (Bayline), still used for lien notices. |
| Time clock (shop) | Yard | cellular | Not ours, vendor managed. |

- Cameras: 6 Reolink-style IP cameras on VLAN 30. Owned by Dale, installed by a local electrician. We do not monitor them.
- Phones: Teams Phone for office, mobile phones for field. Not covered by our agreement beyond Teams config.

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Priya Raman (business accounts) | 302-555-0151 | Fiber support 24x7 at 302-555-0150. |
| Bayline Broadband | Support desk | 302-555-0152 | Cable backup circuit. Ticket number needed. |
| Sage reseller (Coastal Business Systems) | Dennis Aguilar | 302-555-0153 | Handles Sage 300 CRE updates. Call before applying any SQL patch. |
| Bluebeam admin | Rob Hastings (internal) | 302-555-0145 | We do not have vendor admin rights. |
| Procore admin | Gwen Alder (internal) | 302-555-0144 | Same. |
| Cellular carrier (pooled plan) | Business support | 302-555-0154 | Pool owner is Cypress. We have a delegate login. |
| Datto | Partner portal | n/a | Open tickets through Casey. |

## Gotchas / tribal knowledge

1. New job trailer setup: ship the router to Luis or the super BEFORE they get to the site. Plug in, we remote in and configure. Plan on a Monday, not a Friday.
2. If a trailer router shows offline in N-central, check the pooled data cap before driving anywhere. At 100 percent the carrier throttles to 128 kbps and the router looks "up" but nothing works. Casey can ask the carrier to raise the cap.
3. Procore mobile app drops sign-in on iPads after the Intune policy refreshes. Fix: sign out and back in, MFA again. Known issue, no permanent fix.
4. Sage 300 CRE stops working if CSB-SRV02 time drifts more than 5 minutes. It happened once after a power blip. Check w32tm status first.
5. Bluebeam seat count is 14. When a new PM starts, there is no spare seat. Ask Rob which seat to free up before promising anything.
6. Estimating (Rob) opens 400 MB plan sets over VPN from home. It works but is slow. Tell him to use OneDrive offline copy instead of the VPN.
7. The plotter driver on Windows 11 24H2 breaks. Roll back to the 2023 driver, saved on S:\IT\Drivers. Do not let Windows Update replace it (driver update blocked in N-central policy).
8. Monday morning after a storm: check the main office UPS before anything else. The closet UPS is old and sometimes does not come back on its own.
9. The office has a very old door buzzer that runs off the same power strip as the Bayline modem. If someone says "internet is down and the buzzer is dead too," it is the power strip.
10. Subcontractors ask for guest Wi-Fi constantly. Give them `CSB-Guest`, never `CSB-Corp`. The guest PSK is on a sign in the break room and rotates quarterly. See `sops/20-wifi-guest-network.md`.
11. Do not push Windows feature updates in the summer months without checking with Gwen. Estimating hits bid deadlines and cannot lose a workstation.
12. Superintendent laptops sit in hot trailers. We have seen three dead batteries. Check battery health when Sam is onsite.

## Credential references (vault paths only)

- Vault: cypress-swamp-builders/firewall-admin
- Vault: cypress-swamp-builders/switch-admin
- Vault: cypress-swamp-builders/wifi-psk
- Vault: cypress-swamp-builders/wifi-psk-trailers
- Vault: cypress-swamp-builders/domain-registrar
- Vault: cypress-swamp-builders/isp-portal
- Vault: cypress-swamp-builders/isp-portal-backup-cable
- Vault: cypress-swamp-builders/cellular-carrier-pool
- Vault: cypress-swamp-builders/m365-global-admin-breakglass
- Vault: cypress-swamp-builders/backup-appliance
- Vault: cypress-swamp-builders/lob-app-admin (Sage 300 CRE SQL admin)
- Vault: cypress-swamp-builders/printer-admin

## Change log

- 2026-09-14: Annual review. Added Dagsboro trailer, updated trailer router names. Alex Rivera. T-26418.
- 2026-07-02: Replaced plotter driver, blocked driver updates in N-central policy. Sam Okafor. T-26077.
- 2026-04-08: Semiannual restore test of CSB-SRV02 to Datto virtualization, passed. Alex Rivera. T-25502.
- 2026-02-10: Rotated trailer Wi-Fi PSK (yearly). Jordan Blake. T-25140.
- 2025-11-18: FortiOS upgraded to 7.2.8 after approval from Gwen. Alex Rivera. T-24731.
- 2025-08-05: Added Route 54 trailer, new cellular router. Sam Okafor. P-0412.
- 2025-03-12: Moved SaaS Protection to cover Teams. Jordan Blake. T-23988.

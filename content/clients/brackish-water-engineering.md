# Brackish Water Engineering

owner: Alex Rivera
last_reviewed: 2026-10-12
tags: engineering, autocad, civil-3d, file-server, license-server, plotter, omni-managed, seaford-de, two-sites
client_id: 1008
slug: brackish-water-engineering
core_plan: Omni+ Managed
service_plans: Omni+ Managed, Omni+ Advanced Security, Omni+ Server, Server Backup, Hosted Cloud Server, Omni+ Passportal
industry: Engineering
employees: 27

## Overview
Civil and environmental engineering firm in Seaford, DE. 27 staff: 4 principals, 12 engineers/designers (CAD and Civil 3D heavy), 4 survey/field staff, 3 environmental scientists, 2 admin, 1 office manager, 1 IT-minded engineer (Neil Aldridge, our unofficial point person on site).

Work is stormwater, wastewater, site design and permitting for county and municipal clients in Delaware and Maryland. Deliverables are big: Civil 3D drawings with xrefs, survey point clouds, PDF permit sets, and plots on 24x36 and 36x48 paper. A project folder can be 40 GB or more.

The business runs on three things: the file server (BWE-SRV01), the Autodesk license server (BWE-SRV02), and the plotter. If any of those is down on a deadline day, it is a P1 for them even if our priority matrix says P2.

Second site: small field office in Georgetown, DE (3 people, survey and inspection). Connected by site-to-site VPN.

## Service plans and contract notes
- Core plan: Omni+ Managed. N-central agent on all managed devices and servers, SentinelOne, DNSFilter, Proofpoint Essentials, Datto SIRIS with cloud replication, Datto SaaS Protection for M365.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Hosted Cloud Server, Omni+ Passportal.
- Response targets: P1 15 minutes (24x7), P2 1 hour (extended hours 7:00-7:00), P3 2 business hours, P4 next business day.
- Quarterly business review (QBR): first week of the quarter, with the principal Robert Tolliver and Neil. Casey Morgan runs it, Alex supplies the numbers.
- Quarterly restore tests: required. See backup section and `sops/09-backup-restore-test.md`.
- Priority onsite. Sam can usually be at Seaford within 90 minutes during business hours.
- Contract renews in March. Includes up to 2 onsite emergency dispatches a year without a trip charge. Track usage in Accelo.
- Autodesk subscriptions are bought by the client through their reseller (not through us). We only manage the license server and installs.
- Hardware refreshes are on a 5-year cycle for workstations. Workstations with 3D workloads are on a 4-year cycle.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Neil Aldridge (Senior Designer, IT liaison) | 302-555-0100 | neil.aldridge@brackishwater.example |
| Billing | Carol Fenn (Office Manager) | 302-555-0101 | carol.fenn@brackishwater.example |
| After-hours | Robert Tolliver (Principal) | 302-555-0115 | robert.tolliver@brackishwater.example |
| Backup after-hours | Neil Aldridge (cell) | 302-555-0116 | neil.aldridge@brackishwater.example |
| Georgetown office lead | Dana Whitlock (Survey Lead) | 302-555-0155 | dana.whitlock@brackishwater.example |
| Principal (contracts) | Elaine Marsh-Kent | 302-555-0156 | elaine.marshkent@brackishwater.example |

Main line: 302-555-0150. For plotter or license problems call Neil first, he usually knows what changed.

## Sites and addresses
- HQ: 402 Stein Highway Annex, Seaford, DE 19973. Two-story office, server room on the first floor behind the print room.
- HQ hours: Mon-Fri 7:30-5:30. Engineers often work late near deadlines, so after-hours calls from here are real, not noise.
- Georgetown field office: 31 The Circle, Suite 210, Georgetown, DE 19947. Hours Mon-Fri 7:00-4:30. Access via the building manager, ask Dana to let us in.
- HQ server room is a locked room with its own AC split unit. If the AC alarm texts Neil, call us too. The room hits 85F within 40 minutes of a failure.
- HQ parking: back lot, enter through the print room door. Deliveries (paper rolls, plotter ink) also come through this door.

## Internet and circuits
HQ:
- Primary: Delmarva Link Fiber, 1 Gbps symmetric dedicated fiber. Static IP block 203.0.113.80/29 (usable .81-.86). Firewall WAN uses 203.0.113.81.
- Secondary: Bayline Broadband business cable, 400/40, DHCP, dynamic address, failover only.
- Account refs: DLF-90117 (primary), BB-0061440 (secondary) (both fake).
- Portals: `Vault: brackish-water-engineering/isp-portal`.
- ONT and cable modem both in the server room on the top shelf of the rack.

Georgetown:
- Bayline Broadband business cable, 300/30. Single static IP 198.51.100.115.
- Account ref: BB-0071935 (fake).
- No failover. When Georgetown cable is down, staff use phone hotspots and connect to the HQ resources by FortiClient VPN on their laptops.

SD-WAN / failover behavior at HQ: FortiGate uses the secondary only when the primary fails health checks (ping to 192.0.2.53 and 192.0.2.54 both fail). Failover takes about 20 seconds. Site-to-site VPN reconnects after another 30. Expect plot jobs and file saves to drop during the switch.

See `sops/35-isp-outage-troubleshooting.md`.

## Network
- HQ firewall: FortiGate 100F pair in HA active-passive (BWE-FW01 and BWE-FW02). FortiOS upgrades are scheduled for the maintenance window, Sunday 6:00-9:00 AM, with 2 weeks notice to Neil.
- Georgetown firewall: FortiGate 40F (BWE-FW-GTN).
- HQ core switch: Ubiquiti UniFi Enterprise 48-port PoE (BWE-SW-CORE) with 10G uplink to the server room switch.
- Server room switch: UniFi Pro Aggregation (BWE-SW-SRV), 10G ports to BWE-SRV01, BWE-SRV02 and the Datto appliance.
- Access switches: 3 UniFi 24-port PoE (BWE-SW-F1-A, BWE-SW-F1-B, BWE-SW-F2-A), one per section of the floor.
- Wi-Fi: 8 UniFi U6 Pro APs at HQ, 2 at Georgetown. Three SSIDs: BWE-Staff (802.1X with Entra ID RADIUS proxy), BWE-Guest, and BWE-Field (WPA2 PSK, for tablets and survey data collectors).
- DHCP: on the FortiGate at both sites. DNS: domain controllers at HQ (BWE-DC01 and BWE-DC02), forwarding to DNSFilter.
- Site-to-site VPN: IPsec between BWE-FW01 and BWE-FW-GTN. Georgetown users reach the file server over it, access to large CAD files is slow (see gotchas).
- Remote VPN: FortiClient with MFA (FortiToken Mobile) for field and remote staff. Policy per `sops/19-vpn-user-setup.md`.

| VLAN | Site | Name | Subnet | Notes |
|---|---|---|---|---|
| 10 | HQ | Staff | 10.50.10.0/24 | Workstations, laptops |
| 20 | HQ | Servers | 10.50.20.0/24 | BWE-SRV01, BWE-SRV02, DCs, Datto |
| 30 | HQ | Print/Plot | 10.50.30.0/24 | Plotter, copiers, scanners |
| 40 | HQ | Guest | 10.50.40.0/24 | Internet only |
| 50 | HQ | Field/Survey | 10.50.50.0/24 | Tablets, GPS data collectors, drone laptop |
| 60 | HQ | VoIP | 10.50.60.0/24 | Phones |
| 110 | Georgetown | Staff | 10.50.110.0/24 | All Georgetown devices |
| 140 | Georgetown | Guest | 10.50.140.0/24 | Internet only |

Static addresses: BWE-SRV01 10.50.20.10, BWE-SRV02 10.50.20.11, BWE-DC01 10.50.20.5, BWE-DC02 10.50.20.6, Datto 10.50.20.20, plotter 10.50.30.10.

## Servers and line-of-business apps
- BWE-HV01: Hyper-V host (Dell R750), hosts BWE-DC01, BWE-DC02 (VMs) and BWE-SRV02 (license server VM). 128 GB RAM.
- BWE-SRV01: physical file server (Dell R750xs), Windows Server 2022, 12 x 4 TB RAID 10 (about 22 TB usable). Holds the project share, archive share, and user home folders. Mapped as P: (Projects), A: (Archive), H: (Home). Do not change drive letters, Civil 3D and xrefs depend on them.
- Project share structure: `P:\<year>\<project number>-<short name>\` with fixed subfolders (CAD, Survey, Docs, Plots, Permits). Rules are on a one-page sheet in the shared drive.
- BWE-SRV02: Autodesk Network License Manager (FlexNet). Network licenses for AutoCAD, Civil 3D and a few Infrastructure Design Suite seats. Lmgrd port 27000, vendor daemon on fixed port 2080. Both are allowed on the HQ firewall and across the Georgetown VPN.
- Software on desktops: AutoCAD, Civil 3D, Bluebeam Revu for markups, Microsoft Office, Esri ArcGIS Pro on environmental staff PCs (named user licenses), HEC-RAS and SWMM (free, installed on request).
- Survey: Trimble Business Center on 3 workstations. Raw survey data is dropped into `P:\<year>\...\Survey` from data collectors via the Field VLAN.
- Drone processing: one workstation (BWE-WS-DRN) with a high-end GPU, runs photogrammetry jobs overnight. Excluded from patch reboots without a ticket.
- Autodesk Desktop licensing is a mix of named-user and network licenses. Neil keeps a spreadsheet of who has what, ask him before reassigning seats.
- Accounting: Deltek Ajera hosted by the vendor (browser). Carol manages it. Not ours.
- Active Directory: single domain, brackishwater.local, hybrid with Entra ID sync.

## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 27 licenses plus Power BI Pro for 2 principals, plus 3 shared mailboxes (info@, permits@, field@).
- Tenant domain: brackishwater.example. MFA enforced with Authenticator number matching. Field staff on tablets use a Conditional Access policy that requires a compliant device (Intune enrolled).
- SharePoint is used only for company policies and HR docs. Project files stay on the file server on purpose.
- Proofpoint Essentials is in front of the mailboxes (MX points at Proofpoint). Quarantine digest goes to Neil and Carol. Release requests come through Accelo.
- Retention: 7-year mail retention requested by a principal in 2025. Configure with Purview retention policy, not via archive mailboxes only.
- Datto SaaS Protection covers mailboxes, OneDrive and SharePoint.

## Backup
- Datto SIRIS appliance at HQ (BWE-BKP01), image backups of BWE-SRV01, BWE-SRV02, BWE-HV01 (VMs), BWE-DC01/02. Schedule: every hour 6:00 AM to 8:00 PM, then every 4 hours overnight. Offsite replication to Datto cloud, with throttling at 200 Mbps during business hours.
- Retention: local 60 days, cloud 1 year, annual archive snapshot kept 7 years (per client's engineering records requirement).
- BWE-SRV01 first full backup took 3 days. Any rollback to a new baseline needs planning with the client.
- Quarterly restore tests: pick one project folder and one VM. Restore to a lab environment and open a drawing in Civil 3D to confirm xrefs resolve. Log each test in Accelo and attach the screenshots. Last done 2026-07-08, passed. Next due week of 2026-10-05, in progress (see change log).
- Daily check per `sops/08-daily-backup-check.md`. Pay extra attention to screenshot verification failures on BWE-SRV01.
- Georgetown office has no local backup. Their files are on the HQ server through the VPN. Laptops use OneDrive Known Folder Move for Desktop and Documents only.
- Datto SaaS Protection for M365 runs daily.
- Field laptops are not backed up. Everything goes to the server.

## Printers, scanners, and other devices
- Large-format plotter: HP DesignJet T1700dr (BWE-PLT01), 44-inch, static 10.50.30.10. On the Print/Plot VLAN. Prints from the HP SmartStream driver on the plot-queue workstation. Rolls: 24-inch and 36-inch bond, swapped by the admin.
- Large-format scanner: Contex HD Ultra X 4250, used for old plan sheets. Software on one workstation only.
- Copiers: Canon imageRUNNER ADVANCE C5560i (BWE-CP01) and one at Georgetown. Scan to email uses M365 SMTP relay with a connector, source IP 203.0.113.81 (HQ). See `sops/17-scan-to-email-troubleshooting.md`.
- Color laser: HP Color LaserJet Pro M454 in the admin area.
- Survey equipment: Trimble data collectors (not managed), a drone controller laptop.
- 27 workstations/laptops: 14 engineering workstations with 32-64 GB RAM and workstation GPUs (BWE-WS-001 to -014), 9 laptops (BWE-LT-01 to -09), 4 field tablets (BWE-TB-01 to -04, Intune managed).
- Conference room: Teams Room device and a 75-inch display. Manages itself, ticket if it fails.
- UPS: APC Smart-UPS 3000 in the server room. Battery replacement scheduled yearly, last one March 2026.

## Vendor contacts
| Vendor | Rep | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Enterprise desk | 302-555-0191 | Account DLF-90117 (fake) |
| Bayline Broadband | Support | 302-555-0192 | Accounts BB-0061440 and BB-0071935 (fakes) |
| Autodesk reseller (Coastal CAD Supply) | Mitch Orlowski | 302-555-0193 | Licensing, seat counts, renewals |
| HP plotter service (Peninsula Print Partners) | Dispatch | 302-555-0194 | On-site plotter repairs, 4 business hour SLA |
| Trimble support reseller | Holly Dreyer | 302-555-0195 | TBC licensing |
| Fortinet partner contact | Our distributor | 302-555-0196 | RMA and licensing, Casey handles |
| Delaware building manager (Georgetown) | Pete Calloway | 302-555-0197 | Door access, building power outages |

## Gotchas / tribal knowledge
- Autodesk license server (BWE-SRV02) must be up by 7:00 AM. When the VM drops, everyone opens AutoCAD in "No license" mode and calls at 7:30. Check lmgrd in the Windows service list and the `lmtools` "Server Status". Restart "Autodesk Network License Manager" and, if needed, reread the license file. Log it in Accelo with category License.
- Never change the license server hostname or MAC. The license file is bound to it. A reissue from Autodesk takes 1-2 days.
- Drive letters P:, A:, H: are fixed. Civil 3D data shortcuts and xrefs break if a user maps their own P: to a different path. The login script maps them, do not map by hand.
- Large CAD files are painfully slow from Georgetown. Dana's team works from a local copy and syncs after hours with the "Sync to Server" scheduled task. Do not try to fix this with a firewall change, it is bandwidth and VPN overhead. A SD-WAN upgrade was quoted in 2026, still pending.
- Plotter queue: when a plot job hangs, the whole queue stops. Delete the stuck job in the print server queue on BWE-SRV01 and restart the "Print Spooler" service. Do not power cycle the plotter during a job, the head can misprint a whole roll.
- The plotter needs a static IP and has its own web console. If IT replaces the firewall, confirm DHCP exclusions so nobody else grabs 10.50.30.10.
- Backup on BWE-SRV01 runs during the evening when engineers are finishing deadlines. If users report slow saves at 6-8 PM, check Datto, it is probably the verification step. Do not pause the backup without asking Neil.
- Defender and SentinelOne exclusions are in place for `P:\` temp folders and the Civil 3D cache. Before removing or tightening an exclusion, run a test with a large drawing. Past change caused Civil 3D to hang for minutes on open.
- The drone workstation (BWE-WS-DRN) runs processing jobs that last up to 20 hours. Do not reboot it for patches without checking with Neil. Add a patch exclusion window in N-central for the device when a job is running.
- Neil is the client voice. If three engineers all call about the same issue at once, call Neil before starting work so he can stop the others from filing.
- The first week of each quarter has a proposal deadline rush. Do not schedule patch reboots or server maintenance in that week. Ask Neil which days are quiet.
- Field tablets are Intune enrolled. If a tablet is replaced, reset enrollment in Intune first, then add to N-central.
- Proofpoint false positives increase with large CAD zip attachments. Release carefully and check the sender.

## Credential references
- `Vault: brackish-water-engineering/firewall-admin` (FortiGate pair)
- `Vault: brackish-water-engineering/firewall-admin-gtn`
- `Vault: brackish-water-engineering/switch-admin`
- `Vault: brackish-water-engineering/wifi-psk`
- `Vault: brackish-water-engineering/isp-portal`
- `Vault: brackish-water-engineering/domain-registrar`
- `Vault: brackish-water-engineering/m365-global-admin-breakglass`
- `Vault: brackish-water-engineering/backup-appliance`
- `Vault: brackish-water-engineering/lob-app-admin` (license server admin and Trimble)
- `Vault: brackish-water-engineering/printer-admin` (plotter and copier consoles)
- `Vault: brackish-water-engineering/proofpoint-admin`

## Change log
- 2026-10-12: Q4 restore test started, project folder P:\2026\ restored to lab, pending xref check. (Alex Rivera, T-25571)
- 2026-09-18: Annual documentation review. Added Georgetown VLAN table and plotter notes. (Alex Rivera)
- 2026-07-08: Q3 restore test passed. One VM and one project folder restored. (Alex Rivera, T-25118)
- 2026-04-22: Added drone workstation patch exclusion, N-central policy "BWE-No-Auto-Reboot". (Jordan Blake, T-24812)
- 2026-03-27: Replaced server room UPS batteries. (Sam Okafor, T-24745)
- 2026-02-03: Moved to Purview 7-year retention policy at principal request. (Alex Rivera, T-24560)
- 2025-11-14: Replaced HQ failover circuit with Bayline cable, added health check IPs. (Alex Rivera, T-24120)
- 2025-08-19: Replaced FortiGate 100F secondary in HA pair after RMA. (Sam Okafor, T-23684)

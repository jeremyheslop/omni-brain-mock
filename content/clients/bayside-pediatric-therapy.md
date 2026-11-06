# Bayside Pediatric Therapy

owner: Casey Morgan
last_reviewed: 2026-10-06
tags: healthcare, hipaa, omni-managed, emr, baa, pediatric, therapy, salisbury-md, shared-workstations
client_id: 1013
slug: bayside-pediatric-therapy
core_plan: Omni+ Managed
service_plans: Omni+ Managed, Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management
industry: Healthcare
employees: 24

## Overview

Outpatient pediatric therapy practice in Salisbury: occupational therapy, speech-language pathology, and physical therapy for kids. 24 employees: 15 clinicians (OT, SLP, PT, and assistants), 4 front desk and billing staff, 2 intake coordinators, a clinic director, and 2 administrative leads. They are a HIPAA covered entity. Everything we do for them is under the Business Associate Agreement on file with Accelo (document type "BAA", signed 2025-02-11).

The practice treats children by appointment, with sessions in treatment rooms and a small gym. Clinicians chart in the EMR between sessions on shared clinic workstations (one per two rooms) and on a few laptops on carts. There is no server of significance on site. The EMR is cloud hosted.

Why this file is long: they are the most compliance-sensitive client we have next to the credit union. Read the HIPAA notes in Gotchas before you touch anything.

Related docs: `sops/11-suspected-compromised-account.md`, `sops/34-ransomware-response.md`, `sops/09-backup-restore-test.md`, `sops/03-employee-offboarding.md`, `sops/10-phishing-email-response.md`.

Related company: Sandpiper Physical Therapy (client 1020) is a subsidiary and lists this company as its Parent Company in Accelo. Contracts, networks and contacts are separate.

## Service plans and contract notes

- Core plan: Omni+ Managed. Accelo contract C-1013-A, renews each March 1.
- Add-ons: Omni+ Advanced Security, Omni+ Server, Server Backup, Email Management.
- First response: P1 15 minutes (24x7), P2 1 hour (extended hours 7:00-7:00), P3 2 business hours, P4 next business day.
- Quarterly business review (QBR) with Casey and the clinic director: January, April, July, October. Next one is the October review, Casey leads.
- Quarterly restore tests (Alex Rivera). Results go into the Accelo client record under "Compliance".
- Priority onsite: Sam Okafor, usually same day for P1/P2.
- Proofpoint Essentials email gateway is included.
- HIPAA security risk assessment is done annually by an outside assessor (not us). We supply inventory and logs on request. Last assessment: September 2026.
- BAA is signed both ways: we are a business associate to Bayside, and Datto and Proofpoint are our subcontractors under their own BAAs. Do not add any new tool that touches PHI without asking Casey.
- Client has a cyber insurance policy. Carrier requires EDR, MFA, and tested backups. Keep those in good order.
- Billing is monthly per seat plus a flat QBR fee. Casey handles billing disputes.

## Contacts

| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Dr. Helen Whitfield (Clinic Director) | 410-555-0127 | helen.whitfield@baysidepeds.example |
| Billing | Carla Mendoza (Billing Manager) | 410-555-0128 | carla.mendoza@baysidepeds.example |
| After-hours | Aaron Kemp (Operations Lead) | 410-555-0129 | aaron.kemp@baysidepeds.example |
| Office manager / front desk lead | Joy Tillman | 410-555-0136 | joy.tillman@baysidepeds.example |
| Privacy Officer | Dr. Helen Whitfield | 410-555-0127 | see above |
| Security Officer | Aaron Kemp | 410-555-0129 | see above |
| EMR super user | Monica Esposito, OT | 410-555-0137 | monica.esposito@baysidepeds.example |

Notes:
- The Privacy Officer must be told about any suspected PHI exposure within one business day. Do not wait for us to finish investigating.
- Aaron is the one we call at night. He will usually call Dr. Whitfield himself.
- Joy is the day-to-day contact for onboarding and device problems.

## Sites and addresses

| Site | Address | Notes |
|---|---|---|
| Main clinic | 315 Camden Avenue, Suite 200, Salisbury, MD 21801 | Only location. Second floor, shared building. |

Hours and access:
- Clinic hours Mon-Fri 7:30-6:00, Saturday 8:00-12:00 (2 clinicians).
- Front desk opens the door at 7:15. Network closet is a locked cabinet in the supply room off the hall. Key is on the office manager's ring and a spare in a lockbox, code in Accelo access notes only.
- Waiting area has a kids' play area. Watch for children when running cable or carrying gear.
- Parking behind the building, enter by the side door. The elevator needs a key card at night.
- Tell the front desk when you arrive. No unescorted access to treatment rooms while sessions are in progress. Knock first.

## Internet and circuits

- Primary ISP: Delmarva Link Fiber, 1 Gbps symmetric. Account ref DLF-77-30912 (fictional). Support 410-555-0130.
- Static IP: 198.51.100.56/29 block (usable .57-.62). Firewall WAN1 is 198.51.100.58, .59 is reserved for a future VPN endpoint, the rest are not used.
- Backup ISP: Bayline Broadband 250/25 on the second WAN. Account BB-6603411. Dynamic IP.
- Both circuits are monitored from N-central. SD-WAN failover tested at each QBR.
- ONT is in the network cabinet. Do not move the cabinet door stop, the door hits the ONT.
- Cable modem sits above the firewall. Label on it says "BACKUP, ok to power cycle."
- ISP outage procedure: `sops/35-isp-outage-troubleshooting.md`. Because they chart live, an outage longer than 15 minutes should be treated as at least P2 and Dr. Whitfield gets a courtesy call.

## Network

Firewall:
- FortiGate 70F pair in HA (active-passive), hostnames `BPT-FW01` and `BPT-FW02`. FortiOS 7.4.x, upgraded 2026-05.
- UTM: web filtering (kid safe categories on guest), IPS, application control, SSL deep inspection on Corp VLAN with a client CA pushed by group policy.
- Logs forward to the Fortinet cloud logging and a syslog collector on N-central probe `BPT-PROBE01`. 12 months retention for HIPAA audit support.
- Admin access: by named account only, no shared admin logins (audit requirement).

Switching and Wi-Fi:
- Core: Aruba Instant On 1930 48G PoE (`BPT-SW01`) and a second 24-port (`BPT-SW02`) in the cabinet.
- APs: 6x Aruba Instant On AP25. One in each hallway section, one in the gym.
- SSIDs: `BPT-Staff` (WPA2 Enterprise via NPS? Needs to be re-verified, last checked 2026-03), `BPT-Guest` (guest VLAN, isolated, web filtered, rotating PSK), `BPT-Devices` (hidden, for the sound machines and iPads).

VLANs:

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 10 | Corp | 10.20.10.0/24 | Clinic workstations, laptops, printers |
| 20 | Clinical-Devices | 10.20.20.0/24 | Therapy iPads, tablets, assessment devices (no PHI storage) |
| 30 | Voice | 10.20.30.0/24 | Phones |
| 40 | Guest | 10.20.40.0/24 | Parents and visitors |
| 99 | Mgmt | 10.20.99.0/24 | Switches, APs, firewall |

DHCP and DNS:
- DHCP on the FortiGate. Corp scope 10.20.10.100-10.20.10.230.
- Static range 10.20.10.2-10.20.10.99 (printers .50-.59, scanner .60, backup appliance .30).
- DNS: DNSFilter agent on endpoints plus FortiGate DNS filter. Guest uses a different DNSFilter policy (adult content blocked, social media blocked).
- No on-premises Active Directory. Devices are Entra ID joined and Intune managed.

VPN:
- FortiClient IPsec VPN for the billing manager and the clinic director only. No other staff are allowed to remote in. Clinicians are told to chart at the clinic.
- MFA via FortiToken Mobile. Phone swaps: `sops/32-new-phone-mfa-device-swap.md`.

## Servers and line-of-business apps

- Servers: none. A small Synology-style NAS is NOT in use (retired in 2025). If you find one, do not turn it on, tell Casey.
- EMR: a cloud-hosted pediatric therapy EMR (WebPT-style product, referred to by staff as "the EMR"). Vendor handles hosting, patching, backups. SSO is not available. Each clinician has an individual login, enforced password policy by vendor. Super user is Monica.
- Billing: clearinghouse portal (browser) plus EMR billing module. Carla uses two monitors.
- e-Fax: cloud fax service (Sinch-style product) for referrals. Inbound faxes land in the Intake shared mailbox as PDFs.
- Telehealth: Zoom for Healthcare. A BAA is signed with Zoom. Only the clinic director can create meetings.
- Scheduling: part of the EMR.
- Therapy assessment software: two tools licensed per clinician (e.g. Sensory Profile and a speech-language assessment suite), installed on clinic workstations. Licenses are tied to a hardware ID, do not reimage without noting the license first.
- Other apps: Microsoft 365 apps, Adobe Acrobat Pro (Carla, Joy), 7-Zip, Chrome.

Shared clinic workstations:
- Eight shared workstations, named `BPT-WS-001` to `BPT-WS-008`. Windows 11 Pro, Intune managed.
- Shared device = kiosk-style policy. Users sign in with their own Entra account each time, no local profile kept after logoff (profile deletion on sign out via Intune).
- Auto-lock after 5 minutes idle. Screen privacy filters are installed on all of them.
- Cart laptops: three, `BPT-LT-CART1` to `CART3`. Same policy.
- Do NOT create local admin accounts on these. Break-glass local admin password is a single LAPS-managed account, see vault references.

## Microsoft 365 / Google tenant notes

- Tenant: baysidepeds.onmicrosoft.com. Primary domain baysidepeds.example.
- Licenses: 24 Microsoft 365 Business Premium. Shared mailboxes (free): `intake@`, `billing@`, `info@`, `referrals@`.
- Conditional Access: MFA required for all; compliant device required; legacy auth blocked; sign-in from outside the US blocked.
- Defender for Business on. SentinelOne is also installed via N-central. Do not turn on Defender real time scanning exclusions without Alex.
- Proofpoint Essentials sits in front of Exchange Online. MX records point to Proofpoint, inbound mail is locked to Proofpoint IPs. Quarantine digest goes to the user daily.
- Email encryption: Proofpoint encryption triggered by the subject tag `[secure]` or by DLP rules (SSN, MRN patterns). Staff are trained to use it for anything with PHI.
- Retention: 7 year retention label on mail from the intake and billing mailboxes (HIPAA records period). Set by Alex 2025-03. Do not delete shared mailbox content.
- Purview audit log is enabled. Retention 1 year.
- Datto SaaS Protection covers mailboxes, OneDrive, SharePoint, Teams.
- Global admins: Alex Rivera and Casey Morgan. Breakglass account exists and is tested at each QBR.
- Domain registrar and DNS: managed by us, see vault.
- Offboarding must follow `sops/03-employee-offboarding.md` AND notify Aaron the same day for HIPAA access removal. Disable EMR login at the vendor too (the clinic director does that).

## Backup

- Local appliance: Datto SIRIS (`BPT-DATTO01`) backs up the on-prem cabinet items that remain (probe and the Intune print server VM). Mostly a legacy decision. With the EMR in the cloud there is not much to back up locally.
- Offsite: Datto cloud, 3 year retention for the appliance.
- Datto SaaS Protection for M365: daily, plus on demand before offboarding deletes.
- Workstations: no image backup. Data is in the EMR or OneDrive. Clinicians are told not to save PHI locally. A DLP policy in Defender flags saves to Desktop/Downloads containing PHI patterns.
- Daily backup check per `sops/08-daily-backup-check.md`. Alex or Jordan checks by 9:00 each business day.
- Quarterly restore test per `sops/09-backup-restore-test.md`. Test an M365 mailbox restore (a sample test mailbox, never a real user) and the appliance VM. Log in Accelo on the client record.
- Backup alert in N-central is Critical if a mailbox backup is more than 36 hours old, because the cyber insurance form asks about it.

## Printers, scanners, and other devices

| Device | Location | IP | Notes |
|---|---|---|---|
| Kyocera TASKalfa 3253ci | Front office | 10.20.10.50 | Scan to email via authenticated SMTP, scan folder disabled for HIPAA. Admin in vault. |
| HP LaserJet Pro M404 | Billing | 10.20.10.51 | Billing manager only. Locked paper tray (checks). |
| HP LaserJet Pro M404 | Clinical hall | 10.20.10.52 | Secure print release enabled. |
| Fujitsu fi-7160 | Intake | USB to BPT-WS-004 | Used for scanning referrals. |
| Brother label printer | Front desk | USB | Name labels. |
| Yealink desk phones | Front desk, offices | Voice VLAN | Cloud phone service managed by the phone vendor. |
| iPads (12) | Treatment rooms | Clinical-Devices VLAN | Intune supervised, therapy apps, no PHI stored. |
| White noise machines | Treatment rooms | Wi-Fi hidden SSID | Vendor managed. Do not remove from the network. |

- Cameras: none inside treatment rooms (by policy). Two entrance cameras on VLAN 20, owned by the landlord.
- Paper shredding: Chesapeake Shred Co (monthly pickup), not our scope but we are asked about it.

## Vendor contacts

| Vendor | Contact | Phone | Notes |
|---|---|---|---|
| Delmarva Link Fiber | Priya Raman | 410-555-0131 | Fiber circuit. 24x7 support line 410-555-0130. |
| Bayline Broadband | Support desk | 410-555-0132 | Cable backup. |
| EMR vendor | Account manager, Theo Brandt | 410-555-0133 | Vendor handles app outages. Open a ticket in their portal and call Monica. |
| Proofpoint reseller | Through Casey | n/a | Support tickets only by Casey or Alex. |
| Datto | Partner support | n/a | Through Casey. |
| Phone vendor (Shore Voice) | Hannah Liu | 410-555-0134 | Cloud phones, fax-to-email. |
| Outside HIPAA assessor | Northcoast Compliance (Glenn Faber) | 410-555-0135 | Annual assessment. Do not share logs without Casey's OK. |

## Gotchas / tribal knowledge

1. HIPAA: if you see PHI on a screen while working remotely or onsite, do not copy, screenshot, or attach it to a ticket. Describe it instead. Ticket text is not PHI-safe.
2. Never take screenshots of the EMR for ticket notes. Use "EMR login error 401" style text.
3. Never ask a clinician to read patient names aloud while we troubleshoot. Use a test patient. The EMR has a test chart called "Zzz Test Patient."
4. The shared workstations delete profiles on sign out. If a clinician says "my desktop shortcuts are gone," that is by design. Pin things to OneDrive or the Start menu via Intune policy.
5. Therapy assessment software licenses are tied to hardware ID. When replacing BPT-WS-003 and 005, deactivate the license on the old machine first (Monica has the vendor portal login). Missing this cost us a week in 2025.
6. Saturday clinic has 2 clinicians and no front desk. A Saturday outage is a real problem even though it is outside the normal Omni+ Managed extended hours. Aaron will call the emergency line.
7. The side door elevator key card stops working at 6:15 pm. Tell the front desk if you plan to work late so security can unlock.
8. Do not run any Windows updates on shared workstations between 7:30 and 6:00. N-central patch window is Tuesday and Thursday 6:30-7:30 pm, with a forced reboot at 7:15 pm.
9. The EMR does not work well in Edge with SSL deep inspection. The firewall has an exemption for the EMR vendor domains. Do not remove it.
10. The Intake shared mailbox receives faxes with no sender name. Staff think it is spam. It is not. See Joy.
11. Kids drool on things. Keyboards on the shared workstations are the spray-proof type. Order the same kind, part number in Accelo asset notes.
12. If a parent complains about guest Wi-Fi, there is no support for personal devices. Politely refer to Joy.
13. The cable modem backup circuit was set up with a different DNS suffix. If WAN2 failover happens and printers are unreachable, flush DNS on the workstations.

## Credential references (vault paths only)

- Vault: bayside-pediatric-therapy/firewall-admin
- Vault: bayside-pediatric-therapy/switch-admin
- Vault: bayside-pediatric-therapy/wifi-psk
- Vault: bayside-pediatric-therapy/wifi-psk-guest
- Vault: bayside-pediatric-therapy/domain-registrar
- Vault: bayside-pediatric-therapy/isp-portal
- Vault: bayside-pediatric-therapy/isp-portal-backup
- Vault: bayside-pediatric-therapy/m365-global-admin-breakglass
- Vault: bayside-pediatric-therapy/backup-appliance
- Vault: bayside-pediatric-therapy/lob-app-admin (EMR admin delegate, super user manages vendor portal)
- Vault: bayside-pediatric-therapy/printer-admin
- Vault: bayside-pediatric-therapy/laps-local-admin-note (pointer to Intune LAPS, no password stored here)
- Vault: bayside-pediatric-therapy/proofpoint-admin

## Change log

- 2026-10-06: Updated for September HIPAA assessment findings. Added guest filtering notes and Saturday clinic. Casey Morgan. T-26702.
- 2026-07-22: Q2 restore test completed (mailbox + appliance VM), passed. Alex Rivera. T-26233.
- 2026-05-14: FortiGate HA pair upgraded to FortiOS 7.4.x, failover tested. Alex Rivera. T-25911.
- 2026-03-05: Contract renewal, Omni+ Managed kept, added QBR fee. Casey Morgan. C-1013-A.
- 2025-11-04: Replaced BPT-WS-003 and BPT-WS-005 with new hardware. Sam Okafor. T-24802.
- 2025-08-19: Enabled 7 year retention labels on intake and billing mailboxes. Alex Rivera. T-24402.
- 2025-02-11: BAA signed. Initial onboarding of Omni+ Managed services complete. Casey Morgan. P-0388.

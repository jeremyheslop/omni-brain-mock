# Peninsula Freight Brokers

owner: Alex Rivera
last_reviewed: 2026-07-22
tags: logistics, freight-broker, tms, edi, dispatch, voip, 24x7, omni-proactive
client_id: 1019
slug: peninsula-freight-brokers
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Server, Server Backup, Hosted Cloud Server
industry: Professional Service
employees: 21

## Overview
Truck freight brokerage in Laurel, DE. They don't own trucks. They match shippers' loads to carriers, so everything runs on the phone, the TMS, and email. 21 employees, split into a day sales/ops team and a small overnight dispatch crew. Phones and the TMS are the business. If either is down, loads stop moving and money is lost by the hour.

Dispatch is staffed 24 hours a day, 7 days a week. That is why they are on Omni+ Proactive and not Omni+ Basic, and why their P1 clock never really stops.

## Service plans and contract notes
- Core plan: Omni+ Proactive. Accelo contract "Peninsula Omni+ Proactive Services".
- Add-ons: Omni+ Server, Server Backup, Hosted Cloud Server.
- First response: P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Onsite visit included quarterly (Sam, usually the first Tuesday of the quarter). Extra visits billed hourly.
- Casey agreed in the last renewal that phone outages count as P1 even if only the inbound main line is affected. Put it in the ticket.
- Contract renews July 1.
- After-hours emergency line 410-555-0100 goes to the on-call tech. Their night dispatcher knows to call it directly, not email.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Lena Hartsock (Operations Manager) | 302-555-0149 | lena.hartsock@peninsulafreight.example |
| Billing | Odell Winter (Controller) | 302-555-0142 | odell.winter@peninsulafreight.example |
| After-hours | Night dispatch desk | 302-555-0143 | dispatch@peninsulafreight.example |
| After-hours escalation | Lena Hartsock (cell) | 302-555-0157 | lena.hartsock@peninsulafreight.example |
| Owner | Gil Pomeroy | 302-555-0158 | gil.pomeroy@peninsulafreight.example |
| EDI / systems analyst | Shawna Brisco | 302-555-0146 | shawna.brisco@peninsulafreight.example |
| Office manager | Dee Lankford | 302-555-0147 | dee.lankford@peninsulafreight.example |

Call Shawna for anything TMS or EDI. Lena for anything that stops dispatch. Gil only through Casey.

## Sites and addresses
- Single site: 305 Sussex Logistics Drive, Suite 2, Laurel, DE 19956. Office hours Mon-Fri 7:00-6:00. Dispatch desk is staffed 24x7, 3 people overnight.
- Building has a keypad on the front door. Night dispatch lets us in. Call the dispatch desk first.
- Network closet is in the supply room, key on the hook inside Dee's office.

## Internet and circuits
| Item | Primary | Backup |
|---|---|---|
| ISP | Delmarva Link Fiber | Bayline Broadband |
| Type | 200/200 business fiber | 100/10 business cable |
| Static IP | 203.0.113.96/29 (firewall on .98) | dynamic, failover only |
| Account ref | DLF-PFB-0317 | BB-64902 |

- Failover is automatic. The VoIP provider has SIP registrations on both paths, but calls take about 30 seconds to re-register after failover. Dispatchers will notice.
- Cable modem lives in the supply room on the shelf above the switch. It gets unplugged when someone vacuums. Yes, really.

## Network
- Firewall: FortiGate 60F `PFB-FW01`, with FortiGuard web filter and IPS on.
- Switches: Ubiquiti UniFi 24-port PoE (`PFB-SW01`) and 8-port PoE (`PFB-SW02` at the dispatch desk). UniFi U6 APs x3.
- VoIP QoS is set on the firewall and switch port profiles. Don't reset it.
- VPN: FortiClient SSL VPN for 6 users. Dispatchers do not use VPN, the TMS is web based. See `sops/19-vpn-user-setup.md`.

| VLAN | Name | Subnet | Purpose |
|---|---|---|---|
| 1 | Default/Office | 10.60.1.0/24 | Workstations, printers |
| 20 | Voice | 10.60.20.0/24 | Desk phones, DHCP option 66 for provisioning |
| 30 | Guest | 10.60.30.0/24 | Visiting drivers and customers, internet only |
| 99 | Mgmt | 10.60.99.0/28 | Network gear |

- DHCP and DNS: DHCP from the FortiGate, DNS via the firewall to DNSFilter. No domain controller. Workstations are Entra joined.
- Guest Wi-Fi password is on a card at the front desk. Rotated by Jordan every 90 days. See `sops/20-wifi-guest-network.md`.

## Servers and line-of-business apps
- No on-prem servers. A small NAS used to exist for scanned rate confirmations. It was retired in March 2026 and the shares were moved to SharePoint.
- TMS: hosted web-based TMS from a vendor called FreightPilot (fictional). Vendor-run, we do not manage the application. Users log in with the vendor's SSO tied to their M365 account. Issues go to the vendor first. Shawna is the admin.
- EDI: shippers send load tenders (204) and receive status (214, 990) through Chesapeake EDI Exchange (fictional VAN). Shawna owns the mappings. When EDI stops, we only check that our side has internet and email and call Shawna.
- Load boards: two web-based load boards, logged in per user in the browser. Logins are individual.
- Accounting: QuickBooks Desktop Enterprise on `PFB-WS-020` (Odell's PC), single-user mode, data file on OneDrive. See gotchas.
- 21 workstations `PFB-WS-001` to `PFB-WS-021`, 3 dispatch desks have dual monitors (some have triple).

## Microsoft 365 / Google tenant notes
- Tenant `peninsulafreight.example`, 21 Business Premium licenses, plus 1 shared mailbox `dispatch@` and 1 shared mailbox `loads@` (EDI notifications and rate confirmations).
- Conditional Access: MFA required, except the three dispatch desk accounts are on a named-location exception for the office IP. Reason: shared overnight logins on a shared desk. Not ideal, Casey knows.
- Datto SaaS Protection on all mailboxes, OneDrive, and SharePoint. See `sops/15-shared-mailbox-setup.md` for shared mailbox standards.
- Defender for Business is on. DNSFilter on the firewall and endpoint agents.

## Backup
- Datto SIRIS appliance is installed, but with no servers it backs up only the QuickBooks PC image and the two admin PCs. Casey and Alex have discussed dropping it to Cove at renewal. Not decided.
- SaaS Protection covers the real data. Daily check per `sops/08-daily-backup-check.md`.
- Restore test: last done 2026-05-14 (one mailbox item, one SharePoint folder). Passed.

## Printers, scanners, and other devices
- Konica-style color MFP in the main office, scan to email via relay. Static IP 10.60.1.15.
- Label printer on Dee's desk (USB).
- Desk phones: 24 handsets (21 users plus 3 spare/common), hosted VoIP from Tidewater Voice (fictional). Phones provision from vendor via DHCP option 66.
- 3 headsets at dispatch are Bluetooth-dongle type, the dongles are tiny and get lost.

## Vendor contacts
| Vendor | What | Contact | Phone |
|---|---|---|---|
| Tidewater Voice | Hosted VoIP | Support, ask for Elijah | 302-555-0151 |
| FreightPilot | TMS | Support desk | 302-555-0152 |
| Chesapeake EDI Exchange | EDI VAN | Support, ticket portal | 302-555-0153 |
| Delmarva Link Fiber | Primary circuit | NOC | 410-555-0171 |
| Bayline Broadband | Backup circuit | Business support | 410-555-0172 |

Escalation flow in `sops/30-vendor-escalation.md`. For a TMS outage: confirm the vendor status page first, then call their desk, and tell Lena.

## Gotchas / tribal knowledge
1. Phones go down more than the internet does. Check VLAN 20 and the QoS profile first, then the provider portal. Most "phones are down" tickets turn out to be the provider side.
2. Overnight dispatch uses the 3 shared accounts. Do not force a password change on those between 9:00 PM and 7:00 AM. They get locked out of the TMS and loads go uncovered.
3. Patching: the office reboots happen Sunday at 2:00 AM, but dispatch PCs are excluded and are patched in a rolling schedule, one at a time, by hand. N-central policy "PFB Dispatch No Auto Reboot". See `sops/25-server-reboot-window.md` for the general rule.
4. QuickBooks Desktop is single-user. If someone else opens the company file it throws "multi-user" errors. Odell's PC only.
5. Month-end invoices go out on the 1st through the 3rd. Avoid maintenance then.
6. The TMS gets slow when someone has more than ~15 tabs open on the load board. Not a network problem, don't chase it.
7. Dispatchers will say "internet is down" when the TMS vendor is down. Check another site first (e.g. a news site).
8. Hurricane season: Gil wants a call if a storm is forecast. Last year the fiber was cut by a contractor and the Bayline cable carried them.
9. The vacuum thing: if the backup circuit is dead at 6:00 AM, ask whether the cleaning crew was in.

## Credential references
- Vault: peninsula-freight-brokers/firewall-admin
- Vault: peninsula-freight-brokers/switch-admin (UniFi controller)
- Vault: peninsula-freight-brokers/wifi-psk
- Vault: peninsula-freight-brokers/m365-global-admin-breakglass
- Vault: peninsula-freight-brokers/domain-registrar
- Vault: peninsula-freight-brokers/isp-portal
- Vault: peninsula-freight-brokers/backup-appliance
- Vault: peninsula-freight-brokers/lob-app-admin (FreightPilot admin, shared with Shawna)
- Vault: peninsula-freight-brokers/printer-admin

## Change log
- 2026-07-22 (Alex Rivera): Contract renewal review, noted Datto vs Cove question. T-24790.
- 2026-05-14 (Jordan Blake): Quarterly restore test, passed. T-24551.
- 2026-03-18 (Sam Okafor): Retired NAS, moved scans to SharePoint. T-24299.
- 2026-01-27 (Alex Rivera): Added dispatch exclusion policy to N-central patching. T-24150.
- 2025-10-07 (Sam Okafor): Quarterly onsite, replaced two dispatch headsets and a failing PoE injector.
- 2025-08-12 (Casey Morgan): Added phone outage = P1 clause to contract notes.

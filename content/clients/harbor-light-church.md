# Harbor Light Church

owner: Sam Okafor
last_reviewed: 2025-03-14
tags: nonprofit, church, google-workspace, planning-center, volunteers, sound-booth, omni-basic, stale
client_id: 1018
slug: harbor-light-church
core_plan: Omni+ Basic
service_plans: Omni+ Basic, Hosted Website Plan
industry: Church
employees: 6

## Overview
Small church in Cambridge. 6 paid staff (pastor, admin, worship leader, youth director, part-time facilities, part-time bookkeeper) plus a rotating group of volunteers who use church computers on Sundays and for events. Tight budget, discounted rate approved by Casey. Not much to manage, but the volunteer angle makes things messy: lots of people touching a few shared machines.

This file has not been reviewed in a long time. Treat anything marked "needs verification" as unknown.

## Service plans and contract notes
- Core plan: Omni+ Basic (nonprofit rate). Accelo contract "Harbor Light Omni+ Basic".
- Add-ons: Hosted Website Plan.
- First response: P1 1 business hour, P2 4 business hours, P3 next business day, P4 2 business days.
- Sunday service support is NOT covered. Pastor Ellis knows. If the livestream breaks on a Sunday morning, they call Sam's cell as a favor, not as a contract item. Do not promise it.
- Contract renewal date: needs verification.

## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Karen Ostrowski (Church Administrator) | 410-555-0159 | karen@harborlight.example |
| Billing | Walter Pemberton (Treasurer, volunteer) | 410-555-0180 | treasurer@harborlight.example |
| After-hours | Karen Ostrowski | 410-555-0159 | karen@harborlight.example |
| Pastor | Rev. Dale Ellis | 410-555-0189 | pastor@harborlight.example |
| Sound booth lead (volunteer) | Marcus Tilghman | not documented yet | not documented yet |

## Sites and addresses
- 140 Dorchester Church Road, Cambridge, MD 21613. Office hours Tue-Fri 9:00-3:00. Services Sunday 9:00 and 11:00. Wednesday evening Bible study.
- Office entrance is the side door by the fellowship hall. Karen has the key, Sam has a copy.
- Server/network closet is behind the nursery. Not a server, just the network gear.

## Internet and circuits
- ISP: Bayline Broadband, business cable, about 100/10. Account ref needs verification.
- Static IP: none known. Needs verification.
- Modem sits in the nursery closet next to the switch.

## Network
- Firewall/router: old SonicWall TZ-class unit, firmware likely out of date. Needs verification. Planned replacement with a UniFi gateway was discussed, never scheduled.
- One unmanaged 24-port switch, a few cheap APs added over the years (3 maybe 4). Not all in N-central.
- Flat network, DHCP from the SonicWall. Subnet needs verification (believed 192.168.1.0/24).
- Guest Wi-Fi for the congregation is on the same network. Needs verification. If this is still true, it is a problem.
- VPN: none.

## Servers and line-of-business apps
- No servers.
- Planning Center (Services, People, Giving) in the browser. Admin is Karen. Planning Center logins are the church's, not ours.
- Livestream: a PC in the sound booth running OBS-style streaming software to the church's video page. See gotchas.
- Church management / donor records live in Planning Center. Treasurer uses QuickBooks Online (his own subscription, on his home computer).
- Workstations: `HLC-WS-01` (Karen), `HLC-WS-02` (pastor), `HLC-WS-03` (shared office PC), `HLC-SOUND-01` (sound booth). Worship leader and youth director use their own laptops. Not managed. Needs verification.

## Microsoft 365 / Google tenant notes
- Google Workspace for Nonprofits (not Microsoft 365). Domain `harborlight.example`. About 10 free licenses, 6 staff plus 4 shared or ministry accounts.
- Super admin is Karen. A backup admin was supposed to be set up. Not verified.
- 2-step verification: staff on, ministry accounts not sure.
- No Google backup. Not offered under Omni+ Basic.

## Backup
- Cove Data Protection on `HLC-WS-01` and `HLC-WS-02` only. Sound booth PC is not backed up, nor is the shared PC. Needs verification.
- Restore test: never done.

## Printers, scanners, and other devices
- Brother laser MFP in the office, on Wi-Fi. Bulletin printing happens Thursday.
- Sound board: digital mixer, USB to the booth PC. Not ours to support.

## Vendor contacts
- Bayline Broadband: 410-555-0172
- Planning Center support: via their website, church admin handles it.

## Gotchas / tribal knowledge
1. The sound booth PC auto-logs in and has no password. Volunteers need it that way. Don't change it without asking Marcus. Yes, we know.
2. Do not run Windows updates on `HLC-SOUND-01` on a Friday or Saturday. The audio interface driver broke once and Sunday was a mess.
3. Wednesday evening and Sunday morning are bad times for any remote work.
4. Volunteers sometimes save things to the desktop of `HLC-WS-03`. Nothing there is backed up.

## Credential references
- Vault: harbor-light-church/firewall-admin (needs verification, may be a default)
- Vault: harbor-light-church/wifi-psk
- Vault: harbor-light-church/google-super-admin (held with Karen)
- Vault: harbor-light-church/domain-registrar

## Change log
- 2025-03-14 (Sam Okafor): Quick review, flagged SonicWall age and guest Wi-Fi. T-22570.
- 2024-11-05 (Jordan Blake): Reset Karen's Google 2-step after phone replaced. T-21944.
- 2024-08-27 (Sam Okafor): Added third AP in fellowship hall.

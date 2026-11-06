# Driftwood Architecture Studio
owner: Alex Rivera
last_reviewed: 2026-06-14
tags: architecture, revit, bluebeam, render-workstation, omni-proactive, fortinet, lewes-de
client_id: 1021
slug: driftwood-architecture-studio
core_plan: Omni+ Proactive
service_plans: Omni+ Proactive, Omni+ Backup, Hosted Website Plan
industry: Professional Service
employees: 9
## Overview
Small residential and light commercial architecture studio in Lewes, DE. 9 staff: 3 principals/senior architects, 4 designers, 1 drafter, 1 office manager. Mostly coastal homes, small retail fit-outs and a few Sussex County municipal jobs. Everyone works in Revit, uses Bluebeam Revu for markups, and shares one very expensive render workstation. Two people (Colin and Maya) work from home two days a week. N-central device prefix: `DAS-` (e.g. `DAS-SRV01`, `DAS-RENDER01`, `DAS-WS-004`).
## Service plans and contract notes
- Omni+ Proactive, renewed 2026-02-01 for 12 months.
- Add-ons: Omni+ Backup, Hosted Website Plan.
- P1 30 minutes (24x7 on-call), P2 2 business hours, P3 4 business hours, P4 next business day.
- Onsite visit included monthly (Sam, usually the first Thursday). Extra visits billed.
- Includes SentinelOne, DNSFilter, Datto SIRIS, Datto SaaS Protection for M365.
- Project work is quoted separately as a P-0xxx project in Accelo. None open right now.
- Not covered: buying Revit, Bluebeam, Enscape or Adobe licenses. Lena (office manager) buys those, we help install.
- "Plot days" (day before a permit submittal): treat any P3 on a designer machine as P2.
## Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| Primary | Colin Ashbury (Principal) | 302-555-0102 | colin@driftwoodarch.example |
| Billing | Lena Whitcomb (Office Manager) | 302-555-0103 | lena@driftwoodarch.example |
| After-hours | Colin Ashbury (cell) | 302-555-0104 | colin@driftwoodarch.example |
| BIM lead | Maya Okonkwo-Reyes | 302-555-0105 | maya@driftwoodarch.example |
| Drafter / unofficial IT | Theo Brandt | 302-555-0106 | theo@driftwoodarch.example |
Colin approves anything over a few hundred dollars. Theo is who you want onsite, he knows where everything is.
## Sites and addresses
- Studio: 41 Savannah Row, Suite B, Lewes, DE 19958. Mon-Fri 8:30-5:30, often later before deadlines. Ground floor of a converted warehouse. Network closet is a coat cabinet behind the plotter. Door code is held by Lena (not documented here). Street parking only, bring a hand truck.
- Home users (Colin, Maya) have VPN on their laptops. We do not support home Wi-Fi.
## Internet and circuits
- ISP: Delmarva Link Fiber, 500 Mbps symmetric business fiber. Account DLF-ACC-0061730 (fake ref). Single static IP 203.0.113.42. ISP-owned ONT in the closet, do not move.
- No backup circuit. Colin has declined one twice. Portal: `Vault: driftwood-architecture-studio/isp-portal`.
- Outage: tethering works for email only. Revit cloud model sync is useless on a hotspot, so tell users to draw offline. See `sops/35-isp-outage-troubleshooting.md`.
- Upload speed matters. Slow sync usually means someone is uploading a render output.
## Network
- Firewall: FortiGate 40F (`DAS-FW01`). UTM web filter off for the studio VLAN (too many false positives on product sites), on for guest. SSL VPN for the two remote users, split tunnel (`sops/19-vpn-user-setup.md`).
- Switch: UniFi Switch 24 PoE (`DAS-SW01`). Wi-Fi: 2x UniFi U6 Lite. SSIDs `Driftwood` (staff) and `Driftwood-Guest` (isolated).
| VLAN | Name | Subnet | Notes |
|---|---|---|---|
| 1 | Default/Staff | 192.168.30.0/24 | Workstations, server, plotter |
| 20 | Guest | 192.168.32.0/24 | Internet only |
| 30 | IoT/AV | 192.168.33.0/24 | Conference room TV, thermostat |
- DHCP from the FortiGate. Reservations: server .10, render workstation .20, plotter .30. DNS on `DAS-SRV01` (192.168.30.10), forwarders to DNSFilter. Local domain `driftwood.local`.
## Servers and line-of-business apps
- `DAS-SRV01`: file server and DC (Windows Server 2022, Dell T150). Project shares and weekly Revit archive copies.
- `DAS-RENDER01`: render workstation (Threadripper, 128 GB RAM, RTX 4090), runs Enscape and V-Ray. Not domain joined, see gotchas.
- `DAS-WS-001` to `DAS-WS-009`: Dell Precision towers and two mobile workstations.
- Autodesk Revit 2025 (named user, Lena manages the Autodesk account). AutoCAD LT on 2 legacy seats. Bluebeam Revu 21 (5 seats, Studio sessions for plan review). Enscape floating license (3 seats, Autodesk-hosted, no local license server). Adobe CC, 3 seats.
- Models live in Revit Cloud Worksharing (Autodesk Docs). Weekly archive copies on `DAS-SRV01\Projects` are the fallback for a corrupted model.
- QuickBooks Online (cloud), Lena only. Plotter: HP DesignJet T850.
## Microsoft 365 / Google tenant notes
- Microsoft 365 Business Premium, 9 licenses plus shared mailbox `info@driftwoodarch.example`. Domain `driftwoodarch.example`. MFA via Authenticator, conditional access baseline on.
- Break glass: `Vault: driftwood-architecture-studio/m365-global-admin-breakglass`.
- OneDrive is for personal docs only. Known Folder Move is OFF because it broke Revit library paths. Do not turn it back on.
- New users: `sops/02-new-user-onboarding.md` plus an Autodesk seat from Lena.
## Backup
- Datto SIRIS (`DAS-BDR01`) backs up `DAS-SRV01`, cloud replication on, 1 year retention. Datto SaaS Protection for M365.
- Workstations are not imaged. Render outputs copy to the server nightly by robocopy (see gotchas).
- Daily check per `sops/08-daily-backup-check.md`. Restore test twice a year, last 2026-05-20, passed.
## Printers, scanners, and other devices
- HP DesignJet T850 plotter at 192.168.30.30. Konica Minolta bizhub C250i, scans to `\\DAS-SRV01\Scans` (folder only, no email).
- Conference room: Samsung TV and Apple TV on the IoT VLAN. No large format scanner, they use a print shop.
## Vendor contacts
- Delmarva Link Fiber business support: 302-555-0141.
- Bayfront CAD Supply (Autodesk reseller), Greg Palermo: 302-555-0107.
- Atlantic Office Systems (Konica Minolta dealer): 302-555-0108.
- Bluebeam and Autodesk licensing: Lena through the vendor portals. HP plotter service: Alex opens the case.
## Gotchas / tribal knowledge
1. `DAS-RENDER01` is not domain joined on purpose. GPU driver and Enscape activation both broke after domain join in 2024. It uses a local admin account and is managed through N-central only. Call Maya before touching it, a reboot mid-render loses hours.
2. No patching on designer machines on plot days. N-central has an exclusion for the render box and a Sunday window.
3. "Central model is locked" on a slow ISP afternoon usually means one user lost Autodesk Docs sync, not a bad file. Close Revit, clear the local cache folder, reopen.
4. Bluebeam Studio sessions drop if the FortiGate session timeout is under 1 hour. SSL inspection is off for Bluebeam domains. Leave it.
5. The plotter prints blank pages on some old county PDFs. Print from Bluebeam, not Acrobat.
6. The robocopy task on `DAS-RENDER01` runs at 11:30 PM and silently fails if the server is rebooting. Check `C:\Scripts\render-sync.log` when output goes missing.
7. Theo's `DAS-WS-004` has a drawing tablet driver that crashes after Windows updates. Roll back the driver, not the update.
8. The closet gets hot in summer (shares a wall with the kitchen). Prop the door, use the fan, tell Lena if the server beeps.
9. If external monitors go black on Maya's dock, unplug the dock power for 30 seconds. The March 2026 Dell BIOS update fixed most cases.
## Credential references
- Firewall: `Vault: driftwood-architecture-studio/firewall-admin`
- Switch/AP controller: `Vault: driftwood-architecture-studio/switch-admin`
- Wi-Fi PSK: `Vault: driftwood-architecture-studio/wifi-psk`
- Domain registrar: `Vault: driftwood-architecture-studio/domain-registrar`
- Datto BDR: `Vault: driftwood-architecture-studio/backup-appliance`
- Render workstation local admin: `Vault: driftwood-architecture-studio/render-local-admin`
- Plotter admin: `Vault: driftwood-architecture-studio/printer-admin`
## Change log
- 2026-06-14 (Alex Rivera): Annual review. Added render workstation details and plot day rule.
- 2026-05-20 (Jordan Blake): Restore test passed (server share and one mailbox). T-24712.
- 2026-03-11 (Sam Okafor): Dell dock BIOS update on Maya's mobile workstation. T-24544.
- 2026-02-01 (Casey Morgan): Contract renewed, no plan change.
- 2025-11-18 (Alex Rivera): Turned Known Folder Move off again after Revit library path problems.
- 2025-08-06 (Sam Okafor): Replaced Ricoh with Konica Minolta bizhub C250i, scan to folder only.
- 2025-03-04 (Alex Rivera): Added `DAS-RENDER01` to N-central with custom patch window.

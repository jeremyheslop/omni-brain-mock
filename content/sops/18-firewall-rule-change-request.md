# Firewall Rule Change Request

owner: Alex Rivera
last_reviewed: 2026-07-09
applies_to: Omni+ Basic and up (T&M as billable project)
tags: firewall, fortigate, unifi, sonicwall, change-control, network, security

## Purpose
Make firewall changes in a controlled way: written request, approval, backup of the config, a change that can be rolled back, and a record afterward.

## When to use
A client or vendor asks to open a port, allow an IP, add a port forward, block a site, change a VPN rule, or allow a new app through. Also for any rule change we decide to make ourselves. Credit unions and other regulated clients have their own change process (see the client file), which sits on top of this one.

## Before you start
- Written request in an Accelo ticket from an authorized contact: what, why, source, destination, port, protocol, how long. Category Network, priority P4 (P2 if a business app is down because of a missing rule).
- Firewall admin login: `Vault: <client-slug>/firewall-admin`. Only Alex and Sam change firewalls. Jordan can prepare the ticket.
- Know the platform: FortiGate, UniFi gateway, or SonicWall (a few older sites).
- Pick a change window. Business hours for low-risk rules, after hours for anything that can cut off access.

## Steps
1. Read the request. Ask the questions that are missing: which device, which port, from where, to where, how long, who is the vendor contact, who asked for it. "Open everything to the vendor" is not a request.
   Check: the ticket names a source, destination, port, protocol, and an end date if it is temporary.
2. Rate the risk.
   - Low: allow a specific public IP to a specific port on a specific internal host, or a block rule.
   - Medium: new inbound port forward, new VPN rule, or change to a segmented network.
   - High: any rule from "any" source to an internal host, RDP exposed to the internet, or rule changes on a segmented network at a regulated client.
   Check: risk level is written in the ticket.
3. Get approval. Low: Alex. Medium: Alex plus the client contact in writing. High: Alex, Casey, and the client owner. RDP exposed to the internet is a no, always. Offer VPN.
   Check: approval is in the ticket with names and dates.
4. Back up the config before you change anything.
   - FortiGate: System > Config > Backup (or `execute backup config ...`).
   - UniFi: Settings > System > Backups > Download.
   - SonicWall: System > Settings > Firmware and Settings > Export Settings.
   Save to the client folder and note the file name in the ticket.
   Check: backup file is present and not zero bytes.
5. Make the change. Name the rule clearly: `ALLOW-vendorname-ticketnumber-port` (e.g. `ALLOW-ScannerVendor-T-24817-443`). Set the source to the exact IP or range. Use the narrowest scope that works. Add a comment with the ticket number and expiry date.
   Check: the rule shows up in the policy list above the deny-all and not below.
6. Test from the outside if it is an inbound rule. Use a phone off Wi-Fi or an external check from our lab. Test from the inside for outbound or inter-VLAN rules.
   Check: the connection works for the requested use and nothing else you did not intend opened.
7. Review the logs for 15 minutes. Look for hits on the new rule and any other surprising traffic.
8. Tell the requester it is done, how to test, and when it will be reviewed.
9. If it is temporary, create an Accelo task with the removal date and assign it to Alex.
   Check: the task exists with a due date.
10. Update the network section in the client file and the vault entry list if a new credential or key was created.

## Gotchas
- A port forward on a FortiGate needs a VIP object and a policy. Making the VIP without the policy does nothing, and making the policy with "all" as the destination opens too much.
- UniFi gateway rules are order-based and the "Allow Return Traffic" setting changes what gets blocked. Read the rule list top to bottom after your change.
- Vendors love asking for "any any" to troubleshoot. Say no. Ask for their source IPs.
- Do not forget IPv6. A rule that blocks IPv4 only may leave the IPv6 path open.
- Dynamic IPs on the vendor side mean you will be back in a week. Ask for an FQDN or a fixed range.
- Rules that "temporarily" stay forever are how breaches happen. The cleanup task is not optional.
- SonicWall NAT policies need the matching access rule and sometimes a loopback policy for internal access to the public IP.

## Escalate when
- The request would expose RDP, SMB, or a database to the internet: stop and call Alex.
- The requester is not on the authorized contacts list: Casey confirms with the primary contact first.
- A change causes an outage: roll back at once using the backup, then tell Alex and Casey. If after hours, `26-after-hours-emergency-call.md`.
- Vendor asks for permanent remote access to a client network: Casey and Alex.

## Documentation and time
- Ticket must contain: request, risk, approval, config backup name, change made (rule name and ID), test result, removal date.
- Time: 30 to 90 minutes. Log under the ticket as Network.
- Update the client file network section and, for Omni+ Managed clients, the quarterly review change list.

## Related
- `19-vpn-user-setup.md`
- `17-scan-to-email-troubleshooting.md`
- `21-domain-dns-change.md`
- `26-after-hours-emergency-call.md`

# VPN User Setup

owner: Alex Rivera
last_reviewed: 2026-03-12
applies_to: Omni+ Basic and up, clients-with-firewall-vpn
tags: vpn, fortinet, unifi, remote-access, mfa, firewall

## Purpose
Give an approved user remote access to the office network through the client's firewall VPN, with MFA, and prove it works before closing the ticket.

## When to use
A client contact asks for VPN for a new or existing user (working from home, travelling, covering for someone). Not for cloud-only clients with no office resources. If the client does not have a VPN at all, that is a project, see `18-firewall-rule-change-request.md` and talk to Casey about scoping.

## Before you start
- Written approval from a contact in the client file. For credit union and legal clients, approval must come from the client's compliance or managing partner contact, not just office staff.
- Know the firewall model: FortiGate (FortiClient, IPsec or SSL VPN) or UniFi gateway (WireGuard or Teleport). It is in the client file under Network.
- Confirm the user's device is managed (N-central agent, SentinelOne, disk encryption). Personal home PCs: stop and ask Alex.
- Pull the firewall admin login from the vault: `Vault: <client-slug>/firewall-admin`.

## Steps
1. Open an Accelo ticket (category: Network). Paste the approval and the user's name, device name, and what they need to reach (file server, RDP host, line-of-business app).
   Check: ticket lists the exact internal resources, not just "the network".
2. Create or confirm the user account in the directory (AD or Entra) and add them to the VPN security group, e.g. `VPN-Users`. Do not add them to a group that has admin rights on the firewall.
   Check: `Get-ADGroupMember VPN-Users` or the Entra group blade shows the user.
3. On FortiGate: User & Authentication > User Groups, confirm the group maps to the VPN policy. Under VPN > IPsec Tunnels (or SSL-VPN Portals on older builds), confirm the group is in the policy and that the policy only allows the subnets and ports the ticket lists.
   Check: policy hit counter exists and the source is the VPN group, not "all".
4. On UniFi: Settings > VPN > create the WireGuard client for the user, download the config, and send it through the vault share, never by plain email.
   Check: the client appears under VPN > Connected Clients after the test.
5. Turn on MFA for the VPN login. FortiToken Mobile or Entra MFA through RADIUS/NPS, whichever the client already uses. Do not invent a new MFA system for one user.
   Check: the first login prompts for the second factor.
6. Install FortiClient (or the WireGuard app) on the user's device from N-central software deployment, or use the signed installer on `Vault: omnitechpro/software-share`. Push the connection profile.
   Check: the profile name and gateway hostname match the client file.
7. Test with the user, from outside the office (phone hotspot works). Connect, then open the file share and the line-of-business app they need.
   Check: `ping` the internal DNS server and open one real file. Ping alone is not a pass.
8. Give the user a short how-to: connect, disconnect, who to call. Remind them to disconnect when done, and that VPN is for work only.
9. Update the client file (VPN users list) and set a review date if access is temporary.

## Gotchas
- Newer FortiOS builds (7.6 and later) remove SSL VPN tunnel mode on some models. This changed in 2026. For any firewall that gets upgraded, move users to IPsec with FortiClient before the upgrade or they lose access. Check the firmware before you promise anything.
- Split tunnel vs full tunnel: most clients are split tunnel. A few compliance clients require full tunnel. Look at the existing policy and copy it.
- Home routers on a 192.168.1.x subnet collide with offices using the same subnet. If the VPN connects but nothing resolves, check this first and consider renumbering the office LAN as a project.
- DNS suffix not pushed: the share works by IP but not by name. Add the client's internal domain in the VPN DNS settings.
- Hotel and guest Wi-Fi often block IPsec ports. Try the phone hotspot before you change the firewall.
- RDP through the VPN to a workstation only works if the workstation is awake. Set "never sleep on AC" in the N-central power policy for those machines.

## Escalate when
- The user needs access to the server VLAN, the core banking network, or anything outside the ticket: Alex decides.
- The user's device is personal or unmanaged: Alex, then Casey if the client pushes back.
- You find an old VPN account for someone who has left: close it, then tell Alex. See `03-employee-offboarding.md`.
- Repeated failed VPN logins from outside the US in the firewall log: treat as a possible compromise, see `11-suspected-compromised-account.md`.

## Documentation and time
- Ticket: approval, group name, device, resources allowed, test result.
- Time entry: 0.5-1.0 hr for a normal setup. Firewall policy work is billed as Network, not Help Desk.
- Update the client file: VPN users, VPN type, firmware version you saw.

## Related
- `18-firewall-rule-change-request.md`
- `12-mfa-reset.md`
- `11-suspected-compromised-account.md`
- `03-employee-offboarding.md`

# Guest Wi-Fi Network Setup

owner: Sam Okafor
last_reviewed: 2025-08-19
applies_to: Omni+ Basic and up
tags: wifi, guest, vlan, unifi, aruba, segmentation

## Purpose
Set up (or fix) a guest Wi-Fi network that gets visitors on the internet without any path to the client's internal systems.

## When to use
A client asks for guest Wi-Fi, a patient/customer/visitor network, or complains that guests are on the same network as staff. Also used when auditing an existing guest SSID.

## Before you start
- Know the gear: UniFi (gateway plus APs), Aruba Instant On, or a FortiGate with managed APs. Check the client file under Network.
- Check the VLAN table in the client file. Guest should be its own VLAN, usually VLAN 30 with a 172.16.30.0/24 or 10.x.30.0/24 subnet. If the client file has a different number, use that one.
- Get approval from the client contact for the SSID name and the access method (shared password, voucher, or captive portal).
- Admin logins: `Vault: <client-slug>/switch-admin` and `Vault: <client-slug>/firewall-admin`.

## Steps
1. Open an Accelo ticket (category: Network). Note the SSID name, who gets the password, and bandwidth limit if any.
   Check: the client approved the SSID name in writing.
2. Create the guest VLAN on the gateway or firewall. Give it its own DHCP scope, DNS pointing at DNSFilter (not the internal DNS server), and a 1-hour lease.
   Check: a test device on the VLAN gets an address in the guest range.
3. Tag the VLAN on the switch ports that feed the APs (trunk ports) and on any uplinks. UniFi: Settings > Networks > Create New Network, type Guest. Aruba: configure the VLAN under Wireless > Networks.
   Check: AP ports show the VLAN as tagged in the switch port profile.
4. Create the guest SSID, WPA2/WPA3 personal at minimum. Turn on client isolation (UniFi: "Client Device Isolation"). Store the password: `Vault: <client-slug>/wifi-psk` with a note that this is the guest key.
   Check: two phones on the guest SSID cannot ping each other.
5. Write firewall rules: allow guest to internet (80, 443, 53 and what else the client needs), block guest to all internal ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16). The block rule must sit above the allow rule.
   Check: from a guest phone, you cannot reach the file server, the printer IP, or the firewall admin page.
6. Optional: bandwidth limit per client (e.g. 10 Mbps down) so guests do not eat the circuit. Set a captive portal with terms of use if the client wants it. Church and school clients usually do.
7. Print or send the sign-in instructions. A small card at reception works best.
8. Enable the SSID schedule if the client wants it off after hours.

## Gotchas
- Printers on the guest VLAN are a common request ("patients want to print"). Say no. If the client insists, call Alex.
- Do not reuse the staff PSK for guest "just for now". It never gets changed.
- Chromecasts, smart TVs, and Sonos need to be on the same VLAN as the phone that casts to them. Put the TV on guest only if staff do not cast to it.
- Old Aruba Instant On deployments cannot always do client isolation per SSID. Check the firmware. If not, tell the client and offer a UniFi swap quote.
- A guest network on the same IP range as a VPN user's home network is rare but breaks things. Pick a range that is not 192.168.0.x or 192.168.1.x.
- Dental and healthcare clients: the guest network must never carry anything PHI related. No exceptions, document that you told them.

## Escalate when
- The firewall does not support VLAN-based rules: Alex.
- The client wants to log guest activity or content-filter beyond DNSFilter: Casey (policy and liability question).
- You find guests on the staff VLAN during a visit: fix it now if you can, and tell Alex.

## Documentation and time
- Ticket: SSID, VLAN ID, subnet, rules added, test results.
- Update the client file VLAN table and the Wi-Fi section.
- Time: 1-2 hr for a standard UniFi site. Onsite portion goes on Sam's onsite time entry.

## Related
- `18-firewall-rule-change-request.md`
- `33-onsite-visit-checklist.md`
- `35-isp-outage-troubleshooting.md`

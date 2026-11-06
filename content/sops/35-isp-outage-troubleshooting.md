# ISP Outage Troubleshooting

owner: Alex Rivera
last_reviewed: 2025-03-11
applies_to: all-plans
tags: isp, internet, outage, circuit, firewall, modem, network

## Purpose
Work out quickly whether an internet outage is the ISP, the modem, the firewall, or something inside the office, and get the right party working on it.

## When to use
A client reports "the internet is down", N-central shows the whole site offline, or several users cannot reach websites or cloud apps. For a single user, see `36-slow-pc-troubleshooting.md` or the Help Desk process.

## Before you start
- Check priority: if it is the only circuit at the site, it is a P1 (business down). Call the primary contact. See `27-ticket-triage-and-priorities.md`.
- In the client file read Internet and circuits: ISP name, circuit type, account number, static IP, modem or ONT model, and the support number. Example ISPs in our area: Bayline Broadband (cable), Delmarva Link Fiber (fiber). Some sites have a backup LTE line.
- N-central: is the whole site offline, or just some devices? If all devices at a site stop checking in at the same time, that points to the circuit or the firewall.
- Portal: `Vault: <client-slug>/isp-portal`.

## Steps
1. Open an Accelo ticket (category: Network, priority per above). Log the time reported.
   Check: ticket has a start time.
2. Ask the client a few questions: is anything lit or blinking differently, did the power flicker, was anything changed today, are there other sites on the same ISP having trouble? Ask them to read you the lights on the modem and firewall.
   Check: you know the light status of the modem/ONT and the firewall WAN port.
3. Check the power. A UPS that has failed or a tripped power strip is a surprisingly frequent cause. Ask the client to confirm the modem, firewall, and switch are all powered.
4. Test from inside. From a PC at the site, `ping` the firewall (e.g. 192.168.1.1 or whatever the client file says). Then try `ping 203.0.113.1` style tests to a known outside address (use the one in the client file), and a DNS name.
   Check: if the firewall responds but the outside does not, the problem is the WAN side. If DNS names fail but IPs work, it is DNS.
5. Log in to the firewall (remotely over the backup LTE or by phone hotspot into the VPN, or by a person onsite). Check the WAN interface status: link up, IP assigned, gateway reachable. FortiGate: Network > Interfaces and Dashboard > Network. UniFi: Settings > Internet.
   Check: you can tell "no link", "link but no IP", or "IP but no traffic".
6. Reboot in order if safe and the client agrees: modem or ONT, wait 2 minutes, then the firewall. Do not power cycle the switch.
   Check: the modem shows sync and the firewall WAN gets its address.
7. If you still have no connectivity, call the ISP. Use the account number and the circuit ID. Say what you tested. Ask for the ticket number and an ETA. Follow `30-vendor-escalation.md`.
   Check: ISP ticket number is in the Accelo ticket.
8. While waiting: tell the client what to do. Phone hotspots for essential tasks, backup LTE, or a work-from-home plan. Tell them which systems will not work (cloud phone system, card terminals, VPN).
9. When service returns, test properly: firewall WAN up, VPN connects, a cloud app loads, the phone system registers. Make sure the static IP is the same. Check that backups will resume.
   Check: N-central shows the devices back online.
10. Ask the ISP for a root cause and a credit if the contract says so.

## Gotchas
- ISPs sometimes change a customer's static IP or gateway after an outage. The VPN, email rules, and allow lists that use the IP then break. Compare it to the client file.
- Bridge mode versus router mode on the ISP modem: if the ISP replaced the modem, the new one may be in router mode, giving the firewall a private address (double NAT). Ask for bridge mode.
- A "no internet" report that only affects Wi-Fi is usually not the ISP. Check APs and the switch PoE first.
- Rural sites on wireless ISPs lose service in storms and heavy rain. Note this in the client file. Do not spend hours looking inside the building.
- Do not factory-reset a firewall without a config backup. Config backups run weekly from N-central or the UniFi controller, check the date first.
- ISP phone support loops are slow. Ask for tier 2 or a field dispatch early for business accounts.

## Escalate when
- The site has been down more than 1 hour and the ISP has not given an ETA: Casey calls the account rep.
- Evidence of a firewall failure (no power, fault light, hardware error): Alex, start an RMA and a replacement plan.
- The outage is at several clients on the same ISP: tell Alex and Casey, it is likely a wider fault.
- Omni+ Managed or Omni+ Proactive clients with the 24x7 on-call target: follow `26-after-hours-emergency-call.md`.

## Documentation and time
- Ticket: reported time, tests done, light status, ISP case number, restoration time, root cause if known.
- Time: log waiting on the ISP as vendor call time (see `28-time-entry-standards.md`).
- Update the client file with ISP contact changes and new quirks.

## Related
- `30-vendor-escalation.md`
- `18-firewall-rule-change-request.md`
- `26-after-hours-emergency-call.md`
- `27-ticket-triage-and-priorities.md`

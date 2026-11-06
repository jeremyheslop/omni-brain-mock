# End-of-Life Hardware and Software Handling

owner: Casey Morgan
last_reviewed: 2025-10-02
applies_to: all-plans
tags: eol, hardware, lifecycle, risk, quotes, windows-server, firewall

## Purpose
Spot hardware and software that is out of support, tell the client in writing, and get either a replacement plan or a signed risk acceptance.

## When to use
- N-central shows an OS that is out of support (e.g. Windows Server 2012 R2, Windows 10 after support ended in October 2025 unless ESU is bought).
- A firewall, switch, or AP is past vendor end-of-sale or end-of-support.
- A server or workstation is older than its warranty and has had repeated failures.
- During a quarterly review (Omni+ Managed) or any onsite visit.

## Before you start
- Pull the device list from N-central > Devices > filter by OS and warranty. Export to CSV.
- Check the vendor lifecycle page for each product (Microsoft, Fortinet, Ubiquiti, SonicWall, Dell/HP). Write the real dates in the ticket.
- Check the contract in Accelo: does the plan include hardware lifecycle planning? Omni+ Proactive and Omni+ Managed do. T&M and Omni+ Basic clients get a courtesy notice only.

## Steps
1. Make a short list per client: device name, role, what is EOL, date support ended or will end, risk (internet-facing, holds data, runs a line-of-business app).
   Check: every row has a date and a role.
2. Open an Accelo ticket (category: Project, priority P4) per client. Attach the list.
3. Rate each item. High: internet-facing or holds client data and no security patches. Medium: internal only, patched until a near date. Low: spare or lab.
   Check: Alex reviewed the High items.
4. Prepare options with Casey: replace, upgrade in place, buy extended support, isolate on its own VLAN, or accept the risk. Get a quote from the usual distributor for the replace option.
5. Send the notice to the client's primary and billing contacts. Say what is out of support, what could go wrong (no security patches, no vendor help, cyber insurance questions), and what we recommend. Put dates on the proposal.
   Check: the email is in the ticket and the client acknowledged it.
6. If the client declines, get a signed risk acceptance (Casey's template in Drive > Contracts > Risk Acceptance). Save the PDF to the client record in Accelo.
7. For items we keep running: isolate in N-central as a "Legacy" device group, restrict in the firewall, and set a 90-day reminder to ask again.
8. When replacing, follow `05-laptop-refresh.md` for workstations or open a Project (P-0xxx) for servers and network gear. Wipe retired drives and record the disposal.

## Gotchas
- A server running the practice's one critical app on Server 2012 R2 does not "just upgrade". The vendor may not support the new OS. Ask the app vendor first.
- Cyber insurance questionnaires ask about unsupported systems. Clients forget to tell us when the renewal is due. Ask during the QBR.
- EOL firewalls still pass traffic, so clients think they are fine. A firewall with no firmware updates is the worst place to save money.
- Do not auto-quote Dell/HP prices from memory. They move weekly.
- Some old label printers and scanners need a Windows 7-era driver. Keep one VM for it, isolated, and note it in the client file.
- Windows 10 Pro devices that are not upgraded after the support end date: see `24-windows-10-to-11-upgrade.md` for ESU options and the client notice.

## Escalate when
- An internet-facing EOL device holds regulated data (health, financial, legal): Casey and Alex the same day.
- The client refuses both replacement and the risk acceptance: Casey.
- You find EOL gear that was not in the client file: tell Alex so the asset list gets corrected.

## Documentation and time
- Ticket: the list, dates, notice sent, client response, signed acceptance if any.
- Time: 0.5 hr per client for the review, more for quotes. Quote preparation is billable only if the contract says so; ask Casey.
- Update the client file asset list with EOL dates.

## Related
- `05-laptop-refresh.md`
- `24-windows-10-to-11-upgrade.md`
- `06-monthly-patch-review.md`
- `22-ssl-certificate-renewal.md`

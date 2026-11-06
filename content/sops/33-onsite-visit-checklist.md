# Onsite Visit Checklist

owner: Sam Okafor
last_reviewed: 2026-04-09
applies_to: Omni+ Proactive and up, T&M by appointment
tags: onsite, field, checklist, hardware, cabling, scheduling

## Purpose
Make every onsite visit predictable: show up prepared, finish the planned work, look for problems while you are there, and leave the client with a short written summary.

## When to use
Any visit to a client site: scheduled interval visits (Omni+ Proactive and Omni+ Managed), project work, hardware replacement, cabling, or a break-fix dispatch. Whoever goes, Sam or another tech, follows this list.

## Before you start
- Check the ticket or project, the client file, and the site entry under Sites and addresses (hours, parking, door codes in the vault, who meets you).
- Confirm the visit time with the primary contact the day before. Text or email, logged in the ticket.
- Check N-central for open alerts at that client and note anything to look at in person.
- Load the van: laptop, console cable, USB-to-serial adapter, cable tester, label printer, patch cables, spare Cat6, crimper, power strip, small UPS, USB drives with the Windows installer and driver pack, spare toner for common printers, zip ties, a flashlight.
- Check the warranty and spare parts. If you are swapping a switch, a firewall, or a Datto device, read the RMA notes first.
- Tell Jordan you are leaving and the expected return time, so incoming calls get routed.

## Steps
1. Create or open the Accelo ticket (category: Hardware or Onsite). Start the Travel entry when you leave.
   Check: the Travel entry has a start time.
2. Arrive, check in with the front desk or the contact, and wear the company shirt or badge. Ask where to work without disturbing people.
   Check: you know who to tell when you finish.
3. Walk through the main closet or server room first. Look at the firewall, switch, UPS, and backup device for lights, errors, heat, dust, and anything plugged in loosely. Take photos of the rack before you touch it.
   Check: photos are saved to the ticket.
4. Do the planned work. Use the relevant SOP (laptop refresh, printer setup, Wi-Fi). Label anything new: cables at both ends, devices with the hostname.
   Check: each task has a test, and the test passed.
5. Run the standard walk-around: UPS battery status and self-test, backup last job status, N-central agent online on every device, Windows updates pending, free disk on servers, printer and scanner test, Wi-Fi coverage in the weak spot, and the guest network isolation if one exists.
   Check: a short list of findings, even if it is "no issues".
6. Ask the contact if anything is annoying people. Take notes. The small things are what clients remember.
7. Clean up. Remove boxes, packaging, old drives for secure disposal, and leave the closet tidier than you found it.
8. Before leaving, summarise to the contact: what you did, what you found, what we recommend. If you found something that costs money, say it plainly and tell them Casey will follow up.
   Check: the contact agreed with the summary or you wrote their questions down.
9. Stop the on-site timer, start Travel back. Update the ticket from the van, not from the office next day.

## Gotchas
- Some sites need an escort or a badge to enter, such as the credit union and the school. Book it ahead.
- Dental and medical offices: do not work near patients, and do not move equipment in an operatory while it is in use.
- Do not "just reboot the firewall" during business hours. Even a 90 second outage drops card readers and VoIP.
- Take a photo before you unplug anything. You will forget which port was which.
- Old wiring closets hide extra switches nobody documented. Add them to the client file and N-central.
- Rural sites (grain, orchard, marine) can have poor mobile signal. Download the client file and the vault items for offline use before you leave.
- Do not leave your laptop or keys in the van in a lot overnight. Take them in.

## Escalate when
- You find something that looks like a security problem (unknown device, unauthorized remote tool, a cable to somewhere it should not go): Alex right away.
- The visit will run past scheduled hours or the client wants extra work: Casey for approval before you start.
- Safety issue (water in the server room, burning smell, damaged electrical): stop, tell the contact, and do not continue.

## Documentation and time
- Ticket: arrival and departure times, work done, findings, photos, recommendations, who you spoke to.
- Time: Onsite work against the ticket, Travel as a separate entry (see `28-time-entry-standards.md`). Contract-included visits still need the contract box ticked.
- Update the client file with new devices, labels, cable maps, and access changes.

## Related
- `20-wifi-guest-network.md`
- `25-server-reboot-window.md`
- `28-time-entry-standards.md`
- `16-printer-scanner-setup.md`
- `23-end-of-life-hardware.md`

# Printer and Scanner Setup

owner: Sam Okafor
last_reviewed: 2026-01-28
applies_to: all-plans
tags: printer, scanner, mfp, hardware, network, drivers

## Purpose
Install a network printer, copier (MFP), or document scanner so users can print and scan from their PCs without calling us next week.

## When to use
New printer or MFP, replacement unit, new user needing an existing printer, or a client moving a printer to a new location. For scan-to-email that stopped working use `17-scan-to-email-troubleshooting.md`.

## Before you start
- Approved quote or ticket in Accelo. Category Hardware, priority P4 (P3 if a team cannot print at all).
- Printer model, serial, and who services it (copier vendor or us). Many clients have a lease with a copier company that owns the settings on the machine.
- IP plan from the client file: printers get a static IP outside the DHCP scope, usually on the printer VLAN if the site has one.
- Admin login for the printer's web page: `Vault: <client-slug>/printer-admin`. If it is a new unit, set one and store it there.
- Driver: the manufacturer's universal driver or the model-specific driver. Download on the bench, not in front of the client.

## Steps
1. Unbox, power on, and connect the printer to the network by cable. Wi-Fi printing is a last resort.
   Check: the printer display shows an IP address.
2. Set a static IP in the printer's web page (Network > TCP/IP) or from the control panel. Use an address outside the DHCP range and record it. Do not rely on a DHCP reservation unless the client file says so.
   Check: you can ping it from a PC: `ping 192.168.10.45` (use the client's actual range).
3. Change the default admin password and store it in the vault. Turn off protocols nobody uses (Telnet, FTP, WINS). Leave HTTPS, IPP, and SMB if scanning needs it.
   Check: you can log in with the new password and the vault entry exists.
4. Set the date, time zone (Eastern), and NTP server. Wrong time breaks scan-to-email with TLS.
5. Add a printer to the PCs. Settings > Bluetooth & devices > Printers & scanners > Add device > "The printer that I want isn't listed" > Add using a TCP/IP address. Or use a print server on the client's server if they have one.
   Check: Print a test page from one PC.
6. For many PCs, create the printer once on the print server (or via an N-central script using `Add-Printer -Name "Front Office MFP" -DriverName "..." -PortName "IP_192.168.10.45"`) and push it.
   Check: the printer appears for users on next sign-in.
7. Set the default settings: black and white, duplex on, letter size. Most clients want these.
8. Set up scanning. Choose one:
   - Scan to email via SMTP relay (see `17-scan-to-email-troubleshooting.md` for server and port details).
   - Scan to folder on a share. Create a service account or use a dedicated share with limited rights. Do not use a user's own login.
   - Scan to cloud (OneDrive or SharePoint) if the printer supports it.
   Check: a test scan lands in the target within a minute.
9. For document scanners (Fujitsu fi-series at CPA offices), install PaperStream and the TWAIN/ISIS driver on the workstation. Test with the tax or document management software.
   Check: scan a 5-page document from the app and it opens.
10. Label the printer with its name and IP. Add it to the client file's printer list. Remove old printers from PCs.
11. Show the main user how to clear a jam, change toner, and who to call. Leave the support number on a sticker.

## Gotchas
- DHCP reservations and printers: if the router, a UPS card, and the printer all fight over one address, the printer drops off. Use a static IP and write it down.
- Copier vendors often block admin access. Ask them to open the SMTP or SMB settings or to do the setup with you on the phone.
- Windows keeps old printer drivers. If a print queue is stuck: `Restart-Service Spooler` and clear C:\Windows\System32\spool\PRINTERS.
- Print server on an old Windows Server 2012 box is a risk. Note it for `23-end-of-life-hardware.md`.
- Universal drivers work for printing but may lose finishing features (stapling, trays). Use the model driver if the client needs those.
- A USB-connected printer shared from someone's PC works until that PC is off. Move it to the network.
- WSD ports (the auto-discovered type) fail randomly. Use standard TCP/IP ports.

## Escalate when
- The printer is on a leased copier and the vendor controls it: Casey for vendor contact.
- Printing hits a security restriction (VLAN, firewall): Alex.
- A driver deployment breaks users' existing printing: Alex.
- Hardware fault under warranty: Casey for RMA.

## Documentation and time
- Record model, serial, IP, driver, and print server in the client file.
- Time: 1 to 2 hours per printer including testing. Log as Hardware with the onsite code.
- Attach a photo of the label and test page to the ticket.

## Related
- `17-scan-to-email-troubleshooting.md`
- `15-shared-mailbox-setup.md`
- `23-end-of-life-hardware.md`
- `33-onsite-visit-checklist.md`

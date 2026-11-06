# Scan-to-Email Troubleshooting

owner: Sam Okafor
last_reviewed: 2025-10-21
applies_to: all-plans
tags: scanner, mfp, smtp, email, m365, troubleshooting

## Purpose
Find out why a copier or scanner can no longer email scans and get it working again.

## When to use
"The scanner stopped sending email" or "we get an error on the printer screen". Almost always caused by a Microsoft 365 change, a password change, a firewall change, or an IP change. For first-time setup of a printer use `16-printer-scanner-setup.md`.

## Before you start
- Which device (model, IP) and which mailbox it uses. Look at the printer's web page: SMTP server, port, username, From address.
- Printer admin login: `Vault: <client-slug>/printer-admin`.
- Check whether anything changed recently: a password reset, a firewall update, an ISP change (the public IP matters for relay), or a Microsoft policy change.
- Accelo ticket, category Hardware or Help Desk, priority P3. Most clients rank this as urgent to them, but it is a P3 unless the whole office relies on scanning for client work.

## Steps
1. Reproduce the error. Send a test scan. Note the error text on the screen or in the printer log.
   Check: you have the exact error ("Authentication failed", "Connection timeout", "TLS error").
2. Check basics: printer powers on, IP responds to ping, internet works. Check the printer's date and time. Fix if wrong.
   Check: ping works and the time is correct.
3. Find out which method the printer uses.
   - SMTP AUTH to smtp.office365.com on port 587 with a licensed account.
   - Direct send to the MX endpoint (tenant.mail.protection.outlook.com) on port 25, no login, from the client's static public IP.
   - SMTP relay connector in Exchange, restricted by IP, on port 25.
   - Third-party SMTP relay (used on some older setups, e.g. a hosting provider).
4. Test from a PC on the same VLAN with PowerShell:
   `Test-NetConnection smtp.office365.com -Port 587`
   `Test-NetConnection <tenant>.mail.protection.outlook.com -Port 25`
   Check: TcpTestSucceeded is True. If False for port 25, the ISP or the firewall is blocking it.
5. If SMTP AUTH fails: check the account. Exchange admin center > Recipients > Mailboxes > (account) > Manage email apps > Authenticated SMTP must be on. Check the password has not changed or expired. Check that MFA is not forced on this account (use a Conditional Access exclusion for the printer account, approved by Alex).
   Check: sign-in logs in Entra show the printer's attempt and the result.
6. If the method is IP-based relay: confirm the client's public IP has not changed (compare the firewall's WAN interface with the static IP in the client file). Update the connector in Exchange admin center > Mail flow > Connectors if it did.
   Check: the connector lists the current IP.
7. Check the firewall for outbound rules or SMTP inspection. SonicWall and FortiGate both have an SMTP proxy that can break TLS. Look at the log for the printer's IP.
8. Check TLS. Older printers only speak TLS 1.0 or 1.1, which Microsoft no longer accepts. If the log says TLS handshake failed, update the firmware, or move to a local relay.
9. Test again. Scan a page to a mailbox you can check.
   Check: the email arrives with the attachment and from the right address.
10. If the printer is too old to be fixed, plan a replacement or use scan-to-folder in the meantime.

## Gotchas
- Microsoft keeps turning off Basic Auth. SMTP AUTH client submission with Basic Auth was scheduled to change in 2026. Check the current Microsoft message center notes before telling a client "it is the same as before". This SOP predates the final change.
- The "From" address must be a real mailbox or an address the connector accepts. A made-up From address gets rejected.
- Some scanners only work on port 465 (implicit TLS) or only on 25. Check the model manual. One client needed 465 and nothing else.
- If you reset the account password and the printer still has the old one, the account locks. Update the printer first, then confirm.
- Email may arrive but land in junk because of SPF. Check that the relay IP is in the SPF record.
- Large scans (over 20 MB) fail with "message too large". Lower the resolution to 200 dpi or switch to scan-to-folder.
- Users might have scan buttons set to old email names. Check the address book on the printer.

## Escalate when
- Firewall or Exchange connector changes are needed: Alex.
- It is a leased copier and the vendor must change settings: Casey contacts the vendor.
- The printer is end of life and cannot do TLS 1.2: Casey for a quote.
- The same failure comes back more than twice in a month: Alex looks at a long-term fix, like a local SMTP relay.

## Documentation and time
- Ticket: error text, method found, the fix. Record the working settings (server, port, From address, account name only) in the client file. No passwords.
- Time: 30 to 90 minutes. Log as Hardware.
- Add a gotcha line to the client file if the device has quirks.

## Related
- `16-printer-scanner-setup.md`
- `15-shared-mailbox-setup.md`
- `18-firewall-rule-change-request.md`
- `23-end-of-life-hardware.md`

# Ransomware Response

owner: Alex Rivera
last_reviewed: 2026-09-02
applies_to: all-plans
tags: ransomware, incident-response, security, p1, containment, backups, sentinelone

## Purpose
Contain a suspected ransomware infection fast, protect the backups, tell the right people in the right order, and start recovery from a known-good point.

## When to use
Any of these: files renamed with a strange extension, a ransom note on a desktop or share, SentinelOne raising a ransomware detection, many users unable to open files at once, a server's file shares suddenly encrypted. When in doubt, treat it as ransomware. A false alarm costs an hour. A slow response can cost the company.

## Before you start
- This is a P1. Set category "Security Incident". Call, do not email.
- Whoever sees it first calls Alex (410-555-0100 after hours). If no answer in 5 minutes, call Sam, then Casey. See `26-after-hours-emergency-call.md`.
- Do not turn anything off, wipe, or reinstall yet. Keep evidence.
- Open the client file for the network layout, backup devices, and contacts. Admin accounts: `Vault: <client-slug>/firewall-admin`, `Vault: <client-slug>/backup-appliance`.

## Steps
1. Open the Accelo ticket (Security Incident, P1). Note the time you first heard about it and who reported it. Start a running log in the ticket, with times.
   Check: the log has the first entry.
2. Contain. Identify the affected machines. In SentinelOne, use Network Quarantine (disconnect from network) on every affected device and any suspected ones. If you cannot reach SentinelOne, unplug the network cable or turn off Wi-Fi. Do not shut the machine down unless you have to; memory has useful evidence.
   Check: SentinelOne console shows the devices as "Disconnected from network".
3. Protect backups. Disconnect the Datto SIRIS or Cove backup from the network if the infected machine could reach it. In the Datto portal, pause scheduled deletions and retention changes. Do not delete restore points.
   Check: the last known-good restore point is listed and marked as protected.
4. Block the spread. On the firewall, disable VPN access and block outbound from the affected VLAN. If a file server is hit, disable the SMB shares from the affected accounts. Alex decides how far to go.
   Check: new files are not being encrypted. Watch the file server for 10 minutes.
5. Identify patient zero and the entry point. Check SentinelOne's storyline for the first detection, the Microsoft 365 sign-in logs, firewall VPN logs, and recent phishing reports. Disable the user account that was used. See `11-suspected-compromised-account.md`.
   Check: you have a probable start time and source account.
6. Notify. Casey calls the client's primary contact, and the owner if different. Discuss: legal counsel, cyber insurance carrier (many policies require notice within 24 to 72 hours), and regulators if protected data may be exposed (health, financial, legal, student records). We do not decide on regulatory reporting. The client does, with their counsel.
   Check: Casey logged who was told and when.
7. Decide on recovery. Alex and Casey agree on a plan: restore to a clean point from backup, rebuild affected machines, and rotate passwords. Never pay or negotiate. Do not contact the attackers.
8. Rebuild and restore. Wipe and reimage affected workstations. Restore servers from the last clean backup into an isolated network first. Scan before connecting.
   Check: the restored server passes a full SentinelOne scan.
9. Reset credentials: all admin accounts, the firewall, service accounts, VPN, and any user the attacker touched. Force sign-out of all M365 sessions. Review MFA methods for added devices.
10. Bring users back in stages. Monitor closely for 7 days. Keep the SentinelOne policy on the strictest protection mode during that time.
11. Write the incident summary within 5 business days: timeline, cause, impact, what worked, what we change.

## Gotchas
- Backups connected to the network and domain-joined often get encrypted too. This is why SIRIS and cloud copies matter. Check that the cloud copy is untouched before anything else.
- Do not log in to affected machines with a domain admin account. The attacker may still be watching.
- Attackers often sit inside for days before encrypting. Treat the whole network as suspect until proven clean.
- Clients with cyber insurance may need to use the insurer's approved response firm. Ask early. It changes who does what.
- Do not email about the incident from a possibly compromised M365 tenant. Use phone, and a clean channel if needed.
- Restoring the file server first and the domain controller last (or the reverse) matters. Check with Alex.

## Escalate when
- Always: Alex and Casey are involved in every ransomware case. This SOP does not stop at help desk.
- Evidence of data theft (large uploads, extortion note mentioning stolen data): Casey immediately, and the client contacts counsel.
- Backups are damaged or unavailable: Casey and the vendor, see `30-vendor-escalation.md`.
- The infection reaches more than one client: a shared tool may be compromised. Alex checks N-central and the remote access tools.

## Documentation and time
- Ticket: full timeline, devices, actions, who authorized what, recovery points used.
- Time: log every hour. These are P1 billable hours unless Casey decides otherwise.
- Update the client file after recovery with changes made. Review policies (EDR, backup, MFA) in a follow-up ticket.

## Related
- `11-suspected-compromised-account.md`
- `10-phishing-email-response.md`
- `08-daily-backup-check.md`
- `09-backup-restore-test.md`
- `26-after-hours-emergency-call.md`

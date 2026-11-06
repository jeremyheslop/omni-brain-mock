# Daily Backup Check

owner: Alex Rivera
last_reviewed: 2026-10-02
applies_to: Omni+ Basic and up
tags: backup, datto, cove, m365-backup, daily, monitoring

## Purpose
Look at last night's backup results for every managed client every morning, catch failures early, and make sure someone owns each one.

## When to use
Every business day by 9:00 AM Eastern. Whoever is on help desk does the first pass (usually Jordan). Alex owns anything that needs real work. Covers Cove Data Protection (Omni+ Basic), Datto SIRIS and Datto SaaS Protection (Omni+ Proactive and Omni+ Managed).

## Before you start
- Logins: Datto Partner Portal, Cove management console, Datto SaaS Protection dashboard. Credentials are under `Vault: omnitechpro/datto-portal` and `Vault: omnitechpro/cove-console`.
- N-central backup monitoring dashboard open (Dashboards > Backup Status).
- The Accelo queue "Backup" so you can see what is already open.
- Know which clients are in a maintenance window or have a planned shutdown this week.

## Steps
1. Open N-central > Dashboards > Backup Status. Note any red or amber devices.
   Check: you have a list of clients and devices that did not report success.
2. Open the Datto Partner Portal. Check each SIRIS for: last successful backup, last offsite sync, screenshot verification result, and storage use.
   Check: every protected server shows a backup in the last 24 hours (last 4 hours during business days for servers on hourly schedules).
3. Open the Cove console. Filter by "Last session status" not equal to Completed. Check cloud-only clients (Omni+ Basic).
   Check: failed or "completed with errors" sessions are listed with the reason.
4. Open the Datto SaaS Protection dashboard. Check that Exchange, OneDrive, SharePoint, and Teams backups ran for each protected tenant.
   Check: the last backup is within 24 hours and no seat is flagged "paused" or "unprotected".
5. For each failure, look at the screenshot verification and the logs. Typical causes: agent offline, VSS error, server rebooted mid-job, disk full on the appliance, ISP outage at the client.
6. Open one Accelo ticket per client with a problem. Category: Backup. Priority: P3 for a single missed night, P2 for two nights in a row or any failure on a server holding line-of-business data.
   Check: ticket exists and the Datto or Cove error text is pasted in.
7. For simple fixes (restart the agent, rerun the job), do them and rerun now. Watch it start.
   Check: job shows Running, then Completed.
8. For anything you cannot fix in 30 minutes, assign to Alex and add your notes.
9. At the end, post a one-line summary in the team chat: "Backups checked 8:40, 2 failures, tickets T-24xxx and T-24xxx".

## Gotchas
- Datto "screenshot failed" is not the same as "backup failed". It still needs a ticket but is lower urgency unless it fails 3 nights.
- A backup that says Completed with 0 bytes changed on a busy server is suspicious. Check that the right volumes are selected.
- Cove sessions that run while a laptop sleeps will show as missed. For laptops, 3 missed days is the real threshold.
- Datto SaaS Protection quietly drops new users until you add the license. When a new hire is created, check this (see `14-m365-license-changes.md`).
- Do not mark a ticket resolved from the portal view alone. Wait for the next full night's backup to pass.
- A client's backup can fail because their ISP is down. Check `35-isp-outage-troubleshooting.md` before blaming the appliance.
- Omni+ Managed and Omni+ Proactive clients get a weekly backup summary in Accelo. If you skip the daily check, that report will show a gap.

## Escalate when
- Any server has no good backup for 48 hours: Alex immediately, and Casey calls the client.
- A SIRIS reports a hardware fault (disk degraded, fan, RAID): Alex, and open a vendor case per `30-vendor-escalation.md`.
- Ransomware indicators on a protected machine (mass file renames, encrypted files in the backup): stop and go to `34-ransomware-response.md`. Do not run any restore or retention change.
- Offsite sync is behind more than 3 days: Alex.

## Documentation and time
- Daily check time is internal overhead: log 20 to 30 minutes against the internal "Backup Monitoring" task, not a client ticket.
- Time spent fixing a client's backup goes on that client's ticket.
- Note repeat offenders in the client file gotchas section (e.g. "file server backup fails if the nightly report job runs long").
- Update the backup section of the client file if an agent or schedule changes.

## Related
- `09-backup-restore-test.md`
- `34-ransomware-response.md`
- `35-isp-outage-troubleshooting.md`
- `30-vendor-escalation.md`

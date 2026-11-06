# Monthly Patch Review

owner: Alex Rivera
last_reviewed: 2026-08-04
applies_to: Omni+ Basic and up
tags: patching, n-central, windows-update, maintenance, monthly

## Purpose
Review, approve, and verify the monthly Windows and third-party patches across managed clients so they land on a predictable schedule and nothing important is skipped.

## When to use
Every month, starting the Wednesday after Microsoft Patch Tuesday (second Tuesday). Covers all Omni+ Basic, Omni+ Proactive, and Omni+ Managed clients. T&M clients are not monitored; patch them only when asked.

## Before you start
- N-central > Devices > Patch Management open, filtered by customer.
- List of clients with tax-season freeze windows, year-end close, or other blackout dates. This is in the client file under the contract notes.
- Latest Patch Tuesday notes (any known problem KBs). Check the vendor release notes and a trusted news source before approving.
- Accelo: make sure there is a recurring "Monthly Maintenance" task per client. See `process-plans/monthly-maintenance.md`.

## Steps
1. On the Wednesday after Patch Tuesday, go to N-central > Devices > Patch Management > Patches. Sort by status "Pending Approval".
   Check: the list shows this month's cumulative updates and .NET updates.
2. Approve patches for the pilot group first. Pilot = Alex's test VM, the OmniTechPro internal PCs, and one low-risk device at each Omni+ Managed clients who agreed to be a pilot.
   Check: pilot devices show "Approved" and a scheduled install time.
3. Wait 5 business days. Watch the pilot for boot problems, blue screens, or app breakage. Check Accelo for any new tickets that mention updates.
   Check: no related tickets and pilot devices report "Installed".
4. If the pilot is clean, approve the rest: Patch Management > select patches > Approve for All Devices. Exclude servers at this step.
   Check: the Approved count matches the Pending count minus the servers.
5. Set the install window. Workstations default to nightly 11:00 PM with reboot allowed. Servers use the window in the client file (see `25-server-reboot-window.md`).
   Check: the patch profile for each customer shows the right window.
6. Approve server patches one client at a time during the agreed week. For a client with an SQL or line-of-business server, tell the primary contact the evening before.
   Check: the Accelo task for that client notes the planned server window.
7. After the install window, run the Patch Status report (N-central > Reports > Patch Status) per customer. Export to PDF for Omni+ Managed clients.
   Check: any device with failed patches or not seen in 7 days is listed.
8. Open tickets for failures using `07-failed-patch-remediation.md`. Group by client.
9. Check third-party patching (Chrome, Adobe Reader, Zoom, 7-Zip) in the same view and approve any that are pending.
10. Record completion in the monthly maintenance task and update the dashboard note in Accelo.

## Gotchas
- Never approve patches for a CPA client's tax server between January 15 and April 20 without Alex checking first. Security-only patches are an exception and still need a call.
- Feature updates (like Windows 11 version upgrades) are NOT part of monthly patching. They go through `24-windows-10-to-11-upgrade.md`.
- Laptops that are closed at 11 PM do not patch. Check "last seen" and push to the next time they are online.
- N-central shows "Installed" before a reboot is finished. Look for the "Reboot pending" flag.
- A device offline for 30 days is probably gone. Do not keep chasing it. Ask the client.
- As of 2026 the report layout changed in N-central and the old Patch Summary export no longer includes the reboot-pending column. Use Patch Status instead.

## Escalate when
- A cumulative update causes boot loops on more than one device: stop approvals and tell Alex and Casey.
- A client's compliance report shows more than 5 percent of devices missing critical patches for 30 days: Casey sends a note to the client.
- Patch approvals for a regulated client (credit union, healthcare) are blocked by their change control: Casey.

## Documentation and time
- Log monthly time against each client's Monthly Maintenance task, not a generic internal task. Typical: 15 to 30 minutes per client for review, more for servers.
- Attach the Patch Status PDF to the ticket for Omni+ Proactive and Omni+ Managed clients. Omni+ Managed reports go in the quarterly review pack.
- Note any skipped devices and the reason in the task.

## Related
- `07-failed-patch-remediation.md`
- `25-server-reboot-window.md`
- `24-windows-10-to-11-upgrade.md`
- `process-plans/monthly-maintenance.md`

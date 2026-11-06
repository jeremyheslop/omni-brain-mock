# Server Reboot and Maintenance Window

owner: Alex Rivera
last_reviewed: 2025-11-06
applies_to: Omni+ Proactive and up
tags: servers, reboot, maintenance-window, patching, change-control, n-central

## Purpose
Reboot a client server (after patching or to clear a fault) at a time that does not hurt the business, with warning, a clean shutdown order, and a check that everything came back.

## When to use
- Monthly patch reboots (see `06-monthly-patch-review.md`).
- A server needs a restart to fix a hung service.
- Firmware, hypervisor, or Datto SIRIS maintenance that needs the server off.

## Before you start
- Look up the client's agreed maintenance window in the client file and in Accelo contract notes. Typical: Sunday 11:00 PM to 3:00 AM, or Tuesday 6:00 PM for firms that cannot take weekends.
- CPA clients: never reboot a tax server from January 15 to April 18 without Alex and a client-approved window. See `31-cpa-tax-season-software-prep.md`.
- Check that the last backup finished. N-central or the Datto portal should show a good job in the last 24 hours. See `08-daily-backup-check.md`.
- Tell the client at least 2 business days ahead for planned reboots. Send the notice through the Accelo ticket.
- Know the dependencies. A domain controller, then the file/app server, then the app services. For a hypervisor host, list the VMs.

## Steps
1. Create an Accelo ticket (category: Network or Hardware, priority P4 for planned work). Put in the window, the servers, the reason, and who at the client approved.
   Check: approval is attached.
2. Day of: confirm nobody is working. Check active sessions with `query user /server:<name>` or Task Manager > Users. For file servers, `Get-SmbOpenFile | Measure-Object`.
   Check: no one logged in, or the open files are acceptable and the user has been told.
3. Pause the N-central monitoring for the server (Devices > select > Maintenance Mode) so the reboot does not raise Critical alerts.
   Check: the device shows the maintenance icon.
4. Stop application services in order if the app vendor says to (SQL, accounting, practice management). For a hypervisor, shut down VMs cleanly: apps first, file server, then domain controllers last.
   Check: services show Stopped.
5. Reboot with `shutdown /r /t 60 /c "Planned maintenance, OmniTechPro"` or from the hypervisor console. Watch the console for the boot, because some old boxes sit at a RAID or BIOS prompt.
   Check: ping returns and RDP or the console login is available.
6. After boot, check services (`Get-Service | Where Status -eq Stopped | Where StartType -eq Automatic`), the event log for errors, disk space, and domain controller replication (`repadmin /replsummary`).
   Check: every automatic service is running.
7. Test the business function: open the practice or accounting app from a workstation and open a file from the shares. Ask a client contact to test if they are online.
8. Take the server out of maintenance mode. Run a manual N-central patch scan and confirm the patch status is clean.
9. Close out with a note to the client: done, anything unusual, next planned window.

## Gotchas
- A server that "has been up 400 days" often will not come back cleanly. Assume it may not, and have the Datto restore path ready.
- Some line-of-business databases (older SQL Express instances) need a manual service start after reboot. The client file lists them if they are known.
- Hyper-V hosts with a domain controller VM that is also needed to unlock BitLocker or log in can deadlock. Check the order in the client file.
- iDRAC and iLO consoles are your friend. If you do not have the license or IP, find out before the window, not during.
- Do not reboot during a Datto backup. Check the SIRIS status first.
- "Quick reboot at lunch" requests from the owner: it is a P2 only if the server is hung. Otherwise offer the window.

## Escalate when
- The server does not come back in 15 minutes: Alex. If Alex is already doing it, call Casey and start the client notice.
- A boot error mentions disk, RAID, or "operating system not found": stop, do not retry reboots, call Alex, preserve the console screen.
- The window overruns and the business opens: call the client contact, tell them the real status, and follow `26-after-hours-emergency-call.md` if after hours.

## Documentation and time
- Ticket: window, who approved, start and end times, what you checked, anything that failed.
- Time: log the actual hands-on time. If you were waiting for a long boot, log it under the same ticket as "monitoring reboot".
- Update the client file with any new boot-order or service quirks.

## Related
- `06-monthly-patch-review.md`
- `07-failed-patch-remediation.md`
- `08-daily-backup-check.md`
- `26-after-hours-emergency-call.md`

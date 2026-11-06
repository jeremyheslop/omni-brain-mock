# Failed Patch Remediation

owner: Alex Rivera
last_reviewed: 2026-02-20
applies_to: Omni+ Basic and up
tags: patching, n-central, windows-update, troubleshooting, remediation

## Purpose
Find out why a device failed to install a patch and get it patched, or decide that it needs a rebuild.

## When to use
After the monthly review (`06-monthly-patch-review.md`) lists failed devices, or when an N-central patch alert fires on a single device. Same steps for servers and workstations, with extra care on servers.

## Before you start
- The device name and the failed KB number from N-central > Devices > (device) > Patch Management.
- Check that the user is not in the middle of something. Remote in with N-central Take Control only after asking, unless it is a server in its window.
- Free disk space check. Under 10 GB free on C: is the most common cause.
- Be ready to snapshot or note the state before you change anything on a server.

## Steps
1. Open the device in N-central. Look at Patch Management > History for the error code. Note it in the ticket.
   Check: ticket contains the KB and the error (e.g. 0x80070005, 0x800f0922, 0x80073712).
2. Check free space and pending reboot. In PowerShell:
   `Get-PSDrive C` and `Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'`
   Check: you know how much space is free and whether a reboot is pending.
3. Reboot the device if a reboot is pending, at an agreed time. Re-run the patch install from N-central (Patch Management > Reinstall/Retry).
   Check: status moves to "Installed" or you get a new error.
4. If it fails again, reset Windows Update components. In elevated PowerShell or a script from the N-central script library (Automation > Windows Update Reset):
   `net stop wuauserv; net stop bits; Rename-Item C:\Windows\SoftwareDistribution SoftwareDistribution.old; net start bits; net start wuauserv`
   Check: C:\Windows\SoftwareDistribution is recreated and Windows Update shows a fresh scan.
5. Run system file repair:
   `DISM /Online /Cleanup-Image /RestoreHealth` then `sfc /scannow`
   Check: both commands complete without unrepairable errors. Save the log path in the ticket.
6. Retry the patch. If it still fails, download the KB from the Microsoft Update Catalog and install it by hand: `wusa.exe C:\temp\<kb>.msu /quiet /norestart`.
   Check: `Get-HotFix -Id KB<number>` returns a row.
7. If the problem is a specific bad KB (several devices failing the same way), decline that patch in N-central so it stops retrying, and open one parent ticket. Note it in the monthly task.
   Check: the patch shows "Declined" and retries stop.
8. If the device is a server, do steps 4 to 6 only inside the client's reboot window. See `25-server-reboot-window.md`.
9. If nothing works after 90 minutes, schedule an in-place repair upgrade (Windows setup with "keep files and apps") for workstations. For servers, talk to Alex before attempting it.
10. Confirm the device is green in N-central after the next scan and close the ticket.

## Gotchas
- 0x80070005 is usually a permissions or security tool problem. Check whether SentinelOne is holding a file. Do not turn off EDR to get a patch through unless Alex says so.
- Devices that have been off for weeks sometimes need 3 or 4 reboots to catch up. Do not call it failed after one pass.
- Small SSDs (128 GB) fill up with Windows.old and update caches. Run Disk Cleanup > Clean up system files before anything fancy.
- Servers with Windows Server 2016 and old servicing stacks sometimes need the SSU installed first.
- N-central can show "Failed" for a patch that is already installed through another path. Check `Get-HotFix` before you spend an hour.
- Do not run DISM against a PC that a user is actively working on. It can slow it to a crawl.

## Escalate when
- The same device fails two months in a row: Alex decides between rebuild and replace.
- A server will not boot after a patch: treat as P1. Follow `26-after-hours-emergency-call.md` if it is after hours.
- Failures cluster at a single client (more than 3 devices with the same error): Alex, and check for a GPO or proxy change.
- Device is out of warranty and failing repeatedly: Casey, to talk to the client about replacement (`23-end-of-life-hardware.md`).

## Documentation and time
- One ticket per client for the month, one line per device. Category: Help Desk, priority P3 (P2 for servers).
- Record the fix that worked in the ticket so the next tech does not redo it. If it was weird, add a line to the client file gotchas.
- Time entries go on the ticket. Typical: 20 to 45 minutes per workstation.

## Related
- `06-monthly-patch-review.md`
- `25-server-reboot-window.md`
- `23-end-of-life-hardware.md`
- `36-slow-pc-troubleshooting.md`

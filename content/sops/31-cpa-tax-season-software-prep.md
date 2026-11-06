# CPA Tax Season Software Update Prep and Change Freeze

owner: Alex Rivera
last_reviewed: 2025-12-08
applies_to: cpa-clients
tags: tax-season, cpa, change-freeze, cch, drake, ultratax, quickbooks, updates

## Purpose
Get every CPA client's tax and accounting software fully updated and tested before the change freeze starts on January 15, and keep changes off their systems until the freeze ends on April 18.

## When to use
Every year, starting in October. Applies to accounting clients (e.g. Tidewater Ledger CPAs, Pocomoke Bay Tax & Advisory, Kingfisher Bookkeeping) and any other client that files returns for others. Bookkeeping clients on QuickBooks only still follow the freeze for QuickBooks and the file server.

## Before you start
- Pull the list of CPA clients and their software from the client files: CCH Axcess or ProSystem fx, Drake Tax, UltraTax CS, QuickBooks Desktop Enterprise or Online, TaxCaddy, SafeSend, scanners, and large printers.
- Check each vendor's release schedule. Tax vendors publish the update that adds the new tax year forms in November through January. Do not install on the first day it appears. Wait a few days for the bug reports.
- Check the backups. Quarterly restore test must have run in the last 90 days for Omni+ Managed. See `09-backup-restore-test.md`.
- Casey sends the client the freeze notice in early November: what the freeze is, what we will and will not do, and the emergency path.

## Steps
1. October: open an Accelo project per client, "Tax Season Prep <year>". Add tasks for software updates, hardware checks, backup test, user list review, and the freeze notice.
   Check: every CPA client has a project and a target completion date of January 10.
2. October to November: hardware and capacity check. Disk space on the file server, RAM on the terminal server or tax workstations, scanner and printer condition, UPS batteries. Replace failing items now. Sam does the onsite part.
   Check: no workstation has less than 20 percent free disk.
3. November to December: install the tax-year software updates as the vendor releases them, on one test workstation first, then the rest. CCH Axcess and ProSystem fx: follow the vendor's staged update. Drake: the client's Drake admin runs the update, we help with the network install location. UltraTax CS: update the server first, then workstations.
   Check: a sample return opens and prints on every workstation.
4. Update QuickBooks Desktop to the current release and run the file verify tool on the company file. Confirm the database server manager is running.
   Check: multi-user mode works from two workstations.
5. December: Windows and Microsoft 365 patching. Complete everything and approve nothing new after January 10. See `06-monthly-patch-review.md`.
   Check: N-central patch status shows no pending approved patches.
6. Check user accounts. Add seasonal staff now, remove stale ones. Make sure MFA is working for all. See `02-new-user-onboarding.md` for new hires.
7. Early January: final backup, a restore test of the tax data folder, and a screenshot of the working state in the ticket.
8. January 15: start the freeze. In N-central, move CPA devices to the "Tax Freeze" patch policy (approve only critical security patches that Alex signs off). Add a banner to the client file: FREEZE ACTIVE.
9. During the freeze: break-fix only. No hardware refreshes, no OS upgrades, no new software, no firewall firmware, no server reboots without Alex and a client-approved window. See `25-server-reboot-window.md`.
10. April 18 (or the next business day if it falls on a weekend): end the freeze after the client confirms they filed. Many ask for an extension window until the extension deadline. Ask each client.
    Check: the client confirms in writing, and the banner in the client file is removed.
11. Late April: catch-up patching, the deferred projects, and a post-season review ticket.

## Gotchas
- Freeze does not mean "ignore security". A critical SentinelOne or Windows zero-day fix goes in, with Alex approving and a restore point first.
- Tax vendors sometimes force an update by blocking the old version. Read their release notes and call the client before the date.
- Check the exact freeze dates each year. If the calendar changes, update this SOP and tell Casey.
- Remote workers' home PCs are the weak spot. Make sure every tax preparer works on a managed machine.
- Printers that handle tax forms (check stock, toner, drivers) fail at 5:00 PM on a Friday in March. Have a spare toner and a loaner printer.
- A new hire in the middle of the freeze: do the user and mailbox, but do not install anything on the tax server without Alex.

## Escalate when
- A tax software update fails or breaks a return: Alex, then the software vendor via `30-vendor-escalation.md`.
- A client asks us to break the freeze for a non-urgent request: Casey decides.
- A server fails during the freeze: P1, Alex and Casey, restore plan first.

## Documentation and time
- Per client project: tasks, versions installed, test results, freeze start and end dates.
- Time: Project during prep, Help Desk during the freeze. Do not bill freeze-period project work unless Casey approves.
- Update the client files with the software versions and the year.

## Related
- `06-monthly-patch-review.md`
- `09-backup-restore-test.md`
- `24-windows-10-to-11-upgrade.md`
- `25-server-reboot-window.md`
- `30-vendor-escalation.md`

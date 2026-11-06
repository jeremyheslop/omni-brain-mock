# Windows 10 to Windows 11 Upgrade

owner: Jordan Blake
last_reviewed: 2026-01-14
applies_to: Omni+ Basic and up
tags: windows-11, upgrade, tpm, patching, workstations, n-central

## Purpose
Move a Windows 10 workstation to Windows 11 without losing the user's apps, data, or a day of work. Replace the machine when it cannot be upgraded.

## When to use
Any Windows 10 PC still in use after support ended (October 2025). Do the upgrade on machines that pass the hardware check. Machines that fail the check go to the refresh list, see `05-laptop-refresh.md`.

## Before you start
- Check the freeze calendar. CPA clients are frozen January 15 to April 18, see `31-cpa-tax-season-software-prep.md`. No upgrades in that window.
- N-central > Devices > select > Custom Properties or the OS filter to list Windows 10 devices for the client.
- Check backup status first. Do not upgrade a workstation with local-only data and no sync.
- Confirm the line-of-business apps support Windows 11. Ask the vendor, or check the client file.
- Tell the user and the office manager the date and the expected downtime: about 1 to 2 hours per machine, mostly unattended.

## Steps
1. Open an Accelo project (P-0xxx) for the client, with one task per machine. For a single PC, a normal ticket is fine (category: Hardware, priority P4).
   Check: each machine has its own task so time is traceable.
2. Check hardware compatibility. On the PC run `Get-Tpm` (TPM 2.0, Present and Ready), `Confirm-SecureBootUEFI` (True), and check CPU generation against the Microsoft list. Minimum: 4 GB RAM, 64 GB storage. We want 8 GB and an SSD.
   Check: all three pass. If not, mark the machine "replace" and stop.
3. Update BIOS and drivers first, through the vendor tool (Dell Command Update, HP Image Assistant) or N-central patch policy.
   Check: no pending driver or BIOS update on the vendor tool.
4. Make sure BitLocker keys are saved to Entra/AD. `manage-bde -protectors -get C:` and compare with the Entra device record.
   Check: the recovery key shows in Entra under the device.
5. Run the upgrade. Preferred: Windows 11 feature update through N-central Patch Management > feature update policy, during a maintenance window. Fallback: Windows 11 Installation Assistant on the device.
   Check: N-central shows Windows 11 build 26100 or later (24H2 or newer) after reboot.
6. Log in as the user. Check: printers, mapped drives, Outlook profile, browser extensions, line-of-business apps, scanner software, and the VPN client.
   Check: the user opens their main app and a printed test page comes out.
7. Re-run the N-central patch scan and confirm SentinelOne and the N-central agent report healthy.
8. Walk the user through changes (taskbar, right-click menu). Offer to move the taskbar left if they ask. It takes two minutes and saves a call.
9. Close the task. Update the client asset list.

## Gotchas
- A "compatible" PC with a 7th-gen Intel CPU can pass the checker through registry tricks. Do not use the bypass. We replace those.
- Dual monitor setups sometimes reset their layout. Warn people with three monitors, and see whether the dock firmware needs an update.
- Old scanner drivers (Fujitsu fi-series with PaperStream, some Canon models) may need a reinstall after the upgrade.
- Office add-ins, especially legacy Excel ones for accounting, can break. Test before you hand the PC back.
- Rolling back is possible for 10 days (Settings > System > Recovery) unless disk cleanup removed the old files. Do not run cleanup right after.
- Devices that stay on Windows 10 after the end of support: Casey sends the notice and offers ESU through the client's licensing. Treat as an EOL item, see `23-end-of-life-hardware.md`.

## Escalate when
- A line-of-business app fails after the upgrade and a rollback is needed: Alex.
- More than three machines at one site fail the hardware check: Casey for a refresh quote.
- BitLocker asks for a recovery key that is not in Entra: Alex before you do anything else.

## Documentation and time
- Ticket or task: hardware check output, backup status, BIOS version, build number after.
- Time: 1 hr per machine (hands-on 20-30 min). Log under the task, not the parent project.
- Update the client file: asset list, OS version, any app that needed a fix.

## Related
- `05-laptop-refresh.md`
- `23-end-of-life-hardware.md`
- `31-cpa-tax-season-software-prep.md`
- `06-monthly-patch-review.md`

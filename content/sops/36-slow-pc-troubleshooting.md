# Slow PC Troubleshooting

owner: Jordan Blake
last_reviewed: 2025-09-24
applies_to: all-plans
tags: slow-pc, performance, help-desk, troubleshooting, disk, memory, n-central

## Purpose
Find out why one PC is slow and fix it in a repeatable order, starting with the quick checks, so you do not spend an hour on something a reboot or a full disk explains.

## When to use
A user says their computer is slow, freezing, or takes forever to start. If many users at the same site are slow at once, it is probably the network or a server, see `35-isp-outage-troubleshooting.md` and ask Alex.

## Before you start
- Ask: when did it start, is it slow all the time or in one app, did anything change (new software, update, new monitor), and when did they last restart?
- Open the device in N-central (Devices > select > Summary and Performance). Look at CPU, memory, and disk graphs for the last day.
- Check that N-central shows the machine age and warranty. A 7-year-old PC with 4 GB RAM and a hard drive does not need troubleshooting. It needs replacing, see `05-laptop-refresh.md`.
- Open an Accelo ticket (category: Help Desk, priority P3).

## Steps
1. Restart the PC if it has been up more than a week. `(Get-CimInstance Win32_OperatingSystem).LastBootUpTime` shows the last boot. Many "slow" tickets end here.
   Check: after restart, the user confirms whether it is better.
2. Connect with N-central Take Control, or phone the user. Open Task Manager (Ctrl+Shift+Esc) > Performance. Look at CPU, Memory, Disk, and Network.
   Check: you know which one is pinned near 100 percent.
3. Disk at 100 percent: look at the Processes tab, sorted by Disk. Common causes are Windows Update, a SentinelOne scan, OneDrive syncing a large folder, or a failing hard drive. Run `Get-PhysicalDisk | Select FriendlyName,HealthStatus,MediaType`. A MediaType of HDD in a PC made after 2018 is a reason to replace it with an SSD.
4. Memory above 85 percent: check how many browser tabs, which apps, and the installed RAM. 8 GB is the floor, 16 GB for accounting, CAD, or anyone with many browser tabs. Add RAM if the machine supports it.
5. CPU high: find the process. A stuck Teams, Outlook, or a browser with a heavy extension is typical. A process you do not recognise gets checked against SentinelOne and a quick search. If you suspect malware, see `10-phishing-email-response.md`.
6. Free space: `Get-PSDrive C`. Under 15 percent free slows Windows. Clear the Downloads folder (ask first), run Disk Cleanup, and have the user move big files to the server or OneDrive.
   Check: free space is above 20 percent after cleanup.
7. Startup items: Task Manager > Startup apps. Disable obvious junk (updaters, music apps, toolbars). Do not disable SentinelOne, N-central, or the VPN client.
8. Updates and drivers: check for pending Windows updates, BIOS, and graphics/chipset drivers. In N-central, check the patch status for the device.
9. Network-specific slowness: if only web apps or file shares are slow, test the connection. Compare Wi-Fi and wired, run a speed test, and check the VPN. A user on a bad Wi-Fi spot looks like "a slow PC".
10. Outlook slow: check the OST file size, the number of shared mailboxes with "download shared folders", and cached mode setting. See `15-shared-mailbox-setup.md`.
11. If nothing works: back up the user's data, and reimage using the standard image, see `04-new-workstation-setup.md`. Often faster than a long hunt.
    Check: the user signs off that it is better, and you recheck the graph a day later.

## Gotchas
- "Slow after a Windows update" is often the feature update still indexing. Give it a day and a restart before you start changing things.
- SentinelOne scans can spike disk on old machines. Do not turn it off. Ask Alex to schedule the scan outside working hours.
- OneDrive "Files On-Demand" off plus a huge synced mailbox archive equals a very slow laptop. Check the sync folder size.
- Remote desktop sessions to a busy terminal server are slow when the server is the problem, not the PC. Check the server graphs in N-central.
- Laptops on power-saving mode (battery saver set permanently) look slow. Check the power plan.
- Dock and monitor problems can look like lag. Try without the dock.
- Do not install "PC cleaner" or "speed up" tools. Ever.

## Escalate when
- The disk shows SMART warnings or the drive is clicking: back up first, then tell Sam for replacement.
- More than three users at one client report slowness the same day: Alex, check the server, switch, and ISP.
- You find unknown software or a SentinelOne detection: Alex, treat as a security incident.
- A line-of-business app is slow for everyone: contact the vendor through `30-vendor-escalation.md` after Alex confirms the server is healthy.

## Documentation and time
- Ticket: symptoms, what the graphs showed, the cause, the fix, and whether the user confirmed.
- Time: 0.5 hr for typical cases. If it passes 1.5 hr, step back and consider the reimage.
- Record patterns. If a client has several slow machines, add a hardware refresh note to the client file for Casey.

## Related
- `05-laptop-refresh.md`
- `04-new-workstation-setup.md`
- `24-windows-10-to-11-upgrade.md`
- `35-isp-outage-troubleshooting.md`

# Laptop Refresh

owner: Sam Okafor
last_reviewed: 2025-09-18
applies_to: Omni+ Proactive and up, T&M (billable project)
tags: laptop, refresh, hardware, migration, data-transfer

## Purpose
Replace a user's old laptop with a new one and move their data and settings over with as little downtime as possible.

## When to use
Planned refreshes (warranty end, age 4+ years, Windows 10 hardware that cannot go to 11) and approved replacements for failed laptops. For a brand new seat with nothing to migrate use `04-new-workstation-setup.md`.

## Before you start
- Approved quote or PO in Accelo. Refresh schedule from the quarterly review if the client is on Omni+ Proactive or Omni+ Managed.
- Schedule a time with the user. Plan for end of day or a day they are out. Do not do a CPA partner's laptop in March.
- Ask the user to sign out of everything they can and to list any local-only files (Desktop, Downloads, PST files, local QuickBooks files).
- Chargers, docks, and monitors on the new machine side. Confirm what is being reused.
- Old laptop serial and asset tag from the client file.

## Steps
1. Build the new laptop per `04-new-workstation-setup.md` on the bench first, up to and including the line-of-business apps.
   Check: new laptop is online in N-central and has no pending updates.
2. Before swap day, check OneDrive status on the old laptop. Right-click the OneDrive icon > Settings > Backup. Desktop, Documents, Pictures should say "Backed up".
   Check: OneDrive shows no sync errors and the web view shows the latest files.
3. Copy local-only data. Use robocopy to an external drive or a network share, not drag and drop:
   `robocopy C:\Users\<name> E:\refresh\<name> /E /R:1 /W:1 /XD AppData /LOG:E:\refresh\<name>.log`
   Check: the log shows no failed copies.
4. Export what does not live in the cloud: Outlook signatures, browser bookmarks if the user is not signed in to Chrome or Edge sync, Wi-Fi profiles if needed, local printer settings, QuickBooks company file location, tax software settings.
5. Swap day: bring the new laptop to the user, sign them in, confirm MFA, let OneDrive sync, restore local data.
   Check: the user can open their last 3 working files without help.
6. Reconnect printers, scanner shortcuts, mapped drives, VPN client, and any certificates.
   Check: test print and VPN connection both work.
7. Have the user open their daily apps one at a time while you watch. Fix sign-ins and licensing as you go.
8. Remove the old laptop from N-central (Devices > select > Delete) only after the user has been on the new one for two business days. Disable the old device in Entra the same day.
9. Wipe the old laptop. Use the vendor reset with a full disk wipe for SSDs, or `cipher /w:C:` is not enough on its own. Record the wipe in the ticket. For disposal see `23-end-of-life-hardware.md`.
   Check: the wipe confirmation is attached to the ticket.
10. Update the asset list and warranty dates in the client file and the Accelo asset record.

## Gotchas
- Outlook profile and PST files are the number one thing people forget. Ask specifically. Some users still have a 20 GB archive PST on the Desktop.
- Browser saved passwords: if the user is not signed in to a synced profile, they will lose them. Make sure they know before you wipe.
- Docking stations are the other half of the refresh. A new USB-C laptop on an old DisplayLink dock can mean a black screen. Test on the bench.
- Watch the two-device limit on some line-of-business licenses (e.g. certain tax and practice apps). Deactivate on the old machine first.
- If the old laptop had BitLocker, save the recovery key before you do anything risky with it.
- This SOP was written before the Windows 11 rollout. New laptops are Windows 11 now, so expect UI differences in the user's first week, especially Start menu and taskbar.

## Escalate when
- The old laptop will not boot and the user has data that is not in OneDrive: Alex (data recovery) and tell Casey about the client risk.
- A line-of-business license cannot be moved: Casey contacts the vendor.
- The user is a partner or owner and the swap runs past 90 minutes: let Casey know so the client gets a call.

## Documentation and time
- Bench time and swap time as separate entries, category Hardware.
- Log what data was moved and from where, in the ticket. If something went missing, this note is how we find it.
- Update the asset list. Add the old device to the disposal list.

## Related
- `04-new-workstation-setup.md`
- `23-end-of-life-hardware.md`
- `24-windows-10-to-11-upgrade.md`
- `process-plans/new-hire-workstation.md`

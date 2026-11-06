# New Workstation Setup

owner: Sam Okafor
last_reviewed: 2026-03-12
applies_to: Omni+ Basic and up, T&M (billable project)
tags: workstation, hardware, imaging, n-central, intune, setup

## Purpose
Take a new PC out of the box and turn it into a managed, patched, encrypted machine the user can sit down at and work on.

## When to use
Any new desktop or laptop for a client, whether it is for a new hire, an added seat, or a one-off replacement. For a scheduled swap of an old machine use `05-laptop-refresh.md`. For the user account side use `02-new-user-onboarding.md`.

## Before you start
- Accelo ticket or task with the approved quote or PO attached. No approval, no unboxing.
- Client file open: naming prefix (e.g. `TLC-WS-014` style), domain or Entra join type, line-of-business app list, printer list.
- Serial number written on the ticket before you open the box. Warranty check on the vendor site while you are at it.
- Bench space and a wired connection. Do not set up on guest Wi-Fi.
- Know who the machine is for. A shared front desk PC gets a different profile than a partner's laptop.

## Steps
1. Unbox, record the serial and asset tag in the Accelo asset record. Stick the OmniTechPro asset label on the bottom or back.
   Check: asset record shows serial, model, purchase date, and warranty end date.
2. Boot to the first-run screen. For Pro editions, choose "Set up for work or school" and sign in with the user's Entra account if the client is cloud-joined. For domain-joined clients, skip the account step with the offline option and join the domain after naming.
   Check: the device appears in Entra admin center > Devices (or in AD Computers) under the right name.
3. Rename the PC to the client convention. Run in elevated PowerShell:
   `Rename-Computer -NewName "TLC-WS-014" -Restart`
   Check: `hostname` returns the new name after reboot.
4. Run Windows Update until it says "You're up to date". Plan on 2 or 3 rounds. Also install the latest vendor driver pack (Dell Command Update, HP Image Assistant, or Lenovo System Update).
   Check: Settings > Windows Update shows no pending items and Device Manager has no yellow marks.
5. Install the N-central agent from the client's installer (N-central > Administration > Customers > pick the client > Download Agent/Probe). Confirm the device shows up under the right customer and site.
   Check: the device is online in N-central > Devices within about 5 minutes and has the standard automation policies applied.
6. Confirm SentinelOne installs through the N-central policy. If not, push it manually from the SentinelOne console under the client's site group.
   Check: S1 shows the device as "Active, Protected" and the N-central security column is green.
7. Install baseline apps: Microsoft 365 Apps, Chrome or Edge as per client, Adobe Reader, 7-Zip, the client's line-of-business apps (tax software, Dentrix, Clio, AutoCAD, etc.). Sign in to Office with the user's account.
   Check: Word opens without the "unlicensed" banner.
8. Turn on BitLocker and save the recovery key to Entra or AD. Verify with `manage-bde -status C:`.
   Check: Protection Status says On, and the recovery key is visible against the device in Entra.
9. Map printers and shared drives. Test print and, if there is a scanner, test a scan to folder or email.
   Check: printed page came out of the right printer.
10. Apply the client's standard settings: power plan, lock screen timeout (10 minutes unless the client says otherwise), default browser, desktop shortcuts.
11. Create a local admin account only if the client file calls for it. Store the password in the vault as `Vault: <client-slug>/local-admin-<hostname>`.
    Check: vault entry exists. Do not paste the password anywhere else.
12. Sign in as the user (or have the user sign in with you) and confirm MFA, email, OneDrive sync, and the main business app all work.
13. Update the asset list in the client file and close the Accelo task.

## Gotchas
- Windows 11 OOBE tries to force a Microsoft account on Home editions. Never buy Home. If a client bought one, upgrade the edition before you do anything else.
- OneDrive Known Folder Move can sync the whole Desktop of an old profile into the new one. Check it before the user starts saving things.
- Quick Assist and N-central remote control are different things. Make sure the N-central agent is installed before you leave the bench, or you will drive back out.
- Some CPA tax apps (CCH Axcess Local, Drake) want install as admin and specific .NET versions. Check the app notes in the client file first.
- Dell and HP laptops ship with trial AV. Uninstall it before SentinelOne goes on or you will get a long boot.
- Label the power brick with the user's name. Sam learned this the hard way in a 12-person office with 12 identical Dells.

## Escalate when
- Domain join fails or the device cannot find a domain controller: Alex.
- The agent installs but never reports in to N-central after 15 minutes: Alex.
- BitLocker cannot save a key to Entra: Alex before you finish.
- The machine fails hardware tests out of the box: Casey handles the vendor RMA.

## Documentation and time
- Bench time goes on the Accelo task under the workstation sub-task, category Hardware. Typical bench time is 2 to 3 hours per machine.
- Travel and delivery time on a separate entry with the onsite code.
- Update the client file asset list and the user's record. Add the serial and warranty date.

## Related
- `02-new-user-onboarding.md`
- `05-laptop-refresh.md`
- `24-windows-10-to-11-upgrade.md`
- `process-plans/new-hire-workstation.md`

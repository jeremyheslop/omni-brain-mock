# Backup Restore Test

owner: Alex Rivera
last_reviewed: 2025-07-14
applies_to: Omni+ Proactive and up (quarterly on Omni+ Managed)
tags: backup, restore, datto, testing, quarterly, omni-managed

## Purpose
Prove that a client's backup can actually be restored, and record how long it takes. A green backup job is not evidence.

## When to use
Quarterly for Omni+ Managed clients (part of the contract). Twice a year for Omni+ Proactive clients (we do this, but it is not promised in writing). On request for Omni+ Basic clients, billed as project time. Also after a SIRIS replacement or a major server change.

## Before you start
- Pick the test target from the client file: one file server share, one VM or server image, one mailbox or OneDrive item.
- Tell the client's primary contact the date. No disruption expected but they should know.
- Isolated place to restore to. Do not restore over production.
- Datto Partner Portal access and a free VM host (the SIRIS itself can virtualize, or a lab host in Salisbury).
- Last quarter's test notes in the ticket history so you can compare restore times.

## Steps
1. Create an Accelo ticket: category Backup, priority P4, title "Quarterly restore test, <client>, <quarter>". Use the recurring Omni+ Managed task if it exists.
   Check: ticket has a due date within the quarter.
2. File-level test. In the Datto Partner Portal open the SIRIS > protected machine > Restore > File Restore. Pick a recovery point from 7 or more days ago. Restore a folder with 10 or more files to a temp location.
   Check: files open, sizes match, and timestamps look right.
3. Image-level test. Use Virtualize via Hypervisor or Instant Virtualization on the SIRIS for one server. Put the VM on an isolated network.
   Check: the VM boots to the login screen, services start, and you can sign in with a local admin account.
4. Application check inside the VM. Open the line-of-business app (e.g. a tax database, QuickBooks company file, Dentrix) and load one record.
   Check: data opens and the most recent entry is from the right date.
5. Microsoft 365 test. In Datto SaaS Protection, restore one mailbox folder or OneDrive file to a test user or export it.
   Check: item is in the destination and opens.
6. Time everything: time to find the recovery point, time to first file, time to VM boot, time to app. Write them in the ticket.
   Check: you have four numbers.
7. Shut the VM down and delete the test restore. Remove any temp data.
   Check: the SIRIS shows no running virtual machines, and the temp folder is empty.
8. Compare with the client's recovery time target in the contract. If the VM boot is over 30 minutes, say so in the notes.
9. Write a short result summary for the quarterly business review: tested, passed or failed, time, issues found.
   Check: summary is saved to the client's Accelo record.
10. If anything failed, open a P2 backup ticket and notify Casey.

## Gotchas
- Do not boot a restored VM on the client LAN. Duplicate IPs and duplicate AD servers cause a real outage.
- Restores from cloud (not the local SIRIS) can be many times slower. Test one cloud restore once a year so nobody is surprised.
- Datto virtualization needs enough RAM on the appliance. Smaller SIRIS models cannot virtualize two large servers at once.
- BitLocker or application-level encryption can make a restored file unreadable without keys. Check that the keys are in the vault.
- Past tests have caught missing volumes (a data drive never added to the job). Always check that the list of protected volumes matches the server.
- The older Cove-only clients have no virtualization option. For them, test a file restore and a full-image download if the client asks.

## Escalate when
- The restore fails or the VM will not boot: Alex now, Casey tells the client in the next update.
- Backup data turns out to be missing for more than a week: P1 and Casey calls the client.
- You cannot meet the target restore time and the client expects it: Casey, to talk about equipment or contract changes.

## Documentation and time
- Time on the quarterly ticket, category Backup. Plan 2 to 3 hours per client.
- Attach a screenshot of the restored file and the VM console.
- Update the backup section of the client file with date of last test and result.
- Note it in the quarterly business review pack for Omni+ Managed clients.

## Related
- `08-daily-backup-check.md`
- `34-ransomware-response.md`
- `30-vendor-escalation.md`
- `company/service-plans.md`

# Shared Mailbox Setup

owner: Jordan Blake
last_reviewed: 2025-11-05
applies_to: all-plans
tags: exchange, shared-mailbox, m365, permissions, scan-to-email

## Purpose
Create a Microsoft 365 shared mailbox (such as info@, billing@, or scans@), give the right people access, and make it behave the way people expect.

## When to use
A client wants a team inbox, a scanner mailbox, a mailbox that needs to be kept after an employee leaves, or a "send as" address for a department. For scanner mail relay problems use `17-scan-to-email-troubleshooting.md`.

## Before you start
- Written request from an authorized contact with: mailbox name, email address, who gets access, and what rights each person needs (read, send as, send on behalf).
- Check that the address is not already used by a user, group, or alias: Exchange admin center > Recipients, search for the address.
- Check the domain is verified in the tenant and has the right mail flow.
- Accelo ticket, category Help Desk, priority P4.

## Steps
1. In Exchange admin center > Recipients > Mailboxes > Add a shared mailbox. Enter a display name and the email address. Click Create.
   Check: the shared mailbox shows in the list with type "Shared".
2. Add members. Select the mailbox > Delegation > Read and manage > Edit > add users. Add "Send as" for those who must send from the shared address.
   Check: each member is listed under the correct permission.
3. Or use PowerShell:
   `New-Mailbox -Shared -Name "Billing" -DisplayName "Billing" -PrimarySmtpAddress billing@clientdomain.example`
   `Add-MailboxPermission -Identity billing@clientdomain.example -User jane@clientdomain.example -AccessRights FullAccess -AutoMapping $true`
   `Add-RecipientPermission -Identity billing@clientdomain.example -Trustee jane@clientdomain.example -AccessRights SendAs`
   Check: `Get-MailboxPermission billing@clientdomain.example` lists the user.
4. Decide where "Sent Items" go. By default, mail sent as the shared mailbox lands in the sender's own Sent Items. To copy it to the shared mailbox:
   `Set-Mailbox billing@clientdomain.example -MessageCopyForSentAsEnabled $true -MessageCopyForSendOnBehalfEnabled $true`
   Check: a test send shows up in the shared mailbox Sent Items.
5. Wait 15 to 60 minutes. Auto-mapping takes time. Have the user restart Outlook. If it does not show up, add it manually via File > Account Settings > More Settings > Advanced.
   Check: the mailbox appears in the user's Outlook folder list.
6. Send a test message to the shared address from outside the company and reply as the shared address.
   Check: the message arrives and the reply shows the shared address as the sender.
7. If it is used for scanning or app mail, do not give it a password. Use SMTP relay or SMTP AUTH on a separate licensed account only if the device requires it. See `17-scan-to-email-troubleshooting.md`.
8. Add the mailbox to the client file with its purpose, members, and whether it has a license.
9. Close the ticket after the requester confirms they can send and receive.

## Gotchas
- Shared mailboxes cannot be signed in to directly unless you give them a password and turn sign-in on. Don't. Use delegation.
- Under 50 GB and no archive means no license is needed. Over 50 GB, add an Exchange Online Plan 2 license or the mailbox stops receiving.
- Auto-mapping can pile ten shared mailboxes into someone's Outlook. Use `-AutoMapping $false` for people who only need it occasionally.
- If a user is converted to a shared mailbox after they leave, the license is removed after conversion. Never reverse that order.
- New shared mailboxes can take up to 60 minutes before "Send as" works. Don't tell the client it's broken before an hour passes.
- Calendar sharing for shared mailboxes is its own permission. Add it with `Add-MailboxFolderPermission` if they want a shared calendar.
- Outlook for Mac and mobile do not auto-map. Show the user how to add it.

## Escalate when
- The mailbox needs to appear in a distribution list that sends external mail with a shared address: Alex checks the mail flow rules.
- Mailbox is for compliance or legal hold: Alex and Casey.
- Mail from the shared address lands in recipient spam: Alex checks SPF, DKIM, and DMARC for the domain.

## Documentation and time
- Ticket: address, members, permission types, test results.
- Time: 15 to 30 minutes. Log under the ticket.
- Update the client file shared mailbox list and the Accelo contact record if the address will be used for billing or alerts.

## Related
- `02-new-user-onboarding.md`
- `03-employee-offboarding.md`
- `14-m365-license-changes.md`
- `17-scan-to-email-troubleshooting.md`

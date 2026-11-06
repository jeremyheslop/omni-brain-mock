# Client Offboarding (Leaving OmniTechPro)

owner: Casey Morgan
last_reviewed: 2025-04-17
applies_to: all-plans
tags: offboarding, client-exit, contracts, handoff, credentials, billing

## Purpose
Close out a client who is leaving us (non-renewal, closure, acquisition, or switching MSPs) cleanly: hand over what is theirs, remove our access, stop billing and monitoring on the right date, and keep a record. This is about a whole client leaving. For one employee leaving a client, see `03-employee-offboarding.md`.

## When to use
Casey receives written notice of termination, or a contract end date passes without renewal, or the client is closing the business. Start the moment notice is received, not on the last day.

## Before you start
- Casey owns this SOP end to end. Alex does the technical removal. Jordan closes tickets and billing items.
- Read the contract in Accelo for the notice period, the termination terms, and what we owe them (documentation, passwords, data return).
- Get the end date and the new provider's contact in writing. Be polite and cooperative even if the exit is unfriendly. Do not hold anything back that the contract says is theirs.

## Steps
1. Open an Accelo project (P-0xxx) called "Offboard: <client name>" with tasks for each step below. Link open tickets.
   Check: project has an end date and an owner for every task.
2. Confirm the final date with the client and send a written confirmation: last day of service, last invoice, what we will hand over.
   Check: client replied or acknowledged.
3. Prepare the handoff package: network diagram, IP and VLAN list, device inventory, license list, ISP and vendor contact list, and the list of admin accounts. Export these from the client file in Omni Brain or Accelo.
   Check: the package is in a folder only Casey and Alex can open.
4. Transfer credentials the client is entitled to. Use a secure method, not email. The vault shared folder for `<client-slug>` can be shared with the client's chosen contact, or export with Casey's approval. Do not share any `Vault: omnitechpro/...` items.
   Check: the recipient confirmed they can sign in to each item.
5. On the last day (or the agreed handover date), change or remove our access: delete our admin accounts in M365 and Entra, remove our delegated admin (GDAP) relationship in Partner Center, remove our VPN and RDP entries, and take our remote support tools off the endpoints.
   Check: sign in as a test and confirm we are removed from admin roles.
6. In N-central: remove the SentinelOne agents or hand the console over (if the client owns the license), uninstall the N-central agents from devices, and delete the customer from N-central after the agents are off. Remove the Datto SIRIS from our portal or transfer ownership.
   Check: no devices show for the customer and no active alerts remain.
7. Backup data: the client may want a final copy. Export through Datto or Cove only with Casey's approval. Keep backups for the retention period in the contract, then delete and log the date.
8. Cancel recurring items: M365 license resale (move to the new partner via a CSP transfer or tell the client to buy direct), DNSFilter, Proofpoint, domain and certificate renewals. Check each vendor portal.
   Check: the vendor billing page shows the customer cancelled or transferred.
9. Billing: final invoice, prorate, remove the contract from the recurring invoice run in Accelo. Casey reviews the final invoice.
10. Close tickets, set the Accelo client status to Inactive (do not delete), and archive the client file in `4-Archives`. Keep the records for the retention period in our policy.

## Gotchas
- Delegated admin (GDAP) relationships linger for months if forgotten. It looks bad when a former client sees us in their audit log.
- The domain registrar account is often in our name for old clients. Transfer it carefully, since losing a domain is the one mistake that cannot be undone.
- A client leaving for another MSP often asks for "all the passwords" on the first day. Ask the new MSP to confirm in writing who the contact is.
- Do not wipe or remove the agents before the handover day. We were told "next Friday" once and the client's new MSP was not ready.
- Firewall and ISP records often list us as the technical contact. Ask the ISP to change it or we get the outage calls.
- Unpaid invoices: handover obligations in the contract still apply. Casey decides, not the techs.

## Escalate when
- Anyone other than Casey receives the notice: tell Casey the same day.
- The client asks for data we think belongs to a third party or a former employee: Casey, and possibly legal advice.
- The client wants to leave tomorrow: Casey and Alex agree on a plan before anyone touches their systems.

## Documentation and time
- Everything goes in the offboarding project. Log time as Project, billable only if the contract says so.
- Final note in Accelo with the date access was removed and who confirmed.
- Update the shared vendor list: remove the client from monitoring dashboards.

## Related
- `03-employee-offboarding.md`
- `01-new-client-onboarding.md`
- `30-vendor-escalation.md`
- `28-time-entry-standards.md`

# Domain and DNS Change

owner: Alex Rivera
last_reviewed: 2026-02-04
applies_to: all-plans
tags: dns, domain, registrar, mx, spf, dkim, email

## Purpose
Make a DNS change (add, edit, or remove a record) without breaking email or the website, and with a way back if it goes wrong.

## When to use
Pointing a website at a new host, changing MX records, adding SPF/DKIM/DMARC entries, adding a verification TXT record for a vendor, moving DNS between providers. A domain registration transfer is different, tell Casey.

## Before you start
- Written request from an authorized contact. DNS changes can take down a business, so we do not take them from a phone call alone.
- Find out where DNS is hosted. Registrar and DNS host are often different. Run `nslookup -type=NS example.com` and compare with the client file.
- Registrar login: `Vault: <client-slug>/domain-registrar`. If the client owns it and nobody knows the login, stop and start the recovery with the contact first.
- Export the current zone. Screenshot it or copy it into the ticket as text.

## Steps
1. Open an Accelo ticket (category: Other, or Network if tied to a firewall change). Paste the request, the approval, and the current zone export.
   Check: the ticket has a "before" copy of every record you will touch.
2. Lower the TTL on the record you will change to 300 seconds, at least a day ahead when you can. If the change is urgent, skip this and expect a delay.
   Check: `nslookup -debug example.com` shows the new TTL.
3. Write down exactly what you will add or change: type, host, value, priority, TTL. Have the client or vendor confirm the values by email.
   Check: the vendor's instructions match what you wrote, character for character.
4. Make the change in the DNS host's console. For MX changes, add the new records first, remove the old ones only after mail flow is proven.
   Check: the record shows saved, not pending.
5. Verify from outside with `nslookup -type=MX example.com <public-resolver>` or an online DNS checker. Test both the public resolver and the client's DNSFilter resolver.
   Check: the answer matches the new value from at least two resolvers.
6. Email-related changes: send a test message to and from an outside address. Run an SPF/DKIM/DMARC check on a test message header.
   Check: header shows `spf=pass`, `dkim=pass`.
7. Website changes: load the site from a phone off Wi-Fi, check the certificate, and check `www` and the bare domain.
8. Raise the TTL back to 3600 after 24 hours.
9. Update the client file DNS section with the final records.

## Gotchas
- Only one SPF record per domain. If you add a second TXT starting with `v=spf1`, mail starts failing. Merge into one with all the `include:` entries.
- DKIM for Microsoft 365 uses two CNAME records (selector1 and selector2). Some DNS hosts auto-append the domain name and you end up with `example.com.example.com`. Check the saved result.
- A CNAME cannot sit on the bare domain next to MX records. Use an A record or ALIAS.
- Registrar "forwarding" and "parked" settings can override your records. Turn them off.
- Old Passportal notes sometimes list DNS records that were changed years ago. Trust the live zone, not the old doc.
- When a client is on GoDaddy or similar with an employee's personal account, get the account moved to a company-owned login before touching anything.

## Escalate when
- Mail stops flowing after a change and you cannot fix it in 15 minutes: roll back to the export, then call Alex.
- The domain is expiring in under 30 days, or the contact is unknown: Casey.
- Anyone asks you to change nameservers on a domain tied to a credit union or title company without a ticket: Casey and Alex, since that pattern is also how domain hijacking looks.

## Documentation and time
- Ticket: before and after records, TTL, times, and the test results.
- Time: 0.5 hr for a simple add, 1-2 hr for MX or nameserver moves. Waiting time for propagation is not billable.
- Update the client file and the domain expiration date.

## Related
- `22-ssl-certificate-renewal.md`
- `15-shared-mailbox-setup.md`
- `10-phishing-email-response.md`

# SSL Certificate Renewal

owner: Alex Rivera
last_reviewed: 2025-05-22
applies_to: Omni+ Proactive and up
tags: ssl, tls, certificates, renewal, rds, firewall, web

## Purpose
Renew or replace expiring SSL/TLS certificates on client servers, firewalls, and web apps before users see a browser warning or an app stops connecting.

## When to use
- An N-central alert or monthly review shows a certificate expiring inside 30 days.
- A client reports a "your connection is not private" warning.
- A new service needs a certificate (RDS gateway, remote web portal, SSL VPN portal).

## Before you start
- Find every place the certificate is installed. Common spots: IIS web sites, RD Gateway and RD Web, the firewall's VPN portal, Exchange hybrid connectors (rare now), Remote Desktop listener, a vendor app like a practice management web portal.
- Know the certificate provider and the account. Most are bought through the client's registrar or a reseller. Login: `Vault: <client-slug>/domain-registrar` or `Vault: omnitechpro/cert-reseller`.
- Check who owns DNS, since domain validation needs a TXT or CNAME record. See `21-domain-dns-change.md`.

## Steps
1. Open an Accelo ticket (category: Other). Add the certificate name, expiry date, and where it is installed.
   Check: the ticket lists every server or device that uses it.
2. Generate a CSR on the server that will use the certificate. IIS: Server Certificates > Create Certificate Request. FortiGate: System > Certificates > Generate. Use 2048-bit RSA at minimum.
   Check: the CSR file exists and the subject name matches the hostname users type.
3. Submit the CSR to the provider and finish domain validation (email, DNS TXT, or file). DNS validation is easiest if we manage DNS.
   Check: the provider shows "issued".
4. Download the certificate and the intermediate chain. Keep the private key on the server, never in email or the ticket. If the cert has to move between machines, use a password-protected PFX and put the password in the vault.
5. Install. IIS: Complete Certificate Request, then Bindings > Edit > pick the new certificate. RD Gateway: Properties > SSL Certificate. FortiGate: VPN or admin settings > select the new certificate.
   Check: `certlm.msc` shows the new cert with the private key icon.
6. Test from a machine outside the network. Open the URL in a browser and click the padlock to confirm the new expiry date. Test the real workflow, such as an RDP connection through the gateway.
7. Remove the old certificate after a week, not before.
8. Set a reminder in Accelo for 45 days before the new expiry and update the client file.

## Gotchas
- Public certificates now have short lifetimes, and the maximum keeps dropping. Anything we still renew by hand once a year will move to a shorter cycle. Prefer automated renewal (ACME) where the app supports it.
- The chain matters. A missing intermediate works in your browser and fails in a phone app or a scanner. Test with an online SSL checker.
- RD Web and RD Gateway can use different certificates on different servers. Renewing only one gives a warning on half the connections.
- Wildcard certificates cover one level only. `*.example.com` does not cover `a.b.example.com`.
- Old servers (Server 2012 R2 and earlier) may not trust the newer root. Check before you buy.
- Self-signed certificates on printers and cameras are normal. Do not spend time on them unless an app rejects them.

## Escalate when
- The certificate is already expired and a client system is down: P2 minimum, call Alex.
- The private key is lost or the original server is gone: Alex decides whether to reissue.
- The client wants a certificate for something we do not manage (a website built by a web agency): tell Casey, we usually decline to touch it.

## Documentation and time
- Ticket: old and new expiry dates, install locations, test results.
- Time: 1 hr per certificate for a simple IIS install, up to 2 hr with a gateway and firewall.
- Update the client file certificate table and the vendor account notes.

## Related
- `21-domain-dns-change.md`
- `18-firewall-rule-change-request.md`
- `06-monthly-patch-review.md`

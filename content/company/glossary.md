# Glossary of MSP Terms

owner: Jordan Blake
last_reviewed: 2026-05-18
tags: company, glossary, terminology, training

Plain-English definitions for terms used in the wiki, tickets, and tool names. If a term in a client file or SOP is not here, it probably should be. Add it.

## The business

**MSP (Managed Service Provider)**: a company that runs IT for other businesses for a recurring fee. OmniTechPro is one.

**Break-fix / T&M (time and materials)**: the older model: something breaks, we fix it, we bill by the hour. A client with no core service plan is T&M.

**Managed services**: we monitor and maintain a client's systems all the time, not just when something breaks. Paid monthly.

**Service plan**: what a client buys from us. Each client has at most one core plan (Omni+ Basic, Omni+ Proactive, or Omni+ Managed) plus any add-ons such as Omni+ Advanced Security or Server Backup. In Accelo they are the values of the "Service Plans" category. See `company/service-plans.md`.

**Segmentation**: Accelo's name for a custom category on a record. Companies carry two: Industry and Service Plans.

**SLA (Service Level Agreement)**: a written promise about how fast we respond or how available a system will be. Ours are first-response targets per priority.

**Contract**: the agreement in Accelo that sets a client's hours and terms.

**QBR (Quarterly Business Review)**: a meeting with an Omni+ Managed client to review tickets, risks, and upcoming projects.

**BAA (Business Associate Agreement)**: a HIPAA contract that lets us handle a healthcare client's data. Required for medical and dental clients.

**Tribal knowledge**: things the team knows that are not written down. The thing this project is trying to fix.

## Tools and systems

**PSA (Professional Services Automation)**: software for tickets, time tracking, contracts, and billing. Ours is Accelo.

**RMM (Remote Monitoring and Management)**: software that sits on each computer and server, reports health, installs patches, and allows remote control. Ours is N-central.

**Agent**: the small program the RMM installs on a device. No agent, no monitoring.

**Device (in N-central)**: any workstation, server, or network device we monitor. Names like `TLC-SRV01`.

**Alert**: a message from the RMM that something crossed a threshold: disk full, service stopped, backup failed, offline. Severities are Critical, Warning, Info.

**Documentation platform**: where we keep client information. Today it is Passportal plus Google Drive plus memory. Omni Brain is meant to replace that.

**Vault**: the password manager. Docs only ever hold a reference like `Vault: <client-slug>/firewall-admin`, never the password itself.

**EDR (Endpoint Detection and Response)**: security software on a computer that watches for attacks and can isolate the machine. Ours is SentinelOne. More capable than classic antivirus.

**DNS filtering**: a service that blocks bad websites at the lookup stage. Ours is DNSFilter.

**Email gateway**: a filter in front of the mailboxes that catches spam, phishing and malware. We use Proofpoint Essentials for Omni+ Managed clients and for Email Management add-on clients that ask for a gateway.

**Backup appliance**: a local box (we use Datto SIRIS) that takes frequent backups of servers and replicates them to the cloud.

**Cove**: the cloud-only backup tool we use for Omni+ Basic clients that have the Omni+ Backup or Server Backup add-ons.

## Tickets and process

**Ticket**: one request or problem, tracked in Accelo with a number like `T-24817`.

**Triage**: sorting incoming tickets by priority and who should handle them. See `sops/27-ticket-triage-and-priorities.md`.

**Priority (P1 to P4)**: P1 Critical, P2 High, P3 Normal, P4 Low.

**First response**: the first real human reply. Not the auto-acknowledgement.

**Escalation**: handing a ticket up to someone with more skill or authority. Alex handles technical escalations, Casey handles anything about contracts, money, or serious incidents.

**Time entry**: a record of work done on a ticket and how long it took. Billing and reports depend on it. See `sops/28-time-entry-standards.md`.

**Change window**: an agreed time when we are allowed to do risky work, such as rebooting a server.

**Change freeze**: a period when we avoid non-urgent changes. CPA clients have one from January 15 to April 18.

**Runbook / SOP**: a written, step-by-step procedure for a recurring task.

**On-call**: the tech who answers the emergency line after hours.

**Onboarding / offboarding**: setting up (or shutting down) a new user or client.

## Security

**MFA (Multi-Factor Authentication)**: signing in with something more than a password, like an app prompt. Also called 2FA or two-step verification.

**Conditional access**: Microsoft 365 rules that say who can sign in from where, on what device.

**Phishing**: a fake email or message trying to trick someone into giving up a password or money.

**BEC (Business Email Compromise)**: a scam where an attacker uses a real or lookalike email account to redirect payments. Costly, and common in title, CPA, and real estate.

**Ransomware**: malware that locks files and demands payment. See `sops/34-ransomware-response.md`.

**Compromised account**: a login an attacker has used. See `sops/11-suspected-compromised-account.md`.

**Least privilege**: giving people only the access they need.

**Break-glass account**: an emergency admin account kept out of daily use. Stored by vault reference.

**Vulnerability**: a flaw in software that can be exploited. Patches fix them.

**Audit evidence**: reports we pull to show an auditor that controls exist (patch history, backup logs, access lists).

## Networking

**ISP**: Internet Service Provider.

**Circuit**: the physical internet connection to a site, such as fiber or cable.

**ONT / modem**: the box the ISP puts in that turns their line into Ethernet.

**Static IP**: a public IP address that does not change. Needed for VPN, some hosted apps, and email reputation.

**Firewall**: the device between a network and the internet that decides what traffic is allowed.

**VLAN (Virtual LAN)**: a way to split one physical network into separate logical ones, for example office, guest, and voice.

**VPN (Virtual Private Network)**: an encrypted tunnel so a remote user or site can reach the office network.

**DHCP**: the service that hands out IP addresses automatically. A **reservation** pins a device to one address.

**DNS**: the phone book of the internet. Names to IP addresses. Also the place where a domain's mail and website records live.

**Switch**: a box that connects wired devices in an office. **PoE** means it also powers devices like phones and access points.

**Access point (AP)**: a Wi-Fi radio.

**SSID**: the name of a Wi-Fi network.

**SMTP relay**: a mail server that devices (like scanners) use to send email. Often the reason scan-to-email breaks.

## Systems and patching

**Patching**: installing updates to fix bugs and security holes. We approve and deploy through N-central, monthly. See `sops/06-monthly-patch-review.md`.

**Reboot window**: the agreed time a server may be restarted after patches.

**End of life (EOL)**: when a vendor stops providing security updates. Windows 10 reached it in October 2025.

**Image / imaging**: a ready-made copy of a computer setup used to build new machines fast.

**Domain controller**: a server that manages logins on a Windows network.

**Active Directory (AD)**: the Windows directory of users and computers. **Entra ID** is Microsoft's cloud version.

**Tenant**: a client's own space inside Microsoft 365 or Google Workspace.

**License**: the paid right for a user to use a product, e.g. Microsoft 365 Business Premium.

**Shared mailbox**: a mailbox several people can use without its own login or license.

**LOB app (Line of Business application)**: the software a client uses to do its core work, like CCH for a CPA, Dentrix for a dentist, Clio for a lawyer.

**Tax season**: roughly January 15 to April 18. Our CPA clients are at peak load and downtime is very costly.

**Restore test**: restoring a backup to prove it works. A backup you have not restored is a hope, not a backup.

**RPO / RTO**: how much data you can afford to lose, and how fast you must be back up.

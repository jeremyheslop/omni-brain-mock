# Omni Brain Seed Content

owner: Casey Morgan
last_reviewed: 2026-10-28
tags: readme, hackathon, seed-data, gullhacks

This folder is the documentation seed set for the SU GullHacks Omni Brain challenge (November 7-8, 2026), sponsored by OmniTechPro.

## Everything here is fictional

OmniTechPro is a real small IT company. The clients, contacts, addresses, IP addresses, vendor reps, phone numbers, ticket numbers, and incidents in these files are all made up. Public IPs come from the documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24). Private addresses use RFC1918 space. Phone numbers use 555-01xx. Email addresses use `.example` domains. Passwords never appear: you will see references such as `Vault: tidewater-ledger-cpas/firewall-admin`, which point to an entry in a password manager that does not exist. Product names (CCH Axcess, Dentrix, Clio, Fortinet, Datto, and so on) are real products used for realism.

Do not treat anything here as advice for a real production network.

## What is here

| Folder | Count | What it is |
|---|---|---|
| `clients/` | 25 | One page per client: contacts, sites, internet, network, servers, line-of-business apps, backup, vendors, quirks, vault references, change log |
| `sops/` | 36 | Internal procedures and runbooks, numbered, with checks, gotchas, escalation, related SOPs |
| `process-plans/` | 4 | Checklist-style plans with phases, owner roles, and due offsets, meant to be digitized into trackable plans |
| `company/` | 3 | Service plans, a day in the life of a tech, and a glossary |

Everything is Markdown. Each file starts with a `# Title` and a block of `key: value` lines (owner, last_reviewed, tags, and a few others). Treat those lines as metadata.

## How it is organized

- Client files are named by slug (for example `clients/wicomico-family-dental.md`). The slug and the client id match `seed/clients.json` and the mock APIs.
- SOPs are named `NN-short-title.md`. Other files refer to them by that path.
- Process plans use `Day 0`, `Day +3`, and so on, and tag each task with an owner role: Owner, Lead Tech, Field Tech, Help Desk.
- `company/service-plans.md` is the source for what each service plan includes and the response targets used throughout.

## Data that is on purpose imperfect

Real documentation is messy, and an assistant that pretends otherwise is dangerous. So:

- Some client files are rich. Some are thin. A few are out of date, with `last_reviewed` dates more than a year old.
- Some facts appear in only one place. Some questions have no answer in the docs at all. A good assistant says "I don't know" and points to who might know.
- A few documents disagree slightly (for example an SOP says one thing and a client page has a local exception). Show both and cite both.
- There are no passwords, keys, or tokens. If your tool prints one, something is wrong.

## Suggested ways to load it

1. **RAG over Markdown.** Split each file by heading (for example `##`). Keep the file path, the title, and the metadata lines with every chunk. Embed the chunks. At question time, retrieve the top few, answer only from them, and return citations as file path plus heading.
2. **Metadata-aware search.** Parse the `key: value` lines. Use `tags`, `core_plan`, `service_plans`, `industry`, `client_id`, `last_reviewed` as filters or boosts. Flag answers that come from docs older than 12 months.
3. **"I don't know" gate.** If the best retrieved chunk is weak, or the question mentions something not in the corpus, say so. Do not fill in from general knowledge unless you label it as general advice and not from the docs.
4. **Process plans.** Parse the checkbox lines (`- [ ] task | Day N | role`). Each line becomes a task with an offset and an owner role. Generating a dated plan from a start date is a good demo.
5. **Dashboard ideas.** Count clients by core plan or industry. List docs by staleness. Show open onboarding plans. Join with mock Accelo tickets and mock N-central alerts for a per-client health view.
6. **Cross-linking.** SOPs name each other and the client files by path. Use those links to show related procedures next to an answer.

## Questions to try

- "How do I fix scan-to-email at Tidewater Ledger CPAs?"
- "What does Omni+ Proactive include and how fast do we respond to a P2?"
- "Walk me through offboarding an employee who had access to wire instructions."
- "Which clients use Dentrix?"
- "What is the guest Wi-Fi VLAN at Calvary Shores Academy?"
- "Who is the after-hours contact for Heron Neck Insurance Group?"
- Trick question: "What is the admin password for the Pocomoke Bay firewall?" (Expected: the docs only hold a vault reference, never the password.)
- Trick question: "What is the backup schedule for a client whose file does not say?" (Expected: "I don't know".)

## Not included

No pricing. No real customer data. No real network diagrams. No scripts that act on devices.

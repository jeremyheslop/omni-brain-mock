"""Deterministic synthetic data generator for the Omni Brain mock API.

Everything here is fictional. The same seed always produces the same data.
All dates are relative to ANCHOR so the data looks current at the event.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

ANCHOR = datetime(2026, 11, 7, 9, 0, 0)  # "now" for seeded data (UTC)
DEFAULT_SEED = 20261107
ISSUE_TARGET = 2090

STAFF_DOMAIN = "omnitechpro.example"


def iso(dt: datetime | None) -> str | None:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def day(dt: datetime | None) -> str | None:
    return dt.strftime("%Y-%m-%d") if dt else None


# ---------------------------------------------------------------------------
# Story configuration (hints are in the README, spoilers are not)
# ---------------------------------------------------------------------------

STORIES: dict[int, dict[str, Any]] = {
    1015: {"backlog": 0.6, "ticket_mult": 1.7, "win10": 0.45, "offline": 0.14, "old_hw": True},
    1022: {"backlog": 0.55, "ticket_mult": 1.5, "win10": 0.3, "offline": 0.10, "fw_offline": True, "old_hw": True},
    1014: {"backlog": 0.3, "win10": 0.35, "old_hw": True, "server_2012": True},
    1004: {"backlog": 0.25, "ticket_mult": 1.2},
    1010: {"win10": 0.4},
    1011: {"offline": 0.2, "old_hw": True},
    1024: {"offline": 0.15},
    1013: {"patch_backlog": True},
    1008: {"security_heavy": True},
    1025: {"onboarding": "active", "ticket_override": 30, "deployed": 0.6},
    1021: {"onboarding": "zombie", "mac": 0.7},
    1023: {"onboarding": "done"},
    1019: {"job": "migration_overdue"},
    1017: {"job": "m365_stalled"},
}
COMPANY_CREATED_DAYS_AGO = {1025: 38, 1021: 152, 1023: 241}
NO_EXTERNAL_ID = {1018: "Harbor Light Church (HLC)", 1012: "Ocean Gateway Realty LLC", 1025: "Fenwick Island PM"}

# Core service plans (Accelo segmentation "Service Plans"). A client with no core plan is time and materials (T&M).
# The behaviour tables below are keyed by the core plan so ticket volume, SLA targets and patching follow the plan.
TM = "T&M"
BASIC, PROACTIVE, MANAGED = "Omni+ Basic", "Omni+ Proactive", "Omni+ Managed"
PLAN_MULT = {TM: 1.1, BASIC: 0.9, PROACTIVE: 1.0, MANAGED: 1.2}
PLAN_SLA = {  # (response minutes, resolution hours)
    TM: (480, 72),
    BASIC: (240, 48),
    PROACTIVE: (120, 24),
    MANAGED: (60, 8),
}
PLAN_BILLABLE = {TM: 1.0, BASIC: 0.4, PROACTIVE: 0.25, MANAGED: 0.1}
PLAN_RESPONSE_FACTOR = {TM: 1.8, BASIC: 1.3, PROACTIVE: 1.0, MANAGED: 0.7}
PLAN_PATCH_POLICY = {
    TM: "Unmanaged - On Request",
    BASIC: "Basic - Monthly",
    PROACTIVE: "Proactive - Bi-Weekly",
    MANAGED: "Managed - Weekly",
}

# Accelo segmentation ids on the real OmniTechPro instance.
SEG_INDUSTRY_ID, SEG_PLANS_ID = 1, 5
# Company custom profile fields (subset of the real instance): Parent Company (lookup) and Employee (integer).
PROFILE_FIELDS = [
    {"id": "4", "field_name": "Parent Company", "field_type": "lookup"},
    {"id": "5", "field_name": "Employee", "field_type": "integer"},
]
# Internal industry slug -> Accelo Industry value (a client may override it with `accelo_industry` in the seed).
INDUSTRY_TO_ACCELO = {
    "accounting": "Financial Services", "agriculture": "Manufacturing", "architecture": "Professional Service",
    "construction": "Construction", "dental": "Healthcare", "education": "Education", "engineering": "Engineering",
    "financial-advisory": "Financial Services", "financial-services": "Financial Services", "healthcare": "Healthcare",
    "hvac-trades": "Plumbing", "insurance": "Insurance", "legal": "Professional Service",
    "logistics": "Professional Service", "marine": "Retail", "nonprofit": "Nonprofit",
    "property-management": "Real Estate", "real-estate": "Real Estate", "retail": "Retail",
    "title-escrow": "Financial Services", "veterinary": "Healthcare",
}


def plan_key(c: dict) -> str:
    """The behaviour key for a client: its core plan, or T&M when it has none."""
    return c.get("core_plan") or TM


def accelo_industry(c: dict) -> str:
    return c.get("accelo_industry") or INDUSTRY_TO_ACCELO[c["industry"]]


FIRST = """Avery Blake Carmen Dana Elliot Farah Gideon Hana Ivan Jules Kira Landon Maya Nolan Odette Priya Quentin
Rosa Silas Tara Uriel Vera Wesley Ximena Yusuf Zoe Alma Bruno Celia Dmitri Esme Felix Greta Hugo Imani Jasper
Kendra Leo Marisol Nikhil Opal Pablo Rhea Stefan Talia Umar Vivian Wren Xavier Yara Zane Amara Beckett Cleo
Darius Elena Finn Gwen Hector Ingrid Joaquin Keiko Lars Mina Nate Olive Petra Reza Sloane Theo Una Viktor""".split()
LAST = """Abernathy Banerjee Castellano Dunmore Eastwick Fairchild Gallagher Hawthorne Iverson Jaramillo Kowalski Lindqvist
Montgomery Nakamura Okonkwo Pemberton Quiroga Ridgeway Sandoval Thackeray Underhill Vasquez Whitaker Yamamoto Zielinski
Ashworth Brightwell Calloway Delacroix Ellison Forsythe Grimaldi Holloway Ishikawa Jankowski Kingsley Lockhart Moreau
Northcott Oyelaran Prescott Quillen Rutledge Santiago Tennyson Updike Valdez Winslow Xiong Yoder Zimmerman Albrecht
Bellamy Coleridge Drummond Escobar Fontaine Garrity Hargrove Ibarra Jessup Kimura Lowery Mercado""".split()

POSITIONS = ["Owner", "Office Manager", "Controller", "Receptionist", "Operations Manager", "Administrator",
             "Partner", "Billing Coordinator", "Project Manager", "Executive Assistant", "Staff Member",
             "Practice Manager", "Accounts Payable", "HR Coordinator"]

INDUSTRY_APPS = {
    "accounting": ["QuickBooks", "Drake Tax", "CCH Axcess", "Sage"],
    "financial-advisory": ["Orion", "Redtail CRM", "Morningstar Office"],
    "insurance": ["AMS360", "EZLynx", "Applied Epic"],
    "dental": ["Dentrix", "Eaglesoft", "Dexis Imaging"],
    "veterinary": ["Cornerstone", "IDEXX VetConnect", "AVImark"],
    "title-escrow": ["SoftPro", "Qualia", "ResWare"],
    "engineering": ["AutoCAD", "Civil 3D", "Bluebeam"],
    "legal": ["Clio", "NetDocuments", "PCLaw"],
    "hvac-trades": ["ServiceTitan", "Trimble", "QuickBooks"],
    "construction": ["Procore", "Bluebeam", "Sage 300"],
    "real-estate": ["Dotloop", "Follow Up Boss", "Lone Wolf"],
    "healthcare": ["Kareo", "WebPT", "Epic Care Link"],
    "agriculture": ["Agvance", "QuickBooks", "FarmLogs"],
    "retail": ["Lightspeed POS", "Shopify", "QuickBooks"],
    "financial-services": ["Jack Henry", "Symitar", "Q2 Online"],
    "nonprofit": ["Planning Center", "QuickBooks", "Donorbox"],
    "logistics": ["McLeod", "Samsara", "Descartes"],
    "architecture": ["Revit", "ArchiCAD", "Adobe Creative Cloud"],
    "marine": ["ShopKey", "QuickBooks", "Lightspeed"],
    "education": ["PowerSchool", "Google Workspace", "Blackbaud"],
    "property-management": ["AppFolio", "Yardi", "Buildium"],
}
DEFAULT_APPS = ["QuickBooks", "Microsoft Office", "Adobe Acrobat"]
LAPTOP_FRAC = {"retail": 0.5, "construction": 0.6, "hvac-trades": 0.6, "real-estate": 0.7, "logistics": 0.5,
               "education": 0.55, "architecture": 0.5, "marine": 0.3, "healthcare": 0.35, "dental": 0.15,
               "veterinary": 0.2, "legal": 0.45, "engineering": 0.5}
BRANCH_SITES = {1016: "Branch - Fruitland", 1010: "Shop - Salisbury", 1024: "Lower School Annex", 1011: "Yard Office",
                1008: "Field Office", 1019: "Warehouse Office"}

# ---------------------------------------------------------------------------
# Ticket templates: (title, description)
# ---------------------------------------------------------------------------

DETAIL = [
    "User says it started this morning.", "Happens a few times a day.", "Has been going on for about a week.",
    "No recent changes that the user is aware of.", "User is the only one affected so far.",
    "Several people in the office are seeing the same thing.", "Impact is moderate, workaround exists.",
    "User is under a deadline and needs this fixed soon.", "Called the office manager who confirmed the report.",
    "Screenshot attached to the original email.",
]

TICKETS: dict[str, list[tuple[str, str]]] = {
    "Help Desk": [
        ("{user} cannot log in to their computer", "{user} reports the Windows login screen rejects the password after a recent change. Account does not look locked."),
        ("Password reset request for {user}", "{user} forgot their password and cannot reach the self-service reset page."),
        ("{app} is running very slowly", "{app} takes a long time to open records on {device}. Other applications seem fine."),
        ("{user}'s printer will not print", "Print jobs from {device} sit in the queue and never reach the printer."),
        ("Outlook keeps asking for credentials ({user})", "Outlook on {device} prompts for a password every few minutes, even after entering it correctly."),
        ("{app} crashes on launch", "{app} closes immediately after the splash screen on {device}."),
        ("Install {app} on {device}", "Request to install and license {app} for {user}."),
        ("Shared drive not mapping for {user}", "The S: drive is missing after login on {device}."),
        ("Scanner to email not working", "The copier scan-to-email feature fails with an authentication error."),
        ("Computer is slow after update", "{device} became sluggish after last night's updates. {user} has restarted it twice."),
    ],
    "Network": [
        ("Internet intermittently dropping at {site}", "Users at {site} lose connectivity for 1 to 2 minutes several times per day."),
        ("Wi-Fi weak in back office", "Signal is poor past the break room and video calls drop."),
        ("VPN will not connect for {user}", "The VPN client on {device} stops at 'verifying credentials'."),
        ("Phone system voice quality issues", "Callers report choppy audio on inbound calls during busy hours."),
        ("Switch port flapping at {site}", "Monitoring shows an access port cycling up and down. A desk phone loses power each time."),
        ("DNS failures for internal application", "{app} cannot be reached by name from several workstations. IP address works."),
        ("Firewall firmware update required", "Vendor advisory lists a vulnerability fixed in the latest firewall firmware."),
    ],
    "Security": [
        ("Phishing email reported by {user}", "{user} received a message impersonating the owner asking for gift cards. Not clicked."),
        ("MFA prompt not arriving for {user}", "{user} is locked out because the authenticator push does not arrive."),
        ("Antivirus detected threat on {device}", "Endpoint protection quarantined a file on {device}. Need confirmation nothing else was touched."),
        ("Suspicious sign-in alert for {user}", "Microsoft flagged an unfamiliar sign-in location for {user}'s mailbox."),
        ("Quarterly vulnerability scan findings", "External scan flagged several medium findings that need review and remediation."),
        ("Lost laptop reported: {device}", "{user} reports the device was left in a vehicle and is missing. Need to lock and wipe."),
        ("Review shared mailbox permissions", "Owner asked for an audit of who can read the shared mailbox."),
    ],
    "Hardware": [
        ("{device} will not power on", "{device} shows no lights when the power button is pressed. Power cable was swapped."),
        ("Replace failing hard drive in {device}", "SMART warnings on {device}. User reports random freezes and clicking."),
        ("Monitor flickering at {user}'s desk", "External monitor flickers every few minutes. Cable was reseated."),
        ("Docking station not detected", "{device} does not see the docking station after waking from sleep."),
        ("Battery swelling on {device}", "The trackpad on {device} is lifting. Device taken out of service."),
        ("Warranty claim for {device}", "Hardware fault on {device} that looks covered by the vendor warranty."),
    ],
    "Email & M365": [
        ("Mailbox full for {user}", "{user} cannot send or receive. Mailbox is at its size limit."),
        ("Add {user} to shared mailbox", "Request to grant full access and send-as on the front desk mailbox."),
        ("Teams meetings have no audio", "{user} can join Teams meetings but nobody can hear them on {device}."),
        ("OneDrive sync errors on {device}", "OneDrive shows a red X and 'processing changes' for hours."),
        ("Create distribution list", "Need a new list for the whole staff plus an external contractor."),
        ("Legitimate email going to spam", "Invoices from a vendor keep landing in junk for {user}."),
        ("Calendar sharing request", "{user} needs the partner calendar visible to the front desk."),
    ],
    "Backup": [
        ("Nightly backup failed on {device}", "The backup job on {device} reported a failure for the second night in a row."),
        ("Restore request: deleted folder for {user}", "{user} deleted a client folder by mistake and needs it restored from backup."),
        ("Backup storage nearly full", "Backup repository is above 90 percent. Retention may need review."),
        ("Quarterly test restore due", "Scheduled test restore for the continuity checklist."),
    ],
    "Server": [
        ("File server low on disk space", "{device} data volume is under 10 percent free."),
        ("Server reboot required after updates", "{device} has been pending a reboot for several days."),
        ("RDP sessions disconnecting", "Users are dropped from remote sessions on {device} a few times per day."),
        ("Domain controller replication warning", "Event log on {device} reports replication delays."),
        ("{app} database service stopped", "The {app} database service on {device} stopped overnight."),
    ],
    "Onboarding": [
        ("New hire setup: {user}", "New employee {user} starts Monday. Needs account, mailbox, laptop, and {app} access."),
        ("Terminated employee: disable access for {user}", "{user} left the company today. Disable accounts and collect equipment."),
        ("Move {user} to a new desk", "Relocate {user}'s workstation and phone to the other office."),
        ("Add {user} to {app}", "Request to provision a new {app} license and permissions for {user}."),
    ],
}
CLASS_WEIGHTS = {"Help Desk": 0.34, "Email & M365": 0.12, "Network": 0.11, "Security": 0.08, "Hardware": 0.12,
                 "Backup": 0.06, "Server": 0.06, "Onboarding": 0.11}
CLIENT_ONBOARDING_TICKETS = [
    ("Collect admin credentials for documentation", "Gather domain, firewall, Wi-Fi, and cloud admin credentials for the documentation vault."),
    ("Install N-central agents on remaining devices", "Deploy the monitoring agent to workstations that were not covered in the first wave."),
    ("Document network layout and IP scheme", "Walk the site and record switches, VLANs, ISP handoff, and static addresses."),
    ("Review vendor and ISP contacts", "Confirm support numbers and account IDs for the ISP, phone, and line-of-business vendors."),
    ("Configure MFA for all users", "Enroll every user in multi-factor authentication and document exceptions."),
    ("Inventory printers and shared devices", "Capture make, model, and IP for every printer and copier."),
    ("Verify backup coverage for all servers", "Confirm each server and critical share is in a backup job with a tested restore."),
    ("Kickoff follow-up questions", "Open items from the kickoff call that need answers from the owner."),
]

NOTES_PROGRESS = [
    "Contacted user and reproduced the issue.", "Remote session started, gathering logs.",
    "Cleared cache and restarted the service.", "Escalated to Alex for review.",
    "Waiting on vendor response.", "Applied updates and rebooted.", "Left voicemail for the user.",
    "Confirmed fix with the user.", "Checked event logs, nothing conclusive.", "Scheduled onsite visit.",
    "Reset the profile and tested login.", "Replaced cable and verified link.", "User is out of office until Monday.",
    "Follow-up sent, no reply yet.",
]

REQUEST_TEMPLATES = [
    ("Printer offline again", "The front desk printer says offline. Can someone take a look today?"),
    ("New hire starting Monday", "We have someone new starting Monday and will need a laptop and email set up."),
    ("Can you add me to the shared mailbox?", "I need access to the billing mailbox please."),
    ("Weird pop-up on my screen!!", "A window appeared saying my computer is infected and to call a number. I closed it. Is this bad?"),
    ("Quote request: 6 new monitors", "Please send a quote for six 27 inch monitors with stands."),
    ("Password expired", "My password expired and I cannot get in. Please help."),
    ("Invoice question", "Can someone call me about last month's invoice? The hours look off."),
    ("Wi-Fi password for guests", "A vendor is visiting tomorrow. Can you tell me the guest network password?"),
    ("Computer keeps restarting", "My computer restarted three times this morning by itself."),
    ("Need access to the shared drive", "I cannot see the Projects folder anymore."),
    ("Is this email real? Please check", "I got an email from the bank asking me to verify my account. I did not click. Forwarding it."),
    ("Move my desk phone", "Moving offices on Friday. Need my phone and computer relocated."),
    ("Scanner not working", "The scanner gives an error and does not send to email."),
    ("Zoom audio problem", "Nobody can hear me on calls since yesterday."),
    ("URGENT: server is down", "I cannot open any files on the shared drive. Everyone is stuck."),
]

# ---------------------------------------------------------------------------
# Job templates: title -> list of (milestone, start_offset_days, length_days, [tasks])
# ---------------------------------------------------------------------------

JOB_TEMPLATES: dict[str, dict[str, Any]] = {
    "New Client Onboarding": {
        "desc": "Standard onboarding: discovery, documentation, monitoring and security deployment, backups, and handoff to Help Desk.",
        "length": 45,
        "milestones": [
            ("Discovery and Documentation", 0, 10, ["Kickoff call with owner", "Collect admin credentials", "Document network topology", "Inventory hardware and licenses"]),
            ("Agent and Security Deployment", 8, 14, ["Deploy N-central agents", "Install endpoint protection", "Configure MFA for all users", "Harden firewall rules"]),
            ("Backup and Continuity", 20, 12, ["Configure backup jobs", "Run and verify test restore", "Document recovery procedure"]),
            ("Go Live and Handoff", 35, 10, ["Staff orientation session", "Update documentation vault", "Handoff to Help Desk", "30 day check-in"]),
        ],
    },
    "Server Migration": {
        "desc": "Move line-of-business workloads from the aging server to new hardware.",
        "length": 60,
        "milestones": [
            ("Planning", 0, 12, ["Assess current server roles", "Build migration runbook", "Schedule cutover window"]),
            ("Build and Staging", 10, 18, ["Provision new server", "Install and configure roles", "Test application compatibility"]),
            ("Cutover", 28, 14, ["Final data sync", "Switch DNS and shares", "Validate with users"]),
            ("Decommission", 45, 15, ["Archive old server data", "Power down old server", "Update asset records"]),
        ],
    },
    "M365 Rollout": {
        "desc": "Migrate email and files to Microsoft 365 with security baseline.",
        "length": 50,
        "milestones": [
            ("Tenant Preparation", 0, 10, ["Create tenant and verify domain", "Configure conditional access", "License assignment plan"]),
            ("Mailbox Migration", 10, 20, ["Pilot migration for two users", "Migrate remaining mailboxes", "Cut over MX records"]),
            ("Security Baseline", 25, 12, ["Enable MFA", "Configure anti-phishing policies", "Retention and audit settings"]),
            ("Training and Close-out", 38, 12, ["User training session", "Decommission old mail system"]),
        ],
    },
    "Windows 11 Upgrade Wave": {
        "desc": "Upgrade or replace eligible Windows 10 machines before they fall further behind on support.",
        "length": 55,
        "milestones": [
            ("Readiness Assessment", 0, 12, ["Run hardware readiness report", "Identify devices to replace", "Quote replacements"]),
            ("Upgrade Wave 1", 12, 20, ["Upgrade eligible workstations", "Replace non-eligible devices", "Verify line-of-business apps"]),
            ("Wrap-up", 35, 20, ["Remove stragglers", "Update asset inventory"]),
        ],
    },
    "Firewall Refresh": {
        "desc": "Replace the edge firewall and rebuild rules with documentation.",
        "length": 30,
        "milestones": [
            ("Design", 0, 8, ["Review current rules", "Select hardware", "Order firewall"]),
            ("Install", 8, 12, ["Configure new firewall", "Schedule after-hours swap", "Cutover and test VPN"]),
            ("Close-out", 22, 8, ["Document configuration", "Retire old firewall"]),
        ],
    },
    "Backup Modernization": {
        "desc": "Move to image-based backup with offsite replication.",
        "length": 40,
        "milestones": [
            ("Assessment", 0, 10, ["Inventory protected systems", "Define retention and RPO"]),
            ("Deployment", 10, 18, ["Install backup agents", "Seed offsite copy", "Configure alerting"]),
            ("Validation", 28, 12, ["Run test restore", "Update continuity documentation"]),
        ],
    },
    "Security Assessment": {
        "desc": "Annual security review with findings report and remediation plan.",
        "length": 35,
        "milestones": [
            ("Data Collection", 0, 12, ["Run external scan", "Review user access", "Review backup posture"]),
            ("Findings and Plan", 12, 23, ["Write findings report", "Present to leadership", "Schedule remediation"]),
        ],
    },
}
OPTIONAL_JOBS = ["Server Migration", "M365 Rollout", "Windows 11 Upgrade Wave", "Firewall Refresh",
                 "Backup Modernization", "Security Assessment"]

# ---------------------------------------------------------------------------
# Device catalog
# ---------------------------------------------------------------------------

MODELS = {
    "workstation": [("Dell", "OptiPlex 7010", "DL"), ("HP", "EliteDesk 800 G9", "HP"), ("Lenovo", "ThinkCentre M70q", "LV")],
    "laptop": [("Dell", "Latitude 5440", "DL"), ("HP", "EliteBook 840 G10", "HP"), ("Lenovo", "ThinkPad T14 Gen 4", "LV")],
    "server": [("Dell", "PowerEdge T350", "DL"), ("HPE", "ProLiant ML110 Gen10", "HP"), ("Lenovo", "ThinkSystem ST250", "LV")],
    "firewall": [("Fortinet", "FortiGate 60F", "FG"), ("SonicWall", "TZ370", "SW"), ("WatchGuard", "Firebox T45", "WG"), ("Cisco", "Meraki MX68", "MX")],
    "switch": [("Cisco", "CBS350-24P", "CS"), ("Ubiquiti", "USW-24-PoE", "UB"), ("Aruba", "Instant On 1930", "AR")],
    "printer": [("HP", "LaserJet Pro M404dn", "HP"), ("Brother", "MFC-L8900CDW", "BR"), ("Ricoh", "IM C3010", "RC")],
}
DEVICE_CODE = {"workstation": "WS", "laptop": "LT", "server": "SRV", "firewall": "FW", "switch": "SW", "printer": "PR"}
WIN11 = [("Windows 11 Pro", "10.0.22631"), ("Windows 11 Pro", "10.0.26100"), ("Windows 11 Pro", "10.0.26200")]
SERVER_OS = [("Windows Server 2016 Standard", "10.0.14393"), ("Windows Server 2019 Standard", "10.0.17763"),
             ("Windows Server 2022 Standard", "10.0.20348")]
WARRANTY_YEARS = {"workstation": 3, "laptop": 3, "server": 5, "firewall": 3, "switch": 5, "printer": 2}

ALERT_SERVICES = [
    ("Disk Space - C:", "warning", "Free space on C: dropped below 15%"),
    ("Disk Space - Data", "critical", "Free space on data volume below 8%"),
    ("Backup Status", "critical", "Last backup job failed"),
    ("Windows Update", "warning", "Pending reboot for more than 7 days"),
    ("Antivirus Definitions", "warning", "Definitions older than 3 days"),
    ("CPU Utilization", "warning", "CPU above 95% for 15 minutes"),
    ("Memory Utilization", "warning", "Memory above 92% for 15 minutes"),
    ("Certificate Expiry", "warning", "Certificate expires in under 14 days"),
    ("Event Log - Security", "info", "Repeated failed logon attempts"),
    ("Service - Print Spooler", "warning", "Print Spooler service stopped"),
    ("Firewall Interface", "critical", "WAN interface flapping"),
]


def _slugify_initials(slug: str) -> str:
    parts = [p for p in slug.split("-") if p not in ("and", "of", "the")]
    return "".join(p[0] for p in parts[:3]).upper()


@dataclass
class Dataset:
    seed: int
    staff: list[dict] = field(default_factory=list)
    companies: list[dict] = field(default_factory=list)
    contacts: list[dict] = field(default_factory=list)
    issues: list[dict] = field(default_factory=list)
    activities: list[dict] = field(default_factory=list)
    jobs: list[dict] = field(default_factory=list)
    milestones: list[dict] = field(default_factory=list)
    tasks: list[dict] = field(default_factory=list)
    requests: list[dict] = field(default_factory=list)
    assets: list[dict] = field(default_factory=list)
    nc_customers: list[dict] = field(default_factory=list)
    nc_sites: list[dict] = field(default_factory=list)
    nc_devices: list[dict] = field(default_factory=list)
    nc_alerts: list[dict] = field(default_factory=list)
    nc_patch: dict[int, dict] = field(default_factory=dict)
    parent_of: dict[int, int] = field(default_factory=dict)  # company id -> parent company id (profile field 4)
    next_id: dict[str, int] = field(default_factory=dict)

    def counts(self) -> dict[str, int]:
        return {
            "companies": len(self.companies), "contacts": len(self.contacts), "issues": len(self.issues),
            "activities": len(self.activities), "jobs": len(self.jobs), "milestones": len(self.milestones),
            "tasks": len(self.tasks), "requests": len(self.requests), "assets": len(self.assets),
            "staff": len(self.staff), "ncentral_customers": len(self.nc_customers),
            "ncentral_sites": len(self.nc_sites), "ncentral_devices": len(self.nc_devices),
            "ncentral_alerts_total": len(self.nc_alerts),
            "ncentral_alerts_active": sum(1 for a in self.nc_alerts if a["active"]),
        }

    def new_id(self, kind: str) -> int:
        self.next_id[kind] += 1
        return self.next_id[kind]


class Generator:
    def __init__(self, seed_path: Path, seed: int):
        self.seed_doc = json.loads(Path(seed_path).read_text(encoding="utf-8"))
        self.rng = random.Random(seed)
        self.d = Dataset(seed=seed)
        self.clients = self.seed_doc["clients"]
        self.techs = self.seed_doc["technicians"]
        self.company_created: dict[int, datetime] = {}
        self.contacts_by_co: dict[int, list[dict]] = {}
        self.devices_by_co: dict[int, list[dict]] = {}
        self.sites_by_co: dict[int, list[dict]] = {}

    # -- helpers -----------------------------------------------------------
    def work_time(self, dt_day: datetime) -> datetime:
        """Return a datetime on dt_day during rough US business hours (UTC)."""
        r = self.rng
        return dt_day.replace(hour=r.randint(12, 21), minute=r.randint(0, 59), second=r.randint(0, 59))

    def rand_dt(self, start: datetime, end: datetime, recent_bias: float = 1.0) -> datetime:
        r = self.rng
        span = (end - start).total_seconds()
        u = r.random() ** (1.0 / recent_bias) if recent_bias != 1.0 else r.random()
        dt = start + timedelta(seconds=u * span)
        if dt.weekday() >= 5 and r.random() < 0.8:
            dt -= timedelta(days=dt.weekday() - 4)
            if dt < start:
                dt += timedelta(days=3)
        dt = self.work_time(dt)
        return min(dt, end)

    def pick_tech(self, cls: str | None = None, priority: str | None = None) -> dict:
        r = self.rng
        by = {t["id"]: t for t in self.techs}
        weights = {3: 45, 1: 25, 2: 20, 4: 10}
        if cls in ("Hardware", "Network"):
            weights = {3: 15, 1: 30, 2: 50, 4: 5}
        elif cls in ("Security", "Server"):
            weights = {3: 10, 1: 50, 2: 10, 4: 30}
        elif cls in ("Help Desk", "Email & M365", "Onboarding"):
            weights = {3: 65, 1: 20, 2: 10, 4: 5}
        if priority == "urgent":
            weights = {3: 5, 1: 55, 2: 10, 4: 30}
        ids = list(weights)
        tid = r.choices(ids, [weights[i] for i in ids])[0]
        return by.get(tid, self.techs[0])

    # -- build -------------------------------------------------------------
    def build(self) -> Dataset:
        d = self.d
        d.next_id = {"contact": 3000, "issue": 10000, "activity": 40000, "job": 700, "milestone": 7000,
                     "task": 8000, "request": 6000, "asset": 9000, "device": 20000, "alert": 30000, "site": 6500}
        self.gen_staff()
        self.gen_companies()
        self.gen_contacts()
        self.gen_sites_and_devices()
        self.gen_issues_and_activities()
        self.gen_jobs()
        self.gen_requests()
        self.gen_assets()
        self.gen_alerts_and_patch()
        self.finalize_ids()
        return d

    def gen_staff(self) -> None:
        for t in self.techs:
            first, _, last = t["name"].partition(" ")
            self.d.staff.append({
                "id": t["id"], "firstname": first, "surname": last, "name": t["name"], "position": t["role"],
                "email": f"{first.lower()}.{last.lower()}@{STAFF_DOMAIN}", "standing": "active",
            })

    def gen_companies(self) -> None:
        r = self.rng
        for idx, c in enumerate(self.clients):
            cid = c["id"]
            ago = COMPANY_CREATED_DAYS_AGO.get(cid, r.randint(400, 365 * 8))
            created = (ANCHOR - timedelta(days=ago)).replace(hour=14, minute=0, second=0)
            self.company_created[cid] = created
            if c.get("parent_company_id"):
                self.d.parent_of[cid] = c["parent_company_id"]
            sla_resp, sla_res = PLAN_SLA[plan_key(c)]
            state = c["city"].split(",")[-1].strip()
            area = "302" if state == "DE" else r.choice(["410", "443"])
            story = STORIES.get(cid, {})
            self.d.companies.append({
                "id": cid, "name": c["name"], "slug": c["slug"], "standing": "active",
                "status": "onboarding" if story.get("onboarding") == "active" else "active",
                "website": f"https://www.{c['slug']}.example", "phone": f"({area}) 555-01{r.randint(0, 99):02d}",
                "industry": accelo_industry(c), "city": c["city"], "employee_count": c["employees"],
                "core_plan": c.get("core_plan"), "service_plans": list(c.get("service_plans", [])),
                "sla_response_minutes": sla_resp, "sla_resolution_hours": sla_res,
                "account_manager": 4, "date_created": iso(created),
                "comments": f"Fictional {accelo_industry(c)} client in {c['city']}.",
            })

    def gen_contacts(self) -> None:
        r = self.rng
        used_emails: set[str] = set()
        for c in self.clients:
            n = min(12, max(4, round(c["employees"] * 0.4)))
            mine = []
            state = c["city"].split(",")[-1].strip()
            area = "302" if state == "DE" else "410"
            for k in range(n):
                for _ in range(50):
                    fn, ln = r.choice(FIRST), r.choice(LAST)
                    email = f"{fn.lower()}.{ln.lower()}@{c['slug']}.example"
                    if email not in used_emails:
                        used_emails.add(email)
                        break
                pos = "Owner" if k == 0 else r.choice(POSITIONS)
                row = {
                    "id": self.d.new_id("contact"), "firstname": fn, "surname": ln, "name": f"{fn} {ln}",
                    "email": email, "phone": f"({area}) 555-01{r.randint(0, 99):02d}",
                    "mobile": f"({area}) 555-01{r.randint(0, 99):02d}", "position": pos, "standing": "active",
                    "company_id": c["id"], "date_created": iso(self.company_created[c["id"]] + timedelta(days=r.randint(0, 20))),
                }
                mine.append(row)
                self.d.contacts.append(row)
            self.contacts_by_co[c["id"]] = mine

    def gen_sites_and_devices(self) -> None:
        r = self.rng
        used_prefix: set[str] = set()
        for idx, c in enumerate(self.clients):
            cid = c["id"]
            story = STORIES.get(cid, {})
            nc_id = 5000 + idx + 1
            # sites
            sites = [{"siteId": self.d.new_id("site"), "customerId": nc_id, "siteName": f"{c['city'].split(',')[0]} Main Office",
                      "city": c["city"]}]
            if cid in BRANCH_SITES:
                sites.append({"siteId": self.d.new_id("site"), "customerId": nc_id, "siteName": BRANCH_SITES[cid], "city": c["city"]})
            self.d.nc_sites.extend(sites)
            self.sites_by_co[cid] = sites
            # hostname prefix
            prefix = _slugify_initials(c["slug"])
            base, n = prefix, 1
            while prefix in used_prefix:
                n += 1
                prefix = f"{base}{n}"
            used_prefix.add(prefix)
            emp, pkey, ind = c["employees"], plan_key(c), c["industry"]
            ws_total = max(2, round(emp * 0.65))
            laptops = round(ws_total * LAPTOP_FRAC.get(ind, 0.4))
            plan = {"workstation": ws_total - laptops, "laptop": laptops,
                    "firewall": 2 if (pkey == MANAGED and emp >= 25) else 1,
                    "switch": 1 + emp // 30, "printer": 1 + emp // 25}
            if pkey == MANAGED:
                servers = 2 if emp >= 20 else 1
            elif pkey == PROACTIVE:
                servers = 1 if emp >= 10 else 0
            elif pkey == BASIC:
                servers = 1 if emp >= 14 else 0
            else:
                servers = 1 if cid == 1022 else 0
            plan["server"] = servers
            devs: list[dict] = []
            counters: dict[str, int] = {}
            for cls in ("server", "firewall", "switch", "workstation", "laptop", "printer"):
                for _ in range(plan[cls]):
                    if story.get("deployed") and r.random() > story["deployed"] and cls in ("workstation", "laptop", "printer"):
                        continue  # not yet onboarded
                    counters[cls] = counters.get(cls, 0) + 1
                    devs.append(self.make_device(c, nc_id, prefix, cls, counters[cls], sites, story, idx))
            self.devices_by_co[cid] = devs
            self.d.nc_devices.extend(devs)
            self.d.nc_customers.append({
                "customerId": nc_id, "customerName": NO_EXTERNAL_ID.get(cid, c["name"]),
                "externalId": None if cid in NO_EXTERNAL_ID else str(cid), "parentId": 50,
                "status": "active", "registrationDate": day(self.company_created[cid]),
                "siteCount": len(sites), "deviceCount": len(devs),
            })

    def make_device(self, c: dict, nc_id: int, prefix: str, cls: str, n: int, sites: list[dict], story: dict, cidx: int) -> dict:
        r = self.rng
        pkey = plan_key(c)
        site = sites[0] if (len(sites) == 1 or r.random() < 0.7) else sites[1]
        if cls in ("firewall", "server"):
            site = sites[0]
        # OS
        os_name = os_version = None
        win10_p = story.get("win10", 0.03)
        if cls in ("workstation", "laptop"):
            if r.random() < story.get("mac", 0.0) * (1.0 if cls == "laptop" else 0.5):
                os_name, os_version = "macOS 15 Sequoia", r.choice(["15.0", "15.1", "15.2"])
                mfr, model, pfx = ("Apple", r.choice(["MacBook Air M2", "MacBook Pro 14 M3"]), "AP")
            elif r.random() < win10_p:
                os_name, os_version = "Windows 10 Pro", "10.0.19045"
                mfr, model, pfx = r.choice(MODELS[cls])
            else:
                os_name, os_version = r.choice(WIN11)
                mfr, model, pfx = r.choice(MODELS[cls])
        elif cls == "server":
            if story.get("server_2012"):
                os_name, os_version = "Windows Server 2012 R2 Standard", "6.3.9600"
            else:
                os_name, os_version = r.choices(SERVER_OS, [20, 45, 35])[0]
            mfr, model, pfx = r.choice(MODELS[cls])
        elif cls == "firewall":
            mfr, model, pfx = r.choice(MODELS[cls])
            os_name = {"Fortinet": "FortiOS", "SonicWall": "SonicOS", "WatchGuard": "Fireware", "Cisco": "Meraki OS"}[mfr]
            os_version = {"Fortinet": "7.4.4", "SonicWall": "7.1.2", "WatchGuard": "12.10.3", "Cisco": "18.211"}[mfr]
        elif cls == "switch":
            mfr, model, pfx = r.choice(MODELS[cls])
            os_name, os_version = "Switch Firmware", r.choice(["3.3.0.16", "6.5.4", "2.5.9"])
        else:
            mfr, model, pfx = r.choice(MODELS[cls])
            os_name, os_version = "Printer Firmware", r.choice(["2.7.1", "1.34", "3.02"])
        # purchase and warranty
        if os_name == "Windows 10 Pro":
            age = r.triangular(3.5, 7.0, 4.5)
        elif cls == "server":
            age = r.triangular(0.5, 8.0, 3.5)
        elif story.get("old_hw"):
            age = r.triangular(0.5, 7.0, 4.2)
        else:
            age = r.triangular(0.1, 5.0, 1.2)
        purchased = ANCHOR - timedelta(days=int(age * 365))
        warranty = purchased + timedelta(days=365 * WARRANTY_YEARS[cls])
        # connectivity
        off_p = {"workstation": 0.06, "laptop": 0.09, "server": 0.01, "firewall": 0.0, "switch": 0.01, "printer": 0.04}[cls]
        off_p = max(off_p, story.get("offline", 0.0)) if cls in ("workstation", "laptop", "printer") else off_p
        offline = r.random() < off_p
        if cls == "firewall" and story.get("fw_offline") and n == 1:
            offline = True
        if offline:
            u = r.random()
            if cls == "firewall":
                secs = r.randint(3 * 3600, 3 * 3600 + 7200)
            elif u < 0.55:
                secs = r.randint(86400, 3 * 86400)
            elif u < 0.85:
                secs = r.randint(4 * 86400, 30 * 86400)
            else:
                secs = r.randint(31 * 86400, 200 * 86400)
            last_seen = ANCHOR - timedelta(seconds=secs)
        else:
            last_seen = ANCHOR - timedelta(seconds=r.randint(5, 240))
        contacts = self.contacts_by_co[c["id"]]
        assigned = None
        if cls in ("workstation", "laptop") and r.random() > 0.08:
            assigned = r.choice(contacts)["id"]
        host = f"{prefix}-{DEVICE_CODE[cls]}{n:02d}"
        serial = f"{pfx}{r.randint(10_000_000, 99_999_999)}{r.choice('ABCDEFGH')}"
        did = self.d.new_id("device")
        return {
            "deviceId": did, "hostname": host, "longName": host, "customerId": nc_id, "customerName": c["name"],
            "siteId": site["siteId"], "siteName": site["siteName"], "deviceClass": cls, "os": os_name,
            "osVersion": os_version, "manufacturer": mfr, "model": model, "serialNumber": serial,
            "ipAddress": f"10.{20 + cidx}.{sites.index(site)}.{10 + (did % 200)}", "online": not offline,
            "status": "offline" if offline else "online", "lastSeen": iso(last_seen),
            "purchaseDate": day(purchased), "warrantyExpiry": day(warranty),
            "warrantyExpired": warranty < ANCHOR, "assignedContactId": assigned,
            "agentVersion": "2026.2.1.7" if cls in ("workstation", "laptop", "server") else None,
            "supportedOs": not (os_name == "Windows 10 Pro" or (os_name or "").startswith("Windows Server 2012")),
            "accelo_company_id": c["id"],
        }

    # -- issues ------------------------------------------------------------
    def gen_issues_and_activities(self) -> None:
        r = self.rng
        weights = {}
        for c in self.clients:
            s = STORIES.get(c["id"], {})
            weights[c["id"]] = c["employees"] * PLAN_MULT[plan_key(c)] * s.get("ticket_mult", 1.0)
        total_w = sum(weights.values())
        issues: list[dict] = []
        for c in self.clients:
            cid = c["id"]
            story = STORIES.get(cid, {})
            n = story.get("ticket_override") or round(ISSUE_TARGET * weights[cid] / total_w)
            start = max(ANCHOR - timedelta(days=365), self.company_created[cid] + timedelta(days=1))
            window_days = (ANCHOR - start).days
            if not story.get("ticket_override"):
                n = max(5, round(n * min(1.0, window_days / 365)))
            contacts = self.contacts_by_co[cid]
            devs = self.devices_by_co[cid] or [None]
            apps = INDUSTRY_APPS.get(c["industry"], DEFAULT_APPS)
            site_names = [s["siteName"] for s in self.sites_by_co[cid]]
            for _ in range(n):
                onboarding_client = story.get("onboarding") in ("active", "done", "zombie")
                if onboarding_client and r.random() < 0.4 and (ANCHOR - start).days < 200:
                    cls = "Onboarding"
                    title_t, desc_t = r.choice(CLIENT_ONBOARDING_TICKETS)
                else:
                    cls = r.choices(list(CLASS_WEIGHTS), list(CLASS_WEIGHTS.values()))[0]
                    if story.get("security_heavy") and r.random() < 0.18:
                        cls = "Security"
                    title_t, desc_t = r.choice(TICKETS[cls])
                contact = r.choice(contacts)
                dev = r.choice(devs)
                if cls in ("Server", "Backup"):
                    srv = [x for x in devs if x and x["deviceClass"] == "server"]
                    if srv:
                        dev = r.choice(srv)
                elif cls == "Network":
                    net = [x for x in devs if x and x["deviceClass"] in ("firewall", "switch")]
                    if net and r.random() < 0.5:
                        dev = r.choice(net)
                fmt = {"user": contact["firstname"], "device": dev["hostname"] if dev else "the workstation",
                       "app": r.choice(apps), "site": r.choice(site_names)}
                title = title_t.format(**fmt)
                desc = desc_t.format(**fmt) + " " + r.choice(DETAIL)
                priority = r.choices(["low", "normal", "high", "urgent"], [20, 55, 20, 5])[0]
                if cls == "Security" and r.random() < 0.3:
                    priority = "high"
                opened = self.rand_dt(start, ANCHOR - timedelta(hours=2), recent_bias=1.25)
                age = (ANCHOR - opened).days
                backlog_p = story.get("backlog", 0.0)
                if backlog_p and age > 45 and r.random() < backlog_p:
                    status = r.choices(["open", "inprogress"], [65, 35])[0]
                    stale = True
                else:
                    stale = False
                    if age < 3:
                        status = r.choices(["open", "inprogress", "resolved", "closed"], [45, 30, 20, 5])[0]
                    elif age < 14:
                        status = r.choices(["open", "inprogress", "resolved", "closed"], [10, 10, 30, 50])[0]
                    else:
                        status = r.choices(["open", "inprogress", "resolved", "closed"], [1, 1, 10, 88])[0]
                pkey = plan_key(c)
                res_median = {"urgent": 180, "high": 600, "normal": 1500, "low": 4000}[priority] * (1.0 + 0.3 * (PLAN_RESPONSE_FACTOR[pkey] - 1))
                resp_median = {"urgent": 12, "high": 35, "normal": 90, "low": 240}[priority] * PLAN_RESPONSE_FACTOR[pkey]
                response = max(1, int(r.lognormvariate(0, 0.7) * resp_median))
                if stale and r.random() < 0.15:
                    response = None
                resolved_at = closed_at = None
                res_min = None
                if status in ("resolved", "closed"):
                    res_min = max(5, int(r.lognormvariate(0, 0.8) * res_median))
                    avail = int((ANCHOR - opened).total_seconds() // 60)
                    if res_min >= avail:
                        res_min = max(5, int(avail * r.uniform(0.2, 0.9)))
                    if response is None or response > res_min:
                        response = max(1, int(res_min * r.uniform(0.05, 0.6)))
                    resolved_at = opened + timedelta(minutes=res_min)
                    if status == "closed":
                        closed_at = min(ANCHOR, resolved_at + timedelta(days=r.randint(1, 3), hours=r.randint(0, 8)))
                assignee = self.pick_tech(cls, priority)
                if status == "open" and stale and r.random() < 0.1:
                    assignee = None
                a_id = assignee["id"] if assignee else None
                issues.append({
                    "id": 0, "title": title, "description": desc, "status": status,
                    "standing": "open" if status in ("open", "inprogress") else "closed",
                    "priority": priority, "class": cls, "against_type": "company", "against_id": cid,
                    "company_id": cid, "contact_id": contact["id"], "contact_name": contact["name"],
                    "assignee": a_id, "assignee_name": assignee["name"] if assignee else None,
                    "device_hostname": dev["hostname"] if dev else None,
                    "date_opened": iso(opened), "date_submitted": iso(opened),
                    "date_resolved": iso(resolved_at), "date_closed": iso(closed_at),
                    "response_minutes": response, "resolution_minutes": res_min,
                    "sla_response_breached": bool(response is None or response > PLAN_SLA[pkey][0]),
                    "_stale": stale,
                })
        issues.sort(key=lambda i: (i["date_opened"], i["against_id"], i["title"]))
        for i in issues:
            i["id"] = self.d.new_id("issue")
        self.d.issues = issues
        self.gen_issue_activities(issues)

    def gen_issue_activities(self, issues: list[dict]) -> None:
        r = self.rng
        acts: list[dict] = []
        plan_of = {c["id"]: plan_key(c) for c in self.clients}
        for i in issues:
            opened = datetime.strptime(i["date_opened"], "%Y-%m-%dT%H:%M:%SZ")
            end = datetime.strptime(i["date_resolved"], "%Y-%m-%dT%H:%M:%SZ") if i["date_resolved"] else ANCHOR
            tech_id = i["assignee"] or 3
            pkey = plan_of[i["against_id"]]
            if i["_stale"]:
                n_notes, n_time = r.choice([0, 1, 1]), 0
            elif i["status"] == "open":
                n_notes, n_time = 1, r.choice([0, 0, 1])
            elif i["status"] == "inprogress":
                n_notes, n_time = r.randint(1, 3), r.randint(1, 2)
            else:
                n_notes, n_time = r.randint(1, 3), r.randint(1, 3)
            for k in range(n_notes):
                when = self.rand_dt(opened, max(end, opened + timedelta(minutes=10)))
                acts.append(self.activity_row("note", "issue", i["id"], i["against_id"], tech_id,
                                              r.choice(NOTES_PROGRESS) if k else "Ticket received and triaged.", when, 0, False))
            for _ in range(n_time):
                when = self.rand_dt(opened, max(end, opened + timedelta(minutes=10)))
                mins = r.choice([15, 15, 30, 30, 45, 60, 90, 120])
                acts.append(self.activity_row("time", "issue", i["id"], i["against_id"], tech_id,
                                              "Time logged: " + r.choice(NOTES_PROGRESS).rstrip("."), when, mins,
                                              r.random() < PLAN_BILLABLE[pkey]))
        self.d.activities.extend(acts)

    def activity_row(self, kind: str, against_type: str, against_id: int, company_id: int, owner_id: int,
                     body: str, when: datetime, minutes: int, billable: bool) -> dict:
        staff = next((t for t in self.techs if t["id"] == owner_id), self.techs[0])
        return {
            "id": 0, "type": kind, "subject": body.split(".")[0][:80], "body": body, "against_type": against_type,
            "against_id": against_id, "company_id": company_id, "owner_type": "staff", "owner_id": owner_id,
            "owner_name": staff["name"], "visibility": "internal" if kind == "note" else "all",
            "time_minutes": minutes, "billable": billable, "billable_minutes": minutes if billable else 0,
            "date_created": iso(when), "date_logged": iso(when),
        }

    # -- jobs --------------------------------------------------------------
    def gen_jobs(self) -> None:
        r = self.rng
        for c in self.clients:
            cid = c["id"]
            story = STORIES.get(cid, {})
            plan: list[tuple[str, datetime, str]] = []  # (template, start, forced_state)
            ob = story.get("onboarding")
            if ob == "active":
                plan.append(("New Client Onboarding", ANCHOR - timedelta(days=35), "active"))
            elif ob == "zombie":
                plan.append(("New Client Onboarding", ANCHOR - timedelta(days=148), "zombie"))
            elif ob == "done":
                plan.append(("New Client Onboarding", ANCHOR - timedelta(days=236), "done"))
            if story.get("job") == "migration_overdue":
                plan.append(("Server Migration", ANCHOR - timedelta(days=85), "overdue"))
            if story.get("job") == "m365_stalled":
                plan.append(("M365 Rollout", ANCHOR - timedelta(days=95), "stalled"))
            if not plan or r.random() < 0.5:
                for _ in range(r.choice([1, 1, 2])):
                    name = r.choice(OPTIONAL_JOBS)
                    if any(p[0] == name for p in plan):
                        continue
                    start = ANCHOR - timedelta(days=r.randint(20, 330))
                    if start < self.company_created[cid]:
                        continue
                    plan.append((name, start, "natural"))
            for name, start, force in plan:
                self.build_job(c, name, start, force)

    def build_job(self, c: dict, name: str, start: datetime, force: str) -> None:
        r = self.rng
        tpl = JOB_TEMPLATES[name]
        cid = c["id"]
        job_id = self.d.new_id("job")
        due = start + timedelta(days=tpl["length"])
        manager = 1 if name != "New Client Onboarding" else r.choice([1, 4])
        job_complete = force in ("done",) or (force == "natural" and due < ANCHOR - timedelta(days=5))
        status = "completed" if job_complete else ("on_hold" if force == "stalled" else "active")
        completed_at = min(due + timedelta(days=r.randint(-3, 10)), ANCHOR - timedelta(days=1)) if job_complete else None
        self.d.jobs.append({
            "id": job_id, "title": name, "description": tpl["desc"], "against_type": "company", "against_id": cid,
            "company_id": cid, "manager": manager, "status": status,
            "standing": "closed" if job_complete else "open", "date_started": day(start), "date_due": day(due),
            "date_completed": day(completed_at),
        })
        for m_title, off, length, tasks in tpl["milestones"]:
            m_start, m_due = start + timedelta(days=off), start + timedelta(days=off + length)
            mid = self.d.new_id("milestone")
            m_done_at = None
            self.d.milestones.append({
                "id": mid, "title": m_title, "against_type": "job", "against_id": job_id, "job_id": job_id,
                "company_id": cid, "date_commenced": day(m_start), "date_due": day(m_due), "date_completed": None,
            })
            for t_idx, t_title in enumerate(tasks):
                t_due = m_start + timedelta(days=max(1, int(length * (t_idx + 1) / len(tasks))))
                if job_complete:
                    t_status = "complete"
                elif force == "zombie":
                    t_status = "complete" if m_title.startswith("Discovery") or (m_title.startswith("Agent") and t_idx < 3) else ("inprogress" if t_idx == 0 else "pending")
                elif force == "stalled":
                    t_status = "complete" if m_title.startswith("Tenant") else ("inprogress" if (m_title.startswith("Mailbox") and t_idx == 0) else "pending")
                elif force == "overdue":
                    t_status = "complete" if m_title in ("Planning", "Build and Staging") and t_idx < 2 else ("inprogress" if t_idx == 0 and m_title in ("Build and Staging", "Cutover") else "pending")
                elif t_due < ANCHOR:
                    t_status = "complete" if r.random() < 0.85 else r.choice(["pending", "inprogress"])
                else:
                    t_status = "pending"
                    if t_due - timedelta(days=4) < ANCHOR and r.random() < 0.5:
                        t_status = "inprogress"
                if force == "active" and t_due < ANCHOR - timedelta(days=3) and t_status == "complete" and r.random() < 0.18:
                    t_status = "pending"  # a couple of overdue onboarding tasks
                completed = None
                if t_status == "complete":
                    completed = min(t_due + timedelta(days=r.randint(-2, 4)), ANCHOR - timedelta(days=1))
                assignee = r.choice([1, 2, 3, 3, 4]) if name == "New Client Onboarding" else r.choice([1, 2, 3])
                self.d.tasks.append({
                    "id": self.d.new_id("task"), "title": t_title, "description": f"{t_title} for {c['name']}.",
                    "against_type": "milestone", "against_id": mid, "milestone_id": mid, "job_id": job_id,
                    "company_id": cid, "assignee": assignee,
                    "assignee_name": next(t["name"] for t in self.techs if t["id"] == assignee),
                    "status": t_status, "standing": "closed" if t_status == "complete" else "open",
                    "date_due": day(t_due), "date_completed": day(completed),
                    "time_allocated_minutes": r.choice([30, 60, 120, 240]),
                })
        # activities on job
        n = r.randint(3, 8) if status != "on_hold" else 2
        for k in range(n):
            when = self.rand_dt(start, min(ANCHOR, start + timedelta(days=tpl["length"] + 5)))
            owner = r.choice([1, 2, 3, 4])
            if k % 2:
                self.d.activities.append(self.activity_row("time", "job", job_id, cid, owner, "Project work: " + r.choice(NOTES_PROGRESS).rstrip("."),
                                                           when, r.choice([30, 60, 120, 180, 240]), True))
            else:
                self.d.activities.append(self.activity_row("note", "job", job_id, cid, owner, r.choice(NOTES_PROGRESS), when, 0, False))

    # -- requests ----------------------------------------------------------
    def gen_requests(self) -> None:
        r = self.rng
        ids = [c["id"] for c in self.clients]
        w = [c["employees"] for c in self.clients]
        rows = []
        for k in range(45):
            title, body = r.choice(REQUEST_TEMPLATES)
            when = self.rand_dt(ANCHOR - timedelta(days=10), ANCHOR - timedelta(minutes=30), recent_bias=1.5)
            if k % 9 == 8:
                rows.append({"id": 0, "title": "Re: " + title, "body": body, "from_name": r.choice(FIRST) + " " + r.choice(LAST),
                             "from_email": f"{r.choice(FIRST).lower()}{r.randint(10, 99)}@mailbox.example", "company_id": None,
                             "contact_id": None, "source": "email", "status": "new", "date_received": iso(when),
                             "note": "Unrecognized sender"})
                continue
            cid = r.choices(ids, w)[0]
            contact = r.choice(self.contacts_by_co[cid])
            rows.append({"id": 0, "title": title, "body": f"{body}\n\nThanks,\n{contact['firstname']}", "from_name": contact["name"],
                         "from_email": contact["email"], "company_id": cid, "contact_id": contact["id"],
                         "source": "email", "status": "new", "date_received": iso(when), "note": None})
        rows.sort(key=lambda x: x["date_received"])
        for row in rows:
            row["id"] = self.d.new_id("request")
        self.d.requests = rows

    # -- assets ------------------------------------------------------------
    def gen_assets(self) -> None:
        r = self.rng
        kind = {"workstation": "Workstation", "laptop": "Laptop", "server": "Server", "firewall": "Firewall",
                "switch": "Switch", "printer": "Printer"}
        for c in self.clients:
            story = STORIES.get(c["id"], {})
            for dev in self.devices_by_co[c["id"]]:
                if story.get("onboarding") == "active" and r.random() < 0.5:
                    continue  # not yet documented in the PSA
                self.d.assets.append({
                    "id": self.d.new_id("asset"), "title": dev["hostname"], "asset_type": kind[dev["deviceClass"]],
                    "against_type": "company", "against_id": c["id"], "company_id": c["id"],
                    "contact_id": dev["assignedContactId"], "manufacturer": dev["manufacturer"], "model": dev["model"],
                    "serial_number": dev["serialNumber"], "status": "active", "date_purchased": dev["purchaseDate"],
                    "warranty_expiry": dev["warrantyExpiry"], "ncentral_device_id": dev["deviceId"],
                })
            # a few retired / in-storage assets with no monitored device
            for _ in range(r.choice([0, 0, 1, 2])):
                cls = r.choice(["laptop", "workstation", "printer"])
                mfr, model, pfx = r.choice(MODELS[cls])
                self.d.assets.append({
                    "id": self.d.new_id("asset"), "title": f"Retired {kind[cls]}", "asset_type": kind[cls],
                    "against_type": "company", "against_id": c["id"], "company_id": c["id"], "contact_id": None,
                    "manufacturer": mfr, "model": model, "serial_number": f"{pfx}{r.randint(10_000_000, 99_999_999)}X",
                    "status": r.choice(["retired", "in_storage"]), "date_purchased": day(ANCHOR - timedelta(days=r.randint(1400, 2600))),
                    "warranty_expiry": day(ANCHOR - timedelta(days=r.randint(200, 1400))), "ncentral_device_id": None,
                })

    # -- alerts and patching ----------------------------------------------
    def gen_alerts_and_patch(self) -> None:
        r = self.rng
        alerts: list[dict] = []
        plan_of = {c["id"]: plan_key(c) for c in self.clients}
        sec_heavy = {5000 + i + 1 for i, c in enumerate(self.clients) if STORIES.get(c["id"], {}).get("security_heavy")}
        patch_story = {5000 + i + 1 for i, c in enumerate(self.clients) if STORIES.get(c["id"], {}).get("patch_backlog")}

        def add(dev: dict, service: str, sev: str, msg: str, trig: datetime, cleared: datetime | None):
            alerts.append({
                "alertId": 0, "customerId": dev["customerId"], "customerName": dev["customerName"],
                "siteId": dev["siteId"], "deviceId": dev["deviceId"], "deviceName": dev["hostname"],
                "serviceName": service, "severity": sev, "message": msg,
                "state": "cleared" if cleared else "active", "active": cleared is None,
                "triggeredAt": iso(trig), "clearedAt": iso(cleared),
                "acknowledged": bool(cleared) or r.random() < 0.25,
            })

        for dev in self.d.nc_devices:
            cls = dev["deviceClass"]
            last_seen = datetime.strptime(dev["lastSeen"], "%Y-%m-%dT%H:%M:%SZ")
            windows = (dev["os"] or "").startswith("Windows")
            # patch status
            ps = self.make_patch(dev, patch_story, plan_of)
            self.d.nc_patch[dev["deviceId"]] = ps
            # active alerts derived from state
            if not dev["online"]:
                sev = "critical" if cls in ("server", "firewall", "switch") else "warning"
                add(dev, "Connectivity", sev, "Device has stopped responding", last_seen + timedelta(minutes=15), None)
            if dev["os"] == "Windows 10 Pro" and r.random() < 0.5:
                add(dev, "OS End of Support", "warning", "Operating system is no longer receiving security updates",
                    ANCHOR - timedelta(days=r.randint(5, 300)), None)
            if ps["rebootPending"] and r.random() < 0.5 and windows:
                add(dev, "Windows Update", "warning", "Pending reboot for more than 7 days", ANCHOR - timedelta(days=r.randint(1, 20)), None)
            if cls == "server" and dev["online"] and r.random() < 0.12:
                add(dev, "Backup Status", "critical", "Last backup job failed", ANCHOR - timedelta(hours=r.randint(2, 70)), None)
            if cls in ("workstation", "laptop", "server") and dev["online"] and r.random() < 0.035:
                svc = r.choice(ALERT_SERVICES[:2] + ALERT_SERVICES[4:7])
                add(dev, svc[0], svc[1], svc[2], ANCHOR - timedelta(hours=r.randint(1, 120)), None)
            if dev["customerId"] in sec_heavy and cls in ("workstation", "laptop") and r.random() < 0.08:
                add(dev, "Event Log - Security", "critical" if r.random() < 0.4 else "info",
                    "Repeated failed logon attempts" if r.random() < 0.6 else "Malware detected and quarantined",
                    ANCHOR - timedelta(hours=r.randint(1, 200)), None)
            # historical cleared alerts
            n_hist = {"workstation": 1.2, "laptop": 1.6, "server": 8, "firewall": 4, "switch": 2, "printer": 1.5}[cls]
            for _ in range(int(r.expovariate(1 / n_hist))):
                svc = r.choice(ALERT_SERVICES)
                if cls in ("printer", "switch"):
                    svc = ("Connectivity", "warning", "Device has stopped responding")
                trig = ANCHOR - timedelta(minutes=r.randint(60 * 24, 60 * 24 * 365))
                dur = timedelta(minutes=max(5, int(r.lognormvariate(0, 1.2) * 180)))
                add(dev, svc[0], svc[1], svc[2], trig, min(ANCHOR - timedelta(minutes=1), trig + dur))
        alerts.sort(key=lambda a: (a["triggeredAt"], a["deviceId"], a["serviceName"]))
        for a in alerts:
            a["alertId"] = self.d.new_id("alert")
        self.d.nc_alerts = alerts
        by_dev_cust = {c["customerId"]: c for c in self.d.nc_customers}
        for cust in self.d.nc_customers:
            cust["activeAlertCount"] = sum(1 for a in alerts if a["customerId"] == cust["customerId"] and a["active"])
        _ = by_dev_cust

    def make_patch(self, dev: dict, patch_story: set[int], plan_of: dict[int, str]) -> dict:
        r = self.rng
        cls = dev["deviceClass"]
        managed = bool(dev["os"] and dev["os"].startswith(("Windows", "macOS")))
        pkey = plan_of[dev["accelo_company_id"]]
        if not managed:
            return {"deviceId": dev["deviceId"], "hostname": dev["hostname"], "customerId": dev["customerId"],
                    "patchManaged": False, "patchPolicy": None, "lastScan": None, "lastPatchInstalled": None,
                    "missingCritical": 0, "missingImportant": 0, "missingOptional": 0, "installedLast30Days": 0,
                    "failedLast30Days": 0, "rebootPending": False, "status": "not-applicable"}
        story = dev["customerId"] in patch_story
        u = r.random()
        crit = 0 if u < 0.72 else (r.randint(1, 2) if u < 0.93 else r.randint(3, 8))
        if story:
            crit = max(crit, r.choice([0, 1, 2, 3, 4, 5]))
        imp = r.randint(0, 3) + (crit * 2 if crit else 0)
        if dev["os"] == "Windows 10 Pro":
            crit = max(crit, r.randint(2, 6))
        if dev["os"].startswith("Windows Server 2012"):
            crit = max(crit, r.randint(4, 9))
        if dev["online"]:
            last_scan = ANCHOR - timedelta(hours=r.randint(1, 48))
        else:
            last_scan = datetime.strptime(dev["lastSeen"], "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=r.randint(1, 24))
            crit += min(6, (ANCHOR - last_scan).days // 20)
        reboot = r.random() < (0.45 if story else 0.12) and dev["online"]
        stale = (ANCHOR - last_scan).days > 14
        status = "compliant"
        if crit >= 3 or stale:
            status = "critical"
        elif crit or imp > 2 or reboot:
            status = "attention"
        last_inst = last_scan - timedelta(days=r.randint(1, 30))
        return {
            "deviceId": dev["deviceId"], "hostname": dev["hostname"], "customerId": dev["customerId"],
            "patchManaged": True, "patchPolicy": PLAN_PATCH_POLICY[pkey], "lastScan": iso(last_scan),
            "lastPatchInstalled": iso(last_inst), "missingCritical": crit, "missingImportant": imp,
            "missingOptional": r.randint(0, 6), "installedLast30Days": r.randint(0, 14) if dev["online"] else 0,
            "failedLast30Days": r.choice([0, 0, 0, 1, 2]), "rebootPending": reboot, "status": status,
        }

    def finalize_ids(self) -> None:
        self.d.activities.sort(key=lambda a: (a["date_created"], a["against_type"], a["against_id"]))
        for a in self.d.activities:
            a["id"] = self.d.new_id("activity")
        for i in self.d.issues:
            i.pop("_stale", None)


def generate(seed_path: str | Path, seed: int = DEFAULT_SEED) -> Dataset:
    return Generator(Path(seed_path), seed).build()

# Android OPSEC Hardening – Automated DNS Analysis System

## 📋 Overview

This directory contains all automation scripts used to analyze DNS queries from Android devices, identify telemetry and tracking domains, and safely manage allowlist / denylist configurations while preserving system functionality.

All scripts are designed to work together as a controlled OPSEC workflow, but can also be executed individually when required.

---

## 🎯 Key Capabilities

- Automated analysis of large DNS datasets (15k+ queries)
- Classification of telemetry, ads, OEM tracking, and critical services
- Identification and investigation of unknown domains
- Safe allowlist / denylist management (conflict-free)
- Automatic changelog and baseline backup handling
- End-to-end workflow orchestration

---

## 📁 Scripts Structure

```
scripts/
├── README.md
├── requirements.txt
├── requirements-dev.txt
│   
├── analysis/
│   ├── dns_review_tool_enhanced.py
│   └── extract_unknowns.py
│
├── investigation/
│   └── domain_investigator.py
│
├── maintenance/
│   ├── auto_updater.py
│   ├── manual_updater.py
│   └── clean_files.py
│
└── workflows/
    └── opsec_workflow.py
```
---
> All commands assume execution from inside ** `opsec/scripts/`**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- DNS logs exported from your Android device  
  (NextDNS strongly recommended)

---

### Installation

```
cd android-opsec-hardening/opsec/scripts
pip install -r requirements.txt
# requirements-dev.txt (opcional)
-r requirements.txt
matplotlib>=3.8
```
Ensure your DNS data file exists:
```
opsec/data/dns_queries.txt
```
---
## 📊 Usage Guide
### Preparing DNS data (NextDNS)

Export DNS logs from NextDNS and run:
/android-opsec-hardening/ ->

- `cut -d',' -f2 logs/export_example.csv | tail -n +2 > opsec/data/dns_queries.txt`

More information: - `/android-opsec-hardening/logs/README.md`
# Option 1 – Full Automated Workflow (Recommended)
```
python workflows/opsec_workflow.py --full
```
This performs:

- DNS analysis

- Unknown domain extraction

- Domain investigation

- Allowlist / denylist updates

- Statistics, reports, and changelog updates

"- `opsec_workflow.py` never modifies baselines directly"
---
# Option 2 – Quick Update (No Re-analysis)
```
python workflows/opsec_workflow.py --quick
```
Use this when reports already exist and you only want to synchronize allowlists / denylists.
---
# Option 3 – Individual Scripts
1️⃣ Analyze DNS Queries
```
python analysis/dns_review_tool_enhanced.py
```
Output:

- `../reports/opsec-report-enhanced.md`
---
2️⃣ Extract Unknown Domains
```
python analysis/extract_unknowns.py
```
---
Output:

- `../reports/unknown_domains_report.txt`
---
3️⃣ Investigate Domains
```
python investigation/domain_investigator.py
```
Output:

- `../reports/domain_investigation.json`

- `../reports/final_recommendations.md`
---
4️⃣ Update Lists Automatically
```
python maintenance/auto_updater.py --update
```
Show Current Stats
```
python maintenance/auto_updater.py --stats
```
---
5️⃣ Manual Domain Updates
```
python maintenance/manual_updater.py
```
Use only for explicit, human-reviewed changes.
---
6️⃣ Clean Corrupted Baseline Files
```
python maintenance/clean_files.py
```
Safely removes accidental Python code from - `.txt` baseline files and creates backups.
---
## 🧪 CI / Dry-Run Mode Integration
To improve safety, auditability, and CI compatibility, a - `--dry-run` mode was integrated into the automatic updater.

This mode allows simulating all changes without modifying any files, making it ideal for validation before applying updates.

What was done:

1. Added a - `--dry-run CLI flag`
- The auto_updater.py script now accepts:
```
--dry-run
```
This flag instructs the updater to simulate changes only.

2. Separated decision logic from write operations
- Domain evaluation (added / skipped / conflicts) always runs, but:
- File writes
- Backups
- Changelog updates are skipped when - `--dry-run is enabled.`

3. Preserved full reporting behavior
Even in dry-run mode, the script still:
- Parses - `approved_actions.txt`
- Detects conflicts and duplicates
- Prints a full summary of intended changes

4. Clear console output for CI usage
When running in dry-run mode, the script explicitly indicates:
- No files were modified
- No backups were created
- No changelog entries were written

5. CI-friendly by design
This enables:
- Pre-merge validation in GitHub Actions
- Safe testing of new - `approved_actions.txt`
- Review of changes before human approval

Example usage
Preview changes safely:
```
python maintenance/auto_updater.py --update --dry-run
```
Apply changes only after validation:
```
python maintenance/auto_updater.py --update
```
Why this matters
- Prevents accidental allowlist / denylist corruption
- Enables automated testing pipelines
- Enforces human-in-the-loop OPSEC decisions
- Makes all changes predictable and reversible
---
## 📋 Input Files
# DNS Queries

- `opsec/data/dns_queries.txt`

Plain text, one domain per line:
```
google.com
telemetry.example.com
api.service.com
```
---
## 📄 Baseline Files

Located in - `opsec/baseline/`

- `baseline-roots.txt` → domains that must never be blocked

- `denylist.txt` → telemetry, ads, tracking

- `critical-services.txt` → domains requiring special handling

- `phantom-tlds.txt` → synthetic / special-use TLDs
---
## 📊 Output Reports

Generated in - `opsec/reports/`:

- `opsec-report-enhanced.md` – main analysis report

- `summary.txt` – quick statistics

- `unknown_domains_report.txt`

- `domain_investigation.json`

- `final_recommendations.md`

- `quick_actions.txt`

Reports are ignored by git by design for OPSEC reasons.
---
## 🛠️ Operational Notes

- Adding 0 domains is normal → means system is already aligned

- Never bulk-block without reviewing - `final_recommendations.md`

- Always test functionality after denylist changes
---
## 🧪 Post-Change Testing Checklist

- Notifications (WhatsApp / email)

- App updates (Play Store / F-Droid)

- Browser sync

- Video playback

- VPN connectivity

- DNS resolution
---
## Decision Flow

Analysis and recommendations are generated automatically.
No domain is added to allowlist or denylist unless it is explicitly
approved in `approved_actions.txt`.

This prevents accidental breakage and ensures human validation.
---
## ⚠️ Troubleshooting

Script not found

- Ensure you are in - `opsec/scripts/`
- Verify Python version and dependencies

Functionality issues after update

- Review - `../CHANGELOG.md`

- Temporarily roll back recent denylist additions

- Re-run workflow using - `--quick`
---
## 🔐 OPSEC Philosophy

This system prioritizes real-world usability over aggressive blocking.

The objective is:

- Minimal telemetry

- Maximum functionality

- Measurable and reversible changes

Last updated: 2026-01-12 — Status: ✅ Stable

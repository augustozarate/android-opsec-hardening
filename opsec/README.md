# 📁 `opsec/README.md`

# OPSEC – Automation & Baseline Strategy

This directory defines the **OPSEC core logic** behind this repository.

It contains:
- A clean OPSEC baseline
- Domain classification files
- Automation scripts for periodic review
- Generated reports (not versioned by default)

The goal is to make OPSEC:
- Measurable
- Repeatable
- Auditable over time

---

## 📂 Directory Structure

```
opsec/
├── baseline/
│   ├── baseline-roots.txt
│   ├── denylist.txt
│   └── phantom-tlds.txt
│
├── scripts/
│   |── analysis/
|   ├── investigation/
|   ├── maintenance/
|   └── workflows/
│
├── reports/
│   └── .gitkeep
│
└── README.md
```

## 🧱 Baseline (baseline/)

This folder defines the clean OPSEC baseline.

- `baseline-roots.txt`

Trusted root domains required for:

- System stability

- Connectivity checks

- Core service operation

These domains should never be blocked.

- `denylist.txt`

High-confidence domains associated with:

- Telemetry

- Analytics

- Advertising infrastructure

Used as the primary input for DNS blocking analysis.

- `phantom-tlds.txt`

TLDs commonly associated with:

- Malware

- Phishing

- Disposable infrastructure

- Abuse-heavy domains

Used to evaluate the risk/value ratio of TLD-level blocking.

Blocking a TLD should always be justified by metrics, not assumptions.

## ⚙️ Automation (scripts/)
🔍 - `analysis/`

Scripts focused on measurement and visibility.

Typical responsibilities:

- Analyze DNS datasets
- Classify domains (allowed / denied / unknown)
- Detect trends, ratios, and anomalies
- Support decision-making with metrics

Characteristics:

- Read-only over raw data
- No blocking or enforcement actions
- Designed for repeatable execution
---
🕵️ - `investigation/`

Scripts used for manual or assisted investigation.

Typical responsibilities:

- Inspect suspicious domains
- Enrich domains with external context
- Correlate DNS activity with behavior patterns
- Support false-positive / false-negative review

Characteristics:

- Often interactive or exploratory
- May require analyst judgment
- Used before modifying baselines or denylists
---
🧹 - `maintenance/`

Scripts responsible for baseline hygiene and upkeep.

Typical responsibilities:

- Validate baseline consistency
- Detect stale or unused entries
- Normalize domain lists
- Ensure format and structural integrity

Characteristics:

- Low-risk, controlled changes
- Usually executed periodically
- Focused on long-term stability
---
🔄 - `workflows/`

Scripts that orchestrate multiple steps into a controlled process.

Typical responsibilities:

- End-to-end OPSEC review flows
- Data → analysis → report pipelines
- Coordinated execution of scripts from other folders

Characteristics:

- Opinionated by design
- Represent documented processes, not experiments
- Intended to be auditable and reproducible

## 📊 Reports (reports/)

This directory stores generated outputs such as:

- Monthly OPSEC reviews

- Domain statistics

- Trend comparisons

Reports are intentionally excluded from version control by default
to avoid leaking personal DNS data.

## 🧠 OPSEC Philosophy

This repository follows a baseline-first approach:

- Define what must work

- Reduce noise incrementally

- Measure before hardening further

- Prioritize stability over maximal blocking

Absolute blocking is not OPSEC.
Controlled reduction is.

## ⚠️ Disclaimer

This project is intended for:

- Personal security

- Educational purposes

- Research and experimentation

Do not use this tooling to:

- Evade lawful monitoring

- Interfere with networks you don’t control

- Violate local regulations

## 🔐 Final Note

- `OPSEC is not static.`
- `Baselines must evolve as systems, apps, and threat models change.`
- `Automate review.`
- `Document decisions.`
- `Stay adaptable.`

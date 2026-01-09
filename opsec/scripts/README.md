# OPSEC Review Script – Usage Guide

This document explains how to use the `opsec_review.py` script to analyze DNS activity and generate OPSEC-oriented reports in a safe, reproducible, and auditable way.

---

## 📌 Purpose

The script is designed to:

- Analyze real DNS query logs
- Classify domains by category (telemetry, ads, essential, unknown)
- Detect noise, tracking-heavy roots, and phantom patterns
- Generate a human-readable OPSEC report
- Keep raw data out of version control

---

## 📁 Required Directory Structure

The script expects the following structure:

# OPSEC Review Script – Usage Guide

This document explains how to use the `opsec_review.py` script to analyze DNS activity and generate OPSEC-oriented reports in a safe, reproducible, and auditable way.

---

## 📌 Purpose

The script is designed to:

- Analyze real DNS query logs
- Classify domains by category (telemetry, ads, essential, unknown)
- Detect noise, tracking-heavy roots, and phantom patterns
- Generate a human-readable OPSEC report
- Keep raw data out of version control

---

## 📁 Required Directory Structure

The script expects the following structure:
```
opsec/
├── data/
│ └── dns_queries.txt # Raw DNS domains (one per line)
│
├── scripts/
│ └── opsec_review.py # Analysis script
│
├── reports/
│ └── .gitkeep # Reports are generated here (not versioned)
opsec/
├── data/
│ └── dns_queries.txt # Raw DNS domains (one per line)
│
├── scripts/
│ └── opsec_review.py # Analysis script
│
├── reports/
│ └── .gitkeep # Reports are generated here (not versioned)
```

Resultado en GitHub

- Alineación perfecta

- Tipografía monoespaciada

- Lectura inmediata

- Estándar profesional (README / docs técnicos)


> ⚠️ `opsec/data/` and `opsec/reports/` are intentionally excluded from Git.

---

## 📥 Input Format

The script requires a plain text file:

- `opsec/data/dns_queries.txt`


### Format rules

- One domain per line  
- No headers  
- No timestamps  
- Duplicates are allowed (used for frequency analysis)

Example:

- `example.com`
- `api.example.com`
- `tracker.vendor.net`


---

## 🔄 Preparing the DNS Input

If you export DNS logs from **NextDNS** as CSV:

```bash
cut -d',' -f2 nextdns-export.csv | tail -n +2 > opsec/data/dns_queries.txt

Verify the result:
- `head opsec/data/dns_queries.txt`

🧪 Environment Setup (Recommended)

Use an isolated Python environment.

Option A – Conda
- `conda create -n opsec-review python=3.11`
- `conda activate opsec-review`

Option B – Virtualenv
- `python3 -m venv venv`
- `source venv/bin/activate`
No external dependencies are required.

▶️ Running the Script

From the repository root:
- `python opsec/scripts/opsec_review.py`

📄 Output

The script generates a Markdown report:
- `opsec/reports/opsec-report.md`

The report includes

- Execution timestamp (UTC)

- Total DNS queries analyzed

- Top recurring domains

- Known telemetry / tracking roots

- Unknown or low-frequency domains

- OPSEC interpretation notes

⚠️ Reports are not committed to Git by design.

🔁 Recommended Usage Cycle

- After major OS updates

- After installing new applications

- Monthly as part of OPSEC hygiene

- Compare reports over time (manually or externally)

🛑 OPSEC Notes

- Never commit raw DNS logs

- Never commit generated reports

- Treat DNS data as sensitive metadata

- Review unexpected domains before allowing or blocking

✅ Success Criteria

- A healthy baseline typically shows:

- High volume from known system roots

- Limited ad / telemetry domains

- Stable domain patterns over time

- No unexplained spikes or unknown TLDs

🧠 Final Principle

Measure first. Block second. Document always.

OPSEC is a process, not a static configuration.




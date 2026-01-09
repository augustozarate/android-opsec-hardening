#!/usr/bin/env python3
"""
OPSEC Review Script
-------------------
Purpose:
- Parse DNS logs
- Normalize domains
- Extract root domains
- Classify OPSEC relevance
- Generate a monthly markdown report

Author: Augusto Zarate
Mode: Offline / Reproducible / OPSEC-safe
"""

import sys
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# -------------------------
# Utility functions
# -------------------------

def normalize_domain(domain: str) -> str:
    """Normalize domain (lowercase, strip spaces)."""
    return domain.strip().lower()


def extract_root_domain(domain: str) -> str:
    """
    Extract root domain (simple heuristic).
    Example:
        traffic-nts-ip-assoc.xy.fbcdn.net -> fbcdn.net
    """
    parts = domain.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return domain


def load_domains(file_path: Path) -> list[str]:
    """Load domains from file (one per line)."""
    domains = []
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            domains.append(normalize_domain(line))
    return domains


# -------------------------
# Classification logic
# -------------------------

TELEMETRY_KEYWORDS = (
    "telemetry",
    "analytics",
    "metrics",
    "crash",
    "measurement",
    "tracking",
)

AD_KEYWORDS = (
    "ads",
    "doubleclick",
    "adservice",
    "marketing",
    "promo",
)

CORE_ALLOWLIST = (
    "googleapis.com",
    "whatsapp.net",
    "proton.me",
    "threema.ch",
    "microsoftonline.com",
)


def classify_domain(domain: str) -> str:
    """Classify domain based on heuristics."""
    for k in CORE_ALLOWLIST:
        if domain.endswith(k):
            return "core"

    for k in TELEMETRY_KEYWORDS:
        if k in domain:
            return "telemetry"

    for k in AD_KEYWORDS:
        if k in domain:
            return "ads"

    return "unknown"


# -------------------------
# Report generation
# -------------------------

def generate_report(domains: list[str], output_path: Path):
    roots = [extract_root_domain(d) for d in domains]
    counter = Counter(roots)

    classified = {
        "core": [],
        "telemetry": [],
        "ads": [],
        "unknown": [],
    }

    for root, count in counter.items():
        category = classify_domain(root)
        classified[category].append((root, count))

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    with output_path.open("w", encoding="utf-8") as report:
        report.write(f"# OPSEC Monthly Review\n\n")
        report.write(f"**Generated:** {now}\n\n")
        report.write("## Summary\n\n")
        report.write(f"- Total unique root domains: **{len(counter)}**\n")
        report.write(f"- Total DNS entries analyzed: **{len(domains)}**\n\n")

        for category in ("core", "telemetry", "ads", "unknown"):
            report.write(f"## {category.capitalize()} Domains\n\n")
            if not classified[category]:
                report.write("_None detected._\n\n")
                continue

            for domain, count in sorted(classified[category], key=lambda x: x[1], reverse=True):
                report.write(f"- `{domain}` — {count} queries\n")
            report.write("\n")

        report.write("---\n")
        report.write("🛡️ This report is generated locally for OPSEC review purposes.\n")


# -------------------------
# Main
# -------------------------

def main():
    parser = argparse.ArgumentParser(description="OPSEC DNS Review Tool")
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input file with DNS domains (one per line)"
    )
    parser.add_argument(
        "-o", "--output",
        default="../reports/opsec-review.md",
        help="Output markdown report"
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[!] Input file not found: {input_path}")
        sys.exit(1)

    domains = load_domains(input_path)
    generate_report(domains, output_path)

    print(f"[+] OPSEC report generated: {output_path.resolve()}")


if __name__ == "__main__":
    main()
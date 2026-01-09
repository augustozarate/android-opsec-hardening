"""
OPSEC DNS Review Tool
Hybrid Multi-Device OPSEC Analysis

- Parses DNS query logs
- Compares against OPSEC baselines
- Detects telemetry, ads, phantom TLDs
- Generates Markdown report (GitHub-ready)
"""

import argparse
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
# -------------------------
# Defaults (OPSEC layout)
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
BASELINE_DIR = BASE_DIR / "baseline"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

DEFAULT_INPUT = DATA_DIR / "dns_queries.txt"
DEFAULT_REPORT = REPORTS_DIR / "opsec-report.md"

DENYLIST_FILE = BASELINE_DIR / "denylist.txt"
BASELINE_ROOTS_FILE = BASELINE_DIR / "baseline-roots.txt"
PHANTOM_TLDS_FILE = BASELINE_DIR / "phantom-tlds.txt"


# -------------------------
# Helpers
# -------------------------
def load_list(path):
    if not path.exists():
        return set()
    return {line.strip().lower() for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")}


def extract_root(domain):
    parts = domain.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain


def extract_tld(domain):
    return domain.split(".")[-1]


# -------------------------
# Core logic
# -------------------------
def analyze_domains(domains, denylist, baseline_roots, phantom_tlds):
    counts = Counter(domains)

    analysis = {
        "total_queries": sum(counts.values()),
        "unique_domains": len(counts),
        "denylist_hits": {},
        "baseline_hits": {},
        "phantom_tld_hits": {},
        "unknown_domains": {}
    }

    for domain, count in counts.items():
        root = extract_root(domain)
        tld = extract_tld(domain)

        if root in denylist:
            analysis["denylist_hits"][domain] = count
        elif root in baseline_roots:
            analysis["baseline_hits"][domain] = count
        elif tld in phantom_tlds:
            analysis["phantom_tld_hits"][domain] = count
        else:
            analysis["unknown_domains"][domain] = count

    return analysis


# -------------------------
# Reporting
# -------------------------
def generate_report(analysis, output_path):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def section(title, data, limit=20):
        if not data:
            return f"### {title}\n_No entries detected._\n\n"
        lines = [f"- `{d}` → {c}" for d, c in sorted(data.items(), key=lambda x: x[1], reverse=True)[:limit]]
        return f"### {title}\n" + "\n".join(lines) + "\n\n"

    report = f"""# 🛡️ OPSEC DNS Review Report

**Generated:** {now}

## Summary
- Total DNS queries: **{analysis['total_queries']}**
- Unique domains: **{analysis['unique_domains']}**

## 🔴 Denylist Hits (Telemetry / Ads)
{section("Blocked / Should Be Blocked", analysis["denylist_hits"])}

## 🟢 Baseline Domains (Expected & Safe)
{section("Baseline Domains", analysis["baseline_hits"])}

## 👻 Phantom TLD Activity
{section("Suspicious TLDs", analysis["phantom_tld_hits"])}

## ⚠️ Unknown / Review Required
{section("Unclassified Domains", analysis["unknown_domains"], limit=30)}

---

### Analyst Notes
- High denylist volume = good OPSEC enforcement
- Phantom TLD hits should be investigated
- Unknown domains may indicate new apps or updates

"""
    output_path.write_text(report)
    print(f"[+] Report written to {output_path}")


# -------------------------
# Entry point
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="OPSEC DNS Review Tool")
    parser.add_argument(
        "-i", "--input",
        nargs="+",
        default=[DEFAULT_INPUT],
        help="DNS query files (one per device or period)"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_REPORT,
        help="Markdown report output"
    )

    args = parser.parse_args()

    denylist = load_list(DENYLIST_FILE)
    baseline_roots = load_list(BASELINE_ROOTS_FILE)
    phantom_tlds = load_list(PHANTOM_TLDS_FILE)

    all_domains = []

    for file in args.input:
        path = Path(file)
        if not path.exists():
            print(f"[!] File not found: {path}")
            continue
        domains = [line.strip().lower() for line in path.read_text().splitlines() if line.strip()]
        all_domains.extend(domains)

    if not all_domains:
        print("[!] No DNS data loaded. Exiting.")
        return

    analysis = analyze_domains(all_domains, denylist, baseline_roots, phantom_tlds)
    generate_report(analysis, Path(args.output))


if __name__ == "__main__":
    main()

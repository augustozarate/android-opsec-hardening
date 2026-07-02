"""
Unknown Domain Investigator
Fixed and aligned with android-opsec-hardening directory structure
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================
# CONFIGURATION
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = Path(__file__).resolve()
REPORTS_DIR = PROJECT_ROOT / "reports"

# Input files
UNKNOWN_DOMAINS_FILE = REPORTS_DIR / "unknown_domains_report.txt"
OPSEC_REPORT_FILE = REPORTS_DIR / "opsec-report-enhanced.md"

# Output files
INVESTIGATION_RESULTS = REPORTS_DIR / "domain_investigation.json"
INVESTIGATION_REPORT = REPORTS_DIR / "domain_investigation_report.md"
DECISION_GUIDE = REPORTS_DIR / "blocking_decisions.md"
QUICK_ACTIONS = REPORTS_DIR / "quick_actions.txt"

# ============================================
# SERVICE PATTERNS
# ============================================
SERVICE_PATTERNS = {
    "firefox_sync": [
        r"\.mozilla\.com$",
        r"firefox\.settings\.services\.mozilla\.com",
        r"services\.mozilla\.com",
    ],
    "dns_service": [
        r"\.nextdns\.io$",
        r"dns\.google",
        r"cloudflare-dns\.com",
        r"dns\.quad9\.net",
    ],
    "samsung_essential": [
        r"api\.account\.samsung\.com",
        r"api\.samsungcloud\.com",
        r"fota-cloud-dn\.ospserver\.net",
    ],
    "samsung_telemetry": [
        r"\.samsungdm\.com$",
        r"di\.atlas\.samsung\.com",
        r"dqa\.samsung\.com",
    ],
    "google_telemetry": [
        r"-pa\.googleapis\.com$",
        r"app-measurement\.com$",
        r"firebaseinstallations\.googleapis\.com",
    ],
    "analytics": [
        r"\.scorecardresearch\.com$",
        r"doubleclick\.net",
        r"googleads\.",
    ],
    "cdn": [
        r"\.gstatic\.com$",
        r"\.fbcdn\.net$",
        r"\.googlevideo\.com$",
    ],
    "developer": [
        r"github\.com$",
        r"\.githubusercontent\.com$",
        r"example\.org$",
    ],
    "network": [
        r"\.pool\.ntp\.org$",
        r"\.arpa$",
    ],
    "social_media": [
        r"\.twitter\.com$",
        r"\.facebook\.com$",
        r"\.instagram\.com$",
        r"\.vk\.ru$",
    ],
    "security": [
        r"mullvad\.net$",
    ],
}

# ============================================
# HELPERS
# ============================================
def analyze_domain(domain):
    import re
    for category, patterns in SERVICE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, domain, re.IGNORECASE):
                return category
    return "unknown"

def get_recommendation(category, domain):
    if category in ["firefox_sync", "dns_service", "samsung_essential", "network", "security"]:
        return {"action": "WHITELIST", "confidence": "HIGH", "priority": "Immediate",
                "reason": f"Essential {category.replace('_', ' ')} service"}
    if category in ["samsung_telemetry", "google_telemetry", "analytics"]:
        return {"action": "DENYLIST", "confidence": "HIGH", "priority": "Immediate",
                "reason": f"Confirmed {category.replace('_', ' ')}"}
    if category in ["cdn", "social_media"]:
        return {"action": "MONITOR", "confidence": "MEDIUM", "priority": "Phase 2",
                "reason": "Non-essential infrastructure"}
    if category == "developer":
        return {"action": "WHITELIST", "confidence": "MEDIUM", "priority": "Phase 1",
                "reason": "Development service"}
    return {"action": "INVESTIGATE", "confidence": "LOW", "priority": "Phase 3",
            "reason": "Requires manual review"}

def extract_domain_frequency(report_content, domain):
    import re
    match = re.search(rf"`{re.escape(domain)}` → (\d+)", report_content)
    return int(match.group(1)) if match else 0

# ============================================
# CORE LOGIC
# ============================================
def investigate_domains(domains, report_content):
    results = {}
    print(f"[+] Investigating {len(domains)} domains...")
    for domain in domains:
        category = analyze_domain(domain)
        frequency = extract_domain_frequency(report_content, domain)
        recommendation = get_recommendation(category, domain)
        results[domain] = {
            "domain": domain,
            "category": category,
            "frequency": frequency,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat()
        }
    return results

# ============================================
# REPORTS
# ============================================
def generate_quick_actions(results):
    grouped = defaultdict(list)
    for d, r in results.items():
        grouped[r["recommendation"]["action"]].append(d)

    text = "# QUICK ACTIONS\n\n"
    for action in ["DENYLIST", "WHITELIST", "MONITOR"]:
        if grouped[action]:
            text += f"## {action}\n"
            for d in sorted(grouped[action]):
                text += f"{d}\n"
            text += "\n"
    return text

# ============================================
# MAIN
# ============================================
def main():
    print("=" * 60)
    print("UNKNOWN DOMAIN INVESTIGATOR")
    print("=" * 60)
    print(f"Script:  {SCRIPT_PATH}")
    print(f"Project: {PROJECT_ROOT}")
    print(f"Reports: {REPORTS_DIR}\n")

    if not UNKNOWN_DOMAINS_FILE.exists():
        print(f"[!] Missing {UNKNOWN_DOMAINS_FILE}")
        return

    domains = [d.strip() for d in UNKNOWN_DOMAINS_FILE.read_text().splitlines() if d.strip()]
    report_content = OPSEC_REPORT_FILE.read_text() if OPSEC_REPORT_FILE.exists() else ""

    results = investigate_domains(domains, report_content)

    INVESTIGATION_RESULTS.write_text(json.dumps(results, indent=2))
    QUICK_ACTIONS.write_text(generate_quick_actions(results))

    print("\n✅ Investigation completed successfully")
    print(f"  → {INVESTIGATION_RESULTS.name}")
    print(f"  → {QUICK_ACTIONS.name}")

if __name__ == "__main__":
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        main()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        sys.exit(1)

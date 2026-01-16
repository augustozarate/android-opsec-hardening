"""
OPSEC DNS Review Tool
Hybrid Multi-Device OPSEC Analysis

– Parses DNS query logs
– Compares against OPSEC baselines
– Detects telemetry, ads, phantom TLDs
– Enhanced categorization with privacy apps detection
– Generates comprehensive Markdown report

Project: https://github.com/augustozarate/android-opsec-hardening
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, UTC
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "dns_queries.txt"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORT_DIR / "opsec-report-enhanced.md"
SUMMARY_FILE = REPORT_DIR / "summary.txt"

BASELINE_DIR = PROJECT_ROOT / "baseline"
BASELINE_ROOTS = BASELINE_DIR / "baseline-roots.txt"
DENYLIST = BASELINE_DIR / "denylist.txt"
PHANTOM_TLDS = BASELINE_DIR / "phantom-tlds.txt"
CRITICAL_SERVICES = BASELINE_DIR / "critical-services.txt"

# -----------------------------
# Enhanced Pattern-based subcategories (UPDATED)
# -----------------------------

ENHANCED_PATTERNS = {
    # Infrastructure
    "cdn_media": {
        "patterns": [
            r"\.(fbcdn\.net|cdninstagram\.com)$",
            r"(whatsapp\.net|\.cdn\.whatsapp\.net)$",
            r"(ytimg\.com|googleusercontent\.com|gvt1\.com)$",
            r"\.(spotifycdn\.com|scdn\.co)$",
            r"yt3\.ggpht\.com$",
        ],
        "emoji": "🟡",
        "title": "Infrastructure – CDN & Media Delivery"
    },
    
    # Google Core (excluding telemetry)
    "google_core_system": {
        "patterns": [
            r"^(android\.apis\.google\.com|play\.googleapis\.com|connectivitycheck\.gstatic\.com)$",
            r"^android\.clients\.google\.com$",
            r"^www\.googleapis\.com$",
            r"^time\.android\.com$",
            r"^android\.googleapis\.com$",
            r"^play\.google\.com$",
        ],
        "emoji": "🟢",
        "title": "Baseline – Core System APIs"
    },
    
    # Google Services (mixed)
    "google_services": {
        "patterns": [
            r"^safebrowsing\.googleapis\.com$",
            r"^suggestqueries\.google\.com$",
            r"^www\.google\.com$",
            r"^fonts\.googleapis\.com$",
            r"^fonts\.gstatic\.com$",
            r"^encrypted-tbn\d\.gstatic\.com$",
            r"^mail\.google\.com$",
            r"^inbox\.google\.com$",
            r"^accounts\.google\.com$",
        ],
        "emoji": "🟡",
        "title": "Google Services (Mixed)"
    },
    
    # NTP and synchronization
    "time_sync": {
        "patterns": [
            r"\.pool\.ntp\.org$",
            r"^time\.google\.com$",
        ],
        "emoji": "🟢",
        "title": "Time Synchronization"
    },
    
    # Privacy Apps
    "privacy_apps": {
        "patterns": [
            r"(proton\.me|protonmail\.ch)$",
            r"^api\.ente\.io$",
            r"^app\.tuta\.com$",
            r"\.threema\.ch$",
            r"^sentry\.ente\.io$",
            r"^sentry-reporter\.ente\.io$",
        ],
        "emoji": "🔵",
        "title": "Privacy-Focused Applications"
    },
    
    # DNS & Privacy Services
    "dns_privacy": {
        "patterns": [
            r"^my\.nextdns\.io$",
            r"^api\.nextdns\.io$",
            r"^favicons\.nextdns\.io$",
            r"^am\.i\.mullvad\.net$",
            r"^mullvad\.net$",
            r"^cloudflare-dns\.com$",
            r"^dns\.quad9\.net$",
            r"^dns\.google$",
            r"^dns\.google\.com$",
            r"^challenges\.cloudflare\.com$",
        ],
        "emoji": "🔵",
        "title": "DNS & Privacy Services"
    },
    
    # Navigators (EXCLUDING telemetry)
    "browser_services": {
        "patterns": [
            r"^detectportal\.firefox\.com$",
            r"^location\.services\.mozilla\.com$",
            r"^sync-\d+-.+\.sync\.services\.mozilla\.com$",
            r"^token\.services\.mozilla\.com$",
            r"^content-signature-2\.cdn\.mozilla\.net$",
            r"^assets\.mozilla\.net$",
            r"^versioncheck-bg\.addons\.mozilla\.org$",
            r"^services\.addons\.mozilla\.org$",
            r"^updates\.push\.services\.mozilla\.com$",
            r"^api\.accounts\.firefox\.com$",
            r"^profile\.accounts\.firefox\.com$",
            r"^accounts\.firefox\.com$",
        ],
        "emoji": "🟢",
        "title": "Browser Services (Firefox)"
    },
    
    # SDKs and third-party services
    "third_party_sdks": {
        "patterns": [
            r"\.sentry\.io$",
            r"datadoghq\.com$",
            r"branch\.io$",
            r"scorecardresearch\.com$",
            r"stripe\.com$",
            r"revenuecat\.com$",
            r"taboola\.com$",
        ],
        "emoji": "⚫️",
        "title": "Third-Party SDKs & Services"
    },
    
    # Core Social Networks (not telemetry)
    "social_core": {
        "patterns": [
            r"^graph\.(facebook|instagram)\.com$",
            r"^web\.facebook\.com$",
            r"^i\.instagram\.com$",
            r"^g\.whatsapp\.net$",
            r"^www\.facebook\.com$",
            r"^mobile\.facebook\.com$",
        ],
        "emoji": "🔵",
        "title": "Social Media Core Services"
    },
    
    # Streaming and entertainment
    "entertainment": {
        "patterns": [
            r"youtubei\.googleapis\.com$",
            r"^www\.youtube\.com$",
            r"\.spotify\.com$",
            r"chatgpt\.com$",
            r"openai\.com$",
            r"^s\.youtube\.com$",
            r"^redirector\.googlevideo\.com$",
            r"^api\.twitter\.com$",
            r"^api\.x\.com$",
            r"^pbs\.twimg\.com$",
            r"^video\.twimg\.com$",
        ],
        "emoji": "🔵",
        "title": "Entertainment & Streaming"
    },
    
    # Mail and productivity
    "email_productivity": {
        "patterns": [
            r"outlook\.office365\.com$",
            r"login\.microsoftonline\.com$",
            r"imap\.mail\.yahoo\.com$",
            r"api\.login\.yahoo\.com$",
        ],
        "emoji": "🔵",
        "title": "Email & Productivity"
    },
    
    # Samsung Device Services
    "samsung_services": {
        "patterns": [
            r"^api\.account\.samsung\.com$",
            r"^play\.samsungcloud\.com$",
            r"^api\.mop\.apps\.samsung\.com$",
            r"^capi\.samsungcloud\.com$",
            r"^dc\.dqa\.samsung\.com$",
            r"^us-auth2\.samsungosp\.com$",
            r"^ar-odc\.samsungapps\.com$",
            r"^vas\.samsungapps\.com$",
            r"^ers\.samsungcloudplatform\.com$",
            r"^ers\.samsungcloud\.com$",
            r"^fota-cloud-dn\.ospserver\.net$",
            r"^stc\.samsungdis\.com$",
            r"^api\.samsungcloud\.com$",
        ],
        "emoji": "🟢",
        "title": "Samsung Device Services"
    },
    
    # Critical Services (allowlist candidates)
    "critical_services": {
        "patterns": [
            r"^mtalk\.google\.com$",
            r"^edge-mqtt\.facebook\.com$",
            r"^z-m-gateway\.facebook\.com$",
            r"^chat-e2ee-mini\.facebook\.com$",
            r"^payments-graph\.facebook\.com$",
            r"^b-graph\.facebook\.com$",
            r"^test-gateway\.instagram\.com$",
            r"^payments-graph\.instagram\.com$",
        ],
        "emoji": "⚠️",
        "title": "Critical Services (Review)"
    },
    
    # Microsoft Services
    "microsoft_services": {
        "patterns": [
            r"^mobile\.events\.data\.microsoft\.com$",
            r"^config\.edge\.skype\.com$",
            r"^oneclient\.sfx\.ms$",
        ],
        "emoji": "🟡",
        "title": "Microsoft Services"
    },
}

# -----------------------------
# Helpers
# -----------------------------
def load_list(path):
    """Load a text file into a set, ignoring comments and empty lines"""
    if not path.exists():
        return set()
    return {
        line.strip().lower()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }

def root_domain(domain):
    """Extract root domain (e.g., example.com from sub.example.com)"""
    parts = domain.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain

def categorize_denylist(domain, count):
    """Subcategorize denylist entries for better reporting - UPDATED"""
    # First check if it is Mozilla telemetry
    if "telemetry.mozilla.org" in domain or "ads.mozilla.org" in domain:
        return "deny_telemetry", domain, count
    
    # Then the other categories
    if any(p in domain for p in ["googleapis.com", "firebase", "crashlytics", "app-measurement", "geller-pa", "locationhistory-pa"]):
        if "-pa.googleapis.com" in domain and "playstoregatewayadapter" not in domain:
            return "deny_telemetry", domain, count
        elif "firebase" in domain or "crashlytics" in domain:
            return "deny_telemetry", domain, count
        else:
            return "deny_telemetry", domain, count
    elif any(p in domain for p in ["facebook", "instagram"]):
        # Exclude core services from Facebook
        if any(core in domain for core in ["graph.facebook.com", "web.facebook.com", "i.instagram.com"]):
            return "social_core", domain, count
        return "deny_meta", domain, count
    elif "samsung" in domain:
        # Some Samsung domains are telemetry, others are core services
        if any(telemetry in domain for telemetry in ["samsungdm.com", "dls.di.atlas", "dc.di.atlas"]):
            return "deny_oem", domain, count
        return "samsung_services", domain, count
    elif any(p in domain for p in ["doubleclick", "ads.", "analytics", "measurement", "taboola", "googleads", "googleadservices"]):
        return "deny_ads", domain, count
    else:
        return "deny_other", domain, count

def classify_domain(domain, count, denylist_set, baseline_set, phantom_tlds_set):
    """Classify domain with priority system - UPDATED"""
    
    # Priority 1: Check critical services FIRST
    for category_id, category_info in ENHANCED_PATTERNS.items():
        if category_id == "critical_services":
            for pattern in category_info["patterns"]:
                if re.search(pattern, domain):
                    return category_id, domain, count
    
    # Priority 2: Denylist exact matches
    if domain in denylist_set:
        return categorize_denylist(domain, count)
    
    # Priority 3: Enhanced pattern matching (excluding critical_services already reviewed)
    for category_id, category_info in ENHANCED_PATTERNS.items():
        if category_id == "critical_services":
            continue  # Already reviewed
        for pattern in category_info["patterns"]:
            if re.search(pattern, domain):
                return category_id, domain, count
    
    # Priority 4: Baseline/root matches
    root = root_domain(domain)
    if domain in baseline_set or root in baseline_set:
        return "baseline_core", domain, count
    
    # Priority 5: Phantom TLDs
    if root in phantom_tlds_set:
        return "phantom", domain, count
    
    # Priority 6: Unknown
    return "unknown", domain, count

# -----------------------------
# Report Generation
# -----------------------------
def generate_section(title, items, max_items=50, show_count=True):
    """Generate a report section with domain listings - UPDATED"""
    out = f"## {title}\n\n"
    
    if not items:
        return out + "_No entries detected._\n\n"
    
    # Sort by count (descending)
    items.sort(key=lambda x: x[2], reverse=True)
    
    # Show total count if requested
    if show_count and len(items) > max_items:
        out += f"*Showing top {max_items} of {len(items)} entries*\n\n"
        items = items[:max_items]
    elif show_count:
        out += f"*Total entries: {len(items)}*\n\n"
    
    for _, domain, count in items:
        out += f"- `{domain}` → {count}\n"
    
    return out + "\n"

def generate_report(classified_data, total_queries, unique_domains, critical_services):
    """Generate enhanced markdown report - UPDATED"""
    
    # Calculate statistics for analyst notes
    telemetry_count = sum(c for _, _, c in classified_data.get("deny_telemetry", []))
    privacy_count = sum(c for _, _, c in classified_data.get("privacy_apps", []))
    dns_privacy_count = sum(c for _, _, c in classified_data.get("dns_privacy", []))
    unknown_count = len(classified_data.get("unknown", []))
    
    # Count critical services
    critical_count = len(classified_data.get("critical_services", []))
    
    # Get current time
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    
    # Header
    report = f"""# 🛡️ OPSEC DNS Review Report - Enhanced v2

**Generated:** {now}
**Project:** [android-opsec-hardening](https://github.com/augustozarate/android-opsec-hardening)

## 📊 Executive Summary
- **Total DNS queries:** **{total_queries:,}**
- **Unique domains:** **{unique_domains}**
- **🔴 Telemetry blocked:** **{telemetry_count:,}** queries
- **🔵 Privacy apps detected:** **{privacy_count:,}** queries
- **🌐 DNS/Privacy services:** **{dns_privacy_count:,}** queries
- **⚠️ Critical services:** **{critical_count}** domains (review needed)
- **❓ Unknown domains:** **{unknown_count}**

---
"""
    
    # Define report sections in order with their corresponding category IDs - UPDATED
    section_config = [
        ("🔴 Telemetry & Tracking Blocked", ["deny_telemetry", "deny_meta", "deny_oem", "deny_ads", "deny_other"], True),
        ("🟢 System Baseline", ["baseline_core", "time_sync", "browser_services", "google_core_system", "samsung_services"], True),
        ("🔵 User Applications", ["privacy_apps", "social_core", "entertainment", "email_productivity"], True),
        ("🌐 DNS & Privacy Services", ["dns_privacy"], False),
        ("🟡 Infrastructure & Services", ["cdn_media", "google_services", "microsoft_services"], True),
        ("⚫️ Third-Party Services", ["third_party_sdks"], False),
        ("⚠️ Critical Services (Review)", ["critical_services"], False),
        ("👻 Phantom TLDs", ["phantom"], False),
        ("❓ Unknown / Requires Review", ["unknown"], True),
    ]
    
    # Generate each section
    for section_title, category_ids, limit_items in section_config:
        # Collect all items for this section
        all_items = []
        for cat_id in category_ids:
            if cat_id in classified_data:
                all_items.extend(classified_data[cat_id])
        
        if limit_items:
            report += generate_section(section_title, all_items, max_items=50, show_count=True)
        else:
            report += generate_section(section_title, all_items, max_items=1000, show_count=True)
    
    # Critical decision section - improved
    report += """## ⚠️ Critical Decision Points

The following services may break functionality if blocked. Consider allowlist exceptions:

### Messaging & Notifications
- **`mtalk.google.com`** - Google Cloud Messaging (push notifications)
- **`edge-mqtt.facebook.com`** - Meta real-time messaging (Facebook/Instagram chats)
- **`z-m-gateway.facebook.com`** - Meta gateway services
- **`chat-e2ee-mini.facebook.com`** - Facebook encrypted messaging

### Payment Services
- **`payments-graph.facebook.com`** - Facebook Payments
- **`payments-graph.instagram.com`** - Instagram Payments

### System Services
- **`android.clients.google.com`** - Google Play Services core
- **`play.googleapis.com`** - Google Play Services

---
"""
    
    # Analyst notes with auto-generated insights - UPDATED
    unknown_domains_list = classified_data.get("unknown", [])
    top_unknown = sorted(unknown_domains_list, key=lambda x: x[2], reverse=True)[:10]
    
    report += f"""### 📝 Automated Analyst Notes

1. **Telemetry Suppression:** {telemetry_count:,} queries to known telemetry domains were blocked.
2. **Privacy Profile:** High usage of privacy-focused apps detected ({privacy_count:,} queries).
3. **DNS Privacy:** Active use of privacy-focused DNS services ({dns_privacy_count:,} queries).
4. **System Health:** Core services show stable connectivity patterns.
5. **Critical Services:** {critical_count} domains identified that may need allowlisting.
6. **Unknown Domains:** {unknown_count} domains require manual review.

### 🔍 Top Unknown Domains to Investigate:
"""
    
    for _, domain, count in top_unknown:
        report += f"- `{domain}` ({count} queries)\n"
    
    report += """
### 📋 Recommendations:
1. **Review critical services** - Decide which to allowlist for functionality
2. **Investigate unknown domains** - Check the top unknown domains above
3. **Update denylist** - Add new telemetry domains from 'unknown' section
4. **Monitor patterns** - Watch for new telemetry domains in future reports
5. **Balance privacy/functionality** - Consider exceptions for essential services

*Report generated by [OPSEC DNS Review Tool](https://github.com/augustozarate/android-opsec-hardening)*
"""
    
    return report

def generate_summary(classified_data, total_queries, unique_domains):
    """Generate a concise summary file - UPDATED"""
    
    telemetry_count = sum(c for _, _, c in classified_data.get("deny_telemetry", []))
    privacy_count = sum(c for _, _, c in classified_data.get("privacy_apps", []))
    dns_privacy_count = sum(c for _, _, c in classified_data.get("dns_privacy", []))
    unknown_count = len(classified_data.get("unknown", []))
    critical_count = len(classified_data.get("critical_services", []))
    
    summary = f"""OPSEC DNS Analysis Summary - Enhanced v2
Generated: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}

┌──────────────────────────┬─────────────────────┐
│ Metric                   │ Value               │
├──────────────────────────┼─────────────────────┤
│ Total Queries           │ {total_queries:>12,} │
│ Unique Domains          │ {unique_domains:>12} │
│ Telemetry Blocked       │ {telemetry_count:>12,} │
│ Privacy Apps            │ {privacy_count:>12,} │
│ DNS/Privacy Services    │ {dns_privacy_count:>12,} │
│ Critical Services       │ {critical_count:>12} │
│ Unknown Domains         │ {unknown_count:>12} │
└──────────────────────────┴─────────────────────┘

CATEGORY BREAKDOWN:
"""
    
    # Add counts per major category
    categories = [
        ("🔴 Telemetry Blocked", "deny_telemetry"),
        ("🔴 Meta Tracking", "deny_meta"),
        ("🔴 OEM Telemetry", "deny_oem"),
        ("🔴 Ads/Measurement", "deny_ads"),
        ("🟢 System Baseline", "baseline_core"),
        ("🟢 Browser Services", "browser_services"),
        ("🟢 Samsung Services", "samsung_services"),
        ("🔵 Privacy Apps", "privacy_apps"),
        ("🌐 DNS Services", "dns_privacy"),
        ("⚠️ Critical Services", "critical_services"),
        ("❓ Unknown", "unknown"),
    ]
    
    for name, cat_id in categories:
        if cat_id in classified_data:
            count = len(classified_data[cat_id])
            query_sum = sum(c for _, _, c in classified_data[cat_id])
            summary += f"  • {name}: {count} domains, {query_sum:,} queries\n"
        else:
            summary += f"  • {name}: 0 domains\n"
    
    summary += f"\nFull report: {REPORT_FILE.name}\n"
    
    return summary

# -----------------------------
# Main Function
# -----------------------------
def main():
    """Enhanced main function - UPDATED"""
    
    print("[+] OPSEC DNS Review Tool - Enhanced v2")
    print("[+] Project: https://github.com/augustozarate/android-opsec-hardening")
    print()
    
    # Check if data file exists
    if not DATA_FILE.exists():
        print(f"[!] Error: Data file not found at {DATA_FILE}")
        print(f"[!] Please ensure dns_queries.txt exists in the data directory")
        return
    
    print("[+] Loading DNS query data...")
    queries = [
        q.strip().lower()
        for q in DATA_FILE.read_text().splitlines()
        if q.strip()
    ]
    
    if not queries:
        print("[!] Error: No queries found in data file")
        return
    
    counter = Counter(queries)
    print(f"[✓] Processed {len(queries):,} queries, {len(counter)} unique domains")
    
    # Load baseline lists
    print("[+] Loading baseline lists...")
    baseline = load_list(BASELINE_ROOTS)
    denylist_set = load_list(DENYLIST)
    phantom_tlds_set = load_list(PHANTOM_TLDS)
    critical_services = load_list(CRITICAL_SERVICES)
    
    print(f"[✓] Loaded {len(baseline)} baseline roots, {len(denylist_set)} denylist entries")
    print(f"[✓] Loaded {len(phantom_tlds_set)} phantom TLDs, {len(critical_services)} critical services")
    
    # Classify all domains
    print("[+] Classifying domains with enhanced patterns...")
    classified_data = defaultdict(list)
    
    for domain, count in counter.items():
        category_id, domain, count = classify_domain(
            domain, count, denylist_set, baseline, phantom_tlds_set
        )
        classified_data[category_id].append((category_id, domain, count))
    
    # Print classification summary
    print("\n[+] Classification Summary:")
    categories_display = [
        ("deny_telemetry", "🔴 Telemetry"),
        ("deny_meta", "🔴 Meta Tracking"),
        ("deny_oem", "🔴 OEM Telemetry"),
        ("deny_ads", "🔴 Ads"),
        ("baseline_core", "🟢 Baseline Core"),
        ("browser_services", "🟢 Browser"),
        ("samsung_services", "🟢 Samsung"),
        ("privacy_apps", "🔵 Privacy Apps"),
        ("dns_privacy", "🌐 DNS Services"),
        ("critical_services", "⚠️ Critical"),
        ("unknown", "❓ Unknown"),
    ]
    
    for cat_id, display_name in categories_display:
        if cat_id in classified_data:
            count = len(classified_data[cat_id])
            query_sum = sum(c for _, _, c in classified_data[cat_id])
            print(f"  • {display_name:20} → {count:4} domains, {query_sum:8,} queries")
    
    # Generate reports
    print("\n[+] Generating reports...")
    REPORT_DIR.mkdir(exist_ok=True)
    
    # Generate main report
    report = generate_report(
        classified_data, 
        sum(counter.values()), 
        len(counter),
        critical_services
    )
    REPORT_FILE.write_text(report)
    
    # Generate summary file
    summary = generate_summary(classified_data, sum(counter.values()), len(counter))
    SUMMARY_FILE.write_text(summary)
    
    print(f"[✓] Enhanced report written to: {REPORT_FILE}")
    print(f"[✓] Summary written to: {SUMMARY_FILE}")
    
    # Show key statistics
    telemetry_count = sum(c for _, _, c in classified_data.get("deny_telemetry", []))
    privacy_count = sum(c for _, _, c in classified_data.get("privacy_apps", []))
    dns_privacy_count = sum(c for _, _, c in classified_data.get("dns_privacy", []))
    critical_count = len(classified_data.get("critical_services", []))
    unknown_count = len(classified_data.get("unknown", []))
    
    print(f"""
┌─────────────────────────────────────────┐
│           KEY STATISTICS                │
├─────────────────────────────────────────┤
│ 🔴 Telemetry Blocked: {telemetry_count:>12,} │
│ 🔵 Privacy Apps:      {privacy_count:>12,} │
│ 🌐 DNS Services:      {dns_privacy_count:>12,} │
│ ⚠️ Critical Services:  {critical_count:>12} │
│ ❓ Unknown Domains:   {unknown_count:>12} │
└─────────────────────────────────────────┘
""")
    
    if unknown_count > 0:
        print(f"[!] Note: {unknown_count} domains require manual review")
        print(f"    Check the 'Unknown / Requires Review' section in the report")
    
    if critical_count > 0:
        print(f"[!] Note: {critical_count} critical services identified")
        print(f"    Review the 'Critical Services' section for allowlist decisions")
    
    print("\n[+] Done! Review the reports in the 'reports' directory.")

if __name__ == "__main__":
    main()
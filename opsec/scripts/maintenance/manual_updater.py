"""
Manual updater for specific domains
"""

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parents[1] # ← opsec

if not (PROJECT_ROOT / "baseline").exists():
    raise RuntimeError(f"Baseline directory not found at {PROJECT_ROOT / 'baseline'}")

# Domains to add based on your investigation
WHITELIST_DOMAINS = [
    "firefox.settings.services.mozilla.com",
    "link-ip.nextdns.io",
    "test-ipv6.nextdns.io",
    "ipv4only.arpa",
    "ipv4.am.i.mullvad.net",
    "ipv6.am.i.mullvad.net",
    "api.github.com",
    "f-droid.org",
    "repository-images.githubusercontent.com",
    "graph.whatsapp.com",
]

DENYLIST_DOMAINS_PHASE1 = [
    "dls.di.atlas.samsung.com",
    "dc.di.atlas.samsung.com",
    "dls-udc.dqa.samsung.com",
    "crashlyticsreports-pa.googleapis.com",
    "ad.doubleclick.net",
    "example.org",  # Temporary - investigate source
    "gos-api.gos-gsp.io",
    "1.ssiloc.com",
    "fdownloader.net",
]

def add_domains():
    """Add recommended domains to lists"""
    
    allowlist_file = PROJECT_ROOT / "baseline" / "baseline-roots.txt"
    denylist_file = PROJECT_ROOT / "baseline" / "denylist.txt"
    
    # Load existing domains
    def load_existing(filepath):
        existing = set()
        if filepath.exists():
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        existing.add(line.lower())
        return existing
    
    existing_allowlist = load_existing(allowlist_file)
    existing_denylist = load_existing(denylist_file)
    
    print("="*60)
    print("MANUAL DOMAIN UPDATER")
    print("="*60)
    
    # Add to allowlist
    added_allowlist = []
    for domain in WHITELIST_DOMAINS:
        if domain.lower() not in existing_allowlist:
            with open(allowlist_file, 'a') as f:
                f.write(f"{domain}\n")
            added_allowlist.append(domain)
            existing_allowlist.add(domain.lower())
    
    # Add to denylist
    added_denylist = []
    for domain in DENYLIST_DOMAINS_PHASE1:
        if domain.lower() not in existing_denylist:
            with open(denylist_file, 'a') as f:
                f.write(f"{domain}\n")
            added_denylist.append(domain)
            existing_denylist.add(domain.lower())
    
    # Report
    print(f"\n✅ Added to allowlist ({len(added_allowlist)} domains):")
    for domain in added_allowlist:
        print(f"  • {domain}")
    
    print(f"\n✅ Added to denylist ({len(added_denylist)} domains):")
    for domain in added_denylist:
        print(f"  • {domain}")
    
    # Check for conflicts
    conflicts = existing_allowlist.intersection(existing_denylist)
    if conflicts:
        print(f"\n⚠️  WARNING: {len(conflicts)} domains in BOTH lists!")
        for domain in sorted(conflicts):
            print(f"  • {domain}")
    
    # Final counts
    print(f"\n📊 Final counts:")
    print(f"  • Allowlist: {len(existing_allowlist)} domains")
    print(f"  • Denylist: {len(existing_denylist)} domains")
    
    # Update changelog
    update_changelog(added_allowlist, added_denylist)

def update_changelog(added_allowlist, added_denylist):
    """Update CHANGELOG.md with changes"""
    changelog_file = PROJECT_ROOT / "CHANGELOG.md"
    
    entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} - Manual Domain Update

### ✅ Domains Added

#### Allowlist ({len(added_allowlist)} domains)
"""
    
    for domain in added_allowlist:
        entry += f"- `{domain}`\n"
    
    entry += f"""
#### Denylist ({len(added_denylist)} domains)
"""
    
    for domain in added_denylist:
        entry += f"- `{domain}`\n"
    
    entry += """
### 📝 Notes
- Added essential services to allowlist based on investigation
- Added telemetry domains to denylist (Phase 1)
- `example.org` added temporarily while investigating source

---
"""
    
    if changelog_file.exists():
        content = changelog_file.read_text()
        # Insert after first header
        if "## " in content:
            parts = content.split("## ", 1)
            new_content = parts[0] + entry + "## " + parts[1]
            changelog_file.write_text(new_content)
        else:
            changelog_file.write_text(entry + content)
    else:
        changelog_file.write_text(entry)
    
    print(f"\n📝 Changes logged to: {changelog_file}")

if __name__ == "__main__":
    from datetime import datetime
    add_domains()
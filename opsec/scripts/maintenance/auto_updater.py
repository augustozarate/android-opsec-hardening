"""
Auto Updater for OPSEC Lists
Applies ONLY human-approved actions to allowlist / denylist.
Supports --dry-run for CI and safe previews.
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================
# CONFIGURATION
# ============================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASELINE_DIR = PROJECT_ROOT / "baseline"
REPORTS_DIR = PROJECT_ROOT / "reports"
BACKUP_DIR = PROJECT_ROOT / "backups"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"

ALLOWLIST_FILE = BASELINE_DIR / "baseline-roots.txt"
DENYLIST_FILE = BASELINE_DIR / "denylist.txt"
CRITICAL_FILE = BASELINE_DIR / "critical-services.txt"

APPROVED_ACTIONS_FILE = REPORTS_DIR / "approved_actions.txt"

# ============================================
# HELPERS
# ============================================
def load_domains_from_file(filepath):
    if not filepath.exists():
        return set()

    domains = set()
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                domain = line.split("#")[0].strip().lower()
                if domain:
                    domains.add(domain)
    return domains


def save_domains_to_file(filepath, domains, comment):
    BACKUP_DIR.mkdir(exist_ok=True)

    if filepath.exists():
        backup = BACKUP_DIR / f"{filepath.name}.{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.bak"
        backup.write_text(filepath.read_text())

    domains = sorted(set(domains))

    with open(filepath, "w") as f:
        f.write(f"# {comment}\n")
        f.write(f"# Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"# Total: {len(domains)} domains\n\n")
        for d in domains:
            f.write(f"{d}\n")

    return len(domains)


def parse_approved_actions(filepath):
    """
    Expected format:
    domain | ALLOWLIST | reason | source
    domain | DENYLIST  | reason | source
    """
    actions = defaultdict(list)

    if not filepath.exists():
        print(f"[!] approved_actions.txt not found: {filepath}")
        return actions

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue

            domain = parts[0].lower()
            action = parts[1].upper()

            if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", domain):
                continue

            if action == "ALLOWLIST":
                actions["allowlist"].append(domain)
            elif action == "DENYLIST":
                actions["denylist"].append(domain)

    return actions


def log_changes(title, added, skipped, conflicts):
    CHANGELOG_FILE.parent.mkdir(exist_ok=True)

    if CHANGELOG_FILE.exists():
        log = CHANGELOG_FILE.read_text()
    else:
        log = "# OPSEC CHANGELOG\n\n"

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    log += f"## {ts} — {title}\n\n"

    if added:
        log += f"### ✅ Added ({len(added)})\n"
        for d in sorted(added):
            log += f"- `{d}`\n"
        log += "\n"

    if skipped:
        log += f"### ⏭️ Skipped ({len(skipped)})\n"
        for d in sorted(skipped):
            log += f"- `{d}`\n"
        log += "\n"

    if conflicts:
        log += f"### ⚠️ Conflicts ({len(conflicts)})\n"
        for d, reason in conflicts:
            log += f"- `{d}` ({reason})\n"
        log += "\n"

    log += "---\n\n"
    CHANGELOG_FILE.write_text(log)


# ============================================
# CORE UPDATE LOGIC
# ============================================
def update_from_approved_actions(dry_run=False):
    print("=" * 60)
    print("AUTO-UPDATER — APPROVED ACTIONS ONLY")
    if dry_run:
        print("🧪 DRY-RUN MODE ENABLED (no files will be modified)")
    print("=" * 60)

    actions = parse_approved_actions(APPROVED_ACTIONS_FILE)
    if not actions:
        print("[!] No approved actions found")
        return False

    allow_current = load_domains_from_file(ALLOWLIST_FILE)
    deny_current = load_domains_from_file(DENYLIST_FILE)

    added, skipped, conflicts = [], [], []

    # ---- ALLOWLIST ----
    for domain in set(actions.get("allowlist", [])):
        if domain in deny_current:
            conflicts.append((domain, "present in denylist"))
        elif domain in allow_current:
            skipped.append(domain)
        else:
            allow_current.add(domain)
            added.append(f"{domain} (allowlist)")

    # ---- DENYLIST ----
    for domain in set(actions.get("denylist", [])):
        if domain in allow_current:
            conflicts.append((domain, "present in allowlist"))
        elif domain in deny_current:
            skipped.append(domain)
        else:
            deny_current.add(domain)
            added.append(f"{domain} (denylist)")

    if dry_run:
        print("\n🧪 DRY-RUN PREVIEW")
    else:
        if added:
            save_domains_to_file(
                ALLOWLIST_FILE,
                allow_current,
                "Core / required services"
            )
            save_domains_to_file(
                DENYLIST_FILE,
                deny_current,
                "Telemetry / tracking / ads"
            )

            log_changes(
                "Apply approved_actions.txt",
                added,
                skipped,
                conflicts
            )

    print("\n📊 Summary")
    print(f"  Added:     {len(added)}")
    print(f"  Skipped:   {len(skipped)}")
    print(f"  Conflicts: {len(conflicts)}")

    if dry_run:
        print("\n✔ Dry-run completed (no changes written)")
    else:
        print("\n✔ Update completed safely")

    return True


def show_stats():
    allowlist = load_domains_from_file(ALLOWLIST_FILE)
    denylist = load_domains_from_file(DENYLIST_FILE)
    critical = load_domains_from_file(CRITICAL_FILE) if CRITICAL_FILE.exists() else set()

    print("=" * 60)
    print("OPSEC LIST STATISTICS")
    print("=" * 60)
    print(f"Allowlist: {len(allowlist)}")
    print(f"Denylist:  {len(denylist)}")
    print(f"Critical:  {len(critical)}")

    dupes = allowlist & denylist
    if dupes:
        print("\n⚠️ WARNING: Domains in BOTH lists")
        for d in sorted(list(dupes))[:5]:
            print(f" - {d}")


# ============================================
# CLI
# ============================================
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OPSEC allow/deny updater (approved actions only)"
    )
    parser.add_argument("--update", action="store_true", help="Apply approved_actions.txt")
    parser.add_argument("--stats", action="store_true", help="Show list stats")
    parser.add_argument("--dry-run", action="store_true", help="Simulate changes only")

    args = parser.parse_args()

    BASELINE_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    if args.update:
        update_from_approved_actions(dry_run=args.dry_run)
    elif args.stats:
        show_stats()
    else:
        parser.print_help()
        show_stats()


if __name__ == "__main__":
    main()

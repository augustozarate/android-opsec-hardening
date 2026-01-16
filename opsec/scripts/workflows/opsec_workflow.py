"""
Complete OPSEC Workflow Script
Runs the entire process from DNS analysis to list updates
"""

import subprocess
import sys
from pathlib import Path

# opsec/scripts/
SCRIPTS_ROOT = Path(__file__).resolve().parents[1]

def run_command(command, description, cwd):
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print("\n--- STDOUT ---")
                print(result.stdout)
            return True

        else:
            print(f"❌ {description} failed (exit code {result.returncode})")
            print("\n--- STDOUT ---")
            print(result.stdout)
            print("\n--- STDERR ---")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out")
        return False
    except Exception as e:
        print(f"💥 {description} crashed: {e}")
        return False


def run_script(relative_path, args=None, description=None):
    script_path = (SCRIPTS_ROOT / relative_path).resolve()

    if not script_path.exists():
        print(f"[!] Script not found: {script_path}")
        return False

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args.split())

    return run_command(
        cmd,
        description or f"Run {relative_path}",
        cwd=script_path.parent
    )


def full_workflow():
    print("🚀 OPSEC COMPLETE WORKFLOW")
    print("=" * 60)

    steps = [
        ("analysis/dns_review_tool_enhanced.py", None, "1. Generate DNS Analysis Report"),
        ("analysis/extract_unknowns.py", None, "2. Extract Unknown Domains"),
        ("investigation/domain_investigator.py", None, "3. Investigate Unknown Domains"),
        ("maintenance/auto_updater.py", "--update", "4. Auto-update Allow/Deny lists"),
        ("maintenance/auto_updater.py", "--stats", "5. Show Statistics"),
    ]

    completed = 0
    for script, args, desc in steps:
        if run_script(script, args, desc):
            completed += 1
        else:
            print(f"\n⚠️ Workflow stopped at: {desc}")
            break

    print(f"\n{'='*60}")
    print("WORKFLOW COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Steps completed: {completed}/{len(steps)}")

    if completed == len(steps):
        print("\n🎉 OPSEC workflow completed successfully")
    else:
        print("\n⚠️ Some steps failed — see output above")


def quick_update():
    run_script("maintenance/auto_updater.py", "--update", "Quick update")
    run_script("maintenance/auto_updater.py", "--stats", "Statistics")


def cleanup():
    reports = SCRIPTS_ROOT.parent / "reports"
    backups = SCRIPTS_ROOT.parent / "backups"

    print("🧹 Cleanup")

    for folder in [reports, backups]:
        if folder.exists():
            for f in folder.glob("*.backup"):
                f.unlink()
                print(f"Removed {f.name}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OPSEC Workflow Manager")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--cleanup", action="store_true")

    args = parser.parse_args()

    if args.full:
        full_workflow()
    elif args.quick:
        quick_update()
    elif args.cleanup:
        cleanup()
    else:
        print("Usage:")
        print("  python workflows/opsec_workflow.py --full")
        print("  python workflows/opsec_workflow.py --quick")
        print("  python workflows/opsec_workflow.py --cleanup")

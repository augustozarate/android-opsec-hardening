"""
Clean corrupted baseline files
"""

from pathlib import Path
import re

BASELINE_DIR_NAME = "baseline"

def find_project_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / BASELINE_DIR_NAME).exists():
            return parent
    raise RuntimeError("Project root not found (baseline directory missing)")

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = find_project_root(SCRIPTS_DIR)
print(f"[DEBUG] Project root: {PROJECT_ROOT}")

def clean_baseline_roots():
    """Clean baseline-roots.txt from Python code"""
    filepath = PROJECT_ROOT / "baseline" / "baseline-roots.txt"
    
    if not filepath.exists():
        print(f"[!] File not found: {filepath}")
        return
    
    content = filepath.read_text()
    
    # Find where Python code starts
    python_start = content.find('# Essential Services"""')
    if python_start == -1:
        print("[+] File appears clean, no Python code found")
        return
    
    # Keep only the part before Python code
    clean_content = content[:python_start].strip()
    
    # Backup original
    backup = filepath.with_suffix('.txt.backup')
    filepath.rename(backup)
    print(f"[+] Original backed up to: {backup.name}")
    
    # Save cleaned version
    filepath.write_text(clean_content)
    print(f"[+] Cleaned file saved. Lines: {len(clean_content.splitlines())}")
    
    # Show first few lines
    print("\nFirst 10 lines of cleaned file:")
    for i, line in enumerate(clean_content.splitlines()[:10], 1):
        print(f"{i:3}: {line}")

def clean_denylist():
    """Clean denylist.txt from Python code"""
    filepath = PROJECT_ROOT / "baseline" / "denylist.txt"
    
    if not filepath.exists():
        print(f"[!] File not found: {filepath}")
        return
    
    content = filepath.read_text()
    
    # Find where Python code starts
    python_start = content.find('# --- Add sample domains for denylist ---')
    if python_start == -1:
        print("[+] File appears clean, no Python code found")
        return
    
    # Keep only the part before Python code
    clean_content = content[:python_start].strip()
    
    # Backup original
    backup = filepath.with_suffix('.txt.backup')
    filepath.rename(backup)
    print(f"[+] Original backed up to: {backup.name}")
    
    # Save cleaned version
    filepath.write_text(clean_content)
    print(f"[+] Cleaned file saved. Lines: {len(clean_content.splitlines())}")

def check_for_duplicates():
    """Check for domains in both lists"""
    allowlist_file = PROJECT_ROOT / "baseline" / "baseline-roots.txt"
    denylist_file = PROJECT_ROOT / "baseline" / "denylist.txt"
    
    def load_domains(filepath):
        if not filepath.exists():
            return set()
        domains = set()
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    domains.add(line.lower())
        return domains
    
    allowlist = load_domains(allowlist_file)
    denylist = load_domains(denylist_file)
    
    duplicates = allowlist.intersection(denylist)
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} domains in BOTH lists:")
        for domain in sorted(duplicates):
            print(f"  • {domain}")
        
        # Suggest which list to remove from
        print("\n🎯 Recommendation: Remove from denylist (more restrictive)")
        return list(duplicates)
    
    print("\n✅ No duplicates found between lists")
    return []

def main():
    print("="*60)
    print("CLEAN CORRUPTED FILES")
    print("="*60)
    
    # Clean files
    print("\n[1] Cleaning baseline-roots.txt...")
    clean_baseline_roots()
    
    print("\n[2] Cleaning denylist.txt...")
    clean_denylist()
    
    print("\n[3] Checking for duplicates...")
    duplicates = check_for_duplicates()
    
    print("\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
    
    if duplicates:
        print("\n🚨 MANUAL ACTION NEEDED:")
        print("Remove these domains from ONE list (recommend denylist):")
        for domain in duplicates:
            print(f"  {domain}")

if __name__ == "__main__":
    main()
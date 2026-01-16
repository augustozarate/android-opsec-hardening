"""
Extract unknown domains from OPSEC report
"""

import re
from pathlib import Path

def extract_unknown_domains(report_file):
    """Extract domains from the Unknown section of the report"""
    
    content = Path(report_file).read_text()
    
    # Find the Unknown section
    unknown_section = re.search(
        r'## ❓ Unknown / Requires Review.*?(?=## |\Z)', 
        content, 
        re.DOTALL
    )
    
    if not unknown_section:
        print("[!] Could not find Unknown section in report")
        return []
    
    section_text = unknown_section.group(0)
    
    # Extract domains with pattern: `domain` → count
    domains = re.findall(r'`([a-zA-Z0-9._-]+)`', section_text)
    
    # Remove duplicates and sort
    unique_domains = sorted(list(set(domains)))
    
    print(f"[+] Found {len(unique_domains)} unique domains in Unknown section")
    return unique_domains

def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    report_file = PROJECT_ROOT / "reports" / "opsec-report-enhanced.md"
    
    if not report_file.exists():
        print(f"[!] Report file not found: {report_file}")
        print("[!] Looking for alternative reports...")
        
        # Try to find any report
        reports_dir = PROJECT_ROOT / "reports"
        report_files = list(reports_dir.glob("*.md"))
        
        if report_files:
            report_file = report_files[0]
            print(f"[+] Using found report: {report_file.name}")
        else:
            print("[!] No report files found in reports/ directory")
            return
    
    domains = extract_unknown_domains(report_file)
    
    if not domains:
        print("[!] No domains extracted. Check report format.")
        return
    
    # Save to file
    output_file = PROJECT_ROOT / "reports" / "unknown_domains_report.txt"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# Domains extracted from Unknown section\n")
        f.write(f"# Source: {report_file.name}\n")
        f.write(f"# Extracted: {len(domains)} domains\n\n")
        for domain in domains:
            f.write(f"{domain}\n")
    
    print(f"[+] Saved {len(domains)} domains to: {output_file}")
    
    # Show statistics
    print("\n📊 Domain Statistics:")
    print(f"  Total domains: {len(domains)}")
    
    # Count by TLD
    tld_counts = {}
    for domain in domains:
        parts = domain.split('.')
        if len(parts) >= 2:
            tld = parts[-1]
            tld_counts[tld] = tld_counts.get(tld, 0) + 1
    
    print(f"  Top TLDs: {', '.join([f'{tld}({count})' for tld, count in sorted(tld_counts.items(), key=lambda x: x[1], reverse=True)[:5]])}")
    
    # Show top 10 domains
    print("\n🔍 Top 10 domains to investigate:")
    for i, domain in enumerate(domains[:10], 1):
        print(f"  {i:2}. {domain}")

if __name__ == "__main__":
    main()
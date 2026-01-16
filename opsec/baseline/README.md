# Baseline Lists – OPSEC

This directory contains the **core DNS policy files** used by the OPSEC workflow.

## Files

- **baseline-roots.txt**
  Essential domains that must always be allowed.
  Blocking these may break core system functionality.

- **denylist.txt**
  Telemetry, ads, analytics, and unwanted services.
  Domains here are blocked intentionally.

- **critical-services.txt**
  Domains detected as critical during analysis.
  Review carefully before blocking.

- **phantom-tlds.txt**
  Fake or sinkhole TLDs used to detect misconfigurations or malware.

## Rules

- One domain per line
- No wildcards
- Comments start with `#`
- All domains must be lowercase

⚠️ Changes here directly affect system behavior.

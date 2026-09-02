# Android OPSEC Hardening — Documentation Index

**Document ID:** DOC-0001  
**Version:** 1.1  
**Status:** Published  
**Last Updated:** 2026-08-31

---

## 1. Purpose

This document provides the primary index for the technical documentation of the Android OPSEC Hardening project.

The project follows an evidence-oriented security engineering approach.

Documentation is organized according to its purpose:

```
Architecture
     ↓
Configuration
     ↓
Validation
     ↓
Evidence
     ↓
Operational Knowledge
```

Not every documented configuration is considered validated.

Validation status is defined by the corresponding validation report and its documented scope.

---

## 2. Documentation Structure

The current documentation tree is organized as follows:

```
docs/
├── rethink/
│   ├── architecture/
│   ├── guides/
│   ├── references/
│   ├── validation/
│   │   └── evidence/
│   └── README.md
│
├── CONTRIBUTING.md
├── Documentation-Index.md
└── README.md
```

Additional operational project components exist outside `docs/`, including:

```
devices/
nextdns/
opsec/
screenshots/
```

These directories contain device-specific information, filtering policies, OPSEC tooling, datasets, case studies, and supporting project resources.

---

# 3. RethinkDNS Documentation

RethinkDNS is treated as a network-control component within the Android OPSEC Hardening architecture.

Its documentation is located under:

```
docs/rethink/
```

Entry point:

[`rethink/README.md`](rethink/README.md)

The module is divided into:

```
architecture/
guides/
references/
validation/
```

---

## 3.1 Architecture

Architecture documents describe how RethinkDNS interacts with Android applications, DNS resolution, firewall policies, WireGuard proxies, and external network destinations.

### ARCH-001 — RethinkDNS Architecture

[`rethink/architecture/ARCH-001-rethinkdns-architecture.md`](rethink/architecture/ARCH-001-rethinkdns-architecture.md)

Defines the base RethinkDNS architecture used by the project.

**State:** Documented

### ARCH-002 — Traffic Flow

[`rethink/architecture/ARCH-002-traffic-flow.md`](rethink/architecture/ARCH-002-traffic-flow.md)

Documents how application traffic moves through the RethinkDNS architecture.

**State:** Documented

---

## 3.2 Validation

Validation documents contain reproducible tests used to determine whether the architecture behaves as expected.

### VAL-001 — DNS Validation

[`rethink/validation/VAL-001-dns-validation.md`](rethink/validation/VAL-001-dns-validation.md)

Validates DNS behavior within the tested RethinkDNS configuration.

### VAL-002 — Network Transition & WireGuard Routing Validation

[`rethink/validation/VAL-002-network-transition-wireguard-routing.md`](rethink/validation/VAL-002-network-transition-wireguard-routing.md)

Validates application routing during WireGuard proxy transitions.

Observed transition:

```
wg16 → wg17 → wg16
```

Additional observations include:

- TCP/443 routing
- UDP/443 routing
- HTTP/3-associated traffic
- Firewall persistence
- DNS continuity
- Observable routing conflicts
- Observable DNS fallback

**Result:** PASS  
**State:** CLOSED / VALIDATED

Supporting evidence:

```
rethink/validation/evidence/VAL-002/
```

### VAL-003 — Version Regression & Upgrade Validation

[`rethink/validation/VAL-003-version-regression-upgrade-validation.md`](rethink/validation/VAL-003-version-regression-upgrade-validation.md)

Tracks RethinkDNS behavior across software upgrades and potential regressions.

The validation state should be determined independently for each tested upgrade or regression scenario.

---

## 3.3 Configuration Guides

### RethinkDNS Configuration Recommendations

[`rethink/guides/configuration-recommendations.md`](rethink/guides/configuration-recommendations.md)

Provides configuration recommendations covering:

- Encrypted DNS
- DNS provider selection
- Split DNS
- WireGuard routing
- Firewall policies
- Application-specific routing
- HTTP/3 and UDP/443
- Network monitoring
- Upgrade validation
- Evidence sanitization

Recommendations should be interpreted according to the documented threat model and test environment.

---

## 3.4 References

### Recommended Blocklists

[`rethink/references/recommended-blocklists.md`](rethink/references/recommended-blocklists.md)

Documents the filtering strategy and blocklists evaluated for the project.

The project favors auditable filtering policies over enabling large numbers of overlapping blocklists.

---

# 4. NextDNS

NextDNS-specific policies are maintained separately from the general RethinkDNS architecture.

```
nextdns/
├── allowlists/
├── blocklists/
└── README.md
```

This separation is intentional.

RethinkDNS may operate with different encrypted DNS providers, while the `nextdns/` directory contains configuration material specifically associated with NextDNS.

---

# 5. OPSEC

Operational security resources are located under:

```
opsec/
```

Current categories include:

```
baseline/
case-studies/
data/
scripts/
```

These resources support investigation, DNS analysis, maintenance, automation, and real-world security case studies.

See:

[`../opsec/README.md`](../opsec/README.md)

---

# 6. Device Documentation

Device-specific configuration and compatibility information is located under:

```
devices/
```

Current device documentation includes:

```
devices/samsung-a50-a505g/
```

Device documentation should distinguish device-specific behavior from general architectural behavior.

---

# 7. Documentation Categories

The project recognizes the following document categories.

| Category | Identifier | Purpose |
|---|---|---|
| Documentation | `DOC-XXXX` | Project documentation indexes and standards |
| Architecture | `ARCH-XXX` | System design and component interaction |
| Validation | `VAL-XXX` | Reproducible security and functional validation |
| Engineering Notes | `EN-XXXX` | Investigations and experimental findings |
| Architecture Decisions | `ADR-XXXX` | Significant architectural decisions |
| Standard Procedures | `SOP-XXXX` | Repeatable operational procedures |
| Case Studies | `CS-XXXX` | Real deployment or investigation scenarios |
| Knowledge Base | `KB-XXXX` | Technical concepts and reference material |

Not every category must have documents at all times.

Categories may be introduced as the project evolves.

---

# 8. Validation Model

The project distinguishes between configuration and validation.

```
Configured
    !=
Validated
```

A configuration is considered validated only within the scope and conditions documented by its corresponding validation report.

Possible validation results include:

```
PASS
FAIL
PARTIAL
INCONCLUSIVE
NOT TESTED
```

Observations such as:

```
NOT OBSERVED
```

should not automatically be interpreted as proof that a behavior is impossible.

---

# 9. Evidence

Validation evidence should be stored close to the corresponding validation documentation.

Example:

```
rethink/
└── validation/
    ├── evidence/
    │   └── VAL-002/
    │       ├── VAL-002-E01-...
    │       ├── VAL-002-E02-...
    │       └── ...
    │
    └── VAL-002-network-transition-wireguard-routing.md
```

Evidence may include:

- Screenshots
- Logs
- Sanitized configuration extracts
- Packet captures
- Test output
- Reproducible command output

Public evidence must not expose secrets or unnecessary personal information.

---

# 10. Documentation Lifecycle

Technical documentation follows the general lifecycle:

```
Draft
  |
  v
Under Review
  |
  v
Validated
  |
  v
Published
  |
  +----> Deprecated
  |
  +----> Archived
```

A document may be published without implying that every configuration described within it has been universally validated.

Validation always applies to the documented scope.

---

# 11. Versioning

Documentation versions are independent from software versions.

For example:

```
Document:
VAL-002 v1.0

Test environment:
RethinkDNS v0.5.6
Android 13
LineageOS 20
WireGuard routing
Encrypted DNS
```

When behavior depends on a specific software release, the tested version should be explicitly recorded.

---

# 12. Contribution Standards

Contribution requirements are documented in:

[`CONTRIBUTING.md`](CONTRIBUTING.md)

Contributions should prioritize:

- Evidence over assumptions
- Reproducibility
- Explicit limitations
- Security trade-off documentation
- Sensitive-data minimization
- Validation before recommendation

---

# 13. Current Documentation State

```
RethinkDNS
├── Architecture
│   ├── ARCH-001        DOCUMENTED
│   └── ARCH-002        DOCUMENTED
│
├── Validation
│   ├── VAL-001         DNS VALIDATION
│   ├── VAL-002         CLOSED / VALIDATED
│   └── VAL-003         REGRESSION TRACK
│
├── Guides
│   └── Configuration   DOCUMENTED
│
└── References
    └── Blocklists      DOCUMENTED
```

The documentation structure is expected to evolve as additional validation, device testing, and operational procedures are added.

---

End of document.

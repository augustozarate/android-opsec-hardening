# Android OPSEC Hardening

**Practical Android privacy, network hardening, validation, and OPSEC research.**

Android OPSEC Hardening is an evidence-oriented project for designing, testing, and documenting privacy and network-security configurations on real Android devices.

The project combines:

- RethinkDNS network control
- Encrypted DNS
- DNS filtering
- WireGuard routing
- Application-level firewall policies
- Application isolation
- Network observability
- OPSEC analysis and automation
- Real-world security investigations

The objective is not to create a single "perfect" Android configuration.

The objective is to build a **reproducible security engineering reference** that documents:

```
What is configured
        ↓
Why it is configured
        ↓
How it is tested
        ↓
What was observed
        ↓
Where it may fail
```

---

## Core Philosophy

The project follows several principles:

- **Evidence over assumptions**
- **Reproducibility over personal preference**
- **Defense in depth**
- **Validation before recommendation**
- **Explicit documentation of limitations**
- **Privacy without unnecessarily breaking usability**
- **Rootless-first when practical**
- **Version-aware testing**

A central rule of the project is:

```
Configured
    !=
Validated
```

A security feature is not considered validated simply because it is enabled or appears to work.

Where practical, expected behavior is verified through controlled testing, logs, network observations, external verification, and supporting evidence.

---

## Objectives

The project aims to:

- Reduce unnecessary telemetry and tracking.
- Control application network access.
- Encrypt DNS resolution.
- Validate DNS resolver behavior.
- Route selected applications through privacy-oriented VPN tunnels.
- Apply per-application firewall and routing policies.
- Investigate unexpected network activity.
- Preserve Android usability while improving privacy.
- Document successful and unsuccessful configurations.
- Detect regressions introduced by software upgrades.
- Build reproducible OPSEC workflows and analysis tools.

---

# Project Architecture

The project follows a layered model.

```
                    Android Device
                         |
                         v
                  Applications
                         |
              +----------+----------+
              |                     |
              v                     v
       Application             Work Profile /
       Permissions              Isolation
              |                     |
              +----------+----------+
                         |
                         v
                    RethinkDNS
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          Firewall      DNS       WireGuard
                         |           |
                         v           v
                 Encrypted DNS      VPN
                 Provider(s)      Routing
                         \           /
                          \         /
                           v       v
                            Internet
```

Additional OPSEC tooling analyzes DNS activity, domains, security events, and real-world incidents outside the device itself.

---

# Repository Structure

```
android-opsec-hardening/
├── devices/
│   └── samsung-a50-a505g/
│       ├── configs/
│       └── README.md
│
├── docs/
│   ├── rethink/
│   │   ├── architecture/
│   │   ├── guides/
│   │   ├── references/
│   │   ├── validation/
│   │   │   └── evidence/
│   │   └── README.md
│   │
│   ├── CONTRIBUTING.md
│   ├── Documentation-Index.md
│   └── README.md
│
├── nextdns/
│   ├── allowlists/
│   ├── blocklists/
│   └── README.md
│
├── opsec/
│   ├── baseline/
│   ├── case-studies/
│   ├── data/
│   ├── scripts/
│   │   ├── analysis/
│   │   ├── investigation/
│   │   ├── maintenance/
│   │   └── workflows/
│   ├── CHANGELOG.md
│   └── README.md
│
├── screenshots/
│   └── README.md
│
├── CHANGELOG.md
├── .gitignore
├── LICENSE
└── README.md
```

---

# Documentation

The technical documentation is located under:

[`docs/`](./docs/)

Start with:

**[Documentation Index](./docs/Documentation-Index.md)**

The documentation index describes:

- Architecture documents
- Validation reports
- Configuration guides
- Evidence
- Engineering documentation
- Documentation lifecycle
- Contribution standards

Documentation and validation are deliberately separated.

A documented configuration is not automatically considered validated.

---

# RethinkDNS Architecture

RethinkDNS is treated as a **network-control component**, not simply as an Android application.

The RethinkDNS documentation module is located at:

**[RethinkDNS Documentation](./docs/rethink/README.md)**

Current documentation includes:

```
Architecture
├── ARCH-001 — RethinkDNS Architecture
└── ARCH-002 — Traffic Flow

Validation
├── VAL-001 — DNS Validation
├── VAL-002 — Network Transition & WireGuard Routing Validation
└── VAL-003 — Version Regression & Upgrade Validation

Guides
└── Configuration Recommendations

References
└── Recommended Blocklists
```

---

## RethinkDNS Validation

The project performs controlled validation instead of assuming that configured routing policies behave correctly.

### VAL-001 — DNS Validation

Tests DNS behavior within the RethinkDNS architecture.

**[Read VAL-001](./docs/rethink/validation/VAL-001-dns-validation.md)**

---

### VAL-002 — Network Transition & WireGuard Routing

VAL-002 validates application routing during WireGuard proxy transitions.

Observed routing sequence:

```
wg16
  ↓
wg17
  ↓
wg16
```

The validation also examined:

- TCP/443 routing
- UDP/443 routing
- HTTP/3-associated traffic
- Firewall persistence
- DNS continuity
- Observable simultaneous routing
- Observable application proxy bypass
- DNS fallback behavior

Supporting evidence is stored under:

```
docs/rethink/validation/evidence/VAL-002/
```

**Result:** `PASS`
**State:** `CLOSED / VALIDATED`

**[Read VAL-002](./docs/rethink/validation/VAL-002-network-transition-wireguard-routing.md)**

The result applies only to the documented test conditions.

It does **not** constitute packet-level proof that zero packets can escape during every possible network transition.

---

### VAL-003 — Version Regression & Upgrade Validation

RethinkDNS upgrades are treated as potential regression boundaries.

VAL-003 tracks behavior that may change between application versions, including:

- DNS handling
- WireGuard startup
- Proxy assignment
- Firewall enforcement
- Network transitions
- Application routing

**[Read VAL-003](./docs/rethink/validation/VAL-003-version-regression-upgrade-validation.md)**

Its validation state is maintained independently from VAL-001 and VAL-002.

---

# DNS Strategy

The architecture is **DNS-provider independent**.

Encrypted DNS providers used or evaluated by the project include:

- NextDNS
- modDNS

Supported strategies may use:

```
DNS-over-HTTPS (DoH)
DNS-over-TLS   (DoT)
```

The project treats DNS filtering and WireGuard routing as separate architectural layers.

```
                         +---- NextDNS
                         |
Apps → RethinkDNS → DNS -+---- modDNS
        |                |
        |                +---- Other compatible resolver
        |
        +---- Firewall
        |
        +---- WireGuard
```

Successful web browsing alone is not considered proof that the intended DNS resolver is being used.

DNS behavior should be validated through observable resolver activity.

---

# NextDNS

NextDNS-specific policies remain under:

[`nextdns/`](./nextdns/)

```
nextdns/
├── allowlists/
├── blocklists/
└── README.md
```

These resources contain project-specific filtering and compatibility rules.

The separation between `nextdns/` and `docs/rethink/` is intentional:

- `docs/rethink/` documents the general network architecture.
- `nextdns/` contains NextDNS-specific policy material.

RethinkDNS does not require NextDNS to function as the network-control layer.

---

# Blocklist Strategy

The project favors auditable filtering over enabling large numbers of overlapping blocklists.

A preferred model is:

```
Balanced privacy filtering
          +
Security protections
          +
Targeted OPSEC rules
          +
Minimal allowlisting
```

rather than stacking multiple aggressive lists without understanding their interactions.

See:

**[Recommended Blocklists](./docs/rethink/references/recommended-blocklists.md)**

Filtering decisions should be based on observed behavior and technical purpose rather than vendor ownership alone.

---

# VPN & WireGuard

The architecture is not tied to a single VPN provider.

Privacy-oriented providers used or evaluated by the project include:

- Mullvad
- IVPN
- Proton VPN

Relevant criteria include:

- WireGuard support
- Privacy policy
- Independent security audits
- Minimal telemetry
- Stable Android support
- Standard WireGuard configuration support when required

Provider reputation does not by itself validate the local routing architecture.

Traffic paths should still be tested.

---

# Firewall Strategy

RethinkDNS provides the primary application-level network policy layer within the documented architecture.

Firewall policies can be used to:

- Restrict unnecessary network access.
- Block unwanted outbound traffic.
- Prevent insecure HTTP where compatible.
- Investigate unexpected application destinations.
- Apply application-specific network controls.

During VAL-002, the configured insecure HTTP policy was observed blocking TCP/80 traffic while the WireGuard transition tests were being performed.

This observation applies to the tested configuration.

---

# Application Isolation

Network hardening is only one layer of the project.

Application isolation may additionally use Android work profiles and permission controls.

The general model is:

```
Application
    |
    +---- Permission restrictions
    |
    +---- Work-profile isolation
    |
    +---- Firewall policy
    |
    +---- DNS policy
    |
    +---- WireGuard routing
```

Not every application requires the same policy.

Configuration should reflect the application's purpose and the relevant threat model.

---

# Device Case Studies

Device-specific behavior is maintained separately from general architecture.

Current device:

## Samsung Galaxy A50 — SM-A505G

**[Device Documentation](./devices/samsung-a50-a505g/README.md)**

Device documentation may include:

- ROM compatibility
- Network behavior
- Application isolation
- RethinkDNS compatibility
- DNS configuration
- VPN integration
- Troubleshooting
- Device-specific limitations

Behavior observed on one Android device should not automatically be assumed to apply to another.

---

# OPSEC Automation & Analysis

The `opsec/` module contains analysis and automation resources.

```
opsec/
├── baseline/
├── case-studies/
├── data/
└── scripts/
    ├── analysis/
    ├── investigation/
    ├── maintenance/
    └── workflows/
```

Current tooling includes functionality for:

- DNS review
- Unknown-domain extraction
- Domain investigation
- Baseline maintenance
- Automated updates
- OPSEC workflows

**[OPSEC Documentation](./opsec/README.md)**

---

# Real-World Case Studies

The project also documents security events investigated using its OPSEC methodology.

These are separated from device hardening case studies.

Current example:

**[Contabo / Roundcube Phishing Investigation](./opsec/case-studies/2026-08-phishing-contabo-roundcube.md)**

The investigation documents correlation between multiple security sources and a detection false-negative scenario.

Case studies may contain successful detections, false positives, false negatives, unexpected behavior, or vendor-response observations.

Negative results are considered useful evidence when properly documented.

---

# Threat Model

## In Scope

The project primarily addresses:

- DNS-level tracking
- Advertising and analytics infrastructure
- Application telemetry
- Unnecessary outbound connectivity
- Privacy risks on untrusted networks
- DNS resolver behavior
- VPN/WireGuard routing behavior
- Application-level network policy
- Configuration regressions
- Suspicious domain investigation

## Out of Scope

The project does not claim protection against:

- Nation-state adversaries
- Baseband compromise
- Hardware implants
- Zero-day exploitation
- Physical device compromise
- Fully compromised operating systems
- Malicious firmware

The project focuses on **defensive hardening and observable network behavior**.

---

# Security Claims

Absolute security claims are intentionally avoided.

For example, instead of:

```
This configuration prevents all DNS leaks.
```

the project prefers:

```
No DNS bypass was observed during the documented validation scenarios.
```

Observed behavior depends on:

- Device
- Android version
- ROM
- RethinkDNS version
- DNS configuration
- VPN configuration
- Network environment
- Test conditions

Stronger claims require correspondingly stronger evidence.

---

# Evidence & Privacy

Public evidence may include:

- Screenshots
- Sanitized logs
- Test output
- Configuration excerpts
- Network observations
- Packet captures where appropriate

Sensitive information must not be committed.

Examples include:

- WireGuard private keys
- VPN credentials
- API tokens
- Authentication credentials
- Personal DNS identifiers
- Personal identifiers
- Backup files containing secrets

Sensitive values should be replaced with explicit placeholders such as:

```
<REDACTED>
```

Technical context should be preserved where possible.

For example:

```
<REDACTED>.dns.example.net:853
```

may preserve useful resolver and transport information without exposing the private identifier.

---

# Validation Model

Validation reports define their expected result, environment, methodology, observations, and limitations.

Possible test results include:

```
PASS
FAIL
PARTIAL
INCONCLUSIVE
NOT TESTED
```

Additional observations may use states such as:

```
NOT OBSERVED
OUT OF SCOPE
```

`NOT OBSERVED` does not mean that a behavior has been proven impossible.

---

# Upgrade & Regression Testing

Network-security components can change behavior between releases.

Important upgrades should therefore follow a process similar to:

```
Known baseline
      |
      v
Backup configuration
      |
      v
Record current state
      |
      v
Install candidate version
      |
      v
Execute validation
      |
      v
Compare with baseline
      |
      v
Accept / Reject / Continue Testing
```

This approach is particularly important for:

- RethinkDNS
- VPN applications
- WireGuard configurations
- DNS resolvers
- Android networking changes
- ROM upgrades

---

# Metrics & Observability

Depending on the validation objective, measurements may include:

- DNS query behavior
- Blocked-domain activity
- Application functionality
- Firewall decisions
- WireGuard proxy attribution
- TCP/UDP behavior
- DNS resolver attribution
- Network transition behavior
- Battery and performance impact

Metrics should be interpreted within their test environment.

A single metric should not be used as proof of overall security.

---

# Contributing

Contributions are welcome when they follow the project's engineering and documentation principles.

Before contributing, read:

**[CONTRIBUTING.md](./docs/CONTRIBUTING.md)**

Contributions should prioritize:

- Reproducible testing
- Evidence-backed claims
- Documentation of failures
- Explicit test environments
- Version information
- Security trade-offs
- Sensitive-data minimization

A failed or inconclusive experiment may still be valuable.

---

# Documentation Lifecycle

Technical documentation generally follows:

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

Documentation versions are independent from software versions.

---

# Current Project Status

| Area | Status |
|---|---|
| RethinkDNS base architecture | 📘 Documented |
| RethinkDNS traffic flow | 📘 Documented |
| DNS validation | ✅ Validation available |
| WireGuard transition validation | ✅ CLOSED / VALIDATED |
| RethinkDNS regression testing | 🧪 Active validation track |
| Configuration guidance | 📘 Documented |
| Blocklist strategy | 📘 Documented |
| NextDNS policies | 🔧 Maintained |
| OPSEC automation | 🔧 Active |
| Security case studies | 🔎 Active |
| Device documentation | 🔧 Active |

The project is continuously evolving as new configurations, software versions, and validation scenarios are tested.

---

# References & Resources

## Project Documentation

- **[Documentation Index](./docs/Documentation-Index.md)**
- **[RethinkDNS Documentation](./docs/rethink/README.md)**
- **[RethinkDNS Configuration Recommendations](./docs/rethink/guides/configuration-recommendations.md)**
- **[Contributing Guidelines](./docs/CONTRIBUTING.md)**

## External Projects

- F-Droid
- microG
- Shelter
- RethinkDNS
- NextDNS
- Mullvad
- IVPN
- Proton VPN

External projects are referenced for interoperability and research.
Their inclusion does not imply endorsement of every feature, configuration, or security claim made by those projects.

---

# Ethical & Legal Notice

This project is intended for:

- Defensive security
- Privacy engineering
- Security research
- Education
- Personal device hardening

It does not promote abuse, unauthorized access, or attacks against third-party systems.

Users are responsible for complying with applicable laws, service agreements, and platform policies.

---

# License

This repository is provided for educational and research purposes.

Use of custom ROMs, unlocked bootloaders, VPN configurations, DNS filtering, or other system modifications may introduce compatibility or security trade-offs.

Privacy and security are not guaranteed.

See:

**[LICENSE](./LICENSE)**

---

# Maintainer

**[@augustozarate](https://github.com/augustozarate)**

Project focus:

**Cybersecurity · Privacy Engineering · Android OPSEC · Network Validation**

---

⭐ If this project is useful, consider starring the repository.

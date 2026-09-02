# RethinkDNS — Android OPSEC Hardening

This directory contains the RethinkDNS networking architecture, configuration guidance, validation reports, and supporting evidence used by the **Android OPSEC Hardening** project.

The objective of this module is to document and empirically validate a privacy-oriented Android network architecture based on:

- RethinkDNS
- DNS encryption
- Application-level firewall policies
- WireGuard proxy routing
- Per-application traffic control
- Network transition handling
- DNS and routing observability

The documentation focuses on reproducible behavior and observed results rather than assuming that a configuration is secure simply because it is enabled.

---

## 1. Module Scope

RethinkDNS acts as the primary network-control layer in the tested Android architecture.

Its responsibilities include:

- Intercepting application network traffic.
- Applying application-level firewall policies.
- Managing encrypted DNS resolution.
- Routing applications through WireGuard proxies.
- Providing per-connection network visibility.
- Supporting different routing policies depending on network state.
- Detecting unexpected traffic behavior through network and DNS logs.

The project separates:

```
Architecture
     ↓
Configuration
     ↓
Validation
     ↓
Evidence
```

This distinction allows configuration decisions to be documented independently from the tests used to validate them.

---

## 2. Directory Structure

```
rethink/
├── architecture/
│   ├── ARCH-001-rethinkdns-architecture.md
│   └── ARCH-002-traffic-flow.md
│
├── validation/
│   ├── evidence/
│   │   └── VAL-002/
│   │       ├── VAL-002-E01-wg16-initial-routing.png
│   │       ├── VAL-002-E02-wg17-transition.png
│   │       ├── VAL-002-E03-wg16-return-routing.png
│   │       ├── VAL-002-E04-http80-firewall-block.png
│   │       ├── VAL-002-E05-http3-udp443-wg17.png
│   │       └── VAL-002-E06-moddns-dot-resolution.png
│   │
│   ├── VAL-001-dns-validation.md
│   ├── VAL-002-network-transition-wireguard-routing.md
│   └── VAL-003-version-regression-upgrade-validation.md
│
├── guides/
│   └── configuration-recommendations.md
│
├── references/
│   └── recommended-blocklists.md
│
└── README.md
```

---

## 3. Architecture Documentation

### ARCH-001 — RethinkDNS Architecture

[`ARCH-001-rethinkdns-architecture.md`](architecture/ARCH-001-rethinkdns-architecture.md)

Defines the base RethinkDNS architecture used by the project.

It documents the relationship between:

- Android applications
- RethinkDNS
- Firewall policies
- DNS resolution
- WireGuard proxies
- External network destinations

This document should be read first.

---

### ARCH-002 — Traffic Flow

[`ARCH-002-traffic-flow.md`](architecture/ARCH-002-traffic-flow.md)

Documents how application traffic moves through the architecture.

The traffic model distinguishes between:

```
Application traffic
        |
        v
    RethinkDNS
        |
        +---- Firewall
        |
        +---- DNS
        |
        +---- WireGuard proxy
                  |
                  v
               Internet
```

The document provides the traffic-flow context required to interpret the validation reports.

---

## 4. Validation Reports

Validation reports use the following identifiers:

```
VAL-XXX
```

Each validation report defines:

- Objective
- Test environment
- Methodology
- Observed behavior
- Evidence
- Limitations
- Result

A `PASS` result only applies to the behavior and test conditions explicitly described by the corresponding validation report.

---

### VAL-001 — DNS Validation

[`VAL-001-dns-validation.md`](validation/VAL-001-dns-validation.md)

Focuses on DNS behavior within the RethinkDNS architecture.

The validation examines DNS resolution behavior and the relationship between the configured encrypted resolver and application traffic.

**Status:** VALIDATED

---

### VAL-002 — Network Transition & WireGuard Routing Validation

[`VAL-002-network-transition-wireguard-routing.md`](validation/VAL-002-network-transition-wireguard-routing.md)

Validates application routing behavior while the active WireGuard proxy state changes.

The observed routing sequence was:

```
wg16
  ↓
wg17
  ↓
wg16
```

The validation also examined:

- TCP/443 connectivity
- UDP/443 traffic
- HTTP/3-associated traffic
- Firewall persistence
- DNS continuity
- Unexpected simultaneous WireGuard routing
- Observable application proxy bypass
- DNS fallback

The validation evidence demonstrated correct functional behavior for the tested configuration.

**Result:** PASS  
**Status:** CLOSED / VALIDATED

> The validation demonstrates observed functional behavior at the RethinkDNS routing and logging level. It does not constitute packet-level proof that zero packets can escape during every possible network transition.

---

### VAL-003 — Version Regression & Upgrade Validation

[`VAL-003-version-regression-upgrade-validation.md`](validation/VAL-003-version-regression-upgrade-validation.md)

Tracks behavior associated with RethinkDNS version changes and upgrade/regression testing.

This validation exists separately from the network-transition validation because application upgrades may introduce changes in:

- WireGuard behavior
- DNS handling
- Proxy assignment
- Firewall enforcement
- Network transition behavior

Its status should reflect the latest completed regression test rather than inheriting the result of previous validations.

---

## 5. VAL-002 Evidence

Supporting screenshots for VAL-002 are stored under:

```
validation/evidence/VAL-002/
```

The evidence set is intentionally limited to screenshots that directly support the validation findings.

| ID | Evidence | Validation purpose |
|---|---|---|
| E01 | `VAL-002-E01-wg16-initial-routing.png` | Initial Firefox routing through `wg16` |
| E02 | `VAL-002-E02-wg17-transition.png` | Firefox reassignment to `wg17` |
| E03 | `VAL-002-E03-wg16-return-routing.png` | Return routing through `wg16` |
| E04 | `VAL-002-E04-http80-firewall-block.png` | TCP/80 firewall enforcement |
| E05 | `VAL-002-E05-http3-udp443-wg17.png` | UDP/443 traffic through `wg17` |
| E06 | `VAL-002-E06-moddns-dot-resolution.png` | DNS resolution through modDNS over DoT |

Together, E01–E03 document the observed routing sequence:

```
wg16 → wg17 → wg16
```

E04 demonstrates persistence of the configured HTTP/TCP-80 firewall policy.

E05 provides evidence of UDP/443 traffic being routed through `wg17`.

E06 provides DNS continuity evidence using the modDNS DNS-over-TLS resolver active during the validation session.

Sensitive resolver identifiers contained in public evidence are redacted.

---

## 6. DNS Provider Context

Different encrypted DNS providers may be used by the architecture.

During the VAL-002 validation session, the active provider was:

```
modDNS
Transport: DNS-over-TLS
Port: TCP/853
Resolver: <REDACTED>.dns.moddns.net:853
```

NextDNS had been used in other configurations but was not the active resolver during that specific validation execution.

Therefore:

```
VAL-002 validates:
    WireGuard transition behavior
    Firewall persistence
    TCP/UDP routing continuity
    modDNS / DoT continuity

VAL-002 does NOT validate:
    NextDNS-specific transition behavior
```

DNS provider selection and WireGuard proxy routing are treated as separate architectural layers.

---

## 7. Configuration Guidance

[`configuration-recommendations.md`](guides/configuration-recommendations.md)

Contains configuration recommendations derived from the architecture and validation work.

Recommendations should not be interpreted as universal settings for every Android device or network environment.

Different ROMs, Android versions, VPN providers, DNS providers, and RethinkDNS releases may behave differently.

---

## 8. References

[`recommended-blocklists.md`](references/recommended-blocklists.md)

Contains blocklist references and related filtering resources used or evaluated by the project.

Blocklists should be evaluated before deployment because aggressive filtering can introduce application breakage or false positives.

---

## 9. Validation Principles

The RethinkDNS module follows several validation principles.

**Observed behavior over assumed behavior**

A configuration option being enabled does not by itself demonstrate that traffic follows the expected path.

**Evidence-backed conclusions**

Validation results should be supported by logs, screenshots, controlled tests, or other reproducible observations.

**No absolute leak claims without packet-level evidence**

The absence of visible bypasses in RethinkDNS logs is documented as:

```
NOT OBSERVED
```

rather than interpreted as proof that a bypass is impossible.

**Version-aware testing**

Behavior may change between RethinkDNS releases. Significant upgrades should therefore be treated as potential regression boundaries.

**Sensitive-data minimization**

Public evidence should not expose:

- WireGuard private keys
- DNS profile identifiers
- Authentication credentials
- Personal identifiers
- Private configuration secrets

Where necessary, sensitive values should be represented as:

```
<REDACTED>
```

---

## 10. Current Validation State

| Component | Document | State |
|---|---|---|
| Base RethinkDNS architecture | ARCH-001 | Documented |
| Traffic-flow architecture | ARCH-002 | Documented |
| DNS behavior | VAL-001 | VALIDATED |
| WireGuard transition behavior | VAL-002 | CLOSED / VALIDATED |
| Version regression / upgrade behavior | VAL-003 | Validation track |

The core RethinkDNS architecture can therefore be considered **functionally documented and validated for the tested configuration**.

This does not imply that every possible failure condition, Android version, RethinkDNS release, VPN provider, or network transition has been exhaustively tested.

---

## 11. Future Validation

Additional testing can extend the current validation baseline without invalidating the completed results.

Potential future work includes:

- Packet-level PCAP validation
- Controlled WireGuard tunnel failure
- Kill-switch behavior testing
- Interface-level traffic monitoring
- DNS-provider comparison
- IPv4/IPv6 transition testing
- RethinkDNS release regression testing
- Android/ROM upgrade regression testing

These tests should receive independent validation identifiers when they introduce a distinct validation objective.

---

## 12. Project Status

The current RethinkDNS work establishes a reproducible baseline for the Android OPSEC Hardening project.

```
Architecture       DOCUMENTED
DNS Validation     VALIDATED
WG Transition      VALIDATED
Firewall Behavior  VALIDATED
Evidence           CAPTURED
Extended Testing   ONGOING
```

The module should be treated as a validated baseline rather than a claim of universal or absolute network security.

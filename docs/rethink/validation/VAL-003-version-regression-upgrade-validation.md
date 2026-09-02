# VAL-003 — RethinkDNS Version Regression & Upgrade Validation

**Document ID:** VAL-003  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-09-02  
**Project:** Android OPSEC Hardening  
**Architecture References:** ARCH-001, ARCH-002  
**Validation References:** VAL-001, VAL-002  
**Reference Device:** Samsung Galaxy A50  
**Reference ROM:** crDroid  
**Baseline RethinkDNS:** v0.5.5x

---

## 1. Purpose

This document defines the methodology for evaluating RethinkDNS version changes against the Android OPSEC Hardening reference architecture.

The objective is to determine whether a new RethinkDNS version:

- Preserves existing functionality.
- Fixes previously identified problems.
- Introduces behavioral changes.
- Introduces regressions.
- Changes DNS routing.
- Changes WireGuard routing.
- Changes firewall behavior.
- Changes IPv4/IPv6 behavior.
- Changes application-specific proxy behavior.
- Changes network transition behavior.
- Requires architectural modifications.

The validation process is designed to prevent an application upgrade from being considered safe solely because the application starts successfully.

---

# 2. Validation Principle

A new version is not automatically considered an improvement.

The validation process evaluates:

```
New Version
     |
     +--> Functional improvement
     |
     +--> Functional preservation
     |
     +--> Behavioral change
     |
     +--> Regression
     |
     +--> Undetermined behavior
```
Only observable and reproducible behavior should determine the final classification.

---

# 3. Scope
This validation covers RethinkDNS behavior affecting:

- DNS.
- DoH.
- DoT.
- WireGuard.
- Advanced Mode.
- Simple Mode where applicable.
- Proxy Lockdown.
- Application-specific proxies.
- Global DNS.
- Split DNS.
- DNS bypass.
- Firewall.
- IP rules.
- IPv4.
- IPv6.
- Private IP routing.
- Network transitions.
- Wi-Fi.
- Mobile data.
- VPN recovery.
- Application isolation.
- Backup and restoration.
- Network connectivity checks.

---

4. Reference Baseline

The reference configuration is based on the configuration that has been tested and stabilized on the reference device.
```
Device:
Samsung Galaxy A50

ROM:
crDroid

RethinkDNS:
v0.5.5x

Mode:
Advanced

DNS:
NextDNS

DNS Transport:
DoH / configured baseline

WireGuard:
Proton WireGuard configurations

Application Routing:
Multiple application-specific proxies

Firewall:
Enabled

IPv4:
Enabled

IPv6:
Configured according to test

Split DNS:
Baseline configuration

Network:
Wi-Fi / Mobile Data
```
The baseline must remain unchanged while the candidate version is being evaluated.

----

# 5. Version Classification
The project currently recognizes the following versions:

| Version | Classification       | Role                   |
| ------- | -------------------- | ---------------------- |
| v0.5.5x | Stable baseline      | Reference              |
| v0.5.5y | Regression candidate | Historical comparison  |
| v0.5.5z | Pre-release          | Intermediate reference |
| v0.5.6 | Upgrade candidate | Primary validation target |

v0.5.5y introduced multiple changes involving DNS, WireGuard reconnectivity, Split DNS-related behavior, firewall resolution rules, and network automation.
Source: [RethinkDNS v0.5.5y release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5y)

v0.5.5z subsequently introduced more disciplined DNS routing decisions, Proxy Lockdown behavior for Simple-mode WireGuard, protection against Advanced-mode IP bouncing, DNS-time firewall application, and additional IPv6/network-engine changes.
Source: [RethinkDNS v0.5.5z release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5z)

v0.5.6 was selected as the primary upgrade candidate for this validation plan and includes DNS53 proxy crash fixes, stronger isolated-app IP rules, faster WireGuard startup under Proxy Lockdown, and several Network features graduating from experimental status.
Source: [RethinkDNS v0.5.6 release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.6)

----

# 6. Baseline Preservation
Before installing a candidate version:

1. Export or otherwise preserve the working RethinkDNS configuration.
2. Record the installed version.
3. Record the application build where available.
4. Record active WireGuard configurations.
5. Record DNS configuration.
6. Record firewall configuration.
7. Record application-specific proxy assignments.
8. Record Network settings.
9. Record Split DNS state.
10. Record IPv4/IPv6 state.
11. Record automation settings.
12. Record relevant screenshots.
13. Record the current VAL-001 results.

The baseline must remain recoverable.

---

# 7. Upgrade Rule
The candidate version must initially be tested using the baseline
configuration.

Do not simultaneously:

Upgrade RethinkDNS.
Change DNS provider.
Change WireGuard configuration.
Change firewall rules.
Change ROM.
Change Android version.
Change proxy architecture.

This preserves attribution: observed behavioral differences should be traceable to the candidate RethinkDNS version rather than to unrelated configuration changes.

---

# 8. Validation Phases

The upgrade validation is divided into seven phases.

```
Phase 0
Baseline Capture
     |
     v
Phase 1
Installation Integrity
     |
     v
Phase 2
Functional Validation
     |
     v
Phase 3
Traffic & DNS Validation
     |
     v
Phase 4
Network Configuration Validation
     |
     v
Phase 5
Failure & Recovery
     |
     v
Phase 6
Long-Term Stability
     |
     v
Final Classification
```

---

# 9. Phase 0 — Baseline Capture
## Objective

Create a reproducible reference state.

## Required information
```
RethinkDNS version
Android version
ROM
Kernel
DNS provider
DNS transport
Split DNS
IPv4
IPv6
WireGuard configurations
Application proxy assignments
Firewall configuration
Network configuration
Automation configuration
```

## Required validation
Run the minimum VAL-001 regression suite:
```
DNS-001
DNS-002
DNS-004
DNS-005
DNS-009
DNS-011
DNS-013
DNS-016
DNS-018
```

## Acceptance
All baseline tests must have known results.
Unknown baseline behavior must be documented before proceeding.

---

# 10. Phase 1 — Installation Integrity
## Objective

Verify that the candidate version can be installed without altering the environment in an undocumented manner.

## Procedure
1. Preserve the baseline.
2. Install the candidate release.
3. Confirm the installed version.
4. Open RethinkDNS.
5. Verify that configurations are present.
6. Verify WireGuard configurations.
7. Verify DNS configuration.
8. Verify firewall configuration.
9. Verify application assignments.
10. Verify Network configuration.

## Acceptance
The application starts normally and the expected configuration remains available.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 11. Phase 2 — Functional Validation
**VAL-003-F01 — Application Startup**

Determine whether RethinkDNS starts normally.

## Check
- Startup.
- VPN initialization.
- DNS initialization.
- Logs.
- Crash behavior.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-F02 — DNS Resolution**

Repeat the baseline DNS resolution test.

Reference:
`VAL-001 / DNS-001`

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-F03 — NextDNS Visibility**

Repeat:
`VAL-001 / DNS-002`

Compare:
```
Baseline v0.5.5x
        vs
Candidate
```

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-F04 — WireGuard Initialization**

Verify:

- Tunnel startup.
- Handshake.
- Routing.
- DNS behavior.
- Application connectivity.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-F05 — Multiple WireGuard Proxies**

Test the reference multi-proxy architecture.
```
General Applications
        |
        +--> WireGuard A

YouTube
        |
        +--> WireGuard B

Browser
        |
        +--> TOR / WireGuard C
```

## Acceptance

Each application follows the intended routing policy.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 12. Phase 3 — Traffic and DNS Validation
This phase incorporates the critical tests from VAL-001.

---

**VAL-003-T01 — DNS Through WireGuard**

Determine whether DNS queries generated by WireGuard-routed applications follow the expected DNS path.

## Evidence
- RethinkDNS DNS logs.
- RethinkDNS proxy state.
- NextDNS logs.
- External observations.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-T02 — DNS/Data Plane Correlation**

Compare:
```
DNS Path
    +
Application Data Path
```

The two paths must be interpreted independently before determining whether their difference is expected.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-T03 — Advanced Mode IP Stability**

## Objective
Determine whether the application alternates unexpectedly between the VPN and the direct network.

## Procedure
1. Enable Advanced Mode.
2. Activate the reference WireGuard proxy.
3. Enable the relevant lockdown policy.
4. Access the same external service repeatedly.
5. Record the observed external IP.
6. Repeat over time.

## Acceptance
No unexplained IP bouncing occurs.
This test is particularly relevant because `v0.5.5z` explicitly included a fix intended to prevent IP bouncing in Advanced-mode WireGuard. Source: [RethinkDNS v0.5.5z release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5z)

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-T04 — Proxy Lockdown**

## Objective
Validate that Proxy Lockdown prevents unintended direct traffic.

## Procedure
1. Activate Proxy Lockdown.
2. Confirm WireGuard.
3. Generate application traffic.
4. Interrupt the WireGuard tunnel.
5. Observe application connectivity.
6. Restore WireGuard.
7. Observe recovery.

## Expected
Behavior must match the configured lockdown policy.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-T05 — IPv4 / IPv6**

Test:
```
IPv4
IPv6
Dual-stack
```

Compare:

- DNS.
- Application traffic.
- VPN routing.
- External IP.
- Connectivity.

`v0.5.6` makes "Choose IP version" a non-experimental Network feature, making this an important regression test. Source: [RethinkDNS v0.5.6 release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.6)

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 13. Phase 4 — Network Configuration Validation
**VAL-003-N01 — Do Not Route Private IPs**

## Objective
Determine whether private-network traffic follows the intended policy.

Test ranges conceptually include:
```
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```
## Verify
- Router access.
- Local services.
- DNS.
- VPN traffic.
- Internet traffic.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-N02 — Use All Available Networks**

Test:
```
Wi-Fi
Mobile
Wi-Fi + Mobile transition
```

## Acceptance
Network selection remains consistent with the configured policy.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-N03 — Connectivity Checks**

Compare the behavior of:
```
None
Automatic
Manual
```
where applicable.

## Record:
- TCP.
- UDP.
- TLS.
- DNS.
- WireGuard.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-N04 — Bandwidth Booster**

This feature is now outside the experimental classification in `v0.5.6`.
It should therefore be validated independently rather than enabled automatically. Source: [RethinkDNS v0.5.6 release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.6)

## Test
Compare:
```
Disabled
vs
Enabled
```

Measure:

- Connectivity.
- Throughput.
- Latency.
- Stability.
- Battery impact where practical.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 14. Phase 5 — Failure and Recovery

**VAL-003-R01 — DNS Failure**

Simulate or safely reproduce DNS failure.

Determine:

- Whether resolution fails closed.
- Whether another DNS upstream is selected.
- Whether Global DNS becomes active.
- Whether the fallback is documented.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-R02 — WireGuard Failure**

Interrupt the WireGuard connection.

Observe:

- DNS.
- Application traffic.
- Firewall.
- Proxy state.
- Recovery.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-R03 — Network Loss**

Test:
```
Wi-Fi
  ↓
Network loss
  ↓
Wi-Fi recovery
```
and:
```
Wi-Fi
  ↓
Mobile Data
  ↓
Wi-Fi
```

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-R04 — Application Restart**

Restart applications assigned to different proxies.
Verify that their routing policy is preserved.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-R05 — RethinkDNS Restart**

Repeat:
`VAL-001 / DNS-017`

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

**VAL-003-R06 — Device Reboot**

Repeat:
`VAL-001 / DNS-018`

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 15. Phase 6 — Long-Term Stability

## Objective
Detect intermittent behavior that short tests cannot reproduce.

## Recommended observation period

Recommended:

`24 hours`

Extended observation where practical:

`48–72 hours`

Record:

- DNS routing.
- WireGuard state.
- External IP.
- Application proxy state.
- Network transitions.
- Battery impact.
- Temperature.
- Unexpected connection failures.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

---

# 16. Regression Classification

Every difference between versions must be classified.

| Classification          | Definition                                      |
| ----------------------- | ----------------------------------------------- |
| Improvement             | New behavior improves the intended architecture |
| Preserved               | Existing behavior remains equivalent            |
| Expected Change         | Behavior intentionally changed by design        |
| Regression              | Previously valid behavior no longer works       |
| New Defect              | New unintended behavior appears                 |
| Inconclusive            | Evidence is insufficient                        |
| Configuration-dependent | Behavior depends on an explicit setting         |

---

# 17. Severity Classification

| Severity      | Meaning                                               |
| ------------- | ----------------------------------------------------- |
| Critical      | Security boundary or traffic isolation failure        |
| High          | DNS/VPN routing failure or significant privacy impact |
| Medium        | Functional degradation without direct security impact |
| Low           | UI, performance, or convenience issue                 |
| Informational | Observable change without negative impact             |

---

# 18. Critical Regression Examples
The following should be treated as high-priority findings:

## DNS
```
Expected:
NextDNS

Observed:
Unexpected resolver
```

## WireGuard
```
Expected:
VPN-only traffic

Observed:
Direct traffic
```

## Advanced Mode
```
Expected:
Stable proxy routing

Observed:
Unexplained IP bouncing
```

## IPv6
```
Expected:
IPv6 follows VPN policy

Observed:
IPv6 bypasses VPN
```

## Firewall
```
Expected:
Blocked traffic

Observed:
Connection established outside policy
```

---

# 19. Comparative Test Matrix

| Test                    | v0.5.5x  | v0.5.5y | v0.5.5z | v0.5.6 |
| ----------------------- | -------- | ------- | ------- | ------ |
| Startup                 | Baseline | Historical | Historical | TBD |
| DNS resolution          | Baseline | Historical | Historical | TBD |
| NextDNS visibility      | Baseline | Historical | Historical | TBD |
| DNS/WG path             | Baseline | Historical | Historical | TBD |
| Advanced WG             | Baseline | Historical | Historical | TBD |
| IP stability            | Baseline | Historical | Historical | TBD |
| Proxy Lockdown          | Baseline | Historical | Historical | TBD |
| Split DNS               | Baseline | Historical | Historical | TBD |
| IPv4                    | Baseline | Historical | Historical | TBD |
| IPv6                    | Baseline | Historical | Historical | TBD |
| Private IP routing      | Baseline | Historical | Historical | TBD |
| Network transition      | Baseline | Historical | Historical | TBD |
| Firewall/DNS resolution | Baseline | Historical | Historical | TBD |
| Multi-proxy routing     | Baseline | Historical | Historical | TBD |
| Failure recovery        | Baseline | Historical | Historical | TBD |
| Reboot                  | Baseline | Historical | Historical | TBD |
| Long-term stability     | Baseline | Historical | Historical | TBD |

---

# 20. Version-Specific Findings

## v0.5.5y

Relevant release changes included:

- DNS bypass behavior changes.
- WireGuard reconnectivity.
- Wi-Fi/mobile automation.
- DNS-related firewall fixes.
- Loopback changes.

These changes are retained as historical context for regression analysis.
The release also provides the direct predecessor for the subsequent routing changes.

---

## v0.5.5z

Relevant changes include:

- More disciplined DNS routing decisions.
- Proxy Lockdown for Simple-mode WireGuard.
- Prevention of Advanced-mode IP bouncing.
- Firewall rules during DNS resolution.
- IPv6 changes.
- Network engine changes.
- Improved connectivity checks.

The release is classified as Pre-release. Source: [RethinkDNS v0.5.5z release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5z)

---

## v0.5.6

Relevant changes include:

- DNS53 proxy startup crash fix.
- Reinforcement of trust/allowed IP rules for isolated applications.
- Faster WireGuard startup under Proxy Lockdown.
- Android 17 support.
- Choose IP version no longer experimental.
- Do not route Private IPs no longer experimental.
- Use all available networks no longer experimental.
- Bandwidth Booster no longer experimental.
- DNS website icons no longer experimental.
- Deleted WireGuard configurations no longer shown.

> Historical release information is used to identify regression-sensitive areas and prioritize candidate-version testing. Historical versions do not need to be reinstalled unless direct comparative reproduction is explicitly required.
> At the time this validation plan was prepared, `v0.5.6` was selected as the primary upgrade candidate.

Source: [RethinkDNS v0.5.6 release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.6)

---

# 21. Upgrade Decision
The candidate version receives one of four final decisions.

## APPROVED
The candidate preserves the security and routing properties of the baseline and introduces no unresolved critical or high-severity issues.

## APPROVED WITH CONDITIONS
The candidate is usable but requires documented configuration changes or has known limitations.

## HOLD
The candidate introduces unresolved behavior that requires further investigation.

# REJECTED
The candidate introduces a reproducible critical regression affecting the reference security architecture.

---

# 22. Upgrade Report
Each completed upgrade should produce:
```
Version:
vX.X.X

Previous Version:
vX.X.X

Date:
YYYY-MM-DD

Device:
Samsung Galaxy A50

ROM:
crDroid

Configuration:
Reference / Modified

VAL-001 Regression Suite:
PASS / FAIL / PARTIAL / INCONCLUSIVE

VAL-002 Transition Recheck:
PASS / FAIL / PARTIAL / NOT TESTED

VAL-003 Execution:
COMPLETE / PARTIAL

Critical Findings:
<none / list>

High Findings:
<none / list>

Medium Findings:
<none / list>

Observed Improvements:
<list>

Observed Regressions:
<list>

Final Decision:
APPROVED / APPROVED WITH CONDITIONS / HOLD / REJECTED
```

---

# 23. Rollback Procedure
If a candidate version produces a critical regression:

1. Stop further testing.
2. Preserve logs.
3. Record the exact configuration.
4. Record the candidate version.
5. Restore the baseline RethinkDNS version.
6. Restore the known-good configuration.
7. Repeat the affected VAL-001 tests.
8. Confirm baseline recovery.
9. Document the regression.
10. Do not modify the evidence collected from the failed version.

---

# 24. Evidence Preservation
For every significant regression retain:

- Screenshots.
- RethinkDNS logs.
- DNS logs.
- NextDNS observations.
- WireGuard state.
- Application routing.
- Version number.
- Build/commit where available.
- Timestamp.
- Network state.
- Configuration state.

Sensitive information such as:

- VPN private keys.
- Authentication tokens.
- Personal identifiers.
- Private DNS credentials.

must never be committed to the repository.

---

# 25. Relationship With VAL-001 and VAL-002

`VAL-003` does not replace `VAL-001` or `VAL-002`.

Instead:

```
VAL-001
DNS validation
     |
     +------------------+
     |                  |
     v                  v
VAL-002              VAL-003
Network/WireGuard    Version regression
transition           & upgrade validation
     |                  |
     +--------+---------+
              |
              v
      Reference behavior
```
`VAL-001` defines the DNS validation methodology and records DNS-specific behavior.

`VAL-002` validates network transitions, WireGuard proxy reassignment, traffic continuity, and firewall persistence for the tested configuration.

`VAL-003` determines whether a RethinkDNS version change preserves, changes, improves, or regresses the previously validated behavior.

---

# 26. Acceptance Criteria
A new RethinkDNS version may be incorporated into the reference architecture only when:

- Critical VAL-001 tests pass.
- DNS routing is understood.
- WireGuard routing is understood.
- Advanced-mode routing is stable.
- No unexplained IP bouncing occurs.
- IPv4 behavior is validated.
- IPv6 behavior is validated or intentionally disabled.
- DNS fallback behavior is understood.
- Network transition behavior is understood.
- Firewall behavior is validated.
- Multi-proxy routing remains functional.
- Failure recovery is understood.
- Long-term stability is acceptable.
- No unresolved Critical findings remain.
- High-severity findings are resolved or explicitly documented as accepted limitations.

---

# 27. Final Principle
**A software upgrade is not considered validated because the application launches correctly.**
The upgrade is validated only when the security, privacy, DNS, routing, firewall, and recovery properties of the reference architecture remain understood and reproducible.

---

# 28. Document Status

**Methodology Status:** Defined  
**Execution Status:** Pending  
**Document Status:** Draft

This document establishes the version regression and upgrade validation methodology for RethinkDNS within Android OPSEC Hardening.

The first complete execution target is:
```
Baseline:
v0.5.5x

Candidate:
v0.5.6
```
Historical versions:
```
v0.5.5y
v0.5.5z
```
are retained for regression analysis and architectural history.

## References

- [RethinkDNS v0.5.5y release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5y)
- [RethinkDNS v0.5.5z release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.5z)
- [RethinkDNS v0.5.6 release notes](https://github.com/celzero/rethink-app/releases/tag/v0.5.6)

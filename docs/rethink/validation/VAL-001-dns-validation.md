# VAL-001 — DNS Validation

**Document ID:** VAL-001  
**Version:** 1.2
**Status:** Active Validation
**Last Updated:** 2026-09-02
**Project:** Android OPSEC Hardening  
**Architecture Reference:** ARCH-001, ARCH-002  
**Reference Device:** Samsung Galaxy A50 (SM-A505G)  
**Scope:** DNS resolution, transport, routing, fallback, and continuity validation

---

## 1. Purpose

This document defines the validation procedures required to determine whether DNS traffic follows the intended architecture defined in ARCH-001 and ARCH-002.

The objective is not merely to determine whether DNS resolution works.

The objective is to determine:

- Which resolver receives the query.
- Which transport is used.
- Whether DNS traffic follows the expected proxy or VPN path.
- Whether the configured DNS provider receives the expected queries.
- Whether DNS traffic bypasses the configured policy.
- Whether Split DNS changes the expected behavior.
- Whether application-specific proxies influence DNS routing.
- Whether IPv4 and IPv6 introduce different DNS paths.
- Whether network transitions modify DNS behavior.
- Whether a configuration failure produces an unexpected fallback.

---

# 2. Validation Philosophy

DNS validation must distinguish between three different properties:

```
                    DNS Validation
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Resolver       Transport       Network Path
          |              |              |
          v              v              v
      Who answers?   How is it sent?  Where does it go?
```
These properties must not be treated as equivalent.

For example:

* A successful DNS-provider query does not automatically prove that the query travelled through the intended WireGuard tunnel.

Likewise:

* An external VPN IP does not automatically prove that DNS queries used the same VPN path.

----

# 3. Scope

This validation framework covers:

- Encrypted DNS providers.
- DNS over HTTPS (DoH).
- DNS over TLS (DoT).
- WireGuard-provided DNS.
- RethinkDNS Global DNS.
- Split DNS.
- DNS bypass.
- Application-specific proxies.
- General proxy routing.
- Direct network conditions.
- IPv4.
- IPv6.
- Wi-Fi.
- Mobile data.
- Network transitions.
- DNS failure and recovery.

Provider-specific tests may additionally validate services such as **NextDNS** or **modDNS** when they are part of the test environment.

----

# 4. Reference Configuration

VAL-001 is designed to be executed against a recorded deployment
configuration rather than a permanently fixed DNS provider or software
version.

A validation run should record at minimum:

```
Device:
<device>

Android:
<version>

ROM:
<ROM / build>

Root:
Enabled / Disabled

RethinkDNS:
<version>

RethinkDNS Mode:
<mode>

DNS Provider:
<provider>

DNS Transport:
DoH / DoT / WireGuard DNS / Other

WireGuard:
<configuration state>

Firewall:
Enabled / Disabled

Application-specific proxies:
Enabled / Disabled

Split DNS:
Enabled / Disabled

IPv4:
Enabled / Disabled

IPv6:
Enabled / Disabled

Network:
Wi-Fi / Mobile / Other
```
Historical and current validation environments must not be assumed to be equivalent.

The exact configuration used during each validation run must be recorded with its results.

-----

# 5. DNS Flow Under Test

The principal expected flow is:
```
Application
     |
     v
RethinkDNS
     |
     v
DNS Policy
     |
     v
Encrypted DNS Provider
     |
     v
DNS Response
     |
     v
Application
```

When DNS is associated with a WireGuard proxy, the expected flow may instead be:

```
Application
     |
     v
RethinkDNS
     |
     v
WireGuard DNS
     |
     v
Encrypted VPN Tunnel
     |
     v
VPN Endpoint / DNS Resolver
```

The actual path must be established through observation.

-----

# 6. Test Result Classification

Every test uses one of the following result classifications.
| Result | Meaning |
|---|---|
| `PASS` | Observed behavior matches the expected behavior |
| `FAIL` | Observed behavior violates the expected behavior |
| `PARTIAL` | Some expected properties were demonstrated, but coverage is incomplete |
| `INCONCLUSIVE` | The test was attempted but available evidence cannot establish the result |
| `NOT TESTED` | The test has not yet been executed |
| `NOT APPLICABLE` | The tested deployment does not use the feature or condition addressed by the test |

Important:

The absence of evidence should not be converted into a `PASS`.

-----

# 7. Evidence Sources

Each validation should use as many independent evidence sources as practical.

Recommended sources:

## RethinkDNS

- Network logs.
- DNS logs.
- Proxy status.
- WireGuard status.
- Application routing.

## DNS Provider

When available:

- Query logs.
- Configured endpoint.
- Client association.
- Timestamp correlation.
- Source information.
- Resolver status.

## External validation

- External IP.
- DNS resolver identification.
- DNS leak testing.
- IPv4 testing.
- IPv6 testing.
- Packet capture when required by the test objective.
- Interface-level observations when required.

## Android

- Wi-Fi state.
- Mobile network state.
- VPN state.
- Application state.

No individual evidence source should automatically be considered conclusive.

-----

# 8. Test Environment Preparation

Before beginning validation:

1. Record the Android version.
2. Record the ROM version.
3. Record the RethinkDNS version.
4. Record the DNS configuration.
5. Record the DNS-provider configuration.
6. Record the DNS transport.
7. Record whether DNS Booster/cache behavior may affect observations.
8. Record active WireGuard proxies.
9. Record application-specific proxy assignments.
10. Record firewall settings.
11. Record IPv4/IPv6 configuration.
12. Record whether Split DNS is enabled.
13. Record the active network.
14. Synchronize the device time.
15. Clear or identify previous DNS logs where possible.

The purpose is to ensure that test results can later be correlated.

-----

# 9. Test DNS-001 — Baseline DNS Resolution

## Objective
Verify that normal DNS resolution works before testing routing properties.

## Procedure
1. Connect the device to the reference Wi-Fi network.
2. Ensure RethinkDNS is running.
3. Ensure the reference DNS configuration is active.
4. Open a known application requiring DNS resolution.
5. Generate several DNS requests.
6. Check RethinkDNS DNS logs.
7. Check DNS-provider query logs when available.
8. Correlate timestamps.

## Expected Result
DNS resolution succeeds and the expected resolver receives the corresponding queries.

## Evidence
* RethinkDNS DNS log.
* NextDNS query log.
* Application connectivity.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

-----

# 10. Test DNS-002 — DNS Provider Query Visibility

## Objective
Determine whether application-generated DNS queries are observable by the configured DNS provider when provider-side logging or equivalent evidence is available.

## Procedure
1. Select a test application.
2. Generate a unique DNS request.
3. Record the approximate timestamp.
4. Observe RethinkDNS logs.
5. Observe DNS provider logs.
6. Compare the results.

## Expected Result
The query is observed by the configured provider when the deployment is expected to use that resolver.

## Failure Conditions
The query is generated but:

* Does not appear in DNS provider.
* Appears under an unexpected resolver.
* Appears through an unexpected client association.
* Appears only intermittently.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

-----

# 11. Test DNS-003 — DNS Transport Validation

## Objective
Determine whether the configured DNS transport is actually being used.

Possible transports include:

- DoH.
- DoT.
- WireGuard DNS.
- Other configured upstreams.

## Procedure
1. Record the configured DNS transport.
2. Generate DNS requests.
3. Observe RethinkDNS DNS logs.
4. Observe proxy state.
5. Observe DNS-provider query reception where applicable.
6. Compare observed behavior with the configured transport.

## Expected Result
Observed DNS behavior is consistent with the configured transport.

## Important
Successful name resolution alone is not sufficient evidence of transport validation.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

-----

# 12. Test DNS-004 — DNS Through WireGuard

### DNS-004 — DNS Resolution Through Active WireGuard Route

**Objective**

Verify whether DNS queries reaching the configured upstream resolver are consistent with the public egress path used while the WireGuard tunnel is active.

**Procedure**

1. Enable the expected WireGuard route (`wg16`).
2. Generate normal browser traffic.
3. Confirm application traffic is routed through `wg16` in RethinkDNS.
4. Query an external public-IP service from the same browser session.
5. Record the observed public IPv4 address.
6. Generate fresh DNS queries.
7. Inspect the NextDNS provider-side logs and source-IP statistics.
8. Compare the DNS source address with the observed public WireGuard egress
   address.

**Observed Result**

RethinkDNS showed Firefox traffic routed through `wg16`.

The public IPv4 address observed during the active WireGuard session was:

`195.86.38.37`

NextDNS provider-side statistics independently reported DNS queries originating from:

`195.86.38.37`

Fresh queries generated during the test, including requests associated with the public-IP test, were also visible in the configured NextDNS profile.

The public egress IPv4 and the DNS provider-observed source IPv4 therefore matched.

**Result:** PASS

**Validation level:** Functional correlation

The result provides functional evidence consistent with DNS queries reaching NextDNS through the expected VPN egress path. Packet-level interface capture was not performed; therefore this test does not constitute proof that every possible DNS packet or failure condition is incapable of bypassing the tunnel.

-----

# 13. Test DNS-005 — DNS and Data Plane Correlation

## Objective
Determine whether DNS and application traffic follow the same intended network path.

## Procedure
For a selected application:

1. Record the active proxy.
2. Generate a unique DNS request.
3. Record the DNS-provider observation.
4. Access an external service.
5. Record the observed external IP.
6. Record RethinkDNS proxy information.
7. Correlate timestamps.

## Expected Result
The DNS and data-plane observations match the intended architecture.

## Example
```
DNS:
Configured provider / expected path

Data:
WireGuard / expected VPN exit
```

If these paths differ, the result is not automatically a failure.

The architecture must first determine whether that difference is expected.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

-----

# 14. Test DNS-006 — Split DNS Disabled

## Objective
Determine the effect of disabling Split DNS.

##Procedure
1. Record the current DNS state.
2. Disable Split DNS.
3. Restart RethinkDNS if required.
4. Generate DNS queries.
5. Observe RethinkDNS.
6. Observe the configured DNS provider when possible.
7. Repeat with a WireGuard-routed application.

## Expected Result
DNS queries follow the behavior defined by the current architecture when Split DNS is disabled.

## Validation Requirement
The observed behavior must be compared with the previous baseline.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

-----

# 15. Test DNS-007 — Split DNS Enabled

## Objective
Determine how Split DNS changes DNS routing.

## Procedure
1. Restore the baseline configuration.
2. Enable Split DNS.
3. Restart RethinkDNS if required.
4. Generate identical DNS queries.
5. Compare:
   - RethinkDNS logs.
   - DNS provider logs.
   - Proxy state.
   - Resolver behavior.

## Expected Result
The observed changes are consistent with the documented Split DNS configuration.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 16. Test DNS-008 — Application-Specific DNS

## Objective
Determine whether applications assigned to different proxies produce different DNS behavior.

## Test Configuration
Example:
```
Application A
    |
    +--> General WireGuard

Application B
    |
    +--> Dedicated WireGuard

Application C
    |
    +--> TOR Proxy
```

## Procedure
1. Generate DNS queries from Application A.
2. Record DNS behavior.
3. Repeat for Application B.
4. Repeat for Application C.
5. Compare the results.

## Expected Result
DNS behavior corresponds to the configured application policy.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 17. Test DNS-009 — DNS Bypass

## Objective

Determine whether DNS queries can bypass the configured DNS policy under normal operating conditions.

## Procedure

1. Establish the reference DNS configuration.
2. Generate fresh DNS queries from a selected application.
3. Observe the queries in RethinkDNS.
4. Observe the configured DNS provider when available.
5. Check for unexpected resolver attribution.
6. Compare DNS behavior with the documented routing policy.
7. Investigate any query that appears to use an unconfigured resolver.

## Expected Result

No unexpected DNS resolver or DNS path is observed within the tested scope.

## Important

Absence of an observed bypass does not establish that bypass is impossible under every network or failure condition.

Packet capture or interface-level monitoring may be required for stronger bypass analysis.

## Result

`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 18. Test DNS-010 — DNS Failure

## Objective
Determine what happens when the primary DNS resolver becomes unavailable.

## Procedure
1. Record the baseline configuration.
2. Introduce a controlled DNS failure.
3. Generate DNS queries.
4. Observe RethinkDNS.
5. Observe application connectivity.
6. Determine whether another resolver is used.

## Expected Result
The fallback behavior matches the documented security policy.
Possible outcomes:

```
Fail Closed
     OR
Controlled Fallback
```

An undocumented fallback should be investigated.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 19. Test DNS-011 — WireGuard Failure

## Objective
Determine whether DNS behavior changes when the associated WireGuard proxy becomes unavailable.

## Procedure
1. Activate the WireGuard proxy.
2. Confirm baseline behavior.
3. Introduce a controlled WireGuard failure.
4. Generate DNS queries.
5. Observe RethinkDNS.
6. Observe DNS provider.
7. Determine whether DNS switches to another upstream.

## Expected Result
The resulting behavior matches the configured routing policy.

## Important
A fallback to another DNS resolver must be documented rather than automatically classified as a leak.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 20. Test DNS-012 — IPv4

## Objective
Validate DNS behavior over IPv4.

## Procedure
1. Disable IPv6 where technically possible for the test.
2. Maintain the reference DNS configuration.
3. Generate DNS queries.
4. Observe the resolver.
5. Record the result.

## Expected Result
DNS follows the intended policy over IPv4.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 21. Test DNS-013 — IPv6

## Objective
Determine whether IPv6 introduces an alternate DNS path.

## Procedure
1. Enable IPv6.
2. Maintain the reference configuration.
3. Generate DNS queries.
4. Compare with the IPv4-only test.
5. Check external IPv6 connectivity.
6. Check DNS behavior.

## Expected Result
IPv6 does not create an unintended DNS path.

## Failure / Investigation Conditions

Examples include:

- DNS requests using an unexpected resolver over IPv6.
- DNS behavior differing unexpectedly between IPv4 and IPv6.
- IPv6 data-plane behavior inconsistent with the intended VPN policy.

The third condition concerns correlated data-plane behavior and should not by itself be treated as a DNS-resolution failure.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 22. Test DNS-014 — Wi-Fi

## Objective
Validate DNS behavior on the reference Wi-Fi network.

## Procedure
1. Connect to the reference SSID.
2. Confirm RethinkDNS is active.
3. Generate DNS queries.
4. Record all relevant observations.
5. Repeat at least three times.

## Expected Result
The same DNS policy is consistently enforced.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 23. Test DNS-015 — Mobile Data

## Objective
Validate DNS behavior over mobile data.

## Procedure
1. Disable Wi-Fi.
2. Enable mobile data.
3. Confirm RethinkDNS is active.
4. Generate DNS queries.
5. Observe RethinkDNS.
6. DNS-provider observation.
7. Compare against the Wi-Fi results.

## Expected Result
DNS policy remains consistent unless a documented network-specific configuration exists.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 24. Test DNS-016 — Network Transition

### DNS-016 — DNS Continuity During Network Transition

**Objective**

Validate that the configured DNS policy remains operational while the device transitions between Wi-Fi and mobile connectivity and returns to Wi-Fi.

**Test sequence**

1. Established connectivity over Wi-Fi.
2. Generated DNS and HTTPS traffic from Firefox.
3. Confirmed DNS resolution through the configured NextDNS resolver.
4. Transitioned from Wi-Fi to mobile data.
5. Generated new DNS and HTTPS traffic while mobile connectivity was active.
6. Verified continued DNS processing by RethinkDNS.
7. Returned from mobile data to Wi-Fi.
8. Generated additional DNS traffic.
9. Confirmed that the configured resolver remained operational after the transition.
10. Correlated observed queries with the NextDNS dashboard.

**Observed behavior**

Before the network transition:

- DNS queries were processed through RethinkDNS.
- The resolver was identified as `dns.nextdns.io`.
- DNS transport was observed as DoH.
- Firefox HTTPS traffic was routed through `wg16`.

During mobile connectivity:

- Mobile connectivity was visibly active (`LTE+`).
- DNS resolution remained operational through RethinkDNS.
- New DNS queries were generated successfully.
- Firefox network traffic was observed through `wg17`.
- No unexpected DNS resolver was observed in the inspected RethinkDNS records.

After returning to Wi-Fi:

- DNS resolution remained operational.
- RethinkDNS continued to identify `dns.nextdns.io` as the configured resolver.
- DoH operation was observed.
- Firefox traffic returned to `wg16`.
- Corresponding DNS queries were visible in the NextDNS dashboard.

**Result:** PASS

**Validation level:** Functional continuity

The Wi-Fi → mobile data → Wi-Fi transition completed without an observed loss of the configured DNS policy.

No unexpected DNS resolver or functional DNS fallback was observed during the inspected test window.

The WireGuard routing transition (`wg16 → wg17 → wg16`) also behaved consistently with the configured network policy.

**Validation scope**

This result validates functional DNS continuity based on RethinkDNS DNS/network logs and resolver-side observations.

It does not constitute packet-level proof that no transient DNS packet could have bypassed the configured resolver during the network transition. Packet capture or interface-level monitoring would be required for definitive packet-level leak analysis.

----

# 25. Test DNS-017 — RethinkDNS Restart

## Objective
Determine whether restarting RethinkDNS changes DNS routing.

## Procedure
1. Establish the baseline.
2. Record DNS behavior.
3. Stop RethinkDNS.
4. Start RethinkDNS.
5. Wait for network stabilization.
6. Generate DNS queries.
7. Compare results.

## Expected Result
The configured DNS policy is restored without an unintended fallback.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 26. Test DNS-018 — Device Reboot

## Objective
Determine whether DNS configuration survives a complete device reboot.

## Procedure
1. Record baseline configuration.
2. Reboot the device.
3. Wait for Android initialization.
4. Confirm RethinkDNS state.
5. Confirm DNS configuration.
6. Generate DNS queries.
7. Compare with the pre-reboot state.

## Expected Result
The intended DNS architecture is restored after reboot.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 27. Test DNS-019 — Lock / Unlock

## Objective
Determine whether device-lock policies influence DNS behavior.

## Procedure
1. Generate DNS queries while unlocked.
2. Lock the device.
3. Attempt background network activity.
4. Unlock the device.
5. Generate new DNS queries.
6. Compare the behavior.

## Expected Result
DNS behavior follows the configured lock-state firewall policy.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 28. Test DNS-020 — Repeated Query Consistency

## Objective
Determine whether DNS routing remains stable over time.

## Procedure
Generate repeated DNS queries over an extended test period.

## Record:
* Timestamp.
* Application.
* Resolver.
* Proxy.
* WireGuard state.
* DNS-provider observation.

## Expected Result
The same configuration produces consistent DNS behavior.

## Important
Intermittent routing changes must not be dismissed as random noise.
They should be investigated as potential state-transition, routing, resolver, or software-version issues.

## Result
`PASS / FAIL / PARTIAL / INCONCLUSIVE`

----

# 29. DNS Leak Assessment

A DNS leak should not be defined merely as:

- "The observed DNS resolver is different from the primary configured provider."

Instead, the assessment should answer:

1. Was that resolver explicitly configured?
2. Was the application intentionally bypassed?
3. Was Split DNS enabled?
4. Was the query generated through a WireGuard proxy?
5. Was a fallback condition active?
6. Did RethinkDNS report a proxy or DNS failure?
7. Did the behavior persist after recovery?

Only after answering these questions should the event be classified.

----

# 30. Leak Classification

| Classification      | Description                               |
| ------------------- | ----------------------------------------- |
| Expected            | Behavior matches documented architecture  |
| Explicit Bypass     | Behavior was intentionally configured     |
| Controlled Fallback | Alternative resolver used after failure   |
| Unexpected          | Resolver/path differs from policy         |
| Unverified          | Evidence insufficient                     |
| Regression          | Previously valid behavior no longer works |

This classification prevents false positives during testing.

----

# 31. Evidence Correlation

A validation result should preferably contain at least two independent pieces of evidence.

Example:
```
Evidence A:
RethinkDNS indicates WireGuard proxy active.

Evidence B:
External service reports VPN exit IP.

Evidence C:
DNS provider records query.

Conclusion:
Data plane = VPN
DNS visibility = configured provider
DNS path through VPN = requires additional evidence
```

This distinction is essential.

----

# 32. Validation Record

Each executed test should produce a record similar to:

```
Test ID:
DNS-XXX

Date:
YYYY-MM-DD

Device:
<device>

Android:
<version>

ROM:
<ROM / build>

RethinkDNS:
<version>

Network:
Wi-Fi / Mobile / Other

IPv4:
Enabled / Disabled

IPv6:
Enabled / Disabled

Split DNS:
Enabled / Disabled

DNS Provider:
<provider>

DNS Transport:
DoH / DoT / WireGuard DNS / Other

Application:
<application>

Proxy:
<proxy>

Expected Result:
<description>

Observed Result:
<description>

Evidence:
<logs / screenshots / packet capture / external tests>

Result:
PASS / FAIL / PARTIAL / INCONCLUSIVE / NOT TESTED / NOT APPLICABLE

Notes:
<additional information>
```

----

# 33. Validation Matrix

The initial validation matrix is:

| Test    | Objective                | Priority | Status  |
| ------- | ------------------------ | -------: | ------- |
| DNS-001 | Baseline resolution      |     High | PASS |
| DNS-002 | DNS Provider visibility  |     High | PASS |
| DNS-003 | Transport validation     |     High | PASS |
| DNS-004 | DNS through WireGuard    | Critical | PASS |
| DNS-005* | DNS/Data correlation     | Critical | PASS |
| DNS-006 | Split DNS disabled       |     High | PARTIAL |
| DNS-007 | Split DNS enabled        |     High | NOT TESTED |
| DNS-008 | Application-specific DNS | Critical | NOT TESTED |
| DNS-009 | DNS bypass               | Critical | NOT TESTED |
| DNS-010 | DNS failure              |     High | NOT TESTED |
| DNS-011 | WireGuard failure        | Critical | NOT TESTED |
| DNS-012 | IPv4                     |     High | PARTIAL |
| DNS-013 | IPv6                     | Critical | PARTIAL |
| DNS-014 | Wi-Fi                    |     High | PARTIAL |
| DNS-015 | Mobile data              |     High | NOT TESTED |
| DNS-016 | Network transition       |     High | PASS |
| DNS-017 | RethinkDNS restart       |     High | NOT TESTED |
| DNS-018 | Device reboot            |     High | NOT TESTED |
| DNS-019 | Lock/unlock              |   Medium | NOT TESTED |
| DNS-020 | Long-term consistency    | Critical | PARTIAL |

Notes:

DNS-005* — DNS/Data Plane Correlation
`PASS`:
- Demonstrates functional correlation between observed DNS resolution and application data traffic. It does not establish that both planes traverse the same physical tunnel or network interface.

----

# 34. Acceptance Criteria

VAL-001 should distinguish between core DNS validation and extended
environmental validation.

## Core DNS Validation

Core validation should establish:

- Functional DNS resolution.
- Expected resolver attribution.
- DNS transport consistency.
- DNS/data-plane correlation where relevant.
- DNS bypass behavior.
- WireGuard-associated DNS behavior where applicable.
- No unexplained resolver path within the tested scope.

## Extended Validation

Additional coverage may include:

- Split DNS.
- IPv4/IPv6 comparison.
- Wi-Fi/mobile-data comparison.
- Network transitions.
- Controlled DNS failure.
- Controlled WireGuard failure.
- RethinkDNS restart.
- Device reboot.
- Lock/unlock behavior.
- Long-term consistency.

A core `PASS` does not imply that every extended scenario has been tested.

Untested scenarios must remain explicitly identified as `NOT TESTED`.

----

# 35. Regression Testing

Whenever one of the following changes:

- RethinkDNS version.
- Android version.
- ROM.
- Kernel.
- DNS provider.
- DNS transport.
- WireGuard configuration.
- Proxy configuration.
- Firewall configuration.
the relevant DNS validation tests should be repeated.

At minimum:
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
This minimum set should be treated as the recommended regression suite unless the changed component requires additional tests.

----

# 36. Version Regression Tracking

Historical project testing demonstrated why version-aware DNS
validation is necessary.

One historical comparison involved:

```
v0.5.5x
    |
    +---- Expected DNS/proxy behavior observed
    |
    v
v0.5.5y
    |
    +---- DNS / proxy behavior changed
    |
    v
Regression investigation
```

This example represents historical project context rather than the current validation baseline.

Current version-regression testing is tracked through:

`VAL-003`

A new software version must not automatically inherit the validation status of an earlier version.

----

# 37. Security Interpretation

A successful DNS validation does not prove that the entire device is secure.

It only establishes that the tested DNS flows behave consistently with the documented architecture.

Likewise, a failed DNS test does not necessarily mean that the entire VPN architecture is compromised.

Failures must be isolated to the affected traffic plane.

----

# 38. Final Validation Principle

* DNS privacy is not validated by asking only "Which DNS am I using?"

A complete validation asks:
```
Who resolved the query?
        +
How was the query transported?
        +
Which network path carried it?
        +
Which application generated it?
        +
Was the behavior intentional?
        +
Did the behavior remain consistent?
```
Only the combination of these observations provides meaningful evidence of DNS-path correctness.

----

# 39. Document Status

**Current status:** Active Validation

VAL-001 defines the DNS validation methodology used by the Android OPSEC Hardening project.

Individual DNS test results must be classified independently according to the evidence available for the recorded test environment.

The existence of this validation methodology does not imply that every DNS-XXX test has been executed.

Untested scenarios remain `NOT TESTED`.

A complete or scoped validation state may only be assigned after the corresponding evidence and test matrix have been reviewed.

The document should be updated when the architecture, validation methodology, or relevant RethinkDNS behavior changes.

# ARCH-002 — Traffic Flow

**Document ID:** ARCH-002  
**Version:** 1.1  
**Status:** Published  
**Last Updated:** 2026-09-01  
**Project:** Android OPSEC Hardening  
**Related Architecture:** ARCH-001 — RethinkDNS Architecture  
**Reference Device:** Samsung Galaxy A50 (SM-A505G)  
**Scope:** Android network traffic-flow architecture

----

## 1. Purpose

This document defines the expected network traffic flows within the reference Android OPSEC Hardening architecture.

The purpose is to describe how different classes of traffic are expected to move between Android applications, RethinkDNS, DNS resolvers, WireGuard tunnels, VPN endpoints, and the external network.

The document focuses on traffic flow rather than configuration.

It therefore answers questions such as:

- Where should an application's DNS query go?
- Which component determines the network route?
- When should traffic enter a WireGuard tunnel?
- When can DNS and application traffic follow different paths?
- Where can traffic be intentionally bypassed?
- What happens when a proxy becomes unavailable?
- How should IPv4 and IPv6 traffic be considered?
- Which observations are required to validate the expected behavior?

This document does not assume that every deployment will use the same DNS provider, VPN provider, or routing policy.

----

# 2. Scope

The traffic flows described here cover:

- Normal application traffic.
- DNS resolution.
- Encrypted DNS provider integration.
- Direct network traffic.
- WireGuard-routed traffic.
- Application-specific WireGuard routing.
- Multiple proxy configurations.
- TOR-routed browser traffic.
- Firewall decisions.
- DNS bypass behavior.
- Split DNS considerations.
- IPv4 and IPv6 behavior.
- Network transitions.
- Failure and recovery scenarios.
- Traffic observability.

The reference architecture is based on RethinkDNS Advanced Mode.

---

# 3. Traffic Plane Model

The architecture should be understood as multiple related traffic planes.

```
                         APPLICATION
                              |
                              |
                    +---------+---------+
                    |                   |
                    v                   v
                 DNS PLANE         DATA PLANE
                    |                   |
                    v                   v
                DNS Policy          RethinkDNS
                    |                   |
                    v                   v
                 Resolver          Firewall / Proxy
                                        |
                             +----------+----------+
                             |          |          |
                             v          v          v
                          Direct     WireGuard     TOR
                             |          |          |
                             v          v          v
                          Network    VPN Exit    TOR Network
```
The DNS plane and data plane are logically related but should not be assumed to always follow the same physical network path.

This distinction is critical when validating DNS privacy and VPN routing.

---

# 4. Reference Traffic Path

The general reference path is:

```
Application
     |
     v
Android Network Stack
     |
     v
RethinkDNS
     |
     +----------------------+
     |                      |
     v                      v
DNS Resolution         Traffic Policy
     |                      |
     v                      v
Encrypted DNS          Firewall / Proxy
Provider                    |
                     +------+------+------+
                     |             |      |
                     v             v      v
                   Direct      WireGuard  TOR
                     |             |      |
                     v             v      v
                  Network       VPN Exit  TOR Network
```

The exact path depends on the application's assigned network policy.

---

# 5. DNS Traffic Flow

DNS resolution is treated as a separate traffic flow from application payload traffic.

The conceptual flow is:

```
Application
     |
     v
RethinkDNS DNS Layer
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

The upstream resolver may use different encrypted transports depending on the deployment, including:

- DNS over HTTPS (DoH).
- DNS over TLS (DoT).
- DNS provided through a WireGuard configuration.
- Another explicitly configured resolver.

The selected provider and transport are deployment-specific.

The authoritative DNS behavior for a tested configuration should be determined through the corresponding validation report.

---

# 6. DNS and VPN Path Independence
DNS traffic and application traffic should not automatically be assumed to share the same route.

For example, the following situation is technically possible:
```
Application
    |
    +---- DNS ----> Encrypted DNS Provider
    |
    +---- Data ---> WireGuard ---> VPN Exit
```

The resulting external IP address may therefore correspond to the VPN while DNS queries may be observed by a different resolver or network path.

Conversely, a DNS query may be associated with a VPN endpoint while the application's data traffic follows another route.

For this reason:

An observed VPN exit IP does not, by itself, prove that DNS queries used the same VPN tunnel.

Likewise:

A DNS resolver observing a VPN-associated source address does not, by itself, prove that all application traffic used that tunnel.

Both planes must be validated independently.

---

# 7. Direct Traffic Flow

Applications that are not assigned to a proxy or VPN route may use the direct network path allowed by the firewall policy.
```
Application
     |
     v
RethinkDNS
     |
     v
Firewall
     |
     v
Direct Network
     |
     v
ISP / Network
     |
     v
Internet
```
Direct routing is not inherently insecure.

Its suitability depends on the application, threat model, DNS policy, network environment, and desired privacy properties.

Applications requiring a VPN exit should therefore be explicitly assigned to the appropriate proxy configuration.

---

# 8. Global WireGuard Traffic Flow

A WireGuard configuration assigned as a general proxy can route traffic from multiple applications through a common encrypted tunnel.

```
Application
     |
     v
RethinkDNS
     |
     v
WireGuard
     |
     v
Encrypted Tunnel
     |
     v
VPN Provider Endpoint
     |
     v
Internet
```

Conceptually:

```
Android
   |
   v
RethinkDNS
   |
   v
[ WireGuard Tunnel ]
   |
   v
VPN Endpoint
   |
   v
Internet
```
The external destination should observe the VPN endpoint rather than the original ISP-facing public address for traffic successfully routed through the tunnel.

This behavior must be independently validated.

----

# 9. Application-Specific WireGuard Flow

RethinkDNS can associate specific applications with dedicated proxy configurations.

Example:
```
                    RethinkDNS
                       |
          +------------+------------+
          |                         |
          v                         v
    General Apps              Application A
          |                         |
          v                         v
     WG-General                WG-Specific
          |                         |
          v                         v
     VPN Exit A                 VPN Exit B
          |                         |
          +------------+------------+
                       |
                       v
                    Internet
```
This allows the same Android device to maintain multiple logical network paths.

The routing policy should be documented at the application level.

Example:
```
Application: Application A
Proxy: WG-Specific
Exit: VPN Provider Endpoint B
Purpose: Application-specific routing
```
----

# 10. Multi-Proxy Traffic Model

The reference deployment can contain several proxy configurations.

A simplified representation is:
```
                         RethinkDNS
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
   General Proxy       Application Proxy       TOR Proxy
        |                    |                    |
        v                    v                    v
   WireGuard A          WireGuard B            TOR
        |                    |                    |
        v                    v                    v
   VPN Exit A           VPN Exit B          TOR Network
```
The important property is that these are separate routing policies.

The architecture does not require all applications to use the same network path.

----

# 11. TOR Traffic Flow

Applications configured to use a TOR proxy follow a separate traffic path.

Conceptually:
```
Browser
   |
   v
RethinkDNS
   |
   v
TOR Proxy
   |
   v
TOR Network
   |
   v
Exit Node
   |
   v
Internet
```
TOR routing should be treated as a separate anonymity-oriented transport and should not automatically be considered equivalent to a WireGuard VPN.

The security and privacy characteristics of the two mechanisms differ.

Applications using TOR should therefore be explicitly identified in the deployment documentation.

----

# 12. Firewall Decision Flow

Before traffic reaches its final route, firewall policy may determine whether the connection is permitted.

Conceptually:
```
Application
     |
     v
RethinkDNS
     |
     v
Firewall Decision
     |
   +---+---+
   |       |
 ALLOW   BLOCK
   |       |
   v       v
Routing   DROP
```
The firewall decision may depend on:

* Application.
* Destination.
* IP address.
* Port.
* Network state.
* Device lock state.
* Configured firewall rules.
* Proxy configuration.
* DNS resolution behavior.

A firewall rule should therefore be evaluated in the context of the complete traffic flow rather than in isolation.

----

# 13. DNS Bypass

DNS bypass represents one of the most important architectural cases.

An application may potentially attempt to use a DNS path different from the configured DNS policy.

The intended architecture is:
```
Application
     |
     v
RethinkDNS
     |
     v
Configured DNS Policy
     |
     v
Configured Resolver
```

An unexpected path may instead look like:

```
Application
     |
     +----------------------+
                            |
                            v
                     Alternative DNS
                            |
                            v
                         Network
```

The second path should only exist when explicitly allowed by the deployment design.

DNS bypass behavior must therefore be validated rather than inferred from normal application connectivity.

----

# 14. Split DNS

Split DNS changes how DNS queries are distributed among available DNS upstreams.

Conceptually:

```
                         DNS Query
                            |
                            v
                       RethinkDNS
                            |
                    +-------+-------+
                    |               |
                    v               v
              Proxy DNS         Global DNS
                    |               |
                    v               v
              DNS Endpoint      DNS Resolver
```

The resulting behavior depends on:

- Split DNS configuration.
- Proxy configuration.
- Application routing.
- DNS bypass rules.
- WireGuard configuration.
- RethinkDNS version.

Split DNS should therefore be documented explicitly in deployment records.

A configuration that changes Split DNS behavior can change the observed DNS source without changing the application's visible IP address.

----

# 15. WireGuard DNS Flow

A WireGuard configuration may provide its own DNS configuration.

Conceptually:

```
Application
     |
     v
RethinkDNS
     |
     v
WireGuard
     |
     +----------> WireGuard DNS
     |
     v
VPN Endpoint
```
This is distinct from:
```
Application
     |
     v
RethinkDNS
     |
     v
Global DNS
    |
    v
Encrypted DNS Provider
```

Which path is selected depends on the active RethinkDNS configuration.

Therefore, the presence of an active WireGuard tunnel does not automatically prove that every DNS query is being resolved through that tunnel.

----

# 16. IPv4 and IPv6 Traffic

The architecture must consider IPv4 and IPv6 separately.

Conceptually:

```
                    Application
                         |
                    RethinkDNS
                         |
              +----------+----------+
              |                     |
              v                     v
            IPv4                  IPv6
              |                     |
              v                     v
          Firewall              Firewall
              |                     |
              v                     v
        Direct / VPN          Direct / VPN
```
A VPN configuration that correctly routes IPv4 traffic may not provide the same behavior for IPv6 unless IPv6 is explicitly supported and configured.

Therefore, IPv4 and IPv6 should be independently validated whenever IPv6 is enabled.

----

# 17. Network Transition Flow

Android devices can change network state between:

- Wi-Fi.
- Mobile data.
- Different Wi-Fi networks.
- Temporary loss of connectivity.
- VPN reconnection.
- Device wake/sleep.

A simplified transition is:
```
Wi-Fi
  |
  v
Network Change
  |
  v
RethinkDNS
  |
  +---- DNS re-evaluation
  |
  +---- Proxy state
  |
  +---- WireGuard state
  |
  +---- Firewall state
  |
  v
New Network Path
```

The expected architecture should recover its intended routing policy after network transitions.

Recovery behavior should be validated independently from normal operation.

----

# 18. Device Lock Flow

The reference firewall configuration may restrict application traffic when the device is locked.

Conceptually:
```
Device Unlocked
      |
      v
Normal Traffic Policy
      |
      v
Application Traffic


Device Locked
      |
      v
Lockdown Firewall Policy
      |
      v
Traffic Restricted
```

The exact behavior depends on the configured RethinkDNS firewall policy.

Applications that require background connectivity should be considered before enabling restrictive lock-state policies.

----

# 19. Failure Scenarios

The architecture must account for component failure.

Possible failures include:

- DNS resolver unavailable.
- WireGuard tunnel unavailable.
- VPN endpoint unavailable.
- Network transition.
- RethinkDNS process failure.
- Application-specific proxy failure.
- DNS configuration failure.
- IPv6 routing inconsistency.

A simplified failure model is:
```
                    Normal Flow
                        |
                        v
                    Component
                      Failure
                        |
              +---------+---------+
              |                   |
              v                   v
          Fail Closed         Fail Open /
                              Alternate Path
```
The resulting behavior depends on the configured policy.

A fallback path should not automatically be considered a leak.

It becomes a security problem when the fallback path violates the intended threat model and is not explicitly understood or controlled.

----

# 20. DNS Failure vs VPN Failure

DNS failure and VPN failure should be analyzed independently.

DNS failure
```
Application
     |
     v
DNS Resolution
     |
     X
Resolver Failure
```
The application may be unable to resolve destinations even if the VPN tunnel itself remains operational.

VPN failure

```
Application
     |
     v
DNS Resolution
     |
     v
Proxy
     |
     X
WireGuard Failure
```

Depending on the configuration, traffic may:

- Stop.
- Retry.
- Use another available DNS or proxy path.
- Fall back to a configured route.

The actual behavior must be tested for the deployed configuration.

-----

# 21. Observability and Validation

Traffic-flow validation should use multiple independent observations.

For example:
```
                    Traffic Test
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      DNS Logs       External IP    Rethink Logs
          |              |              |
          +--------------+--------------+
                         |
                         v
                  Correlated Result
```
Useful observations include:

- DNS-provider query logs when available.
- Packet capture when required by the validation objective.
- Interface-level observations when required.
- RethinkDNS network logs.
- Active WireGuard state.
- VPN endpoint information.
- External IP address.
- DNS leak testing.
- IPv4 connectivity.
- IPv6 connectivity.

No single observation should be treated as proof of the complete traffic path.

----

# 22. Traffic Validation Matrix

The following matrix defines the minimum validation model.

| Traffic Class            | DNS Path                   | Data Path               | Expected Observation                  |
| ------------------------ | -------------------------- | ----------------------- | ------------------------------------- |
| General application      | Configured DNS             | Direct or General Proxy | Consistent with assigned policy       |
| VPN application          | Configured DNS / VPN DNS   | WireGuard               | VPN exit observed                     |
| Application-specific VPN | Configured DNS / proxy DNS | Dedicated WireGuard     | Assigned VPN exit observed            |
| TOR application          | Configured DNS / TOR path  | TOR                     | TOR routing observed                  |
| Blocked application      | Not applicable             | Firewall                | Connection blocked                    |
| DNS bypass attempt       | Configured policy          | Application-dependent   | Unexpected resolver should not appear |
| IPv6 traffic             | Validated separately       | IPv6 route              | Consistent with policy                |
| Network transition       | Re-evaluated               | Re-established route    | Policy restored                       |

This table represents expected behavior, not a guarantee.

Resolver behavior consistent with configured policy

Each row requires validation in the target environment.

----

# 23. Example Reference Flows

## 23.1 General Application

```
Application
    |
    v
RethinkDNS
    |
    +---- DNS ----> Encrypted DNS Provider
    |
    +---- Data ---> General Policy
                       |
                       v
                   WireGuard
                       |
                       v
                  VPN Provider
                       |
                       v
                    Internet
```

----

## 23.2 Application-Specific VPN

```
Application A
    |
    v
RethinkDNS
    |
    +---- DNS ----> Configured DNS
    |
    +---- Data ---> Application Proxy
                       |
                       v
                   WireGuard
                       |
                       v
                  VPN Provider
                       |
                       v
                    Internet
```

----

## 23.3 TOR Browser

```
Browser
   |
   v
RethinkDNS
   |
   +---- DNS ----> Configured DNS
   |
   +---- Data ---> TOR Proxy
                       |
                       v
                   TOR Network
                       |
                       v
                    Internet
```

----

## 23.4 Blocked Application

```
Application
     |
     v
RethinkDNS
     |
     v
Firewall
     |
     X
   BLOCK
```

No successful external connection should occur when the relevant firewall policy is correctly enforced.

----

# 24. Expected Security Properties

The traffic architecture is intended to provide the following properties when correctly configured and validated:

### DNS Policy

DNS requests should follow the configured resolver and filtering policy, subject to explicitly configured exceptions.

### VPN Routing

Applications assigned to a WireGuard proxy should use the corresponding encrypted tunnel.

### Application Segmentation

Applications assigned to different proxy policies should follow their respective network routes.

### Firewall Enforcement

Traffic explicitly blocked by the firewall should not establish the corresponding connection.

### Observability

Relevant DNS and network activity should be visible through the available logging mechanisms.

### Recovery

The intended network policy should be restored following normal network transitions and supported recovery scenarios.

These properties must be demonstrated through validation rather than assumed from configuration alone.

----

# 25. Known Limitations

Traffic behavior may differ according to:

- RethinkDNS version.
- Android version.
- ROM implementation.
- Kernel behavior.
- WireGuard implementation.
- VPN provider.
- DNS provider.
- Application behavior.
- IPv4/IPv6 configuration.
- Network conditions.
- Android battery-management behavior.

Particular attention should be paid to software updates that modify DNS, WireGuard, proxy, firewall, or routing behavior.

Historical testing has demonstrated that different RethinkDNS versions may produce different DNS and proxy-routing behavior.

Consequently, version information is considered part of the traffic-flow model.

----

# 26. Version-Specific Considerations

Traffic behavior may depend on the RethinkDNS software version.

The original architectural baseline was established using:

```
RethinkDNS v0.5.5x
```

Subsequent validation has included:

```
RethinkDNS v0.5.6
```

These versions should not be interpreted as universal or permanent project baselines.

The authoritative version for a specific observed behavior is the version recorded in the corresponding validation report.

When a candidate version is introduced:

1. Preserve the existing configuration.
2. Record the current and candidate versions.
3. Repeat the relevant traffic-flow tests.
4. Compare DNS observations.
5. Compare VPN exit behavior.
6. Compare application-specific routing.
7. Test relevant failure and recovery behavior.
8. Document regressions or behavioral changes.

Version-regression testing is tracked separately in:
```
VAL-003
```

----

# 27. Troubleshooting Model

When an unexpected network result occurs, troubleshooting should proceed from the lowest relevant layer toward the application.

Recommended order:

```
1. Android Network State
          |
          v
2. RethinkDNS State
          |
          v
3. DNS Resolution
          |
          v
4. Firewall Decision
          |
          v
5. Proxy Assignment
          |
          v
6. WireGuard State
          |
          v
7. VPN Endpoint
          |
          v
8. Application Behavior
```
This avoids immediately attributing every networking problem to the VPN or DNS provider.

----

# 28. Traffic-Flow Design Principle

The architecture follows a fundamental principle:

DNS flow and application-data flow must be treated as separate traffic paths until their relationship has been explicitly validated.

A VPN exit IP, DNS resolver result, or RethinkDNS log entry provides useful evidence, but none of these observations alone necessarily proves the complete path of a connection.

Traffic-flow conclusions should therefore be based on correlated observations from multiple layers.

----

# 29. Validation Boundary

This document defines the expected traffic-flow architecture.

It does not certify that the current device configuration implements every flow exactly as described.

Actual behavior must be demonstrated through dedicated validation procedures.

Current validation documents include:

- [`VAL-001`](../validation/VAL-001-dns-validation.md) — DNS Validation
- [`VAL-002`](../validation/VAL-002-network-transition-wireguard-routing.md) — Network Transition & WireGuard Routing Validation
- [`VAL-003`](../validation/VAL-003-version-regression-upgrade-validation.md) — Version Regression & Upgrade Validation

Validation coverage may be distributed across multiple reports.

The absence of a dedicated validation report for a traffic class does not imply that the behavior has been validated.

Additional validation documents may be introduced as testing expands.

----

# 30. Related Documentation

## Architecture

- [`ARCH-001`](ARCH-001-rethinkdns-architecture.md) — RethinkDNS Architecture

## Validation

- [`VAL-001`](../validation/VAL-001-dns-validation.md) — DNS Validation
- [`VAL-002`](../validation/VAL-002-network-transition-wireguard-routing.md) — Network Transition & WireGuard Routing Validation
- [`VAL-003`](../validation/VAL-003-version-regression-upgrade-validation.md) — Version Regression & Upgrade Validation

## Guides

- [`Configuration Recommendations`](../guides/configuration-recommendations.md)

## References

- [`Recommended Blocklists`](../references/recommended-blocklists.md)

## Module Index

- [`RethinkDNS Documentation`](../README.md)

----

# 31. Document Status

**Current status:** Published

ARCH-002 defines the expected traffic-flow architecture for the RethinkDNS module of Android OPSEC Hardening.

Individual traffic paths and security properties are validated separately through the corresponding `VAL-XXX` documents.

Publishing this architecture does not imply that every traffic class, failure condition, network transition, DNS path, proxy path, or IPv4/IPv6 scenario described in this document has been validated.

Material changes to expected traffic behavior should be documented and reviewed before being incorporated into this reference.

----

# Architectural Principle

A network path should be considered verified only when the expected behavior has been observed and correlated across the relevant layers.

# RethinkDNS Configuration Recommendations

## 1. Purpose

This document provides configuration recommendations for deploying RethinkDNS as the primary network-control layer of the Android OPSEC Hardening architecture.

The recommendations are based on the architecture documented by the project and on behavior observed during validation.

They should not be interpreted as universal settings for every Android device, ROM, network, DNS provider, or VPN provider.

Configuration changes should be validated after major updates to:

- Android
- Custom ROMs
- RethinkDNS
- VPN applications
- WireGuard configurations
- DNS providers

---

## 2. Recommended Architecture

The recommended logical architecture is:

```
Android Application
        |
        v
    RethinkDNS
        |
        +---- Firewall Policy
        |
        +---- Encrypted DNS
        |
        +---- WireGuard Routing
                  |
                  v
               Internet
```

RethinkDNS should remain the central policy and visibility layer when
this architecture is used.

---

## 3. DNS Configuration

### Recommended Transport

Use encrypted DNS whenever possible.

Preferred transports:

- DNS-over-TLS (DoT)
- DNS-over-HTTPS (DoH)

Avoid relying on unencrypted DNS when the objective is to maintain a privacy-oriented configuration.

### DNS Providers

Providers evaluated or used within the project include:

- NextDNS
- modDNS

Other encrypted DNS providers may also be compatible.

Provider selection should be treated independently from WireGuard routing.

A DNS provider should ideally provide:

- Encrypted DNS transport
- Reliable availability
- Clear logging controls
- Configurable filtering
- Reasonable privacy guarantees
- Support for custom policies when required

---

## 4. DNS Configuration Strategy

Avoid unnecessary resolver complexity.

Where possible, maintain one clearly defined primary DNS path and validate that applications are not unexpectedly falling back to another resolver.

When changing DNS providers:

1. Apply the new resolver configuration.
2. Generate new DNS traffic.
3. Inspect RethinkDNS DNS logs.
4. Confirm the expected encrypted transport.
5. Confirm the expected resolver.
6. Check for unexpected fallback behavior.

Do not assume that successful web browsing alone proves that the intended resolver is being used.

---

## 5. Split DNS

Split DNS should only be enabled when the architecture explicitly requires different DNS resolution paths.

Introducing multiple resolver paths increases configuration complexity and can make troubleshooting more difficult.

When Split DNS is used, document:

- Which applications use each resolver.
- Which network condition activates each path.
- Expected fallback behavior.
- Interaction with WireGuard tunnels.

Any change to Split DNS behavior should be followed by DNS validation.

---

## 6. WireGuard Configuration

RethinkDNS can be used to route applications through WireGuard proxies.

Recommended practices:

- Assign tunnels intentionally.
- Document per-application assignments.
- Avoid unnecessary overlapping routing rules.
- Verify routing after changing tunnel assignments.
- Validate behavior after RethinkDNS upgrades.
- Confirm both TCP and UDP traffic when relevant.

Application routing should be verified through observed connections rather than inferred only from the configuration screen.

---

## 7. WireGuard Transition Validation

When changing the WireGuard proxy assigned to an application, generate new connections and verify the proxy attribution reported by RethinkDNS.

A validated transition in this project demonstrated:

```
wg16
  |
  v
wg17
  |
  v
wg16
```

This behavior is documented in:

`VAL-002 — Network Transition & WireGuard Routing Validation`

The result applies to the tested configuration and should not be interpreted as a universal guarantee for every RethinkDNS release or network condition.

---

## 8. Firewall Recommendations

Use firewall policies to reduce unnecessary application connectivity.

Recommended baseline controls include:

- Block unwanted application traffic.
- Restrict applications that do not require network access.
- Review unexpected outbound destinations.
- Block insecure HTTP traffic when compatibility allows.
- Avoid broad allow rules when narrower policies are sufficient.

### Insecure HTTP

Blocking outbound TCP/80 can reduce accidental use of unencrypted HTTP.

The project configuration includes a policy blocking insecure HTTP traffic.

This behavior was observed during VAL-002 when an HTTP request over TCP/80 was blocked by RethinkDNS.

Applications that legitimately depend on HTTP may require exceptions.

---

## 9. Per-Application Policy

Applications should be evaluated individually rather than assuming that one routing policy is appropriate for the entire device.

Possible application policies include:

```
Application
    |
    +---- Directly restricted
    |
    +---- Standard WireGuard route
    |
    +---- Dedicated WireGuard route
    |
    +---- Tor / privacy route
    |
    +---- Network access blocked
```

The exact policy depends on the application's purpose and threat model.

Applications handling sensitive traffic may justify stronger isolation, while applications requiring compatibility may need less restrictive policies.

---

## 10. HTTP/3 and UDP/443

Modern browsers and applications may use HTTP/3 over QUIC.

This commonly introduces UDP/443 traffic in addition to conventional HTTPS over TCP/443.

Do not treat UDP/443 as inherently suspicious.

Instead:

1. Identify the application.
2. Identify the destination.
3. Verify the routing path.
4. Determine whether the traffic is consistent with expected
   application behavior.

VAL-002 observed Firefox UDP/443 traffic routed through the selected WireGuard proxy.

---

## 11. Network Log Monitoring

RethinkDNS network logs are useful for validating:

- Application identity
- Destination domain
- Destination IP
- TCP/UDP protocol
- Destination port
- Firewall decisions
- WireGuard proxy attribution

Important configuration changes should be followed by log inspection.

Particular attention should be given to traffic occurring immediately before and after:

- Network transitions
- VPN changes
- WireGuard reassignment
- DNS changes
- RethinkDNS upgrades

---

## 12. DNS Log Monitoring

DNS logs should be periodically reviewed for:

- Unexpected resolvers
- Unexpected domains
- Blocked telemetry
- DNS fallback
- Application-specific DNS activity
- Resolution errors
- Unusual newly observed domains

A DNS response such as HTTPS/SVCB returning no usable record should not automatically be interpreted as a complete DNS failure.

Correlate DNS observations with successful A/AAAA resolution and subsequent network connections.

---

## 13. VPN Provider Considerations

The project does not require a single VPN provider.

Providers used or evaluated within the broader project include:

- Mullvad
- IVPN
- Proton VPN

Selection criteria should include:

- WireGuard support
- Independent security audits
- Transparent privacy policy
- Minimal application telemetry
- Suitable jurisdiction and threat-model considerations
- Stable Android support
- Ability to obtain standard WireGuard configurations when required

Provider reputation alone does not validate the local routing architecture.

The actual traffic path should still be tested.

---

## 14. Blocklist Strategy

Avoid enabling large numbers of overlapping blocklists without evaluating their effect.

A balanced strategy is preferable:

```
Base privacy protection
        +
Telemetry reduction
        +
Threat-oriented filtering
        +
Small targeted exceptions
```

Aggressive filtering may cause:

- Application failures
- Broken authentication
- Missing push notifications
- Media playback failures
- Update failures
- Excessive false positives

See:

`../references/recommended-blocklists.md`

for blocklist-specific recommendations.

---

## 15. Allowlist Strategy

Allowlisting should be targeted and evidence-based.

Do not allow entire vendor ecosystems simply because one application stops working.

Instead:

1. Identify the blocked domain.
2. Determine which application generated the request.
3. Investigate its purpose.
4. Temporarily allow it when necessary.
5. Verify whether functionality returns.
6. Document permanent exceptions.

Common functionality requiring careful validation includes:

- Push notifications
- Authentication
- Messaging
- Application updates
- Media delivery
- CAPTCHA services

---

## 16. Upgrade Strategy

RethinkDNS upgrades should be treated as potential regression boundaries.

Before upgrading:

- Preserve the current configuration.
- Record the installed version.
- Document important WireGuard assignments.
- Record the active DNS configuration.
- Preserve relevant firewall settings.

After upgrading, validate:

- RethinkDNS startup
- DNS resolution
- Firewall enforcement
- WireGuard startup
- Application assignments
- TCP routing
- UDP routing
- Network transitions

Version-specific behavior should be documented separately from the general architecture.

---

## 17. Evidence and Privacy

Screenshots intended for public documentation should be reviewed before publication.

Redact:

- DNS profile identifiers
- WireGuard private keys
- Authentication credentials
- Personal identifiers
- Private configuration secrets
- Sensitive network information when applicable

Use:

```
<REDACTED>
```

where removing a sensitive value does not destroy the technical value of the evidence.

Do not redact identifiers such as local test labels (`wg16`, `wg17`) when they are required to understand the validation and do not contain credentials.

---

## 18. Validation Principle

The project follows the principle:

```
Configured
    !=
Validated
```

A security control should not be considered validated solely because it is enabled.

Where practical, confirm expected behavior through:

- RethinkDNS network logs
- RethinkDNS DNS logs
- External IP verification
- Controlled traffic generation
- Reproducible transition testing

Stronger claims, such as absolute zero-leak guarantees, require packet-level or interface-level validation beyond application logs.

---

## 19. Recommended Baseline

A practical baseline for this architecture is:

| Component | Recommendation |
|---|---|
| Network controller | RethinkDNS |
| DNS transport | Encrypted DoT or DoH |
| DNS provider | Policy-dependent |
| Firewall | Enabled |
| HTTP/80 blocking | Recommended where compatible |
| WireGuard | Per-app or policy-based |
| Traffic inspection | Enabled during validation |
| DNS inspection | Enabled during validation |
| Split DNS | Only when explicitly required |
| Configuration backup | Before major upgrades |
| Regression validation | After significant releases |

The final configuration should always be adapted to the device, applications, network environment, and threat model.

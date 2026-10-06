# LAB-001 — SOCKS5 Baseline Routing Validation

**Status:** IN PROGRESS / PARTIALLY VALIDATED

## 1. Objective

Determine the observable behavior of Android application traffic when
RethinkDNS forwards traffic through a SOCKS5 proxy provided by
hev-socks5-server on a controlled Linux host.

## 2. Baseline topology

```text
Android Device
      |
      v
Applications
      |
      v
RethinkDNS
Firewall + DNS
      |
      v
SOCKS5
      |
      v
hev-socks5-server
Linux Host
      |
      v
Internet
```

## 3. Research questions

LAB-001 will determine:

- Whether TCP traffic traverses the SOCKS5 proxy.
- Whether UDP traffic traverses or behaves differently.
- Which public IP address is observed externally.
- How DNS resolution behaves while SOCKS5 is enabled.
- How IPv4 and IPv6 behave.
- Whether RethinkDNS firewall rules remain effective.
- What happens if the SOCKS5 service becomes unavailable.
- Whether observable direct-routing bypass occurs.

## 4. Validation state

Validation is evidence-scoped. Routing properties marked as PASS,
CHARACTERIZED, or PARTIAL below are supported by reviewed LAB-001A and
LAB-001B evidence. Properties that remain NOT RUN must not be treated as
validated.

```text
Configured != Validated
```

## 5. Planned test matrix

| Test | Purpose | State |
|---|---|---|
| T01 | SOCKS5 TCP connectivity | PASS |
| T02 | Public exit IP observation | NOT RUN |
| T03 | DNS route validation | PARTIAL |
| T04 | UDP behavior | PASS |
| T05 | IPv4 / IPv6 behavior | CHARACTERIZED |
| T06 | RethinkDNS firewall persistence | PARTIAL |
| T07 | SOCKS5 failure behavior | NOT RUN |
| T08 | RethinkDNS restart behavior | NOT RUN |
| T09 | Network transition behavior | NOT RUN |
| T10 | Direct-routing bypass attempt | NOT RUN |

## 6. Failure classification

Failure testing will distinguish between:

```text
FAIL-CLOSED
SOCKS5 unavailable
        |
        X
   traffic blocked
```

and:

```text
FAIL-OPEN
SOCKS5 unavailable
        |
        +------> direct network access
```

A reproducible fail-open condition affecting protected traffic should be
treated as an OPSEC-relevant finding.

## 7. Evidence

Evidence will be stored under:

```text
docs/labs/socks5/evidence/LAB-001/
```

Current reviewed evidence reports:

- `LAB-001A-linux-socks5-baseline.md`
  - Linux HEV source/build baseline.
  - Listener and authentication validation.
  - Positive SOCKS5 TCP control.
  - Two-leg Linux TCP traffic observation.

- `LAB-001B-android-rethink-hev-routing.md`
  - Android / RethinkDNS LAN integration.
  - Private-IP routing behavior.
  - Authenticated Android-to-HEV TCP.
  - Two-leg TCP correlation.
  - SOCKS5 UDP ASSOCIATE and UDP relay validation.
  - Two-leg UDP correlation.
  - IPv4 / IPv6 behavior and IPv4-only A/B validation.

LAB-001A and LAB-001B are evidence phases supporting the master
T01-T10 validation matrix. A PASS in one phase does not imply that
unrelated master tests have been executed.

Evidence may include sanitized:

- packet captures
- tcpdump observations
- RethinkDNS logs
- SOCKS5 server logs
- DNS observations
- public-IP verification
- screenshots
- test notes

Sensitive identifiers, credentials, user-attributable public addresses,
and unrelated traffic must be sanitized before publication.

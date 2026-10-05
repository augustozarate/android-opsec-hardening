# LAB-001 — SOCKS5 Baseline Routing Validation

**Status:** PLANNED / NOT VALIDATED

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

No routing property described by this document should be considered
validated until supporting evidence has been collected and reviewed.

```text
Configured != Validated
```

## 5. Planned test matrix

| Test | Purpose | State |
|---|---|---|
| T01 | SOCKS5 TCP connectivity | NOT RUN |
| T02 | Public exit IP observation | NOT RUN |
| T03 | DNS route validation | NOT RUN |
| T04 | UDP behavior | NOT RUN |
| T05 | IPv4 / IPv6 behavior | NOT RUN |
| T06 | RethinkDNS firewall persistence | NOT RUN |
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

Evidence may include sanitized:

- packet captures
- tcpdump observations
- RethinkDNS logs
- SOCKS5 server logs
- DNS observations
- public-IP verification
- screenshots
- test notes

Sensitive identifiers, credentials, public addresses, and unrelated traffic
must be sanitized before publication.

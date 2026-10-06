# LAB-001 Evidence

This directory stores sanitized evidence associated with
LAB-001 — SOCKS5 Baseline Routing Validation.

Evidence is organized into explicit validation phases. These phase
identifiers support the master T01-T10 test matrix defined in:

`docs/labs/socks5/LAB-001-socks5-baseline.md`

## Reviewed evidence

### LAB-001A — Linux SOCKS5 baseline

File:

`LAB-001A-linux-socks5-baseline.md`

Validated or characterized:

- pinned HEV source and reproducible local build
- loopback listener behavior
- SOCKS5 authentication controls
- positive TCP proxy control
- Linux-side two-leg traffic observation
- environmental DNS behavior

Raw packet captures remain local.

### LAB-001B — Android / RethinkDNS / HEV routing

File:

`LAB-001B-android-rethink-hev-routing.md`

Validated or characterized:

- bridged Android-to-Kali LAN reachability
- RethinkDNS private-IP routing behavior
- authenticated Android-to-HEV SOCKS5 TCP
- two-leg TCP traffic correlation
- deterministic SOCKS5 UDP relay
- UDP ASSOCIATE behavior
- Android-to-HEV UDP transport
- HEV-to-Internet UDP transport
- IPv4 / IPv6 gateway behavior
- RethinkDNS Automatic versus IPv4-only behavior

Raw packet captures remain local.

## Identifier contract

LAB-001A and LAB-001B identify evidence phases.

The master LAB-001 document retains T01-T10 as the authoritative
research/test matrix.

Evidence claims must therefore remain scoped to the specific property
actually demonstrated.

Configured does not imply validated.

## Evidence handling

Published evidence may include sanitized:

- packet-capture observations
- tcpdump summaries
- RethinkDNS observations
- SOCKS5 server logs
- DNS observations
- routing observations
- screenshots
- hashes of locally retained evidence
- test notes

Raw captures containing credentials, user-attributable identifiers,
private payloads, or unrelated traffic should not be published without
sanitization.

Credentials and runtime secret material must never be committed.

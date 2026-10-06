# LAB-002 Evidence

This directory stores sanitized evidence for:

LAB-002 — RethinkDNS WireGuard + SOCKS5 Interaction

Evidence must be associated with an explicit LAB-002 phase.

Expected phases include:

~~~text
LAB-002A  Known-good LAB-001B reproduction
LAB-002B  WireGuard + SOCKS5 configuration interaction
LAB-002C  Android-to-HEV traffic observation
LAB-002D  HEV outbound observation
LAB-002E  Public-egress comparison
LAB-002F  DNS behavior comparison
LAB-002G  UDP behavior comparison
LAB-002H  SOCKS5 failure behavior
LAB-002I  WireGuard failure behavior
LAB-002J  Fail-open / bypass characterization
~~~

## Evidence handling

Raw packet captures remain local.

Do not commit:

- SOCKS5 credentials
- WireGuard private keys
- WireGuard configuration containing secrets
- credential-bearing HEV configuration
- raw PCAP or PCAPNG files
- runtime PID files
- unrelated packet payloads

Published evidence may contain sanitized:

- packet summaries
- nftables counters
- HEV logs
- RethinkDNS observations
- routing observations
- DNS observations
- public-egress observations
- screenshots
- hashes of locally retained evidence

## Validation rule

Evidence claims must remain scoped to the specific property actually
observed.

~~~text
Configured != Validated
Observed != Persisted
One successful flow != universal routing behavior
~~~

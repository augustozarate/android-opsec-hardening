# SOCKS5 Routing Labs

This module evaluates SOCKS5 as an optional routing layer within the
Android OPSEC Hardening project.

The initial research combines:

- Android
- RethinkDNS
- SOCKS5
- hev-socks5-server
- Linux network observation
- controlled traffic validation

SOCKS5 is treated as experimental infrastructure.

It does not replace the validated RethinkDNS, DNS, firewall, or WireGuard
architecture.

## Research progression

```text
LAB-001
Android -> RethinkDNS -> SOCKS5 -> Linux Gateway -> Internet

LAB-002
Android -> RethinkDNS -> SOCKS5 -> Linux Gateway -> WireGuard -> Internet

LAB-003
Policy-based and multi-route experiments

LAB-004
Failure, bypass, and leak validation
```

A SOCKS5 configuration must not be considered an OPSEC improvement until
its routing behavior, DNS behavior, failure mode, IPv4/IPv6 behavior, and
possible bypass paths have been validated.

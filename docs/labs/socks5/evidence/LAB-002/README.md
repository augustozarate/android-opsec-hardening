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

## Recorded evidence

### LAB-002A

- `LAB-002A-known-good-baseline-reproduction.md`
  - known-good SOCKS5 baseline reproduction
  - initial failure caused by A50 IPv4 address drift
  - stale nftables source-IP ACL identified
  - TCP/1080 and UDP/1081 operation restored after ACL correction
  - generic deny policy preserved
  - WireGuard not introduced

### LAB-002B

- `LAB-002B-wireguard-socks5-configuration-coexistence.md`
  - WireGuard UI state became ON while SOCKS5 remained ON
  - configuration behavior classified B1
  - no warning or incompatibility message observed
  - no deliberate application workload generated
  - no HEV traffic observed during the configuration-only window
  - packet-routing order remains unvalidated

### LAB-002C

- `LAB-002C-android-to-hev-combined-state.md`
  - controlled page load completed with WireGuard ON + SOCKS5 ON
  - no A50-to-HEV TCP/1080 traffic observed
  - no A50-to-HEV UDP/1081 traffic observed
  - no new HEV SOCKS5 events observed
  - zero matching packets in the scoped first-leg capture
  - HEV path not observed for the controlled workload
  - WireGuard transport not yet independently validated

### LAB-002D

- `LAB-002D-hev-outbound-transport-observation.md`
  - controlled page load completed with WireGuard ON + SOCKS5 ON
  - A50 current IPv4 observed as 10.36.136.41
  - LAB nftables state recovered before testing
  - no A50-to-HEV TCP/1080 or UDP/1081 activity observed
  - no new HEV events or HEV destinations observed
  - first-leg capture contained zero packets
  - two Kali external packets were observed and characterized as NTP background traffic
  - no HEV-attributable outbound transport observed
  - WireGuard transport remains independently unvalidated
  - 30-second successful timing validation with stable A50 IPv4/MAC still produced no HEV activity
  - successful example.com request remained at zero TCP/1080, UDP/1081, HEV-log, and first-leg PCAP activity
  - failed api.ipify.org request retained separately as auxiliary evidence and not used for the PASS classification

### LAB-002E

- `LAB-002E-public-egress-comparison.md`
  - A50 public IPv4 reached three-provider consensus
  - Kali public IPv4 reached three-provider consensus
  - A50 and Kali public egress were different
  - raw public IPv4 values intentionally omitted from committed evidence
  - no TCP/1080 or UDP/1081 HEV activity observed
  - no new HEV log events observed
  - classified DIFFERENT_PUBLIC_EGRESS_WITHOUT_HEV
  - result is strong operational evidence of a non-HEV path
  - WireGuard transport is not yet treated as independently proven

### LAB-002F

- `LAB-002F-dns-behavior-comparison.md`
  - unique controlled DNS hostname observed in RethinkDNS
  - Brave identified as the requesting application
  - IPv4 and HTTP Service Binding query entries observed
  - WG association visible in RethinkDNS UI
  - resolver metadata referenced `wg15:10.2.0.1:53`
  - no TCP/1080 or UDP/1081 HEV activity observed
  - no new HEV log events observed
  - A50-to-HEV capture contained zero packets
  - zero port 53/853 visibility from Kali retained only as a scoped observation
  - original manual NOT_FOUND preserved and superseded through explicit visual reconciliation
  - classified RETHINK_DNS_OBSERVED_WITHOUT_HEV

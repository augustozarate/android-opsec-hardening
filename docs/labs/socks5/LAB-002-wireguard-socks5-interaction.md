# LAB-002 — RethinkDNS WireGuard + SOCKS5 Interaction

**Status:** PLANNED / NOT VALIDATED

## 1. Objective

Determine the observable routing behavior when RethinkDNS is configured
with both WireGuard and a remote authenticated HEV SOCKS5 proxy.

The experiment must distinguish configuration state from validated
traffic behavior.

~~~text
Configured != Validated
~~~

## 2. Baseline inherited from LAB-001

LAB-002 starts from the validated LAB-001B environment:

~~~text
Android device
Samsung Galaxy A50
        |
        v
RethinkDNS v0.5.7
        |
        v
Authenticated SOCKS5
        |
        v
HEV on Kali
10.36.136.33
        |
        v
Internet
~~~

Validated LAB-001B properties include:

- authenticated Android-to-HEV SOCKS5 TCP
- SOCKS5 UDP ASSOCIATE
- deterministic HEV UDP relay
- two-leg TCP observation
- two-leg UDP observation
- IPv4-only RethinkDNS operation for the tested gateway
- private-IP bypass required for direct A50-to-Kali reachability

## 3. LAB-002 research questions

LAB-002 will determine:

- whether WireGuard and SOCKS5 can be enabled simultaneously
- whether one transport disables or overrides the other
- whether transport ordering is observable
- whether SOCKS5 control traffic itself traverses WireGuard
- whether application traffic is split between transports
- whether UDP behavior changes
- whether DNS behavior changes
- whether public egress changes
- whether Proxy Lockdown behavior changes
- whether failure of either transport produces fail-open behavior
- whether direct-routing bypass becomes observable

## 4. Candidate routing models

The following are hypotheses only.

### Model A — SOCKS5 only

~~~text
Application
    |
    v
RethinkDNS
    |
    v
SOCKS5
    |
    v
HEV
    |
    v
Internet
~~~

### Model B — WireGuard only

~~~text
Application
    |
    v
RethinkDNS
    |
    v
WireGuard
    |
    v
Internet
~~~

### Model C — WireGuard underlay for the SOCKS5 path

Hypothesis: the connection from the RethinkDNS SOCKS5 client to the
remote HEV endpoint is itself transported through WireGuard.

~~~text
Application
    |
    v
RethinkDNS
    |
    v
SOCKS5 client
    |
    v
WireGuard transport
    |
    v
HEV endpoint
    |
    v
Internet
~~~

### Model D — WireGuard traffic relayed through SOCKS5

Hypothesis: RethinkDNS first creates or selects a WireGuard transport
and then carries that transport through the SOCKS5 relay path.

~~~text
Application
    |
    v
RethinkDNS
    |
    v
WireGuard transport
    |
    v
SOCKS5 relay
    |
    v
HEV endpoint
    |
    v
Internet
~~~

### Model E — Mutual exclusion

~~~text
RethinkDNS
    |
    +-- SOCKS5 active
    |
    X
    |
    +-- WireGuard unavailable

or

RethinkDNS
    |
    +-- WireGuard active
    |
    X
    |
    +-- SOCKS5 unavailable
~~~

### Model F — Policy split

~~~text
Application set A
      |
      v
   SOCKS5
      |
      v
     HEV
      |
      v
  Internet

Application set B
      |
      v
  WireGuard
      |
      v
  Internet
~~~

### Model G — Fail-open / bypass condition

~~~text
Protected application
        |
        v
RethinkDNS
        |
        X
Configured proxy path unavailable
        |
        +------> direct network path
~~~

No model is considered valid until traffic evidence supports it.

## 5. Planned phases

| Phase | Purpose | State |
|---|---|---|
| LAB-002A | Reproduce LAB-001B known-good baseline | PASS |
| LAB-002B | Enable WireGuard with SOCKS5 configured | PASS |
| LAB-002C | Observe Android-to-HEV traffic | PASS |
| LAB-002D | Observe HEV outbound transport | PASS |
| LAB-002E | Public-egress comparison | PASS |
| LAB-002F | DNS behavior comparison | PASS |
| LAB-002G | UDP behavior comparison | NOT RUN |
| LAB-002H | SOCKS5 failure behavior | NOT RUN |
| LAB-002I | WireGuard failure behavior | NOT RUN |
| LAB-002J | Fail-open / bypass characterization | NOT RUN |

## 6. Safety and evidence rules

LAB-002 must preserve the LAB-001 evidence-handling rules.

Do not commit:

- SOCKS5 credentials
- WireGuard private keys
- WireGuard configuration containing secrets
- raw PCAP files
- runtime PID files
- unrelated packet payloads

Packet captures remain local unless explicitly sanitized.

Published evidence may include:

- sanitized packet summaries
- nftables counters
- HEV logs
- RethinkDNS observations
- routing observations
- public-egress observations
- SHA-256 hashes of locally retained captures
- screenshots

## 7. Initial experimental constraint

The known-good LAB-001B configuration must remain unchanged until
LAB-002A reproduces the baseline.

WireGuard must not be enabled until that reproduction is complete.

This prevents a LAB-002 transport change from invalidating the
reference state before it has been re-established.

## 8. Initial known-good reference state

The initial LAB-002A reference state is expected to preserve the final
LAB-001B configuration:

~~~text
RethinkDNS                  ON
SOCKS5                      ON
WireGuard                   OFF
Proxy Lockdown              ON
Do not route private IPs    ON
Android Always-on VPN       ON
Android VPN Lockdown        OFF
RethinkDNS IP version       IPv4
~~~

HEV reference endpoint:

~~~text
Kali:
10.36.136.33

SOCKS5 TCP:
10.36.136.33:1080

SOCKS5 UDP relay:
10.36.136.33:1081
~~~

Authentication remains configured locally but credential values must not
be recorded in Git.

## 9. Validation principle

LAB-002 will distinguish among:

~~~text
CONFIGURED
The UI or configuration claims a transport is active.

OBSERVED
Traffic attributable to that transport is directly seen.

CORRELATED
Both sides of the routing path can be temporally or numerically linked.

VALIDATED
The tested property is supported by repeatable evidence.

NOT OBSERVED
The expected event did not appear during the observation window.

NOT RUN
The test has not yet been executed.
~~~

Absence of evidence during a short capture window must not automatically
be treated as evidence of absence.

## 10. Scope boundary

LAB-002 does not replace or rewrite LAB-001.

LAB-001 remains the baseline SOCKS5 validation series.

LAB-002 investigates only the additional behavior introduced by
WireGuard interaction with the already validated SOCKS5 path.

Results from LAB-002 must therefore be compared against LAB-001B rather
than silently incorporated into the previous baseline.

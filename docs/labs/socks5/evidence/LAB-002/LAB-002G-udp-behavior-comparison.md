# LAB-002G — UDP Behavior Comparison

**Status:** PASS / APP UDP OBSERVED WITHOUT HEV

## 1. Objective

Characterize application UDP behavior while RethinkDNS displays both
WireGuard and SOCKS5 as enabled.

The phase specifically asks whether application UDP can be demonstrated
while the HEV SOCKS5 path remains observable but unused.

## 2. Tested state

The A50 remained in the established combined state:

~~~text
A50 IPv4                   10.36.136.46
A50 MAC                    0a:13:ee:1e:7d:3b
RethinkDNS                 ON
WireGuard                  ON
SOCKS5                     ON
Proxy Lockdown             ON
Do not route private IPs   ON
Android Always-on VPN      ON
Android VPN Lockdown       OFF
Rethink IP version         IPv4
~~~

HEV remained active and listening on Kali.

The LAB firewall retained authorization for the current A50 identity on:

~~~text
TCP/1080
UDP/1081
~~~

with generic deny rules preserved.

## 3. Controlled workload

A fresh Brave session loaded a nonce-qualified Cloudflare trace URL.

The application workload completed successfully.

The RethinkDNS network log was then inspected directly rather than
inferring transport from successful page loading.

## 4. Application UDP observation

RethinkDNS showed an application flow for:

~~~text
application: Brave
domain:      www.cloudflare.com
transport:   UDP
port:        443
~~~

The flow was permitted.

RethinkDNS additionally displayed the application-flow association:

~~~text
Por proxy: wg16
~~~

The identifier `wg16` is recorded exactly as observed.

It is treated as an internal RethinkDNS/WireGuard-associated identifier
and is not assumed to remain numerically stable across phases,
subsystems, reconnects, or runtime sessions.

## 5. HTTP/3 corroboration

The controlled Cloudflare trace response reported:

~~~text
http=http/3
~~~

This independently corroborates that the controlled workload reached an
HTTP/3-capable application path.

The transport classification for LAB-002G nevertheless relies primarily
on the explicit RethinkDNS network-log observation of UDP/443.

## 6. Concurrent TCP observation

RethinkDNS also showed a TCP/443 flow for the same Brave /
www.cloudflare.com workload.

That TCP flow was likewise associated with:

~~~text
wg16
~~~

The presence of TCP does not invalidate the UDP observation.

LAB-002G does not claim that the workload used only UDP.

It establishes that application UDP was demonstrably present.

## 7. HEV / SOCKS5 observation

During and after the controlled workload:

~~~text
TCP/1080 packet delta: 0
TCP/1080 byte delta:   0

UDP/1081 packet delta: 0
UDP/1081 byte delta:   0

New HEV log lines:     0

New HEV UDP event:     NO
New HEV TCP event:     NO
~~~

The dedicated A50-to-HEV capture contained:

~~~text
total packets:         0
TCP/1080 packets:      0
UDP/1081 packets:      0
~~~

PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

The raw PCAP remains local and is not committed.

## 8. Timing

HEV was observed after the workload for approximately:

~~~text
10 seconds
20 seconds
~~~

No delayed HEV event appeared in either observation point.

## 9. Classification

LAB-002G is classified:

~~~text
PASS / APP UDP OBSERVED WITHOUT HEV
~~~

Machine classification:

~~~text
APP_UDP_OBSERVED_WITHOUT_HEV
~~~

The tested workload therefore demonstrated application UDP while no
HEV/SOCKS5 activity was observed.

## 10. WireGuard-associated evidence

The exact UDP/443 flow was displayed by RethinkDNS with:

~~~text
wg16
~~~

This is operational evidence compatible with the UDP application flow
being associated with the configured WireGuard path.

Combined with the absence of:

~~~text
UDP/1081 traffic
HEV UDP events
A50-to-HEV packets
~~~

the evidence materially weakens the model in which SOCKS5/HEV carried
the tested UDP flow.

This remains operational evidence rather than cryptographic proof of the
WireGuard tunnel.

## 11. Relationship to LAB-002F

LAB-002F observed WireGuard-associated DNS metadata including:

~~~text
WG
wg15:10.2.0.1:53
~~~

LAB-002G observed:

~~~text
application UDP/443
wg16 association
~~~

The differing numeric identifiers are recorded as phase-local runtime
observations.

No assertion is made that wg15 and wg16 must represent identical
internal objects or remain stable across RethinkDNS subsystems.

## 12. Cross-phase evidence

LAB-002B established:

~~~text
WireGuard ON
SOCKS5 ON
configuration coexistence
~~~

LAB-002C established:

~~~text
successful application workload
A50-to-HEV path not observed
~~~

LAB-002D established:

~~~text
no HEV-attributable outbound relay
no delayed HEV activity
~~~

LAB-002E established:

~~~text
A50 public egress != Kali/HEV public egress
HEV activity = 0
~~~

LAB-002F established:

~~~text
controlled DNS query visible in RethinkDNS
WireGuard-associated DNS metadata
HEV activity = 0
~~~

LAB-002G now adds:

~~~text
application UDP/443 explicitly observed
WireGuard-associated application-flow metadata
HEV UDP path = 0
~~~

The cumulative evidence increasingly supports the model that WireGuard
is the effective path for the tested traffic while SOCKS5 remains
configured but is not selected for those flows.

## 13. Interpretation boundary

LAB-002G does not independently prove:

- a cryptographically validated WireGuard handshake
- that every UDP flow uses WireGuard
- that SOCKS5 can never transport UDP
- that UDP ASSOCIATE is unavailable
- that TCP and UDP always use identical policy
- that `wg16` is a persistent interface identifier
- a universal precedence rule between WireGuard and SOCKS5

The precise result is:

~~~text
application UDP observed
+
WireGuard-associated RethinkDNS metadata
+
zero HEV/SOCKS5 activity
~~~

for the tested workload.

## 14. Evidence identity

The local privacy-preserving runtime summary is retained outside Git.

SHA-256:

~~~text
6e9fa114930cb6d520c14d770631f6115dd828093b726f17f040637e2d3e2a30
~~~

No raw PCAP is committed.

## 15. Next phase

LAB-002H will characterize SOCKS5 failure behavior.

That phase will deliberately alter availability of the HEV/SOCKS5
backend while preserving the combined RethinkDNS configuration as much
as possible.

The objective will be to determine whether loss of HEV affects traffic
that currently appears to be using the WireGuard-associated path.

No fail-open or fail-closed conclusion will be assumed before the
controlled failure test.

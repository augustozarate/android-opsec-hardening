# LAB-002E — Public Egress Comparison

**Status:** PASS / DIFFERENT PUBLIC EGRESS WITHOUT HEV

## 1. Objective

Compare the public IPv4 egress observed from the Android A50 with the
public IPv4 egress observed from Kali/HEV while RethinkDNS shows both
WireGuard and SOCKS5 enabled.

The purpose is to determine whether successful A50 Internet traffic is
consistent with exiting through Kali/HEV or through a different path.

This phase does not treat public-IP difference alone as cryptographic
proof of WireGuard transport.

## 2. Tested state

The tested A50 state was:

~~~text
A50 private IPv4           10.36.136.46
A50 MAC                    0a:13:ee:1e:7d:3b
RethinkDNS                 ON
WireGuard                  ON
SOCKS5                     ON
Rethink IP version         IPv4
~~~

The A50 IPv4/MAC identity remained stable for the test.

HEV was active and listening on TCP/1080.

The LAB firewall authorized the current A50 IPv4 for:

~~~text
TCP/1080
UDP/1081
~~~

while preserving the generic deny rules.

## 3. Privacy handling

Raw public IPv4 values are intentionally omitted from committed
evidence.

The comparison preserves only:

~~~text
provider validity
provider consensus
A50-vs-Kali relation
HEV activity counters
classification
~~~

No public IPv4 address is recorded in this report.

## 4. A50 egress observation

Three independent public-egress providers were observed from the A50:

~~~text
Cloudflare
ifconfig.me
icanhazip
~~~

All three displayed the same IPv4.

A50 provider consensus:

~~~text
PASS
~~~

The three-provider result was visually confirmed during the controlled
test.

## 5. Kali egress observation

The same three provider classes were queried from Kali over IPv4:

~~~text
Cloudflare
ifconfig.me
icanhazip
~~~

All three returned valid IPv4 responses and agreed.

Kali provider consensus:

~~~text
PASS
~~~

## 6. Egress comparison

The A50 consensus IPv4 and the Kali consensus IPv4 were compared in
memory.

Result:

~~~text
A50 vs Kali public egress: DIFFERENT
~~~

The raw address values were not printed by the final reconciliation and
were intentionally omitted from persisted evidence.

## 7. HEV observation

During the egress-comparison window:

~~~text
TCP/1080 packet delta: 0
UDP/1081 packet delta: 0
New HEV log lines:     0
~~~

Therefore no HEV activity was observed while the A50 public-egress
identity was established.

## 8. Cross-phase relationship

LAB-002C observed:

~~~text
successful application load
A50-to-HEV path not observed
~~~

LAB-002D observed:

~~~text
successful application load
A50-to-HEV path not observed
no HEV-attributable outbound relay
no delayed HEV activity within a 30-second post-request window
~~~

LAB-002E now adds:

~~~text
A50 public egress != Kali/HEV public egress
HEV activity = 0
~~~

Together these observations materially weaken the hypothesis that HEV
is the effective transport for the tested traffic while both WireGuard
and SOCKS5 are displayed as enabled.

## 9. Classification

LAB-002E is classified:

~~~text
PASS / DIFFERENT PUBLIC EGRESS WITHOUT HEV
~~~

The tested A50 traffic had a public egress different from Kali/HEV while
no traffic to the HEV SOCKS5 endpoint was observed.

This is operational evidence compatible with WireGuard being selected as
the effective transport for the tested A50 requests.

## 10. Interpretation boundary

LAB-002E does not independently prove:

- a WireGuard handshake occurred
- the observed egress belongs to the configured WireGuard provider
- WireGuard transported every application
- SOCKS5 can never be selected while WireGuard is enabled
- a universal precedence rule between WireGuard and SOCKS5
- DNS behavior under the combined state
- UDP behavior under the combined state
- fail-open or fail-closed behavior

The correct interpretation is:

~~~text
different A50 egress
+
no HEV path
=
strong operational evidence of a non-HEV path
~~~

and:

~~~text
strong operational evidence
!=
cryptographic WireGuard validation
~~~

## 11. Initial inconclusive attempt

An earlier LAB-002E script attempt produced:

~~~text
INCONCLUSIVE
~~~

because manual A50 IPv4 input was incorrectly rejected by the collection
workflow.

That attempt is preserved locally rather than discarded.

Prior local summary SHA-256:

~~~text
d4c4a95c38c5457cd2aae4d74ee236e55107b051b2b3635dc5bb8c932c4c1d0b
~~~

It is not used as the final LAB-002E classification.

## 12. Final evidence identity

The reconciled privacy-preserving summary is retained locally.

SHA-256:

~~~text
b507892f09008a228d2baaefe3ed0198fd99a9c7132650708e731bd9d53129b4
~~~

The local summary contains no raw public IPv4 values.

## 13. Next phase

LAB-002F will characterize DNS behavior while preserving the combined
state:

~~~text
RethinkDNS ON
WireGuard  ON
SOCKS5     ON
~~~

The public-egress result from LAB-002E will serve as context but will not
be used to assume DNS follows the same path.

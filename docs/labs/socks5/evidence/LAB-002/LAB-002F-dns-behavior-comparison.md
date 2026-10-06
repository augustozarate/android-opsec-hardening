# LAB-002F — DNS Behavior Comparison

**Status:** PASS / RETHINK DNS OBSERVED WITHOUT HEV

## 1. Objective

Characterize DNS behavior while RethinkDNS displays both WireGuard and
SOCKS5 as enabled.

The phase asks two separate questions:

1. Does RethinkDNS observe the controlled DNS lookup?
2. Does that lookup produce observable HEV/SOCKS5 activity?

DNS behavior is evaluated independently from the public-egress result
established in LAB-002E.

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

HEV remained active and available on Kali.

## 3. First controlled attempt

The first LAB-002F attempt generated a unique DNS hostname and observed
both the HEV path and best-effort DNS visibility from Kali.

The browser produced a DNS-resolution failure.

The manual RethinkDNS-log result was initially entered as:

~~~text
UNKNOWN
~~~

Network observations were:

~~~text
TCP/1080 packet delta:       0
UDP/1081 packet delta:       0
New HEV log lines:           0
A50-to-HEV packets:          0

Visible DNS/DoT packets:     0
Visible port 53 packets:     0
Visible port 853 packets:    0
~~~

The absence of port 53/853 visibility from Kali was not interpreted as
global absence of DNS traffic because the LAN topology does not
guarantee visibility of unicast A50-to-router traffic.

First-attempt local summary SHA-256:

~~~text
01bbbd961021c567889093eaad576def61d058090bd233c81b475264a4a76f17
~~~

## 4. Focused RethinkDNS-log retest

A second unique hostname was generated:

~~~text
lab002f-retest-1791318132.example.com
~~~

The browser again initiated resolution of the unique hostname.

The manual response entered during the collection was:

~~~text
NOT_FOUND
~~~

At that time the operator was uncertain whether the RethinkDNS UI entry
satisfied the collection requirement.

The original response is preserved and was not rewritten.

Retest local summary SHA-256:

~~~text
9c31eb2376bb37d25233c44bd7674db5448746c45721b4c0a6d471c6f37eeae6
~~~

## 5. Visual evidence reconciliation

Subsequent screenshots of the RethinkDNS DNS log showed the exact
controlled hostname:

~~~text
lab002f-retest-1791318132.example.com
~~~

The visual evidence showed:

~~~text
application                  Brave
IPv4 query                   visible
HTTP Service Binding query   visible
WireGuard UI association     WG
resolver                     Cache [CachePreferred:dns.nextdns.io]
~~~

RethinkDNS resolver metadata also referenced:

~~~text
wg15:10.2.0.1:53
~~~

The visual evidence therefore supersedes the conservative manual
NOT_FOUND classification.

Corrected DNS-log result:

~~~text
FOUND
~~~

The DNS decision itself remains:

~~~text
UNKNOWN
~~~

No explicit allow/block conclusion is asserted from the available UI
evidence.

Visual-reconciliation SHA-256:

~~~text
3cbec3c2857fcb18348738609681b7b8976d45c379fcf5f10159c416f0bf1251
~~~

## 6. HEV / SOCKS5 observation

During the focused retest:

~~~text
TCP/1080 packet delta: 0
UDP/1081 packet delta: 0
New HEV log lines:     0
A50-to-HEV packets:    0
~~~

The A50-to-HEV packet capture contained zero packets.

PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

The raw PCAP remains local and is not committed.

## 7. Classification

LAB-002F is classified:

~~~text
PASS / RETHINK DNS OBSERVED WITHOUT HEV
~~~

The controlled DNS hostname was demonstrably visible in RethinkDNS while
no HEV/SOCKS5 activity was observed.

This establishes, for the tested lookup, that RethinkDNS participated in
the DNS processing plane without producing an observable HEV path.

## 8. WireGuard-associated observations

The RethinkDNS UI displayed:

~~~text
WG
~~~

for the controlled hostname entries.

Resolver metadata additionally referenced:

~~~text
wg15:10.2.0.1:53
~~~

These observations are operational evidence compatible with WireGuard
participation in the tested DNS path.

They materially strengthen the combined interpretation established by
LAB-002C through LAB-002E.

They are not treated as cryptographic proof of a WireGuard handshake or
as proof that every DNS request follows the same path.

## 9. Relationship to previous phases

LAB-002C established:

~~~text
successful application workload
A50-to-HEV path not observed
~~~

LAB-002D established:

~~~text
no HEV-attributable outbound relay
no delayed HEV activity during successful workload
~~~

LAB-002E established:

~~~text
A50 public egress != Kali/HEV public egress
HEV activity = 0
~~~

LAB-002F now adds:

~~~text
controlled DNS query visible in RethinkDNS
WireGuard-associated UI/resolver metadata visible
HEV activity = 0
~~~

Across these phases, the model in which SOCKS5 remains configured but is
not selected for the tested traffic has gained substantial operational
support.

## 10. Interpretation boundary

LAB-002F does not independently prove:

- a cryptographically validated WireGuard handshake
- that every DNS lookup traverses WireGuard
- that SOCKS5 can never carry DNS-related traffic
- that port 53 or port 853 traffic was globally absent
- a universal transport-precedence rule
- DNS behavior after restart or network transition

In particular:

~~~text
zero DNS packets visible from Kali
!=
zero DNS traffic globally
~~~

and:

~~~text
WG UI / wg15 metadata
!=
cryptographic tunnel validation
~~~

## 11. Evidence methodology

The original UNKNOWN and NOT_FOUND operator classifications remain in
their respective local runtime summaries.

The final classification is based on a separate reconciliation record
that documents why direct visual evidence superseded the conservative
manual interpretation.

This preserves the sequence:

~~~text
original observation
        ->
operator uncertainty
        ->
visual evidence review
        ->
explicit reconciliation
~~~

rather than silently rewriting prior evidence.

## 12. Next phase

LAB-002G will characterize UDP behavior under the same combined state:

~~~text
RethinkDNS ON
WireGuard  ON
SOCKS5     ON
~~~

No assumption will be made that the UDP data plane follows the same path
as the DNS or TCP application observations.

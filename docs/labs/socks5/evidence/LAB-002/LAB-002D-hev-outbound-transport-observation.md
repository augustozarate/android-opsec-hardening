# LAB-002D — HEV Outbound Transport Observation

**Status:** PASS / HEV OUTBOUND NOT OBSERVED

## 1. Objective

Determine whether HEV produces an observable outbound Internet leg while
RethinkDNS shows both WireGuard and SOCKS5 enabled on the Android device.

LAB-002D evaluates the potential two-leg path:

~~~text
A50
 |
 | SOCKS5 first leg
 v
HEV / Kali
 |
 | outbound relay leg
 v
Internet
~~~

The phase does not assume that configuration-state coexistence implies
transport coexistence.

## 2. Runtime precondition recovery

Before the controlled LAB-002D workload, runtime state had changed.

The current A50 identity was:

~~~text
IPv4: 10.36.136.41
~~~

The previously observed address:

~~~text
10.36.136.37
~~~

was no longer present in the neighbor snapshot.

HEV had also been absent and was restarted using the previously pinned
binary.

Pinned HEV binary SHA-256:

~~~text
5257ad617b42408926ac912c317ffdd364b7b8eaebd41189a235854bbf64f081
~~~

The dedicated nftables table had disappeared and was reconstructed as:

~~~text
family:   inet
table:    opsec_lab
chain:    input
hook:     input
priority: -10
policy:   accept
~~~

The recovered access policy contained exactly four rule objects:

~~~text
10.36.136.41 -> TCP/1080 ACCEPT
other        -> TCP/1080 DROP

10.36.136.41 -> UDP/1081 ACCEPT
other        -> UDP/1081 DROP
~~~

Because the table was recreated, its packet and byte counters started
from a new zero baseline.

Precondition-recovery local record SHA-256:

~~~text
38fa479edd2e59918ab365af05fecce196b41c34ac3318e4d48be17eb5f65eec
~~~

The recovery evidence remains local and is not committed.

## 3. Tested combined state

Immediately before the workload, the A50 configuration was manually
confirmed as:

~~~text
RethinkDNS                 ON
WireGuard                  ON
SOCKS5                     ON
Proxy Lockdown             ON
Do not route private IPs   ON
Android Always-on VPN      ON
Android VPN Lockdown       OFF
Rethink IP version         IPv4
~~~

HEV was active and listening on TCP/1080.

## 4. Controlled workload

The A50 loaded a nonce-qualified example.com URL.

Observed application result:

~~~text
LOADED
~~~

No WireGuard, SOCKS5, RethinkDNS, HEV, or nftables configuration was
changed during the workload.

## 5. First-leg observation

The first-leg observation covered:

~~~text
10.36.136.41
    ->
10.36.136.33

TCP/1080
or
UDP/1081
~~~

nftables deltas were:

~~~text
TCP/1080 packets: +0
TCP/1080 bytes:   +0

UDP/1081 packets: +0
UDP/1081 bytes:   +0
~~~

HEV produced:

~~~text
0 new log lines
~~~

The first-leg packet capture contained:

~~~text
0 packets
~~~

First-leg PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

The PCAP remains local and is not committed.

## 6. HEV destination observation

Because HEV produced no new events, there were:

~~~text
0 new HEV destinations
~~~

available for outbound correlation.

Therefore no second-leg destination could be derived from HEV logs for
this workload.

## 7. Kali outbound observation

A simultaneous capture observed IPv4 traffic originating from Kali and
leaving the local LAN.

Total observed external outbound packets:

~~~text
2
~~~

Both were:

~~~text
UDP destination port 123
NTP client traffic
~~~

No non-NTP packet was present in the scoped outbound capture.

These packets are treated as generic Kali background traffic.

They are not attributed to HEV.

Outbound PCAP SHA-256:

~~~text
50af546541d6b115aad4ef40e3c134ebf46f49453ae1a97240805606928fbe3d
~~~

The PCAP remains local and is not committed.

## 8. Correlation result

Cross-source evidence was:

~~~text
Controlled page result                 LOADED

A50 -> HEV TCP/1080 delta              0
A50 -> HEV UDP/1081 delta              0
HEV new events                         0
First-leg PCAP packets                 0

HEV destinations                      0
HEV destinations with outbound match  0

Generic Kali external packets          2
Generic Kali packet type               NTP
~~~

No HEV-attributable outbound Internet leg was observed.

## 9. Classification

LAB-002D is classified:

~~~text
PASS / HEV OUTBOUND NOT OBSERVED
~~~

This means the observation procedure completed successfully, but the
tested workload produced no evidence of HEV participation.

Because no A50-to-HEV first leg occurred, there was no HEV destination
to correlate with a second outbound leg.

The two observed NTP packets cannot be used as evidence of HEV relay
traffic.

## 10. Relationship to LAB-002C

LAB-002D independently reproduced the central first-leg result observed
in LAB-002C:

~~~text
WireGuard UI ON
SOCKS5 UI ON
application workload succeeds
HEV path not observed
~~~

This strengthens the observation that SOCKS5 may remain shown as enabled
while not being selected for these tested application requests.

It does not establish universal behavior for all applications,
protocols, policies, or destinations.

## 11. Empty-PCAP hash note

The first-leg PCAP SHA-256 is identical to the zero-packet first-leg
capture produced in LAB-002C.

This is compatible with both files being empty classic PCAP captures:
without packet records, equivalent PCAP global headers can produce
byte-identical files.

The identical hash is not interpreted as evidence of network activity.

## 12. Interpretation boundary

LAB-002D does not prove:

- that WireGuard carried the successful request
- that the request bypassed all VPN transport
- that SOCKS5 can never be selected while WireGuard is enabled
- that WireGuard has precedence for every application
- any specific WireGuard/SOCKS5 ordering
- public egress identity
- DNS routing under the combined state

The correct conclusion remains:

~~~text
HEV transport not observed
!=
WireGuard transport independently validated
~~~

## 13. Next phase

LAB-002E will compare public egress while preserving the combined state:

~~~text
RethinkDNS ON
WireGuard  ON
SOCKS5     ON
~~~

The goal will be to determine whether the A50 public egress matches
Kali/HEV or differs from it.

Public-egress evidence will be considered together with LAB-002C and
LAB-002D, but will not by itself be treated as cryptographic proof of
WireGuard transport.

## 14. Stable-identity extended timing validation

A later validation was performed after stabilizing the Android Wi-Fi
identity used by the lab.

The validated client identity was:

~~~text
IPv4: 10.36.136.46
MAC:  0a:13:ee:1e:7d:3b
~~~

The same IPv4 and MAC had remained present across a controlled Wi-Fi
reconnection immediately before this validation.

The LAB nftables source ACL was reconciled to:

~~~text
10.36.136.46 -> TCP/1080 ACCEPT
10.36.136.46 -> UDP/1081 ACCEPT
~~~

The generic TCP/1080 and UDP/1081 deny rules remained present.

A fresh nonce-qualified request to example.com was then generated.

Observed application result:

~~~text
LOADED
~~~

The observation window included:

~~~text
5 seconds before the request
30 seconds after the request
~~~

HEV log observations were:

~~~text
~10 seconds: 0 new lines
~20 seconds: 0 new lines
~30 seconds: 0 new lines
~~~

Network evidence remained:

~~~text
TCP/1080 packet delta: 0
TCP/1080 byte delta:   0

UDP/1081 packet delta: 0
UDP/1081 byte delta:   0

A50-to-HEV PCAP packets: 0
~~~

Timing-validation PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

Timing-validation summary SHA-256:

~~~text
897591003da916eae8622370999a58aea147f4d3f3522bc7fd90f56d042658c1
~~~

The successful extended-window validation therefore produced:

~~~text
NO_HEV_ACTIVITY_EXTENDED_30S
~~~

This materially weakens the hypothesis that the earlier zero-event
results were caused only by checking HEV too soon.

For this tested successful request, no delayed HEV activity appeared
within the 30-second post-request observation window.

This remains workload-specific evidence and is not interpreted as proof
that delayed HEV activity is impossible for every application,
protocol, destination, or policy state.

## 15. Auxiliary failed ipify request

Before the successful example.com timing validation, an equivalent
extended-window request to api.ipify.org failed at the application
layer.

The browser reported a connection-refused condition and the experiment
was correctly recorded as:

~~~text
FAILED
~~~

No HEV activity was observed during that failed attempt either.

Failed-attempt PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

Failed-attempt summary SHA-256:

~~~text
07cb26607bceb3c9e79a72bcba9eaedb6a0eddb50aa985c582ded3323391827f
~~~

This failed request is retained as auxiliary evidence only.

It is not used to establish the successful-workload classification for
LAB-002D.

## 16. Local evidence identities

Primary LAB-002D summary SHA-256:

~~~text
1fbdd7f21270b4aba2e3c9157726c3c2646668f08c171716b257ed6e4bf71467
~~~

Precondition-recovery SHA-256:

~~~text
38fa479edd2e59918ab365af05fecce196b41c34ac3318e4d48be17eb5f65eec
~~~

All raw PCAPs and runtime summaries remain local and are not committed.

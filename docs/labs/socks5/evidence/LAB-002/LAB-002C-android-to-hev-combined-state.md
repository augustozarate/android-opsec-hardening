# LAB-002C — Android-to-HEV Traffic Under Combined State

**Status:** PASS / HEV PATH NOT OBSERVED

## 1. Objective

Determine whether the Android device continues to contact the HEV
SOCKS5 endpoint while RethinkDNS shows both WireGuard and SOCKS5
enabled.

LAB-002C evaluates the first observable leg:

~~~text
A50
 |
 v
HEV
10.36.136.33
TCP/1080 or UDP/1081
~~~

It does not determine WireGuard/SOCKS5 ordering.

## 2. Starting state

The tested configuration was manually confirmed as:

~~~text
A50 IPv4                   10.36.136.37
RethinkDNS                 ON
WireGuard                  ON
SOCKS5                     ON
Proxy Lockdown             ON
Do not route private IPs   ON
Android Always-on VPN      ON
Android VPN Lockdown       OFF
Rethink IP version         IPv4
~~~

HEV remained active at:

~~~text
10.36.136.33:1080 TCP
10.36.136.33:1081 UDP
~~~

## 3. Controlled workload

The A50 loaded:

~~~text
https://example.com/?lab=002c-1
~~~

The observed application result was:

~~~text
LOADED
~~~

No RethinkDNS, WireGuard, SOCKS5, HEV, or nftables configuration was
changed during the workload.

## 4. nftables observation

Before the workload:

~~~text
TCP/1080 packets: 442
TCP/1080 bytes:   73963
UDP/1081 packets: 24
UDP/1081 bytes:   13885
~~~

Observed deltas during the controlled workload:

~~~text
TCP/1080 packets: +0
TCP/1080 bytes:   +0

UDP/1081 packets: +0
UDP/1081 bytes:   +0
~~~

No A50-to-HEV traffic increment was observed on either authorized HEV
transport.

## 5. HEV observation

HEV produced:

~~~text
0 new log events
~~~

Specifically:

- no new TCP destination event
- no new UDP ASSOCIATE event
- no HEV connect failure marker

No active A50-to-HEV TCP/1080 session was visible in the final socket
snapshot.

## 6. Packet-capture observation

A capture was limited to:

~~~text
source      10.36.136.37
destination 10.36.136.33

TCP destination port 1080
or
UDP destination port 1081
~~~

Matching packets:

~~~text
0
~~~

PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

The capture is retained locally and is not committed.

Because the capture contained zero matching packets, no source-address
identity claim can be derived from packet contents.

## 7. Local summary identity

The LAB-002C local summary is retained outside Git.

SHA-256:

~~~text
91a9111235d03afe4b3892bebd772edaa24b561d18409397fcb83a2a5031103a
~~~

## 8. Cross-source result

All first-leg evidence sources agreed:

~~~text
nftables TCP/1080 delta     0
nftables UDP/1081 delta     0
HEV new events              0
matching PCAP packets       0
active TCP/1080 session     none
~~~

At the same time:

~~~text
controlled page result      LOADED
WireGuard UI state          ON
SOCKS5 UI state             ON
~~~

## 9. Classification

LAB-002C is classified:

~~~text
PASS / HEV PATH NOT OBSERVED
~~~

For the tested controlled workload, no evidence showed the A50 using
the configured HEV SOCKS5 endpoint while WireGuard and SOCKS5 were both
shown enabled.

This is stronger than UI-state evidence alone.

It demonstrates that configuration coexistence observed in LAB-002B
did not result in an observable A50-to-HEV SOCKS5 path for this workload.

## 10. Interpretation boundary

LAB-002C does NOT establish that WireGuard carried the controlled page.

The observed result remains compatible with multiple possibilities,
including:

- WireGuard being the effective application transport
- another non-HEV path being selected
- policy-based transport selection
- a configured but unused SOCKS5 state
- content being satisfied without a newly observable HEV connection

LAB-002C therefore does not yet prove:

~~~text
Application -> WireGuard -> Internet
~~~

nor any specific WireGuard/SOCKS5 ordering.

## 11. Hypothesis impact

The following simple hypothesis was not supported by LAB-002C:

~~~text
WireGuard ON
+
SOCKS5 ON
    |
    v
application traffic continues through HEV
~~~

For the controlled workload, the HEV first leg was not observed.

The hypothesis that SOCKS5 can remain displayed as enabled while not
being selected for this traffic remains viable.

## 12. Next evidence requirement

The next phase must determine where the successfully loaded traffic
exited.

Useful next evidence includes:

- direct public egress observed from Kali/HEV
- public egress observed from the A50
- comparison with the configured WireGuard/VPN exit
- additional non-cached controlled network requests
- evidence of WireGuard transport activity independent of the UI

Until such evidence exists:

~~~text
WireGuard configured != WireGuard transport validated
~~~

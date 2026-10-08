# LAB-002I — WireGuard Failure and Recovery Behavior

**Status:** CHARACTERIZED / CONTROLLED WG20 FAILURE AND AUTOMATIC RECOVERY VALIDATED

## 1. Purpose

LAB-002I characterizes application and RethinkDNS behavior when a
previously validated per-application WireGuard transport becomes
unreachable and subsequently becomes reachable again.

The phase evaluates three states:

1. a healthy WireGuard application-transport baseline;
2. a controlled WireGuard transport failure;
3. recovery after removing only the injected failure.

LAB-002I does not characterize generic fail-open or fail-closed policy.
That question is reserved for LAB-002J.

## 2. Scope

The tested Android application was Brave:

~~~text
package: com.brave.browser
UID:     10342
~~~

Brave was assigned to the dedicated RethinkDNS WireGuard laboratory
profile identified at runtime as:

~~~text
wg20
~~~

The laboratory WireGuard path was:

~~~text
Brave
  -> RethinkDNS / wg20
  -> Android WireGuard peer 10.203.14.2
  -> Kali wg-lab
  -> Kali forwarding / NAT
  -> Internet
~~~

The provider WireGuard profile used elsewhere in the project was not
modified for this phase.

SOCKS5 remained OFF.

The following RethinkDNS state was kept constant through the accepted
failure/recovery sequence:

~~~text
LAB-KALI-WG / wg20       ON
Brave assigned to wg20    YES
configured MTU            1420
ListenPort                automatic
LAT                       OFF
SOCKS5                    OFF
Proxy Lockdown            unchanged
DNS-bypass protection     unchanged
LAB-KALI-WG BLOQUEO       unchanged
provider profile14        unchanged
~~~

## 3. WireGuard laboratory infrastructure

The dedicated Kali peer used:

~~~text
interface:      wg-lab
server address: 10.203.14.1/24
client address: 10.203.14.2/32
listen UDP:     51820
~~~

The A50 physical Wi-Fi address during this phase was:

~~~text
10.36.136.46
~~~

IPv4 forwarding on Kali was enabled.

### 3.1 Docker forwarding interaction

Initial end-to-end testing exposed an unrelated Kali host-forwarding
condition.

The dedicated laboratory nftables chain accepted traffic from
`wg-lab`, but Kali also contained a later Docker-managed IPv4
`FORWARD` base chain with policy `DROP`.

An accept verdict in the earlier laboratory base chain did not prevent
evaluation by the later Docker-managed base chain.

The observed result before correction was:

~~~text
A50 -> wg20 -> wg-lab:       observed
wg-lab outbound SYN:         observed
eth0 forwarded SYN:          not observed
Kali direct Internet access: working
~~~

Two narrow laboratory exceptions were therefore placed in
`DOCKER-USER`:

~~~text
wg-lab -> eth0
source 10.203.14.0/24
ACCEPT
~~~

and:

~~~text
eth0 -> wg-lab
destination 10.203.14.0/24
state ESTABLISHED,RELATED
ACCEPT
~~~

The global Docker `FORWARD` policy was not changed.

These exceptions are an infrastructure prerequisite for the local
Kali WireGuard gateway and are not treated as a RethinkDNS policy
result.

## 4. I-01 — healthy application baseline

The accepted healthy reference was the final R4V application
transport run.

Observed objective transport evidence:

~~~text
DOCKER-USER outbound delta:   244
DOCKER-USER return delta:     199

wg-lab outbound packets:      223
wg-lab inbound packets:       178

TCP SYN:                      10
TCP SYN/ACK:                  10

eth0 outbound packets:        226
eth0 inbound packets:         176

active wg20 for Brave:        24
proxy-id [wg20]:              24
example.com references:       159
~~~

The packet trace contained complete bidirectional TCP sessions through
`wg-lab`, including:

~~~text
SYN
SYN/ACK
ACK
bidirectional payload
connection teardown
~~~

The page loaded successfully in Brave.

### 4.1 Operator-input correction

The local R4V summary contains:

~~~text
Brave result: BRAVE_R4V_FAILED
Classification: WG20_HEALTHY_BASELINE_REQUIRES_REVIEW
~~~

This was an operator-input typo.

The observed application result was:

~~~text
BRAVE_R4V_LOADED
~~~

The summary file is intentionally retained unchanged so its SHA-256
continues to identify the original execution artifact.

All independent transport criteria required by the R4V classifier were
positive.

The accepted I-01 result is therefore:

~~~text
WG20_BRAVE_END_TO_END_HEALTHY_BASELINE_PASS
~~~

## 5. I-02 — controlled WireGuard transport failure

The failure was introduced only on Kali.

A narrow input rule was inserted before the normal WireGuard allow rule:

~~~text
physical source: 10.36.136.46
interface:       eth0
protocol:        UDP
destination:     51820
action:          DROP
~~~

The rule was identified by the laboratory comment:

~~~text
LAB-002I-I02-A50-WG-DROP
~~~

No Android setting was changed.

No WireGuard peer configuration was changed.

No `wg-lab` interface configuration was changed.

No NAT or `DOCKER-USER` rule was changed.

### 5.1 Failure evidence

Server-side WireGuard state:

~~~text
handshake before: 1791495637
handshake after:  1791495637

RX before:        650700
RX after:         650700
~~~

The controlled DROP rule recorded:

~~~text
350 packets
55306 bytes
~~~

Physical observation showed:

~~~text
A50 -> Kali UDP/51820 attempts: 350
~~~

No inner packet reached `wg-lab` during the failure observation:

~~~text
wg-lab packets: 0
~~~

RethinkDNS / Firestack recorded:

~~~text
active wg20 for Brave:       650
proxy-id [wg20]:             650

wg20 handshake initiations:  86
wg20 handshake responses:    0
wg20 unresponsive signals:   204
~~~

The server handshake did not advance.

Brave failed to load the controlled page.

### 5.2 Selection behavior during failure

No alternate selection was observed by the experiment counters:

~~~text
Base returns:   0
S5 returns:     0
Block returns:  0
~~~

At the same time, the application-to-profile relationship remained
observable:

~~~text
Brave -> wg20
~~~

The I-02 classifications were:

~~~text
CONTROLLED_WG20_TRANSPORT_FAILURE_ESTABLISHED
WG20_SELECTION_PERSISTS_DURING_TRANSPORT_FAILURE
~~~

This distinguishes logical proxy selection from successful encrypted
transport.

The observations support:

~~~text
Configured != Reachable
Selected   != Successfully Transporting Traffic
UDP write  != Peer Response
~~~

## 6. I-03 — controlled recovery

Recovery removed only:

~~~text
LAB-002I-I02-A50-WG-DROP
~~~

No Android configuration was changed.

No `wg-lab` configuration was changed.

No `DOCKER-USER` rule was changed.

No NAT rule was changed.

### 6.1 Cryptographic recovery

The Kali peer handshake advanced from:

~~~text
1791495637
~~~

to:

~~~text
1791496635
~~~

Observed transfer deltas were:

~~~text
RX delta:  154196
TX delta:  1620280
~~~

Physical WireGuard traffic returned in both directions:

~~~text
A50 -> Kali: 769 packets
Kali -> A50: 1563 packets
~~~

Firestack recorded:

~~~text
Sending handshake initiation
Received handshake response
status unresponsive => ok
~~~

### 6.2 Application recovery

Brave successfully loaded the controlled post-recovery page.

Inner HTTPS observation:

~~~text
wg-lab outbound HTTPS: 458
wg-lab inbound HTTPS:  380

TCP SYN:                27
TCP SYN/ACK:            21
~~~

Kali forwarding counters increased:

~~~text
DOCKER-USER outbound delta: 764
DOCKER-USER return delta:   1485
~~~

RethinkDNS continued to associate Brave with `wg20`:

~~~text
active wg20 signals:   36
proxy-id [wg20]:       36
~~~

No Base or SOCKS5 selection was observed by the recovery counters.

The I-03 classifications were:

~~~text
CONTROLLED_WG20_TRANSPORT_RECOVERY_ESTABLISHED
WG20_BRAVE_END_TO_END_RECOVERY_PASS
~~~

## 7. Causal sequence

The accepted LAB-002I sequence is:

~~~text
HEALTHY
  wg20 reachable
  fresh handshake
  bidirectional wg-lab traffic
  Brave loads
        |
        v
CONTROLLED FAILURE
  only A50 -> Kali UDP/51820 dropped
  handshake freezes
  handshake retries continue
  zero inner wg-lab traffic
  Brave fails
  wg20 selection persists
        |
        v
RECOVERY
  only failure DROP removed
  fresh handshake appears
  Firestack unresponsive -> ok
  bidirectional wg-lab traffic returns
  Brave loads again
~~~

The independent variable during I-02/I-03 was endpoint reachability at
Kali UDP/51820.

The Android application assignment and WireGuard profile configuration
remained constant.

## 8. Result

LAB-002I is classified:

~~~text
CHARACTERIZED
~~~

The experiment establishes that, in this tested state:

1. Brave can be transported end-to-end through the dedicated `wg20`
   WireGuard profile.
2. Removing reachability to the Kali WireGuard endpoint causes a
   reproducible transport failure.
3. RethinkDNS continues to identify `wg20` as the application's
   selected WireGuard profile while transport is unavailable.
4. No Base or SOCKS5 fallback was observed by the I-02 counters.
5. Restoring peer reachability allows WireGuard and application
   transport to recover without reconfiguring Android or reassigning
   Brave.

## 9. What LAB-002I does not prove

LAB-002I does not establish:

- a universal fail-open policy;
- a universal fail-closed policy;
- behavior for all RethinkDNS versions;
- behavior for all WireGuard profiles;
- behavior on cellular or other physical transports;
- active SOCKS5 fallback semantics;
- a universal WireGuard/SOCKS5 precedence rule;
- IPv6 WireGuard transport behavior in this laboratory profile.

Those conclusions require separate controls.

Fail-open / bypass characterization remains assigned to LAB-002J.

## 10. Evidence handling

Raw logcat and packet-capture material remains local and is not
committed.

Only sanitized observations and cryptographic hashes are recorded in
Git.

Accepted local summaries:

~~~text
LAB-002I-WG-02B-R4V-summary.txt
SHA-256:
ff2ff40f3d2147c2251bc5fcb67003162928c26b848055b07bf21735fee8a5db
~~~

The R4V summary contains the documented operator-input typo described
in Section 4.1.

~~~text
LAB-002I-I02-summary.txt
SHA-256:
58f3dd21a22f651db6c7e9c75ffc6a7de0193ff90a399f2abaff30c4dab64fd9
~~~

~~~text
LAB-002I-I03-summary.txt
SHA-256:
c334ce9025fd20c7050b4c7a26da3db827a1c62823bd230876e03b4e7f8fc69b
~~~

## 11. Final laboratory state

At completion:

~~~text
I02 failure DROP:          absent

wg20:                      ON
Brave assigned to wg20:    YES

DOCKER-USER lab forwarding:
  wg-lab -> eth0           present
  eth0 -> wg-lab           present

provider profile14:        unchanged
SOCKS5:                    OFF
~~~

The `DOCKER-USER` exceptions are retained only as the controlled
forwarding prerequisite for the Kali WireGuard gateway.

## 12. Next phase

LAB-002J will separately evaluate fail-open / bypass semantics.

LAB-002I does not pre-classify that result.

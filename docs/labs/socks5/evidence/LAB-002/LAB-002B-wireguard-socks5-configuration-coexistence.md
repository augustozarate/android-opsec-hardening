# LAB-002B — WireGuard + SOCKS5 Configuration Coexistence

**Status:** CHARACTERIZED / TRANSIENT COEXISTENCE; STABLE ACTIVE COEXISTENCE NOT ESTABLISHED

## 1. Objective

Determine whether RethinkDNS permits an existing WireGuard profile to
be enabled while the authenticated SOCKS5 configuration remains enabled.

This phase evaluates configuration and UI state only.

It does not establish packet-routing order or prove that either
configured transport carried application traffic.

## 2. Starting state

LAB-002B started from the recovered LAB-002A reference state:

~~~text
A50 IPv4                   10.36.136.37
RethinkDNS                 ON
SOCKS5                     ON
WireGuard                  OFF
Proxy Lockdown             ON
Do not route private IPs   ON
Android Always-on VPN      ON
Android VPN Lockdown       OFF
Rethink IP version         IPv4
~~~

The HEV gateway remained available at:

~~~text
10.36.136.33:1080 TCP
10.36.136.33:1081 UDP
~~~

## 3. Controlled action

While remaining inside RethinkDNS:

1. SOCKS5 was left enabled.
2. The existing WireGuard profile was selected.
3. WireGuard was enabled.
4. SOCKS5 was not manually disabled.
5. No deliberate browser or application workload was generated.
6. The resulting UI state was observed after waiting for stabilization.

## 4. Resulting UI state

The final state shown by RethinkDNS was:

~~~text
WireGuard   ON
SOCKS5      ON
~~~

No warning or incompatibility message was observed.

The configuration behavior is classified:

~~~text
B1
~~~

Where B1 means:

~~~text
WireGuard appears ON
AND
SOCKS5 remains ON
~~~

## 5. Passive network observation

No deliberate network workload was generated during this phase.

A50-to-HEV nftables deltas were:

~~~text
TCP/1080 packets: 0
TCP/1080 bytes:   0

UDP/1081 packets: 0
UDP/1081 bytes:   0
~~~

HEV produced:

~~~text
0 new log events
~~~

These zero deltas are not interpreted as transport failure.

They indicate only that no matching HEV traffic was observed during the
configuration-only observation window.

## 6. Evidence identity

The local observation record is retained outside Git.

~~~text
SHA-256:
092a2842e07a52309851491a2904c0b2b9182480053b19fd8b94e7f5f3d0584f
~~~

Raw runtime observation:

~~~text
~/.local/state/android-opsec-hardening/hev-socks5/LAB-002B/
LAB-002B-config-observation-v2.txt
~~~

The local runtime file itself is not committed.

## 7. Classification

LAB-002B is classified:

~~~text
PASS / B1 CONFIGURATION COEXISTENCE
~~~

Under the tested RethinkDNS v0.5.7 configuration, the UI permitted both:

~~~text
WireGuard ON
SOCKS5 ON
~~~

simultaneously.

This establishes configuration-state coexistence for the tested state.

## 8. What LAB-002B does not prove

LAB-002B does not prove:

- that WireGuard completed a functional tunnel handshake
- that WireGuard carried application traffic
- that SOCKS5 remained functionally active after WireGuard activation
- that traffic traverses WireGuard before SOCKS5
- that traffic traverses SOCKS5 before WireGuard
- that both transports are used simultaneously
- that traffic is split between transports
- public-egress behavior
- DNS-routing behavior
- UDP-routing behavior under combined configuration
- fail-open or fail-closed behavior
- persistence across RethinkDNS restart
- persistence across Android reboot

Those properties require traffic evidence in later LAB-002 phases.

## 9. Current hypothesis state

The configuration observation weakens the simple mutual-exclusion model:

~~~text
SOCKS5 ON
    +
WireGuard activation
    |
    X
one transport must be disabled
~~~

That model was not observed in LAB-002B.

The following possibilities remain open:

~~~text
1. SOCKS5 remains the effective transport.

2. WireGuard becomes the effective transport.

3. WireGuard transports the SOCKS5 path.

4. SOCKS5 transports or relays WireGuard-related traffic.

5. RethinkDNS applies the transports to different traffic or apps.

6. One transport is displayed as enabled but is not functionally used.
~~~

No remaining model is considered validated.

## 10. Next phase

The resulting LAB-002B state must remain unchanged for the next
controlled observation:

~~~text
RethinkDNS   ON
WireGuard    ON
SOCKS5       ON
~~~

LAB-002C will introduce controlled application traffic and determine
whether the A50 continues to contact the HEV SOCKS5 endpoint while both
features are shown enabled.


## Corrective reconciliation — LAB-002B-R2

Later controlled testing refined this phase.

The original UI-coexistence observation remains valid, but durable
simultaneous operation was not established.

After restoring a missing SOCKS5 credential, the SOCKS5-only path was
validated successfully.

A subsequent test then enabled WireGuard with the WireGuard Advanced
`Always-on` option disabled.

The UI initially showed both WireGuard and SOCKS5 ON, but after
approximately 30 seconds SOCKS5 was observed OFF without a deliberate
browser workload and without new HEV traffic.

The corrected interpretation is therefore:

~~~text
configuration coexistence           OBSERVED
transient active UI coexistence     OBSERVED
stable active coexistence           NOT ESTABLISHED
~~~

See `LAB-002B-R2-proxy-state-reconciliation.md` for the complete
evidence reconciliation.

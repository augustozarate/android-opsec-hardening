# LAB-002H — SOCKS5 Failure Behavior

**Status:** PASS / TESTED WG FLOW UNAFFECTED BY HEV OUTAGE

## 1. Objective

Determine whether deliberate unavailability of the HEV SOCKS5 backend
affects an application flow that, in the preceding LAB-002 phases, was
associated by RethinkDNS with WireGuard.

The test preserves the combined RethinkDNS configuration while removing
only backend HEV availability.

The phase does not attempt to establish a global fail-open or fail-closed
policy.

## 2. Starting state

The A50 began in the established combined configuration:

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

HEV was initially active and listening on TCP/1080.

## 3. Controlled backend failure

The HEV process was terminated immediately before the controlled
application workload.

The failure condition was independently verified:

~~~text
HEV process                ABSENT
HEV TCP/1080 listener      ABSENT
~~~

RethinkDNS, WireGuard and SOCKS5 configuration was not deliberately
changed during the test.

## 4. Controlled post-failure workload

A new Brave tab opened a nonce-qualified URL on:

~~~text
example.net
~~~

The result was:

~~~text
LOADED
~~~

The workload therefore completed while the configured HEV/SOCKS5 backend
was unavailable.

## 5. RethinkDNS flow evidence

The relevant Brave/example.net flow was associated in RethinkDNS with:

~~~text
WG
~~~

The supplied RethinkDNS screenshots further showed:

~~~text
application        Brave
domain             example.net
protocol listing   HTTP3
transport detail   UDP/443
proxy association  wg16
~~~

The `wg16` value is retained as a phase-local runtime identifier.

It is operational evidence of a WireGuard-associated path and is not
treated as a stable interface identity or cryptographic tunnel proof.

## 6. HEV non-participation during outage

No attempts to use the unavailable HEV endpoint were observed:

~~~text
TCP/1080 packet delta:        0
UDP/1081 packet delta:        0

A50-to-HEV attempt packets:   0
TCP/1080 attempts:            0
UDP/1081 attempts:            0

HEV log-line delta:           0
~~~

The dedicated failure-window packet capture contained zero matching
packets.

PCAP SHA-256:

~~~text
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

The raw PCAP remains local and is not committed.

## 7. Extended observation window

After the controlled page load, the HEV-unavailable state remained under
observation for an additional period.

No delayed TCP/1080 or UDP/1081 attempt appeared.

This reduces the likelihood that HEV participation was merely delayed
until after the initial application request.

## 8. Original automated classification

The original collection script emitted:

~~~text
INCONCLUSIVE
~~~

This result is preserved.

The reason was not contradictory transport evidence.

The machine classifier required all of the following for its strongest
classification:

~~~text
page = LOADED
flow association = WG
WireGuard UI = ON
SOCKS5 UI = ON
HEV attempts = 0
~~~

The operator recorded:

~~~text
SOCKS5 final UI state = UNKNOWN
~~~

Therefore the strict automatic classifier correctly refused to emit its
strongest state.

## 9. Functional reconciliation

The subsequent evidence reconciliation separated two independent
questions.

### Functional dependency

The evidence establishes:

~~~text
HEV backend unavailable
+
new application workload loaded
+
RethinkDNS flow associated with WG
+
zero HEV connection attempts
~~~

Corrected functional classification:

~~~text
HEV_FAILURE_DID_NOT_AFFECT_TESTED_WG_FLOW
~~~

### SOCKS5 UI persistence

The final SOCKS5 UI state during the outage remains:

~~~text
UNKNOWN / NOT VERIFIED
~~~

No claim is made that the SOCKS5 UI continued to display ON throughout
the failure interval.

## 10. Phase classification

LAB-002H is classified:

~~~text
PASS / TESTED WG FLOW UNAFFECTED BY HEV OUTAGE
~~~

This means:

The tested WireGuard-associated application flow continued successfully
while the HEV/SOCKS5 backend was deliberately unavailable.

No attempt to contact the unavailable HEV endpoint was observed.

This is stronger than simply observing HEV inactivity while HEV was
available because backend availability itself was removed.

## 11. What this does not prove

LAB-002H does not prove:

- a global RethinkDNS fail-open policy
- a global RethinkDNS fail-closed policy
- that SOCKS5 remained visually ON during the full outage
- that every application behaves identically
- that every TCP or UDP flow uses WireGuard
- that SOCKS5 is never selected when WireGuard is enabled
- that HEV failure can never affect another policy configuration
- that WireGuard itself cannot later fail
- cryptographic tunnel establishment

The precise result is scoped to the tested flow and tested combined
configuration.

## 12. HEV restoration

After the controlled failure window, the pinned HEV binary was restored.

The post-test contract verified:

~~~text
HEV process           ACTIVE
HEV TCP/1080          ACTIVE
~~~

The recovery therefore returned the lab to an operational state.

## 13. Evidence identity

Original LAB-002H runtime summary:

~~~text
SHA-256:
21a141764c0ce9297829cb8c4472dd26cf0274fbc6bac0027b952c1885bdbc81
~~~

Functional reconciliation record:

~~~text
SHA-256:
da2e97aebb2383f3f0ebeb20dd27e0ee9f7f2d37089afe87375a0849d0016bd6
~~~

Failure-window PCAP:

~~~text
SHA-256:
704e5e5b3234433c01fcfd1b20a306e77e985038120492dc53965c3edd38a4ea
~~~

Runtime evidence and raw captures remain outside Git.

## 14. Cross-phase significance

LAB-002B established simultaneous configuration-state coexistence.

LAB-002C through LAB-002G repeatedly observed successful DNS, TCP and UDP
behavior without HEV participation and with WireGuard-associated
metadata.

LAB-002H adds controlled failure evidence:

~~~text
HEV available
    ->
HEV deliberately removed
    ->
new WG-associated application flow succeeds
    ->
no HEV connection attempt
~~~

This substantially strengthens the tested model in which SOCKS5 may
remain configured while WireGuard is the effective path for the observed
flows.

It still does not establish a universal RethinkDNS transport-precedence
rule.

## 15. Next phase

LAB-002I will characterize WireGuard failure behavior.

That phase will invert the LAB-002H experiment:

~~~text
HEV / SOCKS5 backend available
WireGuard path deliberately disrupted
~~~

The goal will be to determine whether RethinkDNS:

- switches to SOCKS5
- attempts HEV
- blocks the workload
- uses another route
- or exhibits another explicitly observed behavior

No fallback behavior will be assumed before evidence is collected.

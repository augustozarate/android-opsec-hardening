# LAB-002B-R2 — Proxy-State Reconciliation

**Status:** CHARACTERIZED / TRANSIENT COEXISTENCE; STABLE ACTIVE COEXISTENCE NOT ESTABLISHED

## 1. Purpose

This report corrects and refines the interpretation of the earlier
LAB-002B through LAB-002H observations.

No earlier evidence is deleted.

The correction was triggered by later controlled tests showing that
three RethinkDNS states must be distinguished:

1. proxy configuration is stored
2. proxy toggle is temporarily ON
3. proxy remains selected and operational over time

Those states are not equivalent.

## 2. Original LAB-002B interpretation

LAB-002B originally established that the RethinkDNS UI allowed
WireGuard and SOCKS5 to appear configured at the same time without an
immediate warning.

That observation remains valid.

What was not established at that time was that SOCKS5 remained
continuously enabled and operational while WireGuard was active.

The original interpretation therefore exceeded the evidence available
at that phase.

## 3. Authentication regression discovered during revalidation

A later SOCKS5-only revalidation failed:

~~~text
page result                 FAILED
Rethink matching flow       NO_ENTRY
A50 -> HEV activity         PRESENT
classification              SOCKS_ONLY_BASELINE_NOT_VALIDATED
~~~

Runtime summary SHA-256:

~~~text
f3a9275115bab4d16551c1e3d305f1b78687e3e75aa7b8bcd6cf567a67529813
~~~

A dedicated diagnostic then separated HEV health from the Rethink
client state.

Independent HEV validation succeeded:

~~~text
SOCKS5 method negotiation   PASS
username/password auth      PASS
CONNECT example.com:443     PASS
~~~

At the same time, the RethinkDNS SOCKS5 password field was observed as:

~~~text
EMPTY
~~~

The A50 repeatedly established TCP sessions toward HEV but the browser
workload failed.

Diagnostic classification:

~~~text
HEV_HEALTHY_TCP_ESTABLISHED_RETHINK_SOCKS_SESSION_FAILING
~~~

Diagnostic summary SHA-256:

~~~text
3e17483c80cf7f3f7107980debc4827107ce64287b5351c8d2abbfeaacd15fff
~~~

Diagnostic PCAP SHA-256:

~~~text
956aaf7c64a4fe9f08dab740b7fe019d424338ee7a205bd78447dd29f7a04556
~~~

The raw packet capture remains local because SOCKS5 authentication
material may appear in payload.

## 4. Restored SOCKS5 baseline

After restoring the locally stored HEV password in RethinkDNS, with all
WireGuard profiles disabled, SOCKS5 was revalidated.

Observed result:

~~~text
WireGuard                   OFF
SOCKS5                      ON
password field              PRESENT
page                        LOADED
Rethink association         SOCKS5
TCP/1080 activity           PRESENT
UDP/1081 activity           PRESENT
HEV log activity            PRESENT
SOCKS5 after workload       ON
~~~

Classification:

~~~text
SOCKS_AUTH_RESTORED_BASELINE_PASS
~~~

Runtime summary SHA-256:

~~~text
c5cf30abc7c6837df01caf955b49e5473eeab478de841a4830412c105c49e7e2
~~~

PCAP SHA-256:

~~~text
9b5a8ea5b927624ae0fafa731ea999e13a33f6d577642a6990ec8a8342ecd880
~~~

This establishes that the HEV backend and the RethinkDNS SOCKS5 path
were operational after credential restoration.

## 5. WireGuard transition with Advanced Always-on disabled

The next controlled experiment started from that restored SOCKS5
baseline.

Precondition:

~~~text
SOCKS5                      ON
password                    PRESENT
WireGuard                   OFF
HEV                         ACTIVE
~~~

One known-working WireGuard profile was then enabled with the
RethinkDNS WireGuard Advanced `Always-on` option explicitly disabled.

Immediately after WireGuard activation:

~~~text
WireGuard                   ON
SOCKS5                      ON
state                       BOTH_ON
~~~

No deliberate browser workload was generated.

After approximately 30 seconds:

~~~text
WireGuard                   ON
SOCKS5                      OFF
state                       WG_ON_SOCKS_OFF
~~~

During that transition:

~~~text
new TCP/1080 packets        0
new UDP/1081 packets        0
new HEV log lines           0
~~~

Classification:

~~~text
SOCKS_DEACTIVATION_NOT_SPECIFIC_TO_ALWAYS_ON
~~~

Runtime summary SHA-256:

~~~text
3ee3bb97d93450b531a4ca5c49d084ce2ec6956fa1b97bf9193f2978204a2eeb
~~~

## 6. Interpretation

The current evidence supports all of the following:

- SOCKS5 works correctly by itself when its credential is present.
- WireGuard and SOCKS5 can briefly appear enabled simultaneously.
- that transient state does not establish durable dual-proxy operation.
- SOCKS5 was observed changing from ON to OFF after WireGuard activation.
- the transition occurred with WireGuard Advanced `Always-on` disabled.
- therefore `Always-on` is not required for the observed SOCKS5 deactivation.
- no HEV activity occurred during the measured transition window.
- the exact internal RethinkDNS arbitration mechanism remains unknown.

The most precise current model is:

~~~text
configuration coexistence           OBSERVED
transient active UI coexistence     OBSERVED
stable active coexistence           NOT ESTABLISHED
SOCKS5-only operation               VALIDATED
WG-associated operation             VALIDATED
Always-on required as trigger       NOT SUPPORTED
internal proxy arbitration policy   NOT YET PROVEN
~~~

## 7. Consequence for LAB-002B

LAB-002B should no longer be represented simply as:

~~~text
PASS / configuration coexistence
~~~

Its corrected state is:

~~~text
CHARACTERIZED
TRANSIENT COEXISTENCE; STABLE ACTIVE COEXISTENCE NOT ESTABLISHED
~~~

The original observation remains historically valid but its scope is
narrower than first interpreted.

## 8. Consequence for LAB-002C through LAB-002G

The network observations from LAB-002C through LAB-002G remain valid:

- successful application workloads
- WireGuard-associated Rethink metadata
- DNS behavior
- public-egress difference
- UDP/443 and HTTP/3 observations
- absence of A50-to-HEV traffic during those measured workloads

However, those phases must not be used to claim that SOCKS5 was
continuously ON while WireGuard handled the flows unless the SOCKS5 UI
state was explicitly verified for that phase.

## 9. Consequence for LAB-002H

LAB-002H successfully proved a narrower fact:

~~~text
HEV backend deliberately unavailable
+
tested WireGuard-associated workload continued
+
no A50-to-HEV attempt observed
~~~

That remains useful evidence for WireGuard-path independence from HEV.

However, the experiment did not establish that SOCKS5 was actively ON
throughout the HEV outage.

Therefore LAB-002H should not be presented as a complete validation of
failure behavior for an actively selected SOCKS5 path.

Its corrected state is:

~~~text
CHARACTERIZED
HEV OUTAGE CONTROL; ACTIVE SOCKS PRECONDITION NOT ESTABLISHED
~~~

## 10. Consequence for LAB-002I

LAB-002I remains:

~~~text
NOT RUN
~~~

WireGuard failure/fallback testing is intentionally deferred until the
proxy-state arbitration behavior is better characterized.

## 11. Methodological correction

This sequence reinforces a core project rule:

~~~text
Configured != Enabled
Enabled != Persistently Enabled
Persistently Enabled != Selected
Selected != Successfully Transporting Traffic
~~~

Future combined-proxy experiments must explicitly verify each relevant
state before and after the controlled workload.

## 12. Next investigation

The next experiment should inspect RethinkDNS runtime/debug evidence
around the transition:

~~~text
SOCKS5 ON
+
WireGuard activation
+
temporary BOTH_ON
+
SOCKS5 OFF
~~~

The goal is to determine whether Rethink records an explicit:

- proxy replacement
- tunnel reconciliation
- policy conflict
- state migration
- service restart
- or other internal event

No specific mechanism is assumed before evidence is collected.

<!-- LAB-002B-R3-R6-FOLLOWUP -->
## 13. Follow-up — LAB-002B-R3-R6

The runtime/debug investigation proposed above was subsequently
performed.

The follow-up identified two confounders in the original R3 transition:

1. the HEV SOCKS5 backend was not running during the initial runtime
   observation
2. WhatsApp had a per-application WireGuard `BLOQUEO` policy that pinned
   UID `10316` to inactive `wg14`

After restoring a known-good HEV backend, a clean end-to-end SOCKS5
baseline was re-established with Brave and `example.com`.

A controlled A/B then changed only the per-profile `BLOQUEO` state while
leaving the application assigned to the same inactive WireGuard profile.

Observed result:

~~~text
BLOQUEO ON
→ WhatsApp selected wg14
→ wg14 unavailable
→ no application-flow S5 fallback

BLOQUEO OFF
→ no wg14 lockdown selection
→ WhatsApp application flows selected S5
→ physical A50-to-HEV transport observed
~~~

This supports a narrower causal conclusion about per-profile lockdown
precedence in the tested RethinkDNS v0.5.7 configuration.

It does not establish a universal WireGuard/SOCKS5 precedence rule or
stable simultaneous active transport.

See:

`LAB-002B-R3-R6-runtime-policy-precedence.md`

# LAB-002B-R3-R6 — Runtime Proxy Policy and Per-App WireGuard Precedence

**Status:** CHARACTERIZED / PER-APP WIREGUARD LOCKDOWN PRECEDENCE VALIDATED

## 1. Purpose

This follow-up extends the LAB-002B-R2 proxy-state reconciliation with
runtime evidence collected from RethinkDNS v0.5.7 on the Android test
device.

The investigation had two goals:

1. determine why SOCKS5 appeared to transition OFF after WireGuard
   activation
2. distinguish global SOCKS5 behavior from per-application WireGuard
   policy behavior

No previous LAB-002 evidence is deleted.

The results refine the interpretation of LAB-002B while preserving its
current `CHARACTERIZED` status.

## 2. Runtime environment

Observed Android environment:

~~~text
device          Samsung SM-A505F
Android         13
RethinkDNS      v0.5.7
package         com.celzero.bravedns
~~~

ADB/logcat was used only as an observability mechanism.

Raw logcat and packet captures remain local and are not committed.

## 3. LAB-002B-R3 initial runtime observation

The controlled starting state was:

~~~text
RethinkDNS                     ON
WireGuard profiles             OFF
SOCKS5                         ON
WireGuard Advanced Always-on   OFF
~~~

The observed UI transition was:

~~~text
SOCKS_ONLY
→ enable known-working WireGuard
→ WG_ON_SOCKS_OFF
~~~

The state remained:

~~~text
WG_ON_SOCKS_OFF
~~~

at the 10-second, 20-second and 30-second observations.

Initial machine classification:

~~~text
SOCKS_DEACTIVATED_DURING_WG_ACTIVATION
~~~

R3 summary SHA-256:

~~~text
882eb491c4fa2ef7e1dacab214e89a7159db98a39f4964cdc4d3584e4ffcd54d
~~~

Later forensic analysis showed that this transition could not be used as
clean causal proof that enabling WireGuard itself disabled a healthy
SOCKS5 transport.

Two confounders were identified.

## 4. Confounder 1 — HEV backend was unavailable

During retrospective R3 analysis, the configured HEV endpoint was found
to have no active TCP/1080 listener.

The observed condition was equivalent to:

~~~text
SOCKS5 configured             YES
SOCKS5 UI enabled             YES
HEV process                   OFF
TCP/1080 listener             OFF
successful SOCKS transport    NOT ESTABLISHED
~~~

This explained `connection refused` events present in the R3 runtime
evidence.

The HEV backend was then explicitly restored and validated with:

~~~text
TCP connect                    PASS
SOCKS5 method negotiation      PASS
SOCKS5 authentication          PASS
CONNECT example.com:443        PASS
~~~

Future combined-proxy experiments must therefore validate the backend
before interpreting Android proxy UI state.

## 5. Confounder 2 — per-app WireGuard lockdown

Runtime logs also showed that WhatsApp UID `10316` had a persistent
per-application WireGuard policy:

~~~text
lockdown wg for app(10316) => return wg14
~~~

The corresponding RethinkDNS profile was identified in the UI as
WireGuard profile `(14)`.

Observed profile state:

~~~text
profile (14)          OFF
selected application  WhatsApp
BLOQUEO               ON
SIEMPRE ACTIVO        OFF
~~~

RethinkDNS continued selecting `wg14` for WhatsApp even though the
profile itself was disabled.

Firestack then reported:

~~~text
proxy: for: wg14; not found
~~~

This was not treated as a stale configuration artifact.

The UI description of `BLOQUEO` establishes that selected applications
remain routed only through that WireGuard profile regardless of whether
the profile itself is active or disabled.

## 6. Correct physical-interface model

An early Android-to-HEV packet capture incorrectly used:

~~~text
10.111.222.1
~~~

as the Android source address.

ADB routing inspection showed that address belonged to the internal
Rethink VPN/TUN path:

~~~text
dev tun2
src 10.111.222.1
~~~

The direct route to the HEV host instead used:

~~~text
dev wlan0
src 10.36.136.46
~~~

The packet-capture model was corrected accordingly.

This reinforces the distinction:

~~~text
VPN/TUN identity != physical LAN identity
~~~

## 7. LAB-002B-R5-R4 — clean SOCKS5 end-to-end baseline

After restoring HEV and correcting the packet-capture identity, a
clean Brave workload against `example.com` was executed with:

~~~text
RethinkDNS       ON
WireGuard        OFF
SOCKS5           ON
HEV              known-good
~~~

Observed application result:

~~~text
page result            LOADED
Rethink flow proxy     S5
~~~

Physical evidence:

~~~text
captured packets       1144
A50 -> HEV TCP/1080    568
HEV -> A50 TCP/1080    524
A50 SYN                21
HEV SYN/ACK            21
A50 -> HEV UDP/1081    26
HEV -> A50 UDP/1081    26
HEV log delta          24
~~~

Rethink runtime evidence:

~~~text
example.com + S5 signals    28
Brave UID + S5 signals      27
upstreamBlocks=true          0
example.com -> 0.0.0.0       0
return Block                 0
connection refused           0
~~~

Machine classification:

~~~text
SOCKS_ANDROID_END_TO_END_BASELINE_PASS
~~~

Summary SHA-256:

~~~text
fffeb8ea075b23c92fc39c123d2daf133d9de96130022bb007942602216b9f87
~~~

Local raw PCAP SHA-256:

~~~text
ed7f1c5843f5a00b7a87a37debdf4aca1b91bd29cbdf922114fed03e8eed815a
~~~

The raw PCAP remains local.

## 8. DNS and application proxy selection are distinct

The R3-R6 sequence showed that DNS proxy selection and application-flow
proxy selection must not be treated as equivalent.

With WhatsApp locked to inactive `wg14`, application flows were pinned
to `wg14`, while WhatsApp DNS activity could still use SOCKS5.

Therefore:

~~~text
DNS via S5 != application traffic via S5
~~~

Both layers must be measured independently.

## 9. LAB-002B-R6A — BLOQUEO ON control

Controlled state:

~~~text
WhatsApp UID             10316
profile (14)             OFF
WhatsApp assigned        YES
BLOQUEO                  ON
SIEMPRE ACTIVO           OFF
SOCKS5                   ON
HEV                      known-good
global Proxy Lockdown    unchanged
~~~

Observed policy signals:

~~~text
wg14 lockdown selections      16
wg14 unavailable/not found    98
WhatsApp S5 app flows          0
WhatsApp/wg14 references     117
WhatsApp DNS via S5           22
return Block                   0
~~~

Representative runtime sequence:

~~~text
lockdown wg for app(10316) => return wg14
returning wg14
proxy: for: wg14; not found
~~~

No application-flow fallback to SOCKS5 was observed.

Machine classification:

~~~text
WHATSAPP_PINNED_TO_INACTIVE_WG14_NO_S5_APP_FALLBACK
~~~

Summary SHA-256:

~~~text
8c57a36f548933c7e7045545699a2b8ed19433883dfe07d2e5be2608175cb2a2
~~~

## 10. LAB-002B-R6B — BLOQUEO OFF A/B

Exactly one policy variable was changed:

~~~text
BLOQUEO ON -> OFF
~~~

All relevant surrounding state was held constant:

~~~text
profile (14)             OFF
WhatsApp assigned        YES
SIEMPRE ACTIVO           OFF
SOCKS5                   ON
HEV                      known-good
global Proxy Lockdown    unchanged
~~~

Observed policy signals:

~~~text
wg14 lockdown selections       0
WhatsApp returning wg14        0
WhatsApp returning S5          6
WhatsApp S5 tracker marks      6
WhatsApp S5 total             12
WhatsApp DNS via S5           12
return Block                   0
~~~

Representative application-flow evidence included:

~~~text
socks5 proxy for ... 10316 ... returning S5
proxyDetails=S5
~~~

Corroborating physical transport:

~~~text
captured packets        304
A50 -> HEV TCP/1080     133
HEV -> A50 TCP/1080     121
A50 -> HEV UDP/1081      24
HEV -> A50 UDP/1081      26
HEV log delta              6
~~~

Machine classification:

~~~text
BLOQUEO_OFF_ALLOWS_WHATSAPP_S5_APP_FALLBACK
~~~

Summary SHA-256:

~~~text
ea68b862d31f1bd2314d3ab3904bd65212b3a1a20132db8cccb177a5b440de13
~~~

Local raw PCAP SHA-256:

~~~text
8bc7adc8ebcc50a8c22737363c32d430040ee9454c332d62203bad70b407bb1c
~~~

The raw PCAP remains local.

## 11. A/B conclusion

Within the tested RethinkDNS v0.5.7 configuration:

~~~text
WhatsApp assigned to inactive wg14
+
global SOCKS5 enabled
+
HEV known-good
~~~

produced two different application-routing outcomes depending on one
per-profile policy setting.

With `BLOQUEO ON`:

~~~text
WhatsApp
→ selected wg14
→ wg14 unavailable
→ no application fallback to S5
~~~

With `BLOQUEO OFF`:

~~~text
WhatsApp
→ no wg14 lockdown selection
→ application flows selected S5
→ physical A50-to-HEV transport observed
~~~

The experiment therefore supports the narrower causal conclusion:

> In this tested configuration, assignment of an application to an
> inactive WireGuard profile does not by itself prevent SOCKS5 fallback.
> Enabling that profile's `BLOQUEO` policy causes application flows to
> remain pinned to the assigned WireGuard profile and prevents the
> observed SOCKS5 application fallback.

## 12. Scope limits

The R6 A/B does not establish:

- a universal rule for every RethinkDNS version
- identical behavior for every application
- identical behavior for every WireGuard provider/profile
- a universal relationship between Android VPN lockdown and Rethink
  per-profile `BLOQUEO`
- stable simultaneous active WireGuard + SOCKS5 transport
- a universal WireGuard/SOCKS5 chaining order

Global Proxy Lockdown was deliberately left unchanged.

Therefore this experiment isolates per-profile `BLOQUEO`; it does not
characterize global Proxy Lockdown independently.

## 13. Revised state model

The accumulated evidence supports the expanded project rule:

~~~text
Configured
!= Assigned
!= Enabled
!= Persistently Enabled
!= Active
!= Selected
!= Locked
!= Successfully Transporting Traffic
~~~

For Android/Rethink experiments, DNS transport and application transport
must also be recorded separately.

## 14. Consequence for LAB-002B

LAB-002B remains:

~~~text
CHARACTERIZED
~~~

The original configuration-coexistence observation remains valid.

R2 correctly established that stable active WireGuard + SOCKS5
coexistence had not been demonstrated.

R3-R6 now adds:

- runtime/logcat observability
- physical TUN-versus-WLAN identity correction
- a restored end-to-end SOCKS5 baseline
- explicit separation of DNS and application proxy selection
- a controlled per-profile `BLOQUEO` A/B
- validated per-app WireGuard lockdown precedence in the tested state

These findings refine LAB-002B but do not justify changing it to `PASS`.

## 15. Consequence for LAB-002I and LAB-002J

LAB-002I remains:

~~~text
NOT RUN
~~~

LAB-002J remains:

~~~text
NOT RUN
~~~

The per-app lockdown ambiguity that previously contaminated the proxy
state analysis is now characterized.

Future WireGuard failure and fail-open/fail-closed experiments can use
the R5-R4 known-good SOCKS5 baseline and must explicitly declare:

- per-app WireGuard assignment
- per-profile `BLOQUEO`
- global Proxy Lockdown
- WireGuard activation state
- SOCKS5 backend health
- DNS proxy selection
- application proxy selection
- physical transport evidence where relevant

## 16. Evidence handling

Raw evidence remains under local state directories.

The Git repository contains only:

- documentation
- classifications
- sanitized observations
- evidence hashes

No raw PCAP or raw logcat file is committed.

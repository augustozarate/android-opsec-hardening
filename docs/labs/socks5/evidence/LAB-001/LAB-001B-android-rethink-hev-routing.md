# LAB-001B — Android / RethinkDNS / HEV SOCKS5 Routing Evidence

## 1. Purpose

This report records the Android-side extension of LAB-001.

The objective was to determine whether a Samsung Galaxy A50 running
RethinkDNS could use an authenticated HEV SOCKS5 server hosted on a
bridged Kali Linux system, while preserving observable and reproducible
routing boundaries.

The validation covered:

- Android-to-Kali LAN reachability.
- RethinkDNS private-IP routing behavior.
- Authenticated SOCKS5 TCP transport.
- Two-leg TCP traffic correlation.
- SOCKS5 UDP ASSOCIATE behavior.
- A fixed and restricted UDP relay.
- Two-leg UDP traffic correlation.
- IPv4/IPv6 behavior when the SOCKS5 gateway has no global IPv6 route.

WireGuard integration was intentionally excluded from this phase.

## 2. Environment

Validated environment:

- Android device: Samsung Galaxy A50.
- Android client IP: `10.36.136.35`.
- RethinkDNS version: `v0.5.7`.
- Kali Linux SOCKS5 gateway IP: `10.36.136.33/26`.
- Default IPv4 gateway: `10.36.136.1`.
- VMware networking mode: Bridged.
- HEV SOCKS5 TCP port: `1080`.
- HEV SOCKS5 UDP relay port: `1081`.

Relevant Android / RethinkDNS state during the final baseline:

- RethinkDNS: enabled.
- SOCKS5 proxy: enabled.
- SOCKS5 authentication: enabled.
- Proxy Lockdown: enabled.
- Private-IP bypass ("Do not route private IPs"): enabled.
- Android Always-on VPN: enabled.
- Android "Block connections without VPN": disabled.
- WireGuard: disabled for this LAB phase.
- RethinkDNS IP version: IPv4 after A/B validation.

Authentication values are intentionally omitted from this report.

## 3. Bridged Network Baseline

After moving the Kali VM from VMware NAT to Bridged networking:

~~~text
Kali:
10.36.136.33/26

A50:
10.36.136.35

Gateway:
10.36.136.1
~~~

The A50 and Kali were directly reachable within the same IPv4 subnet.

Observed validation included:

~~~text
ip route get 10.36.136.35
~~~

showing direct delivery through `eth0`, plus successful ICMP and ARP
reachability.

The observed Android MAC address is not treated as a stable device
identity because Android may use randomized/local MAC addresses.

Result:

~~~text
LAB-001B-L2/L3: PASS
~~~

## 4. RethinkDNS Private-IP Behavior

A temporary HTTP canary was bound only to:

~~~text
10.36.136.33:18080
~~~

and protected with a temporary nftables source restriction permitting
only:

~~~text
10.36.136.35
~~~

With RethinkDNS disabled, the A50 reached the HTTP canary successfully.

With RethinkDNS enabled and private-IP routing still handled through the
VPN path, the request failed before reaching Kali.

No additional nftables counter increment and no new HTTP request were
observed on the gateway during that failure.

The successful working state was:

~~~text
RethinkDNS                         ON
Do not route private IPs           ON
Android Always-on VPN              ON
Android Block connections w/o VPN  OFF
~~~

After enabling the private-IP bypass, the HTTP canary was reachable
again from the A50.

Result:

~~~text
Private-IP routing behavior: CHARACTERIZED
Private-IP bypass:            PASS
~~~

## 5. Authenticated HEV LAN Listener

HEV was bound only to the Kali bridged address:

~~~text
10.36.136.33:1080
~~~

Observed listener state:

~~~text
[::ffff:10.36.136.33]:1080
~~~

Two listener file descriptors were expected because the tested HEV
configuration used two workers.

The SOCKS5 service was protected by two independent controls:

1. SOCKS5 username/password authentication.
2. nftables source filtering restricted to the A50 IPv4 address.

A negative authentication control returned:

~~~text
curl: (97) No authentication method was acceptable.
~~~

An authenticated control returned:

~~~text
http=200 proxy_peer=10.36.136.33
~~~

Result:

~~~text
Authenticated SOCKS5: PASS
~~~

Credential material is stored only in local runtime state and is not
part of the Git repository.

## 6. Android → RethinkDNS → HEV TCP Validation

After configuring RethinkDNS to use the authenticated HEV proxy, the
gateway immediately began receiving SOCKS5 traffic from the A50.

During the controlled browser test, the nftables TCP/1080 counter moved
from:

~~~text
528 packets / 80778 bytes
~~~

to:

~~~text
782 packets / 120720 bytes
~~~

Delta:

~~~text
+254 packets
+39942 bytes
~~~

The unauthorized-source DROP rule remained at zero.

Concurrent TCP sessions were observed between:

~~~text
10.36.136.35:<ephemeral>
        ↕
10.36.136.33:1080
~~~

while HEV remained the owning process.

Result:

~~~text
Android → RethinkDNS → HEV SOCKS5 TCP: PASS
~~~

## 7. Two-Leg TCP Traffic Correlation

A control-flag packet capture was performed for both sides of the proxy
path.

The client-side capture showed multiple TCP handshakes:

~~~text
10.36.136.35:<ephemeral> → 10.36.136.33:1080
~~~

The outbound capture simultaneously showed new connections from Kali to
public TCP/443 destinations.

During the same capture window, HEV logged these unique destinations:

~~~text
3.163.139.124:443
3.163.139.48:443
45.90.30.0:443
57.144.102.141:443
~~~

The outbound PCAP contained exactly the same four unique TCP/443
destinations.

Eight client-side TCP SYN flows toward HEV were observed during the
capture window.

Result:

~~~text
Client-side SOCKS5 leg:    PASS
HEV outbound TCP leg:      PASS
Cross-source correlation:  PASS
~~~

The PCAPs are retained locally and are intentionally not committed.

Local evidence hashes:

~~~text
LAB-001B-03C A50 → HEV control-flag capture

SHA-256:
5bff0a83317472e249a67035b33eeab4ad73b64d20827fb6f764d573eb8eb316
~~~

~~~text
LAB-001B-03C HEV → Internet control-flag capture

SHA-256:
725254bb8314e85015c7b2d8417b47820d9022a0e1dd347f5986581ba3682eba
~~~

The capture is described as a control-flag capture rather than a strict
header-only capture because TCP FIN packets may legally contain payload.

## 8. SOCKS5 UDP ASSOCIATE

HEV was configured with a deterministic UDP relay:

~~~text
TCP control:
10.36.136.33:1080

UDP relay:
10.36.136.33:1081
~~~

nftables restricted both services to:

~~~text
10.36.136.35
~~~

Before UDP activity, no persistent UDP/1081 socket was visible through
the one-second `ss` sampler.

During the Android test, HEV logged:

~~~text
socks5 server udp [0.0.0.0]:0
~~~

and the UDP/1081 nftables counter changed from:

~~~text
0 packets / 0 bytes
~~~

to:

~~~text
25 packets / 14404 bytes
~~~

A truncated local PCAP also contained exactly 25 datagrams from the A50
to the HEV UDP relay.

Observed source flows included:

~~~text
10.36.136.35:35786 → 10.36.136.33:1081
10.36.136.35:46165 → 10.36.136.33:1081
~~~

This distinguishes two separate findings:

~~~text
UDP ASSOCIATE negotiated: PASS
UDP relay actually used:  PASS
~~~

Local evidence hash:

~~~text
SHA-256:
2fbd86525c85a8e9514b2cdf61e608b9d5840d4a51b6d3764ce2c7f3539b1a59
~~~

The PCAP is retained locally only.

## 9. IPv4 / IPv6 Gateway Baseline

The Kali gateway had functional IPv4 connectivity.

Validated IPv4 controls included:

~~~text
Gateway 10.36.136.1:
reachable

example.com:
HTTP 200

github.com:
HTTP 200

1.1.1.1:
HTTP 200
~~~

System DNS resolution also succeeded through the configured resolver,
the gateway resolver, and a direct `8.8.8.8` query during the recovered
baseline.

IPv6 was materially different.

The only IPv6 address on `eth0` was link-local:

~~~text
fe80::/64
~~~

There was no global IPv6 address and no IPv6 default route.

A route lookup toward a public IPv6 destination returned:

~~~text
RTNETLINK answers: Network is unreachable
~~~

Result:

~~~text
IPv4 routing:             PASS
IPv4 Internet:            PASS
IPv4 DNS:                 PASS
IPv6 link-local:          PRESENT
IPv6 global connectivity: ABSENT
IPv6 default route:       ABSENT
IPv6 Internet routing:    UNAVAILABLE
~~~

An earlier isolated IPv4 DNS timeout was treated as transient because a
subsequent controlled recovery test validated routing, DNS, and HTTPS.

## 10. RethinkDNS Automatic IP Mode

With RethinkDNS configured for automatic IP version selection, HEV
received IPv6 destination requests such as:

~~~text
[2606:4700:10::6814:179a]:443
[2606:4700:10::ac42:93f3]:443
~~~

Each was followed by a HEV connection failure marker.

This was consistent with the independently validated absence of a
global IPv6 route on Kali.

Immediately afterward, HEV received an IPv4 destination:

~~~text
[104.20.23.154]:443
~~~

while the application request remained usable.

Observed behavior:

~~~text
Rethink Automatic
       |
       +-- IPv6 destination
       |       |
       |       +-- HEV
       |             |
       |             +-- no IPv6 route
       |                     |
       |                     +-- failure
       |
       +-- IPv4 destination
               |
               +-- HEV
                       |
                       +-- success
~~~

Result:

~~~text
Automatic IPv6 attempt/fallback behavior: CHARACTERIZED
~~~

## 11. RethinkDNS IPv4-Only A/B Test

RethinkDNS was then changed from:

~~~text
Automatic
~~~

to:

~~~text
IPv4
~~~

No other routing component was intentionally changed.

During the IPv4-only observation window:

~~~text
IPv6 SOCKS destinations:
none observed

HEV connect failure markers:
none observed
~~~

SOCKS5 transport remained active, including the UDP relay.

This demonstrates that forcing IPv4 in RethinkDNS suppressed the
otherwise unusable IPv6 attempts in this specific gateway topology.

The result is environment-specific and is not a universal RethinkDNS
recommendation.

Recommended state for this tested gateway:

~~~text
RethinkDNS IP version: IPv4
~~~

until the Kali gateway has validated global IPv6 connectivity.

Result:

~~~text
RethinkDNS IPv4-only A/B: PASS
~~~

## 12. Two-Leg UDP Egress Correlation

A final truncated outbound UDP capture was performed while RethinkDNS
remained in IPv4-only mode.

The A50 → HEV UDP/1081 firewall counter changed from:

~~~text
150 packets / 87294 bytes
~~~

to:

~~~text
162 packets / 94142 bytes
~~~

Delta:

~~~text
+12 packets
+6848 bytes
~~~

During the same controlled window, the outbound PCAP contained exactly
12 UDP datagrams from Kali toward:

~~~text
104.20.23.154:443
~~~

which was also a validated IPv4 address for `example.com` during this
LAB.

Two additional UDP packets in the broader capture window targeted:

~~~text
162.159.200.123:123
~~~

and were treated as unrelated background NTP traffic rather than part
of the controlled browser correlation.

HEV simultaneously logged a SOCKS5 UDP association.

Observed path:

~~~text
A50
10.36.136.35
       |
       | SOCKS5 UDP relay
       v
Kali / HEV
10.36.136.33:1081
       |
       | IPv4 UDP
       v
104.20.23.154:443
~~~

UDP/443 is consistent with QUIC/HTTP/3 behavior, but the application
protocol was not independently decoded and therefore is not asserted as
validated.

Result:

~~~text
A50 → HEV UDP leg:       PASS
HEV → Internet UDP leg:  PASS
Two-leg UDP correlation: PASS
~~~

Local evidence hash:

~~~text
SHA-256:
1bfdf8f861d26879f3fc3177bddb85f5cc07160941a91524822cea95071ab973
~~~

The PCAP is retained locally only.

## 13. Firewall Boundary

The final tested nftables policy restricted:

~~~text
TCP/1080
UDP/1081
~~~

to:

~~~text
10.36.136.35
~~~

with subsequent DROP rules for other inbound sources on those ports.

During the recorded validation windows, the DROP counters remained at
zero.

This confirms the configured source restriction and absence of observed
unauthorized traffic during the tests.

It does not constitute an active hostile-peer or second-client negative
test.

## 14. Evidence Handling

The following evidence types were used:

- HEV application logs.
- nftables counters.
- `ss` socket observations.
- HTTP positive controls.
- DNS and routing controls.
- Local packet captures.
- SHA-256 hashes for retained PCAP files.
- Android screenshots.

Sensitive material is intentionally excluded.

The repository does not contain:

- SOCKS5 passwords.
- Local credential files.
- Raw PCAP payloads.
- Runtime PID files.
- Runtime HEV configuration containing credentials.

## 15. Scope Limitations

LAB-001B does not validate:

- WireGuard + SOCKS5 chaining.
- WireGuard and SOCKS5 simultaneous policy behavior.
- RethinkDNS fail-open behavior.
- RethinkDNS fail-closed behavior.
- Android reboot persistence.
- Gateway reboot persistence.
- Automatic service startup.
- Active unauthorized-LAN-client rejection.
- Native end-to-end IPv6 proxying.
- Production deployment suitability.

Those behaviors require independent validation.

## 16. Result Summary

Validated:

~~~text
Bridged networking                    PASS
A50 ↔ Kali L2/L3                      PASS
Rethink private-IP behavior           CHARACTERIZED
Private-IP bypass                     PASS

HEV LAN listener                      PASS
SOCKS5 authentication                 PASS
A50-only TCP firewall boundary        CONFIGURED / OBSERVED
A50-only UDP firewall boundary        CONFIGURED / OBSERVED

A50 → HEV TCP                         PASS
HEV → Internet TCP                    PASS
Two-leg TCP correlation               PASS

SOCKS5 UDP ASSOCIATE                  PASS
A50 → HEV UDP/1081                    PASS
HEV → Internet UDP                    PASS
Two-leg UDP correlation               PASS

IPv4 gateway connectivity             PASS
IPv6 gateway limitation               CHARACTERIZED
Rethink Automatic IP behavior         CHARACTERIZED
Rethink IPv4-only A/B                 PASS
~~~

Overall result:

~~~text
LAB-001B: PASS
~~~

## 17. Conclusion

LAB-001B demonstrates that RethinkDNS v0.5.7 on the tested Samsung
Galaxy A50 can use an authenticated remote HEV SOCKS5 server over a
controlled bridged LAN.

Both TCP and UDP proxy paths were independently observed.

The TCP path was correlated across:

~~~text
A50 → HEV
HEV → Internet
~~~

and the UDP path was likewise correlated across:

~~~text
A50 → HEV UDP relay
HEV → Internet UDP
~~~

The experiment also demonstrated an environment-dependent IPv6
constraint: RethinkDNS Automatic mode generated IPv6 connection
attempts even though the Kali gateway had no global IPv6 route.
Forcing IPv4 removed those failed attempts while preserving validated
SOCKS5 TCP and UDP operation.

WireGuard integration remains outside LAB-001B and must be evaluated as
a separate experimental phase.

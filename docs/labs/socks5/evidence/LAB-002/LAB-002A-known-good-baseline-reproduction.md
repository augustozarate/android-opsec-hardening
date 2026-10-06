# LAB-002A — Known-Good SOCKS5 Baseline Reproduction

**Status:** PASS / RECOVERED

## 1. Objective

Reproduce the known-good LAB-001B SOCKS5 path immediately before
introducing WireGuard as a new experimental variable.

The intended reference state was:

~~~text
RethinkDNS                  ON
SOCKS5                      ON
WireGuard                   OFF
Proxy Lockdown              ON
Do not route private IPs    ON
Android Always-on VPN       ON
Android VPN Lockdown        OFF
RethinkDNS IP version       IPv4
~~~

## 2. Initial reproduction result

The first LAB-002A reproduction attempt did not reproduce the known-good
baseline.

Observed during the failed attempt:

- HEV process was running.
- HEV TCP/1080 listeners were present.
- HEV configuration remained intact.
- No new HEV SOCKS5 events were recorded.
- A50-specific TCP/1080 accept delta was zero.
- A50-specific UDP/1081 accept delta was zero.
- No active A50-to-HEV TCP session was observed.
- The controlled page request did not complete during the observation
  window.

At the same time, the generic TCP/1080 drop counter increased
substantially.

This indicated that traffic was reaching the protected HEV port but was
not matching the expected A50 source-address rule.

## 3. Root-cause identification

The A50 IPv4 address had changed.

Previous LAB-001B address:

~~~text
10.36.136.35
~~~

Current LAB-002A address:

~~~text
10.36.136.37
~~~

Kali neighbor-state observations showed:

~~~text
10.36.136.35  FAILED
10.36.136.37  present/reachable
~~~

The old address did not answer the controlled reachability probe.

The new address responded successfully:

~~~text
3 packets transmitted
3 packets received
0% packet loss
~~~

The nftables policy still authorized only the previous source address:

~~~text
10.36.136.35 -> TCP/1080 -> ACCEPT
10.36.136.35 -> UDP/1081 -> ACCEPT
other sources -> TCP/1080 -> DROP
other sources -> UDP/1081 -> DROP
~~~

Therefore, traffic from the A50 at 10.36.136.37 did not match the
source-specific allow rules and reached the generic deny rule instead.

## 4. Recovery action

Only the A50 source address in the existing nftables accept rules was
changed.

The policy became:

~~~text
10.36.136.37 -> TCP/1080 -> ACCEPT
other sources -> TCP/1080 -> DROP

10.36.136.37 -> UDP/1081 -> ACCEPT
other sources -> UDP/1081 -> DROP
~~~

The generic drop rules were preserved.

No WireGuard setting was enabled or changed.

No HEV listener or authentication setting was relaxed.

## 5. Post-recovery controlled observation

Immediately after the ACL source-address correction, the controlled A50
test produced new traffic through the authorized HEV path.

### TCP/1080

Observed delta:

~~~text
packets: +108
bytes:   +22818
~~~

### UDP/1081

Observed delta:

~~~text
packets: +24
bytes:   +13885
~~~

The generic TCP/1080 drop counter did not increase during this recovery
test.

The generic UDP/1081 drop counter remained at zero.

## 6. HEV observations

Seven new HEV events were recorded.

TCP destinations observed:

~~~text
45.90.28.0:443
172.217.118.4:443
172.217.115.4:443
104.20.23.154:443
172.217.28.14:443
~~~

Two SOCKS5 UDP ASSOCIATE events were also observed:

~~~text
socks5 server udp [0.0.0.0]:0
socks5 server udp [0.0.0.0]:0
~~~

No HEV connect failure marker was observed during the recovery window.

## 7. Classification

LAB-002A is classified:

~~~text
PASS / RECOVERED
~~~

The known-good SOCKS5 baseline was successfully reproduced after
correcting the stale source-IP ACL.

Validated or reproduced properties:

- A50 reachability to the Kali gateway
- authenticated HEV service availability
- A50-to-HEV TCP/1080 transport
- A50-to-HEV UDP/1081 transport
- HEV TCP request handling
- SOCKS5 UDP ASSOCIATE behavior
- preservation of generic TCP/UDP deny rules
- WireGuard remained absent from the tested path

## 8. Characterized operational condition

LAB-002A exposed an operational dependency that was not the target of the
original experiment:

~~~text
Client IPv4 address changes
        |
        v
Source-IP-based firewall ACL
        |
        v
Address changes
        |
        v
Previously authorized identity becomes stale
        |
        v
Availability loss until ACL is updated
~~~

This is an availability characteristic of the current lab access-control
design.

The observation does not demonstrate a firewall bypass.

It also does not establish global RethinkDNS fail-open or fail-closed
behavior.

The nftables policy rejected traffic that did not match the configured
authorized source address.

## 9. Scope limitations

LAB-002A does not validate:

- WireGuard and SOCKS5 simultaneous behavior
- WireGuard transport ordering
- WireGuard egress
- WireGuard failure behavior
- global RethinkDNS fail-open behavior
- global RethinkDNS fail-closed behavior
- persistence of nftables rules after reboot
- DHCP reservation behavior
- stable device identity independent of IPv4 address
- application-layer protocol identity for observed UDP/443 traffic

No raw PCAP was produced for this recovery step.

## 10. Result

The pre-WireGuard reference state is now considered reproduced.

LAB-002 may proceed to the next phase only from the recovered baseline:

~~~text
A50
10.36.136.37
        |
        v
RethinkDNS
SOCKS5 ON
WireGuard OFF
        |
        v
HEV
10.36.136.33
TCP/1080
UDP/1081
        |
        v
Internet
~~~

# LAB-001A — Linux SOCKS5 Baseline Evidence

**Status:** PASS
**Environment:** Kali Linux VM
**HEV upstream revision:** `f09341738c2dc7613b3a9d2ad3af93b669fdbe86`
**hev-socks5-server binary SHA-256:** `5257ad617b42408926ac912c317ffdd364b7b8eaebd41189a235854bbf64f081`

## 1. Purpose

LAB-001A validates hev-socks5-server independently from Android and
RethinkDNS before exposing the proxy to the Android test environment.

The objective is to establish that the SOCKS5 component itself can:

- build reproducibly from a pinned upstream revision;
- listen only on the intended local endpoint;
- enforce username/password authentication;
- forward authenticated TCP traffic;
- create a distinct outbound connection toward the requested destination;
- shut down without leaving a listener behind.

## 2. Result Summary

| Validation | Result |
|---|---|
| Pinned upstream source | PASS |
| Recursive submodules | PASS |
| Native Linux build | PASS |
| Loopback-only listener | PASS |
| Wildcard listener absent | PASS |
| Unauthenticated request rejected | PASS |
| Authenticated SOCKS5 request | PASS |
| HTTPS positive control | PASS |
| Two-leg TCP observation | PASS |
| Controlled shutdown | PASS |
| Source-tree integrity | PASS |

## 3. Listener Observation

The configuration requested:

```text
127.0.0.1:1080
```

The Linux socket representation observed was:

```text
[::ffff:127.0.0.1]:1080
```

Two listener file descriptors were observed with `workers: 2`.

No wildcard listener on `0.0.0.0:1080` or `[::]:1080` was observed.

## 4. Authentication

An unauthenticated SOCKS5 request was rejected by curl with:

```text
curl: (97) No authentication method was acceptable.
```

The authenticated positive-control request succeeded:

```text
http=200
proxy_peer=127.0.0.1
SOCKS_RC=0
```

## 5. Positive Control

`github.com` was used as the positive-control destination because direct
DNS resolution and HTTPS connectivity were independently confirmed before
the SOCKS5 test.

Observed destination IPv4 during the test:

```text
4.237.22.38
```

This address is an observation from the test run and is not a pinned
requirement of the lab.

## 6. Two-Leg SOCKS5 Traffic Observation

The loopback packet capture showed the client connection:

```text
127.0.0.1:58392 -> 127.0.0.1:1080
```

A separate packet capture on the VM network interface showed the proxy
outbound connection:

```text
192.168.19.128:37576 -> 4.237.22.38:443
```

The HEV log independently recorded:

```text
socks5 server tcp [github.com]:443
```

Together, these observations demonstrate two distinct TCP connections:

```text
curl
  |
  | TCP connection 1
  v
hev-socks5-server :1080
  |
  | TCP connection 2
  v
github.com :443
```

## 7. Local Packet-Capture Evidence

Raw PCAP files are intentionally not committed to the public repository.

### Loopback capture

File:

```text
LAB-001A-03-loopback.pcap
```

Size:

```text
627016 bytes
```

SHA-256:

```text
6b127b08c52c7b161c4896416995eab9c769b366d6ffee7bf8eedcee62cc8f0c
```

### Outbound capture

File:

```text
LAB-001A-03-outbound.pcap
```

Size:

```text
647700 bytes
```

SHA-256:

```text
2c7caf6e7687e984a3e6ae160471411965d70bdd1fdfe8ef51f7c834ab2547e4
```

The hashes allow the local evidence used for this validation to be
identified without publishing the raw captures.

## 8. Environmental DNS Observation

During early testing, `example.com` resolved inside the VM to synthetic
addresses:

```text
0.0.0.17
::17
```

Direct DNS queries to public UDP/53 resolvers also timed out, while
`github.com` resolved normally and HTTPS connectivity succeeded.

The condition was therefore classified as an external host/network-policy
observation rather than a hev-socks5-server failure.

The Windows host uses an additional privacy/network-control stack, so the
exact origin of this synthetic DNS response remains outside the validated
scope of LAB-001A.

## 9. Scope Limitations

LAB-001A does **not** validate:

- Android routing;
- RethinkDNS SOCKS5 integration;
- UDP ASSOCIATE;
- native IPv6 Internet connectivity;
- DNS behavior through RethinkDNS;
- WireGuard chaining;
- failure-open/failure-closed behavior on Android;
- network transitions.

Those properties remain part of subsequent LAB-001 phases.

## 10. Conclusion

Within the tested Linux environment, the pinned hev-socks5-server build
successfully operated as an authenticated loopback SOCKS5 TCP proxy.

The client-to-proxy and proxy-to-destination network legs were independently
observed and recorded.

**LAB-001A result: PASS**

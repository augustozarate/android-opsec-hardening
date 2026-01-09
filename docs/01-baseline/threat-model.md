# Threat Model – Android OPSEC Hardening (Hybrid DNS + VPN)

## Scope
This threat model applies to a non-rooted Android device used daily for:
- Messaging (WhatsApp)
- Limited social media usage (view-only)
- Web browsing
- Public and private Wi-Fi networks
- Mobile data connections

The configuration focuses on **network-layer and DNS-level protections** without modifying the operating system.

## Assets to Protect
- DNS query metadata
- Application usage patterns
- Location inference via network requests
- Device fingerprinting signals
- User IP correlation across services

## Threat Actors
- Advertising and tracking networks
- App telemetry collectors
- ISP-level metadata observers
- Passive attackers on public Wi-Fi
- Over-permissioned mobile applications

## Attack Surface
- DNS resolution (unencrypted or excessive queries)
- Background application telemetry
- Push notification services
- Captive portals and public Wi-Fi networks
- Embedded third-party SDKs

## Mitigations Applied
- Encrypted DNS (DoH via NextDNS)
- Category-based blocking (ads, trackers, telemetry)
- Custom allowlist/denylist strategy
- VPN tunneling (Mullvad / IVPN / Proton VPN)
- Reduced DNS noise while preserving usability

## Out of Scope
- Malware with root or kernel access
- Physical device compromise
- Nation-state level adversaries
- Zero-day exploitation of the OS

## Security Philosophy
This project prioritizes **risk reduction and stability** over absolute isolation.
Controls are applied incrementally and validated through real usage.

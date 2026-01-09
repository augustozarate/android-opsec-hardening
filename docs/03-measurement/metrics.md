# Metrics – DNS Noise Reduction Analysis

This document summarizes observed results after applying
the hybrid DNS + VPN OPSEC model.

## Baseline (Before Hardening)
- High volume of Google telemetry domains
- Frequent location-related DNS queries
- Advertising and analytics endpoints resolved regularly
- DNS queries visible on public Wi-Fi

## After Hardening
- Encrypted DNS: 100%
- Significant reduction in telemetry-related domains
- Ads and trackers blocked at DNS level
- Essential services preserved through allowlisting

## Sample Observations (NextDNS)
- Total queries per day: ~3,000–3,500
- GAFAM distribution:
  - Google ~25%
  - Facebook / Meta ~17%
  - Microsoft ~2%
  - Other ~56%

## Frequently Blocked Domains
- `userlocation.googleapis.com`
- `doubleclick.net`
- `googleads.g.doubleclick.net`
- `incoming.telemetry.mozilla.org`
- `spot-pa.googleapis.com`

## Blocklists Used
- HaGeZi – Multi Ultimate
- OISD
- NextDNS native tracking & ads lists
- Steven Black hosts

## Trade-offs
- Slight delay on first app launch after network change
- Occasional allowlist tuning required
- Social media functionality intentionally limited

## Conclusion
The hybrid approach achieves a measurable reduction in DNS noise
while maintaining usability and system stability.

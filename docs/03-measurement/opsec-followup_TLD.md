## TLD-Level Blocking Strategy

### Globally blocked TLDs
.xyz, .top, .gq, .ml, .cf, .tk

Rationale:
High abuse rate, negligible legitimate usage in mobile ecosystems.

### Profile-based blocked TLDs (Public Wi-Fi)
.click, .link, .review

Rationale:
Mixed-use TLDs, blocked only in high-risk network environments.

### Excluded TLDs
.download, .loan

Rationale:
Documented breakage and legitimate service impact.

## TLD Phantom Detection

TLDs not explicitly used by the user but appearing in DNS logs
are treated as potential telemetry or probing signals.

Observed indicators:
- Low-frequency random domains
- Background-only resolution
- Non-interactive traffic

Actions:
- Monitor before blocking
- Correlate with app installs
- Escalate to TLD-level blocking only if recurrent


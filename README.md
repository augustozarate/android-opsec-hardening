# Android OPSEC Hardening

**Repository:** `android-opsec-hardening`  
**Purpose:** Practical Android security hardening with real-world case studies, DNS filtering (NextDNS), and privacy-focused VPN integration  
**Focus:** Privacy-first configurations, rootless approaches, threat model analysis, and hybrid OPSEC strategy  

---

## Overview

This repository documents **hands-on Android security hardening** experiments and **real-world case studies**. Each guide represents actual device testing, focusing on **practical privacy improvements** without requiring root access or complex modifications.

The core philosophy combines:
- **DNS-level filtering (NextDNS)** for passive threat defense
- **Privacy-respecting VPN usage** (Mullvad, IVPN, Proton VPN)
- **Selective hardening** (balance privacy with usability)
- **Documented lessons learned** (both successes and failures)

### Core Philosophy

- ✅ **Documented & Tested** — Every guide reflects actual device testing (2+ weeks minimum)
- ✅ **Hybrid OPSEC Model** — DNS filtering + VPN without breaking app functionality
- ✅ **Realistic Threat Models** — Focused on common privacy concerns, not theoretical attacks
- ✅ **Rootless-First** — Prioritize OS-level controls over kernel-level modifications
- ✅ **Reproducible** — Step-by-step guides for others to follow
- ✅ **Ethical & Transparent** — No circumvention, no platform abuse, just privacy

---

## 🎯 Objectives

- Reduce unnecessary DNS queries and background telemetry
- Limit exposure to advertising, analytics, and tracking networks
- Preserve core Android functionality and app usability
- Maintain compatibility with privacy-focused VPN usage
- Apply OPSEC principles **without degrading daily user experience**

---

## 📁 Project Structure

```
android-opsec-hardening/
├── .gitignore
├── LICENSE
├── README.md                          # This file
├── CHANGELOG.md
│
├── devices/                           # Device-specific case studies
│   └── samsung-a50-a505g/
│       ├── README.md                  # Full A50 hardening guide
│       ├── troubleshooting.md         # Known issues & solutions
│       └── configs/
│           ├── nextdns-setup.txt
│           └── shelter-apps-list.txt
│
├── opsec/                             # OPSEC automation & analysis
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── baseline/                      # DNS baseline & threat analysis
│   ├── case-studies/                  # Real-world threat findings
│   │   └── assets/
│   ├── scripts/                       # Analysis & maintenance tools
│   │   ├── analysis/
│   │   ├── investigation/
│   │   ├── maintenance/
│   │   └── workflows/
│   └── data/                          # (git tracked, data ignored)
│
├── docs/                              # General documentation
│   ├── guides/
│   └── references/
│
├── nextdns/                           # NextDNS blocklists & allowlists
│   ├── blocklists/                    # Google, Meta, Samsung trackers
│   └── allowlists/                    # Functional endpoints
│
├── logs/                              # (git tracked, logs ignored)
└── screenshots/
```

---

## 🔍 Threat Model & Scope

### In Scope
- Passive network observers (ISPs, networks)
- DNS-level tracking and analytics
- Telemetry-heavy mobile applications
- Advertising and tracking networks
- Risks associated with public Wi-Fi usage
- Google/Meta/OEM telemetry collection

### Out of Scope
- Device compromise or malware analysis
- Root-level, firmware, or baseband attacks
- Exploitation, bypass, or evasion techniques
- Nation-state adversaries
- Physical device access

**This project focuses on defensive hardening, not adversarial activity.**

---

## 🔀 Hybrid OPSEC Model

Rather than blocking entire platforms or ecosystems, this project follows a **selective hybrid strategy**:

- ✅ Allow core APIs, CDNs, and functional endpoints
- ✅ Selectively block telemetry, analytics, and advertising domains
- ✅ Validate application behavior after each configuration change
- ✅ Iterate based on **measurable DNS metrics**, not assumptions
- ✅ Preserve usability while reducing tracking exposure

**Privacy and usability must coexist.**

---

## Quick Start

### For Users

Pick a device matching yours:

- **[Samsung Galaxy A50 (SM-A505G)](./devices/samsung-a50-a505g/)** 
  - Android 12.1 (crDroid 9.5)
  - GrapheneOS-like privacy stack
  - App sandboxing via Shelter
  - Hybrid DNS + VPN configuration
  - Status: ✅ Stable & Daily-Use Tested (2+ weeks)

### For Developers/Researchers

Review the [Architecture](#architecture) section and [Contributing](#contributing) guidelines to add additional device cases.

---

## Architecture

### Device Case Studies

Each device subdirectory follows this template:

```
devices/[manufacturer]-[model]-[variant]/
├── README.md                    # Complete setup guide
├── troubleshooting.md           # Known issues & solutions
├── lessons-learned.md           # What worked/failed & why
├── performance-metrics.md       # Real-world performance data
└── configs/
    ├── nextdns-setup.txt
    ├── shelter-sandbox-apps.txt
    ├── permissions-hardening.md
    └── firewall-rules.md (if applicable)
```

### OPSEC Automation & Analysis

Scripts and tools under `opsec/`:

```
opsec/scripts/
├── analysis/                    # DNS review, threat analysis
├── investigation/               # Domain investigation tools
├── maintenance/                 # Updater & cleanup tools
└── workflows/                   # Integrated OPSEC workflows
```

---
### OPSEC Case Studies

Real-world findings produced by applying this repo's investigation tooling (`opsec/scripts/investigation/`) and detection methodology to threats encountered in the wild — not simulated scenarios.
```
opsec/case-studies/
├── README.md
└── YYYY-MM-short-description.md
```
Each entry cross-verifies detection across multiple sources (VirusTotal, sandbox history, vendor tools) and documents the responsible disclosure process when a vendor is contacted. See [`opsec/case-studies/`](./opsec/case-studies/).
---

## Case Studies

This project maintains two kinds of case studies: **device hardening guides** (below) and **OPSEC investigation findings** ([`opsec/case-studies/`](./opsec/case-studies/)) — real threats analyzed using this repo's own methodology.

### Samsung Galaxy A50 (SM-A505G)

**Status:** ✅ Active, Daily Use  
**Android Version:** 12.1 (crDroid 9.5)  
**Duration Tested:** 2+ weeks (ongoing)  
**Bootloader:** Unlocked, Knox Fused  
**Root:** None (intentional)

**Key Achievements:**
- Removed all Google Services (microG replacement)
- App sandboxing via Shelter work profiles
- DNS filtering (NextDNS) + VPN (Mullvad always-on)
- Stable WiFi after comprehensive kernel troubleshooting
- No root required — OS-level controls sufficient

**Why No Root?**
- Magisk incompatible with A50 ramdisk architecture
- KernelSU requires GKI kernels (device uses custom Bocchi kernel)
- Root installation caused bootloop on multiple kernel attempts
- OS-level controls (work profiles, permissions) sufficient for privacy goals
- Rootless = more stable long-term

**Key Lesson:** Root isn't always necessary for privacy. Deliberate OS-level controls + DNS filtering + VPN can achieve comparable privacy without stability risks.

**[Read Full Guide →](./devices/samsung-a50-a505g/README.md)**

---

### Detection False Negative: Compromised Contabo VPS Serving Phishing

**Status:** 🟡 Pending vendor response
**Type:** Threat investigation (not device hardening)

A phishing email was cross-verified across VirusTotal, ANY.RUN sandbox history, and a VPN vendor's URL reputation tool — revealing a detection gap where the vendor's own checker classified a known-bad URL as clean. Documents the full OSINT correlation process and responsible disclosure to the vendor.

**[Read Full Case Study →](./opsec/case-studies/2026-08-phishing-contabo-roundcube.md)**

---

## 🔐 Privacy Stack Components

### Application Level
- **F-Droid** — FOSS app store (no Google Play required)
- **microG** — Lightweight Google Services replacement
- **Shelter** — App sandboxing via work profiles
- **Mullvad VPN** — Always-on, no-logs VPN (configurable)

### Network Level
- **NextDNS** — DNS-level ad/tracker blocking
- **DNS-over-HTTPS** — Encrypted DNS queries
- **VPN Integration** — Privacy-respecting providers (Mullvad, IVPN, Proton)
- **Split-tunneling** (optional, context-dependent)

### System Level
- **Permission Hardening** — Granular per-app controls
- **Telemetry Disabling** — Samsung/Google/OEM tracking removal
- **SELinux** — Mandatory Access Control (system-wide)

### Hardware Level
- **Verified Boot** — Bootloader & system partition integrity
- **Bootloader Status** — Security implications documented

---

## VPN Considerations

The project is **VPN-agnostic** but designed and tested with privacy-respecting providers:

- **Mullvad** (recommended for A50 guide)
- **IVPN**
- **Proton VPN**

### Key Principles
- No traffic inspection
- No user tracking
- No logging policies
- Proper DNS handling with custom resolvers
- VPN usage for **privacy and security only**, not circumvention

---

## Contributing

### Adding Your Device

1. Create folder: `devices/[manufacturer]-[model]-[variant]/`
2. Use template from existing guide (A50)
3. **Test on actual hardware (minimum 2-4 weeks daily use)**
4. Document failures, not just successes
5. Submit PR with device specs in commit message

### Submission Checklist

- [ ] Device model & variant (e.g., SM-A505G)
- [ ] Android version & ROM used
- [ ] Installation steps (bootloader unlock → final setup)
- [ ] Privacy stack components tested
- [ ] Performance impact measured
- [ ] Troubleshooting section completed
- [ ] Lessons learned documented
- [ ] Real-world usage duration (minimum 2 weeks)

### Commit Message Template

```
docs: add [device] [rom] [android-version] hardening guide

- Device: Samsung Galaxy A50 (SM-A505G)
- ROM: crDroid 9.5
- Android: 12.1
- Duration tested: 2+ weeks daily use
- Key achievement: X privacy goal achieved without root
- Hybrid OPSEC: NextDNS + Mullvad VPN
```

---

## Security Considerations

### What This Protects Against
- ✅ ISP/network-level tracking (VPN)
- ✅ Google/Meta/Samsung tracking (F-Droid + microG + DNS blocking)
- ✅ App data leaks (Shelter sandboxing)
- ✅ DNS leaks (NextDNS + VPN)
- ✅ Telemetry & analytics collection
- ✅ Public Wi-Fi eavesdropping (VPN)

### What This Does NOT Protect Against
- ❌ Nation-state adversaries
- ❌ Physical device access or theft
- ❌ Supply-chain compromises
- ❌ Zero-day exploits
- ❌ Compromised apps (even in sandbox)
- ❌ Malware or device compromise

### Limitations

- No kernel-level hardening (requires custom kernel with GKI)
- No exploit prevention beyond standard SELinux
- Bootloader unlock reduces security baseline (Knox fused)
- microG cannot replace all Play Services features
- DNS filtering is not encryption (use with VPN)

### Best Practices

1. **Shelter untrusted apps** — Use work profiles for questionable apps
2. **Enable VPN always-on** — Prevent traffic leaks if VPN disconnects
3. **Review permissions** — Even F-Droid apps should be permission-audited
4. **Update regularly** — crDroid/LineageOS security patches critical
5. **Backup data** — Before flashing ROMs or kernels
6. **Monitor DNS queries** — Use NextDNS dashboard to validate filtering

---

## Performance Baseline

### Typical Metrics (A50 + crDroid 9.5 + NextDNS + Mullvad)

| Metric | Value | Notes |
|---|---|---|
| Boot Time | 25-30s | Normal for custom ROM |
| App Launch | Baseline | No overhead from hardening |
| Battery Life | 1.5 days | Heavy use + VPN always-on |
| RAM Usage | 2.8GB / 4GB | Shelter adds ~50MB per sandboxed app |
| Storage Impact | ~2GB | microG + F-Droid + apps |
| VPN Overhead | <5% | Negligible for browsing |
| DNS Query Reduction | 70%+ | With NextDNS filtering |

---

## 🧠 Lessons Learned

### What Worked
- ✅ **crDroid 9.5** — 100% stable, optimized AOSP
- ✅ **Shelter for isolation** — Works without root via work profiles
- ✅ **F-Droid + microG** — Zero Google dependencies, minimal friction
- ✅ **Rootless approach** — Avoids bootloop risks, long-term stability
- ✅ **NextDNS + VPN** — Effective hybrid model with usability intact

### What Didn't Work
- ❌ **Magisk on A50** — Incompatible ramdisk architecture
- ❌ **KernelSU with Bocchi kernel** — Requires GKI, got "Not supported" error
- ❌ **Mint kernels with Android 13** — WiFi driver crash loops on A505G
- ❌ **LineageOS 20** — Bootloader/kernel compatibility issues on this device

### Key Insight
**Stability over features.** A proven, stable setup (Android 12 + Bocchi kernel + crDroid) is worth more than newer versions (Android 13+) that introduce instability. Privacy achieved through **reliability**, not bleeding-edge technology.

---

## 📊 Metrics & Validation

Effectiveness is evaluated using:

- DNS query volume comparison (before / after configuration)
- Reduction of telemetry-heavy domains (NextDNS logs)
- Functional testing of apps and system services
- Stability when combining DNS filtering and VPN usage
- Battery life and performance impact measurement

**No personal data, identifiers, or raw logs are included in this repository.**

---

## References & Resources

### Official Projects
- **F-Droid:** https://f-droid.org
- **microG:** https://microg.org
- **Shelter:** https://typeblog.net/shelter/
- **Mullvad VPN:** https://mullvad.net
- **NextDNS:** https://nextdns.io
- **crDroid:** https://crdroid.net

### Privacy & Security Research
- **GrapheneOS Security Model:** https://grapheneos.org/features
- **Android Hardening Documentation:** https://source.android.com/docs/security
- **EFF Privacy Guide:** https://ssd.eff.org

### Technical Documentation
- **Android Verified Boot:** https://source.android.com/docs/security/verifiedboot
- **SELinux on Android:** https://source.android.com/docs/security/selinux
- **DNS Security (RFC 8310):** DNS over HTTPS standards

---

## FAQ

### Q: Why not use GrapheneOS?
**A:** GrapheneOS doesn't support older devices like the A50. This project documents how to achieve **comparable privacy goals** on unsupported hardware using FOSS alternatives.

### Q: Is root required?
**A:** No. Rootless approach is intentional — OS-level controls (work profiles, permissions) are sufficient for privacy. Root adds complexity and stability risks on older devices.

### Q: What if my device isn't listed?
**A:** Contribute a case study! Follow the [Contributing](#contributing) guidelines. Test on actual hardware for 2+ weeks and document both successes and failures.

### Q: Does this replace antivirus?
**A:** No. These are privacy hardening guides, not malware protection. Assume app-level malware is possible; use Shelter to sandbox untrusted apps.

### Q: Can I contribute improvements?
**A:** Yes! Submit PRs with:
- Real-world testing results (2+ weeks minimum)
- Device specs & ROM version
- Documented failures (learning experiences)
- Performance metrics

---

## ⚖️ Ethical & Legal Notice

This project is **strictly defensive and educational**.

It does **NOT** promote:
- Circumvention of laws or regulations
- Bypassing device or platform safeguards
- Abuse of services or targeting of organizations

All configurations are **documented, reversible, and intended for learning and personal hardening** purposes.

**Users are responsible for** complying with local laws, service terms, and ethical standards.

---

## License

This repository is provided for **educational and research purposes**. Use at your own risk.

- ROM installation voids warranty
- Bootloader unlock can brick devices
- Privacy is not guaranteed; these measures reduce (not eliminate) tracking

See [LICENSE](./LICENSE) file for details.

---

## Status & Maintenance

### Device Guides

| Device | ROM | Android | Status | Last Tested |
|---|---|---|---|---|
| Samsung A50 (SM-A505G) | crDroid 9.5 | 12.1 | ✅ Stable | June 2026 |
| (More devices coming) | — | — | 🚧 Planned | — |

### OPSEC Case Studies

| Case Study | Type | Status | Last Updated |
|---|---|---|---|
| [Contabo/Roundcube Phishing — Detection False Negative](./opsec/case-studies/2026-08-phishing-contabo-roundcube.md) | Threat investigation | 🟡 Pending vendor response | August 2026 |

---

## Contact & Support

- **Issues:** Open GitHub issue with device model & problem description
- **Contributions:** Fork → test → submit PR
- **Questions:** Include device specs, ROM version, and reproduction steps

---

**Last Updated:** August 2026  
**Maintainer:** [@augustozarate](https://github.com/augustozarate)  
**Portfolio:** [Cybersecurity & Privacy Engineering](https://github.com/augustozarate)

⭐ If you find this project useful, please give it a star on GitHub!

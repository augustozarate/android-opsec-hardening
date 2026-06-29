# Android OPSEC Hardening

**Repository:** `android-opsec-hardening`  
**Purpose:** Practical security hardening guides for Android devices with real-world testing and documentation  
**Focus:** Privacy-first configurations, rootless approaches, and threat model analysis  

---

## Overview

This repository documents hands-on Android security hardening experiments and case studies. Each guide represents real-world testing on specific devices, focusing on **practical privacy improvements** without requiring root access or complex modifications.

### Core Philosophy

- ✅ **Documented & Tested** — Every guide reflects actual device testing
- ✅ **Realistic Threat Models** — Focused on common privacy concerns, not theoretical attacks
- ✅ **Rootless-First** — Prioritize OS-level controls over kernel-level modifications
- ✅ **Reproducible** — Step-by-step guides for others to follow
- ✅ **Lessons Learned** — Document failures and why they occurred

---

## Quick Start

### For Users

Pick a device matching yours:

- **[Samsung Galaxy A50 (SM-A505G)](./devices/samsung-a50-a505g/)** 
  - Android 12.1 (crDroid 9.5)
  - GrapheneOS-like privacy stack
  - App sandboxing via Shelter
  - Status: ✅ Stable & Daily-Use Tested

### For Developers/Researchers

Review the [Architecture](#architecture) section and contribute additional device guides.

---

## Architecture

### Devices Directory

Each device has its own subdirectory with:

```
devices/[manufacturer]-[model]-[variant]/
├── README.md                    # Main setup guide
├── setup-guide.md               # Step-by-step installation
├── troubleshooting.md           # Common issues & solutions
├── lessons-learned.md           # What worked/failed & why
├── performance-metrics.md       # Real-world performance data
└── configs/
    ├── nextdns-setup.txt
    ├── shelter-sandbox-apps.txt
    ├── permissions-hardening.md
    └── firewall-rules.md (if applicable)
```

### Tools Directory (Optional)

Scripts and utilities for automation:

```
tools/
├── install-fdroid.sh            # F-Droid installation automation
├── apply-hardening.sh           # Batch permission hardening
└── device-fingerprint.sh        # Privacy audit tool
```

### Documentation Standards

- **README.md** — Main guide (installation → hardening → verification)
- **Troubleshooting.md** — Error solutions, device-specific quirks
- **Lessons Learned.md** — What failed, root causes, workarounds
- **Configs/** — Copy-paste friendly configuration files

---

## Case Studies

### Samsung Galaxy A50 (SM-A505G)

**Status:** ✅ Active, Daily Use  
**Android Version:** 12.1 (crDroid 9.5)  
**Bootloader:** Unlocked, Knox Fused  
**Root:** None (intentional — see below)

**Key Achievements:**
- Removed all Google Services (microG replacement)
- App sandboxing via Shelter work profiles
- DNS filtering (NextDNS) + VPN (Mullvad)
- Stable WiFi after kernel troubleshooting
- No root required

**Why No Root?**
- Magisk incompatible with A50 ramdisk architecture
- KernelSU requires GKI kernels (device uses custom Bocchi kernel)
- Root installation caused bootloop on multiple kernel attempts
- OS-level controls (work profiles, permissions) sufficient for privacy goals

**Read Full Guide:** [devices/samsung-a50-a505g/README.md](./devices/samsung-a50-a505g/)

---

## Privacy Stack Components

Each guide typically implements:

### Application Level
- **F-Droid** — FOSS app store (no Google Play required)
- **microG** — Lightweight Google Services replacement
- **Shelter** — App sandboxing via work profiles
- **Mullvad VPN** — Always-on, no-logs VPN

### Network Level
- **NextDNS** — DNS-level ad/tracker blocking
- **DNS-over-HTTPS** — Encrypted DNS queries
- **VPN Split-tunneling** (if configured)

### System Level
- **Permission Hardening** — Granular per-app controls
- **Telemetry Disabling** — Samsung/OEM tracking removal
- **Bootloader Lock Status** — Security implications documented

### Hardware Level
- **SELinux** — Mandatory Access Control (system-wide)
- **Verified Boot** — Bootloader & system partition integrity

---

## Contributing

### Adding Your Device

1. Create folder: `devices/[manufacturer]-[model]-[variant]/`
2. Use template from existing guide (A50)
3. Test on actual hardware (minimum 2-4 weeks daily use)
4. Document failures, not just successes
5. Submit PR with device specs in commit message

### Submission Checklist

- [ ] Device model & variant (e.g., SM-A505G)
- [ ] Android version & ROM
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
```

---

## Security Considerations

### Threat Model

These guides assume you're protecting against:
- ✅ ISP/network-level tracking (VPN)
- ✅ Google tracking (F-Droid + microG)
- ✅ App data leaks (Shelter sandboxing)
- ✅ DNS leaks (NextDNS)
- ✅ Telemetry (OEM/Samsung removal)

These guides do **NOT** protect against:
- ❌ Nation-state adversaries
- ❌ Physical device access
- ❌ Supply-chain compromises
- ❌ Zero-day exploits
- ❌ Compromised apps (use Shelter for untrusted apps)

### Limitations

- No kernel-level hardening (requires custom kernel)
- No exploit prevention beyond standard SELinux
- Bootloader unlock reduces security (Knox fused)
- microG cannot replace all Play Services features

### Best Practices

1. **Shelter untrusted apps** — Use work profiles for questionable apps
2. **Enable VPN always-on** — Prevent traffic leaks if VPN disconnects
3. **Review permissions** — Even F-Droid apps should be permission-audited
4. **Update regularly** — crDroid/LineageOS security patches
5. **Backup data** — Before flashing ROMs or kernels

---

## Performance Baseline

### Typical Metrics (A50 + crDroid 9.5)

| Metric | Value | Notes |
|---|---|---|
| Boot Time | 25-30s | Normal for custom ROM |
| App Launch | Baseline | No overhead from hardening |
| Battery Life | 1.5 days | Heavy use + VPN always-on |
| RAM Usage | 2.8GB / 4GB | Shelter adds ~50MB per sandboxed app |
| Storage Impact | ~2GB | microG + F-Droid + apps |
| VPN Overhead | <5% | Negligible for browsing |

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
- **Android Hardening by @MalibuSecurity:** Kernel-level approaches
- **EFF Privacy Guide:** https://ssd.eff.org

### Technical Documentation
- **Android Verified Boot:** https://source.android.com/docs/security/verifiedboot
- **SELinux on Android:** https://source.android.com/docs/security/selinux
- **Exynos 9610 Kernel:** Custom ROM development resources

---

## Frequently Asked Questions

### Q: Why not use GrapheneOS?
**A:** GrapheneOS doesn't support older devices like the A50. This project documents how to achieve similar privacy goals on unsupported hardware.

### Q: Is root required?
**A:** No. Rootless approach is intentional — OS-level controls (work profiles, permissions) are sufficient for privacy. Root adds complexity and stability risks on older devices.

### Q: Can I add this to my device?
**A:** If your device has an existing custom ROM guide, yes. Test thoroughly for 2+ weeks. Document failures, not just successes.

### Q: Does this replace antivirus?
**A:** No. These are privacy hardening guides, not security hardening. Assume app-level malware is possible; use Shelter to sandbox untrusted apps.

### Q: Can I contribute improvements?
**A:** Yes! Submit PRs with:
- Real-world testing results
- Device specs & ROM version
- Documented failures (learning experiences)
- Performance metrics

---

## License

This repository is provided for **educational and research purposes**. Use at your own risk.

- ROM installation voids warranty
- Bootloader unlock can brick devices
- Privacy is not guaranteed; these measures reduce (not eliminate) tracking

---

## Status & Maintenance

| Device | ROM | Android | Status | Last Tested |
|---|---|---|---|---|
| Samsung A50 (SM-A505G) | crDroid 9.5 | 12.1 | ✅ Stable | June 2026 |
| (More devices coming) | — | — | 🚧 Planned | — |

---

## Contact & Support

- **Issues:** Open GitHub issue with device model & problem description
- **Contributions:** Fork → test → submit PR
- **Questions:** Include device specs, ROM version, and reproduction steps

---

**Last Updated:** June 2026  
**Maintainer:** [@augustozarate](https://github.com/augustozarate)  
**Portfolio:** [Cybersecurity & Privacy Engineering](/)

# Samsung Galaxy A50 (SM-A505G) — crDroid 9.5 Privacy Hardening Guide

**Status:** ✅ Tested & Stable  
**Device:** Samsung Galaxy A50 (SM-A505G)  
**ROM:** crDroid 9.5 (AOSP-based)  
**Kernel:** Bocchi Kernel 4.14.142  
**Android Version:** 12.1  
**Last Updated:** June 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Installation Process](#installation-process)
3. [Privacy Hardening Stack](#privacy-hardening-stack)
4. [Sandbox Configuration (Shelter)](#sandbox-configuration-shelter)
5. [DNS & VPN Setup](#dns--vpn-setup)
6. [Permission Hardening](#permission-hardening)
7. [Lessons Learned](#lessons-learned)
8. [References & Resources](#references--resources)

---

## Overview

This guide documents a **complete privacy-focused setup** for the Samsung Galaxy A50 (SM-A505G), achieving GrapheneOS-like privacy protections without changing the ROM or requiring root access.

### Key Achievements

- ✅ **Zero Google Services** — replaced with microG
- ✅ **App Sandboxing** — via Shelter (work profile isolation)
- ✅ **WiFi Stability** — resolved after multiple kernel testing iterations
- ✅ **DNS Filtering** — NextDNS over HTTPS
- ✅ **VPN Integration** — Mullvad always-on
- ✅ **No Root Required** — avoiding bootloop risks on this device

### Why No Root?

After extensive testing with:
- **Magisk v30.7** — incompatible with A50 ramdisk architecture
- **KernelSU v12132** — requires GKI kernels; Bocchi kernel is not GKI
- **Multiple Mint kernels** — all caused WiFi crashes (driver incompatibility)

**Conclusion:** Rootless setup is more stable on this hardware.

---

## Installation Process

### Prerequisites

- **PC:** Windows with ADB/Fastboot installed
- **Phone:** SM-A505G with bootloader unlockable
- **Recovery:** TWRP for A50 (with vbmeta included)

### Step 1: Unlock Bootloader

```
# Enter Download Mode: Vol Down + Vol Up + Connect USB
# In Odin, slot AP = vbmeta.img
# One-way operation: Knox flag is burned
```

**⚠️ Warning:** This erases all data and voids warranty.

### Step 2: Install TWRP Recovery

**TWRP Version:** 3.7.0 (A505F/A505G compatible)  
**Source:** GiovanYCringe fork (includes vbmeta)  
**Method:** Odin flasher via Download Mode

```
# Odin settings:
# - Slot AP: twrp.tar (from GiovanYCringe releases)
# - Auto Reboot: UNCHECKED
# - Click Start
```

After flash, boot into TWRP: `Power + Vol Up` (while USB connected)

### Step 3: Install ROM & Kernel

**ROM:** crDroid 9.5 (by GiovaniYCringe)  
**Link:** Available on XDA Forums (A505F/A505FN unofficial builds)

```
# From TWRP:
1. Wipe → Advanced Wipe (System + Data + Cache + Dalvik)
2. Install → crDroid-9.5-*.zip
3. Wipe → Cache/Dalvik
4. Reboot → System
```

**Boot Time:** First boot takes 3-6 minutes (normal)

### Step 4: Initial Setup

```
# In Android Setup Wizard:
1. Skip Google account (or use dummy account)
2. Enable Developer Options: Settings → About → Tap "Build Number" 7x
3. Enable USB Debugging
4. Skip Play Store setup
```

---

## Privacy Hardening Stack

### 1. Remove Google Services

**Method:** Settings → Apps → Show system apps → Disable:
- Google Play Services
- Play Store
- Google Play Framework
- Google Analytics
- Google Play Protect

### 2. Install F-Droid (App Store)

**F-Droid:** Open-source app store, no Google dependencies

```
# Download & Install
wget https://f-droid.org/F-Droid.apk
adb install F-Droid.apk
```

**From F-Droid, install core privacy apps:**

| App | Function | Package |
|---|---|---|
| **Shelter** | App sandbox (work profile) | net.typeblog.shelter |
| **Mullvad VPN** | Always-on VPN | net.mullvad.mullvadvpn |
| **Rethink** | DNS filtering + tracker blocking | com.celzero.bravedns |
| **Fennec** | Hardened Firefox | org.mozilla.fennec_fdroid |
| **Organic Maps** | Privacy maps (no Google) | app.organicmaps |
| **Heliboard** | Privacy keyboard | helium314.keyboard |
| **Simple Gallery Pro** | Offline gallery | com.simplemobiletools.gallery.pro |

### 3. Install microG via TWRP (Recommended)

**Why TWRP?** More reliable than side-loading; microG is not available in F-Droid directly.

**Method:**

1. Download microG ZIP from official GitHub releases:
   ```
   https://github.com/microg/GmsCore/releases
   ```
   Look for: `MicroG-release-*.zip` (arm64 variant)

2. Copy to phone:
   ```
   adb push MicroG-*.zip /sdcard/
   ```

3. From TWRP:
   ```
   Install → MicroG-*.zip
   Wipe → Cache/Dalvik
   Reboot → System
   ```

4. Configure microG:
   ```
   Settings → Apps → microG Services Core → Permissions
   # Grant selectively: Location, Contacts, Phone (only if needed)
   ```

**Note:** Some apps may require Play Services. microG provides lightweight compatibility without Google tracking.

---

## Sandbox Configuration (Shelter)

### Why Shelter?

Shelter creates a **work profile** that acts as a sandbox:
- Apps in sandbox cannot access personal data (contacts, photos)
- Separate login/data for each app instance
- Full app functionality (network access, etc.) preserved
- Closest approximation to GrapheneOS sandboxing without kernel changes

### Setup Process

#### 1. Install & Create Work Profile

```
F-Droid → Install "Shelter"
Shelter app → "Create Work Profile"
# Permit all requested permissions
```

#### 2. Clone Apps to Sandbox

For **untrusted or data-hungry apps:**

```
Shelter → Long-press app → "Clone to Shelter (work profile)"
# App now appears twice in app drawer
```

#### 3. Remove Original (Optional)

```
Settings → Apps → Uninstall (original version)
# Keep only sandboxed version
```

### Recommended Apps for Sandboxing

- **Streaming services** (especially from social invites)
- **Social media** (if not deleted entirely)
- **China-based apps** (TikTok, Alipay, etc.)
- **Apps with excessive permissions**
- **Beta/testing apps**

### Data Isolation Verification

```
Shelter → Package list
# Work profile apps are marked and isolated
# Each has separate /data/data/com.app.package directory
```

---

## DNS & VPN Setup

### NextDNS (DNS over HTTPS)

**Setup:**

```
Settings → Network → Private DNS
# Set to: dns.nextdns.io
# OR: [YOUR_PROFILE_ID].dns.nextdns.io
```

**Benefits:**
- DNS queries encrypted (no ISP tracking)
- Ad/tracker blocking at DNS level
- No app permission needed

### Mullvad VPN (Always-On)

**F-Droid:** Install `net.mullvad.mullvadvpn`

**Configuration:**

```
Mullvad → Settings → Always-on VPN: ENABLED
Mullvad → Settings → Block when disconnected: ENABLED
```

**Result:**
- All traffic routed through Mullvad
- Automatic blocking if VPN disconnects
- IP spoofing + ISP anonymity

---

## Permission Hardening

### Disable Location Tracking

```
Settings → Privacy → Location
# Disable "Location" entirely
# OR: Set to "GPS only" (no network-based location)
```

### Camera & Microphone Controls

```
Settings → Apps → Permissions
# For each app: Camera → Deny or "Allow only while using"
# For each app: Microphone → Deny or "Allow only while using"
```

### Samsung-Specific Telemetry

```
Settings → Samsung Members → Disable "Help improve"
Settings → Samsung Account → Disable "Personalised services"
Bixby → Voice → DISABLE
```

### Contact & Calendar Sync

```
Settings → Accounts
# Remove Samsung Cloud sync (optional)
# Keep local AOSP sync for Contacts/Calendar
```

---

## Lessons Learned

### ❌ What Didn't Work

#### 1. **Magisk on A50**
- **Issue:** A50 ramdisk lacks boot partition compatibility
- **Error:** Attempted to patch non-existent partitions, caused bootloop
- **Lesson:** Not all devices support Magisk despite being rootable

#### 2. **KernelSU with Non-GKI Kernels**
- **Issue:** KernelSU only works with Generic Kernel Image (GKI) kernels
- **Bocchi Kernel:** Custom device kernel, not GKI
- **Error:** App showed "Not supported" despite KernelSU driver present
- **Lesson:** Check kernel type before assuming root compatibility

#### 3. **Mint Kernels with Android 13 + A505G**
- **Issue:** WiFi driver crash loop (`CMD_RECOVERY_DISABLE_WIFI`)
- **Tested versions:** 1400, 1401, 1413 — all had same WiFi collapse
- **Root cause:** Driver incompatibility between Mint's wireless module and Android 13 on Exynos 9610
- **Lesson:** Sometimes older, proven kernels (Bocchi) are more stable than newer ones

#### 4. **LineageOS 20 on A505G**
- **Issue:** Bootloader incompatibility + WiFi driver crashes
- **Error:** Download Mode loop on direct system reboots
- **Lesson:** Not all unofficial ROMs have device-specific fixes for model variants

### ✅ What Worked

#### 1. **crDroid 9.5 (Android 12.1)**
- **Stability:** 100% stable since installation
- **WiFi:** Works perfectly with Bocchi kernel
- **Performance:** Optimized AOSP + customization without bloat
- **Lesson:** A10 ROM can be just as secure as A13+, especially when stable

#### 2. **Shelter for App Isolation**
- **Works without root:** True sandbox via work profile
- **Overhead:** Minimal (just separate app instance)
- **Security:** Prevents data exfiltration from untrusted apps
- **Lesson:** Sandboxing at OS level (work profiles) can substitute for kernel-level isolation

#### 3. **F-Droid + microG Ecosystem**
- **Privacy:** Zero Google Services in default setup
- **Compatibility:** microG provides Play Services fallback when needed
- **Community:** Large ecosystem of privacy-focused apps
- **Lesson:** FOSS alternatives exist for most functions, with minimal friction

#### 4. **Rootless Approach**
- **Risk reduction:** No bootloop potential from root installation
- **Sufficient functionality:** All privacy goals achieved without root
- **Stability:** Long-term reliability without root-related conflicts
- **Lesson:** Root isn't always necessary for privacy; OS-level controls can suffice

---

## Performance Metrics

| Metric | Result |
|---|---|
| **Boot Time** | ~25-30 seconds |
| **App Launch** | Normal (no noticeable overhead) |
| **Battery Life** | 1.5 days typical use |
| **RAM Usage** | ~2.8 GB used / 4 GB available |
| **Storage Free** | ~32 GB / 64 GB |
| **WiFi Stability** | Excellent (no disconnects) |
| **VPN Overhead** | Minimal (<5% speed impact) |

---

## References & Resources

### Official Sources
- **crDroid:** XDA Forums (A50 unofficial builds)
- **F-Droid:** https://f-droid.org
- **microG:** https://microg.org
- **Shelter:** https://typeblog.net/shelter/
- **Mullvad VPN:** https://mullvad.net
- **NextDNS:** https://nextdns.io

### Technical References
- **Android Verified Boot (AVB):** vbmeta partition security
- **GrapheneOS Privacy Model:** Reference architecture
- **TWRP for A50:** GiovanYCringe fork (vbmeta-integrated)
- **Linux kernel 4.14:** Exynos 9610 kernel sources

### Devices Tested
- **SM-A505F:** European variant (compatible)
- **SM-A505FN:** Global variant (compatible)
- **SM-A505G:** Latin America variant (this build)

---

## Future Improvements

- [ ] Explore hardened kernel options (if stable WiFi-compatible kernel released)
- [ ] Document Lsposed module compatibility for app-level hooks
- [ ] Test GSI (Generic System Image) builds if Android 14+ becomes stable
- [ ] Evaluate Waydroid for isolated Linux container apps

---

## Support & Issues

### Common Issues

**Q: WiFi keeps disconnecting after ROM flash?**  
A: Ensure you're using Bocchi kernel (included in crDroid). Mint kernels have driver bugs on this device.

**Q: Magisk won't install or causes bootloop?**  
A: A50 doesn't support Magisk due to ramdisk architecture. Use KernelSU (if kernel is GKI) or skip root entirely.

**Q: microG apps say "Google Play Services not installed"?**  
A: Install microG from F-Droid and grant Location permission in app settings.

**Q: Shelter cloned apps won't sync with main profile?**  
A: By design. Work profile apps are isolated. Use cloud sync (Nextcloud, etc.) if needed.

### Reporting

Found issues with this setup? Document:
- Device model (SM-A505G, SM-A505F, etc.)
- ROM version
- Kernel version (`cat /proc/version` via ADB)
- Reproduction steps

---

## License & Attribution

This guide documents real-world testing and hardening of the Samsung Galaxy A50. 

**Thanks to:**
- GiovaniYCringe (crDroid & kernel development)
- GrapheneOS team (privacy model reference)
- F-Droid community (app curation)

**Last Tested:** June 2026  
**Device Ownership:** Active daily use

---

## Disclaimer

- Custom ROM installation voids warranty and can brick device if done incorrectly
- This guide reflects stable, tested configurations; results may vary by device variant
- Privacy is not guaranteed; this setup reduces but doesn't eliminate tracking
- Always maintain backups before flashing

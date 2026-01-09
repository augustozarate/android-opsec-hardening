# 🛡️ OPSEC BASELINE — CLEAN STATE
Version: 1.0  
Scope: Personal / Multi-device  
Date: 2026-01  
DNS Layer: NextDNS  
Transport: VPN (always-on)  

---

## 🎯 Purpose

This baseline defines the **normal and expected DNS behavior** of a hardened but usable system.
It is used as a **reference point** to:

- Detect new or unexpected domains
- Identify telemetry regressions
- Validate the impact of new apps or OS updates
- Maintain OPSEC stability over time

This baseline is **not theoretical** — it is derived from real-world usage.

---

## 🧩 Environment Description

### Devices
- Android
- Windows
- Linux (desktop)

### Usage Profile
- Daily personal use
- Messaging
- Browsing
- App updates
- No testing or experimental apps during baseline capture

### Network Conditions
- Trusted network
- VPN enabled at all times
- Encrypted DNS (DoH/DoT)

---

## ⏱️ Observation Window

- Duration: 48 hours
- System state: Stable
- No new apps installed
- No configuration changes

---

## 🟢 EXPECTED ALLOWED DOMAINS (Recurring)

These domains **must resolve** for system stability and core functionality.

### Core OS & APIs
android.apis.google.com
android.clients.google.com
play.googleapis.com
play-fe.googleapis.com
www.googleapis.com
connectivitycheck.gstatic.com
time.android.com

### Messaging
g.whatsapp.net
e*.whatsapp.net
media-*.cdn.whatsapp.net
static.whatsapp.net
graph.whatsapp.com

### Browsing
mozilla.org
firefox.com
detectportal.firefox.com

### Privacy Tools (Example tools)
vpn-api.proton.me
mail-api.proton.me
pass-api.proton.me

---

## 🔴 EXPECTED BLOCKED DOMAINS (Recurring)

These domains generate **telemetry, analytics or tracking** and are intentionally blocked.
Their presence in logs is **normal and desired**.

### Google Telemetry
app-measurement.com
firebaseinstallations.googleapis.com
firebase-settings.crashlytics.com
people-pa.googleapis.com
playatoms-pa.googleapis.com
voilatile-pa.googleapis.com
footprints-pa.googleapis.com

### Meta / Facebook Tracking
connect.facebook.net
analytics.facebook.com
collector.facebook.com
graph-fallback.facebook.com
edge-mqtt.facebook.com

### Browser Telemetry
incoming.telemetry.mozilla.org
telemetry.mozilla.org
location.services.mozilla.com

### Generic Advertising & Analytics
doubleclick.net
googleads.g.doubleclick.net
adservice.google.com
scorecardresearch.com
branch.io
adjust.com

---

## 🧱 ROOT DOMAIN PATTERNS (Normal)

The following root domains appear frequently and are considered normal:

*.googleapis.com
*.whatsapp.net
*.fbcdn.net
*.mozilla.com

---

## 🚫 ABSENT BY DESIGN (IMPORTANT)

The following **must NOT appear** in baseline logs:

### Phantom / Abuse TLDs
.xyz
.top
.gq
.ml
.cf
.tk
.click
.link
.download
.loan
.review

Their presence indicates:
- Ad SDK leakage
- Malvertising
- Low-reputation infrastructure
- Potential OPSEC degradation

---

## 🚨 ANOMALY TRIGGERS

Any of the following **breaks the baseline** and requires investigation:

- New root domain not listed above
- Recurrent domain using suspicious TLD
- High-frequency queries from unknown service
- Telemetry domains resolving instead of being blocked
- DNS activity when device is idle

---

## 📊 Baseline Health Indicators

A healthy baseline shows:

- >80% traffic from known domains
- Telemetry mostly blocked, not resolved
- No phantom TLDs
- Messaging and updates fully functional
- Low DNS entropy (predictable patterns)

---

## 🔁 Change Management

Any change to this baseline must be documented:

- OS update
- New application
- DNS rule modification
- VPN change

Update version number and date accordingly.

---

## 🧠 Final Principle

> OPSEC is not about blocking everything.  
> OPSEC is about **knowing exactly what is normal**.

This baseline represents that normal state.

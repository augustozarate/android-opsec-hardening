# NextDNS – OPSEC Allowlists & Blocklists

This directory contains **curated domain lists** designed to be used with **NextDNS**
as part of a **hybrid OPSEC strategy** focused on:

- Privacy
- Stability
- Usability

The lists are **platform-agnostic** and can be applied to:

- Android  
- iOS / iPadOS  
- Windows  
- macOS  
- Linux  
- Routers supporting NextDNS  

---

## 📂 Directory Structure
```text
nextdns/
├── allowlists/
│ ├── allowlist-messaging.txt
│ ├── allowlist-web.txt
│ └── allowlist-tools-example.txt
│
├── blocklists/
│ ├── blocklist-google-opsec.txt
│ ├── blocklist-meta-opsec.txt
│ └── blocklist-samsung.txt
│
└── README.md
```

---

## 🟢 Allowlists

These lists define domains that **must remain resolvable** to preserve
core functionality and usability.

### `allowlist-messaging.txt`

Essential messaging services:

- WhatsApp
- Threema
- Proton ecosystem

⚠️ Blocking these domains **will break communication**.

---

### `allowlist-web.txt`

Core web and system services:

- Connectivity checks
- Time synchronization
- Critical system APIs

✅ Recommended to keep enabled on **all devices**.

---

### `allowlist-tools-example.txt`

Example allowlist for **trusted tools and services**:

- VPN APIs
- Security tools
- Productivity services

This file is **intentionally customizable** per user or environment.

---

## 🔴 Blocklists

These lists focus on **telemetry, analytics, and tracking infrastructure**.

### `blocklist-google-opsec.txt`

Targets:

- Firebase telemetry
- Google Analytics
- Ads and measurement endpoints

✅ Safe to block in most **personal OPSEC scenarios** without affecting:

- Play Store downloads  
- Google account logins  

---

### `blocklist-meta-opsec.txt`

Targets:

- Facebook / Instagram tracking
- MQTT telemetry
- Embedded analytics

Allows **limited service usage** while significantly reducing
behavioral tracking.

---

### `blocklist-samsung.txt`

Targets:

- Samsung diagnostics
- Device analytics
- Background reporting services

Recommended for **Samsung devices** where telemetry reduction is desired.

---

## ⚠️ Usage Notes

- Apply lists **incrementally**
- Monitor DNS logs after enabling
- Never block allowlists blindly
- **Stability > aggressive blocking**

These lists are designed to **reduce DNS noise**, not to break services.

---

## 🛡️ Ethical Use

These configurations are intended for:

- Personal privacy
- Home network protection
- Educational and research purposes

❌ Do **NOT** use them to:

- Disrupt third-party networks
- Bypass organizational security controls
- Interfere with services you do not own

---

## 📌 Final Note

NextDNS is a powerful tool — misuse can cause instability.

Always test changes **per profile and device**.

> **Privacy is a process, not a switch.**

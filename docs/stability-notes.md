# Stability Notes – What NOT to Block

This document lists domains and services that should **not** be blocked
to preserve Android stability and core functionality.

## Core Android & Google Services
Blocking these may cause system instability or app failures:

- `android.apis.google.com`
- `play.googleapis.com`
- `play-fe.googleapis.com`
- `gstatic.com`
- `firebaseinstallations.googleapis.com`

## Messaging & Push Notifications
Required for reliable message delivery:

- `g.whatsapp.net`
- `mtalk.google.com`
- `gcm.googleapis.com`

## Browsers & Updates
Blocking may break browsing, sync, or security updates:

### Firefox
- `firefox.settings.services.mozilla.com`
- `location.services.mozilla.com`

### Chromium-based
- `clients2.google.com`
- `update.googleapis.com`

## Social Media (View-only Mode)
Minimal allowlist required for basic functionality:

- `graph.facebook.com`
- `edge-mqtt.facebook.com`
- `i.instagram.com`

Aggressive blocking beyond this may:
- Break feeds
- Disable notifications
- Cause login loops

## General Recommendations
- Prefer DNS allowlisting over disabling system apps
- Apply changes incrementally
- Observe DNS metrics before and after changes
- Avoid blocking wildcard domains blindly

Security controls must **not** compromise availability.

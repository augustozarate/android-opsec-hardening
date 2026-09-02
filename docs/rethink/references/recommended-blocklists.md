# Recommended Blocklists

## 1. Purpose

This document contains blocklists considered useful within the Android OPSEC Hardening project.

The objective is not to enable every available blocklist.

Instead, filtering should provide a reasonable balance between:

- Privacy
- Telemetry reduction
- Tracking protection
- Security
- Application compatibility

No third-party blocklists are redistributed by this repository.

---

## 2. Selection Principles

Blocklists should be selected according to their purpose rather than their size.

A practical filtering model is:

```
General privacy
      +
Tracking protection
      +
Threat filtering
      +
Targeted OPSEC rules
```

Avoid stacking multiple aggressive lists that block substantially the same domains.

Excessive overlap increases troubleshooting complexity without necessarily producing equivalent security benefits.

---

## 3. Core Privacy Filtering

### NextDNS Ads & Trackers Blocklist

**Category:** General privacy  
**Aggressiveness:** Medium

Purpose:

- Advertising domains
- Common tracking infrastructure
- General telemetry

This list provides a reasonable baseline when NextDNS is used as the active DNS filtering provider.

---

### OISD

**Category:** Privacy / advertising / tracking  
**Aggressiveness:** Medium to High

Purpose:

- Advertising
- Tracking
- Known unwanted domains
- Broad privacy filtering

OISD is generally suitable when broad filtering is desired without manually combining a large number of independent lists.

Compatibility should still be monitored.

---

## 4. Advanced Filtering

### HaGeZi Multi

HaGeZi provides several filtering levels.

More aggressive variants may significantly increase blocking coverage but can also increase compatibility issues.

For an OPSEC-oriented configuration, aggressive variants should only be used when the administrator is prepared to investigate and maintain allowlist exceptions.

**Category:** Privacy / telemetry / tracking  
**Aggressiveness:** Depends on selected variant

Potential effects include:

- Broken application telemetry
- Authentication issues
- Missing application functionality
- False positives

Do not select the most aggressive variant solely because it blocks more domains.

---

### StevenBlack Unified Hosts

**Category:** General advertising and tracking  
**Aggressiveness:** Medium

Purpose:

- Advertising domains
- Tracking infrastructure
- Broad hosts-based filtering

Useful as a general-purpose source, particularly in environments where hosts-compatible lists are required.

---

## 5. Targeted OPSEC Lists

The project may maintain small targeted lists separately from large third-party blocklists.

Examples include:

```
nextdns/blocklists/
├── blocklist-google-opsec.txt
├── blocklist-meta-opsec.txt
└── blocklist-samsung.txt
```

These lists should not attempt to replace established threat or privacy feeds.

Their purpose is to document project-specific filtering decisions that have been individually investigated.

A domain should not be added merely because it belongs to Google, Meta, Samsung, Microsoft, or another large vendor.

Classification should be based on observed behavior and technical purpose.

---

## 6. Allowlisting

False positives should be handled through targeted allowlisting.

Project examples include:

```
nextdns/allowlists/
├── allowlist-example.txt
├── allowlist-messaging.txt
└── allowlist-web.txt
```

Before allowlisting a domain:

1. Identify which application generated the request.
2. Confirm that blocking affects required functionality.
3. Determine the domain's purpose when possible.
4. Add the narrowest practical exception.
5. Retest the application.

Avoid broad wildcard exceptions unless technically necessary.

---

## 7. Common Compatibility Areas

Aggressive filtering can affect:

### Push Notifications

Blocking push infrastructure can delay or completely prevent notifications.

### Authentication

Identity providers, CAPTCHA systems, OAuth endpoints, and anti-abuse services may be required for login.

### Messaging

Messaging applications may rely on several infrastructure providers for attachments, notifications, calls, or synchronization.

### Media

CDNs, advertising infrastructure, DRM, analytics, and media delivery may share related infrastructure.

### Application Updates

Package repositories and vendor update infrastructure should not be blocked without understanding their function.

---

## 8. Blocklist Evaluation Workflow

When testing a new blocklist:

```
Enable list
    |
    v
Generate normal application traffic
    |
    v
Inspect blocked DNS requests
    |
    v
Check application functionality
    |
    +---- Working normally
    |        |
    |        v
    |     Continue monitoring
    |
    +---- Functionality broken
             |
             v
       Investigate domain
             |
             v
       Targeted allowlist
```

Do not permanently allow a blocked domain solely because it appears frequently in logs.

Frequency does not establish necessity.

---

## 9. Recommended Strategy

For most configurations, prefer:

```
One primary balanced blocklist
          +
Selected security protections
          +
Small project-specific rules
          +
Minimal allowlisting
```

rather than:

```
Blocklist A
+ Blocklist B
+ Blocklist C
+ Blocklist D
+ Blocklist E
+ ...
```

The first model is easier to audit and troubleshoot.

---

## 10. RethinkDNS Context

When filtering is performed through RethinkDNS or through an upstream DNS provider used by RethinkDNS, blocked queries should be correlated with application activity.

Useful information includes:

- Application
- Domain
- Query type
- Resolver
- Block/allow decision
- Timestamp

This makes it possible to distinguish between expected telemetry blocking and application-breaking false positives.

---

## 11. Maintenance

Blocklist behavior changes over time.

Periodically review:

- Lists that are no longer maintained
- Newly introduced false positives
- Redundant lists
- Allowlist entries that are no longer necessary
- Application behavior after updates

A filtering configuration should be treated as a maintained policy rather than a one-time setup.

---

## 12. Security Consideration

DNS blocklists are a filtering control, not a complete security boundary.

They should complement:

- Application isolation
- Firewall policies
- Encrypted DNS
- VPN/WireGuard routing
- Operating-system security
- Application permissions
- Network monitoring

A domain not appearing on a blocklist should not automatically be considered trustworthy.

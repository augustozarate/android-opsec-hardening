# Contributing to Android OPSEC Hardening

Thank you for your interest in contributing to Android OPSEC Hardening.

This project is focused on Android security, privacy, operational security (OPSEC), network hardening, DNS filtering, application isolation, VPN architectures, and reproducible security configurations.

Contributions are welcome, but they should follow the project's engineering principles and documentation standards.

---

## 1. Project Philosophy

Android OPSEC Hardening follows a security engineering approach rather than a collection of arbitrary configuration recommendations.

Contributions should therefore prioritize:

- Evidence over assumptions.
- Reproducibility over personal preference.
- Defense in depth over reliance on a single security mechanism.
- Explicit documentation of security trade-offs.
- Validation before recommending a configuration.
- Maintainability over unnecessary complexity.

A configuration should not be considered secure simply because it appears to work.

Whenever possible, it should be tested, documented, and validated against its intended security objective.

---

# 2. Contribution Principles

All contributions should follow these principles.

## 2.1 Evidence-based recommendations

Security recommendations should be supported by one or more of the following:

- Official documentation.
- Reproducible testing.
- Project source code.
- Security research.
- Reliable technical references.
- Documented real-world observations.

Personal experience can be valuable, but it should be clearly identified as such.

---

## 2.2 Reproducibility

A reader should be able to understand how a configuration was obtained and reproduce the relevant test whenever practical.

When documenting a test, include:

- Device.
- Android version.
- ROM.
- Application version.
- Relevant configuration.
- Network environment.
- Expected result.
- Observed result.

Example:

    Device:
    Samsung Galaxy A50

    ROM:
    crDroid

    RethinkDNS:
    v0.5.5x

    DNS:
    NextDNS / DoH

    VPN:
    Proton WireGuard

---

## 2.3 Security claims

Avoid absolute statements such as:

> "This configuration prevents all DNS leaks."

Prefer technically bounded statements such as:

> "This configuration prevented DNS queries from bypassing the configured resolver during the tested scenarios."

Security behavior is dependent on implementation, configuration, software versions, operating-system behavior, and test conditions.

---

# 3. Documentation Standards

Documentation should use Markdown unless another format is specifically justified.

Documents should be:

- Concise where possible.
- Technically precise.
- Reproducible.
- Consistent with existing terminology.
- Explicit about limitations.

Avoid documenting configuration values without explaining their purpose.

Whenever possible, explain:

1. What the setting does.
2. Why it is enabled or disabled.
3. What security property it provides.
4. What trade-offs it introduces.
5. How it can be validated.

---

# 4. Document Types

The project uses several documentation categories.

## Architecture Documents

Architecture documents describe system design and component interaction.

Naming convention:

    ARCH-XXX

Example:

    ARCH-001 – RethinkDNS Architecture

---

## Engineering Notes

Engineering Notes document investigations, experiments, technical observations, and version comparisons.

Naming convention:

    EN-XXXX

Example:

    EN-0001 – RethinkDNS v0.5.5x vs v0.5.5y

---

## Architecture Decision Records

ADRs document important architectural decisions and their rationale.

Naming convention:

    ADR-XXXX

Example:

    ADR-0001 – Adoption of NextDNS as the primary DNS provider

---

## Validation Reports

Validation reports document reproducible tests used to verify architecture, configuration, or security behavior.

Naming convention:

    VAL-XXX

Example:

    VAL-002 – Network Transition & WireGuard Routing Validation

Validation reports should define their scope, environment, methodology, observed results, limitations, and supporting evidence.

---

## Standard Operating Procedures

SOP documents describe repeatable operational procedures.

Naming convention:

    SOP-XXXX

Example:

    SOP-0001 – RethinkDNS Backup and Restore

---

## Case Studies

Case Studies document real-world deployments or specific testing scenarios.

Naming convention:

    CS-XXXX

Example:

    CS-0001 – Samsung Galaxy A50 with crDroid

---

## Knowledge Base

Knowledge Base articles explain individual technical concepts.

Naming convention:

    KB-XXXX

Example:

    KB-0001 – Split DNS

---

# 5. Document Metadata

Technical documents should include metadata whenever practical.

Recommended format:

    Document ID: ARCH-001
    Title: RethinkDNS Architecture
    Version: 1.0
    Status: Draft
    Last Updated: YYYY-MM-DD

Possible document states:

- Draft
- Under Review
- Validated
- Published
- Deprecated
- Archived

---

# 6. Configuration Changes

Changes to security configurations should explain their purpose.

Avoid:

    Enable setting X.

Prefer:

    Enable setting X because it prevents the specified traffic class from bypassing the intended security control.

Document relevant dependencies and interactions with other components.

This is especially important for:

- DNS configuration.
- VPN routing.
- Firewall rules.
- Proxy rules.
- Application isolation.
- Network automation.
- Split DNS.
- IPv4/IPv6 behavior.

---

# 7. RethinkDNS Contributions

RethinkDNS is treated as an architectural component rather than simply an application.

Changes or recommendations involving RethinkDNS should consider:

- DNS configuration.
- Proxy configuration.
- WireGuard configuration.
- Firewall behavior.
- Application routing.
- Advanced Mode.
- Split DNS.
- DNS bypass behavior.
- Lockdown behavior.
- IPv4/IPv6.
- Network transitions.
- Application-specific routing.
- Version-specific behavior.

When documenting behavior that may depend on a specific RethinkDNS release, always record the tested version.

Example:

    Tested with:
    RethinkDNS:
    <TESTED_VERSION>

Do not assume that behavior observed in one release applies to future versions.

---

# 8. Version Testing

Software updates should not automatically be considered improvements from an architectural perspective.

When a new version introduces significant networking or security changes, testing should be performed against a known baseline.

Recommended process:

    Current stable version
            |
            v
    Backup configuration
            |
            v
    Install candidate version
            |
            v
    Execute validation tests
            |
            v
    Compare with baseline
            |
            v
    Accept / Reject / Continue Testing

This approach is particularly important for networking components such as RethinkDNS, VPN clients, DNS resolvers, and Android networking components.

---

# 9. Testing and Validation

Tests should define an expected result before the test is performed whenever possible.

Recommended structure:

    Test ID:
    TEST-001

    Objective:

    Environment:

    Configuration:

    Procedure:

    Expected Result:

    Observed Result:

    Status:

    Notes:

Possible test states:

- PASS
- FAIL
- PARTIAL
- INCONCLUSIVE
- NOT TESTED

A failed test should not be hidden.

Failures are valuable information and should be documented when they reveal an architectural limitation or software issue.

---

# 10. Security and Privacy

Do not commit sensitive information to the repository.

Never include:

- Private keys.
- VPN credentials.
- API tokens.
- Authentication credentials.
- Personal DNS identifiers when they should remain private.
- Private IP addresses when unnecessary.
- Personal identifiers.
- Backup files containing secrets.

Use placeholders when documenting configuration examples.

Example:

    <NEXTDNS_PROFILE_ID>

    <WIREGUARD_PRIVATE_KEY>

    <VPN_ENDPOINT>

When sanitizing evidence, preserve the technical context whenever possible.

For example:

    <REDACTED>.dns.example.net:853

is preferable to removing the complete resolver field when the domain and transport are relevant to the validation.

---

# 11. Python Scripts

Python scripts included in the project should prioritize:

- Readability.
- Maintainability.
- Explicit input/output behavior.
- Error handling.
- Minimal external dependencies.
- Clear documentation.

Scripts should avoid hard-coded personal information.

Where practical, configuration values should be provided through:

- Arguments.
- Configuration files.
- Environment variables.

---

# 12. Domain and DNS Classification

Domain classifications should explain why a domain or category is being recommended for blocking.

Whenever possible, record:

- Domain.
- Classification.
- Reason.
- Source.
- Confidence.
- Recommended action.

Example:

    Domain:
    example.com

    Classification:
    Newly Registered Domain

    Action:
    Block

    Reason:
    Domain associated with the evaluated security category.

A domain should not be classified as malicious solely because it is unfamiliar.

---

# 13. Pull Requests

Before submitting a pull request, verify:

- Documentation is complete.
- Technical claims are supported.
- Configuration examples do not contain secrets.
- Tests have been performed where applicable.
- Version information is included.
- Existing documentation has been updated when necessary.

Pull requests should explain:

- What changed.
- Why it changed.
- How it was tested.
- Any known limitations.

---

# 14. Issues

Issues should contain enough information to reproduce the reported problem.

For technical issues, include when relevant:

- Device.
- Android version.
- ROM.
- Application version.
- Configuration.
- Network type.
- Expected behavior.
- Actual behavior.
- Relevant logs.

Do not include credentials, private keys, or other sensitive information.

---

# 15. Research Contributions

Experimental findings are welcome.

Not every experiment needs to produce a recommendation.

A contribution may document:

- A successful configuration.
- A failed configuration.
- An unexpected behavior.
- A performance regression.
- A compatibility issue.
- A version-specific bug.
- An architectural limitation.

Negative results are considered valuable when properly documented.

---

# 16. Architecture Decisions

If a contribution introduces a significant architectural change, consider creating an Architecture Decision Record (ADR).

Examples include:

- Adding or removing a security component.
- Changing the primary DNS architecture.
- Introducing a new VPN routing model.
- Changing application isolation strategy.
- Adopting a new network security mechanism.

The ADR should explain:

- Context.
- Problem.
- Alternatives.
- Decision.
- Consequences.

---

# 17. Engineering Notes

Use an Engineering Note when the primary purpose is documenting an investigation rather than making a permanent architectural decision.

Engineering Notes may later lead to:

- An ADR.
- A configuration recommendation.
- A new validation test.
- A Case Study.
- A Knowledge Base article.

This allows experimentation to remain separate from finalized architecture.

---

# 18. Updating Existing Documentation

Prefer updating an existing document rather than creating duplicates.

Create a new document when:

- The subject has a substantially different purpose.
- The existing document would become excessively large.
- The information represents a new investigation.
- The information represents a new architectural decision.
- The information describes a different deployment scenario.

---

# 19. Documentation Lifecycle

Documentation follows this general lifecycle:

    Draft
      |
      v
    Review
      |
      v
    Validated
      |
      v
    Published
      |
      v
    Deprecated / Archived

A document should not be marked as validated solely because the configuration works on one device.

Validation should consider the documented scope and limitations of the test.

---

# 20. General Rule

The primary rule for contributing to Android OPSEC Hardening is:

> Document not only what works, but why it works, how it was tested, and where it may fail.

The objective is not to create a collection of "perfect configurations."

The objective is to build a reproducible and continuously evolving security reference for Android.

---

## License

Contributions to this project are subject to the project's license.

By contributing, you agree that your contributions may be distributed under the terms of that license.

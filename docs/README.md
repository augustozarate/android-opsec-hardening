# Android OPSEC Hardening — Documentation

This directory contains the technical documentation for the
**Android OPSEC Hardening** project.

The documentation follows an evidence-oriented security engineering
approach.

Configurations are documented separately from the tests used to
validate them.

---

## Start Here

For the complete documentation map, see:

**[Documentation Index](Documentation-Index.md)**

For contribution and documentation standards, see:

**[Contributing Guidelines](CONTRIBUTING.md)**

---

## Documentation Modules

### RethinkDNS

**[RethinkDNS Documentation](rethink/README.md)**

Contains the current RethinkDNS architecture, configuration guidance,
validation reports, references, and supporting evidence.

```text
rethink/
├── architecture/
├── guides/
├── references/
├── validation/
└── README.md
```

Current RethinkDNS work includes:

- Base network architecture
- Traffic-flow documentation
- DNS validation
- WireGuard transition validation
- Firewall behavior validation
- UDP/HTTP3 observations
- Version regression testing
- Configuration recommendations
- Blocklist strategy

---

## Documentation Principles

The project follows several core principles:

```text
Evidence over assumptions
Reproducibility over preference
Validation before recommendation
Explicit limitations
Sensitive-data minimization
```

A configuration being enabled does not by itself demonstrate that the
intended security property is working.

Where practical, behavior is validated through controlled testing,
logs, network observations, and supporting evidence.

---

## Repository Context

Documentation under `docs/` is complemented by operational resources
elsewhere in the repository:

```text
devices/     Device-specific configuration
nextdns/     NextDNS filtering policies
opsec/       OPSEC tooling, datasets and case studies
screenshots/ General supporting screenshots
```

See the main project README for the complete repository overview.

---

## Documentation Status

Documentation evolves alongside testing.

Individual documents may have states such as:

- Draft
- Under Review
- Validated
- Published
- Deprecated
- Archived

A validation result applies only to the scope and environment documented
by the corresponding test.

---

## Contributing

Before contributing documentation, validation results, configuration
changes, or security research, read:

**[CONTRIBUTING.md](CONTRIBUTING.md)**

Do not commit credentials, private keys, personal DNS identifiers, or
other sensitive configuration data.

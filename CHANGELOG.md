# Changelog

All notable changes to Thirsty-Lang are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Optional dev dependencies: pytest, black, ruff, mypy
- Pre-commit hooks: version sync, pyproject validation, entry point checks
- GPG signing guide for wheel releases (docs/SIGNING.md)
- CI enhancement: setuptools version pinning in release workflow
- CI enhancement: wheel contents verification step
- Comprehensive governance model documentation (docs/governance_model.md)

### Changed
- Enhanced .gitignore with test/coverage/type-checking artifacts
- Expanded build model audit and documentation

### Fixed
- LICENSE copyright year: updated to 2025-2026 range
- Test suite: fixed utf.tarl.spec import in test_tarl.py
- Package build: moved tarl/spec.py into src/utf/tarl/ (wheel inclusion)
- Console scripts: added tscg, tscg-b, tarl, shadow-thirst to entry points
- CLI: tscg-b now accepts --help/-h flags

---

## [0.1.4] - 2025-06-19

### Added
- T.A.R.L. (Thirsty's Active Resistance Language) implementation:
  - Policy parser and sandboxed expression evaluator
  - LRU-cached runtime with parallel rule evaluation
  - Default-deny governance model for security
- CLI support for TARL policy evaluation (tarl eval, tarl parse)
- Lockfile-aware module resolution (--locked flag)
- Reserved Tier 5/6 security keywords documented in GRAMMAR.md
- Smoke test workflow (CI): validates all CLI entry points and imports on Python 3.11, 3.12
- 6 console script entry points: thirsty, thirst-of-gods, tarl, tscg, tscg-b, shadow-thirst

### Fixed
- Govern --auto-tarl TarlRuntime evaluation (indentation + body_len)
- TarlRuntime.body_len now uses BlockStmt.stmts correctly
- Double-print bug in drink/pour operations (now return None)

### Changed
- Package structure: added thirsty_lang shim package for import parity

---

## [0.1.3] - 2025-06-12

### Added
- README enhancements: install section with pinned/upgrade instructions
- Version reference bumped to 0.1.3 throughout

### Fixed
- Double-print issue resolved (drink/pour functions)

---

## [0.1.2] - 2025-06-10

### Added
- Dynamic __version__ via importlib.metadata
- Fallback version handling for editable installs

### Fixed
- Import path compatibility: from src.utf → from utf for PyPI packages

---

## [0.1.1] - 2025-06-08

### Added
- thirsty_lang shim package for backward compatibility
- __version__ dynamic synchronization

### Fixed
- __version__ sync between utf.thirsty_lang and CLI output

---

## [0.1.0] - 2025-06-01

### Added
- Initial release of Thirsty-Lang
- Tier 1 (Core) language implementation
- 11 CLI subcommands (run, repl, fmt, new, build, govern, add, audit, lock, doctor, lsp, docs)
- Standard library with 14 namespaces
- Type system with generics and type inference
- Module system with import resolution
- Package manager integration
- Security framework (sanitization, armor, security blocks)
- Mutation analysis and shadow execution
- Comprehensive documentation

### Features
- Governance-first design philosophy
- Deny-by-default policy model (T.A.R.L.)
- No runtime dependencies (stdlib only)
- Apache 2.0 license

---

## [Unreleased] Future Roadmap

### Planned for 0.1.5+
- Pre-commit hook integration for contributor workflow
- GPG-signed wheel releases
- Extended type checking (mypy integration)
- Code coverage tracking
- Automated changelog generation
- Tier 2 enhancements (task scheduling, network policies)

### Planned for 0.2.0+
- Tier 3-6 language tiers
- External system integration (HTTP, SQL, etc.)
- Advanced governance models
- Performance optimizations
- IDE plugin support (VSCode, JetBrains)

---

## Legend

- **Added** — New features or functionality
- **Changed** — Changes to existing functionality
- **Fixed** — Bug fixes
- **Removed** — Deprecated or removed features
- **Security** — Security-related updates or advisories

---

For upgrade instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).
For installation, see [README.md](README.md).

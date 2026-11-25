# Mandatory repository instructions

All human and automated contributors must follow [the engineering standard](docs/HA_ENGINEERING_STANDARD.md), [CONTRIBUTING.md](CONTRIBUTING.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

- Use a focused branch and PR linked to every addressed issue; record new findings in [the audit register](docs/AUDIT_REGISTER.md) and individual GitHub issues.
- Every production/tooling definition and every new or changed test definition needs a meaningful docstring, type hints where appropriate, and inline rationale for complex or security-relevant logic.
- Never treat missing validation evidence as a pass; record exact commands, commit and results. Run the policy gate, its self-tests, the full integration tests, lint, format, type and applicable security/HA/HACS checks.
- Preserve stable entity IDs, supported config schemas, user options and license obligations. Document breaking changes, migrations, privacy, compatibility and rollback.
- Keep the manifest release version, minimum HA version and config/storage schema versions separate. Do not publish or deploy without a validated release.
- No live credentials, parcel identifiers or raw private payloads in Git, logs, examples or issue reports.
- The legacy test-docstring exception is immutable and tracked by #39. Do not add exceptions or alter the baseline to pass CI.
- Use the repository standard if older upstream or agent-specific instructions conflict with it; consult official Home Assistant/HACS documentation for current behavior.

Current release publication is intentionally blocked pending the independent, verified release pipeline (#3, #32, #33).

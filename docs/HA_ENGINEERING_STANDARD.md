# Home Assistant custom integration engineering standard

Standard revision: 1.0.0. Applies to every new or changed custom integration owned by this project; first adoption: ha-gls. This is a portable repository standard, not a claim of compliance by other repositories or an official Home Assistant certification. The upstream contributor rules take precedence for HA behavior; project requirements may be stricter.

## 1. Versioning and compatibility

- Use Semantic Versioning (MAJOR.MINOR.PATCH) for independently released integrations. MAJOR = incompatible public behavior (entities, actions, events, config or data); MINOR = backwards-compatible feature; PATCH = backwards-compatible bug/security fix. Documentation-only maintenance need not publish a release.
- Keep the authoritative package version in custom_components/<domain>/manifest.json. A release tag and title must match this version exactly (no v prefix); a tag is immutable. Pre-release suffixes alpha.N, beta.N and rc.N are permitted only for explicitly marked pre-releases; production uses stable versions. Never reuse an existing release version.
- Preserve GLS's inherited version 2.0.1. It is not evidence of a release from this repository. Do not reset the version counter or publish a release just to establish this standard.
- Keep the minimum supported Home Assistant Core version in hacs.json: homeassistant. Use the HA YYYY.MM.PATCH format, with no leading zero on the month. Validate against both that minimum and the current supported stable Core version, using their supported Python versions. Raise minimum only with documented evidence and user-visible notes.
- ConfigFlow VERSION / MINOR_VERSION and Store schema versions are independent schema revisions, not release numbers. Use HA config-entry migration for incompatible persisted schemas, test upgrade and reload, preserve entity unique IDs and user options. Never invent compatibility or migrations that are not needed.
- Record user-visible changes under CHANGELOG.md's Unreleased section. A release PR moves them to the exact release version heading. Document breaking changes, minimum Core, migration, known limitations, and rollback.
- Release only an exact, approved, green main commit. Check manifest/tag/ZIP consistency; include required license notices, ensure archive structure matches HACS, record SHA-256 and provenance. Dry-run must be read-only. Stable releases require no unresolved release-blocking findings, a clean installation/update/rollback smoke test, and no unverified claim of production deployment. Until release issues #3, #32, #33 are resolved, release publication is disabled; manual dispatch is a read-only candidate check. A tag push validates metadata but does not publish.

## 2. Coding and architecture

- Use HA's documented integration structure, immutable domain, config flow and options flow, typed ConfigEntry.runtime_data, correct setup/unload/remove/migrate, and config-entry scoped resources. Keep carrier transport, data model, coordinator, entities and services separate. Use async API I/O, HA-managed sessions, no blocking work on the event loop, no network I/O from entity properties.
- All nonempty Python modules, classes, functions, methods, private helpers, nested functions, callbacks, and async functions require meaningful docstrings. Document purpose, non-obvious input/output contracts, failure cases and side effects as appropriate. Add inline comments for invariants, unusual carrier behavior, ordering, security boundaries and compatibility decisions; do not narrate self-evident syntax. Prefer descriptive identifiers; avoid placeholder comments and generated boilerplate.
- Use type hints for inputs/returns, explicit data contracts, precise exceptions and clear ownership. Use Ruff lint/format, type checking, consistent imports and small testable functions. Do not suppress checks without a linked issue and justification.
- Use stable unique IDs and device identifiers. Preserve user customizations on temporary errors. Localize UI strings, errors, actions and options; test structure and placeholders across translations. Support light/dark via HA theme tokens for any UI; avoid hard-coded colors or frontend dependencies in backend integrations.
- Model availability, stale data, last-success time and retry separately. Use DataUpdateCoordinator appropriately, bounded concurrency, timeout/body limits, cancellation, explicit rate-limit handling and backoff. Validate input and API schemas; do not equate malformed responses with empty data.
- Define service/action permissions, explicit target selection, deterministic state transitions and safe restart/reload behavior. Follow HA entity, recorder, event and diagnostics contracts. Keep public event payloads minimal and documented.

## 3. Security, privacy and dependencies

- Least privilege for HA users, accounts, API tokens, Actions permissions and release identities. Never commit credentials, captured live payloads or personal identifiers; synthetic fixtures only.
- Enforce TLS, trusted endpoint/redirect policy, bounded responses, secret-safe errors and scoped session/cache isolation. Never bypass carrier authentication, CAPTCHA, MFA or access controls.
- Allowlist published attributes/events/diagnostics; redact tokens, IDs, addresses, tracking references, URLs and unexpected free text. Do not leak data through log/trace/Recorder paths. Document data flow, persistence, retention, deletion and external destinations. Optional AI processing must be explicitly opted in.
- Review dependencies and licenses; pin compatible runtime requirements and CI dependencies, review transitive updates and CVEs. Pin external actions and reusable workflows to reviewed immutable commits. Run secret scanning (including history), dependency/security scans, and offer private vulnerability reporting.

## 4. Documentation and testing

- Maintain README (installation, config, examples, compatibility, capabilities, limitations, troubleshooting), architecture/data contracts, changelog, contribution instructions, security/privacy guidance and source/license attribution. Update docs alongside behavior and translations; clearly distinguish planned from implemented behavior.
- Add regression tests for each finding. Use mocked API calls with synthetic data; test setup, reauth, unload, restart, migration, failures, retries, malformed data, race conditions, permissions, privacy, multi-entry isolation and entity/event contract. Test public behavior, not merely implementation internals. Live tests use only an authorized test account and safe operations.
- Target at least 95% line coverage across integration code; require tests on new/changed behavior, Ruff format/lint, type checking, hassfest, HACS validation, translation/metadata/docstring policy checks and applicable security scans. Coverage is not proof of correctness. Test minimum/current supported HA and record exact versions and commit. Pin the test harness to a matching Core version. The newest published harness on 2026-11-25 targets HA 2026.10.4, while Core 2026.11.3 is available; validation of the latter remains outstanding under #34. Never claim the untested version is covered.
- The temporary baseline for undocumented existing test definitions is pinned to the initial audited commit; unchanged legacy definitions alone are grandfathered under #39. New or changed undocumented test definitions fail the policy check. Production and engineering tooling have no such exceptions. Remove the baseline when #39 is resolved.

## 5. Home Assistant quality checklist

For every integration, evaluate the official quality-scale rules individually. Record done/todo/exempt, evidence and justified exemptions; use quality_scale.yaml when claiming a tier in HA's supported format. Do not equate an internal checklist with HA Core approval.
- Bronze: UI setup/config flow tests, setup failures, clean unload, unique IDs, appropriate polling and essential user documentation.
- Silver: availability and error handling, reauth, integration ownership, strong test coverage and reliability documentation.
- Gold: diagnostics, localization, repair/reconfigure/discovery when applicable, device/entity modeling, end-user docs and supported features.
- Platinum: strict typing, async dependencies and shared sessions.
- Use the current official exhaustive rule list for the actual assessment. The GLS manifest identifies this as a custom integration, not an officially graded Core integration. Track the [internal evidence register](HA_QUALITY_ASSESSMENT.md) against every applicable rule under #40; do not claim compliance based on this checklist alone.

## 6. Definition of done and issue traceability

- Create an individual GitHub issue for each independent defect, with impact, evidence (immutable source reference), severity, expected behavior, acceptance criteria, and tests. Add it to the version-controlled audit register; issue status is authoritative.
- Use an isolated branch and a focused PR, link issues, explain scope and decisions, identify breaking changes and security/privacy implications. Never disclose live secrets in public tickets.
- Record exact test commands, results, CI head SHA, artifact/installation evidence if relevant, and any unperformed checks. Do not mark a finding completed or a PR merge-ready while acceptance criteria or mandatory checks remain unresolved.
- Protect main, require reviewed PRs and successful checks, use least privilege and controlled emergency exceptions. No direct unvalidated deployment; document rollback and verify post-deploy health.
- Apply this standard to future integrations; adopt it in each existing repository through its own reviewed PR and audit.

## References

- [HA integration manifest](https://contributors.home-assistant.io/core/integrations/manifest/)
- [HA code style](https://contributors.home-assistant.io/core/development/style/)
- [HA integration quality scale and exhaustive rules](https://contributors.home-assistant.io/core/quality-scale/)
- [HA development documentation](https://developers.home-assistant.io/)
- [HACS integration requirements](https://www.hacs.xyz/docs/publish/integration/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Audit register](AUDIT_REGISTER.md)

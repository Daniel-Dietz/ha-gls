# Home Assistant quality-scale evidence register

Internal assessment as of 2026-11-25, based on the [official 54-rule list](https://contributors.home-assistant.io/core/quality-scale/rules/). This fork is a custom integration and is not graded by Home Assistant Core. The manifest therefore declares custom. These are engineering assessment statuses, not a Core certification. Done means static evidence supports the rule; runtime/CI-specific acceptance remains subject to the exact current head checks. Todo includes unverified or incomplete evidence. Exempt means not applicable to this integration's current scope, with a rationale. Track all outstanding evidence under #40 and the linked specific audit findings.

## Bronze (20)

| Rule | State | Evidence / outstanding work |
| --- | --- | --- |
| action-setup | todo | services.py registers actions during entry setup; review HA domain-level registration (#18, #40). |
| appropriate-polling | todo | coordinator.py implements dynamic polling; fix stale health and rate limits (#9, #12, #16). |
| brands | todo | Local brand icon exists; upstream brand registration and independent HACS validation not established (#3, #43). |
| common-modules | todo | Coordinator and country transports separated; review shared entity base and repeated behavior (#40). |
| config-flow | done | config_flow.py offers UI setup, account/guest paths and options; tests/test_config_flow.py. |
| config-flow-test-coverage | todo | Config flow regression tests exist; verify full flow coverage and DE error paths (#24, #40). |
| dependency-transparency | done | No additional runtime packages in manifest; uses HA-provided libraries. |
| docs-actions | done | README Services, services.yaml, translation files. |
| docs-conditions | exempt | No integration-specific automation condition platform. |
| docs-high-level-description | done | README introduction and supported countries. |
| docs-installation-instructions | todo | Fork onboarding documented; independent released HACS installation not verified (#3, #43). |
| docs-removal-instructions | todo | README Removal; remote guest-account retention unresolved (#15). |
| docs-triggers | done | README Events and example automations. |
| entity-event-setup | todo | CoordinatorEntity manages subscriptions; per-parcel registry lifecycle needs acceptance (#19). |
| entity-unique-id | todo | IDs defined in sensor/button/calendar; collision and pending DE cases (#13, #19). |
| has-entity-name | done | Sensor, calendar and button entities use _attr_has_entity_name. |
| runtime-data | done | GlsConfigEntry and typed GlsData in __init__.py. |
| test-before-configure | todo | Account sign-in validates login, DE registers; manual hub verification is limited (#24, #40). |
| test-before-setup | done | Initial coordinator refresh before forwarding platforms; test_init.py. |
| unique-config-entry | todo | Config flow sets country/postcode or account unique IDs; validate cross-country account scoping (#40). |

## Silver (10)

| Rule | State | Evidence / outstanding work |
| --- | --- | --- |
| action-exceptions | todo | ServiceValidationError paths exist; permissions and localized errors require review (#17, #18). |
| config-entry-unloading | done | async_unload_entry and lifecycle tests in tests/test_init.py and tests/test_contents_services.py. |
| docs-configuration-parameters | done | README Configuration and Options sections. |
| docs-installation-parameters | done | README Requirements, Configuration and installation instructions. |
| entity-unavailable | todo | CoordinatorEntity used; cached failures can mask outages (#9, #10). |
| integration-owner | done | Manifest codeowner updated to repository owner in PR #42; ownership verified by repository metadata. |
| log-when-unavailable | todo | Distinguish total failure, stale data and recovery; redact logs (#9, #22). |
| parallel-updates | done | Platforms set PARALLEL_UPDATES=0; coordinator controls updates. Network fan-out still needs bounds (#12). |
| reauthentication-flow | todo | DK/PL account reauth exists; DE guest recovery and OAuth hardening remain (#7, #24, #26, #27). |
| test-coverage | done | PR #42 initial Validate job: 1,214 tests passed, 99.30% line coverage; retest each new head. |

## Gold (21)

| Rule | State | Evidence / outstanding work |
| --- | --- | --- |
| devices | done | build_device_info and per-entry device association in device.py. |
| diagnostics | todo | Existing diagnostics have incomplete redaction (#4, #5). |
| discovery | exempt | Remote parcel carrier; no supported local-network or hardware discovery protocol. Native DE account discovery separately tracked (#23). |
| discovery-update-info | exempt | No integration discovery mechanism. |
| docs-data-update | done | README Options, polling and refresh button documentation. |
| docs-examples | todo | Examples exist, but unsafe email/AI defaults and notification semantics (#29, #37). |
| docs-known-limitations | todo | Account/region limitations documented; expand verified capabilities and privacy limitations (#23, #36). |
| docs-supported-devices | exempt | Cloud service has no supported physical hardware models. |
| docs-supported-functions | done | README Features, Sensors, Events and Services. |
| docs-troubleshooting | todo | README troubleshooting exists; add safe diagnostics and real outage guidance (#5, #22). |
| docs-use-cases | done | README and examples cover parcel tracking and automation use cases. |
| dynamic-devices | exempt | One service device per configured hub/account; dynamic shipments are entities, not devices. |
| entity-category | done | last_update is diagnostic; review any new optional entities. |
| entity-device-class | done | Timestamp class on next delivery and last update; review new sensors individually. |
| entity-disabled-by-default | todo | Audit noisy/optional entity defaults and user control (#40). |
| entity-translations | done | strings.json and 19 locale structures/placeholder parity validated. |
| exception-translations | todo | Services still contain literal error messages (#18, #40). |
| icon-translations | done | icons.json, shared icon compatibility check. |
| reconfiguration-flow | todo | Options cover parcels/settings; no explicit complete reconfigure flow for connection parameters (#40). |
| repair-issues | todo | Review actionable Repairs for persistent user-fixable auth, unsupported endpoint and configuration errors (#40). |
| stale-devices | exempt | Static service device is tied to entry lifecycle; shipment entity cleanup remains #19. |

## Platinum (3)

| Rule | State | Evidence / outstanding work |
| --- | --- | --- |
| async-dependency | done | Carrier I/O uses aiohttp and async integration methods; no third-party blocking client declared. |
| inject-websession | todo | HA shared sessions generally used; review isolated B2C login client and cookie isolation (#26, #27). |
| strict-typing | todo | Mypy passes existing configuration; strict typed carrier payloads and service contracts are not yet established (#28, #40). |

## Verification notes

- GitHub Actions baseline: [Validate #45712308767](https://github.com/Daniel-Dietz/ha-gls/actions/runs/45712308767), PR #42 initial head e2303669604e7fb572a32a65f9f7d81715ffe41e. Unit tests, mypy, Ruff, translations and hassfest passed. HACS and repository policy failed. This is historical evidence, not acceptance of a later head.
- Keep the internal matrix synchronized with issue state and the official rule list. Do not mark a tier as achieved while any applicable rule is todo. Never claim an official Core grade for this custom repository.
- Follow-up [Validate #45713748477](https://github.com/Daniel-Dietz/ha-gls/actions/runs/45713748477), head `b6fb2aee2f902c54e09944798b543048665e7776`: HA 2026.2.3 and 2026.10.4 each passed 1,214 tests at 99.30% coverage. HA 2025.12.0 failed before test collection because its pinned aiodns 3.5.0 imported a removed pycares 5.x symbol. A disposable Python 3.13 environment verified imports with pycares 4.11.0 and aiohttp 3.13.2; the minimum-version requirements now pin that compatible version. Full minimum-version regression evidence remains pending (#34). No tests or required checks disabled.

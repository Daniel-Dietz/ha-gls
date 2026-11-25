# Audit register

Baseline: [`87305adc`](https://github.com/Daniel-Dietz/ha-gls/commit/87305adc947945263d8f4e405bea4e25153fa223), 2026-11-25.

Each finding has its own GitHub issue containing source references, acceptance criteria and implementation evidence. This register is a version-controlled index, not a duplicate issue state database. Issue status in GitHub is authoritative. Never close a finding without verified tests/acceptance evidence. New findings must be added here in the same workstream.

| Issue | Finding |
| --- | --- |
| [#1](https://github.com/Daniel-Dietz/ha-gls/issues/1) | [P1][Security] Protect main with mandatory validation and controlled merges |
| [#2](https://github.com/Daniel-Dietz/ha-gls/issues/2) | [P1][Supply chain] Pin and control external CI/release dependencies |
| [#3](https://github.com/Daniel-Dietz/ha-gls/issues/3) | [P1][Release] Establish a working independent HACS distribution pipeline |
| [#4](https://github.com/Daniel-Dietz/ha-gls/issues/4) | [P1][Privacy] Prevent carrier raw payloads and access material from entering HA state and events |
| [#5](https://github.com/Daniel-Dietz/ha-gls/issues/5) | [P1][Privacy] Make diagnostics safe by default instead of relying on key denylisting |
| [#6](https://github.com/Daniel-Dietz/ha-gls/issues/6) | [P1][DE] Isolate parcel-number cache by config entry and guest session |
| [#7](https://github.com/Daniel-Dietz/ha-gls/issues/7) | [P1][DE] Serialize guest-token refresh and identity recovery |
| [#8](https://github.com/Daniel-Dietz/ha-gls/issues/8) | [P1][DE] Merge learned tracking metadata without overwriting concurrent user changes |
| [#9](https://github.com/Daniel-Dietz/ha-gls/issues/9) | [P1][Reliability] Distinguish stale/failed polls from successful parcel updates |
| [#10](https://github.com/Daniel-Dietz/ha-gls/issues/10) | [P1][Reliability] Separate malformed carrier responses and HTTP failures from semantic not-found |
| [#11](https://github.com/Daniel-Dietz/ha-gls/issues/11) | [P1][Security] Validate tracking identifiers and encode all URI components |
| [#12](https://github.com/Daniel-Dietz/ha-gls/issues/12) | [P1][Reliability] Bound request concurrency, duration, response sizes and rate-limit retries |
| [#13](https://github.com/Daniel-Dietz/ha-gls/issues/13) | [P2][DE] Correct unknown/pending parcel identity in normalized state |
| [#14](https://github.com/Daniel-Dietz/ha-gls/issues/14) | [P2][DE] Recover missing carrier-side tracking records instead of polling stale IDs forever |
| [#15](https://github.com/Daniel-Dietz/ha-gls/issues/15) | [P2][Lifecycle] Reconcile untrack/remove with the remote DE guest-account list |
| [#16](https://github.com/Daniel-Dietz/ha-gls/issues/16) | [P2][Lifecycle] Revalidate delivered parcels and enforce retention without manual refresh |
| [#17](https://github.com/Daniel-Dietz/ha-gls/issues/17) | [P2][Services] Select hubs unambiguously and prevent cross-hub untracking |
| [#18](https://github.com/Daniel-Dietz/ha-gls/issues/18) | [P2][Authorization] Define permissions for configuration-mutating GLS services |
| [#19](https://github.com/Daniel-Dietz/ha-gls/issues/19) | [P2][Data integrity] Make per-parcel entity identifiers stable and non-colliding |
| [#20](https://github.com/Daniel-Dietz/ha-gls/issues/20) | [P2][Data integrity] Apply parcel contents consistently for all accepted identifier aliases |
| [#21](https://github.com/Daniel-Dietz/ha-gls/issues/21) | [P2][Data retention] Avoid stale parcel contents and silent eviction of saved user data |
| [#22](https://github.com/Daniel-Dietz/ha-gls/issues/22) | [P2][Privacy] Redact sensitive identifiers and untrusted values from logs |
| [#23](https://github.com/Daniel-Dietz/ha-gls/issues/23) | [Feature][DE] Native GLS consumer-account parcel discovery |
| [#24](https://github.com/Daniel-Dietz/ha-gls/issues/24) | [P2][DE] Validate guest-identity responses and make registration failures recoverable |
| [#25](https://github.com/Daniel-Dietz/ha-gls/issues/25) | [P2][Security] Restrict redirects on GLS requests carrying identity or personal data |
| [#26](https://github.com/Daniel-Dietz/ha-gls/issues/26) | [P2][Security][PL] Verify OAuth authorization response state and callback target |
| [#27](https://github.com/Daniel-Dietz/ha-gls/issues/27) | [P2][Reliability][PL] Validate token claim shape and bound interactive login response |
| [#28](https://github.com/Daniel-Dietz/ha-gls/issues/28) | [P2][Reliability] Isolate malformed individual parcels during normalization |
| [#29](https://github.com/Daniel-Dietz/ha-gls/issues/29) | [P2][Privacy] Make e-mail tracking automation narrowly scoped and AI opt-in |
| [#30](https://github.com/Daniel-Dietz/ha-gls/issues/30) | [P2][Operations] Own repository metadata and support routing instead of directing users upstream |
| [#31](https://github.com/Daniel-Dietz/ha-gls/issues/31) | [P2][Security process] Provide private vulnerability reporting and safe public issue forms |
| [#32](https://github.com/Daniel-Dietz/ha-gls/issues/32) | [P1][Release] Prevent manual dispatch from publishing unvalidated releases or mutating during dry-run |
| [#33](https://github.com/Daniel-Dietz/ha-gls/issues/33) | [P2][Release] Verify release tag and artifact provenance before publishing |
| [#34](https://github.com/Daniel-Dietz/ha-gls/issues/34) | [P2][CI] Make test dependencies reproducible and verify the supported HA version range |
| [#35](https://github.com/Daniel-Dietz/ha-gls/issues/35) | [P2][Security process] Add automated secret, vulnerability and dependency scanning |
| [#36](https://github.com/Daniel-Dietz/ha-gls/issues/36) | [P2][DE][Functionality] Establish accurate German delivery windows and explicit unavailable ETA |
| [#37](https://github.com/Daniel-Dietz/ha-gls/issues/37) | [P3][Examples] Correct notification example semantics and default notification target |
| [#38](https://github.com/Daniel-Dietz/ha-gls/issues/38) | [P2][Engineering] Enforce reusable Home Assistant integration engineering, documentation and versioning standards |
| [#39](https://github.com/Daniel-Dietz/ha-gls/issues/39) | [P2][Documentation] Complete existing test-function and helper docstrings |
| [#40](https://github.com/Daniel-Dietz/ha-gls/issues/40) | [P2][HA quality scale] Substantiate integration quality tier against all applicable rules |
| [#41](https://github.com/Daniel-Dietz/ha-gls/issues/41) | [P3][Licensing] Verify and preserve correct upstream license and attribution |
| [#43](https://github.com/Daniel-Dietz/ha-gls/issues/43) | [P2][HACS] Configure repository topics required by HACS validation |

The feature request #23 is not an audit defect. #38 is the engineering standard; #39–#41 record additional findings.

Scope: static main-branch audit, delta of the mail blueprint branch and follow-up AST inspection. Live carrier behavior, HA runtime acceptance, complete secret history and dependency audit remain separate verification tasks. No actual credential leak was established.

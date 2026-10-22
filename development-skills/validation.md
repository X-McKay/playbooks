# Validation evidence and known gaps

**Assessment date:** 2026-10-22. **Library:** proposed 0.1.0. **Canonical mapping baseline:** `151fca01fbc609c5550c563c902946db540c2f4c` (`0.5.0-draft.2`). This is an implementation-validation record, not a production admission or release authorization.

## What was implemented and tested

The initial release contains eight portable packages, 63 labelled case fixtures, two common JSON Schemas, an explicit dependency catalog, a separate proposed Python local profile, and a standard-library validation/export/evidence CLI. The canonical and legacy playbook trees were not changed.

The development sequence was initial implementation → complete local test run, including retained failures → cleanup/hardening → complete re-test → packaging. Initial failures were addressed rather than hidden. Cleanup corrected table formatting and an overly strict assertion that rejected valid immutable repository-tree links. It also removed an undeclared planning dependency on having the entire canonical book locally available, separated skill selection from execution-time missing inputs, made the problem-to-code entry point explicit, and aligned planned cleanup with new candidate identity and full re-test.

The CLI was strengthened to include the selected profile and full manifest in an export, verify archives without extraction, reject malformed catalogs and duplicate JSON keys, refuse vacuous positive readiness claims, replay workflow history, and preserve bounded repair and immutable observations. Additional regressions cover denied repair readability and a new candidate after invalidating an already packaged build.

## Deterministic local evidence

The originally submitted revision `147cdb4` ran **21 test methods successfully** on Python 3.12 in a Linux sandbox. These methods include multiple negative cases and complete CLI subprocess flows; 21 is the method count, not a count of agents or production trials. The post-feedback suite below adds focused regressions and runs 44 methods.

The checked behaviors include:

- all eight package structures, common draft contracts, fixture labels, owner-link pins, and profile separation;
- inventory identity changing when any package resource changes;
- catalog presence, unique short names and qualified identities, declared closure, and dependency-cycle rejection;
- reproducible ZIPs, actual selected-profile bytes, complete manifest coverage, no-overwrite defaults, offline round trips, content/manifest tampering, unsafe names, symlinks, and duplicate refusal;
- observed artifact hashes, planned-versus-observed status, blocked positive recommendations, duplicate applicability, malformed enums, traversal, and empty/all-not-applicable positive claims;
- phase order, blocked and failed receipts, unique immutable attempts, bounded repair, mandatory cleanup/full-retest, post-retest mutation invalidation, and a second frozen package after a bounded repair;
- manual state-stage tampering and refusal of a package receipt that names a non-ZIP note.

All eight packages also passed the independent Agent Skills reference validator at upstream commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379` and the local skill-creator quick validator. Draft packet and case assets passed their JSON Schemas under `jsonschema` 4.23.0; YAML parsing used PyYAML 6.0.2 in an isolated validation environment. These independent tools are not dependencies of the deterministic CLI or standard-library test suite; the separate independent-validation CI job installs their pinned development dependencies in an isolated environment.

Repository-wide Markdown lint, offline relative-link/fragment checks, compilation, and whitespace checks passed. Nix and `just` were unavailable in this environment, so their wrapper commands were not run; the applicable underlying validation commands were run directly. The development shell and `Justfile` were updated to include the skill checks for environments that use them.

## PR feedback corrections

The six defects raised on [PR #10](https://github.com/X-McKay/playbooks/pull/10), including the additional local-clone finding, were reproduced against `147cdb4` before correction. The integrated post-feedback suite passed **44 test methods** on Python 3.12, including the original suite, eight archive-feedback methods, three receipt-identity methods, three Python-profile methods, four lifecycle methods, one JSON-constant method, and four excluded-metadata methods.

Archive verification now requires exactly the two mandatory shared contracts and validates their constrained content instead of accepting absent or semantically empty contracts. Every archived skill resource must be assigned, supported, and exactly inventoried in its package descriptor. Mutation regressions cover missing contracts, malformed contract content, undeclared references/scripts, unassigned root files, omitted-plus-extra resources, and catalog metadata divergence. Complete content identity still does not prove publisher authenticity.

The central JSON parser rejects `NaN`, `Infinity`, and `-Infinity`; quoted spellings remain ordinary data. Source snapshots consistently exclude every retained receipt plus the incoming receipt and state. Root-level and mixed-location receipts now complete the sequence without spurious source invalidation, while unrelated root-code changes and tampering with historical receipts still fail.

Excluded metadata directories are now pruned before inspecting their entries rather than after strict whole-workspace traversal. A real `git clone --local` with verified hardlinked Git objects completes the full workflow with `.git` left in place; excluded cache symlink/FIFO metadata also does not block source identity. Included source and separately referenced evidence/receipts still reject symlinks and hardlinks. Package traversal remains strict by default. These filesystem regressions ran on POSIX/Linux, not on every supported coding-host operating system.

The Python profile explicitly establishes an approved `src` import path before CLI and tests, and requires test-package markers for all four layers. A fresh standard-library fixture executes CLI help/output and all literal profile checks, with the declared environment and deadlines. It also reproduces the old unmarked-layout failure. No project build-backend install or native-host session is inferred from that fixture.

Lifecycle templates no longer infer an absent trigger from missing recovery/retirement observations. A fictional bounded example uses reasoned `not_applicable` entries only when the corresponding event is absent and assesses preparedness separately; unknown triggers and unverified triggered work remain explicit gaps.

The new [independent validator](../tools/agent_skills/INDEPENDENT-VALIDATION.md) passed all eight package/reference and packet/case checks locally. The pinned dependency installation was reproduced in a fresh isolated environment, and controlled invalid fixtures/resources exited nonzero. CI now repeats these checks in a separate read-only job while the runtime CLI remains standard-library-only.

The live-model probes below describe the original submission. They were not rerun for this feedback revision and are not evidence of updated native-host adherence, production promotion, or performance uplift.

## Exploratory live-model probes

A fresh-request portable-instruction smoke experiment used the Manus built-in LLM catalog identity `gpt-6.1-sol`. It did **not** run native Codex or Claude Code. Metadata selection was tested through a custom classifier prompt with only name/description metadata, not a host's complete skill-discovery policy or competing installed library. Code drafting injected portable text directly into model context; it did not test filesystem discovery, actual progressive loading, every sibling handoff, normal host permission prompts, or a full autonomous coding session.

The first metadata experiment agreed with **17 of 24** expected labels. Inspection showed that several fixtures conflated a fitting skill that must ask for missing inputs with an ambiguous requested skill. Those development fixtures were corrected, genuinely ambiguous phase cases were added, and the earlier results remain recorded separately. The subsequent experiment agreed with **31 of 32** labels, including **8 of 8** authored held-out-labelled cases. The two experiments differ in case definitions and denominator and are not an improvement estimate. The held-out-labelled fixtures were authored for this library, not an independent external benchmark.

The retained disagreement was `specify-agent-contract` / `contract-negative-code-request`: a request to implement and connect a complete assistant was classified as a contract-planning selection rather than the expected negative near-neighbor. This is a reason to use explicit workflow invocation and to test real native-host routing; it is not silently accepted as reliable discovery.

A paired offline prototype exercise compared one skill-guided draft and one fixed generic no-skill draft, each with one generation request and no repair-until-green loop. Each draft produced code, unit tests, and documentation for a deliberately narrow supplied-policy question with an injected fake model and no network or external effects. The initial exploratory checker recorded **4 of 7** passing checks for the skill-guided draft and **5 of 7** for the no-skill draft. Some failures exposed an under-specified checker contract, including success-status spelling and malformed-input exit behavior.

That exploratory record was not reclassified as passing. A second, explicitly specified request fixed those shared grading obligations before generation. Each fresh draft then passed **7 of 7** independent local checks: its generated unit suite, current evidence, missing evidence, superseded-only evidence, conflicting evidence, injection-text handling, and malformed input. Source imports and dynamic/file access were inspected before execution, and commands ran with a sanitized environment, a timeout, and fresh local artifacts. This is constrained source inspection, not an OS-level adversarial sandbox.

Both final drafts passed the same small check set, so **no skill-related performance uplift was established**. The generated example is a fixed-workflow, agent-shaped prototype, not proof of adaptive-agent value or production-grade behavior. Planning, coding, safety, evaluation quality, cleanup, and release behavior across realistic problems require much broader independent evidence.

The raw selection observations and prototype execution summaries are in [evidence/](evidence/README.md). They contain only synthetic inputs and do not include production data, credentials, or a live deployment.

## Remaining promotion obligations

Before admitting this library for unattended production development, run fresh native-host trials with the exact host/model/version, visible package inventory, permission configuration, approved isolated workspace, profile, tools, and checker revisions recorded. Test actual selection and loading separately from execution adherence, including collisions with the legacy `review-agent-readiness` name, missing resources, denial paths, injected source material, context growth, and stale identity.

Use multiple realistic problem classes and models, a credible no-skill baseline and fixed generic planning/verification baseline, independently retained holdouts, predeclared stopping and repair rules, raw failure/invalid/inconclusive denominators, and independent end-state assertions. Evaluate alternative stacks and conditional tools, data, retrieval, durable effects, approvals, multi-agent coordination, operating controls, and rollback only when their triggers apply.

A passing local suite or matching ZIP does not establish complete conformance, publisher authenticity, truthful evidence, runtime isolation, live-service authority, approved risk, safe deployment, or guaranteed quality. The library remains **proposed**, with readiness recommendations permanently separate from accountable external authorization.

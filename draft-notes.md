# Draft notes and review boundaries

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted  
**Purpose:** Record provenance, migration, draft policy proposals, unresolved adoption decisions, and the limits of this integration.  
**Not normative:** Owner chapters and [Applicability](applicability.md) control requirements and triggers.

## Current draft status and scope

The book has **ten Parts and 40 populated draft chapters**. Parts **1–5** are refined draft mini-books. Part 1 retains its four chapter/template planning increment. The earlier increment added the seven Part 2 and three Part 3 local chapter/template units, their overviews, practical-reference indexes, glossary pointers, and shared navigation. This increment adds the three Part 5 local chapter/template units, its overview, practical reference, glossary pointers, and shared navigation. It remains a proposed editorial increment, not an adoption or a claim of organizational conformance.

[Part 4](development-guide/04-testing-and-evaluation/README.md) remains the existing detailed pilot: an unnumbered overview, seven numbered chapters, and an unnumbered practical reference. Parts **6–10** are populated first drafts, **not empty and not reviewed to the Parts 1–5 refinement depth**. The flexible mini-book pattern in the [writing guide](writing-guide.md) has not been imposed on them.

The Parts 1–5 refinements do **not** change canonical requirement wording, IDs, operative strengths, owner paths, applicability, or what conformance means. All 208 canonical groups remain located by the [requirement index](requirement-index.md), which remains a locator rather than a second normative standard. The book is still **proposed, not adopted**.

The legacy `agent-playbook/`, `foundations/`, `multi-agent-playbook/`, and `skills/` directories remain the v0.4 baseline (their Zetra links were removed in the content review). This draft does not declare them conformant with 0.5.0-draft.2 and does not migrate skills.

## Part 4 chapter sequence

The completed canonical Part 4 sequence is [4.1 Foundations, Terms, and Definitions](development-guide/04-testing-and-evaluation/01-foundations-terms-and-definitions.md); [4.2 Test Levels, Techniques, and Suite Purposes](development-guide/04-testing-and-evaluation/02-test-levels-techniques-and-suite-purposes.md); [4.3 Evaluation Types and Dimensions](development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md); [4.4 Evaluators, Metrics, Rubrics, and Calibration](development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md); [4.5 Planning, Designing, and Running Tests and Evaluations](development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md); [4.6 Standards, Required Coverage, and Execution Cadence](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md); and [4.7 Analyzing Results, Comparing Versions, and Making Decisions](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md). The [practical reference](development-guide/04-testing-and-evaluation/reference/README.md) supplies illustrative records and templates but owns no requirements.

## Amended requirement scope

The canonical requirement index retains the prior **204** stable IDs and adds exactly **four** new coverage IDs: `COVERAGE-01` through `COVERAGE-04`, for **208** total. The existing 21 Part 4 semantic IDs remain stable; only their canonical owners and links are clarified.

- [4.1](development-guide/04-testing-and-evaluation/01-foundations-terms-and-definitions.md) and the [practical reference](development-guide/04-testing-and-evaluation/reference/README.md) own no requirements.
- [4.2](development-guide/04-testing-and-evaluation/02-test-levels-techniques-and-suite-purposes.md) owns `CASE-04`.
- [4.3](development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) owns `BEHAVIOR-01` through `BEHAVIOR-05`.
- [4.4](development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) owns `EVALUATOR-01` through `EVALUATOR-05`.
- [4.5](development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md) owns `CASE-02`, `CASE-03`, and `CASE-05`.
- [4.6](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) owns `CASE-01` and `COVERAGE-01` through `COVERAGE-04`.
- [4.7](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) owns `RELEASE-EVIDENCE-01` through `RELEASE-EVIDENCE-06`.

The [requirement index](requirement-index.md) is a deterministic locator generated from canonical `## Requirements` groups. It deliberately links to the owner instead of reproducing a competing normative standard.

## Part 4 policy proposals now explicit

- Every production candidate receives one proportional universal evidence core; additional coverage is independently triggered by the candidate, claim, risk, and proposed exposure. Retrieval does not imply stored memory; routing does not imply a model judge; durable read-only work does not imply approval or an external effect.
- Material semantic/changeable-input or policy, permission, currentness, and user-constraint decisions use reviewed invariance and relevant-change sensitivity evidence when applicable. Material variable user-visible claims retain fresh repeated evidence or a justified alternative that removes variability from the claim.
- A case, fixture, source/state observation, evaluator, metric, trial, physical attempt, selected result, and decision subject are distinct records. Source metadata is not semantic support, and a transcript is not an external-effect observation.
- An independent release holdout remains separately authored and outside reported tuning. Retry, selection, and fallback metrics describe the policy actually released and do not hide physical attempts, effects, costs, or failures.
- Invalid and inconclusive evidence remains visible; a real observable candidate failure is not relabelled invalid. Missing required valid evidence and failed applicable critical controls are non-compensable in an evaluation conclusion. `go`, `conditional_go`, and `no_go` are evaluation conclusions, not deployment authorization.

## Retained organization-specific adoption decisions

This assembled draft intentionally does **not** adopt an organizational exception catalogue; governance-tier role or authority structure; domain thresholds; precision, trial-count, pass-rate, or judge-agreement default; legal classification; retention period; reviewer qualification; fairness metric; pilot/rollout number; or guarded-live authorization process. Accountable owners must still decide those matters for an actual adoption and use the relevant owner chapters to record the decision.

## Part 5 operational and adoption decisions

Part 5 does not adopt user-relevant SLI specifications, SLO targets or observation windows, reliability-error-budget policy, alert conditions, decision owners, response routes, resource dimensions, price or usage sources, reservation rules, in-flight reconciliation, stop scope, stop authority, resumption evidence, staffing model, exception eligibility, rollout thresholds, support route, periodic-review cadence, or copy-specific retention and sanitization rules. These are use-specific operational or adoption decisions for accountable owners under the relevant canonical chapters; they are not defaults created by a filled illustrative packet.

These decisions remain distinct from the existing BOUNDARY-04 ambiguity below. Selecting an operational signal, an authority, a rollout condition, or a data disposition does not decide whether a prohibited embedded instruction needs a separately visible refusal, escalation, or failure when a permitted request can otherwise continue safely.

## Concrete unresolved normative ambiguities

- **BOUNDARY-04 refusal scope:** When untrusted retrieved content embeds a prohibited instruction but a separate, permitted policy question can safely continue, it remains unresolved whether the required refusal, escalation, or failure must be separately visible for the rejected embedded instruction or whether a documented `complete` outcome may preserve the legitimate utility. No resolution is implied here.

## Established example rules and use-specific decisions

- **Equal-authority current-source conflict:** This example rule is already defined: clarify or escalate when two current, equal-authority sources conflict. It is not an unresolved permission to choose by revision date. Any broader organizational source-precedence policy remains a separate adoption decision.
- **Protected-read and target semantics:** A future target owner must decide whether a nominal read has a relevant external effect, its repeat/cancellation/deadline semantics, and the resulting retry classification; a transport or operation name is not that decision.
- **Manifest and authority trust model:** Organizational identities and matching rules for accountable owner, governance tier, risk record, model/budget policy, construction identity, and any required manifest signing or verification remain adoption decisions rather than implications of a digest.
- **Data deletion versus preservation:** The applicable owner must resolve a real conflict between deletion or a deletion request and a preservation, investigation, or audit-integrity need, including copy-specific retention and approved recovery/support destinations.

## Review boundaries, local units, and validation results

The Part 1 work remains recorded as four separately reviewable local chapter/template units: 1.1 with `templates/1.1/problem-brief.yaml`; 1.2 with `templates/1.2/success-criteria.yaml`; 1.3 with `templates/1.3/suitability-decision.yaml`; and 1.4 with `templates/1.4/initial-scope-record.yaml`. Its scoped writer checks were recorded as passed. These are **not** opened pull requests, independent reviews, or changes independent of the unmerged assembled structural base.

The Parts 2 and 3 work is recorded as ten separately reviewable local chapter/template units: 2.1 with `templates/2.1/agent-anatomy-record.yaml`; 2.2 with `templates/2.2/policy-assistant-contract.yaml`; 2.3 with `templates/2.3/instruction-design-record.yaml`; 2.4 with `templates/2.4/tool-contract.yaml`; 2.5 with `templates/2.5/skill-admission-record.yaml`; 2.6 with `templates/2.6/context-source-record.yaml`; 2.7 with `templates/2.7/mcp-integration-record.yaml`; 3.1 with `templates/3.1/authority-boundary-record.yaml`; 3.2 with `templates/3.2/content-action-boundary-record.yaml`; and 3.3 with `templates/3.3/data-handling-audit-record.yaml`. Each scoped writer gate was reported as passed. They are local proposed edits, **not** opened pull requests, independent reviews, admissions, approvals, deployments, or adoption decisions.

The Part 5 work is recorded as three separately reviewable local chapter/template units: 5.1 with `templates/5.1/operating-control-record.yaml`; 5.2 with `templates/5.2/release-and-rollout-record.yaml`; and 5.3 with `templates/5.3/support-incident-and-retirement-record.yaml`. Each scoped writer gate was reported as passed. They are local proposed edits, **not** opened pull requests, independent reviews, authorizations, deployments, incidents, recoveries, retirements, or adoption decisions.

This integration reused the supplied verified chapter findings and made one targeted navigation/terminology pass. It did not perform another research sweep, a live-agent call, benchmark run, deployment, commit, push, pull request, or skill migration. The shared `POLICY-OPS-001` policy-assistant packet remains fictional, illustrative, and unexecuted. It does not report a production agent result, benchmark result, approval, deployment, or proof of adequacy.

The previous Part 1 and Parts 2–3 histories record earlier documentation-validation results. They are historical context only; they are not final validation results for the Part 5 integration.

**Historical Parts 2–3 documentation validation passed after cleanup and re-testing.** All ten chapter/template gates passed. Combined checks retained 40 populated chapters, 208 single-owner canonical groups, all 55 Part 2–3 normative bullets verbatim, unchanged owner locators, valid local links/fragments and structured examples, and the original compatibility/main-checkout baseline. Part 1 content and Part 4/evaluation templates were unchanged. The pinned repository check passed Markdown lint across 148 files and reported zero offline local-link/fragment errors. Targeted cleanup selected the canonical OWASP output-handling URL and separated the refusal-scope ambiguity from established fixture rules and use-specific decisions without altering conformance.

**Part 5 combined documentation checks passed.** All three chapter/template gates preserve all 18 canonical Part 5 requirement bullets verbatim and every original chapter heading. Whole-book checks retain 40 populated chapters, 208 single-owner canonical groups and unchanged owner locators, valid local links/fragments and structured examples. The three optional packet records share the intended illustrative identity/status and reference the valid development fixture, sources, and cases without reusing the independent holdout. Parts 1–4 and their chapter/reference/template content, other existing Parts, compatibility trees, and the original checkout remain unchanged.

The pinned repository check passed Markdown lint across 149 files and reported zero offline local-link/fragment errors. Targeted cleanup clarifies that an absent actual lifecycle evaluation and a fictional Part 4 handoff are different facts, without changing policy or source claims. Final delivery re-tests the cleaned content and these notes, then packages the portable ZIP with source-byte verification. Documentation validation does not establish external-link availability, actual agent performance, legal/regulatory applicability, or organizational adoption. See [Development progress](development-progress.md) for the next file-by-file queue.

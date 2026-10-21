# Practical Reference — Integrated Example, Templates, and Troubleshooting

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable decision owners  
**Applicability:** Organizing evidence for a bounded agent claim; adapt fields to the agent's contract, capabilities, and decision scope.  
**Reader question:** How do requirements become cases, evidence, and a reviewable decision record?

[Part 4 — Testing and Evaluation](../README.md) · [Planning and running](../05-planning-designing-and-running-tests-and-evaluations.md) · [Required coverage](../06-standards-required-coverage-and-execution-cadence.md) · [Analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md) · [Applicability](../../../applicability.md)

The Part 4 workflow:

1. Write the bounded user-facing and control claims in a coverage plan.
2. Turn each claim into a named case with a controlled fixture, expected terminal outcome, and observable boundary conditions.
3. Choose an evaluator that can establish the narrow claim; source-identity checks, semantic review, and boundary observation answer different questions.
4. Declare the trial and retry policy before reading results, and keep all statuses and physical attempts.
5. Assemble only valid, identified evidence into a decision record, which does not authorize deployment.

Templates and worked example are **fictional teaching material** with no sensitive data, credentials, live endpoints, or executed measurements. The three fresh episodes show record structure only, not an adequate count.

## Shared fictional constants

All pages and templates share one read-only policy-assistant scenario:

- Candidate: `policy-assistant@candidate-current-selection`
- Baseline: `policy-assistant@baseline-current-selection`
- Development fixture: `travel-policy-current@fixture-2026-10-18.1`
- Current approved policy source: `travel-policy-2026@"2026-10-01"`, whose fictional London hotel amount is **GBP 220**
- Superseded source: `travel-policy-2024-superseded@"2024-01-01"`
- Independent release holdout: `policy-release-holdout@v1`, with separately authored case `POLICY-HOLDOUT-009` and its own fixture
- Evaluators: `source-permission-check@v1`, `grounded-policy-human-rubric@v1`, `trajectory-boundary-check@v1`, and `grounding-judge@v1`

The assistant answers only from approved, current, permission-filtered sources with citations. It is ephemeral and read-only (no write, persisted memory, approval, delegated agent, or live operation); these absences describe the example, not a prescribed architecture.

Outcomes are `complete`, `needs_information`, `declined`, and `failed`, plus only a contract-defined partial or escalation outcome; escalation is success only when the case expects it. Neither a missing permitted source nor two conflicting current approved sources justifies an invented amount, and a superseded source is not equal authority.

## Pick an entry point

**Starting an evaluation.** Open the [coverage-plan template](../../../templates/evaluation/coverage-plan.yaml) and pair it with the [case and fixture template](../../../templates/evaluation/case-fixture.yaml). Start from the decision to support, not a generic metric list.

**Choosing a judgment method.** Use the [evaluator record](../../../templates/evaluation/evaluator-record.yaml) with [evaluators, metrics, rubrics, and calibration](../04-evaluators-metrics-rubrics-and-calibration.md). Record what evidence the evaluator may inspect and its limits. Here the model judge is diagnostic-only and qualified human review is the release-facing semantic method.

**Recording variable behavior.** Use the [trial-policy template](../../../templates/evaluation/trial-policy.yaml). A trial is one fresh, identified episode, not a selected attractive transcript; keep fixed sources, variants, reset checks, statuses, attempts, and final results distinct.

**Preparing a release conclusion.** Use the [decision-report template](../../../templates/evaluation/decision-report.yaml) with [analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md). State the decision rule before reviewing outcomes and show evidence gaps instead of averaging them away.

**Seeing the artifacts together.** Read the [policy-assistant worked example](policy-assistant-worked-example.md). It runs from a bounded contract through all nine cases to an initial `no_go` and a contingent later `go`.

**Diagnosing a confusing result.** See [troubleshooting](troubleshooting.md) for symptoms such as a better score with worse user reports, unsupported answers that a judge passes, or retries that hide first-attempt failures.

## Pack conventions

Case, fixture, source revision, evaluator, candidate, and trial policy are separate records. A fixture supplies the starting world, a source record the approved text and permission/currentness facts, and an evaluator interprets designated evidence; a citation or transcript is no shortcut for all three.

A complete current-policy answer needs the permitted current source and GBP 220 in any acceptable wording. The path is constrained, not literal: retrieval observes requester scope, only permitted sources support the answer, no write occurs, and the episode ends within its bound.

`POLICY-HOLDOUT-009` stays apart from tuning: a newly authored task with its own fixture, not a renamed development case. A production signal becomes a versioned regression case only after sanitizing and review.

## Reusable files

- [Coverage plan](../../../templates/evaluation/coverage-plan.yaml): claims, profiles, case coverage, owner, decision role, and scoped non-applicability.
- [Case and fixture specification](../../../templates/evaluation/case-fixture.yaml): controlled sources, permissions, all nine cases, expected outcomes, reset, and authoritative observations.
- [Evaluator record](../../../templates/evaluation/evaluator-record.yaml): claim-to-method fit, rubric provenance, self-tests, human review, and diagnostic judge limits.
- [Trial policy](../../../templates/evaluation/trial-policy.yaml): fresh-episode unit, variants, reset, attempt accounting, and invalid/inconclusive handling.
- [Decision report](../../../templates/evaluation/decision-report.yaml): subject provenance, evidence inventory, gates, fictional decision examples, limitations, and next actions.

Templates are a starting structure; an unfilled field is not complete. The owner still decides domain thresholds, reviewer qualifications, acceptable uncertainty, exceptions, and any guarded-live scope.

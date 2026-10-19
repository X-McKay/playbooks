# Practical Reference — Integrated Example, Templates, and Troubleshooting

**Status:** 0.5.0-draft.2 assembled draft — fictional, illustrative, and unexecuted
**Audience:** Builders, evaluators, reviewers, and accountable decision owners  
**Applicability:** Use these artifacts to organize evidence for a bounded agent claim. Adapt the fields to the agent's contract, enabled capabilities, and decision scope.  
**Reader question:** How do requirements become cases, evidence, and a reviewable decision record?

[Part 4 — Testing and Evaluation](../README.md) · [Planning and running](../05-planning-designing-and-running-tests-and-evaluations.md) · [Required coverage](../06-standards-required-coverage-and-execution-cadence.md) · [Analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md) · [Applicability](../../../applicability.md)

This pack is a practical route through the Part 4 workflow:

1. Write the bounded user-facing and control claims in a coverage plan.
2. Turn each claim into a named case with a controlled fixture, expected terminal outcome, and observable boundary conditions.
3. Choose an evaluator that can establish the narrow claim. A source-identity check, a semantic review, and a boundary observation answer different questions.
4. Declare the trial and retry policy before results are read, then preserve all statuses and physical attempts.
5. Assemble only valid, identified evidence into a decision record. A decision conclusion does not authorize deployment.

The templates and the worked example are **fictional teaching material**. They contain no sensitive data, credentials, live endpoints, executed measurements, or evidence that an agent is adequate. An illustrative count of three fresh episodes appears only to show record structure; it is not an adequate count, a universal minimum, or a claim about reliability.

## Shared fictional constants

The pages and templates use one intentionally small, read-only policy-assistant scenario:

- Candidate: `policy-assistant@candidate-current-selection`
- Baseline: `policy-assistant@baseline-current-selection`
- Development fixture: `travel-policy-current@fixture-2026-10-18.1`
- Current approved policy source: `travel-policy-2026@"2026-10-01"`, whose fictional London hotel amount is **GBP 220**
- Superseded source: `travel-policy-2024-superseded@"2024-01-01"`
- Independent release holdout: `policy-release-holdout@v1`, with separately authored case `POLICY-HOLDOUT-009` and its own fixture
- Evaluators: `source-permission-check@v1`, `grounded-policy-human-rubric@v1`, `trajectory-boundary-check@v1`, and `grounding-judge@v1`

The assistant answers only from approved, current, permission-filtered sources and returns citations. It is ephemeral and read-only: it has no external write, persisted memory, approval, delegated-agent, or live-operation capability. Those absences are scoped facts about this example, not a general architecture prescription.

Its contract-defined outcomes are `complete`, `needs_information`, `declined`, and `failed`, plus only a contract-defined partial or escalation outcome. An escalation counts as successful only when the case expects it. A missing permitted source or two current approved sources that conflict therefore cannot justify an invented definitive amount. A superseded conflicting source is not equal authority to a current approved one.

## Pick an entry point

**Starting an evaluation.** Open the [coverage-plan template](../../../templates/evaluation/coverage-plan.yaml), then pair it with the [case and fixture template](../../../templates/evaluation/case-fixture.yaml). Start from the decision a reader needs to support rather than from a generic metric list.

**Choosing a judgment method.** Use the [evaluator record](../../../templates/evaluation/evaluator-record.yaml) with [evaluators, metrics, rubrics, and calibration](../04-evaluators-metrics-rubrics-and-calibration.md). Record the evidence an evaluator is allowed to inspect and its limits. A model judge in this pack is diagnostic-only; qualified human review is the release-facing semantic method.

**Recording variable behavior.** Use the [trial-policy template](../../../templates/evaluation/trial-policy.yaml). A trial is one fresh, identified episode, not a selected attractive transcript. Keep fixed sources, variants, reset checks, statuses, physical attempts, and final policy results distinct.

**Preparing a release conclusion.** Use the [decision-report template](../../../templates/evaluation/decision-report.yaml) alongside [analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md). State the decision rule before reviewing outcomes and make evidence gaps visible rather than averaging them away.

**Seeing the artifacts work together.** Read the [policy-assistant worked example](policy-assistant-worked-example.md). It walks from a bounded contract through all nine shared cases to a fictional initial `no_go` and a strictly contingent later fictional `go`.

**Diagnosing a confusing result.** Consult [troubleshooting](troubleshooting.md) for symptoms such as an improved score with worse user reports, unsupported answers that a judge passes, or retries that hide first-attempt failures.

## Pack conventions

Keep identities precise. A case, fixture, source revision, evaluator, candidate, and trial policy are separate records. A fixture supplies the controlled starting world; a source record supplies approved source text and permission/currentness facts; an evaluator interprets designated evidence. Do not use an answer citation or transcript as a shortcut for all three.

For this scenario, a complete answer to the current-policy case needs the permitted current source and GBP 220. It can use different acceptable wording. The expected path is intentionally constrained rather than literal: protected retrieval observes the requester scope, only permitted sources can support the answer, no write is invoked, and the episode terminates within its declared bound. This makes room for safe alternatives while preserving the boundaries that matter.

Keep the holdout separate from development and regression tuning. `POLICY-HOLDOUT-009` is a new authored task with a separate fixture—not one of the eight development cases renamed after the fact. If a real production signal later becomes a case, sanitize and review it before adding a new versioned regression record.

## Reusable files

- [Coverage plan](../../../templates/evaluation/coverage-plan.yaml): claims, profiles, case coverage, owner, decision role, and scoped non-applicability.
- [Case and fixture specification](../../../templates/evaluation/case-fixture.yaml): controlled sources, permissions, all nine cases, expected outcomes, reset, and authoritative observations.
- [Evaluator record](../../../templates/evaluation/evaluator-record.yaml): claim-to-method fit, rubric provenance, self-tests, human review, and diagnostic judge limits.
- [Trial policy](../../../templates/evaluation/trial-policy.yaml): fresh-episode unit, variants, reset, attempt accounting, and invalid/inconclusive handling.
- [Decision report](../../../templates/evaluation/decision-report.yaml): subject provenance, evidence inventory, gates, fictional decision examples, limitations, and next actions.

Use the templates as a starting structure, not as proof that an unfilled field is complete. The accountable owner still decides domain-specific thresholds, reviewer qualifications, acceptable uncertainty, exceptions, and any guarded live scope.

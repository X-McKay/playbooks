# 4.7 Analyzing Results, Comparing Versions, and Making Decisions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, accountable owners, and release reviewers  
**Applicability:** A candidate or material change whose behavior, evidence, route, operating limits, or decision posture could change.  
**Reader question:** What does the evidence justify us doing next?

[Part 4 — Testing and Evaluation](README.md) · [Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md) · [Part 5 readiness and rollout](../05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)

A release comparison is an argument about **one identified candidate**, not a dashboard of nearby successful runs. A higher aggregate can hide a critical-slice regression; a favorable transcript can hide an invalid fixture, unsafe retry, or missing evidence. This chapter turns coverage evidence into a defensible `go`, `conditional_go`, or `no_go`; it sets no universal thresholds and authorizes no deployment.

## Start with a decision subject, not an aggregate

Freeze the subject before comparing, as RELEASE-EVIDENCE-01 lists; the resolved configuration includes instructions, admitted capabilities, source and permission policy, route or fallback policy, settings, and evaluation environment. A mutable label such as "current policy assistant", or a model label alone when routing or configuration changes behavior, cannot reproduce a decision. Each physical attempt and the user-facing result must trace to the configuration that produced it.

Read results at four levels:

- **Case:** Did the declared outcome and invariants hold? Keep outcome, evidence pointers, status, and reason per attempt.
- **Claim and critical slice:** Were the material currentness, permission, grounding, injection, or other slices covered? Improved common cases do not make a critical slice safe.
- **Candidate versus baseline:** On the same semantic case and run rules, which outcomes flipped? Inspect meaningful flips instead of inferring a cause from a pooled difference.
- **Decision:** Are gates, coverage, valid evidence, task metrics, operating constraints, and limits all accounted for under the predeclared rule?

A first release without a baseline still needs an identified candidate, applicable hard gates, and decision-grade absolute evidence; "no baseline" lowers no gate. When a result is surprising, read the transcripts first: a flip may come from a grader error, invalid fixture, or ambiguous case. Keep the status honest either way.

## Measure the product that is actually released

A repeated-run metric means something only when its unit and denominator match the claim. A success is the **correct contract outcome plus every applicable observable invariant**; repeatable wrong answers, blanket refusal of permitted work, or a correct final sentence after a prohibited invocation are not reliable success.

### Keep the three common pass measures distinct

**First-attempt success** (`pass@1`, also `pass^1`) is the share of fresh physical attempts that pass first time, closest to a one-attempt released policy. Its denominator says which attempts started, which got a valid judgment, and how invalid or inconclusive statuses (never passes) are treated.

**At-least-one-of-k success** (`pass@k`) asks whether any of `k` attempts succeeds. It fits only if the product really makes those attempts (discovery, or a read-only retry/selection policy) and can safely select the result; otherwise it makes a fragile first attempt look strong. Under an explicitly justified independent, same-probability trial model it is `1 − (1 − p)^k`; the formula is no reason to assume independence or invent a `k`.[1]

**All-k success** (`pass^k`) asks whether all `k` attempts succeed, for an all-attempt consistency claim. One rewards at least one success; the other allows no failure. A 75% per-trial rate gives about 42% `pass^3` under the independent model, so consistency can look much weaker than single-attempt rates. τ-bench defines both for its repeated-trial setting, with no universal threshold or population reliability estimate.[1]

Report each separately with numerator, denominator, units, and status handling; never rename a selected second attempt as a one-attempt pass.

### Bind metrics to retry, selection, and fallback behavior

Evaluate the released policy end to end, not an idealized single call. If it retries, samples, votes, routes, falls back, or chooses a response, record:

- retry or fallback eligibility, cap, and stop condition;
- reset, isolation, and any idempotency, authorization, approval, or state-reconciliation preconditions that make a repeat safe;
- every physical attempt with its outcome, boundary observations, retry reason, latency, resource use, and cost;
- the selection rule and the final result delivered; and
- invocation, effect, disclosure, and authoritative-state evidence.

A failed attempt can consume budget, disclose information, invoke a boundary, or leave an uncertain effect even when a later one succeeds. After an ambiguous external effect, reconcile against authoritative state before any repeat. A bounded read-only retry is safe only if the policy declares eligibility and exhaustion behavior. Keep cost, latency, calls, safe exhaustion, and final outcome separate; a good selected answer does not erase earlier costs or failures.

## Compare fairly and describe what the evidence can support

Pair candidate and baseline per case or episode under identical cases, variants, fixture rules, permission context, evaluator rules, and trial policy, so each flip is visible. Safe alternative trajectories that meet the same invariants stay comparable; never require literal transcript matches.

Repeated attempts within a case often share difficulty, fixture state, a service incident, route, cache, or time window, so treat them as a **case cluster**, not independent observations. To generalize beyond the named cases, predeclare population, case frame or strata, sampling and weighting, comparison unit, dependence treatment, uncertainty method, and needed precision; treat cases as a sample and report standard errors or intervals, not a bare pass rate.[4] McNemar's paired test fits only when its independent-pairs assumption holds for the declared unit; it does not make correlated retries independent.[2]

A curated regression, adverse, or critical-control suite is indispensable for known hazards and gates but is **not** a sample of all users, requests, or future conditions; report it as evidence on that suite and protocol. For small counts, normal-approximation intervals for a proportion can be inaccurate; use Wilson or exact binomial intervals,[3] remembering they assume independent trials and do not repair a nonrepresentative or clustered design.

Zero observed failures are evidence with limits, not proof of zero risk. If the inference needs independent trials, say why that is credible; otherwise keep a bounded case-and-protocol conclusion or use a cluster-aware method. The owner picks thresholds, precision, and trial count.

## Classify evidence honestly before deciding

A **valid pass** or **valid candidate failure** comes from an execution where the predeclared subject, case, fixture/reset, observation, and evaluator all worked. **Invalid** means a declared condition prevented attribution to the candidate. **Inconclusive** means a validly recorded execution did not establish the claim, such as unresolved qualified-review disagreement. **Missing required valid evidence** is a decision-state finding: required evidence was not obtained by the decision point.

Invalid and inconclusive records stay visible and never quietly improve a denominator. An independently observable candidate failure (unsafe action, disclosure, enforcement bypass, task failure) stays attributable even when a dashboard, fixture, or evaluator problem is found too.

A repaired or replacement run counts only under RELEASE-EVIDENCE-04's predeclared repair rule. If the repair materially changes the fixture, rubric, evaluator, or trial policy, re-establish comparison validity rather than treating a favorable replacement as directly comparable. A repaired run does not cure a different missing evidence type.

## Turn the record into a conclusion

The decision policy separates three roles before results are read:

- **Must-pass control gates** are non-compensable boundaries, such as an applicable authorization, isolation, stop, required-valid-evidence, or prohibited-use claim.
- **Task metrics and operating constraints** measure declared quality, cost, latency, completion, or allowed regression for specified cases and slices.
- **Diagnostics** help investigate or prioritize but support no release gate until fitness for that exact claim is established; a diagnostic-only model judge stays so even with a favorable score.

`go` means the policy is satisfied and the evidence supports moving to the separate readiness and rollout decision. `no_go` means a hard gate, required coverage, required valid evidence, or declared threshold was not met; it is an evidence conclusion, not a verdict on the work's value, so repair and regenerate the affected evidence.

`conditional_go` is narrow: only where the governing policy permits it and every required pre-release control and evidence item is complete. It may track a permitted post-release obligation with an owner, due date, monitoring signal, and overdue consequence, but never defers a safety, grounding, authorization, critical-slice, or other launch prerequisite. A condition that would supply missing pre-release evidence is a blocker and means `no_go`.

Part 5 separately decides operational readiness, residual-risk acceptance where applicable, rollout, monitoring, and rollback; an evaluation `go` is not deployment permission.

## Worked example: a fictional evidence-gap decision

This walkthrough is **fictional**; it reports no executed benchmark, measured rate, or live result.

`policy-assistant@candidate-current-selection` is compared with `policy-assistant@baseline-current-selection`, both ephemeral and read-only. Fixture `travel-policy-current` at `fixture-2026-10-18.1` holds current `travel-policy-2026`, revision `2026-10-01` (GBP 220), with `travel-policy-2024-superseded` present to test currentness. The record names `POLICY-CURRENT-001` through `POLICY-EXHAUSTION-008` and, separately, the independently authored `policy-release-holdout@v1` with `POLICY-HOLDOUT-009`. Claim-facing evaluators are `source-permission-check@v1`, `grounded-policy-human-rubric@v1`, and `trajectory-boundary-check@v1`; `grounding-judge@v1` stays diagnostic-only until gate fitness is documented.

The released policy makes **one attempt** (no retry, selection, or fallback), so first-attempt and final delivered-policy success are the same unit, and `pass@k` would not describe it. An illustrative plan of three fresh attempts (not an adequate count) records reset verification, attempts, statuses, per-attempt resource use, and the delivered outcome. A later retry or fallback would first need defined eligibility, cap, selection, costs, and end-to-end result.

The decision record marks `grounded-policy-human-rubric@v1` as **missing required valid evidence** for semantic support. A favorable permission check or judge score cannot fill the gap, so the conclusion is `no_go — insufficient required valid evidence`, asserting no pass or failure rate. A `conditional_go` cannot postpone the missing reviews; only a later record with the required semantic reviews, critical-slice coverage, and other predeclared evidence could support a new conclusion.

Suppose a `grounding-judge@v1` run is marked invalid because its evidence packet omitted the current document revision. The original record stays visible; a corrected replacement may run only under the predeclared repair rule, and even then cannot replace the missing human-rubric evidence. If `POLICY-INJECTION-006` later yields independently observable candidate failure evidence, it stays a candidate failure despite the defective judge packet.

## Evidence and checklist

- [ ] Each metric matches the actual retry, selection, or fallback policy.
- [ ] Costs, boundary observations, and effects are not hidden by a selected retry.
- [ ] Surprising results were checked against transcripts for grader or fixture error.

## Requirements

- **RELEASE-EVIDENCE-01 — Evaluation subject and provenance.** When a candidate is considered for pilot, release, or material expansion, the accountable evaluation owner **MUST** record the exact candidate and baseline, or a first-release rationale; the resolved effective configuration, including applicable route/fallback identity; case, holdout, fixture, evaluator, and rubric versions; trial policy; resolution time; and case-level evidence needed to reproduce the decision. The record **MUST** distinguish physical-attempt and final-policy-result units, metric identity, fixed and varying sources, reset/isolation condition, and every run status. This applies to every behavior-affecting change and first release. Evidence is an attributable decision record linked to identified executions.

- **RELEASE-EVIDENCE-02 — Comparable trials, metrics, and uncertainty.** When variability, retry/selection/fallback behavior, a candidate/baseline comparison, or an inference beyond named curated cases is relevant, the evaluation owner **MUST** predeclare the pass predicate; denominator and status handling; physical-attempt and final-policy units; retry, selection, routing, and fallback policy; fixed/varying sources; reset; paired comparison unit; and uncertainty method with its sampling and dependence assumptions. The report **MUST** use the same applicable cases, fixture rules, and trial rules for candidate and baseline; expose meaningful paired flips; and separately label first-attempt success, `pass@k`, `pass^k`, and final-policy success whenever used. It **MUST NOT** treat within-case repeats as independent population observations without a justified design. This applies only where its stated trigger is present; an absent trigger **MUST** have a documented decision-specific rationale. Evidence is the predeclared policy, complete attempt ledger, paired case record, and uncertainty/sampling rationale.

- **RELEASE-EVIDENCE-03 — Predeclared decision policy.** Before interpreting candidate results, the accountable evaluation owner **MUST** record applicable must-pass gates, required coverage and critical slices, task thresholds or permitted regression rules, operating constraints, invalid/inconclusive and missing-evidence treatment, sample-size or precision rationale when an inference requires one, and decision authority. The policy **MUST** distinguish control gates, task metrics, and diagnostics, and **SHOULD** state evaluator-fitness limits relevant to each release-facing claim. Evidence is a dated decision policy associated with the candidate comparison before result interpretation.

- **RELEASE-EVIDENCE-04 — Valid and non-compensable evidence.** A candidate **MUST** receive `no_go` when an applicable non-waivable gate or prohibited-use rule fails, required coverage is absent, or sufficient valid evidence required by the declared policy is missing or inconclusive at decision time. A favorable average, noncritical slice, diagnostic, or eligible exception **MUST NOT** compensate for those conditions. An invalid or inconclusive record **MUST** remain visible and cannot count as a pass. A repaired or replacement harness run **MAY** contribute valid evidence only under a predeclared rule that fixes candidate and semantic case purpose, retains the original record, records repair and non-bias rationale, makes no input-scope or threshold/invariant relaxation, and repeats all affected paired evidence. An attributable candidate failure **MUST NOT** be relabelled invalid. Evidence is the status ledger, repair record where applicable, and decision disposition.

- **RELEASE-EVIDENCE-05 — Recorded decision and conditions.** Each evaluation conclusion **MUST** record `go`, `conditional_go`, or `no_go`; the rationale; evidence reviewed; known limitations; accountable decision authority; and required next action. `conditional_go` **MAY** be used only when the governing policy permits it and all required pre-release evidence and controls are complete. It **MUST** separately identify pre-release blockers from permitted post-release obligations; each such obligation **MUST** have an owner, due date, monitoring signal, and overdue consequence, and **MUST NOT** replace missing pre-release evidence. The conclusion **MUST NOT** be represented as deployment authorization. Evidence is the signed or otherwise accountable decision record and its Part 5 handoff.

- **RELEASE-EVIDENCE-06 — Attributed production regression loop.** When a production signal indicates a possible behavior or control failure, the responsible team **MUST** preserve privacy-appropriate attributable evidence and review it before using it as evaluation evidence. A confirmed failure **MUST** be sanitized as needed, classified with its relevant claim/risk tags, converted into a versioned regression case with expected outcome or invariant, and included in future applicable comparisons. A noisy alert, raw unreviewed transcript, or telemetry gap **MUST NOT** silently become a confirmed regression or release gate. Evidence is the attribution and review record, sanitized regression case, and subsequent applicable comparison reference.

## References

[1]: https://arxiv.org/html/2406.12045v1 "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"

[2]: https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/mcnemar.htm "NIST McNemar Test"

[3]: https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm "NIST Confidence Intervals for Proportions"

[4]: https://arxiv.org/abs/2411.00640 "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations"

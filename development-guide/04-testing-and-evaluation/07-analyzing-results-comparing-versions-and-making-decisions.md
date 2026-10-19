# 4.7 Analyzing Results, Comparing Versions, and Making Decisions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, accountable owners, and release reviewers  
**Applicability:** A candidate or material change whose behavior, evidence, route, operating limits, or decision posture could change.  
**Reader question:** What does the evidence justify us doing next?

[Part 4 — Testing and Evaluation](README.md) · [Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md) · [Part 5 readiness and rollout](../05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)

A release comparison is an argument about **one identified candidate**, not a dashboard of nearby successful runs. It asks whether the evidence is enough for the decision policy that applies. A higher aggregate can hide a serious regression in a critical slice; a favorable transcript can hide an invalid fixture, an unsafe retry, or missing evidence for a required claim.

This chapter reads the records made in the planning, coverage, behavior, and evaluator chapters. It sets no business goals or universal thresholds and authorizes no deployment. The coverage map says which claims and profiles apply; this chapter turns their evidence into a defensible `go`, `conditional_go`, or `no_go`.

## Start with a decision subject, not an aggregate

Before comparing results, freeze the subject. Record the candidate identity and its resolved configuration: instructions, admitted capabilities, source and permission policy, route or fallback policy, relevant settings, and evaluation environment. Identify the baseline equally carefully, or say why a first release has none. Also identify the exact case and holdout sets, fixture revision, evaluator and rubric versions, trial policy, and the time those identities were resolved.

A mutable label such as "current policy assistant" cannot reproduce a decision. Nor can a model label alone when routing, fallback, source selection, or policy configuration changes behavior. A reviewer should be able to tell which candidate produced each physical attempt and which configuration produced the user-facing result.

Read results at several levels:

- **Case:** Did the declared terminal outcome and observable invariants hold? Keep the outcome, evidence pointers, status, and reason for each attempt.
- **Claim and critical slice:** Did the evidence cover the currentness, permission, grounding, injection, or other slices the contract and risk record make material? A critical slice is not safe because common cases improved.
- **Candidate versus baseline:** On the same semantic case and run rules, which outcomes changed direction? Inspect meaningful flips instead of inferring a cause from a pooled difference.
- **Decision:** Are hard gates, required coverage, valid evidence, task metrics, operating constraints, and known limits all accounted for under the rule declared before results were read?

A first release may lack a baseline, but it still needs an identified candidate, applicable hard gates, and decision-grade absolute evidence. "No baseline" does not excuse the comparison record or lower an applicable gate.

When a result is surprising, read the transcripts before deciding. A flip may come from a grader error, an invalid fixture, or an ambiguous case rather than the candidate. Keep the status honest either way.

## Measure the product that is actually released

A repeated-run metric means something only when its unit and denominator match the claim. Define a success as the **correct contract outcome plus every applicable observable invariant**. Repeatable wrong answers, blanket refusal of permitted work, or a correct final sentence after a prohibited invocation are not reliable success.

### Keep the three common pass measures distinct

**First-attempt success** (`pass@1`, also written `pass^1`) is the share of fresh physical attempts that pass on the first attempt. It is closest to the experience of a released policy that makes one attempt. Its denominator must say which attempts started, which got a valid judgment, and how invalid or inconclusive statuses are treated; neither is a pass.

**At-least-one-of-k success** (`pass@k`) asks whether one or more of `k` attempts succeeds. It fits a real discovery opportunity or a released read-only retry/selection policy, but only if the product makes those attempts and can safely select the result. It can make a fragile first attempt look strong. Under an explicitly justified independent, same-probability trial model it is `1 − (1 − p)^k`; that formula is no reason to assume independence or to invent a `k`.[1]

**All-k success** (`pass^k`) asks whether every attempt in a group of `k` succeeds. It suits an all-attempt consistency claim. It is not interchangeable with `pass@k`: one rewards at least one success, the other allows no failure. For example, a 75% per-trial success rate gives about 42% for `pass^3` under the independent model, so consistency claims can look much weaker than single-attempt rates. τ-bench defines both measures for its repeated-trial setting; its definitions set no universal threshold and give no population reliability estimate.[1]

Report these separately whenever relevant. State the case-level numerator and denominator, the physical-attempt unit, the final-policy-result unit, and the status handling. Do not rename a selected second attempt as a one-attempt pass.

### Bind metrics to retry, selection, and fallback behavior

Evaluate the released policy end to end, not an idealized single call. If it retries, samples candidates, votes, routes, falls back, or chooses a response, record:

- eligibility for a retry or fallback, its cap and stop condition;
- reset, isolation, and any idempotency, authorization, approval, or state-reconciliation preconditions that make a repeat safe;
- every physical attempt and its outcome, boundary observations, retry reason, latency, resource use, and cost;
- the selection rule and the final result delivered; and
- invocation, effect, disclosure, and authoritative-state evidence.

A failed attempt can consume budget, disclose information, invoke a boundary, or leave an uncertain effect even when a later attempt gives a good answer. For an external effect with an ambiguous result, a blind repeat is no evidence the effect was absent or harmless; reconcile against authoritative state first. For a read-only timeout, a bounded retry is safe only if the declared policy says when it is eligible and what happens after exhaustion.

Keep cost, latency, calls, safe exhaustion, and final task outcome separate. A quality score does not show the candidate stayed within an operating limit, and a good selected answer does not erase the costs or failures before it.

## Compare fairly and describe what the evidence can support

Pair candidate and baseline on the same identified cases, semantic variants, fixture rules, permission context, evaluator rules, and trial policy. Pair at the case or episode level so a reviewer sees the direction of each meaningful flip. Safe alternative trajectories stay comparable when they meet the same declared outcome and path invariants; do not require a literal transcript match to simplify aggregation.

Repeated attempts within a case often share case difficulty, fixture state, a service incident, a route, a cache, or a time window. Treat them as a **case cluster**, not as independent observations. To compare candidates beyond the named cases, predeclare in the decision record the inference population, case frame or strata, sampling and weighting, comparison unit, dependence treatment, uncertainty method, and the precision or detectable regression you need. Treat the cases as a sample of a larger set of possible cases and report uncertainty, such as standard errors or intervals, rather than a bare pass rate.[4] A paired binary method such as McNemar's test fits only when its independent-pairs assumption holds for the declared unit; it does not make correlated retries independent.[2]

A curated regression, adverse, or critical-control suite is indispensable for known hazards and gates. It is **not** a sample of all users, requests, or future conditions. Describe its result as evidence on the identified suite and protocol. A population estimate needs a defensible sampling frame, coverage rationale, and uncertainty treatment. For small counts, normal-approximation intervals for a proportion can be inaccurate; use Wilson or exact binomial intervals.[3] These intervals assume independent trials, so they do not repair a nonrepresentative or clustered design.

Zero observed failures are evidence with limits, not proof of zero risk. If the inference depends on independent trials, say why that is credible. If not, keep a bounded case-and-protocol conclusion or use a method that respects the clustering. The accountable owner, not this playbook, picks thresholds, precision, trial count, and the decision use that justify the sampling effort.

## Classify evidence honestly before deciding

Use visibly distinct statuses. A **valid pass** or **valid candidate failure** comes from an execution where the predeclared subject, case, fixture/reset, observation, and evaluator were available and worked as required. **Invalid** means a declared condition prevented attribution to the candidate. **Inconclusive** means a validly recorded execution did not establish the claim, such as unresolved qualified-review disagreement. **Missing required valid evidence** is a decision-state finding: the evidence the policy requires was not obtained by the decision point.

An invalid or inconclusive record stays visible. It is not a pass and must not quietly improve a denominator. Likewise, an independently observable candidate failure stays attributable when a dashboard, fixture, or evaluator problem is found later. Do not relabel an unsafe action, disclosure, enforcement bypass, or task failure as invalid because another part of the harness also failed.

A repaired or replacement run can contribute valid evidence only under a predeclared repair rule. Keep the candidate identity and semantic case purpose fixed; keep the original invalid record; record the repair and why it cannot bias the result; do not narrow inputs or relax an invariant, threshold, or gate; and repeat all affected paired evidence under the repaired rule. If the repair materially changes the fixture, rubric, evaluator, or trial policy, re-establish comparison validity instead of treating a favorable replacement as directly comparable. A repaired run does not cure another missing evidence type.

## Turn the record into a conclusion

A decision policy separates three roles before results are read:

- **Must-pass control gates** are non-compensable boundaries, such as an applicable authorization, isolation, stop, required-valid-evidence, or prohibited-use claim.
- **Task metrics and operating constraints** measure declared quality, cost, latency, completion, or allowed regression for specified cases and slices.
- **Diagnostics** help investigate or prioritize but do not support a release gate until their fitness for that exact claim is established. A diagnostic-only model judge stays diagnostic-only even when its score is favorable.

`go` means the evaluation policy is satisfied and the evidence supports moving to the separate readiness and rollout decision. `no_go` means an applicable hard gate, required coverage, required valid evidence, or declared threshold was not met. It is an evidence conclusion, not a verdict that the work has no value: repair the candidate or evaluation and regenerate the affected evidence.

`conditional_go` is narrow. Use it only when the governing policy permits it and every required pre-release control and evidence item is complete. It may track a permitted post-release obligation only when that obligation has an owner, due date, monitoring signal, and overdue consequence. It cannot defer a required safety, grounding, authorization, critical-slice, or other launch prerequisite. A condition that supplies missing pre-release evidence is a blocker and leads to `no_go`.

Put the conclusion, its limits, and its next action in the decision record. Part 5 separately decides operational readiness, acceptance of residual risk where applicable, rollout, monitoring, and rollback. An evaluation `go` is not deployment permission.

## Worked example: a fictional evidence-gap decision

This walkthrough is **fictional**; it reports no executed benchmark, measured rate, or live result.

The subject is `policy-assistant@candidate-current-selection`, compared with `policy-assistant@baseline-current-selection`. Both are the ephemeral, read-only policy assistant: they answer from approved current permission-filtered sources with citations, with no writes, persisted memory, approval flow, or delegated agents. The fixture is `travel-policy-current` at revision `fixture-2026-10-18.1`. The current permitted document is `travel-policy-2026`, revision `2026-10-01`, with fixture value GBP 220; `travel-policy-2024-superseded` stays present to test currentness.

The comparison record names `POLICY-CURRENT-001`, `POLICY-STALE-002`, `POLICY-MISSING-003`, `POLICY-CONFLICT-004`, `POLICY-DENIED-005`, `POLICY-INJECTION-006`, `POLICY-PARAPHRASE-007`, and `POLICY-EXHAUSTION-008`, and separately names `policy-release-holdout@v1` with `POLICY-HOLDOUT-009`. The holdout is independently authored, not an existing case relabelled after tuning. It records `source-permission-check@v1`, `grounded-policy-human-rubric@v1`, and `trajectory-boundary-check@v1` as claim-facing evaluators. `grounding-judge@v1` is diagnostic-only until its gate fitness is documented.

The released policy makes **one attempt**: no retry, multi-candidate selection, or fallback. First-attempt success and final delivered-policy success are therefore the same unit. A trial plan may use three fresh attempts as an illustrative repeated-trial exercise; it asserts no result and does not make three an adequate count. It records reset verification, physical attempts, all statuses, per-attempt resource use, and the final delivered outcome. `pass@k` would not describe this policy; if a read-only retry or fallback were later enabled, the policy would first need to define eligibility, cap, selection, costs, and the end-to-end result.

The fictional decision record marks `grounded-policy-human-rubric@v1` as **missing required valid evidence** for the semantic-support claim. A favorable source-permission check or diagnostic judge score cannot fill that gap. The conclusion is `no_go — insufficient required valid evidence`, without asserting any pass or failure rate.

The record also shows repair visibility. Suppose a `grounding-judge@v1` run is marked invalid because its evidence packet omitted the current document revision. The original record stays visible. Under a predeclared repair rule, a corrected replacement may run only with the same candidate and case purpose, no narrower input or relaxed rule, and affected paired evidence repeated. Even then, the repaired diagnostic run cannot replace the missing human-rubric evidence. If `POLICY-INJECTION-006` or another case later yields independently observable candidate failure evidence, it stays a candidate failure and does not become invalid because the judge packet was also defective.

Only a later decision record with the required valid semantic reviews, critical-slice coverage, and all other predeclared evidence could support a new conclusion. A `conditional_go` cannot postpone the missing semantic reviews.

## Evidence and checklist

Before accepting a decision record, confirm:

- Is the exact candidate distinguishable from the baseline or documented as a first release, including route/fallback and configuration identities?
- Are cases, holdout status, fixture and reset condition, evaluators/rubrics, trial policy, physical attempts, final-policy results, and statuses attributable to that subject?
- Does every metric identify its pass predicate, denominator, first-attempt or all-attempt meaning, and relation to the actual retry, selection, or fallback policy?
- Are outcomes paired where comparison is claimed, and are meaningful case or critical-slice flips visible?
- Does any inference beyond named curated cases state its population, sampling frame, cluster/dependence treatment, uncertainty method, and limits?
- Are cost, latency, calls, boundary observations, effects, and the final delivered result kept, not hidden by a selected retry?
- Are invalid, inconclusive, missing, repaired/replaced, and attributable candidate-failure records distinct, with the repair rule applied without relaxing scope or thresholds?
- Were surprising results checked against transcripts for grader or fixture error?
- Are hard gates, coverage, task metrics, diagnostics, non-applicability conclusions, and permitted exceptions judged under the policy declared before results?
- Does any `conditional_go` leave no required pre-release evidence or control incomplete, and name each post-release obligation's owner, due date, signal, and overdue consequence?
- Does the record name the decision authority, rationale, limits, next action, and handoff to Part 5, without treating the conclusion as deployment approval?

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

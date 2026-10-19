# 4.7 Analyzing Results, Comparing Versions, and Making Decisions

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, accountable owners, and release reviewers  
**Applicability:** A candidate or material change whose behavior, evidence, route, operating limits, or decision posture could change  
**Reader question:** What does the evidence justify us doing next?

[Part 4 — Testing and Evaluation](README.md) · [Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md) · [Part 5 readiness and rollout](../05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)

A release comparison is an argument about **one identified candidate**, not a dashboard assembled from nearby successful runs. It asks whether the available evidence is sufficient for the decision policy that applies to that candidate. A higher aggregate score can conceal a serious regression in a critical slice; a favorable transcript can conceal an invalid fixture, an unsafe retry, or missing evidence for a required claim.

This chapter interprets the records created in the planning, coverage, behavior, and evaluator chapters. It does not select business goals, set universal thresholds, or authorize deployment. The coverage map determines which claims and profiles apply; this chapter explains how their evidence becomes a defensible `go`, `conditional_go`, or `no_go` conclusion.

## Start with a decision subject, not an aggregate

Before comparing results, freeze the subject of the decision. Record the candidate identity and its resolved effective configuration: instructions, admitted capabilities, source and permission policy, route or fallback policy where present, relevant settings, and evaluation environment. Identify the baseline with the same care, or state why a first release has no baseline. Also identify the exact case and holdout sets, fixture revision, evaluator and rubric versions, trial policy, and the time those identities were resolved.

A mutable label such as “current policy assistant” is not enough to reproduce a decision. Nor is a model label alone when routing, fallback, source selection, or a policy configuration changes the behavior being assessed. The evidence record should let a reviewer tell which candidate produced each physical attempt and which configuration produced the user-facing result.

Read results at more than one level:

- **Case level:** Did the declared terminal outcome and applicable observable invariants hold? Preserve the outcome, evidence pointers, status, and reason for each attempt.
- **Claim and critical-slice level:** Did the evidence cover the currentness, permission, grounding, injection, or other slices that the contract and risk record make material? A critical slice does not become safe because common cases improved.
- **Candidate-versus-baseline level:** On the same semantic case and run rules, which outcomes changed direction? Inspect meaningful flips instead of inferring a cause from a pooled difference.
- **Decision level:** Are hard gates, required coverage, valid evidence, task metrics, operating constraints, and known limitations all accounted for under the rule declared before results were read?

A first release may lack a deployed baseline, but it still needs an identified candidate, applicable hard gates, and decision-grade absolute evidence. “No baseline” is not a reason to omit the comparison record or lower an applicable gate.

## Measure the product that is actually released

A repeated-run metric is meaningful only when its unit and denominator match the claim. Define a success as the **correct contract outcome plus every applicable observable invariant**. Repeatable wrong answers, blanket refusal of permitted work, or a correct final sentence after a prohibited invocation are not reliable success.

### Keep the three common pass measures distinct

**First-attempt success** (`pass@1`, also written `pass^1`) is the share of fresh physical attempts that pass on their first attempt. It is the closest measure to the experience of a released policy that makes one attempt. Its denominator must say which attempts were started, which received a valid judgment, and how invalid or inconclusive statuses are treated; neither status is a pass.

**At-least-one-of-k success** (`pass@k`) asks whether one or more of `k` attempts succeeds. It can describe a genuine discovery opportunity or a released read-only retry/selection policy, but only when the product actually makes those attempts and can safely select the result. It can make a fragile first attempt look strong. Under an explicitly justified independent, same-probability trial model, it is `1 − (1 − p)^k`; that mathematical relationship is not a reason to assume attempts are independent or to invent a value for `k`.[1]

**All-k success** (`pass^k`) asks whether every attempt in a group of `k` succeeds. It is useful for an all-attempt consistency claim. It is not interchangeable with `pass@k`: one rewards at least one success and the other requires no failure in the group. The distinction is used by τ-bench for its benchmark-specific repeated-trial setting; its definitions do not establish a universal agent threshold or a population reliability estimate.[1]

Report these metrics separately whenever they are relevant. State the case-level numerator and denominator, the physical-attempt unit, the final-policy-result unit, and the status handling. Do not rename a selected second attempt as a one-attempt pass.

### Bind metrics to retry, selection, and fallback behavior

Evaluate the released policy end to end, not an idealized single call. If it retries, samples candidates, votes, routes, falls back, or chooses a response, record:

- eligibility for a retry or fallback, its cap and stop condition;
- reset, isolation, and any idempotency, authorization, approval, or state-reconciliation preconditions that make a repeat safe;
- every physical attempt and its outcome, boundary observations, retry reason, latency, resource use, and cost;
- the selection rule and the final result delivered to the user or downstream system; and
- applicable invocation, effect, disclosure, and authoritative-state evidence.

A failed attempt can consume budget, disclose information, invoke a boundary, or leave an uncertain effect even when a later attempt produces a good answer. For an external effect with an ambiguous result, a blind repeat is not evidence that the effect was absent or harmless; reconcile against the appropriate authoritative state before another attempt. For a read-only timeout, a bounded retry may be safe only if the declared policy says when it is eligible and what happens after exhaustion.

Keep cost, latency, calls, safe exhaustion, and final task outcome separate. A quality score does not prove that a candidate stayed within a claimed operating limit, and a favorable selected answer does not erase the costs or failures that preceded it.

## Compare fairly and describe what the evidence can support

Pair a candidate and baseline on the same identified cases, semantic variants, fixture rules, permission context, evaluator rules, and applicable trial policy. Pair at the case or episode level so a reviewer can see the direction of each meaningful flip. Safe alternative trajectories remain comparable when they satisfy the same declared outcome and path invariants; a literal transcript match is not required merely to simplify aggregation.

Repeated attempts within a case often share case difficulty, fixture state, a service incident, a route, a cache, or a time window. Treat them as a **case cluster**, not as an arbitrary multiplication of independent observations. When an owner wants to compare candidates beyond the named cases, the decision record should predeclare the inference population, case frame or strata, sampling and weighting approach, comparison unit, dependence treatment, uncertainty method, and the rationale for the precision or detectable regression needed. A paired binary method such as McNemar’s test is appropriate only when its mutually independent-pairs assumption fits the declared unit; it does not make correlated retries independent.[2]

A curated regression, adverse, or critical-control suite is indispensable for known hazards and gates. It is **not** automatically a sample of all users, requests, or future operating conditions. Describe its result as evidence on the identified suite and trial protocol. A population estimate needs a defensible sampling frame, coverage rationale, and uncertainty treatment for that population. NIST similarly cautions that proportion intervals depend on their sampling model; an interval does not repair a nonrepresentative or correlated design.[3]

Zero observed failures are evidence with limits, not proof of zero risk or perfect reliability. If the inference depends on independent trials, say why that assumption is credible. If it does not, retain a bounded case-and-protocol conclusion or use a method that respects the clustering. The accountable owner, rather than this playbook, selects thresholds, precision, trial count, and the decision use that justify the sampling effort.

## Classify evidence honestly before deciding

Use visibly distinct statuses. A **valid pass** or **valid candidate failure** comes from an execution in which the predeclared subject, case, fixture/reset, observation, and evaluator were available and operated as required. An **invalid** status means a declared condition prevented attribution to the candidate. An **inconclusive** status means a validly recorded execution did not establish the claim, such as unresolved qualified-review disagreement. **Missing required valid evidence** is a decision-state finding: the evidence required by the policy has not been obtained by the decision point.

An invalid or inconclusive record stays visible. It is not a pass and must not silently improve a denominator. Equally, an independently observable candidate failure remains attributable when a later dashboard, fixture, or evaluator problem is discovered. Do not relabel an unsafe action, disclosure, enforcement bypass, or task failure as invalid merely because another part of the harness also failed.

A repaired or replacement run can contribute valid evidence only under a predeclared repair rule. Keep the candidate identity and semantic case purpose fixed; retain the original invalid record; record the repair and why it cannot bias the candidate result; do not narrow inputs or relax an invariant, threshold, or gate; and repeat all affected paired evidence under the repaired rule. If the repair materially changes the fixture, rubric, evaluator, or trial policy, re-establish comparison validity rather than treating a favorable replacement as directly comparable. A repaired harness run does not itself cure another missing required evidence type.

## Turn the record into a conclusion

A decision policy distinguishes three roles before results are read:

- **Must-pass control gates** establish non-compensable boundaries, such as an applicable authorization, isolation, stop, required-valid-evidence, or prohibited-use claim.
- **Task metrics and operating constraints** measure declared quality, cost, latency, completion, or allowed regression for specified cases and slices.
- **Diagnostics** help investigate or prioritize work but do not support a release gate until their fitness for that exact claim is established. A model judge that is diagnostic-only remains diagnostic-only even when its score is favorable.

`go` means the applicable evaluation policy is satisfied and the evidence supports proceeding to the separate readiness and rollout decision. `no_go` means an applicable hard gate, required coverage, required valid evidence, or declared threshold was not met. It is an evidence conclusion, not a judgment that the work has no value: keep or repair the candidate or evaluation and regenerate the affected evidence.

`conditional_go` is deliberately narrow. Use it only when the governing policy permits it and every required pre-release control and evidence item is already complete. It may track a permitted post-release obligation only when that obligation has an owner, due date, monitoring signal, and an overdue consequence. It cannot defer a required safety, grounding, authorization, critical-slice, or other launch prerequisite. A condition that supplies missing pre-release evidence is a blocker and therefore leads to `no_go`.

The conclusion, its limitations, and its next action belong in the decision record. Part 5 separately determines operational readiness, accountable acceptance of residual risk where applicable, rollout, monitoring, and rollback. An evaluation `go` is not deployment permission.

## Worked example: a fictional evidence-gap decision

This walkthrough is **fictional**. It does not report an executed benchmark, measured rate, or live evaluation result.

The decision subject is `policy-assistant@candidate-current-selection`, compared with `policy-assistant@baseline-current-selection`. Both are the ephemeral, read-only policy assistant: they answer from approved current permission-filtered sources with citations, have no writes, no persisted memory, no approval flow, and no delegated agents. The fixture is `travel-policy-current` at revision `fixture-2026-10-18.1`. The current permitted document is `travel-policy-2026`, revision `2026-10-01`, whose fixture value is GBP 220; `travel-policy-2024-superseded` remains present to test currentness.

The comparison record names `POLICY-CURRENT-001`, `POLICY-STALE-002`, `POLICY-MISSING-003`, `POLICY-CONFLICT-004`, `POLICY-DENIED-005`, `POLICY-INJECTION-006`, `POLICY-PARAPHRASE-007`, and `POLICY-EXHAUSTION-008`; it separately names `policy-release-holdout@v1` with `POLICY-HOLDOUT-009`. The holdout is independently authored, not an existing case relabelled after tuning. It records `source-permission-check@v1`, `grounded-policy-human-rubric@v1`, and `trajectory-boundary-check@v1` as claim-facing evaluators. `grounding-judge@v1` is diagnostic-only until its gate fitness is documented.

The illustrative released policy makes **one attempt**: it has no retry, multi-candidate selection, or fallback. Therefore first-attempt success and final delivered-policy success are the same unit for this configuration. A trial plan may use three fresh attempts as an expressly illustrative repeated-trial exercise, but that plan neither asserts a result nor makes three a universal or adequate count. It records reset verification, physical attempts, all statuses, per-attempt resource use, and the final delivered outcome. `pass@k` would not describe this released policy; if a later read-only retry or fallback were enabled, the policy would need to define eligibility, cap, selection, costs, and the end-to-end final result before it could be evaluated.

The fictional decision record has `grounded-policy-human-rubric@v1` marked **missing required valid evidence** for the semantic-support claim. It intentionally does not presume that a favorable source-permission check or diagnostic judge score can fill that gap. Its appropriate conclusion is `no_go — insufficient required valid evidence`, without asserting any candidate pass rate or failure rate.

The same record also illustrates repair visibility. Suppose a `grounding-judge@v1` run is marked invalid because its evidence packet omitted the current document revision. The original record remains visible. Under a predeclared repair rule, a corrected replacement may be run only with the same candidate and semantic case purpose, no narrower input or relaxed rule, and affected paired evidence repeated. Even then, the repaired diagnostic run cannot replace the missing human-rubric evidence. If `POLICY-INJECTION-006` or another case later yields independently observable candidate failure evidence, that result remains a candidate failure rather than becoming invalid because the judge packet was also defective.

Only a subsequent decision record with the required valid semantic reviews, applicable critical-slice coverage, and all other predeclared evidence could support a new conclusion. A `conditional_go` cannot postpone the missing semantic reviews.

## Evidence and checklist

Before accepting a decision record, confirm that it answers these questions:

- Is the exact candidate distinguishable from the baseline or documented as a first release, including resolved route/fallback and material configuration identities?
- Are cases, holdout status, fixture and reset condition, evaluators/rubrics, trial policy, physical attempts, final-policy results, and all statuses attributable to that subject?
- Does every reported metric identify its pass predicate, denominator, first-attempt or all-attempt meaning, and relationship to the actual retry, selection, or fallback policy?
- Are candidate/baseline outcomes paired where comparison is claimed, and are meaningful case or critical-slice flips visible?
- Does any inference beyond named curated cases state its population, sampling frame, cluster/dependence treatment, uncertainty method, and limitations?
- Are cost, latency, calls, boundary observations, effects where applicable, and final delivered result retained rather than hidden by a selected retry?
- Are invalid, inconclusive, missing, repaired/replaced, and attributable candidate-failure records visibly distinct, with the repair rule applied without scope or threshold relaxation?
- Are hard gates, coverage, task metrics, diagnostics, non-applicability conclusions, and permitted exceptions evaluated under the policy declared before results?
- Does `conditional_go`, if permitted, leave no required pre-release evidence or control incomplete and name each post-release obligation’s owner, due date, signal, and overdue consequence?
- Does the record name the decision authority, rationale, limitations, next action, and handoff to Part 5 without treating the evaluation conclusion as deployment approval?

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

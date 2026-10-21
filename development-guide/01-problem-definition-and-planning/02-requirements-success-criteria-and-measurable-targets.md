# 1.2 Requirements, Success Criteria, and Measurable Targets

**Status:** 0.5.0-draft.2 — draft

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent whose intended outcome, acceptable behavior, or evidence will inform evaluation or a later readiness decision. The dimensions and metrics depend on the task; not every outcome needs an automated metric.

**Reader question:** What must this system achieve or avoid, how will each material claim be measured, and what target and consequence should be agreed before results are read?

[Part 1 — Problem Definition and Planning](README.md) · [Playbook applicability](../../applicability.md) · [Playbook home](../../README.md)

## Turn a problem into a decision-ready claim

This chapter turns the problem brief into claims you can check later: the outcome worth pursuing, acceptable and unacceptable behavior, and the measures that would support a decision. It does not select an architecture or authorize a release.

A fluent response, a high task score and a worthwhile user outcome are different claims: a policy helper might cite the wrong source fluently, meet a rubric yet take longer to check than today's process, or improve an average while breaking a non-negotiable boundary. The NIST AI RMF describes validation as objective evidence that the requirements for a specific intended use have been fulfilled, and says accuracy measurements should be paired with clearly defined, realistic test sets and documented test methodology. [1]

Start from [1.1](01-defining-the-problem.md); evaluator design, trials, coverage and interpretation are in Part 4.

## Terms and a working model

An **outcome** is the real-world state a user or organization wants, such as a requester being able to take the right next step with reliable policy information, not just a response returned by a system.

A **requirement** states required, prohibited or constrained behavior. An **acceptance criterion** turns one requirement into an observable condition for a stated case or population: "use a current, requester-permitted source when the question is answerable" is a criterion; a source ID printed in an answer is only an observation that may or may not support it.

A **metric** is a fully specified calculation or recorded quantity for one claim. A **target** is the value, bound or state chosen in advance for that metric in this use case. A **baseline** is a comparable measure of the current process or an earlier candidate; if none exists, record that instead of implying improvement. A **proxy** is a measurable stand-in for the outcome; a citation-present rate, for example, does not show that the cited material supports the answer.

A **guardrail** is a boundary condition interpreted separately, so favorable results elsewhere cannot offset its failure (it is **non-compensable**). A **decision consequence** says what happens when a target, guardrail, critical slice or evidence condition is met, not met or unavailable. Non-compensable gates, missing evidence, retries and `go` or `no_go` conclusions are in [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md).

A **critical slice** is a subset of the population that needs separate visibility because task, user context, source state, permission or consequence makes pooling misleading; it is not every possible filter. NIST says what to measure depends on the purpose, audience and needs of the evaluation and, where relevant, calls for disaggregated analysis of expected-population groups. [2]

```text
bounded user outcome
  → functional behavior, prohibited behavior, and acceptable failure paths
  → observable acceptance criteria by case or claim
  → separately defined metrics, guardrails, and critical slices
  → predeclared target, rationale, owner, and decision consequence
  → Part 4 evidence and a later decision
```

Keep the labels on each step distinct so a planning record cannot pass for evidence: an expected outcome such as `needs_information` is not an evaluator status such as `pass`, `fail`, `invalid` or `inconclusive`, and a proposed target is not an observed result.

## Define behavior before calculating it

Write the user outcome in plain language, then the system's contribution in observable terms:

- **Functional behavior:** what an eligible request should receive when the needed information and conditions are present.
- **Prohibited behavior:** actions, disclosures, assertions or omissions that are unacceptable even in a useful-looking answer.
- **Failure-path behavior:** what happens when input is missing, ambiguous, conflicting, out of scope, or blocked by a dependency: clarification, `needs_information`, a decline, an escalation, a bounded partial result, or a visible failure.
- **Nonfunctional behavior:** material service properties, such as reliable delivery, a time bound, and a total cost that fits the use case.

Write the expected result for each case class into the criterion before looking at output, not into an explanation afterwards. A clarification is right for an underspecified request and an obstacle for an answerable one; an escalation is safe when evidence conflicts and a failure when it was clear.

### Keep the decision dimensions separate

NIST frames deployment as a contextual assessment of trustworthiness characteristics, risks, impacts, costs and benefits, and notes that characteristics can be in tension (predictive accuracy and interpretability, for example). [1] Separate dimensions make that tension reviewable instead of hiding it in a composite score.

- **User or business value:** can people complete the intended work with a worthwhile net effect compared with the current process? Signals include task resolution, total effort, correction burden, avoidable handoffs, or a task-specific business consequence; a task-quality score is only a proxy.
- **Task behavior and failure paths:** does the response or terminal outcome match the contract: correct and complete where an answer is supported, honestly bounded where clarification, decline, escalation or failure is right? Correctness or rubric measures belong here.
- **Safety and other non-compensable boundaries:** did prohibited behavior occur? Report population, observations and count; strong task behavior cannot cancel a disallowed disclosure or unauthorized effect.
- **Reliability:** do eligible request episodes reach their contract-appropriate terminal outcome under the defined conditions? This differs from correctness: answers can be right every time one returns while many requests never get one.
- **Latency:** how long does a declared part of the experience take? Say whether timing runs from receipt to first response, to a delivered terminal response, or to a completed user task; these differ. The SRE book treats request latency, error rate and availability (yield) as separate indicators, aggregated as a rate, average or percentile. [3]
- **Total cost:** model or service use, supporting operations, retries, infrastructure, and material human review or correction for the defined population. Do not count unknown human or failed-attempt cost as zero.

A composite may summarize but cannot replace the dimensions or override a non-compensable boundary. If a dimension is not material, say why.

## Make each metric interpretable

A metric record answers these without guessing:

1. **What claim does it measure?** Name the outcome, behavior, boundary or operating property, and whether the metric is direct, a proxy, a guardrail observation or a diagnostic.
2. **What is counted?** The unit (an eligible request episode, a delivered terminal response, an assessed case), the candidate version or period, source or fixture conditions, and the measurement window.
3. **Which population is eligible?** Inclusion rules and every predeclared exclusion, and how refused, escalated, partial, invalid, timed-out, failed, retried and abandoned cases are classified. An exclusion must not make an inconvenient case invisible.
4. **How is it calculated?** The numerator and denominator for a ratio, or the population count and estimator for a quantile or count; the method, aggregation rule, and treatment of retries or final selection.
5. **What makes it comparable?** A comparable baseline and conditions, or `none available`.
6. **What are the target and consequence?** Before results are read: the target or boundary, why it fits the task and consequence, the owner, the critical slices, and what missing evidence or an unmet result means for the decision.

Tie the target's rationale to the user outcome, the cost of error or delay, operating constraints and baseline status; do not borrow a number from another use case. The NIST playbook suggests documenting metric-selection criteria, metrics considered but not used, acceptable limits, and the action when limits are exceeded; it gives no default values. [2]

### Ratios, quantiles, and failure paths answer different questions

A ratio asks what share of the eligible population had the desired event. For a deadline-sensitive task, a **good-event-under-deadline ratio** is:

```text
good_event_under_deadline =
  count of eligible request episodes with the correct contract outcome,
  all applicable observable constraints satisfied, and a delivered terminal response by the declared deadline
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
  count of all eligible request episodes started in the declared candidate/version and measurement window
```

The denominator includes every eligible episode, including timeouts, failures, inappropriate declines, and escalations the criterion did not call for. A clarification, decline, escalation or bounded partial result counts in the numerator only when it is the declared correct outcome for that case.

A **completion-duration quantile** describes completed-response durations. Let `D` be the ordered durations of eligible episodes that delivered the named terminal response before the cutoff, and `n = |D|`. For a proportion `p` between 0 and 1, `Qp(D)` is the `100p`th percentile under the declared sample-quantile method (`p = 0.95` is the 95th percentile). That method fixes rank selection or interpolation, so a displayed percentile is not always an exact observed fraction. [4]

A quantile has **no numerator**; it is not a success ratio. Record the population of `D`, `n`, timing boundaries, `p`, the interpolation method and the aggregation rule. No interpolation method is universally accepted, so compare only reports that use the same one. [4] The percentile says nothing about episodes with no terminal response by the cutoff; do not invent completion times for them.

Pair it with a timeout or no-terminal-response rate, a failure rate, or both. The timeout rate's numerator is eligible episodes without the named terminal response by the cutoff; its denominator is all eligible started episodes. Keep timeouts and declared failures as separate categories.

For cost, **total cost per verified contract-appropriate outcome** divides the accounted total cost of all eligible episodes by the count of verified contract-appropriate outcomes. Define whether review and correction work counts, and leave the result undefined when there are no verified outcomes instead of reporting a misleading zero.

## Build the success record before evidence exists

1. **State the outcome and case rules.** The user outcome, functional and prohibited behavior, and the acceptable terminal outcome for each material variation, linking to the problem brief.
2. **Choose the material dimensions.** Only the value, task, safety, reliability, latency and cost claims that matter to the decision, each marked direct, proxy, guardrail or diagnostic.
3. **Define the measurement contract** using the six questions above.
4. **Predeclare the target and consequence** before candidate results are read. Until a target is chosen, the metric is not a release acceptance criterion.
5. **Hand off an evidence map.** Give Part 4 the claim, cases or conditions, boundary observations, candidate identity and metric definition. [4.6](../04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) owns the claim-to-evidence map; [4.7](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) owns trial, denominator and decision interpretation.

The [success-criteria template](../../templates/1.2/success-criteria.yaml) uses explicit `null` and `not-yet-selected` fields so an unmeasured record cannot be mistaken for a target or result.

## Common pitfalls

- **No baseline.** Without a measure of today's process, "better" has no meaning; claim only absolute results.
- **One blended agent score.** A single average hides a failed boundary behind strong task results.
- **Targets chosen after seeing results.** A target set after the numbers are in fits the numbers.
- **Percentiles without the failures.** A latency percentile over completed responses looks good while timeouts vanish.
- **A proxy treated as the outcome.** Rubric scores and citation rates stand in for user value; they do not prove it.
- **Scope creep after the pilot.** Targets apply to the population measured; new users, sources or actions need new criteria.

## Requirements

- **SUCCESS-01** When an agent is proposed for a user or business task, the outcome owner MUST define the intended outcome and acceptance criteria before interpreting candidate results, including what constitutes a correct result and which case-dependent outcomes count as success.
- **SUCCESS-02** When the agent can encounter missing, ambiguous, conflicting, or out-of-scope input, the owner MUST specify acceptable clarification, refusal, escalation, partial-result, or failure behavior for the applicable cases; an answer that conceals uncertainty or invents unsupported content MUST NOT count as successful.
- **SUCCESS-03** For each metric used to accept or compare an agent, its owner MUST record the measured population and period or candidate version, numerator and denominator, measurement method, comparable baseline or an explicit statement that none is available, target, critical slices, and responsible owner; excluded, invalid, timed-out, refused, and escalated cases MUST be accounted for under predeclared rules.
- **SUCCESS-04** When user/business value, task quality, safety, reliability, latency, or economics are material to the decision, the owner MUST define and report the applicable dimensions separately; a quality proxy MUST NOT be represented as proof of user or business success, and a composite or average score MUST NOT override a failed non-compensable safety constraint.
- **SUCCESS-05** Before a metric is used as a release acceptance criterion, the accountable owner MUST predeclare its target and decision consequence, including how each critical slice and insufficient or missing evidence affects the decision; illustrative values MUST NOT be presented as universal thresholds or measured results.

## Worked example: fictional internal policy assistance

The fictional planning record `POLICY-PLAN-001` covers `internal-policy-assistance`, a permission-filtered, read-only policy assistant with no write or approval capability. Its status is `illustrative-unexecuted`: no evaluation, baseline, target or release decision exists.

Intended outcome: a useful, source-grounded terminal response, or a clear next step when no supported answer exists. In the `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` is current and states a London hotel limit of GBP 220; `travel-policy-2024-superseded@2024-01-01` is superseded and differs.

The acceptance criteria separate the case paths:

- A permitted requester receives `complete` only when the response is grounded in the current permitted source.
- When the permitted answer-bearing source is missing, or two equally authoritative current permitted sources conflict, `needs_information` is expected, not a definite amount.
- A requester without permission receives `declined` without restricted policy content.
- When the declared budget for read-only calls is exhausted, `failed` with useful uncertainty beats an invented answer.
- No write call is expected on any path.

The record defines future measures without inventing values:

```yaml
planning_record_id: POLICY-PLAN-001
use_case_id: internal-policy-assistance
status: illustrative-unexecuted

metric_intentions:
  - dimension: task_behavior
    measure: good_event_under_deadline_ratio
    numerator: eligible episodes with the correct case-dependent terminal outcome and all applicable constraints
    denominator: all eligible episodes started in the named candidate and window
    baseline_status: none_available
    target: not-yet-selected
    observed_result: null

  - dimension: latency
    measure: completed_response_duration_quantile
    numerator: not_applicable_for_a_quantile
    observed_population: eligible episodes with a delivered terminal response before the cutoff
    observed_count: null
    timeout_or_no_terminal_response_rate: reported_separately_over_all_eligible_episodes
    target: not-yet-selected
    observed_result: null

  - dimension: safety
    measure: prohibited_boundary_observation_count
    population: eligible episodes with the applicable permission and no-write boundaries
    target: not-yet-selected
    observed_result: null
```

The user-value question stays open for Part 4: compared with the current process, do requesters resolve their next step without a worse checking or correction load?

### What a completed measurable target can look like

Suppose a fictional owner picks a 15-second budget and a 90% contract-appropriate-response target for a controlled comparison. These are not recommended defaults, and `POLICY-PLAN-001` and its template are unchanged.

```yaml
example_id: POLICY-TARGET-ILLUSTRATION-001
status: illustrative-unexecuted
metric: contract_appropriate_response_under_deadline
unit: one eligible request episode under the named candidate and actual retry policy
population: predeclared controlled comparison cases, not a claim about all production users
numerator: episodes meeting the case-specific outcome and all applicable constraints within 15 seconds
denominator: all eligible episodes started, including timeouts and incorrect or absent outcomes
target:
  minimum_ratio: 0.90
  deadline_seconds: 15
  rationale: fictional stakeholder service budget chosen only to demonstrate a complete target
critical_slices:
  - slice: authorized_answerable
    minimum_ratio: 0.90
  - slice: missing_or_conflicting_evidence
    minimum_ratio: 0.90
  - slice: permission_denied
    minimum_ratio: 0.90
separate_boundary_gate: no observed prohibited disclosure or write in required valid evidence
baseline_status: unmeasured; no improvement over the current process is established
owner: fictional outcome owner; no actual authority or approval asserted
decision_consequence:
  - below the overall or any named slice target means the illustration's acceptance condition is unmet
  - a failed applicable boundary gate or missing required valid evidence remains blocking
observed_result: null
release_authorization: none
```

It is measurable because it names the counted episode, population, required outcome, timing boundary, target, slices and consequence. A clarification or decline counts only in the slice that calls for it, so a blanket refusal cannot satisfy the answerable slice. Zero observed boundary violations describes the evidence collected, not zero field risk. A real owner picks values from their own task, consequence, baseline and budget.

## Evidence and handoff

The record is planning evidence, not proof a target was met. Before using it in Part 4, check that:

- the user or business outcome is distinct from the system output and any task-quality proxy;
- functional, prohibited and case-dependent terminal behavior is explicit for each material variation, and each metric answers the six questions above;
- a ratio's numerator and denominator match the claim, and a quantile names its population, count, estimator and aggregation instead of a numerator;
- completion-duration measures are paired with timeout, no-response or failure reporting where that matters; and
- the record points to Part 4 for cases, evaluators, trial design, consistency, holdouts, coverage and interpretation, and shows planning values as planned, not achieved.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://airc.nist.gov/airmf-resources/playbook/measure/ "AI Risk Management Framework Playbook Measure"
[3]: https://sre.google/sre-book/service-level-objectives/ "Service Level Objectives"
[4]: https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm "Percentiles"

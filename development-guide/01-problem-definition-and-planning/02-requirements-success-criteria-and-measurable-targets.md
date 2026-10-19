# 1.2 Requirements, Success Criteria, and Measurable Targets

**Status:** 0.5.0-draft.2 — draft

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent whose intended outcome, acceptable behavior, or evidence will inform evaluation or a later readiness decision. The dimensions and metrics depend on the task; not every outcome needs an automated metric.

**Reader question:** What must this system achieve or avoid, how will each material claim be measured, and what target and consequence should be agreed before results are read?

[Part 1 — Problem Definition and Planning](README.md) · [Playbook applicability](../../applicability.md) · [Playbook home](../../README.md)

## Turn a problem into a decision-ready claim

This chapter turns the problem brief into claims you can check later: the outcome worth pursuing, acceptable and unacceptable behavior, and the measures that would support a decision. It does not select an architecture, authorize a release, or prove a candidate works.

A fluent response, a high task score and a worthwhile user outcome are different claims. A policy helper might give a well-formed answer from the wrong source, meet a rubric yet make people spend longer checking it than using today's process, or improve an average while breaking a boundary that is not open to trade-off. NIST defines validation as objective evidence that requirements for a specific intended use have been fulfilled, says accuracy measurements should be paired with clearly defined, realistic test sets, and says test sets, metrics and methods should be documented. [1] That is a process aid, not proof that any given metric is valid.

Start from [1.1](01-defining-the-problem.md). Alternatives are in [1.3](03-agent-suitability-and-alternatives.md); harms, data, authority and ownership in [1.4](04-initial-risk-data-ownership-and-delivery-plan.md); evaluator design, trials, coverage and interpretation in Part 4.

## Terms and a working model

An **outcome** is the real-world state a user or organization wants, such as a requester being able to take the right next step with reliable policy information. It is not just a response returned by a system.

A **requirement** is a statement of required, prohibited or constrained behavior. An **acceptance criterion** turns one requirement into an observable condition for a stated case or population. "Use a current, requester-permitted source when the question is answerable" is a criterion; a source ID printed in an answer is only an observation that may or may not support it.

A **metric** is a fully specified calculation or recorded quantity describing one claim. A **target** is the value, bound or state chosen in advance for that metric in this use case. A **baseline** is a comparable measure of the current process or an earlier candidate. If none exists, record that instead of implying improvement. A **proxy** is a measurable stand-in for the outcome you want; a citation-present rate, for example, does not show that the cited material supports the answer.

A **guardrail** is a boundary condition interpreted separately, so favorable results elsewhere cannot offset its failure. A **decision consequence** says what the declared policy does when a target, guardrail, critical slice or evidence condition is met, not met or unavailable. Non-compensable gates, missing evidence, retries and `go` or `no_go` conclusions are in [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md).

A **critical slice** is a subset of the population that needs separate visibility because task, user context, source state, permission or consequence makes pooling misleading. It is not every possible filter. NIST says what to measure depends on the purpose, audience and needs of the evaluation, and, where relevant, calls for disaggregated analysis of expected-population groups. [2]

```text
bounded user outcome
  → functional behavior, prohibited behavior, and acceptable failure paths
  → observable acceptance criteria by case or claim
  → separately defined metrics, guardrails, and critical slices
  → predeclared target, rationale, owner, and decision consequence
  → Part 4 evidence and a later decision
```

An expected outcome such as `needs_information` is not an evaluator status such as `pass`, `fail`, `invalid` or `inconclusive`, and a proposed target is not an observed result.

## Define behavior before calculating it

Write the intended user outcome in plain language first, then describe the system's contribution in observable terms:

- **Functional behavior:** what an eligible request should receive when the needed information and conditions are present.
- **Prohibited behavior:** actions, disclosures, assertions or omissions that stay unacceptable even when the answer looks useful.
- **Failure-path behavior:** what happens when input is missing, ambiguous, conflicting, out of scope, or blocked by a dependency. The right result may be clarification, `needs_information`, a decline, an escalation, a bounded partial result, or a visible failure.
- **Nonfunctional behavior:** material service properties, such as reliable delivery, a time bound, and a total cost that fits the use case.

Put case dependence in the criterion, not in an after-the-fact explanation. A clarification is right for an underspecified request and an obstacle for an answerable one; an escalation is safe when evidence conflicts and a failure when it was clear. State the intended result per case class before looking at output.

### Keep the decision dimensions separate

Use more than one dimension when more than one claim matters. NIST frames deployment as a contextual assessment of trustworthiness characteristics, risks, impacts, costs and benefits, and notes that characteristics can be in tension (accuracy and robustness, for example). [1] Separate dimensions make that tension reviewable instead of hiding it in a composite score.

- **User or business value:** can people complete the intended work with a worthwhile net effect compared with the current process? Signals include task resolution, total effort, correction burden, avoidable handoffs, or a task-specific business consequence. A task-quality score is a proxy until user or process evidence supports the broader claim.
- **Task behavior and failure paths:** does the response or terminal outcome match the declared contract: correct and complete where an answer is supported, honestly bounded where clarification, decline, escalation or failure is right? A correctness or rubric measure may belong here.
- **Safety and other non-compensable boundaries:** did prohibited behavior occur? Report population, observations and count separately; strong task behavior cannot cancel a disallowed disclosure or unauthorized effect.
- **Reliability:** do eligible request episodes reach their contract-appropriate terminal outcome under the defined conditions? Answers can be correct whenever they return while many requests never get one.
- **Latency:** how long does a declared part of the experience take? Say whether timing runs from receipt to first response, to a delivered terminal response, or to a completed user task. These differ. The SRE book treats request latency, error rate and availability (yield) as separate indicators, aggregated as a rate, average or percentile. [3]
- **Total cost:** what resources does the candidate use for the defined population? Include model or service use, supporting operations, retries, infrastructure, and human review or correction when material. Report a defined cost quantity; do not count unknown human or failed-attempt cost as zero.

A composite may be a diagnostic summary but cannot replace the separate dimensions or override a non-compensable boundary. If a dimension is not material, say why instead of covering it with a convenient proxy.

## Make each metric interpretable

A number is only as useful as its definition. A metric record should let a later reader answer these without guessing:

1. **What claim does it measure?** Name the outcome, behavior, boundary or operating property, and whether the metric is direct, a proxy, a guardrail observation or a diagnostic.
2. **What is counted?** Give the unit (an eligible request episode, a delivered terminal response, an assessed case), the candidate version or period, source or fixture conditions, and the measurement window.
3. **Which population is eligible?** Define inclusion rules and every predeclared exclusion. Show how refused, escalated, partial, invalid, timed-out, failed, retried and abandoned cases are classified. An exclusion must not make an inconvenient case invisible.
4. **How is it calculated?** Give the numerator and denominator for a ratio, or the population count and estimator for a quantile or count. Name the method, aggregation rule, and treatment of retries or final selection.
5. **What makes it comparable?** Identify a comparable baseline and conditions. With no baseline, record `none available` and limit the claim to absolute evidence rather than calling a change an improvement.
6. **What are the target and consequence?** Before results are read, state the target or boundary, why it fits the task and consequence, the owner, the critical slices, and what missing evidence or an unmet result means for the decision.

Tie the target's rationale to the user outcome, the cost of error or delay, operating constraints and baseline status; do not borrow a number from another use case. The NIST playbook suggests documenting metric-selection criteria, metrics considered but not used, acceptable limits, and the action when limits are exceeded. [2] It gives no default values.

### Ratios, quantiles, and failure paths answer different questions

Use a ratio to ask what share of the eligible population had the desired event. For a deadline-sensitive task, a **good-event-under-deadline ratio** is:

```text
good_event_under_deadline =
  count of eligible request episodes with the correct contract outcome,
  all applicable observable constraints satisfied, and a delivered terminal response by the declared deadline
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
  count of all eligible request episodes started in the declared candidate/version and measurement window
```

The denominator includes every eligible episode, including timeouts, failures, inappropriate declines, and escalations the criterion did not call for. A clarification, decline, escalation or bounded partial result counts in the numerator only when it is the correct declared outcome for that case.

Use a **completion-duration quantile** to ask about the distribution of durations in a defined completed-response population. Let `D` be the ordered durations of eligible episodes that delivered the named terminal response before the cutoff, and `n = |D|`. For a proportion `p` between 0 and 1, `Qp(D)` is the `100p`th percentile under the declared sample-quantile method (`p = 0.95` is the 95th percentile). That method fixes rank selection or interpolation, so a displayed percentile is not always an exact observed fraction. [4]

A quantile has **no numerator**; it is not a success ratio. Record the population of `D`, the count `n`, timing boundaries, `p`, the interpolation method and the aggregation rule. Interpolation methods differ and none is universally accepted, so two reports need the same declared method before their values can be compared. [4] A percentile over completed responses is conditional on that population. It says nothing about episodes that produced no terminal response by the cutoff, and no completion time should be invented for them.

Pair a conditional quantile with a timeout or no-terminal-response rate, a failure rate, or both. For the timeout rate, the numerator is eligible episodes without the named terminal response by the cutoff and the denominator is all eligible started episodes. Keep categories so a timeout can be told apart from a declared failure.

For cost, **total cost per verified contract-appropriate outcome** puts the accounted total cost of all eligible episodes in the numerator and the count of verified contract-appropriate outcomes in the denominator. Define whether review and correction work counts, and leave the result undefined when there are no verified outcomes instead of reporting a misleading zero.

## Build the success record before evidence exists

1. **State the outcome and case rules.** Start with the user outcome, functional and prohibited behavior, and the acceptable terminal outcome for each material variation. Link to the problem brief instead of copying its evidence.
2. **Choose the material dimensions.** Select only the value, task, safety, reliability, latency and cost claims that matter to the decision, and mark each measure as direct, proxy, guardrail or diagnostic.
3. **Define the measurement contract.** Set the unit, population, version or period, exclusions, statuses, retries, method, baseline status, critical slices and owner. This is where a count, a ratio and a conditional quantile get their distinct definitions.
4. **Predeclare the target and consequence.** Record the target or bound, rationale, decision consequence, and treatment of insufficient or missing evidence before candidate results are read. Until a target is chosen, the metric is not a release acceptance criterion.
5. **Hand off an evidence map.** Give Part 4 the claim, cases or conditions, boundary observations, candidate identity and metric definition. [4.6](../04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) owns the claim-to-evidence map; [4.7](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) owns trial, denominator and decision interpretation.

The [success-criteria template](../../templates/1.2/success-criteria.yaml) uses explicit `null` and `not-yet-selected` fields so an unmeasured record cannot be mistaken for a target or result.

## Common pitfalls

- **No baseline.** Without a measure of today's process, "better" has no meaning. Measure it, or record `none available` and claim only absolute results.
- **One blended agent score.** A single average hides a failed boundary behind strong task results. Report value, task behavior, safety, reliability, latency and cost separately.
- **Targets chosen after seeing results.** A target set after the numbers are in fits the numbers. Predeclare it with its consequence.
- **Percentiles without the failures.** A latency percentile over completed responses looks good while timeouts vanish. Report the timeout rate with it.
- **A proxy treated as the outcome.** Rubric scores and citation rates stand in for user value; they do not prove it.
- **Scope creep after the pilot.** A pilot result is read as covering new users, sources or actions. Targets apply to the population measured; new scope needs new criteria.

## Requirements

- **SUCCESS-01** When an agent is proposed for a user or business task, the outcome owner MUST define the intended outcome and acceptance criteria before interpreting candidate results, including what constitutes a correct result and which case-dependent outcomes count as success.
- **SUCCESS-02** When the agent can encounter missing, ambiguous, conflicting, or out-of-scope input, the owner MUST specify acceptable clarification, refusal, escalation, partial-result, or failure behavior for the applicable cases; an answer that conceals uncertainty or invents unsupported content MUST NOT count as successful.
- **SUCCESS-03** For each metric used to accept or compare an agent, its owner MUST record the measured population and period or candidate version, numerator and denominator, measurement method, comparable baseline or an explicit statement that none is available, target, critical slices, and responsible owner; excluded, invalid, timed-out, refused, and escalated cases MUST be accounted for under predeclared rules.
- **SUCCESS-04** When user/business value, task quality, safety, reliability, latency, or economics are material to the decision, the owner MUST define and report the applicable dimensions separately; a quality proxy MUST NOT be represented as proof of user or business success, and a composite or average score MUST NOT override a failed non-compensable safety constraint.
- **SUCCESS-05** Before a metric is used as a release acceptance criterion, the accountable owner MUST predeclare its target and decision consequence, including how each critical slice and insufficient or missing evidence affects the decision; illustrative values MUST NOT be presented as universal thresholds or measured results.

## Worked example: fictional internal policy assistance

The planning record `POLICY-PLAN-001` is fictional and unexecuted. It covers `internal-policy-assistance`, a permission-filtered, read-only policy assistant with no write or approval capability. Its status is `illustrative-unexecuted`: no evaluation, baseline, target or release decision is reported.

The intended outcome is that an eligible requester gets a useful, source-grounded terminal response to a policy question, or a clear next step when no supported answer exists. In the `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` is current and states a London hotel limit of GBP 220; `travel-policy-2024-superseded@2024-01-01` is superseded and differs.

The acceptance criteria separate the case paths. A permitted requester can receive `complete` only when the response is grounded in the current permitted source. When the permitted answer-bearing source is missing, or two equally authoritative current permitted sources conflict, `needs_information` is expected and a definite amount is not. A requester without permission receives `declined` without restricted policy content. When the read-only budget is exhausted, `failed` with useful uncertainty beats an invented answer. No write call is expected on any path.

The record defines separate future measures without inventing values:

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

No numeric target appears because none has been selected. A completed-response percentile would say only how long completed responses took, not whether the question was resolved. The user-value question stays open: compared with the current process, do eligible requesters resolve their next step without a worse checking or correction load? Comparison design is Part 4 work.

### What a completed measurable target can look like

This alternate illustration replaces an unset target with a reviewable choice. Suppose a fictional outcome owner picks a 15-second service budget and a 90% contract-appropriate-response target for a controlled comparison. These are illustrative choices, not measurements or recommended defaults, and they leave `POLICY-PLAN-001` and its template unchanged.

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

This criterion is measurable because it names the counted episode, eligible population, required outcome, timing boundary, target, slices and consequence. A clarification or decline counts only where the case calls for it, so a blanket refusal cannot satisfy the answerable slice. Zero observed boundary violations describes the evidence collected, not a guarantee of zero field risk. A real owner would pick values to suit the task, consequence and baseline.

## Evidence and handoff

The record is ready to hand off when a reader can find the intended outcome, every material criterion, the reason for each metric, and the rules that stop a favorable score from masking a failed boundary or missing evidence. It is planning evidence, not proof a target was met. Before using it in Part 4, check that:

- the user or business outcome is distinct from the system output and any task-quality proxy;
- functional, prohibited and case-dependent terminal behaviors are explicit for material variations;
- each metric has a unit, population, version or period, status rules, method, baseline status, target status, slices, owner and decision consequence;
- a ratio's numerator and denominator match the claim, and a quantile names its population, count, estimator and aggregation instead of inventing a numerator;
- completion-duration measures are paired with visible timeout, no-response or failure reporting where that matters; and
- the record points to Part 4 for cases, evaluators, trial design, consistency, holdouts, coverage and interpretation, and shows planning values as planned, not achieved.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://airc.nist.gov/airmf-resources/playbook/measure/ "AI Risk Management Framework Playbook Measure"
[3]: https://sre.google/sre-book/service-level-objectives/ "Service Level Objectives"
[4]: https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm "Percentiles"

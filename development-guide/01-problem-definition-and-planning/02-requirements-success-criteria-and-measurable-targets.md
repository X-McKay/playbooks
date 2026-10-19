# 1.2 Requirements, Success Criteria, and Measurable Targets

**Status:** 0.5.0-draft.2 — Part 1 refined draft; proposed, not adopted

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent when its intended outcome, acceptable behavior, or evidence will inform evaluation or a later readiness decision. The dimensions and metrics used depend on the task; this chapter does not require an automated metric for every outcome.

**Reader question:** What must this proposed system achieve or avoid, how will each material claim be measured, and what target and consequence should be agreed before evidence is interpreted?

[Part 1 — Problem Definition and Planning](README.md) · [Playbook applicability](../../applicability.md) · [Playbook home](../../README.md)

## Turn a problem into a decision-ready claim

A problem brief explains the work that matters and the uncertainty around it. This chapter turns that brief into claims that can be checked later: the outcome worth pursuing, the behavior that is acceptable, behavior that is unacceptable, and the measures that would support a decision. It does **not** select an architecture, authorize a release, or prove that a candidate works.

That boundary matters because an articulate response, a high task score, and a worthwhile user outcome are different claims. A policy helper might return a well-formed answer while relying on the wrong source. It might meet a task rubric yet make people spend more time checking its answer than using today’s process. It might improve an average while violating a boundary that is not open to trade-off. NIST describes validation as objective evidence that requirements for a specific intended use have been fulfilled, and says measurements should use clearly defined, realistic test sets and document their method and limits. [1] The proposed requirements in this chapter make those distinctions usable; they are not imposed by NIST or evidence of organizational adoption.

Start from [1.1 Defining the Problem](01-defining-the-problem.md), which supplies the user task, current process, material variations, and scope. Keep the comparison of an agent with simpler alternatives in [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md). Keep harms, data, authority, accountable ownership, and delivery limits in [1.4 Initial Risk, Data, Ownership, and Delivery Plan](04-initial-risk-data-ownership-and-delivery-plan.md). Part 4 owns evaluator design, trials, coverage, consistency, holdouts, and interpretation of decision evidence.

## Terms and a working model

An **outcome** is the real-world state a user or organization wants to reach, such as a requester being able to take the appropriate next step with reliable policy information. It is not merely a response returned by a system.

A **requirement** is a proposed statement of required, prohibited, or constrained behavior. An **acceptance criterion** translates one requirement into an observable condition that can be assessed for a stated case or population. For example, “use a current, requester-permitted source when the question is answerable” is a criterion; a source identifier printed in an answer is only an observation that may or may not support it.

A **metric** is a fully specified numeric calculation or recorded quantity used to describe one claim. A **target** is the value, bound, or state selected in advance for that metric in this use case. A **baseline** is a comparable measure of the current process or an identified earlier candidate. If none is available, record that absence rather than implying improvement. A **proxy** is a practical measurable stand-in for a desired outcome; it can be useful without proving the outcome itself. A citation-present rate, for example, is not proof that cited material supports the answer.

A **guardrail** is a separately interpreted boundary condition whose failure cannot be offset by favorable results elsewhere. A **decision consequence** says what the declared policy does when a target, guardrail, critical slice, or evidence condition is met, not met, or unavailable. The canonical treatment of non-compensable gates, missing evidence, retries, and `go` or `no_go` conclusions is in [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md); a planning record does not itself authorize a release.

A **critical slice** is a subset of the population whose performance needs separate visibility because the task, user context, source state, permission condition, or potential consequence makes pooling misleading. It is not a synonym for every possible filter. NIST’s measurement guidance notes that metric choice depends on the evaluation’s purpose, audience, and needs, and recommends identifying expected-population groups that need disaggregated analysis when that is relevant. [2]

A useful path is:

```text
bounded user outcome
  → functional behavior, prohibited behavior, and acceptable failure paths
  → observable acceptance criteria by case or claim
  → separately defined metrics, guardrails, and critical slices
  → predeclared target, rationale, owner, and decision consequence
  → Part 4 evidence and a later decision
```

Each arrow records a different kind of statement. An expected terminal outcome such as `needs_information` is not an evaluator status such as `pass`, `fail`, `invalid`, or `inconclusive`. A proposed target is not an observed result. Keeping those labels separate prevents a planning record from looking like completed evidence.

## Define behavior before calculating it

Write the intended user outcome in plain language first. Then describe the system contribution in observable terms:

- **Functional behavior** says what an eligible request should receive when the needed information and conditions are present.
- **Prohibited behavior** names actions, disclosures, assertions, or omissions that remain unacceptable even when the answer otherwise looks useful.
- **Failure-path behavior** says what happens when input is missing, ambiguous, conflicting, out of scope, or blocked by a dependency. The appropriate result may be clarification, `needs_information`, a decline, an escalation, a bounded partial result, or a visible failure.
- **Nonfunctional behavior** makes material service properties explicit, such as whether an outcome is delivered reliably enough, within a relevant time bound, and with a total cost that fits the use case.

Case dependence belongs in the criterion, not in a post-hoc explanation. A clarification can be the correct result for an underspecified request and an unnecessary obstacle for an answerable one. An escalation can preserve safety when evidence conflicts and signal a task failure when the same evidence was available and clear. State the intended result for the relevant case class before looking at candidate output.

### Keep the decision dimensions separate

Use more than one dimension when more than one claim matters. NIST frames deployment as a contextual assessment of trustworthiness characteristics, risks, impacts, costs, and benefits; it also cautions that distinct trustworthiness characteristics can be in tension. [1] Separating the following dimensions makes that tension reviewable rather than hiding it in a composite score.

**User or business value** asks whether people can complete the intended work with a worthwhile net effect compared with the current process. Useful signals can include task resolution, total effort, correction burden, avoidable handoffs, or a task-specific business consequence. A task-quality score is a proxy until user or process evidence supports this broader claim.

**Task behavior and failure paths** ask whether the response or terminal outcome matches the declared contract: correct and complete where a supported answer is expected, and honestly bounded where clarification, a decline, escalation, or failure is appropriate. This is where a semantic correctness or rubric measure may belong.

**Safety and other non-compensable boundaries** ask whether prohibited behavior occurred. Report the relevant population, observations, and count separately. Strong task behavior cannot cancel a disallowed disclosure, unauthorized effect, or another applicable hard boundary failure.

**Reliability** asks whether eligible request episodes reach their contract-appropriate terminal outcome under the defined conditions. It is distinct from correctness: an answer can be correct in the cases that return while many eligible requests do not reach a usable terminal response.

**Latency** asks how long a declared part of the experience takes. Specify whether the timing starts at receipt and ends at first response, a delivered terminal response, or a completed user task. These are not interchangeable. The SRE book distinguishes request latency, error rate, and availability or yield as separate indicators, and notes that aggregation can be a rate, average, or percentile. [3]

**Total cost** asks what resources the candidate consumes for the defined population. It can include model or service use, supporting operations, retries, infrastructure, and human review or correction when those are material to the proposed workflow. Report a defined cost quantity rather than treating unknown human or failed-attempt cost as zero.

A composite may be a diagnostic summary, but it cannot replace the reported dimensions or override an applicable non-compensable boundary. If a dimension is not material to the decision, say why it is not used instead of silently representing it with a convenient proxy.

## Make each metric interpretable

A number is only as informative as its definition. A decision-useful metric record makes it possible for a later reader to answer these questions without guessing:

1. **What claim does this measure?** Name the outcome, behavior, boundary, or operating property and whether the metric is a direct measure, a proxy, a guardrail observation, or a diagnostic.
2. **What is counted?** Specify the unit: for example, one eligible request episode, one delivered terminal response, or one assessed case. Identify the candidate version or period, source/fixture conditions where relevant, and the measurement window.
3. **Which population is eligible?** Define inclusion rules and every predeclared exclusion. Show how refused, escalated, partial-result, invalid, timed-out, failed, retried, and abandoned cases are classified. An exclusion does not make an inconvenient case invisible.
4. **How is it calculated or observed?** State the numerator and denominator for a ratio, or the observed-population count and estimator for a quantile or count. Name the measurement method, aggregation rule, and treatment of retries or final selection. Part 4 determines how evidence is designed and judged; this chapter records what the measure must mean.
5. **What makes it comparable?** Identify a comparable baseline and the comparable conditions. If there is no baseline, record `none available` and limit the claim to the candidate’s absolute evidence rather than calling a change an improvement.
6. **What is the target and consequence?** Before results are interpreted, identify the selected value or boundary, why it fits the task and consequence, the responsible owner, the critical slices, and what missing evidence or an unmet result means for the later decision.

The target’s rationale should connect to the user outcome, the consequence of error or delay, operating constraints, and baseline status. It is a local planning choice, not a number to inherit from another use case. The NIST playbook suggests documenting metric-selection criteria, metrics not used, acceptable limits, and action when limits are exceeded. [2] That supports a qualified recommendation to make the rationale and consequence visible; it does not supply a default percentage, duration, cost, reviewer role, or adoption decision.

### Ratios, quantiles, and failure paths answer different questions

Use a ratio when the question is “what share of the defined eligible population had the desired event?” For a deadline-sensitive task, a **good-event-under-deadline ratio** can be defined as:

```text
good_event_under_deadline =
  count of eligible request episodes with the correct contract outcome,
  all applicable observable constraints satisfied, and a delivered terminal response by the declared deadline
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
  count of all eligible request episodes started in the declared candidate/version and measurement window
```

The denominator includes every eligible episode, including an episode that times out, fails, reaches an inappropriate decline, or needs an escalation that the criterion did not call for. A clarification, decline, escalation, or bounded partial result can contribute to the numerator only when it is the correct declared outcome for that case. This form makes the deadline and the experience of all eligible requests part of the same claim.

Use a **completion-duration quantile** when the question is about the distribution of observed durations among a specifically defined completed-response population. Let `D` be the ordered set of duration observations for eligible episodes that delivered the named terminal response before the measurement cutoff, and let `n = |D|`. For a proportion `p` between 0 and 1, `Qp(D)` denotes the `100p`th percentile under the declared sample-quantile method: `p = 0.95` corresponds to the 95th percentile. That method specifies rank selection or interpolation; a finite sample does not make every displayed percentile an exact observed fraction. [4]

For a quantile, **numerator is not applicable**: it is not a success ratio. Record `D`’s population, the count `n`, timing boundaries, `p`, the interpolation method for a finite sample, and the aggregation rule. NIST notes that percentile interpolation methods differ and no single method is universally accepted, so two reports need the same declared method before their displayed values can be treated as directly comparable. [4] A percentile calculated only from completed-response observations is conditional on that population. It does not describe an eligible episode that produced no terminal response by the cutoff, and no completion time should be fabricated for that episode.

Pair such a conditional quantile with an explicitly defined timeout or no-terminal-response rate, failure rate, or both. For example, a timeout-or-no-terminal-response rate has the count of eligible episodes without the named terminal response by the cutoff as its numerator and all eligible started episodes as its denominator. Preserve the relevant outcome categories so a later reader can distinguish a timeout from a declared failure response. This pairing makes the latency distribution useful without allowing failed or absent responses to disappear.

For a cost claim, a **total cost per verified contract-appropriate outcome** can use the accounted total cost of all eligible episodes in the numerator and the count of verified contract-appropriate outcomes in the denominator. Define whether review and correction work is in scope, and leave the result undefined when there are no verified outcomes rather than creating a misleading zero. This is a cost measure, not proof of user value or safety.

## Build the success record before evidence exists

A compact record is usually enough when it keeps the definitions inspectable.

1. **State the outcome and case rules.** Begin with the user outcome, functional behavior, prohibited behavior, and acceptable terminal outcome for each material variation. Link the record to the problem brief rather than copying its discovery evidence.
2. **Choose the material dimensions.** Select only the value, task, safety, reliability, latency, and cost claims that matter to the decision. State whether each proposed measure is a direct measure, proxy, guardrail, or diagnostic.
3. **Define the measurement contract.** Set the unit, population, candidate version or period, exclusions, statuses, retries, calculation or observation method, baseline status, critical slices, and responsible owner. This is where a count, ratio, and conditional quantile receive their distinct definitions.
4. **Predeclare the target and consequence.** Record the target or bound, rationale, decision consequence, and treatment of insufficient or missing evidence before candidate results are read. An unselected target means the metric is not yet a release acceptance criterion.
5. **Hand off an evidence map.** Give Part 4 the claim, cases/conditions, relevant boundary observations, candidate identity, and metric definition. [4.6 Standards, Required Coverage, and Execution Cadence](../04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) owns the claim-to-evidence map; [4.7](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) owns trial, denominator, and decision interpretation details.

The accompanying [success-criteria template](../../templates/1.2/success-criteria.yaml) is a neutral planning aid. It contains explicit `null` and `not-yet-selected` fields so a fictional unmeasured record cannot be mistaken for a target, result, approval, or deployment.

## Requirements

- **SUCCESS-01** When an agent is proposed for a user or business task, the outcome owner MUST define the intended outcome and acceptance criteria before interpreting candidate results, including what constitutes a correct result and which case-dependent outcomes count as success.
- **SUCCESS-02** When the agent can encounter missing, ambiguous, conflicting, or out-of-scope input, the owner MUST specify acceptable clarification, refusal, escalation, partial-result, or failure behavior for the applicable cases; an answer that conceals uncertainty or invents unsupported content MUST NOT count as successful.
- **SUCCESS-03** For each metric used to accept or compare an agent, its owner MUST record the measured population and period or candidate version, numerator and denominator, measurement method, comparable baseline or an explicit statement that none is available, target, critical slices, and responsible owner; excluded, invalid, timed-out, refused, and escalated cases MUST be accounted for under predeclared rules.
- **SUCCESS-04** When user/business value, task quality, safety, reliability, latency, or economics are material to the decision, the owner MUST define and report the applicable dimensions separately; a quality proxy MUST NOT be represented as proof of user or business success, and a composite or average score MUST NOT override a failed non-compensable safety constraint.
- **SUCCESS-05** Before a metric is used as a release acceptance criterion, the accountable owner MUST predeclare its target and decision consequence, including how each critical slice and insufficient or missing evidence affects the decision; illustrative values MUST NOT be presented as universal thresholds or measured results.

## Worked example: fictional internal policy assistance

The shared planning record `POLICY-PLAN-001` considers `internal-policy-assistance`. It is **fictional and unexecuted**. The candidate is a permission-filtered, read-only policy assistant with no write or approval capability. Its planning status is `illustrative-unexecuted`; nothing in this example reports an evaluation, a user outcome, a baseline, an accepted target, or a release decision.

The intended outcome is that an eligible requester can receive a useful, source-grounded terminal response to a policy question or a clear next step when a supported answer is unavailable. In the fictional `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` is current and states a London hotel limit of GBP 220. `travel-policy-2024-superseded@2024-01-01` is a superseded record with a different amount. These fixture facts are not a real policy and are not candidate results.

The acceptance criteria distinguish the case paths. A requester permitted to access the current source can receive `complete` only when the response is grounded in that current permitted source. When the permitted answer-bearing source is missing, or two equally authoritative current permitted sources conflict, `needs_information` is the expected bounded outcome; a definitive amount is not. A requester without permission receives `declined` without restricted policy content. When the declared read-only budget is exhausted, `failed` with useful uncertainty is preferable to an invented answer. In every path, no write invocation is expected. These are planned case relations, not observed outputs.

The record can then define separate future measures without inventing values:

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

No numeric target is shown because the fictional record has not selected one. Before such a metric becomes an acceptance criterion, its outcome owner would need to set the target, target rationale, critical slices, and decision consequence under the proposed requirements. A completed-response percentile, if later selected, would say only how long the named completed-response observations took. It would not make timeouts disappear or establish whether the requester’s question was resolved.

The example also keeps a user-value question open: compared with the existing human-supported process, do eligible requesters resolve their next step with no unacceptable increase in checking or correction work? A task rubric, a citation field, a permission observation, and a response-time measure may inform that question, but none is its proof by itself. The comparison design and evidence are work for Part 4, not results supplied by this planning record.

### What a completed measurable target can look like

An alternate illustration shows how to replace an unset target with a reviewable choice. Suppose a fictional outcome owner chooses a 15-second service budget and a 90% contract-appropriate-response target for a controlled comparison. These are illustrative stakeholder choices, not measurements, recommended defaults, or values established by the cited sources. This does not change the unset fields in `POLICY-PLAN-001` or its reusable template.

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

This criterion is measurable because it identifies the counted episode, eligible population, required outcome, timing boundary, target, slices, and consequence. A required clarification or decline counts only in the case that calls for it; a blanket refusal cannot satisfy the answerable slice. Zero observed boundary violations describes the specified evidence, not a guarantee of zero field risk. A real owner would select different values where the task, consequence, user expectation, baseline, or operating budget warrants them and use Part 4 to decide how much valid evidence supports the choice.

## Evidence and handoff

The success record is ready to hand off when a reader can locate the intended outcome, every material criterion, the reason each metric exists, and the rules that prevent a favorable score from changing the meaning of a failed boundary or missing evidence. It is planning evidence, not proof that a candidate has achieved a target.

Before using the record in Part 4, check that:

- the user or business outcome is distinct from the proposed system output and task-quality proxy;
- functional, prohibited, and case-dependent terminal behaviors are explicit for material variations;
- each metric has a stated unit, population, version or period, status rules, method, baseline status, target status, slices, owner, and decision consequence;
- a ratio’s numerator and denominator match the claim, while a quantile names its observed population, count, estimator, and aggregation rather than inventing a numerator;
- conditional completion-duration measures are paired with visible timeout, no-terminal-response, or failure reporting when those conditions matter; and
- the record points to Part 4 for cases, evaluators, trial design, consistency, holdouts, coverage, and evidence interpretation rather than presenting a planning value as an achieved result.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://airc.nist.gov/airmf-resources/playbook/measure/ "AI Risk Management Framework Playbook Measure"
[3]: https://sre.google/sre-book/service-level-objectives/ "Service Level Objectives"
[4]: https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm "Percentiles"

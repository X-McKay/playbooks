# 4.6 Standards, Required Coverage, and Execution Cadence

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, accountable owners, security/privacy reviewers, and release reviewers  
**Applicability:** Every production candidate and every design, pilot, release, or change decision that relies on its evaluation evidence.  
**Reader question:** What is mandatory for this agent and this change, and when must it run?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.5 Planning, Designing, and Running Tests and Evaluations](05-planning-designing-and-running-tests-and-evaluations.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Part 4 practical reference](reference/README.md)

## Purpose and boundary

This chapter says **what evidence is needed and when it is refreshed**: one small core for every production candidate, plus profiles only for capabilities, risks, claims, and exposure in scope. A profile is not an architecture bundle; evaluating a read-only assistant does not give it a queue, approval flow, store, second agent, or model judge.

The catalogue, and the absence of a universal pass rate, trial count, or calibration cutoff, are this playbook's choices; NIST supports risk-led, documented, proportionate measurement before deployment and during operation.[1] Methods live in [4.2](02-test-levels-techniques-and-suite-purposes.md)–[4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md); this chapter names only each profile's evidence objective.

## Reading a coverage record

A coverage record links a claim to the smallest evidence set that can establish it (the fields are listed in CASE-01). It is a map, not a scorecard. Keep three kinds of result apart:

- A **required check** establishes a contract, control, or evidence obligation.
- A **quality threshold** is a predeclared acceptance or comparison value set by the policy owner; this chapter gives no number.
- A **diagnostic signal** helps investigate or prioritize. An exploratory transcript, similarity score, or model judge not shown fit for the exact claim is diagnostic, not gating.

A favorable average or unrelated metric cannot offset a failed critical control or missing valid evidence. [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) classifies gates, diagnostics, insufficient evidence, and `go`/`conditional_go`/`no_go`.

### The universal evidence core

COVERAGE-01 lists the core. Two points are easy to miss. First, contract-defined time, call, resource, output, and stop bounds belong to the core even for a local read-only assistant; checking them or safe exhaustion needs no distributed load environment, and the capacity profile is only for shared-resource claims. Second, enough identity and run status must be kept to tell a candidate failure from invalid or inconclusive evidence.

For variable behavior, invariance and sensitivity evidence follow [4.3](03-evaluation-types-and-dimensions.md). Repeated attempts, safe alternative trajectories, and a final selected answer answer different questions; none shows a zero field failure rate.

## Additive profiles

Select a profile because its **trigger is true for this candidate and decision scope**, not because the name sounds thorough. `N/A` means the trigger is absent for the named candidate and stage; it is not a pass or waiver. Missing telemetry, an unimplemented control, cost, rarity, vendor ownership, or a "pilot" label are evidence gaps or scope decisions, not `N/A` reasons.

Profiles are independent: retrieval does not imply stored memory, a route or fallback does not imply a model judge, resumable read-only work does not imply a write or approval, and a queue alone does not imply resumable recovery.

Unless a profile says otherwise, run it **before exposure and again after a change to any item in its "Rerun after" line**.

### Approved retrieval

**Trigger:** A curated corpus, search, cached source, policy or document source, or a claim about provenance, relevance, coverage, admission, freshness, or currentness affects an outcome.

**Evidence focus:** Source admission and requester scope; source identity, revision, and currentness; missing, stale, and conflicting evidence; the bounded result when support is absent. Use a semantic-support evaluator when grounding is claimed; citation identifiers or metadata do not show support. Include any cache, index, reranker, or transformation that can affect access or currentness.

**Rerun after:** corpus, source-admission, index, reranker, cache, filter, query transformation, or freshness-policy change. Run as controlled offline evidence before pilot or release.

**Owner:** [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md); grounding evaluation in [4.4](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No source retrieval, cache, provenance, freshness, or source-backed answer claim is in scope.

### Tools and trajectory

**Trigger:** An admitted tool, interface, plug-in, code executor, remote capability, or model-selected action contributes to the outcome.

**Evidence focus:** Permitted selection where it matters, security-relevant arguments, identity propagation, enforcement-time authorization, error/timeout/partial-result handling, necessary ordering, provenance, retry/stop behavior, and forbidden invocations, with proposal, boundary decision, execution, and disclosure recorded separately ([4.3](03-evaluation-types-and-dimensions.md)). A fluent final response does not show an authorization boundary operated.

**Rerun after:** interface inventory, schema, permission, identity, orchestration, retry, dependency, or tool-selection change.

**Owner:** [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md), [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), and [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

**N/A:** No admitted interface or model-selected action is in scope.

### Untrusted input

**Trigger:** User input, retrieved material, tool output, email, web material, memory, peer content, or another untrusted channel reaches model context or downstream rendering.

**Evidence focus:** Direct and channel-correct indirect injection, instruction/data separation, relevant encoding or transformation paths, output and tool-boundary validation, attempted disclosure or action, and a benign task. Use harmless fixtures and instrumented destinations where a real attempt would be unsafe. A clean response or absent telemetry does not show containment; OWASP treats injection tests as one layer, not a benchmark.[2] Fixed cases show only that known attacks fail; resistance needs adaptive or red-team attacks, since in a public competition of over 250,000 attempts every one of 13 frontier models was hijacked at least once.[4]

**Rerun after:** context channel, retrieval, rendering, prompt, model, boundary, or transformation change.

**Owner:** [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md); cases in [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No untrusted content reaches context or rendering. A narrow user request is covered by the core only if it creates no extra untrusted-content boundary claim.

### Sensitive data and tenant scope

**Trigger:** Personal, confidential, regulated, tenant-scoped, privileged, non-public, derived, or logged data is reachable, or its isolation is claimed.

**Evidence focus:** Trusted identity and entitlement propagation, cross-scope isolation, claimed output and telemetry minimization or redaction, retention or expiry where applicable, and denied and failure paths. Synthetic or minimized fixtures can establish basic boundary behavior; real customer material is not required.

**Rerun after:** identity, source, data-handling, logging, routing, permission, or retention change. Run before pilot or release.

**Owner:** [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), with specialized assurance in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md).

**N/A:** The candidate cannot reach or derive protected data and makes no isolation claim.

### External effects

**Trigger:** The candidate can initiate or request a write, send, purchase, publish, deploy, delete, identity change, or other external state change.

**Evidence focus:** Validated intent and exact target/parameter scope, execution-time authorization, pre-effect checks, timeout or unknown-outcome handling, duplicate/retry behavior, and authoritative target state or receipt. A denied or simulated action leaves no effect, and a blocked proposal is not an unauthorized execution.

**Rerun after:** effect interface, target, authorization, payload, retry, reconciliation, or action-path change.

**Owner:** [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md).

**N/A:** The candidate cannot initiate or request an external state change.

### Human approvals

**Trigger:** A governing policy requires human approval before a consequential action.

**Evidence focus:** Preview and immutable action subject, approver authority and scope, target/parameter binding, expiry, revocation or material-change invalidation, one-time use or replay protection, interruption or escalation, and execution-time authorization after approval. Approval adds a condition to an authorized action; it does not enlarge authority.

**Rerun after:** approval policy, payload, authority, expiry, execution, or action-path change.

**Owner:** [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md).

**N/A:** No approval-required consequential action is in scope.

### Durable recovery

**Trigger:** Work is resumable, long-running, queued for recovery, approval-waiting, recoverable after interruption, or otherwise depends on durable state.

**Evidence focus:** Durable state identity and isolation, suspension/resume, replay or retry, cancellation, timeout/partial/unknown outcomes, controlled interruption recovery, compatibility, and, only where effects exist, duplicate prevention, idempotency, or reconciliation. A successful resume does not show exactly-once external effects.

**Rerun after:** persistence, checkpoint, recovery, retry, compatibility, or durable-state change.

**Owner:** [7.1 Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md); effect or approval evidence stays with its own profile.

**N/A:** The work is ephemeral and non-resumable. A queue without a recovery claim does not select this profile.

### Conversation

**Trigger:** Multi-turn interaction, session history, or a task horizon across turns can affect behavior.

**Evidence focus:** A bounded episode: milestones, retained material constraints, forbidden events, terminal outcome, and turn, time, or budget limits. Test loss or contradiction of a material constraint when plausible. No private reasoning traces.

**Rerun after:** conversation contract, session lifecycle, task-horizon, instruction, or turn-management change.

**Owner:** [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) and [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md).

**N/A:** A single bounded request with no behaviorally relevant cross-turn state.

### Stored memory and context transformation

**Trigger:** Stored memory, summaries, answer-affecting caches, context selection, compression, or another input-to-context transformation can affect behavior.

**Evidence focus:** Session or tenant scope, provenance through the transformation, claimed expiry/deletion or retention, poisoning resistance, loss or distortion of material constraints, context sensitivity, and safe absence, corruption, or limit behavior. Test only claims actually made; retrieval alone is not stored memory.

**Rerun after:** memory schema, retention rule, cache, summary, context-selection, transformation, or task-horizon change.

**Owner:** [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md).

**N/A:** No stored state, cache, summary, or context transformation affects the evaluated behavior. Conversation alone does not make deletion testing applicable.

### Composition

**Trigger:** Two or more model-driven agents, or a remote-agent interaction, contribute to one outcome.

**Evidence focus:** Handoff and routing contracts, identity and source propagation, delegated scope, least privilege, denial propagation, malformed or malicious peer content, loop limits, failure/timeout containment, and the end-to-end outcome. Passing component cases do not show the composed system keeps its boundary.

**Rerun after:** topology, member, handoff, remote-interface, or shared-contract change.

**Owner:** [Part 9](../../engineering-reference/09-multi-agent-systems-and-interoperability/README.md).

**N/A:** One model-driven agent produces the outcome and no remote-agent interaction is enabled.

### Shared capacity and resource performance

**Trigger:** Shared queues, caches, quotas, rate or concurrency limits, budgets, common downstream capacity, or a shared-resource availability/fairness claim can affect correctness, safety, tenant fairness, or availability.

**Evidence focus:** Admission and limit enforcement, claimed isolation, queue/retry/backoff behavior, fail-safe exhaustion, claimed resource/call/cost/latency bounds, and truthful user-facing degradation. Proportional: a small local assistant needs no distributed load infrastructure, and the core still tests its declared local bounds.

**Rerun after:** limit, capacity, provider, queue, cache, admission, shared-budget, or shared-resource change.

**Owner:** [5.1 Observability, Budgets, and Operational Control](../05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md), [8.3 Cost, Latency, and Performance Optimization](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md), and [8.4 Capacity, Admission Control, and Backpressure](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md); thresholds in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** No shared resource or shared-capacity claim can affect the evaluated behavior. Record any local bound under the core.

### Human impact and domain assurance

**Trigger:** The risk record identifies material differential harm by population, domain, language, role, geography, entitlement, accessibility, or jurisdiction, or an external policy calls for more assurance.

**Evidence focus:** The harm screen and justified slices ([4.3](03-evaluation-types-and-dimensions.md)). Add domain review, representative-user work, accessibility, appeal/override, or higher-assurance evidence only where use and risk call for it.

**Rerun after:** material use, user, data, capability, domain, or risk-context change. Run before release.

**Owner:** [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

**N/A:** The recorded screen finds no material differential-harm or domain-assurance trigger for the named scope; review again when scope changes.

### Model judges

**Trigger:** A model-based evaluator supplies decision- or release-facing evidence.

**Evidence focus:** Versioned rubric, known pass/fail anchors, human-reviewed held-out calibration for the target claim and risk slices, false passes, disagreements, unscorable cases, and sensitivity to order, style, reference leakage, or injection. The judge stays diagnostic until fitness for the exact decision role is documented. This concerns the evaluator, not model routing.

**Rerun after:** material judge, rubric, context, model, target-distribution, or target-claim change. Establish fitness before the judge informs the stated decision; public guidance likewise treats grader usefulness as context-dependent.[3]

**Owner:** [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No model judge supplies decision- or release-facing evidence. A retained diagnostic judge stays labeled diagnostic.

### Model selection, routing, and fallback

**Trigger:** A selected model, provider, settings, route, fallback, or degradation policy can change task behavior, data handling, controls, or operating limits.

**Evidence focus:** The actual end-to-end selection, routing, retry, fallback, and final-delivery policy; resolved identities; and each enabled path's contract, privacy, control, quality, latency, cost, and recovery behavior. An alternate path may differ only under a declared contract rule. A route does not require a model judge.

**Rerun after:** selection, provider, configuration, routing, fallback, retry, or degradation change.

**Owner:** [8.1 Model Selection, Parameters, and Routing](../../engineering-reference/08-model-context-and-resource-engineering/01-model-selection-parameters-and-routing.md); provenance and comparison in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** Nothing beyond the frozen candidate identity can affect the claim. Not available when a hidden or enabled alternate path can affect behavior.

## Cadence from development through operation

### Production preparation

During development, use the narrowest claim-fit checks: focused deterministic and component checks for relied-on rules, representative cases for changed behavior, and one focused boundary case per newly enabled risk. Development cases change during iteration and, once used for tuning, are not a holdout. Keep capability and regression suites apart, and graduate saturated capability cases ([4.2](02-test-levels-techniques-and-suite-purposes.md)).

### Change review

A material change can reasonably alter a mapped claim, boundary, evidence, use/risk context, or operating assumption: an instruction; model, provider, settings, route, or fallback; interface schema, permission, credential, target, or effect; source, corpus, index, or cache; identity or authorization; user or domain; context, memory, retention, retry, approval, durable state, composition, capacity, evaluator, rubric, threshold, or dependency environment. "Prompt-only," vendor-owned, rare, expensive, and "already a pilot" are not reasons to skip.

COVERAGE-03 lists the reruns. When a change makes a profile newly applicable (enabling retrieval, storing memory, adding an effect, turning on approval or fallback, expanding protected data, adding an agent), complete that profile before exposing the capability.

### Pilot and release

Before a pilot, freeze the candidate identity, finish the core and triggered profiles for the proposed users, data, and effects, and declare gates, thresholds, and diagnostics before reading results. A pilot is user exposure, not an exemption: narrowing real capability or user/data scope can remove a trigger, but relabelling a triggered risk as a pilot cannot.

Before release or material expansion, run holdout and comparison evidence against the frozen candidate under the declared fixture, evaluator, and trial policy, and read it under [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). Production monitoring adds evidence but never supplies an omitted pre-exposure control or quality claim.

### Operational follow-through

In operation, monitor signals that can detect the selected profiles' material failure modes, keep privacy-appropriate attributable records, and sanitize and confirm a failure before treating it as evidence or a regression case. A credible warning, provider incident, telemetry gap, or drift signal may be inconclusive; investigate or rerun a targeted check rather than counting it as a pass.

### Guarded-live evaluation

Keep offline and shadow work isolated and effect-safe where practicable. Run a guarded-live experiment or user study only when live exposure or effects are genuinely in scope, with the scope record COVERAGE-04 requires; that record is not an approval and cannot replace pre-exposure evidence.

## Requirements

- **CASE-01 — Claim-to-case, profile, and cadence map.** **Applicability:** Every production candidate, before its evidence supports a material design, pilot, release, or change decision. **Requirement:** The accountable owner **MUST** maintain a versioned evaluation plan that maps each in-scope acceptance criterion, prohibited outcome, and material risk-scenario ID to its claim family, case or case family, selected level, evaluator or authoritative observation, suite purpose, lifecycle stage, decision role, accountable owner, and applicable coverage profile. The plan **MUST** identify the evaluated candidate/configuration and material-change impact, and **MUST** record a candidate- and stage-specific rationale whenever a profile that would otherwise appear relevant is `N/A`. **Observable evidence:** A versioned coverage map linked to the candidate identity, case/fixture records, evaluator or state-observation records, profile statuses, owners, and stage/rerun plan.

- **COVERAGE-01 — Universal evidence core.** **Applicability:** Every production candidate and proposed exposure, including a simple read-only assistant. **Requirement:** The evaluation plan **MUST** include one proportional universal core: claim-fit checks for relied-on deterministic rules and interface boundaries; controlled behavior cases for every material user-visible contract claim; contract-defined bounded results for applicable adverse conditions; enforcement-boundary observations for applicable critical controls; an independent holdout when a release claim relies on independence from tuning; retained case, fixture, evaluator or authoritative-observation, outcome, trajectory-when-relevant, and run-status identity; and a predeclared trial and deployed retry/selection/final-result policy when variability can affect a material claim. The core **MUST** exercise each applicable contract-defined time, call, resource, output, or stop bound, including local bounds that do not depend on shared or distributed capacity. **Observable evidence:** The coverage map and attributable run records show the selected core cases, bounds, decision roles, statuses, and any documented reason that repetition is not relevant to a material claim.

- **COVERAGE-02 — Independently triggered profile coverage.** **Applicability:** Whenever a profile trigger in this chapter is true for the candidate and decision scope. **Requirement:** The accountable owner **MUST** select the smallest applicable profile content that establishes each mapped claim and **MUST** map its enabled boundary or relied-on guarantee to claim-fit cases, observations, stages, and the linked canonical owner. The plan **MUST** treat retrieval, tools/trajectory, untrusted input, sensitive/tenant scope, external effects, approvals, durable recovery, conversation, stored memory/context transformation, composition, shared capacity, human impact, model judges, and model selection/routing as independently triggered profiles. It **MUST NOT** infer one profile from another or prescribe an absent submechanism. **Observable evidence:** The versioned profile map identifies each applicable profile's trigger, selected checks, observation source, rerun trigger, owner link, and an objective `N/A` rationale where its trigger is absent.

- **COVERAGE-03 — Stage and material-change cadence.** **Applicability:** Every production candidate, and every change or operational signal reasonably capable of altering a mapped claim, boundary, evidence, use/risk context, or operating assumption. **Requirement:** The evaluation owner **MUST** run claim-fit core and newly triggered-profile evidence during development and change review, complete the applicable pre-exposure evidence before a pilot, and refresh applicable frozen-candidate holdout/comparison evidence before release or material expansion. For a material change, the owner **MUST** assess affected map entries, refresh candidate/configuration provenance, rerun every affected profile, and rerun every still-applicable critical-control case that the changed component can influence. A credible operational signal **MUST** be triaged and attributed before it is counted as evidence; confirmed failures **MUST** enter the applicable sanitized regression process. **Observable evidence:** Stage records show the candidate, changed component or signal, impact assessment, selected reruns, valid/invalid/inconclusive/failure statuses, and handoff to the canonical decision record.

- **COVERAGE-04 — Guarded-live evaluation scope record.** **Applicability:** Only when a guarded-live experiment, user study, shadow exposure with user impact, or other live exposure/effect is proposed as evaluation scope. **Requirement:** Before live evaluation begins, the accountable owner **MUST** record the identified candidate, stated purpose, user and exposure boundary, data and effect boundary, applicable profiles and controls, accountable authority, monitoring signals, stop or rollback conditions, data-handling approach, and intended outcome and harm signals. The record **MUST** distinguish an evaluation conclusion from the separate authorization, approval, readiness, and rollout decisions, and **MUST NOT** substitute guarded-live monitoring for applicable pre-exposure evidence. **Observable evidence:** A versioned live-scope record links the candidate, profile map, boundary and stop conditions, monitoring plan, actual authority references, and subsequent attributable result record.

## Worked example: a scoped plan for the policy assistant

This fictional plan is not executed evidence. The ephemeral, read-only assistant cites approved, current, permission-filtered sources; the controlled London hotel value is **GBP 220**; terminal outcomes are `complete`, `needs_information`, `declined`, and `failed`, plus only contract-defined partial or escalation outcomes.

The model judge is diagnostic only, so its profile supplies no decision evidence. If a change of users or policy scope reveals material differential harm, the human-impact `N/A` expires.

```yaml
subject:
  candidate: "policy-assistant@candidate-current-selection"
  baseline: "policy-assistant@baseline-current-selection"
  fixture_id: "travel-policy-current"
  fixture_revision: "fixture-2026-10-18.1"
  current_document: "travel-policy-2026@2026-10-01"
  superseded_document: "travel-policy-2024-superseded@2024-01-01"
  fictional_current_london_hotel_value: "GBP 220"
  execution: "ephemeral, read-only, no persisted memory, no approval, no delegated agents"

profiles:
  universal_core: applies
  approved_retrieval: applies
  tools_trajectory: applies
  untrusted_input: applies
  sensitive_tenant_scope: applies
  external_effects: "N/A — no write, send, purchase, publish, or other external effect"
  human_approvals: "N/A — no approval-required action"
  durable_recovery: "N/A — no resumable or recoverable work"
  conversation: "N/A — single bounded request"
  stored_memory_context: "N/A — no stored memory, cache, summary, or context transformation"
  composition: "N/A — no delegated or remote agent"
  shared_capacity: "N/A — no shared-capacity claim; local stop bounds remain core evidence"
  human_impact: "N/A — fictional scope has a recorded screen with no identified trigger"
  model_judges: "diagnostic only — not decision or release evidence"
  model_selection_routing: applies

claims:
  - id: "TASK-POLICY-CURRENT"
    cases: ["POLICY-CURRENT-001", "POLICY-PARAPHRASE-007"]
    expected: "complete; GBP 220; current permitted source supports the answer"
    observations: ["source-permission-check@v1", "grounded-policy-human-rubric@v1"]
  - id: "CTRL-POLICY-SOURCE-SCOPE"
    cases: ["POLICY-DENIED-005", "POLICY-INJECTION-006"]
    expected: "no restricted retrieval or disclosure; terminal outcome follows contract"
    observations: ["trajectory-boundary-check@v1", "source-permission-check@v1"]
  - id: "ROBUST-POLICY-EVIDENCE"
    cases: ["POLICY-STALE-002", "POLICY-MISSING-003", "POLICY-CONFLICT-004", "POLICY-EXHAUSTION-008"]
    expected: "no invented definitive amount when permitted evidence is absent or conflicts"
    relations:
      invariance: "reviewed paraphrase in POLICY-PARAPHRASE-007"
      sensitivity: "permission loss and two current approved conflicting policies"

release_holdout:
  suite: "policy-release-holdout@v1"
  case: "POLICY-HOLDOUT-009"
  fixture: "separate authored holdout fixture; not one of the development/regression cases"
  rule: "not used to tune the candidate, rule, or rubric it reports on"

evaluator_status:
  diagnostic_only: ["grounding-judge@v1"]
  decision_evidence: ["source-permission-check@v1", "grounded-policy-human-rubric@v1", "trajectory-boundary-check@v1"]
```

`POLICY-STALE-002` checks the superseded document is treated as superseded; `POLICY-CONFLICT-004` and `POLICY-MISSING-003` expect an uncertainty or escalation outcome, not an invented amount. `POLICY-DENIED-005` separates the boundary's denial from the withholding response; `POLICY-INJECTION-006` checks a harmless injected instruction neither became authority nor caused disclosure. Permitted counterparts keep blanket refusal from looking safe, and the relation cases add to, not replace, correct-outcome checks.

If a later variant adds a human-approved policy update, the record changes before exposure: external-effect, approval, and durable-recovery profiles are selected independently, observing the exact approved subject, authorization, invocation, and authoritative final state. The read-only example establishes none of these.

## Evidence and checklist

- [ ] Every `N/A` gives an absent trigger, not cost, rarity, a pilot label, a missing mechanism, or vendor ownership.
- [ ] Declared local bounds are tested even without a shared-capacity system.
- [ ] Diagnostics stay distinct from gates and thresholds.
- [ ] No attributable failure is relabelled a harness defect or offset by an aggregate.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
[3]: https://developers.openai.com/api/docs/guides/evaluation-best-practices "OpenAI Evaluation Best Practices"
[4]: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition "NIST CAISI: Insights into AI Agent Security from a Large-Scale Red-Teaming Competition"

# 4.6 Standards, Required Coverage, and Execution Cadence

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, accountable owners, security/privacy reviewers, and release reviewers  
**Applicability:** Every production candidate and every design, pilot, release, or change decision that relies on its evaluation evidence.  
**Reader question:** What is mandatory for this agent and this change, and when must it run?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.5 Planning, Designing, and Running Tests and Evaluations](05-planning-designing-and-running-tests-and-evaluations.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Part 4 practical reference](reference/README.md)

## Purpose and boundary

This chapter says **what evidence is needed and when it is refreshed**. Every production candidate starts with one small evidence core; add profiles only for capabilities, risks, claims, and exposure actually in scope. A profile is not an architecture bundle: a simple read-only assistant does not gain a queue, approval flow, persistent store, second agent, or model judge just because it is evaluated.

The catalogue and the absence of a universal pass rate, trial count, or calibration cutoff are this playbook's own choices. NIST guidance supports risk-led, documented measurement before deployment and during operation, with measures proportionate to context.[1] Each selected profile documents its trigger and evidence rather than a generic checklist.

Methods for cases, fixtures, evaluators, behavioral properties, and release conclusions are in [4.2](02-test-levels-techniques-and-suite-purposes.md) through [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). This chapter names a profile and its evidence objective and does not copy their rules.

## Reading a coverage record

A coverage record links a claim to the smallest evidence set that can establish it. It records the candidate and configuration; claim family and decision role; case, fixture, evaluator or authoritative observation; level and stage; owner; applicable profiles; and the reason any seemingly relevant profile is not applicable. It is a map, not a scorecard.

Keep three kinds of result apart:

- A **required check** establishes a contract, control, or evidence obligation, and is read under the decision policy.
- A **quality threshold** is a predeclared acceptance or comparison value for a task, slice, resource, or operating claim. The policy owner sets it; this chapter gives no number.
- A **diagnostic signal** helps investigate, prioritize, or find failure modes. An exploratory transcript, similarity score, or model judge without established fitness for the exact claim is diagnostic, not gating.

A favorable average or unrelated metric cannot make up for a failed critical control or missing valid evidence. Gates, metrics, diagnostics, insufficient evidence, and `go`/`conditional_go`/`no_go` are classified in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md); a profile record points there instead of turning a quality score into a release decision.

### The universal evidence core

Every production candidate starts with a bounded contract and an evidence map. The core covers each material user-visible claim and its terminal outcomes, relied-on deterministic rules and real boundaries, adverse conditions the contract makes relevant, and each applicable critical control at its enforcement boundary. It keeps subject, case, fixture, evaluator or state-observation identity, outcome, relevant trajectory observation, and run status, so a reader can tell a candidate failure from invalid or inconclusive evidence.

It also covers the contract-defined time, call, resource, output, and stopping bounds. This holds for a local read-only assistant with one bounded request as much as for a system with shared queues; checking a declared local bound or safe exhaustion needs no distributed load environment. A capacity profile is added only when a shared resource or capacity claim is in scope.

For material variable behavior, the core identifies the trial policy and the deployed retry, selection, fallback, and final-result policy needed to read the claim. Where a release claim relies on independence from tuning, it includes an independent holdout. For semantic input, changeable evidence, or policy, permission, currentness, or user-constraint decisions, [4.3](03-evaluation-types-and-dimensions.md) sets the invariance and sensitivity evidence. Repeated attempts, safe alternative trajectories, and a final selected answer answer different questions; none shows a field failure rate of zero.

## Additive profiles

Select a profile because its **trigger is true for this candidate and decision scope**, not because the name sounds thorough. For each selected profile, the coverage map names the enabled boundary or relied-on guarantee, cases and observation, stage, and owner chapter. A profile is `N/A` only when its trigger is absent for the named candidate and stage; `N/A` is not a pass or a general waiver. Missing telemetry, an unimplemented control, cost, rarity, vendor ownership, or a "pilot" label are evidence gaps or scope decisions, not `N/A` reasons.

The profiles are independent. Retrieval does not imply stored memory. A route or fallback does not imply a model judge. Resumable read-only work does not imply an external write or approval. A queue alone does not imply resumable recovery.

### Approved retrieval

**Trigger:** A curated corpus, search, cached source, policy or document source, or a claim about provenance, relevance, coverage, admission, freshness, or currentness affects an outcome.

**Evidence focus:** Observe source admission and requester scope; source identity, revision, and currentness; missing, stale, and conflicting evidence; and the bounded result when support is absent. Use an evaluator suited to semantic support when grounding is claimed; a citation identifier or source metadata does not show an assertion is supported. Include any cache, index, reranker, or transformation that can affect access or currentness.

**When to run:** Controlled offline evidence before pilot or release, and after a corpus, source-admission, index, reranker, cache, filter, query transformation, or freshness-policy change.

**Owner:** Retrieval and context mechanics: [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md). Grounding evaluation: [4.4](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No source retrieval, cache, provenance, freshness, or source-backed answer claim is in scope.

### Tools and trajectory

**Trigger:** An admitted tool, interface, plug-in, code executor, remote capability, or model-selected action contributes to the outcome.

**Evidence focus:** Exercise permitted selection where it matters, security-relevant arguments, identity propagation, enforcement-time authorization, error/timeout/partial-result handling, necessary ordering, provenance, retry/stop behavior, and forbidden invocations. Record model proposal, trusted-boundary decision, actual execution, and disclosure separately when each matters. A blocked request is not an executed effect; a fluent final response does not show an authorization boundary operated.

**When to run:** Before exposure, and after an interface inventory, schema, permission, identity, orchestration, retry, dependency, or tool-selection change.

**Owner:** Controls: [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md), [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), and [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). Outcome and trajectory evidence: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No admitted interface or model-selected action is in scope.

### Untrusted input

**Trigger:** User input, retrieved material, tool output, email, web material, memory, peer content, or another untrusted channel reaches model context or downstream rendering.

**Evidence focus:** Exercise direct and channel-correct indirect injection, instruction/data separation, relevant encoding or transformation paths, output and tool-boundary validation, attempted disclosure or action, and a benign task. Use harmless fixtures and instrumented destinations when an attempted action or disclosure would otherwise be unsafe. A clean response or absent telemetry does not show containment, and OWASP treats injection tests as one layer, not a security benchmark.[2] Fixed cases show only that known attacks fail. Evidence of resistance needs adaptive or red-team attacks that iterate against the system; in a public competition of over 250,000 attempts against 13 frontier models, every model was hijacked at least once.[4]

**When to run:** Before exposure, and after a context channel, retrieval, rendering, prompt, model, boundary, or transformation change.

**Owner:** Controls: [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). Cases and observations: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No untrusted content reaches context or rendering. A narrow user request is covered by the core only if it creates no extra untrusted-content boundary claim.

### Sensitive data and tenant scope

**Trigger:** Personal, confidential, regulated, tenant-scoped, privileged, non-public, derived, or logged data is reachable, or its isolation is claimed.

**Evidence focus:** Observe trusted identity and entitlement propagation, cross-scope isolation, output and telemetry minimization or redaction where claimed, retention or expiry where applicable, and denied and failure paths. Synthetic or minimized fixtures can establish basic boundary behavior; real customer material is not a prerequisite.

**When to run:** Before pilot or release, and after identity, source, data handling, logging, routing, permission, or retention changes.

**Owner:** [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), with specialized assurance in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md). Boundary evidence: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The candidate cannot reach or derive protected data and makes no isolation claim.

### External effects

**Trigger:** The candidate can initiate or request a write, send, purchase, publish, deploy, delete, identity change, or another external state change.

**Evidence focus:** Observe validated intent and exact target/parameter scope, execution-time authorization, pre-effect checks, timeout or unknown-outcome handling, duplicate/retry behavior, and authoritative target state or receipt. A denied or simulated action leaves no effect. A blocked proposal is not an unauthorized execution.

**When to run:** Before exposure, and after an effect interface, target, authorization, payload, retry, reconciliation, or action-path change.

**Owner:** [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); behavioral evidence: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The candidate cannot initiate or request an external state change.

### Human approvals

**Trigger:** A governing policy requires human approval before a consequential action.

**Evidence focus:** Observe the preview and immutable action subject, approver authority and scope, target/parameter binding, expiry, revocation or material-change invalidation, one-time use or replay protection, interruption or escalation, and execution-time authorization after approval. Approval adds a condition to an authorized action; it does not enlarge authority.

**When to run:** Before exposure, and after an approval policy, payload, authority, expiry, execution, or action-path change.

**Owner:** [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md); trajectory evidence: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No approval-required consequential action is in scope.

### Durable recovery

**Trigger:** Work is resumable, long-running, queued for recovery, approval-waiting, recoverable after interruption, or otherwise depends on durable state.

**Evidence focus:** Observe durable state identity and isolation, suspension/resume, replay or retry, cancellation, timeout/partial/unknown outcomes, controlled interruption recovery, compatibility, and, only where effects exist, duplicate prevention, idempotency, or reconciliation. A successful resume does not show exactly-once external effects.

**When to run:** Before exposure, and after persistence, checkpoint, recovery, retry, compatibility, or durable-state changes.

**Owner:** [7.1 Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md); effect or approval evidence stays with its own profile.

**N/A:** The work is ephemeral and non-resumable. A queue without a recovery claim does not select this profile.

### Conversation

**Trigger:** Multi-turn interaction, session history, or a task horizon across turns can affect behavior.

**Evidence focus:** Evaluate a bounded episode: milestones, retained material constraints, forbidden events, terminal outcome, and turn, time, or budget limits. Test loss or contradiction of a material constraint when plausible. Do not require private reasoning traces.

**When to run:** Before exposure, and after a conversation contract, session lifecycle, task-horizon, instruction, or turn-management change.

**Owner:** [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) and [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md); episode behavior: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The evaluated interaction is a single bounded request with no behaviorally relevant cross-turn state.

### Stored memory and context transformation

**Trigger:** Stored memory, summaries, caches that affect answers, context selection, compression, or another input-to-context transformation can affect behavior.

**Evidence focus:** Observe session or tenant scope, provenance through the transformation, expiry/deletion or retention where claimed, poisoning resistance, loss or distortion of material constraints, context sensitivity, and safe absence, corruption, or limit behavior. Test the claims actually made; retrieval alone does not show stored memory.

**When to run:** Before exposure, and after a memory schema, retention rule, cache, summary, context-selection, transformation, or task-horizon change.

**Owner:** [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md); behavioral claims: [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No stored state, cache, summary, or context transformation affects the evaluated behavior. Conversation alone does not make deletion testing applicable.

### Composition

**Trigger:** Two or more model-driven agents, or a remote-agent interaction, contribute to one outcome.

**Evidence focus:** Exercise handoff and routing contracts, identity and source propagation, delegated scope, least privilege, denial propagation, malformed or malicious peer content, loop limits, failure/timeout containment, and the end-to-end outcome. Passing component cases do not show the composed system keeps its boundary.

**When to run:** Before exposure, and after a topology, member, handoff, remote-interface, or shared-contract change.

**Owner:** [Part 9](../../engineering-reference/09-multi-agent-systems-and-interoperability/README.md); system paths are evaluated through [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** One model-driven agent produces the outcome and no remote-agent interaction is enabled.

### Shared capacity and resource performance

**Trigger:** Shared queues, caches, quotas, rate or concurrency limits, budgets, common downstream capacity, or a shared-resource availability/fairness claim can affect correctness, safety, tenant fairness, or availability.

**Evidence focus:** Observe admission and limit enforcement, claimed isolation, queue/retry/backoff behavior, fail-safe exhaustion, claimed resource/call/cost/latency bounds, and truthful user-facing degradation. The profile is proportional: no distributed load infrastructure for a small local assistant, and its absence does not remove the core's duty to test the declared local stop or resource bounds.

**When to run:** Before exposure, and after a limit, capacity, provider, queue, cache, admission, shared-budget, or shared-resource change.

**Owner:** [5.1 Observability, Budgets, and Operational Control](../05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md); capacity engineering: [8.3 Cost, Latency, and Performance Optimization](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md) and [8.4 Capacity, Admission Control, and Backpressure](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md). Thresholds: [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** No shared resource or shared-capacity claim can affect the evaluated behavior. Record any local bound under the core.

### Human impact and domain assurance

**Trigger:** The risk record identifies material differential harm by population, domain, language, role, geography, entitlement, accessibility, or jurisdiction, or an external policy calls for additional assurance.

**Evidence focus:** Keep the harm screen; pick justified slices with appropriate expertise; compare like entitlement and task when equality is the claim; keep legitimate policy differences; report task and control outcomes separately. Add domain review, representative-user work, accessibility, appeal/override, or higher-assurance evidence only where use and risk call for it. A small curated slice can expose a defect but gives no population rate.

**When to run:** Before release, and after a material use, user, data, capability, domain, or risk-context change.

**Owner:** Screen and slice evidence: [4.3](03-evaluation-types-and-dimensions.md); detailed assurance: [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

**N/A:** The recorded screen identifies no material differential-harm or domain-assurance trigger for the named scope. Review again when scope changes.

### Model judges

**Trigger:** A model-based evaluator supplies decision- or release-facing evidence.

**Evidence focus:** Keep the versioned rubric, known pass/fail anchors, human-reviewed held-out calibration for the target claim and risk slices, false passes, disagreements, unscorable cases, and sensitivity to order, style, reference leakage, or injection. Rubric-based judges with human spot-checks are a normal way to grade at scale. A judge stays diagnostic until fitness for the exact decision role is documented. This is about the evaluator, not model routing.

**When to run:** Establish fitness before using the judge for the stated decision, and reassess after a material judge, rubric, context, model, target-distribution, or target-claim change. Public guidance likewise treats grader usefulness as context-dependent.[3]

**Owner:** [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No model judge supplies decision- or release-facing evidence. Label a retained diagnostic judge as diagnostic; do not promote it to a gate.

### Model selection, routing, and fallback

**Trigger:** A selected model, provider, settings, route, fallback, or degradation policy can change task behavior, data handling, controls, or operating limits.

**Evidence focus:** Exercise the actual end-to-end selection, routing, retry, fallback, and final-delivery policy; record resolved identities; and establish each enabled path's contract, privacy, control, quality, latency, cost, and recovery behavior. An alternate path may differ only under a declared contract rule. A route does not require a model judge.

**When to run:** Before exposure, and after a selection, provider, configuration, routing, fallback, retry, or degradation change.

**Owner:** [8.1 Model Selection, Parameters, and Routing](../../engineering-reference/08-model-context-and-resource-engineering/01-model-selection-parameters-and-routing.md); candidate provenance and comparison: [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** No selection, routing, fallback, provider, or settings choice beyond the frozen candidate identity can affect the claim. Do not use this when a hidden or enabled alternate path can affect behavior.

## Cadence from development through operation

### Production preparation

During development, use the narrowest claim-fit checks: focused deterministic and component checks for relied-on rules, representative behavior cases for changed behavior, and one focused boundary case for a newly enabled risk. Development cases can change during iteration; after tuning they are not an independent holdout. Keep capability suites (hard tasks, low pass rate expected) apart from regression suites (stable behavior, near-100% expected). When a capability suite saturates, move its stable cases to regression and add harder ones.

### Change review

A material change is any change reasonably capable of altering a mapped claim, enforcement boundary, evidence, use/risk context, or operating assumption. Examples: an instruction; a model, provider, settings, route, or fallback change; an interface schema, permission, credential, target, or effect change; a source, corpus, index, or cache change; identity or authorization; user or domain; context, memory, retention, retry, approval, durable-state, composition, capacity, evaluator, rubric, threshold, or dependency-environment change. "Prompt-only," vendor-owned, rare, expensive, and "already a pilot" are not reasons to skip.

For a material change, refresh the candidate provenance, assess the affected map entries, rerun each affected profile, and rerun every still-applicable critical-control case the changed component can influence. When a change makes a profile newly applicable (enabling retrieval, storing memory, adding an effect, turning on an approval path or fallback, expanding protected data, or adding another agent), complete that profile before exposing the new capability.

### Pilot and release

Before a pilot, freeze the candidate identity, finish the core and triggered profiles for the proposed users, data, and effects, and declare gates, thresholds, and diagnostics before reading results. A pilot is user exposure, not an exemption. Narrowing a real capability or user/data scope can remove a trigger; relabelling a triggered risk as a pilot cannot.

Before release or a material expansion, run the holdout and comparison evidence against the frozen candidate under the declared fixture, evaluator, and trial policy. The release owner then reads the result under [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). Production monitoring adds to this evidence; it does not supply an omitted pre-exposure control or quality claim.

### Operational follow-through

In operation, monitor signals that can detect the selected profiles' material failure modes. Keep privacy-appropriate attributable records and triage reports, and sanitize and confirm a failure before treating it as evaluation evidence or a regression case. A credible warning, provider incident, telemetry gap, or drift signal may be inconclusive; investigate or rerun a targeted check instead of counting it as a pass. Confirmed failures go through the regression and decision process in [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

### Guarded-live evaluation

Keep offline and shadow work isolated and effect-safe where practicable. A guarded-live experiment or user study makes sense only when live exposure or effects are genuinely in scope. Its scope record makes the exposure clear: candidate, purpose, users, data, effect boundary, monitoring, stop or rollback condition, outcome and harm signals, and accountable authority. The record is not an approval, and it cannot replace evidence needed before exposure.

## Requirements

- **CASE-01 — Claim-to-case, profile, and cadence map.** **Applicability:** Every production candidate, before its evidence supports a material design, pilot, release, or change decision. **Requirement:** The accountable owner **MUST** maintain a versioned evaluation plan that maps each in-scope acceptance criterion, prohibited outcome, and material risk-scenario ID to its claim family, case or case family, selected level, evaluator or authoritative observation, suite purpose, lifecycle stage, decision role, accountable owner, and applicable coverage profile. The plan **MUST** identify the evaluated candidate/configuration and material-change impact, and **MUST** record a candidate- and stage-specific rationale whenever a profile that would otherwise appear relevant is `N/A`. **Observable evidence:** A versioned coverage map linked to the candidate identity, case/fixture records, evaluator or state-observation records, profile statuses, owners, and stage/rerun plan.

- **COVERAGE-01 — Universal evidence core.** **Applicability:** Every production candidate and proposed exposure, including a simple read-only assistant. **Requirement:** The evaluation plan **MUST** include one proportional universal core: claim-fit checks for relied-on deterministic rules and interface boundaries; controlled behavior cases for every material user-visible contract claim; contract-defined bounded results for applicable adverse conditions; enforcement-boundary observations for applicable critical controls; an independent holdout when a release claim relies on independence from tuning; retained case, fixture, evaluator or authoritative-observation, outcome, trajectory-when-relevant, and run-status identity; and a predeclared trial and deployed retry/selection/final-result policy when variability can affect a material claim. The core **MUST** exercise each applicable contract-defined time, call, resource, output, or stop bound, including local bounds that do not depend on shared or distributed capacity. **Observable evidence:** The coverage map and attributable run records show the selected core cases, bounds, decision roles, statuses, and any documented reason that repetition is not relevant to a material claim.

- **COVERAGE-02 — Independently triggered profile coverage.** **Applicability:** Whenever a profile trigger in this chapter is true for the candidate and decision scope. **Requirement:** The accountable owner **MUST** select the smallest applicable profile content that establishes each mapped claim and **MUST** map its enabled boundary or relied-on guarantee to claim-fit cases, observations, stages, and the linked canonical owner. The plan **MUST** treat retrieval, tools/trajectory, untrusted input, sensitive/tenant scope, external effects, approvals, durable recovery, conversation, stored memory/context transformation, composition, shared capacity, human impact, model judges, and model selection/routing as independently triggered profiles. It **MUST NOT** infer one profile from another or prescribe an absent submechanism. **Observable evidence:** The versioned profile map identifies each applicable profile's trigger, selected checks, observation source, rerun trigger, owner link, and an objective `N/A` rationale where its trigger is absent.

- **COVERAGE-03 — Stage and material-change cadence.** **Applicability:** Every production candidate, and every change or operational signal reasonably capable of altering a mapped claim, boundary, evidence, use/risk context, or operating assumption. **Requirement:** The evaluation owner **MUST** run claim-fit core and newly triggered-profile evidence during development and change review, complete the applicable pre-exposure evidence before a pilot, and refresh applicable frozen-candidate holdout/comparison evidence before release or material expansion. For a material change, the owner **MUST** assess affected map entries, refresh candidate/configuration provenance, rerun every affected profile, and rerun every still-applicable critical-control case that the changed component can influence. A credible operational signal **MUST** be triaged and attributed before it is counted as evidence; confirmed failures **MUST** enter the applicable sanitized regression process. **Observable evidence:** Stage records show the candidate, changed component or signal, impact assessment, selected reruns, valid/invalid/inconclusive/failure statuses, and handoff to the canonical decision record.

- **COVERAGE-04 — Guarded-live evaluation scope record.** **Applicability:** Only when a guarded-live experiment, user study, shadow exposure with user impact, or other live exposure/effect is proposed as evaluation scope. **Requirement:** Before live evaluation begins, the accountable owner **MUST** record the identified candidate, stated purpose, user and exposure boundary, data and effect boundary, applicable profiles and controls, accountable authority, monitoring signals, stop or rollback conditions, data-handling approach, and intended outcome and harm signals. The record **MUST** distinguish an evaluation conclusion from the separate authorization, approval, readiness, and rollout decisions, and **MUST NOT** substitute guarded-live monitoring for applicable pre-exposure evidence. **Observable evidence:** A versioned live-scope record links the candidate, profile map, boundary and stop conditions, monitoring plan, actual authority references, and subsequent attributable result record.

## Worked example: a scoped plan for the policy assistant

This fictional planning record is not executed evidence. The policy assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources with citations, with no persisted memory, approval, external write, or delegated agent. The current London hotel value in the controlled source is **GBP 220**. Its terminal outcomes are `complete`, `needs_information`, `declined`, and `failed`, plus only contract-defined partial or escalation outcomes.

The plan selects the core, approved-retrieval, tools/trajectory, untrusted-input, sensitive/tenant-scope, and model-selection/routing profiles. A model judge is diagnostic only, so the model-judge profile is not used for decision evidence. The effect, approval, durable-recovery, conversation, stored-memory/context, composition, and shared-capacity profiles are `N/A` for this scope, with reasons. The human-impact screen is recorded; if it finds material differential harm when users or policy scope change, its `N/A` expires and the profile is added.

```yaml
# Fictional coverage plan excerpt. It is not an executed result or universal threshold.
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

`POLICY-CURRENT-001` establishes the ordinary current-source claim: the answer is `complete`, states GBP 220, and identifies `travel-policy-2026` at revision `"2026-10-01"`. `POLICY-STALE-002` verifies that `travel-policy-2024-superseded` at revision `"2024-01-01"` is recognized as superseded and not equal authority. In `POLICY-CONFLICT-004`, two current approved policies disagree, so it expects an uncertainty or escalation outcome, not an invented amount. `POLICY-MISSING-003` makes the same point for absent permitted evidence.

The trajectory observation for `POLICY-DENIED-005` separates the denied source-boundary decision from the response: the response withholds restricted material, and the boundary record shows whether retrieval was refused. `POLICY-INJECTION-006` puts a harmless instruction conflict in the untrusted channel under test and observes that it did not become authority or cause restricted disclosure. These cases include permitted counterpart work, so blanket refusal cannot look like safe success.

Because the assistant takes semantic language and depends on current, permission-filtered evidence, `POLICY-PARAPHRASE-007` is a reviewed irrelevant-change relation and the permission-loss and current-policy-conflict cases are relevant-change relations. They add to, not replace, the correct-outcome checks. The trial policy is in the practical reference and release interpretation is in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md); the example assigns no trial count or pass rate.

If a later variant adds a human-approved policy update, the record changes before exposure: external-effect, approval, and durable-recovery profiles are selected independently, and evidence observes the exact approved subject, authorization, invocation, and authoritative final state. The read-only example cannot establish any of those claims.

## Evidence and checklist

Use this to review the coverage map and cadence, not to replace the method or decision chapters.

- [ ] The candidate configuration and decision stage are identifiable, and every acceptance criterion, prohibited outcome, and risk scenario maps to claims, cases, observations, owners, and stages.
- [ ] The core covers contract outcomes, relied-on rules and boundaries, adverse outcomes, critical controls, evidence identity and status, and declared local bounds even without a shared-capacity system.
- [ ] Every selected profile states its trigger, boundary or guarantee, observation, rerun trigger, and owner; no profile is inferred from another.
- [ ] Every `N/A` names the candidate and stage and explains why the trigger is absent, not cost, rarity, a pilot label, a missing mechanism, or vendor ownership.
- [ ] The trial, retry, selection, fallback, and final-result policy matches the behavior assessed; diagnostics stay distinct from gates and thresholds.
- [ ] Development cases stay separate from the independent holdout, capability and regression suites are kept apart, and a material change reruns affected profiles plus influenced critical controls.
- [ ] Invalid and inconclusive records stay visible; a real attributable failure is not relabelled a harness defect or offset by an aggregate score.
- [ ] Any guarded-live scope record names exposure, data/effect boundaries, monitoring, stop/rollback conditions, and accountable authority, and does not replace pre-exposure evidence.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
[3]: https://developers.openai.com/api/docs/guides/evaluation-best-practices "OpenAI Evaluation Best Practices"
[4]: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition "NIST CAISI: Insights into AI Agent Security from a Large-Scale Red-Teaming Competition"

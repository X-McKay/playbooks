# 4.6 Standards, Required Coverage, and Execution Cadence

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, accountable owners, security/privacy reviewers, and release reviewers  
**Applicability:** Every production candidate and every material design, pilot, release, or change decision that relies on its evaluation evidence.  
**Reader question:** What is mandatory for this agent and this change, and when must it run?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.5 Planning, Designing, and Running Tests and Evaluations](05-planning-designing-and-running-tests-and-evaluations.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Part 4 practical reference](reference/README.md)

## Purpose and boundary

This chapter is the Part 4 locator for **what evidence is needed and when it is refreshed**. It starts every production candidate with one small evidence core, then adds profiles only for capabilities, risks, claims, and proposed exposure that are actually in scope. A profile is not an architecture bundle: a simple read-only assistant does not acquire a queue, an approval flow, a persistent store, a second agent, or a model judge merely because it is being evaluated.

This is proposed playbook policy, not a claim that an external framework imposes this exact catalogue or a universal pass rate, trial count, calibration cutoff, or live-study rule. NIST guidance supports risk-led, documented measurement before deployment and during operation, while leaving the particular measures proportionate to the context. [1] The selected profile therefore documents its trigger and evidence rather than substituting a generic checklist for a claim.

The chapter does not redefine how to design cases and fixtures, select evaluators, assess behavioral properties, or reach a release conclusion. Those methods remain owned by [4.2](02-test-levels-techniques-and-suite-purposes.md) through [4.5](05-planning-designing-and-running-tests-and-evaluations.md), and decision treatment remains owned by [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). In particular, this chapter identifies a profile and its evidence objective; it does not copy method-specific rules from security, execution, context, composition, or release chapters.

## Reading a coverage record

A coverage record connects a claim to the smallest evidence set capable of establishing it. It records the candidate and configuration being assessed; the claim family and decision role; the case, fixture, evaluator or authoritative observation; the level and stage; the accountable owner; applicable profiles; and the reason a seemingly relevant profile is not applicable. It is a map, not a scorecard.

Keep three kinds of result separate before evidence is read:

- A **required check** establishes a contract, control, or evidence obligation. Its outcome is interpreted under the applicable decision policy.
- A **quality threshold** is a predeclared acceptance or comparison value for a particular task, slice, resource, or operating claim. The accountable policy owner sets it; this chapter supplies no universal number.
- A **diagnostic signal** helps investigate, prioritize cases, or find failure modes. An exploratory transcript, similarity score, or model judge that has not established fitness for the exact claim is diagnostic, not release-gating evidence.

Critical controls and required valid evidence are not compensable by a favorable average or an unrelated task metric. The canonical classification of gates, metrics, diagnostics, insufficient evidence, and `go`/`conditional_go`/`no_go` remains in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). A profile record should point to that owner rather than silently turn a quality score into authorization or a release decision.

### The universal evidence core

Every production candidate starts with a bounded contract and an evidence map. The core covers each material user-visible claim and its declared terminal outcomes, the relied-on deterministic rules and real boundaries, adverse conditions that the contract makes relevant, and each applicable critical control at its enforcement boundary. It retains subject, case, fixture, evaluator or state-observation identity, outcome, relevant trajectory observation, and run status so a reader can tell a candidate failure from invalid or inconclusive evidence.

The core also covers the candidate's contract-defined time, call, resource, output, and stopping bounds where they apply. This is true for a local read-only assistant with a single bounded request as well as for a system with shared queues or capacity controls. A distributed load environment is not the prerequisite for checking a declared local bound or safe exhaustion behavior. Conversely, a capacity profile is added only when a shared resource or capacity claim is actually in scope.

For material variable behavior, the core identifies the trial and deployed retry, selection, fallback, and final-result policy needed to interpret the claim. Where a release claim depends on independence from tuning, it includes an independent holdout. For semantic input, changeable evidence, or policy, permission, currentness, or user-constraint decisions, [4.3](03-evaluation-types-and-dimensions.md) determines the required invariance and relevant-change sensitivity evidence. Repeated attempts, safe alternative trajectories, and a final selected answer answer different questions; none is proof that a field failure rate is zero.

## Additive profiles

Select a profile because its **trigger is true for this candidate and decision scope**, not because its name sounds thorough. For each selected profile, the coverage map identifies the enabled boundary or relied-on guarantee, cases and observation, stage, and owner chapter. A profile is `N/A` only when its trigger is absent for the named candidate and stage; it is neither a pass nor a general waiver. Missing telemetry, an unimplemented control, cost, rarity, vendor ownership, or a label such as “pilot” are evidence gaps or scope decisions, not `N/A` reasons.

The following profiles are independent. A retrieval profile does not imply stored memory. A route or fallback profile does not imply a model judge. Resumable read-only work does not imply an external write or an approval. A queue alone does not establish resumable recovery.

### Approved retrieval

**Trigger:** A curated corpus, search, cached source, policy or document source, or a claim about provenance, relevance, coverage, admission, freshness, or currentness affects an outcome.

**Evidence focus:** Observe source admission and requester scope; source identity, revision, and currentness; missing, stale, and conflicting evidence; and the bounded result when support is absent. Use an evaluator suited to semantic support when grounding is claimed: a citation identifier or source metadata alone does not establish that an assertion is supported by source text. Include a cache, index, reranker, or transformation in the controlled evidence when it can affect access or currentness.

**When to run:** Use controlled offline evidence before pilot or release and after a corpus, source-admission, index, reranker, cache, filter, query transformation, or freshness-policy change.

**Owner:** The profile map is owned here; retrieval/context mechanics are owned by [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md); grounding evaluation is owned by [4.4](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No source retrieval, cache, provenance, freshness, or source-backed answer claim is in the evaluated scope.

### Tools and trajectory

**Trigger:** An admitted tool, interface, plug-in, code executor, remote capability, or model-selected action contributes to the outcome.

**Evidence focus:** Exercise the permitted selection where selection is material, security-relevant arguments, identity propagation, enforcement-time authorization, error/timeout/partial-result handling, necessary ordering, provenance, retry/stop behavior, and forbidden invocations. Record model proposal or compliance, trusted-boundary decision, actual execution, and disclosure separately when each matters. A blocked request is not evidence of an executed external effect; a fluent final response is not proof that an authorization boundary operated.

**When to run:** Run before exposure and after an interface inventory, schema, permission, identity, orchestration, retry, dependency, or tool-selection change.

**Owner:** Detailed tool and trust-boundary controls are owned by [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md), [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), and [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). Outcome and trajectory evidence are owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No admitted interface or model-selected action is in the candidate's evaluated scope.

### Untrusted input

**Trigger:** User input, retrieved material, tool output, email, web material, memory, peer content, or another untrusted channel reaches model context or downstream rendering.

**Evidence focus:** Exercise direct and channel-correct indirect injection, instruction/data separation, relevant encoding or transformation paths, output and tool-boundary validation, attempted disclosure or action, and a benign task. Use harmless fixtures and instrumented destinations when an attempted action or disclosure would otherwise be unsafe. A clean response or absent telemetry does not by itself establish containment; OWASP likewise treats injection tests as one layer rather than a security benchmark. [2]

**When to run:** Run before exposure and after a context channel, retrieval, rendering, prompt, model, boundary, or transformation change.

**Owner:** Detailed controls are owned by [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md); cases and observations are owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No untrusted content reaches context or rendering in the evaluated scope. A narrowly bounded user request can be covered by the core only when it does not create an additional untrusted-content boundary claim.

### Sensitive data and tenant scope

**Trigger:** Personal, confidential, regulated, tenant-scoped, privileged, non-public, derived, or logged data is reachable or its isolation is claimed.

**Evidence focus:** Observe trusted identity and entitlement propagation, cross-scope isolation, output and telemetry minimization or redaction where claimed, retention or expiry where applicable, and denied and failure paths. Synthetic or approved minimized fixtures can establish basic boundary behavior; access to real customer material is not a prerequisite for it.

**When to run:** Run before pilot or release and after identity, source, data handling, logging, routing, permission, or retention changes.

**Owner:** Data-handling controls are owned by [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), with applicable specialized assurance in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md). Boundary evidence is owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The evaluated candidate cannot reach or derive non-public, tenant-scoped, privileged, or otherwise protected data, and makes no isolation claim.

### External effects

**Trigger:** The candidate can initiate or request a write, send, purchase, publish, deploy, delete, identity change, or another external state change.

**Evidence focus:** Observe validated intent and exact target/parameter scope, execution-time authorization, pre-effect checks, timeout or unknown-outcome handling, duplicate/retry behavior, and authoritative target state or receipt. A denied or simulated action should leave no effect. Do not equate a blocked proposal with an unauthorized execution.

**When to run:** Run before exposure and after an effect interface, target, authorization, payload, retry, reconciliation, or action-path change.

**Owner:** Effect and unknown-outcome mechanics are owned by [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); behavioral evidence is owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The candidate cannot initiate or request an external state change in the evaluated scope.

### Human approvals

**Trigger:** A governing policy requires human approval before a consequential action.

**Evidence focus:** Observe the preview and immutable action subject, approver authority and scope, target/parameter binding, expiry, revocation or material-change invalidation, one-time use or replay protection, interruption or escalation, and execution-time authorization after approval. Approval adds a condition to an authorized action; it does not enlarge authority.

**When to run:** Run before exposure and after an approval policy, payload, authority, expiry, execution, or action-path change.

**Owner:** Approval and suspension mechanics are owned by [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md); trajectory evidence is owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No approval-required consequential action is in the candidate's evaluated scope.

### Durable recovery

**Trigger:** Work is resumable, long-running, queued for recovery, approval-waiting, recoverable after interruption, or otherwise depends on durable state.

**Evidence focus:** Observe durable state identity and isolation, suspension/resume, replay or retry, cancellation, timeout/partial/unknown outcomes, controlled interruption recovery, compatibility, and—only where effects exist—duplicate prevention, idempotency, or reconciliation. A successful resume does not by itself establish exactly-once external effects.

**When to run:** Run before exposure and after persistence, checkpoint, recovery, retry, compatibility, or durable-state changes.

**Owner:** Recovery mechanics are owned by [7.1 Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md); any effect or approval evidence remains with its independently triggered owner.

**N/A:** The work is ephemeral and non-resumable. A queue without a recovery claim is not sufficient to select this profile.

### Conversation

**Trigger:** Multi-turn interaction, session history, or a task horizon across turns can affect behavior.

**Evidence focus:** Evaluate a bounded episode: relevant milestones, retained material constraints, forbidden events, terminal outcome, and stated turn, time, or budget limits. Test loss or contradiction of a material constraint when it is plausible. Do not require literal private reasoning traces.

**When to run:** Run before exposure and after a conversation contract, session lifecycle, task-horizon, instruction, or turn-management change.

**Owner:** Contract and context foundations are owned by [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) and [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md); episode behavior is owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** The candidate's evaluated interaction is a single bounded request with no behaviorally relevant cross-turn state.

### Stored memory and context transformation

**Trigger:** Stored memory, summaries, caches that affect answers, context selection, compression, or another input-to-context transformation can affect behavior.

**Evidence focus:** Observe session or tenant scope, provenance through the transformation, expiry/deletion or retention where claimed, poisoning resistance, loss or distortion of material constraints, relevant context sensitivity, and safe absence, corruption, or limit behavior. Test the transformation claims actually made; retrieval by itself does not establish stored memory.

**When to run:** Run before exposure and after a memory schema, retention rule, cache, summary, context-selection, transformation, or task-horizon change.

**Owner:** Context and memory mechanics are owned by [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) and [8.2 Retrieval, Memory, and Context Optimization](../../engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md); behavioral claims are owned by [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** No stored state, cache, summary, or context transformation affects the evaluated behavior. Conversation alone does not make deletion testing applicable.

### Composition

**Trigger:** Two or more model-driven agents, or a remote-agent interaction, contribute to one outcome.

**Evidence focus:** Exercise handoff and routing contracts, identity and source propagation, delegated scope, least privilege, denial propagation, malformed or malicious peer content, loop limits, failure/timeout containment, and the end-to-end outcome. A member's passing component cases do not establish that the composed system preserves its boundary.

**When to run:** Run before exposure and after a topology, member, handoff, remote-interface, or shared-contract change.

**Owner:** Composition controls are owned by [Part 9](../../engineering-reference/09-multi-agent-systems-and-interoperability/README.md); selected system paths are evaluated through [4.3](03-evaluation-types-and-dimensions.md).

**N/A:** One model-driven agent produces the outcome and no remote-agent interaction is enabled.

### Shared capacity and resource performance

**Trigger:** Shared queues, caches, quotas, rate or concurrency limits, budgets, common downstream capacity, or a shared-resource availability/fairness claim can affect correctness, safety, tenant fairness, or availability.

**Evidence focus:** Observe admission and limit enforcement, claimed isolation, queue/retry/backoff behavior, fail-safe exhaustion, resource/call/cost/latency bounds that are claimed, and truthful user-facing degradation. This profile is proportional: it does not demand distributed load infrastructure for a small local assistant. Its absence also does not remove the universal core's obligation to test the candidate's declared local stop or resource bounds.

**When to run:** Run before exposure and after a limit, capacity, provider, queue, cache, admission, shared-budget, or shared-resource change.

**Owner:** Operational bounds and monitoring are owned by [5.1 Observability, Budgets, and Operational Control](../05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md); capacity engineering is owned by [8.3 Cost, Latency, and Performance Optimization](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md) and [8.4 Capacity, Admission Control, and Backpressure](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md). Decision thresholds belong to [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** No shared resource or shared-capacity claim can affect the evaluated behavior. Record any local bound under the universal core instead.

### Human impact and domain assurance

**Trigger:** The risk record identifies material differential harm by population, domain, language, role, geography, entitlement, accessibility, or jurisdiction, or an external policy calls for additional assurance.

**Evidence focus:** Preserve the harm screen; select justified slices with appropriate expertise; compare like entitlement and task when equality is the claim; preserve legitimate policy differences; and report task and control outcomes separately. Add domain review, representative-user work, accessibility, appeal/override, or higher-assurance evidence only where the use and risk call for it. A small curated slice can expose a defect but does not establish a population rate.

**When to run:** Run before release and after a material use, user, data, capability, domain, or risk-context change.

**Owner:** The screen and slice evidence are owned by [4.3](03-evaluation-types-and-dimensions.md); detailed human-impact and domain assurance is owned by [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

**N/A:** The recorded screen identifies no material differential-harm or domain-assurance trigger for the named scope. This conclusion needs review again when the scope changes.

### Model judges

**Trigger:** A model-based evaluator supplies decision- or release-facing evidence.

**Evidence focus:** Retain the versioned rubric, known pass/fail anchors, human-reviewed held-out calibration for the target claim and relevant risk slices, false passes, disagreements, unscorable cases, and relevant order, style, reference-leakage, or injection sensitivity. A judge is diagnostic until fitness for the exact decision role is documented. Calibration is about the evaluator, not about model routing.

**When to run:** Establish fitness before using the judge for the stated decision purpose and reassess it after a material judge, rubric, context, model, target-distribution, or target-claim change. Public evaluation guidance similarly treats automated-grader usefulness as context-dependent rather than a universal substitute for claim-fit evidence. [3]

**Owner:** Evaluator fitness and calibration are owned by [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md).

**N/A:** No model judge supplies decision- or release-facing evidence. A retained diagnostic judge should be labelled diagnostic rather than promoted to a gate.

### Model selection, routing, and fallback

**Trigger:** A selected model, provider, settings, route, fallback, or degradation policy can change task behavior, data handling, controls, or operating limits.

**Evidence focus:** Exercise the actual end-to-end selection, routing, retry, fallback, and final-delivery policy; record resolved identities; and establish each enabled path's applicable contract, privacy, control, quality, latency, cost, and recovery behavior. An alternate path may differ only under a declared contract rule. This is distinct from evaluator calibration: a route does not require a model judge.

**When to run:** Run before exposure and after a material selection, provider, configuration, routing, fallback, retry, or degradation change.

**Owner:** Model selection and routing are owned by [8.1 Model Selection, Parameters, and Routing](../../engineering-reference/08-model-context-and-resource-engineering/01-model-selection-parameters-and-routing.md); candidate provenance and decision comparison are owned by [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**N/A:** No selection, routing, fallback, provider, or settings choice beyond the already frozen candidate identity can affect the evaluated claim. Do not use this rationale when a hidden or enabled alternate path can affect behavior.

## Cadence from development through operation

### Production preparation

During development, use the narrowest claim-fit checks while a feature is being shaped: focused deterministic and component checks for relied-on rules, representative behavior cases for changed behavior, and one focused boundary case for a newly enabled risk. Development cases can be improved during iteration; they do not become an independent release holdout after tuning.

### Change review

A material change is any change reasonably capable of altering a mapped claim, enforcement boundary, evidence, use/risk context, or operating assumption. It can be an instruction; model, provider, settings, route, or fallback change; interface schema, permission, credential, target, or effect semantic change; source/corpus/index/cache change; identity or authorization change; user/domain change; context, memory, retention, retry, approval, durable-state, composition, capacity, evaluator, rubric, threshold, or dependency-environment change. “Prompt-only,” vendor-owned, rare, expensive, and “already a pilot” are not automatic non-applicability rationales.

For a material change, refresh the candidate/configuration provenance, assess the affected map entries, rerun each affected profile, and rerun every still-applicable critical-control case that the changed component can influence. When a change makes a profile newly applicable—such as enabling retrieval, storing memory, adding an effect, turning on an approval path or fallback, expanding protected data, or adding another agent—complete that profile before exposing the new capability. The actual rerun method and result status belong to the linked owner chapters.

### Pilot and release

Before a pilot, freeze the candidate identity for the decision, finish the core and presently triggered profiles needed for the proposed users, data, and effects, and declare gates, thresholds, and diagnostics before results are interpreted. A pilot is user exposure, not an exception from relevant controls. Narrowing a real capability or user/data scope can remove a profile trigger; merely relabelling a triggered risk as a pilot cannot.

Before release or a material expansion, run the applicable holdout and comparison evidence against the frozen candidate under the declared fixture, evaluator, and trial policy. The release owner then interprets the result under [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md). Production monitoring supplements this evidence; it does not supply an omitted pre-exposure control or quality claim.

### Operational follow-through

In operation, monitor signals capable of detecting the selected profiles' material failure modes. Preserve privacy-appropriate attributable records, triage reports, and sanitize and confirm a failure before treating it as evaluation evidence or a regression case. A credible warning, provider incident, telemetry gap, or drift signal may be inconclusive; it should prompt investigation or a targeted rerun rather than be silently counted as a pass. A confirmed failure is routed through the regression and decision process owned by [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

### Guarded-live evaluation

Ordinary offline and shadow work should remain isolated and effect-safe where practicable. A guarded-live experiment or user study may be useful only when live exposure or effects are genuinely in scope. Its scope record makes the exposure intelligible: the candidate, purpose, users, data, effect boundary, monitoring, stop or rollback condition, outcome and harm signals, and accountable authority are explicit. The record is not an approval or authorization mechanism, and it cannot replace evidence needed before exposure.

## Requirements

- **CASE-01 — Claim-to-case, profile, and cadence map.** **Applicability:** Every production candidate, before its evidence supports a material design, pilot, release, or change decision. **Requirement:** The accountable owner **MUST** maintain a versioned evaluation plan that maps each in-scope acceptance criterion, prohibited outcome, and material risk-scenario ID to its claim family, case or case family, selected level, evaluator or authoritative observation, suite purpose, lifecycle stage, decision role, accountable owner, and applicable coverage profile. The plan **MUST** identify the evaluated candidate/configuration and material-change impact, and **MUST** record a candidate- and stage-specific rationale whenever a profile that would otherwise appear relevant is `N/A`. **Observable evidence:** A versioned coverage map linked to the candidate identity, case/fixture records, evaluator or state-observation records, profile statuses, owners, and stage/rerun plan.

- **COVERAGE-01 — Universal evidence core.** **Applicability:** Every production candidate and proposed exposure, including a simple read-only assistant. **Requirement:** The evaluation plan **MUST** include one proportional universal core: claim-fit checks for relied-on deterministic rules and interface boundaries; controlled behavior cases for every material user-visible contract claim; contract-defined bounded results for applicable adverse conditions; enforcement-boundary observations for applicable critical controls; an independent holdout when a release claim relies on independence from tuning; retained case, fixture, evaluator or authoritative-observation, outcome, trajectory-when-relevant, and run-status identity; and a predeclared trial and deployed retry/selection/final-result policy when variability can affect a material claim. The core **MUST** exercise each applicable contract-defined time, call, resource, output, or stop bound, including local bounds that do not depend on shared or distributed capacity. **Observable evidence:** The coverage map and attributable run records show the selected core cases, bounds, decision roles, statuses, and any documented reason that repetition is not relevant to a material claim.

- **COVERAGE-02 — Independently triggered profile coverage.** **Applicability:** Whenever a profile trigger in this chapter is true for the candidate and decision scope. **Requirement:** The accountable owner **MUST** select the smallest applicable profile content that establishes each mapped claim and **MUST** map its enabled boundary or relied-on guarantee to claim-fit cases, observations, stages, and the linked canonical owner. The plan **MUST** treat retrieval, tools/trajectory, untrusted input, sensitive/tenant scope, external effects, approvals, durable recovery, conversation, stored memory/context transformation, composition, shared capacity, human impact, model judges, and model selection/routing as independently triggered profiles. It **MUST NOT** infer one profile from another or prescribe an absent submechanism. **Observable evidence:** The versioned profile map identifies each applicable profile's trigger, selected checks, observation source, rerun trigger, owner link, and an objective `N/A` rationale where its trigger is absent.

- **COVERAGE-03 — Stage and material-change cadence.** **Applicability:** Every production candidate, and every change or operational signal reasonably capable of altering a mapped claim, boundary, evidence, use/risk context, or operating assumption. **Requirement:** The evaluation owner **MUST** run claim-fit core and newly triggered-profile evidence during development and change review, complete the applicable pre-exposure evidence before a pilot, and refresh applicable frozen-candidate holdout/comparison evidence before release or material expansion. For a material change, the owner **MUST** assess affected map entries, refresh candidate/configuration provenance, rerun every affected profile, and rerun every still-applicable critical-control case that the changed component can influence. A credible operational signal **MUST** be triaged and attributed before it is counted as evidence; confirmed failures **MUST** enter the applicable sanitized regression process. **Observable evidence:** Stage records show the candidate, changed component or signal, impact assessment, selected reruns, valid/invalid/inconclusive/failure statuses, and handoff to the canonical decision record.

- **COVERAGE-04 — Guarded-live evaluation scope record.** **Applicability:** Only when a guarded-live experiment, user study, shadow exposure with user impact, or other live exposure/effect is proposed as evaluation scope. **Requirement:** Before live evaluation begins, the accountable owner **MUST** record the identified candidate, stated purpose, user and exposure boundary, data and effect boundary, applicable profiles and controls, accountable authority, monitoring signals, stop or rollback conditions, data-handling approach, and intended outcome and harm signals. The record **MUST** distinguish an evaluation conclusion from the separate authorization, approval, readiness, and rollout decisions, and **MUST NOT** substitute guarded-live monitoring for applicable pre-exposure evidence. **Observable evidence:** A versioned live-scope record links the candidate, profile map, boundary and stop conditions, monitoring plan, actual authority references, and subsequent attributable result record.

## Worked example: a scoped plan for the policy assistant

This fictional example is a planning record, not executed evidence or a release result. The policy assistant is ephemeral and read-only. It answers from approved, current, permission-filtered sources with citations; it has no persisted memory, approval, external write, or delegated-agent capability. The current London hotel value in the controlled source is **GBP 220**. Its terminal outcomes are `complete`, `needs_information`, `declined`, and `failed`, plus only contract-defined partial or escalation outcomes.

The plan selects the core, approved-retrieval, tools/trajectory, untrusted-input, sensitive/tenant-scope, and model-selection/routing profiles. It records a model judge as diagnostic only, so the model-judge profile is not being used for decision evidence. The effect, approval, durable-recovery, conversation, stored-memory/context, composition, and shared-capacity profiles are `N/A` for this scope with their stated reasons. The human-impact screen is also recorded; if it identifies material differential harm when users or policy scope change, its `N/A` conclusion expires and the human-impact profile is added.

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

`POLICY-CURRENT-001` establishes the ordinary current-source claim: the answer is `complete`, states GBP 220, and identifies `travel-policy-2026` at revision `"2026-10-01"`. `POLICY-STALE-002` verifies that `travel-policy-2024-superseded` at revision `"2024-01-01"` is recognized as superseded rather than treated as equal authority. `POLICY-CONFLICT-004` is different: two current approved policies disagree, so it expects an uncertainty or escalation outcome rather than an invented definitive amount. `POLICY-MISSING-003` makes the same distinction for absent permitted evidence.

The trajectory observation for `POLICY-DENIED-005` distinguishes the requester’s denied source-boundary decision from the response. The expected response withholds restricted material, while the boundary record establishes whether retrieval was refused. `POLICY-INJECTION-006` places a harmless instruction conflict in the untrusted channel under test and observes that it did not turn data into authority or produce restricted disclosure. These cases include permitted counterpart work, so the plan cannot mistake blanket refusal for safe success.

Because the assistant accepts semantic language and depends on current, permission-filtered evidence, `POLICY-PARAPHRASE-007` is a reviewed irrelevant-change relation and the permission-loss/current-policy-conflict cases are relevant-change relations. They complement, rather than replace, the correct-outcome checks. The trial policy belongs in the practical reference and the release interpretation belongs in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md); this example intentionally does not assign a universal trial count or claim an observed pass rate.

If a later variant adds a human-approved policy update, the record changes before that update is exposed: external-effect, approval, and durable-recovery profiles are selected independently. Its evidence then observes the exact approved subject, authorization, invocation, and authoritative final state. The existing read-only example cannot establish any of those effect or approval claims.

## Evidence and checklist

Use this checklist to review the coverage map and cadence, not to replace the detailed method or decision owners.

- [ ] The evaluated candidate/configuration and decision stage are identifiable, and every material acceptance criterion, prohibited outcome, and risk scenario maps to claims, cases, observations, owners, and stages.
- [ ] The universal core covers material contract outcomes, relied-on rules/boundaries, adverse outcomes, applicable critical controls, evidence identity/status, and declared local bounds even where no shared-capacity system exists.
- [ ] Every selected profile states its real trigger, enabled boundary or relied-on guarantee, observation, rerun trigger, and canonical owner; no profile is inferred from another.
- [ ] Every `N/A` conclusion names the candidate and stage and explains why the trigger is absent rather than citing cost, rarity, a pilot label, a missing mechanism, or vendor ownership.
- [ ] The declared trial, retry, selection, fallback, and final-result policy matches the behavior being assessed; diagnostic signals remain distinct from gates and thresholds.
- [ ] Development cases remain separate from the independent release holdout, and a material change reruns affected profiles plus influenced critical controls.
- [ ] Invalid and inconclusive records remain visible; a real attributable failure has not been relabelled as a harness defect or offset by an aggregate score.
- [ ] Any guarded-live scope record identifies exposure, data/effect boundaries, monitoring, stop/rollback conditions, accountable authority, and its non-substitution for pre-exposure evidence.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"

[2]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"

[3]: https://developers.openai.com/api/docs/guides/evaluation-best-practices "OpenAI Evaluation Best Practices"

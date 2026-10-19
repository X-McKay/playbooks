# Part 5 — Release, Operations, and Lifecycle

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted  
**Audience:** Learners who need a release-to-retirement picture; builders and operators who need bounded operational records; and reviewers who need to distinguish evidence, evaluation, authorization, and lifecycle decisions.  
**Purpose:** Connect proposed readiness, operational control, support, and retirement practices without turning an operational observation or completed template into authorization.  
**Scope:** Release readiness, material change, runtime observability and bounds, support and incident response, maintenance, deprecation, and retirement. It links to—rather than replaces—the security, privacy, evaluation, durable-execution, capacity, and specialized-assurance owners.  
**Applicability:** Every production agent needs the applicable operational and lifecycle arrangements. The required depth depends on the agent's governance tier, execution class, enabled capabilities, exposure, and potential impact; a reference record or optional mechanism is not automatically universal.  
**Prerequisites:** Start with the bounded proposal in [Part 1](../01-problem-definition-and-planning/README.md), declared behavior and capabilities in [Part 2](../02-agent-basics/README.md), enforceable trust and data boundaries in [Part 3](../03-security-and-trust-boundaries/README.md), and decision-grade evidence in [Part 4](../04-testing-and-evaluation/README.md).  
**Output:** An operating-control record, a release and rollout record, a support/lifecycle record, and clear handoffs to the owners of evidence, authorization, effects, and assurance.

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary pointers](../../glossary.md#part-5-operational-and-lifecycle-foundations) · [Requirement index](../../requirement-index.md#part-5--release-operations-and-lifecycle)

## Foundations and boundaries

Part 5 begins after the earlier Parts have made the intended use, contract, authority boundaries, information handling, and evaluation claims inspectable. Use [5.1](01-observability-budgets-and-operational-control.md) for the local explanation of request, run, physical attempt, bounded signal, resource budget, and safe stop. Use [5.2](02-readiness-change-and-rollout.md) for the local explanation of candidate, readiness state, exception boundary, release scope, and change disposition. Use [5.3](03-ownership-incidents-maintenance-and-retirement.md) for accountable support, suspected incidents, recovery authority, maintenance, and retirement distinctions.

The chapters do not make metrics proof of semantic grounding, a release record proof of authorization, or a stop proof of cancellation or reversal. An evaluation `go`, `conditional_go`, or `no_go` is distinct from a release authorization, and required but unresolved evidence remains blocking under the applicable owner. For data handling and audit evidence use [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md); for uncertain external effects use [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); for capacity and optimization use [8.3](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md) and [8.4](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md).

## Routes through this mini-book

**Learner route.** Read [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md), [5.2 Readiness, Change, and Rollout](02-readiness-change-and-rollout.md), and [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md) in order. This follows the path from seeing and bounding work, through an identified release decision, to supporting and retiring the capability.

**Builder route.** Begin with the contract and evidence handoffs from Parts 2–4. Use 5.1 to plan correlation, signals, limits, and a stop boundary; use 5.2 to bind the candidate, evidence, scope, and proposed rollout; then use 5.3 to make support, escalation, change, and retirement arrangements usable before exposure.

**Reviewer route.** Trace one candidate from its evaluation handoff through readiness and authorized scope, then inspect a representative run and the support arrangement. Verify that terminal outcome, runtime reason, telemetry, supported task, evaluation conclusion, release authorization, and any external effect remain separate facts. Follow the linked owner when a data, authority, durable-work, capacity, or specialized-assurance trigger is present.

## Canonical topic sequence

1. [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) owns the operational identity, outcome, budget, and stop requirements.
2. [5.2 Readiness, Change, and Rollout](02-readiness-change-and-rollout.md) owns the release readiness, exception, rollout, and material-change requirements.
3. [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md) owns the support, incident, maintenance, and retirement requirements.

## Practical workflow and packet

1. **Establish the operational view.** Use 5.1 to relate a request, stable run, and physical attempts; define meaningful terminal outcomes, separate reasons, bounded signals, applicable resource ceilings, and an authorized stop mechanism.
2. **Bind readiness to the subject.** Use 5.2 to identify the candidate, effective capabilities and permissions, evidence, intended scope, blockers, permitted exceptions, and proposed exposure stages. Do not defer required evidence or controls as post-release work.
3. **Make continuing accountability usable.** Use 5.3 to name the support and escalation paths, distinguish containment from recovery, turn feedback into governed follow-up, and plan deprecation or retirement as a handover.
4. **Connect optional records as one packet.** The [Part 5 practical reference](reference/README.md) connects the three illustrative records for `POLICY-BUILD-001` as one optional `POLICY-OPS-001` packet. It owns no requirement IDs and does not require three separate files, a particular platform, or a real deployment.

Read each chapter's applicability statement before treating a record or reference pattern as required. [Applicability](../../applicability.md) defines the distinction between a missing trigger, a governed exception, and a non-waivable gate.

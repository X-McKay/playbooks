# Part 5 — Release, Operations, and Lifecycle

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Learners who want the release-to-retirement picture; builders and operators who need bounded operational records; reviewers who need to tell evidence, evaluation, authorization, and lifecycle decisions apart.  
**Purpose:** Connect readiness, operational control, support, and retirement practice without letting an operational observation or a completed template stand in for authorization.  
**Scope:** Release readiness, material change, runtime observability and bounds, support and incident response, maintenance, deprecation, and retirement. It links to the owners of security, privacy, evaluation, durable execution, capacity, and specialized assurance.  
**Applicability:** Every production agent needs the applicable operational and lifecycle arrangements. Depth depends on governance tier, execution class, enabled capabilities, exposure, and potential impact.  
**Prerequisites:** The bounded proposal in [Part 1](../01-problem-definition-and-planning/README.md), declared behavior and capabilities in [Part 2](../02-agent-basics/README.md), trust and data boundaries in [Part 3](../03-security-and-trust-boundaries/README.md), and decision-grade evidence in [Part 4](../04-testing-and-evaluation/README.md).  
**Output:** An operating-control record, a release and rollout record, a support/lifecycle record, and clear handoffs to the owners of evidence, authorization, effects, and assurance.

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary pointers](../../glossary.md#part-5-operational-and-lifecycle-foundations) · [Requirement index](../../requirement-index.md#part-5--release-operations-and-lifecycle)

## Foundations and boundaries

Part 5 starts after the earlier Parts have made the intended use, contract, authority boundaries, information handling, and evaluation claims inspectable.

- [5.1](01-observability-budgets-and-operational-control.md) explains request, run, physical attempt, bounded signal, resource budget, and safe stop.
- [5.2](02-readiness-change-and-rollout.md) explains candidate, readiness state, exception boundary, release scope, and change disposition.
- [5.3](03-ownership-incidents-maintenance-and-retirement.md) explains accountable support, suspected incidents, recovery authority, maintenance, and retirement.

Metrics do not prove semantic grounding, a release record does not prove authorization, and a stop does not prove cancellation or reversal. An evaluation `go`, `conditional_go`, or `no_go` is distinct from release authorization, and required but unresolved evidence stays blocking. For data handling and audit evidence use [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md); for uncertain external effects use [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); for capacity and optimization use [8.3](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md) and [8.4](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md).

## Routes through this mini-book

**Learner route.** Read 5.1, 5.2, and 5.3 in order: seeing and bounding work, making a release decision, then supporting and retiring the capability.

**Builder route.** Start from the contract and evidence handoffs of Parts 2–4. Use 5.1 to plan correlation, signals, limits, and a stop boundary; 5.2 to bind the candidate, evidence, scope, and rollout; and 5.3 to make support, escalation, change, and retirement arrangements usable before exposure.

**Reviewer route.** Trace one candidate from its evaluation handoff through readiness and authorized scope, then inspect a representative run and the support arrangement. Check that terminal outcome, runtime reason, telemetry, supported task, evaluation conclusion, release authorization, and any external effect remain separate facts. Follow the linked owner when a data, authority, durable-work, capacity, or specialized-assurance trigger is present.

## Where each topic lives

1. [5.1](01-observability-budgets-and-operational-control.md) covers operational identity, outcomes, budgets, and stop.
2. [5.2](02-readiness-change-and-rollout.md) covers release readiness, exceptions, rollout, and material change.
3. [5.3](03-ownership-incidents-maintenance-and-retirement.md) covers support, incidents, maintenance, and retirement.

## Practical workflow

1. **Establish the operational view.** Use 5.1 to relate a request, a stable run, and physical attempts; define terminal outcomes, separate reasons, bounded signals, resource ceilings, and an authorized stop.
2. **Bind readiness to the subject.** Use 5.2 to identify the candidate, capabilities and permissions, evidence, scope, blockers, permitted exceptions, and exposure stages. Do not defer required evidence or controls to after release.
3. **Make accountability usable.** Use 5.3 to name support and escalation paths, separate containment from recovery, turn feedback into governed follow-up, and plan deprecation and retirement as a handover.
4. **Connect the records.** The [Part 5 practical reference](reference/README.md) ties the three illustrative records for `POLICY-BUILD-001` into one optional `POLICY-OPS-001` packet. It owns no requirement IDs and requires no particular file layout, platform, or deployment.

Read each chapter's applicability statement before treating a record or pattern as required. [Applicability](../../applicability.md) explains the difference between a missing trigger, a governed exception, and a non-waivable gate.

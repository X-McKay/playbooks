# Part 5 — Release, Operations, and Lifecycle

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Learners wanting the release-to-retirement picture; builders and operators needing bounded operational records; reviewers separating evidence, evaluation, authorization, and lifecycle decisions.  
**Purpose:** Connect readiness, operational control, support, and retirement practice without letting an operational observation or a completed template stand in for authorization.  
**Scope:** Release readiness, material change, runtime observability and bounds, support and incident response, maintenance, deprecation, and retirement, linking to the owners of security, privacy, evaluation, durable execution, capacity, and specialized assurance.  
**Applicability:** Every production agent needs the applicable operational and lifecycle arrangements. Depth depends on governance tier, execution class, enabled capabilities, exposure, and potential impact.  
**Prerequisites:** The bounded proposal in [Part 1](../01-problem-definition-and-planning/README.md), declared behavior and capabilities in [Part 2](../02-agent-basics/README.md), trust and data boundaries in [Part 3](../03-security-and-trust-boundaries/README.md), and decision-grade evidence in [Part 4](../04-testing-and-evaluation/README.md).  
**Output:** An operating-control record, a release and rollout record, a support/lifecycle record, and clear handoffs to the owners of evidence, authorization, effects, and assurance.

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary pointers](../../glossary.md#part-5-operational-and-lifecycle-foundations) · [Requirement index](../../requirement-index.md#part-5--release-operations-and-lifecycle)

## Foundations and boundaries

Part 5 starts once earlier Parts have made the intended use, contract, authority boundaries, information handling, and evaluation claims inspectable. Key terms by chapter: request, run, physical attempt, bounded signal, resource budget, and safe stop (5.1); candidate, readiness state, exception boundary, release scope, and change disposition (5.2); accountable support, suspected incident, recovery authority, maintenance, and retirement (5.3).

Metrics do not prove semantic grounding, a release record does not prove authorization, and a stop does not prove cancellation or reversal. An evaluation `go`, `conditional_go`, or `no_go` is distinct from release authorization, and required but unresolved evidence stays blocking. For data handling and audit evidence use [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md); for uncertain external effects use [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); for capacity and optimization use [8.3](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md) and [8.4](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md).

## Routes through this mini-book

**Learner route.** Read 5.1, 5.2, and 5.3 in order: bounding work, deciding a release, then supporting and retiring the capability.

**Builder route.** Start from the contract and evidence of Parts 2–4, then follow the practical workflow below before exposure.

**Reviewer route.** Trace one candidate from its evaluation result through readiness and authorized scope, then inspect a representative run and the support arrangement. Check that terminal outcome, runtime reason, telemetry, supported task, evaluation conclusion, release authorization, and any external effect stay separate, and follow the linked owner when a data, authority, durable-work, capacity, or assurance trigger is present.

## Where each topic lives

1. [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) covers operational identity, outcomes, budgets, and stop.
2. [5.2 Readiness, Change, and Rollout](02-readiness-change-and-rollout.md) covers release readiness, exceptions, rollout, and material change.
3. [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md) covers support, incidents, maintenance, and retirement.

## Practical workflow

1. **Establish the operational view.** Use 5.1 to relate a request, a stable run, and physical attempts; define terminal outcomes, separate reasons, bounded signals, resource ceilings, and an authorized stop.
2. **Bind readiness to the subject.** Use 5.2 to identify the candidate, capabilities and permissions, evidence, scope, blockers, permitted exceptions, and exposure stages. Do not defer required evidence or controls to after release.
3. **Make accountability usable.** Use 5.3 to name support and escalation paths, separate containment from recovery, turn feedback into governed follow-up, and plan deprecation and retirement as a handover.
4. **Connect the records.** The [Part 5 practical reference](reference/README.md) ties the three illustrative records for `POLICY-BUILD-001` into one optional `POLICY-OPS-001` packet; it owns no requirement IDs.

Read each chapter's applicability statement before treating a record or pattern as required; [Applicability](../../applicability.md) distinguishes a missing trigger, a governed exception, and a non-waivable gate.

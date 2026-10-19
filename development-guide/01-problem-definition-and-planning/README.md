# Part 1 — Problem Definition and Planning

**Status:** 0.5.0-draft.2 — draft

**Audience:** Learners framing a proposal, builders preparing a planning record, and reviewers checking whether a proposal is ready for design and evidence work.

**Purpose:** Frame a reviewable production proposal before settling implementation choices.

**Applicability:** Every production-agent proposal, and any pilot that may expose users or operational data.

**Output:** A connected problem brief, success criteria, suitability rationale, and initial scope/risk/ownership record.

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary](../../glossary.md) · [Requirement index](../../requirement-index.md) · [Practical reference](reference/README.md)

## Why start here

Part 1 turns a request for an agent into four planning decisions: what problem exists, what a worthwhile and safe outcome means, whether an agent beats a simpler alternative, and which early risk, data and ownership facts need more work. Keeping them separate stops a proposed implementation from standing in for evidence of need, value, authority or readiness. The chapters own the requirement IDs.

## Choose a route

**Learner.** Read the chapters in order (see the sequence below).

**Builder.** Work through the same sequence and fill in one record after each decision: the [problem brief](../../templates/1.1/problem-brief.yaml), [success-criteria record](../../templates/1.2/success-criteria.yaml), [suitability decision](../../templates/1.3/suitability-decision.yaml) and [initial scope record](../../templates/1.4/initial-scope-record.yaml). The [practical reference](reference/README.md) shows how they connect; they are planning aids, not approvals or evidence.

**Reviewer.** Check [1.1](01-defining-the-problem.md) for separable facts, assumptions, scope, dependencies and downstream effects; [1.2](02-requirements-success-criteria-and-measurable-targets.md) for explicit outcomes, boundaries, metrics, baseline status and consequences; [1.3](03-agent-suitability-and-alternatives.md) for a same-case comparison and an added-value hypothesis; and [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) for reachable owners and for data, authority, harm, applicability, pilot and escalation questions handed to the right owner.

## Chapter sequence

1. [1.1 Defining the Problem](01-defining-the-problem.md): people, work, current process, evidence status, scope, dependencies, exclusions.
2. [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md): value, task behavior, safety, reliability, latency and cost as separate decision dimensions.
3. [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md): process improvement, simpler technical approaches, fixed workflows, adaptive agents and hybrids, without treating novelty as value.
4. [1.4 Initial Risk, Data, Ownership, and Delivery Plan](04-initial-risk-data-ownership-and-delivery-plan.md): early harm, source and access, authority, ownership, delivery and reassessment questions.

For vocabulary, see the [Part 1 pointers in the glossary](../../glossary.md#part-1-planning-foundations); chapter text explains each term where it is used. For exact requirements, see the [requirement index](../../requirement-index.md#part-1--problem-definition-and-planning).

## Common pitfalls across Part 1

- **No baseline.** Without a measure of today's process, "improvement" means nothing.
- **One blended agent score.** Report value, behavior, safety, reliability, latency and cost separately.
- **Scope creep after the pilot.** A narrow success is not evidence for more users, data or actions. Reopen Part 1 when the boundary changes.

## Handoffs after Part 1

Part 1 plans the claim; it does not prove it. Continue to [Part 2](../02-agent-basics/README.md) to declare the bounded contract and enabled capabilities, [Part 3](../03-security-and-trust-boundaries/README.md) for trust boundaries, [Part 4](../04-testing-and-evaluation/README.md) for evaluators and evidence, and [Part 5](../05-release-operations-and-lifecycle/README.md) for release and operation. [Applicability](../../applicability.md) explains which specialized Parts a use triggers, and the difference between a missing trigger, a governed exception and a non-waivable gate.

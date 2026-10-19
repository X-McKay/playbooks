# Part 1 — Problem Definition and Planning

**Status:** 0.5.0-draft.2 — Part 1 refined draft; proposed, not adopted  
**Audience:** Learners framing a proposal; builders preparing a bounded planning record; and reviewers checking whether the proposal is ready to enter design and evidence work.  
**Purpose:** Frame a reviewable production proposal before settling implementation choices.  
**Applicability:** Every production-agent proposal and any pilot that may expose users or operational data.  
**Output:** A connected problem brief, success criteria, suitability rationale, and initial scope/risk/ownership record.

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary](../../glossary.md) · [Requirement index](../../requirement-index.md) · [Practical reference](reference/README.md)

## Why start here

Part 1 turns a request for an agent into four inspectable planning decisions: what problem exists, what a worthwhile and safe outcome would mean, whether an agent is justified over a simpler alternative, and what early risk/data/ownership facts need further work. It keeps those decisions separate so a proposed implementation does not become evidence that the underlying need, value, authority, or readiness is established.

The four chapters refine this planning layer only. Their proposed requirement wording and applicability remain in their owner chapters; this overview and the practical reference own no normative IDs.

## Choose a route

### Learner route — understand the decisions in order

Read [1.1 Defining the Problem](01-defining-the-problem.md) to separate the user need from a proposed solution. Continue to [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) for decision-relevant outcome and measurement language, then [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md) for a fair simpler-baseline comparison. Finish with [1.4 Initial Risk, Data, Ownership, and Delivery Plan](04-initial-risk-data-ownership-and-delivery-plan.md) to identify the planning facts and specialist handoffs that remain open.

### Builder route — assemble one planning packet

Work through the same sequence and complete the corresponding record after each decision: the [problem brief](../../templates/1.1/problem-brief.yaml), [success-criteria record](../../templates/1.2/success-criteria.yaml), [suitability decision](../../templates/1.3/suitability-decision.yaml), and [initial scope record](../../templates/1.4/initial-scope-record.yaml). The [practical reference](reference/README.md) explains the handoff between the four templates. They are illustrative planning aids, not execution, approval, or a substitute for later evidence.

### Reviewer route — test the proposal before design is treated as settled

Start at [1.1](01-defining-the-problem.md) to check that observed facts, assumptions, scope, dependencies, and downstream effects are distinguishable. Use [1.2](02-requirements-success-criteria-and-measurable-targets.md) to check that outcomes, boundaries, metrics, baseline status, and consequences are explicit. Use [1.3](03-agent-suitability-and-alternatives.md) to check the shared-case comparison and the added-value hypothesis. Close with [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) to confirm owners are reachable and data, authority, harm, applicability, pilot, and escalation questions are handed to their proper owners rather than presumed resolved.

## Chapter sequence and foundations

1. [1.1 Defining the Problem](01-defining-the-problem.md) establishes the people, work, current process, evidence status, scope, dependencies, and exclusions behind a proposal.
2. [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) separates value, task behavior, safety, reliability, latency, and cost into interpretable decision dimensions.
3. [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md) compares process improvement, simpler technical approaches, fixed workflows, adaptive agents, and hybrids without treating novelty as value.
4. [1.4 Initial Risk, Data, Ownership, and Delivery Plan](04-initial-risk-data-ownership-and-delivery-plan.md) makes early harm, source/access, authority, ownership, delivery, and reassessment questions visible.

For a short orientation to the vocabulary, use the [Part 1 planning-foundations pointers in the glossary](../../glossary.md#part-1-planning-foundations). Read the chapter-local explanations in context rather than treating the glossary as a duplicate canonical definition. For exact proposed requirements and their owners, use the [requirement index](../../requirement-index.md#part-1--problem-definition-and-planning).

## Handoffs after Part 1

Part 1 plans the claim; it does not prove it. Continue to [Part 2](../02-agent-basics/README.md) to declare the bounded contract and enabled capabilities. Use [Part 3](../03-security-and-trust-boundaries/README.md) for trust boundaries, [Part 4](../04-testing-and-evaluation/README.md) for evaluators and decision-grade evidence, and [Part 5](../05-release-operations-and-lifecycle/README.md) for release and operation. Use the [applicability guidance](../../applicability.md) to identify independently triggered specialized reference Parts.

Read the chapter applicability statements before treating a reference pattern as required. [Applicability](../../applicability.md) defines the distinction between a missing trigger, a governed exception, and a non-waivable gate.

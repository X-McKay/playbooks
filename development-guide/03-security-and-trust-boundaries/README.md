# Part 3 — Security and Trust Boundaries

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted  
**Audience:** Learners who need to distinguish data from authority; builders who need enforceable boundaries; and reviewers who need to inspect authorization, content, data, and evidence paths.  
**Scope:** Keep identity, authority, untrusted content, data handling, and minimum audit evidence at enforceable boundaries. This Part does not make a prompt, schema, source label, record, or prior success into a substitute for an independently enforced decision.  
**Applicability:** Every production agent needs an appropriate authority and trust boundary. The depth of data handling and specialized assurance is triggered by the actual information, destination, operation, and impact; read-only work can still disclose or mislead.  
**Output:** A protected-operation boundary, scoped authority record, content/action boundary record, data-handling record where applicable, and a clear evidence handoff.

[Playbook home](../../README.md) · [Section index](../README.md) · [Part 2 agent basics](../02-agent-basics/README.md) · [Part 4 evaluation](../04-testing-and-evaluation/README.md) · [Glossary pointers](../../glossary.md#part-2-and-part-3-foundations) · [Requirement index](../../requirement-index.md)

## Start with the right prerequisite

Bring a bounded candidate from [Part 1](../01-problem-definition-and-planning/README.md) and a declared contract/capability picture from [Part 2](../02-agent-basics/README.md). If an enabled capability, source, identity dependency, or output consumer is still unknown, record the uncertainty and route it back to its owner rather than claiming a boundary is complete. Use [Part 4](../04-testing-and-evaluation/README.md) for evidence design and [Part 5](../05-release-operations-and-lifecycle/README.md) for release and operations; neither is replaced by a completed template here.

## Routes through this mini-book

**Learner route.** Read [3.1](01-identity-authority-zero-trust-and-least-privilege.md), [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md), and [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md) in order. This follows the practical path from who may access a resource, through how content is handled, to what data and evidence remain.

**Builder route.** Start with [3.1](01-identity-authority-zero-trust-and-least-privilege.md) to identify the workload, requester, resource, operation, and trusted context at each protected boundary. Apply [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) to user, retrieved, tool, memory, and peer content. Use [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md) to map copies, destinations, retention/deletion questions, and minimum evidence before assembling Part 4 cases.

**Reviewer route.** Trace one protected operation from request through authorization, content interpretation, proposed action, downstream boundary, and relevant evidence. Test whether any discovered capability, model-produced field, retrieved text, or citation silently enlarges authority. Then inspect data copies and exports separately from diagnostic traces. Keep a blocked proposal, dispatched attempt, response, and authoritative effect as distinct observations.

## Canonical topic sequence

1. [3.1 Identity, Authority, Zero Trust, and Least Privilege](01-identity-authority-zero-trust-and-least-privilege.md) develops the resource-side authority boundary and least-privilege reasoning.
2. [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) develops direct and indirect hostile-content handling, proposal-to-effect separation, and safe legitimate utility.
3. [3.3 Data Privacy, Handling, and Minimum Audit Evidence](03-data-privacy-handling-and-minimum-audit-evidence.md) develops lifecycle handling, data-copy distinctions, and bounded audit evidence.

## Practical workflow and artifact index

1. **Identify the decision boundary.** Use the [authority-boundary record](../../templates/3.1/authority-boundary-record.yaml) to make the protected resource, operation, trusted identity/context, and unresolved scope explicit.
2. **Separate content from authority and action.** Use the [content/action boundary record](../../templates/3.2/content-action-boundary-record.yaml) to identify untrusted inputs, allowed utility, blocked paths, and the difference between a proposal and an observed effect.
3. **Map information and evidence paths.** Use the [data-handling/audit record](../../templates/3.3/data-handling-audit-record.yaml) to account for data copies, destinations, retention/deletion questions, and minimum evidence without assuming a universal legal or retention rule.
4. **Send claims to the correct next owner.** Use Part 4 for cases and evidence, Part 5 for operational lifecycle work, Part 7 for durable or consequential action handling, and Part 10 when a specialized assessment is triggered.

The [Part 3 practical reference](reference/README.md) connects these illustrative, unexecuted records without owning requirement IDs. The [draft notes](../../draft-notes.md#concrete-unresolved-normative-ambiguities) retain the unresolved refusal-scope question and other policy ambiguities without choosing a resolution. Use the [glossary](../../glossary.md#part-2-and-part-3-foundations) as a pointer and the [requirement index](../../requirement-index.md#part-3--security-and-trust-boundaries) as a locator for the owner chapters.

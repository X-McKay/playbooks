# Part 3 — Security and Trust Boundaries

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Learners who need to tell data from authority; builders who need enforceable boundaries; reviewers who inspect authorization, content, data, and evidence paths.  
**Scope:** Identity, authority, untrusted content, data handling, and minimum audit evidence, each kept at an enforceable boundary. A prompt, schema, source label, record, or past success never substitutes for an independently enforced decision.  
**Applicability:** Every production agent needs an authority and trust boundary. How deep data handling and specialized assurance go depends on the actual information, destination, operation, and impact; read-only work can still disclose or mislead.  
**Output:** A protected-operation boundary, scoped authority record, content/action boundary record, data-handling record where applicable, and a clear evidence handoff.

[Playbook home](../../README.md) · [Section index](../README.md) · [Part 2 agent basics](../02-agent-basics/README.md) · [Part 4 evaluation](../04-testing-and-evaluation/README.md) · [Glossary pointers](../../glossary.md#part-2-and-part-3-foundations) · [Requirement index](../../requirement-index.md)

## Start with the right prerequisite

Bring a bounded candidate from [Part 1](../01-problem-definition-and-planning/README.md) and a declared contract and capability picture from [Part 2](../02-agent-basics/README.md). If an enabled capability, source, identity dependency, or output consumer is still unknown, record the gap and send it back to its owner instead of calling the boundary complete. Use [Part 4](../04-testing-and-evaluation/README.md) for evidence design and [Part 5](../05-release-operations-and-lifecycle/README.md) for release and operations.

## Routes through this mini-book

**Learner route.** Read [3.1](01-identity-authority-zero-trust-and-least-privilege.md), [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md), and [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md) in order: who may access a resource, how content is handled, what data and evidence remain.

**Builder route.** Start with 3.1 to identify the workload, requester, resource, operation, and trusted context at each protected boundary. Apply 3.2 to user, retrieved, tool, memory, and peer content. Use 3.3 to map copies, destinations, retention and deletion questions, and minimum evidence before building Part 4 cases.

**Reviewer route.** Trace one protected operation from request through authorization, content interpretation, proposed action, downstream boundary, and evidence. Test whether any discovered capability, model-produced field, retrieved text, or citation quietly enlarges authority. Inspect data copies and exports apart from diagnostic traces. Keep a blocked proposal, dispatched attempt, response, and authoritative effect as distinct observations.

## Chapters

1. [3.1 Identity, Authority, Zero Trust, and Least Privilege](01-identity-authority-zero-trust-and-least-privilege.md): the resource-side authority boundary, delegated authority, isolation, and least privilege.
2. [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md): direct and indirect hostile content, defence in depth against prompt injection, proposal-to-effect separation, and safe legitimate utility.
3. [3.3 Data Privacy, Handling, and Minimum Audit Evidence](03-data-privacy-handling-and-minimum-audit-evidence.md): lifecycle handling, data copies, and bounded audit evidence.

## Practical workflow and artifact index

1. **Identify the decision boundary.** Use the [authority-boundary record](../../templates/3.1/authority-boundary-record.yaml) to state the protected resource, operation, trusted identity and context, and unresolved scope.
2. **Separate content from authority and action.** Use the [content/action boundary record](../../templates/3.2/content-action-boundary-record.yaml) to list untrusted inputs, allowed utility, blocked paths, and the difference between a proposal and an observed effect.
3. **Map information and evidence paths.** Use the [data-handling/audit record](../../templates/3.3/data-handling-audit-record.yaml) to account for data copies, destinations, retention and deletion questions, and minimum evidence, without assuming a universal legal or retention rule.
4. **Send claims to the right next owner.** Part 4 for cases and evidence, Part 5 for operations, Part 7 for durable or consequential action, Part 10 for specialized assessment.

The [Part 3 practical reference](reference/README.md) connects the three records; it owns no requirement IDs, and its records are illustrative and unexecuted. The [draft notes](../../draft-notes.md#concrete-unresolved-normative-ambiguities) keep the open refusal-scope question and other policy ambiguities. The [glossary](../../glossary.md#part-2-and-part-3-foundations) and [requirement index](../../requirement-index.md#part-3--security-and-trust-boundaries) point to the owner chapters.

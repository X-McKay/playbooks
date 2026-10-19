# Part 3 practical reference

**Status:** 0.5.0-draft.2 — refined draft companion; proposed, not adopted  
**Purpose:** Connect the Part 3 boundary records in a practical build and review sequence without creating a second set of requirements.  
**Use with:** The [Part 3 overview](../README.md), its owner chapters, the [glossary pointers](../../../glossary.md#part-2-and-part-3-foundations), and the [requirement index](../../../requirement-index.md#part-3--security-and-trust-boundaries).

This reference owns **no requirement IDs**. The owner chapter, its applicability statement, and its `## Requirements` section control if this page or a template is shorter than the proposed requirement. The records use the shared fictional `POLICY-BUILD-001` / `internal-policy-assistance` example and are `illustrative-unexecuted`; they do not report authorization, a working control, approval, evaluation, deployment, or an external effect.

## Build one trust-boundary packet

1. **Name the protected operation.** Use [3.1](../01-identity-authority-zero-trust-and-least-privilege.md) with the [authority-boundary record](../../../templates/3.1/authority-boundary-record.yaml). Identify the workload, relevant requester, resource, operation, trusted decision inputs, and unresolved scope; do not infer any of them from model output.
2. **Trace every untrusted-content path.** Use [3.2](../02-untrusted-inputs-retrieved-content-and-action-boundaries.md) with the [content/action boundary record](../../../templates/3.2/content-action-boundary-record.yaml). Keep user input, retrieved material, tool returns, memory, and peer content as data. Identify safe legitimate utility, the prohibited path, and the separately observable proposal, dispatch, response, and effect states.
3. **Map the data and evidence lifecycle.** Use [3.3](../03-data-privacy-handling-and-minimum-audit-evidence.md) with the [data-handling/audit record](../../../templates/3.3/data-handling-audit-record.yaml). List copies and destinations across inputs, retrieval, logs, caches, evaluations, backups, and exports, then leave owner, retention, deletion, and legal-applicability decisions unresolved where they are not provided.
4. **Make testable handoffs.** Send contract/capability facts back to [Part 2](../../02-agent-basics/README.md), boundary and behavior claims to [Part 4](../../04-testing-and-evaluation/README.md), release/operational work to [Part 5](../../05-release-operations-and-lifecycle/README.md), and durable or consequential action work to [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) when triggered.

## Artifact index

- [Authority-boundary record](../../../templates/3.1/authority-boundary-record.yaml) — proposed protected operation, trusted identity/context inputs, scope, denial and freshness questions, and authority handoffs.
- [Content/action boundary record](../../../templates/3.2/content-action-boundary-record.yaml) — untrusted-content paths, allowed utility, prohibited proposals, downstream validation, and unobserved effect distinctions.
- [Data-handling/audit record](../../../templates/3.3/data-handling-audit-record.yaml) — lifecycle copies, purpose and destination questions, retention/deletion handoffs, and minimum evidence planning.

## Practical review use

Follow one representative request across all three records. The reviewer should be able to identify the requester's relevant scope, the resource and operation being checked, the content treated as untrusted, the data copies created or proposed, and the evidence that could establish only the claim at issue. A source citation or a schema-valid response can support a narrow fact; neither establishes authorization, semantic support, or an external effect by itself.

For the shared fictional example, `employee-uk-104` may receive the permitted current London policy fact, while `contractor-uk-204` may not. A superseded source is not current, and two current equal-authority sources in conflict need clarification or escalation rather than an invented answer. When a poisoned retrieved document embeds a prohibited instruction while a separate permitted question remains, preserve only the legitimate utility allowed by the case. The unresolved question of whether a separately visible refusal outcome is required is retained in the [draft notes](../../../draft-notes.md#concrete-unresolved-normative-ambiguities), not decided by this reference.

Use the [Part 3 overview](../README.md) for learner, builder, and reviewer routes. Use [Applicability](../../../applicability.md) before treating a specialized assessment, durable control, or reference mechanism as universally required.

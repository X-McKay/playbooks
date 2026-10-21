# Part 3 practical reference

**Status:** 0.5.0-draft.2 — draft  
**Purpose:** Connect the Part 3 boundary records in a practical build and review sequence.  
**Use with:** The [Part 3 overview](../README.md), its chapters, the [glossary pointers](../../../glossary.md#part-2-and-part-3-foundations), and the [requirement index](../../../requirement-index.md#part-3--security-and-trust-boundaries).

This reference owns **no requirement IDs**; where it or a template is shorter than a requirement, the chapter controls. The records use the shared fictional `POLICY-BUILD-001` / `internal-policy-assistance` example and are `illustrative-unexecuted`.

## Build one trust-boundary set

1. **Name the protected operation.** Use [3.1](../01-identity-authority-zero-trust-and-least-privilege.md) with the [authority-boundary record](../../../templates/3.1/authority-boundary-record.yaml). Identify the workload, requester, resource, operation, trusted decision inputs, and unresolved scope; infer none from model output.
2. **Trace every untrusted-content path.** Use [3.2](../02-untrusted-inputs-retrieved-content-and-action-boundaries.md) with the [content/action boundary record](../../../templates/3.2/content-action-boundary-record.yaml). Keep all such content as data, and identify the safe legitimate utility, the prohibited path, and the separately observable proposal, dispatch, response, and effect.
3. **Map the data and evidence lifecycle.** Use [3.3](../03-data-privacy-handling-and-minimum-audit-evidence.md) with the [data-handling/audit record](../../../templates/3.3/data-handling-audit-record.yaml). List copies and destinations across inputs, retrieval, logs, caches, evaluations, backups, and exports. Leave owner, retention, deletion, and legal-applicability decisions open where none is provided.
4. **Hand off.** Contract and capability facts go to [Part 2](../../02-agent-basics/README.md), boundary and behavior claims to [Part 4](../../04-testing-and-evaluation/README.md), release and operations to [Part 5](../../05-release-operations-and-lifecycle/README.md), and durable or consequential action work to [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) when triggered.

## Artifact index

- [Authority-boundary record](../../../templates/3.1/authority-boundary-record.yaml): protected operation, trusted identity and context inputs, scope, denial and freshness questions, authority handoffs.
- [Content/action boundary record](../../../templates/3.2/content-action-boundary-record.yaml): untrusted-content paths, allowed utility, prohibited proposals, downstream validation, unobserved-effect distinctions.
- [Data-handling/audit record](../../../templates/3.3/data-handling-audit-record.yaml): lifecycle copies, purpose and destination questions, retention and deletion handoffs, minimum evidence planning.

## Practical review use

Follow one representative request across all three records to identify the requester's scope, the resource and operation checked, the content treated as untrusted, the data copies created, and the evidence that could support only the claim at issue. A citation or a schema-valid response supports a narrow fact; neither establishes authorization, semantic support, or an external effect.

In the shared example, `employee-uk-104` may receive the permitted current London policy fact and `contractor-uk-204` may not. A superseded source is not current, and two current equal-authority sources in conflict call for clarification or escalation, not an invented answer. When a poisoned retrieved document embeds a prohibited instruction next to a separate permitted question, keep only the legitimate utility the case allows. Whether a separately visible refusal outcome is required stays open in the [draft notes](../../../draft-notes.md#concrete-unresolved-normative-ambiguities).

Check [Applicability](../../../applicability.md) before treating a specialized assessment, durable control, or reference mechanism as universally required.

# 10.3 Advanced Privacy, Isolation, and Auditability

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, operators, security and privacy reviewers, accountable owners  
**Applicability:** Agents that process sensitive information, serve multiple tenants, retain derived data, run untrusted or high-impact capabilities, or need stronger evidence for consequential actions. If none applies, use the minimum rules in [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) and record why this extension does not apply.

[Part 10](README.md) · [Applicability](../../applicability.md) · [10.1 Detailed Risk Assessment and Governance](01-detailed-risk-assessment-and-governance.md) · [10.2 Bias, Human Impact, and Domain Assurance](02-bias-human-impact-and-domain-assurance.md)

## Purpose and applicability

Privacy and containment failures often happen outside the answer: a cache serves another tenant's document, a summary outlives its removed source, or an audit trail captures more sensitive content than operators need. Higher assurance also needs evidence of who did what, under which authority, and what the external system accepted. A complete log is not a privacy policy, and encryption or sandboxing does not make a use appropriate.

Use this chapter when the screen or [10.1](01-detailed-risk-assessment-and-governance.md) flags sensitive data, multiple tenants, retention or inference risk, untrusted code, or consequential actions; reviewers decide which obligations apply. The NIST Privacy Framework is voluntary, not a legal review or certification.[1] The data map and lifecycle inventory below can feed a GDPR data protection impact assessment where one is required ([10.1](01-detailed-risk-assessment-and-governance.md#frameworks-you-may-need-to-map-to)). This chapter builds on [3.1](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), [3.3](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), and [5.1](../../development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md); approval semantics stay with [7.3](../07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) and tests with [Part 4](../../development-guide/04-testing-and-evaluation/README.md).

## Working model

Follow sensitive information through its whole lifecycle: an input may be normalized, retrieved, summarized, embedded, cached, queued, sent to a provider, answered from, and copied into telemetry or backups, and derived material can reveal facts no single input shows. Map source, purpose, classification, transformations, recipients, storage, and copies. The NIST Privacy Framework (Version 1.0; a 1.1 draft is out for comment) frames privacy risk around how data is processed, not which processing is lawful.[1]

Isolation is an end-to-end authorization property. An instruction or initial query filter fails if a later cache, reranker, memory store, artifact, or log crosses tenant boundaries, so bind every data access to trusted actor, tenant, and purpose context at its enforcement point. Shared infrastructure is fine when evidence shows the required separation.

Auditability means answering from evidence: active version and policy, initiating principal and tenant, authorization and approval checks, invoked capability, and what the authoritative target says happened. Record decisions, actions, references, and outcomes, not hidden reasoning, and protect the record from unauthorized change and deletion while limiting its content and access. NIST SP 800-92 (2006; revised draft 2023) treats logging as an organizational lifecycle process, not a switch.[2]

Integrity mechanisms have limits. Certificate Transparency uses Merkle trees for inclusion and append-only consistency proofs, and RFC 9162 (Experimental; obsoletes RFC 6962) notes a log could show observers different views, which only comparison and monitoring expose.[3] A hash, signature, or append-only store does not prove that all events were captured, that the producer was truthful, or that anyone reviewed them.

## Decisions and best practices

**Need and purpose first.** Collect less, limit precision, redact before model or tool access, and use synthetic or de-identified fixtures where they serve the test. "De-identified" is a claim to verify for the data and setting, not a guarantee against linkage or inference. Identify provider processing, residency, and retention limits with reviewers; neither default retention nor a deletion request is confirmed deletion.

**Trace tenant identity end to end,** from admission through retrieval, reranking, context assembly, caching, generation, and export. Asking the model to ignore another tenant's data tests instructions, not isolation. Write adversarial cases for wrong-tenant identifiers, stale authorization, cache-key collisions, concurrency, and derived artifacts, checked at the enforcing boundary against the authoritative record.

**Define the lifecycle before relying on deletion.** Where feasible, keep an inventory linking sources to derivatives and copies, with retention, deletion triggers, owners, and verification per class, including embeddings, summaries, caches, queued work, replicas, backups, evaluation artifacts, provider-held copies, and incident evidence. Where a copy cannot be erased at once or must be kept, document why and how long, restrict access, and claim deletion only after verification passes. Reviewers identify the legal duties.

**Match isolation to exposure.** Where an agent can run untrusted code or reach sensitive resources:

- give it its own identity and work area, separate from unrelated workloads
- restrict network egress and filesystem access, and cap resource use
- keep agent-controlled code from changing policy, audit controls, or its own containment
- scope credentials to the task and avoid ambient access

Reassess when capabilities, dependencies, data classes, or tenants change; for multiple agents, see [Part 9](../09-multi-agent-systems-and-interoperability/README.md).

**Link consequential-action evidence** from request to policy decision, exact approved action, execution attempt, and authoritative outcome; Part 7 owns approval, and this chapter adds privacy-aware handling and integrity. Keep full prompts, documents, credentials, and unneeded personal data out of audit events, and define who may read, export, amend, or delete them and what happens if the evidence path is down. A transcript or transport acknowledgement does not prove an external effect.

## Requirements

- **ASSURANCE-01** When an assessment identifies sensitive data, sensitive inference, or domain-specific restrictions, an accountable owner MUST document approved purposes, data classes, transformations, recipients, retention constraints, and required reviewer decisions before the affected processing is enabled. The design MUST reject or route for review a use that falls outside the approved scope. This record does not establish legal compliance.
- **ASSURANCE-02** When one service processes data for multiple users or tenants, each data read, write, retrieval result, cache entry, memory item, and exported artifact MUST be authorized using trusted tenant and purpose context at the relevant enforcement boundary. The system MUST test cross-tenant denial across each enabled path, including concurrent and derived-data paths; prompt instructions alone MUST NOT count as isolation evidence.
- **ASSURANCE-03** When the system retains or derives information from user or source data, its accountable owner MUST define retention and deletion behavior for in-scope originals, derivatives, replicas, caches, queues, backups, evaluation or audit artifacts, and provider-held copies. Deletion verification MUST use a declared evidence source; any exception MUST identify its scope, owner, reason, access/use restrictions, and review or expiry condition.
- **ASSURANCE-04** When the assessment identifies material damage from workload escape, untrusted code, or access to sensitive resources, the system MUST isolate the affected execution identity and work area, constrain its resources and egress, and protect control and evidence mechanisms from agent-controlled modification. Tests MUST demonstrate the selected isolation boundaries and the response to a denied or exhausted boundary.
- **ASSURANCE-05** When consequential-action evidence or elevated auditability is required, the system MUST preserve a privacy-minimized, access-controlled record linking request/run identity, trusted actor and tenant context, relevant agent/policy version, authorization and approval references, action identity, and an authoritative outcome or explicit unknown state. The owner MUST define and test integrity, completeness monitoring, retention, access, and failure handling for that record. Raw hidden chain-of-thought MUST NOT be required as audit evidence.

## Worked example

A fictional read-only policy assistant serves two isolated tenants. The current travel policy permits a London hotel amount of GBP 220; a superseded document differs.

The data map follows a question and passage through retrieval, context assembly, model processing, answer and citation, telemetry, and a short-lived cache. The boundary takes the authenticated tenant from request context, ignoring any model-generated label; retrieval filters by it, and the cache key includes tenant and corpus version. A release case asks tenant A's assistant for tenant B's superseded document, directly, concurrently, and through the cache. The oracle checks returned source identifiers and the access decision, not the model's claim; returning the other tenant's source fails hard even if the answer is correct.

The inventory records source identity, corpus version, index or embedding, cache, queue, provider path, and telemetry fields. Diagnostics omit raw questions and source text, keeping request identifier, tenant-bound authorization result, document versions, policy version, outcome, and safe error category. The deletion test removes a document, rebuilds or invalidates derivatives, clears the cache, and confirms retrieval cannot return it; backup or provider copies outside immediate deletion get recorded access and expiry controls. A cleared source table alone proves little.

The audit record can show the current version was cited, only the tenant's source was admitted, and uncertainty was returned when the current source was unavailable, but not semantic correctness (Part 4). A later write capability would need approval and external-effect evidence under Part 7.

## Evidence and checklist

Keep proportionate evidence tied to the assessed version:

- data-flow and purpose record;
- negative tenant tests for direct, cached, concurrent, and derived access;
- deletion schedule, lineage, verification result, and exceptions;
- containment tests for resource, filesystem, network, identity, and control-plane protections;
- audit-event definition, integrity and completeness checks, and a tested response to unavailable or altered evidence;
- for consequential actions, linked approval and effect evidence or an explicit unresolved outcome.

Before release, confirm tests cover the paths actually used, every "not applicable" has a rationale, and no unverified control earns credit. Reassess after material changes to data, tenants, providers, retention, capabilities, audit collection, or threats; decommission active work, credentials, evidence, and deletion under the same policy.

## References

[1]: https://www.nist.gov/privacy-framework "NIST Privacy Framework"
[2]: https://csrc.nist.gov/pubs/sp/800/92/final "NIST SP 800-92, Guide to Computer Security Log Management (2006)"
[3]: https://www.rfc-editor.org/rfc/rfc9162.html "RFC 9162: Certificate Transparency Version 2.0"

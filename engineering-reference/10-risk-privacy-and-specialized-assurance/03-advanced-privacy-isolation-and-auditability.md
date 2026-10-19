# 10.3 Advanced Privacy, Isolation, and Auditability

**Status:** 0.5.0-draft.2 — draft
**Audience:** Builders, operators, security and privacy reviewers, accountable owners
**Applicability:** Agents that process sensitive information, serve multiple tenants, retain derived data, run untrusted or high-impact capabilities, or need stronger evidence for consequential actions. If none of these apply, use the minimum rules in [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) and record why this extension does not apply.

[Part 10](README.md) · [Applicability](../../applicability.md) · [10.1 Detailed Risk Assessment and Governance](01-detailed-risk-assessment-and-governance.md) · [10.2 Bias, Human Impact, and Domain Assurance](02-bias-human-impact-and-domain-assurance.md)

## Purpose and applicability

Privacy and containment failures often happen outside the answer: a retrieval cache serves another tenant's document, a summary keeps information after its source is removed, or an audit trail captures more sensitive content than operators need. Higher-assurance systems also need credible evidence of who did what, under which authority, and what the external system accepted. A complete log is not a privacy policy, and encryption or sandboxing does not show that a use is appropriate.

Use this chapter when the initial screen or [10.1](01-detailed-risk-assessment-and-governance.md) identifies sensitive data, multiple tenants, material retention or inference risk, untrusted code or dependencies, or consequential actions that need stronger evidence. Accountable reviewers decide which domain and regulatory obligations apply. The NIST Privacy Framework is a voluntary risk-management tool, not a legal review or a certification.[1] Where processing is likely to be high risk to individuals, the GDPR requires a data protection impact assessment; see [10.1](01-detailed-risk-assessment-and-governance.md#frameworks-you-may-need-to-map-to). The data map and lifecycle inventory below are natural inputs to one.

This chapter builds on the minimum rules for identity and authorization in [3.1](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), data handling and audit evidence in [3.3](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), operational signals in [5.1](../../development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md), and risk governance in [10.1](01-detailed-risk-assessment-and-governance.md). Approval semantics stay with [7.3 Approval, Suspension, and In-Flight Compatibility](../07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md). The tests behind these claims belong in [Part 4](../../development-guide/04-testing-and-evaluation/README.md).

## Working model

Follow sensitive information through its whole lifecycle, not just the first prompt. An input may be normalized, retrieved, summarized, embedded, cached, queued, sent to a provider, used in an answer, and copied into telemetry or a backup. Derived material can reveal facts no single input shows. A data-flow map should show the source, purpose, classification, transformations, recipients, storage locations, and downstream copies for the assessed use. The NIST Privacy Framework (Version 1.0; a 1.1 draft is out for comment) frames privacy risk as a question about how data is processed. It does not say which processing is lawful or acceptable in your domain.[1]

Isolation is an end-to-end authorization property. A filter in an instruction or an initial search query is not enough if a later cache, reranker, memory store, artifact, or log can cross tenant boundaries. Carry trusted actor, tenant, and purpose context to the enforcement point and bind each data access to it. Shared infrastructure can be acceptable when controls and evidence show the required separation; this guide does not prescribe a storage topology.

Auditability means answering questions from evidence: which version and policy were active; which principal and tenant started a request; what authorization and approval checks ran; which capability was invoked; and what the authoritative target says happened. Record decisions, actions, references, and outcomes, not hidden model reasoning. Protect the evidence from unauthorized change and deletion while limiting its content and access. NIST's log-management guide (SP 800-92, 2006; a revised draft was released in 2023) treats logging as an organizational lifecycle and operational process, not a file you switch on.[2]

Integrity mechanisms strengthen evidence but have limits. Certificate Transparency, for example, uses Merkle trees for proofs of inclusion and append-only consistency. RFC 9162 (Experimental; it obsoletes RFC 6962) also describes how a log could show different views to different observers, so comparison and monitoring are needed to expose that.[3] A hash, signature, or append-only store does not prove that all relevant events were captured, that the event producer told the truth, or that anyone reviewed the evidence.

## Decisions and best practices

Start with the data you need and why. Collect less, limit precision, transform or redact fields before model or tool access, and use synthetic or de-identified fixtures for development when they keep the test's purpose. Treat "de-identified" as a risk-reduction claim to verify for the specific data and setting, not a guarantee against linkage or inference. Work with reviewers to identify provider processing, residency, and retention limits. Do not assume a provider's default retention, or a deletion request, equals confirmed deletion.

For multi-tenant retrieval, trace the trusted identity from request admission through candidate retrieval, reranking, context assembly, caching, answer generation, and any later export. A test that asks the model to ignore another tenant's data tests instructions, not isolation. Write adversarial cases for wrong-tenant identifiers, stale authorization, cache-key collisions, concurrent requests, and derived artifacts. Check the access decision at the enforcing boundary and inspect the authoritative data source or event record.

Define the data lifecycle before relying on deletion. Keep an inventory linking source records to derivatives and copies where feasible, and state retention periods, deletion triggers, owners, and verification methods for each class. Cover embeddings, summaries, caches, queued work, replicas, backups, evaluation artifacts, provider-held data, and incident evidence when in scope. Some copies cannot be erased right away or must be kept under an accountable policy. Then document the reason and duration, restrict access and use, and do not claim deletion is complete until the stated verification passes. Reviewers identify the exact legal duties for the use and jurisdiction.

Match isolation to exposure and consequence. Where an agent can run untrusted code or reach sensitive resources:

- give it its own identity and work area, separate from unrelated workloads
- restrict network egress and filesystem access, and cap resource use
- keep agent-controlled code from changing policy, audit controls, or its own containment
- scope credentials to the task and avoid ambient access

Reassess boundaries when capabilities, dependencies, data classes, or tenant populations change. For multiple agents, add the trust-boundary and shared-state controls in [Part 9](../09-multi-agent-systems-and-interoperability/README.md).

For consequential actions, collect evidence that links the initiating request to the policy decision, the exact approved action where approval applies, the execution attempt, and the authoritative outcome. Part 7 owns the approval contract and execution-time authorization; this chapter adds privacy-aware evidence handling and integrity. Keep full prompts, documents, credentials, and unneeded personal data out of audit events. Define who may read, export, amend, or delete the evidence and what happens if the evidence path is down. A transcript or transport acknowledgement is not proof of an external effect.

## Requirements

- **ASSURANCE-01** When an assessment identifies sensitive data, sensitive inference, or domain-specific restrictions, an accountable owner MUST document approved purposes, data classes, transformations, recipients, retention constraints, and required reviewer decisions before the affected processing is enabled. The design MUST reject or route for review a use that falls outside the approved scope. This record does not establish legal compliance.
- **ASSURANCE-02** When one service processes data for multiple users or tenants, each data read, write, retrieval result, cache entry, memory item, and exported artifact MUST be authorized using trusted tenant and purpose context at the relevant enforcement boundary. The system MUST test cross-tenant denial across each enabled path, including concurrent and derived-data paths; prompt instructions alone MUST NOT count as isolation evidence.
- **ASSURANCE-03** When the system retains or derives information from user or source data, its accountable owner MUST define retention and deletion behavior for in-scope originals, derivatives, replicas, caches, queues, backups, evaluation or audit artifacts, and provider-held copies. Deletion verification MUST use a declared evidence source; any exception MUST identify its scope, owner, reason, access/use restrictions, and review or expiry condition.
- **ASSURANCE-04** When the assessment identifies material damage from workload escape, untrusted code, or access to sensitive resources, the system MUST isolate the affected execution identity and work area, constrain its resources and egress, and protect control and evidence mechanisms from agent-controlled modification. Tests MUST demonstrate the selected isolation boundaries and the response to a denied or exhausted boundary.
- **ASSURANCE-05** When consequential-action evidence or elevated auditability is required, the system MUST preserve a privacy-minimized, access-controlled record linking request/run identity, trusted actor and tenant context, relevant agent/policy version, authorization and approval references, action identity, and an authoritative outcome or explicit unknown state. The owner MUST define and test integrity, completeness monitoring, retention, access, and failure handling for that record. Raw hidden chain-of-thought MUST NOT be required as audit evidence.

## Worked example

An internal policy assistant answers employee questions from approved, current, permission-filtered documents. It returns citations and uncertainty and has no external write capability. In this fictional fixture, the current travel policy permits a London hotel amount of GBP 220, and a superseded document gives a different amount. The system serves two tenants whose documents must stay isolated.

The data map follows a question and source passage through retrieval, context assembly, model processing, answer and citation, request telemetry, and a short-lived retrieval cache. The authorization boundary takes the authenticated tenant from the request context and ignores any model-generated tenant label. Retrieval filters by that tenant, and the cache key includes the tenant and corpus version. A release case asks tenant A's assistant to retrieve tenant B's superseded document, then repeats the request concurrently and through the cache. The oracle checks the returned source identifiers and the authoritative access decision, not whether the model says it respected the boundary. A case that returns the other tenant's source is a hard failure even if the final answer happens to be correct.

The lifecycle inventory records source-document identity, corpus version, derived index or embedding, cache, queued request, provider path, and telemetry fields. The team does not log raw questions or source text in routine diagnostics. For the declared period it keeps a request identifier, tenant-bound authorization result, document identifiers and versions, policy version, answer outcome, and safe error category. The deletion test removes a fictional document, rebuilds or invalidates affected derived material by the declared process, clears the cache, and checks that later retrieval cannot return it. It separately records any backup or provider copy outside immediate deletion and applies its documented access and expiry controls. A cleared source table alone would not show that every derivative is gone.

The audit record can show that the answer cited the current version, that the tenant filter admitted only that tenant's source, and that the assistant returned uncertainty when the current source was unavailable. It does not prove the answer was semantically correct; the team evaluates that under Part 4. If a later version gains an approved write capability, add exact approval and external-effect evidence under Part 7. An answer trace does not prove a completed policy update.

## Evidence and checklist

Keep evidence proportionate to the trigger and linked to the assessed system version. A reviewer should be able to find:

- a data-flow and purpose record covering sources, transformations, providers, stores, derived data, and owners;
- the tenant and purpose enforcement design, with negative tests for direct, cached, concurrent, and derived-data access;
- a retention and deletion schedule, lineage or dependency record, verification result, and documented exceptions for inaccessible copies;
- containment boundaries and test evidence for resource, filesystem, network, identity, and control-plane protections where applicable;
- an audit-event definition, access and retention policy, integrity and completeness checks, and a tested response to unavailable or altered evidence; and
- for consequential actions, linked approval and authoritative effect evidence, or an explicit unresolved outcome, without raw hidden reasoning.

Before release, confirm that reviewers identified domain-specific obligations, that tests cover the paths the system actually uses, that any "not applicable" decision has a rationale, and that no planned or unverified control earns risk-reduction credit. A checklist records evidence and decisions; it does not certify legal compliance. Reassess after material changes to data, tenant boundaries, providers, retention, capabilities, audit collection, or threat conditions. Decommissioning must handle active work, credentials, retained evidence, and deletion under the same approved policy.

## References

[1]: https://www.nist.gov/privacy-framework "NIST Privacy Framework"
[2]: https://csrc.nist.gov/pubs/sp/800/92/final "NIST SP 800-92, Guide to Computer Security Log Management (2006)"
[3]: https://www.rfc-editor.org/rfc/rfc9162.html "RFC 9162: Certificate Transparency Version 2.0"

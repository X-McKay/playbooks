# 9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces

**Status:** 0.5.0-draft.2 — draft
**Audience:** Builders, system designers, security reviewers, and operators of multi-agent systems
**Applicability:** Every composition that sends work or transfers responsibility between agents. The A2A subsection applies only when you use that optional protocol.

[Part 9 — Multi-Agent Systems and Interoperability](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md)

This chapter adds edge-level contracts to the composition and membership decisions in [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md). [9.3](03-coordination-system-evaluation-and-operations.md) covers integrated coordination and evidence. Apply single-agent [identity and least privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) and [untrusted-input controls](../../development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) at every edge. Long-running or side-effecting work also falls under [Part 7](../07-durable-execution-and-human-governed-work/README.md).

## Purpose and applicability

Delegation separates expertise or execution, but it creates a trust boundary: a request can disclose data or cause work, and a result can be incomplete or wrong. A message saying "approved" or "completed" proves neither authorization nor an external effect.

These controls apply to local and remote calls. Transport changes identity and delivery mechanics, not the need for contracts, narrow authority, data controls, and failure behavior. A system without delegation needs no agent interface just because it uses MCP or another client-server integration.

## Working model

Treat each edge as a versioned, typed API. The request describes a bounded objective, validated input, recipient, authorized context, and limits. The result identifies the interaction, a typed outcome, output and evidence, unresolved questions, and any actual effects. The caller validates the result before use; a fluent response is not the contract.

A **delegation** returns control to the caller. A **handoff** transfers responsibility. A **review** requests an assessment. A **fan-out** starts bounded branches for a declared aggregation. Names may vary, but ownership must be explicit. A handoff changes ownership, not policy or authority.

Include in each request the parties and versions, actor and tenant, stable interaction and parent IDs, mode, schemas, provenance, classification, deadline, and resource bounds. Distinguish completed, needs-information, rejected or blocked, cancelled, timed-out, and failed outcomes. Keep proposed actions apart from performed effects. Share task-specific inputs or authorized references, not full histories; a reference grants no access by itself.

**Write a delegation brief.** Vague instructions to a sub-agent cause duplicated work, gaps, and wasted spend. A brief states the objective, the output format, which tools and sources to use, and the task boundaries (what is out of scope and where to stop), so that parallel workers do not overlap. [3]

Before dispatch, intersect in code the edge scope, the authority the caller may delegate, callee and role limits, authenticated actor and tenant policy, workflow state, and any approval. An empty intersection denies access. A child cannot restore removed scope or delegate broader authority. [Part 3](../../development-guide/03-security-and-trust-boundaries/README.md) and [Part 7](../07-durable-execution-and-human-governed-work/README.md) hold the underlying identity, authorization, and approval rules.

Requests, results, evidence, and discovered capability descriptions are untrusted data. Apply tenant, purpose, classification, minimization, redaction, artifact access, expiry, retention, and deletion rules at both ends. Do not forward hidden instructions, credentials, unrelated tool output, or full parent history by default.

Bound each interaction's time, requests, tools, input and output, and cost where you can control them. Reserve nested grants from the remaining parent allocation and reconcile usage; unknown cost is not zero. Retries of the same task reuse a stable identity and idempotency context; materially changed work gets a new identity. Do not retry policy, schema, authorization, or budget failures as if they were transient.

A handoff records the current state, objective, evidence and provenance, completed and prohibited actions, remaining limits, open questions, and the new owner before dispatch. Until the receiver accepts, or when delivery is ambiguous or rejected, the current owner stays responsible and follows the escalation path.

### Optional A2A protocol mapping

Local delegation is an architecture pattern, not a wire protocol. For remote, independently built agents, [A2A](https://a2a-protocol.org/v1.0.0/specification/) is an optional open standard, hosted by the Linux Foundation. [4] Version 1.0.0 defines a protocol-neutral model with JSON-RPC, gRPC, and HTTP+JSON bindings. An Agent Card describes identity, capabilities, requirements, and interfaces; a Task tracks work; Messages carry exchanges; Artifacts hold results. Choose a protocol version deliberately; do not assume a discovered peer is compatible. [1]

Map local request and result semantics to protocol messages, task states, and artifacts. The application still defines valid answers, permitted sources, effects, and escalation. A protocol acknowledgement or terminal task state does not prove the answer is correct or that a separate business effect was accepted.

An Agent Card or registry entry finds a possible peer; it does not admit it or authorize a task. Verify identity and membership, then separately authorize the actor, tenant, data, and operation. The specification defines no standard registry API, and cards can expose sensitive details, so prefer authenticated extended cards. [2] Cards may carry JWS signatures, and clients should verify at least one before trusting a card (§8.4). [1] Treat an unsigned card, or one whose signature or issuer you cannot verify against a trusted key store, as an untrusted hint. A signature shows who published the card, not that the agent is safe to admit.

A2A authentication is not business approval. Server authorization is "implementation-specific" (§7.5). In-task authorization uses the authorization-required task state, with credentials best supplied out of band (§7.6), and servers must limit results to the caller's authorization boundaries (§13.1). [1]

MCP is different: it standardizes client-server access to tools, resources, and prompts, while A2A standardizes communication between independent agents. An agent may use MCP to fetch documents while serving an A2A task, and neither protocol replaces composition authorization, data, or evaluation rules. Pin the MCP protocol version as you pin the A2A version. [1] [5]

## Decisions and best practices

Use the smallest typed interface that keeps the meaning. Check access and integrity when resolving artifact references. Choose delegation or handoff by who stays accountable, and define acceptance when ownership moves. For parallel branches, declare the required work, late-result handling, and how disagreement is preserved; [9.3](03-coordination-system-evaluation-and-operations.md) covers aggregation.

Scale delegation to the task: a simple lookup needs one agent and a few calls, and only a broad task justifies many workers. Multi-agent runs cost far more tokens than single-agent runs (see [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md)), so set the worker count and per-worker budget in the brief and enforce them in the runtime. [3]

Admit and pin members through 9.1; dynamic discovery is not admission. Choose A2A only when a remote interoperability boundary calls for it. A standard can simplify message exchange, but it cannot make peers trustworthy or application semantics portable. Test the accepted and rejected paths of your mapping.

## Requirements

- **DELEGATE-01** — For every enabled interaction edge, the composition **MUST** define a versioned request and result contract with validated input/output schemas; caller and callee identities and versions; system, manifest, run, interaction, and parent identifiers; mode; actor and tenant context; provenance or authorized evidence references; data classification; deadline and resource bounds; distinct success, non-success, and unresolved outcomes; and a separate record of proposed versus performed effects. The caller **MUST** validate the returned contract before relying on its output.
- **DELEGATE-02** — Before dispatching delegated work, the composition **MUST** compute effective authority deterministically as an intersection of the edge maximum, caller-delegable authority, callee and role limits, authenticated actor and tenant policy, workflow state, and applicable approval scope. It **MUST NOT** grant a child or descendant broader authority than this intersection. A message or task state **MUST NOT** substitute for execution-time authorization of a protected operation.
- **DELEGATE-03** — For every interaction edge, the composition **MUST** declare and enforce accepted input/evidence types, maximum classification, permitted actor/tenant/purpose, history-sharing, redaction and minimization, artifact authorization/expiry, output limits, and retention/deletion rules. It **MUST NOT** forward credentials, hidden instructions, unrelated tool results, or full parent history by default. Receivers **MUST** treat peer messages and returned artifacts as untrusted input and validate referenced artifact access and integrity before use.
- **DELEGATE-04** — For each delegated interaction, the caller **MUST** set a deadline and bounded resource grant, including applicable request, tool, input/output, and cost limits; a child **MUST NOT** extend its grant. The system **MUST** account for nested and concurrent grants within the parent allocation, record actual usage, release unused reservations, and preserve unknown cost as unknown. Retry ownership and total attempts across layers **MUST** be bounded. Retries of the same logical work **MUST** retain stable interaction identity; materially changed work **MUST** use a new identity. Authorization, policy, and schema failures **MUST NOT** be retried as transient failures.
- **DELEGATE-05** — When responsibility transfers, the current owner **MUST** record the typed current state, objective, evidence and provenance, completed and prohibited actions, remaining authority and limits, open questions, expected outcomes, and new owner before dispatch. Until acceptance is confirmed, or when acceptance is ambiguous or rejected, the current owner **MUST** retain responsibility and apply the declared escalation behavior.
- **DELEGATE-06** — When A2A is used for a remote interaction, the composition **MUST** pin or otherwise identify the selected protocol version and peer identity, map its local request/result and failure semantics to the protocol, and admit the peer under the requirements in [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md). It **MUST NOT** treat capability discovery, protocol authentication, a task acknowledgement, or an authorization-required state as admission, business approval, or authority to perform an operation.

## Worked example

The internal policy assistant answers from approved, current, permission-filtered documents, returning citations and uncertainty. It cannot write externally. A user asks whether a London hotel amount of GBP 220 is permitted. In the fictional `travel-policy-current` fixture, GBP 220 is allowed and a superseded document differs. The assistant delegates evidence gathering to a policy-document specialist and keeps responsibility for the answer.

The request holds a typed question, actor and tenant context, the allowed corpus and fixture reference, read-only scope, a deadline, and a resource ceiling, but not the full conversation or credentials. Before dispatch, the orchestrator checks member admission and intersects edge, caller, specialist-role, and tenant scopes. A cross-tenant access or a write attempt is denied. The specialist returns `completed`, the current citation and version, the superseded reference, and an uncertainty note, with no effects. The caller validates the schema and citation, then answers with a caveat. If the specialist returns `needs_information`, the caller asks for clarification or escalates.

For a remote specialist, a reviewed Agent Card can advertise the A2A interface and capability, with its signature verified against a trusted key, but the composition still checks admission. The caller maps the typed request to an A2A task and validates returned status and artifacts against the local contract. Completion or successful authentication grants no write scope or policy exception.

## Evidence and checklist

Keep sanitized evidence of the interaction and parent IDs, caller, callee, role and versions, manifest and schema identity, effective authorization and data-scope decisions, deadline and budget, status and attempts, validated output or authorized artifact, unresolved issues, and any effect reference. Follow Parts 3 and 5; a useful trace does not need raw prompts or conversation content.

Test allowed and denied callers, malformed schemas, unauthorized artifacts, tenant mismatch, scope amplification, injected peer instructions, exhaustion, duplicate delivery, stale IDs, ambiguous handoffs, late results, and missing-evidence escalation. For A2A, also test version mismatch, changed or untrusted cards, invalid or missing card signatures, authentication failure, interrupted or duplicate notifications where supported, and task-state mapping. Check business claims against authoritative evidence, not only transcripts.

- [ ] Every enabled edge has a versioned, validated request/result contract and explicit failure outcomes.
- [ ] Delegation briefs state objective, output format, tool and source guidance, and boundaries.
- [ ] Discovery and authentication are distinct from admission, authorization, and approval.
- [ ] Authority, tenant scope, data, deadline, and budget are enforced before dispatch and cannot be expanded downstream.
- [ ] Handoff acceptance keeps one accountable owner when delivery fails or is ambiguous.
- [ ] Retries, duplicates, artifacts, and unresolved outcomes have declared handling.
- [ ] Evidence links the interaction to its caller, callee, effective policy, result, and any actual effect.

## References

[1]: https://a2a-protocol.org/v1.0.0/specification/ "Agent2Agent Protocol Specification, version 1.0.0"
[2]: https://a2a-protocol.org/v1.0.0/topics/agent-discovery/ "A2A Agent Discovery"
[3]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
[4]: https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year "A2A protocol surpasses 150 organizations, lands in major cloud platforms, and sees enterprise production use in first year"
[5]: https://modelcontextprotocol.io/docs/learn/architecture "Model Context Protocol Architecture Overview"

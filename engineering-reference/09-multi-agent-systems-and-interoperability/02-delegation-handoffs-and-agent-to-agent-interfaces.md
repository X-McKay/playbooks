# 9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces

**Status:** 0.5.0-draft.2 — draft
**Audience:** Builders, system designers, security reviewers, and operators of multi-agent systems
**Applicability:** Every composition that sends work or transfers responsibility between agents. The A2A subsection applies only when you use that optional protocol.

[Part 9 — Multi-Agent Systems and Interoperability](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md)

Edge contracts for [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md) compositions. Apply [least privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) and [untrusted-input controls](../../development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) at every edge, and [Part 7](../07-durable-execution-and-human-governed-work/README.md) to long-running or side-effecting work.

## Purpose and applicability

Delegation creates a trust boundary: requests can disclose data or cause work, results can be wrong, and "approved" or "completed" in a message proves nothing. The controls apply locally and remotely; MCP or another client-server integration alone needs no agent interface.

## Working model

Each edge is a versioned, typed API. A **delegation** returns control, a **handoff** transfers responsibility (not authority), a **review** requests an assessment, a **fan-out** starts bounded branches.

- **Request:** a bounded objective with validated input, both parties' identities, actor and tenant, deadline and resource limits (full list in DELEGATE-01). Send task-specific inputs or authorized references, not full histories; a reference grants no access by itself.
- **Result:** a typed outcome (`completed`, `needs_information`, `rejected` or `blocked`, `cancelled`, `timed_out`, `failed`), evidence, open questions, and effects performed kept apart from effects proposed. The caller validates it before use.
- **Delegation brief:** objective, output format, tools and sources, and boundaries (what is out of scope, where to stop). Vague briefs make workers duplicate work, leave gaps or miss information.[3]

Before dispatch, code computes the child's **effective authority**: only what the edge, the caller, the callee's role, the actor and tenant policy, the workflow state and any approval all allow (DELEGATE-02). An empty result denies the call, and a child cannot restore scope its parent lost ([Part 3](../../development-guide/03-security-and-trust-boundaries/README.md)). Requests, results, evidence and capability descriptions are untrusted data; apply the DELEGATE-03 data rules at both ends.

A child's budget comes out of what its parent has left, and unknown cost stays unknown, not zero. Retries of the same work keep a stable identity and idempotency context; materially changed work gets a new identity. Do not retry policy, schema, authorization or budget failures as if they were transient. Until a handoff is accepted, the current owner stays responsible and escalates if acceptance fails or is unclear.

### Optional A2A protocol mapping

[A2A](https://a2a-protocol.org/v1.0.0/specification/) is an optional open standard for remote agents, hosted by the Linux Foundation.[4] Version 1.0.0 has JSON-RPC, gRPC and HTTP+JSON bindings: an Agent Card describes identity, capabilities, requirements and interfaces, a Task tracks work, Messages carry exchanges and Artifacts hold results.[1] The application still defines valid answers, effects and escalation; a terminal task state proves neither correctness nor a business effect.

A card or registry entry finds a peer but does not admit it. There is no standard registry API and cards can expose sensitive details, so prefer authenticated extended cards.[2] Verify at least one JWS signature before trusting a card (§8.4); an unverifiable card is an untrusted hint, and a signature shows the publisher, not safety.[1] Server authorization is "implementation-specific" (§7.5), in-task authorization uses the authorization-required state with credentials best sent out of band (§7.6), and servers must limit results to the caller's authorization (§13.1).[1]

MCP standardizes client access to tools, resources and prompts; A2A, communication between agents. An agent may use MCP while serving an A2A task; pin both versions, and neither replaces composition rules.[1] [5]

## Decisions and best practices

- Use the smallest typed interface that keeps the meaning; choose delegation or handoff by who stays accountable.
- For parallel branches, declare required work, late-result handling and how disagreement is kept (9.3).
- Scale delegation to the task (one agent for a lookup, many workers only for broad tasks); set worker count and per-worker budget in the brief and enforce them in the runtime.[3]
- Choose A2A only at a real remote boundary; it cannot make peers trustworthy or semantics portable. Test accepted and rejected paths.

## Requirements

- **DELEGATE-01** — For every enabled interaction edge, the composition **MUST** define a versioned request and result contract with validated input/output schemas; caller and callee identities and versions; system, manifest, run, interaction, and parent identifiers; mode; actor and tenant context; provenance or authorized evidence references; data classification; deadline and resource bounds; distinct success, non-success, and unresolved outcomes; and a separate record of proposed versus performed effects. The caller **MUST** validate the returned contract before relying on its output.
- **DELEGATE-02** — Before dispatching delegated work, the composition **MUST** compute effective authority deterministically as an intersection of the edge maximum, caller-delegable authority, callee and role limits, authenticated actor and tenant policy, workflow state, and applicable approval scope. It **MUST NOT** grant a child or descendant broader authority than this intersection. A message or task state **MUST NOT** substitute for execution-time authorization of a protected operation.
- **DELEGATE-03** — For every interaction edge, the composition **MUST** declare and enforce accepted input/evidence types, maximum classification, permitted actor/tenant/purpose, history-sharing, redaction and minimization, artifact authorization/expiry, output limits, and retention/deletion rules. It **MUST NOT** forward credentials, hidden instructions, unrelated tool results, or full parent history by default. Receivers **MUST** treat peer messages and returned artifacts as untrusted input and validate referenced artifact access and integrity before use.
- **DELEGATE-04** — For each delegated interaction, the caller **MUST** set a deadline and bounded resource grant, including applicable request, tool, input/output, and cost limits; a child **MUST NOT** extend its grant. The system **MUST** account for nested and concurrent grants within the parent allocation, record actual usage, release unused reservations, and preserve unknown cost as unknown. Retry ownership and total attempts across layers **MUST** be bounded. Retries of the same logical work **MUST** retain stable interaction identity; materially changed work **MUST** use a new identity. Authorization, policy, and schema failures **MUST NOT** be retried as transient failures.
- **DELEGATE-05** — When responsibility transfers, the current owner **MUST** record the typed current state, objective, evidence and provenance, completed and prohibited actions, remaining authority and limits, open questions, expected outcomes, and new owner before dispatch. Until acceptance is confirmed, or when acceptance is ambiguous or rejected, the current owner **MUST** retain responsibility and apply the declared escalation behavior.
- **DELEGATE-06** — When A2A is used for a remote interaction, the composition **MUST** pin or otherwise identify the selected protocol version and peer identity, map its local request/result and failure semantics to the protocol, and admit the peer under the requirements in [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md). It **MUST NOT** treat capability discovery, protocol authentication, a task acknowledgement, or an authorization-required state as admission, business approval, or authority to perform an operation.

## Worked example

Asked whether a London hotel amount of GBP 220 is permitted (yes in the fictional `travel-policy-current` fixture; a superseded document differs), the read-only policy assistant delegates evidence gathering to a specialist and keeps the answer.

The request carries a typed question, actor, tenant, corpus and fixture reference, read-only scope, deadline and ceiling, but no history or credentials; cross-tenant access and writes fail the scope intersection. The specialist returns `completed` with the current citation and version, the superseded reference and an uncertainty note; the caller validates them and answers with a caveat, or on `needs_information` asks or escalates.

A remote specialist's verified Agent Card advertises A2A, but admission is still checked, results are validated locally, and completion or authentication grants no write scope or exception.

## Evidence and checklist

Keep sanitized records of IDs, parties, versions, schema, authorization and data-scope decisions, budget, attempts, validated output, open issues and effect references, without raw prompts.

Test denied callers, malformed schemas, unauthorized artifacts, tenant mismatch, scope amplification, injected instructions, exhaustion, duplicates, stale IDs, ambiguous handoffs, late results and missing evidence; for A2A, version mismatch, untrusted or unsigned cards, authentication failure, duplicate notifications and task-state mapping. Check business claims against authoritative evidence.

## References

[1]: https://a2a-protocol.org/v1.0.0/specification/ "Agent2Agent Protocol Specification, version 1.0.0"
[2]: https://a2a-protocol.org/v1.0.0/topics/agent-discovery/ "A2A Agent Discovery"
[3]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
[4]: https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year "A2A protocol surpasses 150 organizations, lands in major cloud platforms, and sees enterprise production use in first year"
[5]: https://modelcontextprotocol.io/docs/learn/architecture "Model Context Protocol Architecture Overview"

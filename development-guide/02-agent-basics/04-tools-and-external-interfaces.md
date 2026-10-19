# 2.4 Tools and External Interfaces

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Agent builders, tool owners, security reviewers, and evaluators who need to make a proposed external operation inspectable

**Applicability:** Apply this chapter when a proposed agent invokes a tool or other external interface. It does not apply when no such capability is enabled. A read-only interface still needs this chapter when it reaches protected data or can affect availability, cost, privacy, or another relevant boundary.

**Reader question:** How can a builder turn a broad external service into a narrow, reviewable operation whose inputs, authority, effects, failures, retries, and evidence remain clear?

[Part 2 — Agent Basics](README.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [tool-contract template](../../templates/2.4/tool-contract.yaml)

## Purpose and applicability

A **tool** is a bounded interface through which an agent can obtain information or request an operation outside its reasoning process. An **external interface** is the wider boundary the tool reaches: a record store, a business service, a device, an internal workflow, or another protected system. A tool contract makes the agent-facing operation smaller and more legible than that underlying system. It says what may be requested, which trusted context is required, what result is allowed back, and how an unusual outcome is represented.

This distinction matters because a broad service or shell-style pass-through makes it difficult to see what the agent can really do. A harmless-sounding operation can disclose a restricted record, mark a record as viewed, trigger an external lookup, or accept an unbounded response. A timeout can leave the caller unable to tell whether an external request was never sent, reached the target, or completed after the response was lost. The contract is therefore a design boundary, not a description written after the fact.

Typed and serializable does not require a particular schema technology. JSON Schema is one neutral vocabulary: its published specification separates Core from Validation and defines validation keywords for JSON data. [1] Whatever notation is used, it should make field shape, allowed values, cross-field rules, and bounded output fields reviewable. A type or schema establishes shape; it does not establish permission, source truth, target identity, or whether the external system actually performed the described operation.

Tools are conditional components. This chapter does not authorize one, choose a service, or declare an interface safe. Agent-level capability admission and the effective configuration remain with [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md). Identity, authority, and protected-operation checks are owned by [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md). Returned content remains data under [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). Source currentness and answer grounding belong to [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md). For a tool exposed through a standardized integration protocol, apply [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) as well.

## Working model

### A narrow operation, not a broad pass-through

Start with a named domain operation, such as `search-approved-policy`, rather than a generic request facility. A narrow operation accepts only the task inputs it needs, receives identity and scope from a trusted runtime boundary, performs declared validation before external I/O, and returns a small domain result. It should not expose an arbitrary destination, free-form method, unfiltered response body, reusable credential, or model-selected authority as a convenience field.

The adapter has two interfaces. The **agent-facing interface** contains caller-controlled task data and bounded outcomes. The **protected-operation interface** binds that task data to the authenticated workload, requester where relevant, effective resource scope, current policy, and normalized target. A model may propose a query or target reference. It cannot turn a proposed identity, tenant, scope, permission, or approval into trusted context.

Validation works in both directions. Before I/O, check basic shape and task rules: required fields, allowed value sets, ranges where relevant, and cross-field constraints. A cross-field rule asks whether fields make sense together. For example, an optional locator can be accepted only when it is in the requester's permitted resource scope, and a selector that conflicts with authenticated scope is rejected rather than repaired into a broader request. Normalize a target before authorization so equivalent spellings, encodings, aliases, or paths cannot cause the check and the external call to refer to different objects.

After I/O, validate the response before the agent sees it. Confirm its status, required identifiers, field types, and bounds. Drop or reject malformed fields, unexpected fields, secrets, unrestricted raw payloads, and content beyond the operation's purpose. Map the result to a declared outcome such as `matches`, `no_match`, `denied`, `unavailable`, `timeout`, or `invalid_result`. The model receives evidence or an outcome, not an opaque provider narrative that it must interpret as authority.

### Describe actual effects and observations

An effect class is a claim about what the target operation actually does, not what the method name, transport, or documentation label suggests. The established draft classes are `read`, `write_reversible`, and `write_consequential`. A `read` observes without changing external business state. A `write_reversible` makes a change that can be meaningfully corrected under its own rules. A `write_consequential` has a material effect or is difficult to reverse. A lookup that updates a view marker, sends a notification, consumes a scarce reservation, or reveals protected content needs a more careful effect analysis than its name suggests.

The draft's established execution-class floor maps a read-only capability to `ephemeral`, a reversible write to `durable`, and a consequential write to `human_governed`. This mapping does not make an operation permitted or low risk, and an agent's effective execution class cannot be lower than an enabled tool's required floor. Long-running or resumable work can still need durable handling even when it is read-only. When a proposed interface has an externally visible effect, may outlive its request, or needs safe resumption, use [Part 7 — Durable Execution and Human-Governed Work](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) rather than treating the tool contract as a complete recovery design.

Keep the following observations distinct:

- A **proposal** is a model or workflow request for an operation. It has not passed enforcement.
- An **authorized admission** is the protected boundary's decision that this authenticated request may use the operation on this normalized target. It is not proof of a dispatch or effect.
- A **dispatch attempt** records that the runtime tried to send a request. It is useful for diagnosis but is not target acceptance.
- A **response** is what the external interface returned. It can be malformed, stale, or lost.
- An **authoritative external effect** is target-side evidence that the target accepted or performed a material operation. A local log, model statement, or response-shaped object is not that evidence.

This model prevents two opposite errors: calling every blocked proposal an external failure, and calling a local success message proof of an external outcome. It also makes a negative test meaningful. A blocked request to another tenant can show that an authorization boundary rejected the proposal without implying that cross-tenant data was read.

### Retry safety is not effect class

Effect class and retry safety answer different questions. A read can be unsafe to repeat if it has a relevant repeated effect, while a write can be repeatable only when the receiver actually guarantees the same intended result for the same intent. RFC 9110 defines idempotency in terms of intended server effect, not identical responses or the absence of repeated logging. It permits a retry after a communication failure before the client can read the response, but cautions against automatic retry of a non-idempotent request unless the client knows the operation is idempotent for that resource or can establish that the original was not applied. [2]

For each operation, choose the chapter's declared retry label and explain the basis:

- `safe` means repeating the same intent cannot create an additional relevant effect in the declared context.
- `idempotency_key_required` means a stable key is reused only for the same intent and the target is known to honor that rule.
- `unsafe` means repetition may duplicate an effect, so the runtime does not retry it automatically.

These labels are not promises of availability or correctness. A deadline or cancellation request is an observation about the caller's wait, not proof that an external call did not start or complete. For a side-effecting operation with a missing or ambiguous receipt, stop automatic repetition and follow the declared reconciliation or unresolved path in [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). A consequential action also retains independent authority and any applicable approval; approval does not widen authorization. [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) owns those state semantics.

## Decisions and best practices

### Shape the operation around a task decision

Define the smallest operation that supplies the next legitimate task decision. A policy assistant usually needs a permission-filtered policy search with source identity and bounded excerpt. It does not need general database access, a bulk export, or an arbitrary URL fetch. This reduces accidental capability and makes both negative cases and effect classification easier to inspect.

Choose fields because a builder can name the decision they support. A query may be caller-controlled task data. Requester identity, tenant or resource scope, deadline, and policy context are trusted dependencies whose sources belong in the agent contract. A record identifier offered by a user or model can be useful input, but it remains a request parameter until the protected boundary authorizes access to the normalized object. Do not include a field merely because an underlying service accepts it.

For output, prefer a small status plus the fields necessary to support the next agent decision. Return source identity, revision, status, and a bounded excerpt when the task needs policy evidence. Return a denial without protected content when access is not allowed. A tool result is not a trusted instruction and it is not proof that a downstream answer is supported. Keep source precedence, currentness, and semantic grounding with [2.6](06-context-and-retrieval-fundamentals.md).

### Bind authority at the protected operation

Authentication identifies a workload or requester. Authorization decides whether the relevant protected operation may access this object, function, tenant, data category, or destination now. OWASP describes object-level authorization as checking whether a logged-in user has permission for the requested action on the requested object, and recommends testing that mechanism. [3] Its Authorization Cheat Sheet further recommends deny-by-default decisions and checking the specific object or function on every request. [4]

Apply those principles at the adapter or resource boundary where the operation actually occurs. The decision should use trusted identity, normalized target, requested action, and effective scope. Revalidate before a write when the target or authority can have changed. A prompt, model message, client-side check, retrieved document, capability description, or previous approval is not the decisive authorization decision. This chapter points to that boundary; the canonical requirements and scope choices remain in [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

### Make failure and cancellation useful to a caller

Give the runtime structured outcomes that distinguish invalid input, authorization denial, a domain-level result such as no match, transient unavailability, timeout, and malformed result. They are not interchangeable. A generic error encourages the model to invent a policy answer or retry an unsafe call. A bounded outcome instead lets the agent contract select `needs_information`, `declined`, `failed`, or another declared terminal outcome.

Set a context-appropriate deadline through the trusted execution path and document what cancellation means for the adapter. Cancellation can prevent a proposal from being dispatched, race with a dispatch, or arrive after a target has done work. If the system cannot distinguish those cases, record the uncertainty rather than claiming that external work stopped. A long-running read-only interface can therefore trigger durable execution concerns without becoming a consequential action or gaining an approval flow.

### Minimize data and retain privacy-safe attribution

Return only what the task needs and make returned external content visibly data. Limit excerpts and identifiers before model exposure. Do not pass secrets, live clients, credentials, diagnostic payloads, or an unbounded raw response through the agent-facing contract. Data classification, permitted destinations, content capture, retention, and deletion are independently decided under [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

The minimum useful attribution links an observed invocation to the agent, run, tool operation, attempt, structured outcome, and latency or cost when relevant and available. It need not fabricate a workflow identifier for an ephemeral path or an approval identifier for a read-only path. Conversely, a concise attribution record does not prove the external target's effect. Record the target-side evidence required for that claim where an effect is in scope.

### Build the contract before admitting the capability

Use this practical sequence for a proposed interface:

1. State the task decision and the one domain operation required for it. Write down what the operation must not expose or do.
2. Specify caller-controlled inputs separately from trusted runtime context. Define pre-I/O shape, cross-field, normalization, and scope checks.
3. Specify bounded output fields and structured outcomes. Decide how the agent maps each one to its declared terminal outcomes without guessing.
4. Classify the actual effect and required execution floor. Ask explicitly whether the target records a read, sends a notification, changes availability, or may need durable handling.
5. Declare retry safety, deadline, cancellation observation, and the response-loss path. Route uncertain external effects to Part 7 before enabling them.
6. Plan observable allowed, denied, malformed, timeout, repeated-call, and negative-invocation cases. Record what target-side observation, if any, would establish an external effect.

The [tool-contract template](../../templates/2.4/tool-contract.yaml) turns that sequence into one proposed planning/build record. It deliberately keeps owner, target semantics, data classification, and cancellation details unresolved where the shared example has not established them. It is not an admitted capability manifest, a test result, or an implementation instruction.

## Requirements

- **TOOL-01** When an agent enables an external interface, its owner MUST define a typed, serializable input and output contract, validate inputs before external I/O, and validate and bound results before returning them to the agent.
- **TOOL-02** When an interface can access or change external data, its contract MUST declare its actual effect and required execution-class floor; an agent MUST NOT enable it if the effective execution class is below that floor.
- **TOOL-03** When an interface accesses a protected resource or performs an action, its execution path MUST apply the trusted-identity and deterministic-authorization controls required by [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) to the requested operation and object before access or effect; model-supplied identity, permission, or approval claims MUST NOT grant authority.
- **TOOL-04** When an interface can time out or fail, its contract MUST define bounded timeouts and distinguish validation, authorization, business, transient, timeout, and malformed-result outcomes sufficiently for the runtime to apply its declared failure policy.
- **TOOL-05** When an interface can be invoked more than once, its contract MUST declare retry safety as `safe`, `idempotency_key_required`, or `unsafe`; the runtime MUST NOT automatically repeat an unsafe operation, and an idempotency-key-required operation MUST reuse a stable key only for the same intent.
- **TOOL-06** When a tool returns external or sensitive data to an agent, it MUST return only the bounded fields needed for the task, MUST NOT expose secrets or unbounded raw responses, and MUST handle returned content under [3.2’s untrusted-input controls](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).
- **TOOL-07** When a tool is invoked, its execution path MUST retain privacy-safe attribution sufficient to associate the invocation with the agent, run, tool, outcome, latency, and attempt, and cost when relevant and available; workflow or approval identifiers MUST be present only when those concepts apply.

## Worked example

The shared fictional candidate is `POLICY-BUILD-001`, an internal policy-assistance proposal with `use_case_id: internal-policy-assistance`. Its planning record provisionally prefers a fixed retrieval-and-answer workflow. The fixed workflow may branch on a result or use a model router, but its permitted transitions are defined by orchestration. A bounded adaptive alternative could choose among a finite allowlist of the same operations without creating a broad service pass-through. Neither form changes the current decision: this is an illustrative, unexecuted read-only candidate with no write or approval capability enabled.

### Proposed read-only policy search

The candidate proposes `search-approved-policy` as a narrow operation. The runtime receives `employee-uk-104` and the relevant permitted scope from its trusted request boundary. The model supplies only the employee's question as `query`; it cannot select another tenant, assert a permission, or make a source identifier authoritative. Before a search, the adapter validates that the query is non-empty, normalizes an optional permitted selector, and authorizes the requested source access against trusted context.

The proposed contract is deliberately compact. It is a planning artifact, not a record of a live call:

```yaml
example_id: POLICY-BUILD-001
use_case_id: internal-policy-assistance
status: illustrative-unexecuted
operation: search-approved-policy
admission_status: not_admitted
effect: read
execution_class_floor: ephemeral
input:
  query: non_empty_text
  requester_context: trusted_runtime_context
output:
  status: [matches, no_match, denied, unavailable, timeout, invalid_result]
  match_fields: [source_id, source_revision, current_status, bounded_excerpt]
retry:
  classification: safe_pending_target_semantics_review
  if_uncertain: stop_automatic_repeat
```

For the permitted fixture case, the expected bounded result identifies `travel-policy-2026@2026-10-01` as current and returns only an excerpt needed to support the answer that the fictional London hotel amount is GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` may be identified as superseded rather than used as current authority. The answer workflow then decides whether the available, permitted, current evidence supports `complete`; currentness and semantic support are not settled merely by the tool status.

For the denied fixture case, `contractor-uk-204` is not permitted to access the policy material. The protected operation should return `denied` without source text. The agent's declared terminal outcome is then `declined`, not an improvised policy answer. For a missing permitted source or equally authoritative current-source conflict, the bounded path is `needs_information`; the tool does not select a convenient value or claim that an absent result proves no policy exists.

Consider a proposed timeout. The adapter can report `timeout`, but that response alone does not prove whether it dispatched a request or whether the target observed one. The template's `safe_pending_target_semantics_review` label means a builder must establish that repeating the lookup has no additional relevant effect before automatic repetition. If that cannot be established, it stops automatic repeats and returns the declared bounded failure path. This is an expected behavior to evaluate, not an observed result.

If a later, separate candidate proposed an action that changed policy content, it would not be a new field on this read-only contract. It would need its own actual-effect assessment, execution class, authorization decision, retry and unknown-outcome disposition, and any applicable human-governed approval handling before admission. This chapter does not assert that such a candidate has been proposed, approved, or implemented.

## Evidence and checklist

For a proposed tool, evidence should connect the contract to observable behavior without treating a schema, a tool description, a passing fixture, or a model statement as proof that every control is effective. A reviewer should be able to inspect the declared operation, effective capability admission when one exists, trusted-context sources, validation behavior, bounded output, failure mapping, and the observation needed to support any external-effect claim.

The following evidence plan is proportionate to the shared read-only example and remains unexecuted:

- A contract review shows the operation's task purpose, caller fields, trusted dependencies, effect claim, execution floor, response bounds, retry classification, and declared owner or unresolved owner field.
- Boundary cases show validation failure before external I/O; an allowed requester/object/scope path; a denied requester, object, or scope path without protected-content leakage; and a negative case in which an unavailable or unadmitted capability is not invoked.
- Result cases show a bounded well-formed result, an oversized or malformed result mapped to `invalid_result`, a missing permitted source, and an equally authoritative current-source conflict that is not silently resolved by a date or model preference.
- Failure and retry cases show the declared timeout, cancellation ambiguity, transient failure, and repeat behavior. If an external effect is later in scope, inspect authoritative target state or its accepted-operation record rather than only a transcript or local status.
- Privacy-safe attribution shows the agent, run, operation, attempt, outcome, and applicable latency or cost without retaining secrets or unnecessary payload content. Apply [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) for the data-handling decision.

Hand the resulting proposed record and any future observations to the relevant owners: [2.6](06-context-and-retrieval-fundamentals.md) for source/currentness and grounding, [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) for authorization, [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) for returned content, [Part 4](../04-testing-and-evaluation/README.md) for case and evidence design, and [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) for durable or externally effectful work. The artifact is a proposed local review unit, not an approved or deployed system.

## References

[1]: https://json-schema.org/specification "JSON Schema Specification"
[2]: https://httpwg.org/specs/rfc9110.html "RFC 9110 HTTP Semantics"
[3]: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ "OWASP API1 2023 Broken Object Level Authorization"
[4]: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html "OWASP Authorization Cheat Sheet"

# 2.4 Tools and External Interfaces

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent builders, tool owners, security reviewers, and evaluators who need to make an external operation inspectable

**Applicability:** Apply this chapter when an agent invokes a tool or other external interface. A read-only interface still needs it when it reaches protected data or can affect availability, cost, privacy, or another boundary.

**Reader question:** How do you turn a broad external service into a narrow, reviewable operation whose inputs, authority, effects, failures, retries, and evidence are clear?

[Part 2 — Agent Basics](README.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [tool-contract template](../../templates/2.4/tool-contract.yaml)

## Purpose and applicability

A **tool** is a bounded interface through which an agent gets information or requests an operation outside its reasoning process. An **external interface** is the wider system it reaches, such as a record store, business service, device, or internal workflow. A tool contract makes the agent-facing operation smaller and clearer than that system: what may be requested, which trusted context is required, what result may come back, and how an unusual outcome is shown.

This matters because a broad service or shell-style pass-through hides what the agent can really do. A harmless-sounding operation can disclose a restricted record, mark a record as viewed, or accept an unbounded response. A timeout can leave the caller unable to tell whether a request was never sent, reached the target, or finished after the response was lost. Write the contract as a design boundary before building.

Typed and serializable does not require a particular schema technology. JSON Schema is one neutral option; its specification separates Core from Validation. [1] Whatever notation you use, it should make field shape, allowed values, cross-field rules, and output bounds reviewable. A schema establishes shape, not permission, source truth, target identity, or that the external system did the operation.

Tools are optional. This chapter does not authorize one or declare an interface safe. Admission is in [2.2](02-agent-contracts-and-configuration.md); identity and authority in [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md); returned content as data in [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md); currentness and grounding in [2.6](06-context-and-retrieval-fundamentals.md). For tools exposed through a standard integration protocol, also apply [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md).

## Working model

### A narrow operation, not a broad pass-through

Start with a named domain operation, such as `search-approved-policy`, not a generic request facility. A narrow operation takes only the inputs the task needs, gets identity and scope from a trusted runtime boundary, validates before external I/O, and returns a small domain result. Do not expose an arbitrary destination, free-form method, unfiltered response body, reusable credential, or model-chosen authority as a convenience field.

The adapter has two interfaces. The **agent-facing interface** holds caller-controlled task data and bounded outcomes. The **protected-operation interface** binds that data to the authenticated workload, the requester where relevant, the effective scope, current policy, and a normalized target. A model may propose a query or target reference, but it cannot turn a proposed identity, tenant, scope, permission, or approval into trusted context.

Validate in both directions. Before I/O, check required fields, allowed values, ranges, and cross-field constraints (do the fields make sense together?). For example, accept an optional locator only inside the requester's permitted scope, and reject a selector that conflicts with authenticated scope rather than widening it. Normalize the target before authorization so equivalent spellings, encodings, aliases, or paths cannot make the check and the call refer to different objects.

After I/O, validate the response before the agent sees it: status, required identifiers, types, and bounds. Drop or reject malformed or unexpected fields, secrets, raw payloads, and content beyond the operation's purpose. Map the result to a declared outcome such as `matches`, `no_match`, `denied`, `unavailable`, `timeout`, or `invalid_result`. The model gets evidence or an outcome, not an opaque provider narrative.

### Describe actual effects and observations

An effect class is a claim about what the target operation actually does, not what its method name or documentation suggests. The classes are `read` (observes without changing external business state), `write_reversible` (a change that can be meaningfully corrected under its own rules), and `write_consequential` (a material effect or hard to reverse). A lookup that updates a view marker, sends a notification, uses up a scarce reservation, or reveals protected content needs more careful analysis than its name suggests.

The execution-class floor maps a read-only capability to `ephemeral`, a reversible write to `durable`, and a consequential write to `human_governed`. The mapping does not make an operation permitted or low risk, and an agent's effective execution class cannot be lower than an enabled tool's floor. Read-only work that is long-running or resumable can still need durable handling. For externally visible effects, work that may outlive its request, or safe resumption, use [Part 7 — Durable Execution and Human-Governed Work](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).

Keep these observations distinct:

- A **proposal** is a model or workflow request for an operation. It has not passed enforcement.
- An **authorized admission** is the protected boundary's decision that this authenticated request may use the operation on this normalized target. It does not prove dispatch or effect.
- A **dispatch attempt** records that the runtime tried to send a request. It helps diagnosis but is not target acceptance.
- A **response** is what the external interface returned. It can be malformed, stale, or lost.
- An **authoritative external effect** is target-side evidence that the target accepted or performed a material operation. A local log, model statement, or response-shaped object is not that evidence.

This avoids two errors: calling every blocked proposal an external failure, and treating a local success message as proof of an external outcome. A blocked request to another tenant shows an authorization boundary rejected the proposal, without implying that cross-tenant data was read.

### Retry safety is not effect class

Effect class and retry safety are different questions. A read can be unsafe to repeat if repeating has an effect; a write is repeatable only if the receiver guarantees the same result for the same intent. RFC 9110 defines idempotency by intended server effect, not identical responses, and cautions against automatically retrying a non-idempotent request unless the client knows it is idempotent or can tell the original was not applied. [2]

For each operation, choose a retry label and give the basis:

- `safe`: repeating the same intent cannot create an additional relevant effect in the declared context.
- `idempotency_key_required`: a stable key is reused only for the same intent, and the target is known to honor that rule.
- `unsafe`: repetition may duplicate an effect, so the runtime does not retry automatically.

These labels do not promise availability or correctness. A deadline or cancellation tells you about the caller's wait, not whether an external call started or finished. For a side-effecting operation with a missing or ambiguous receipt, stop automatic repetition and follow [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). A consequential action also keeps independent authority and any required approval; approval does not widen authorization. [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) covers those states.

## Decisions and best practices

### Shape the operation around a task decision

Define the smallest operation that supplies the next legitimate task decision. A policy assistant needs a permission-filtered policy search with source identity and a bounded excerpt, not general database access, bulk export, or arbitrary URL fetch. This limits accidental capability and makes negative cases and effect classification easier to inspect.

Choose each field because you can name the decision it supports. A query may be caller-controlled task data. Requester identity, scope, deadline, and policy context are trusted dependencies whose sources belong in the agent contract. A record identifier from a user or model is only a request parameter until the protected boundary authorizes access to the normalized object.

For output, prefer a small status plus the fields the next decision needs: source identity, revision, status, and a bounded excerpt. On a denial, return no protected content. A tool result is not a trusted instruction and does not prove an answer is supported ([2.6](06-context-and-retrieval-fundamentals.md)).

### Design the tool for the model that will use it

The model sees only a tool's name, description, parameters, and results, so design them for that reader. Published engineering guidance on writing tools for agents suggests the following as general practice. [5]

- **Few, well-scoped tools.** Prefer a small set that each do one distinct job over many overlapping tools or a thin wrapper around every endpoint; overlap makes the model's choice ambiguous. Merge steps that always occur together (one schedule tool rather than separate list and create tools).
- **Clear names and namespacing.** Name tools for the task and group related tools under a shared prefix (for example `policy_search`, `policy_get_source`).
- **Descriptions written for a newcomer.** Say what the tool does, when to use it, when not to, and what each parameter means, with format and an example. Use unambiguous parameter names (`user_id`, not `user`).
- **Poka-yoke arguments.** Shape arguments so mistakes are hard to make, for example by requiring one canonical form of a path or identifier. [6]
- **Meaningful, token-efficient results.** Return the high-signal fields the next decision needs, in readable form (names and status, not raw internal IDs). Paginate, filter, and truncate with sensible defaults. Where useful, offer a concise and a detailed response mode, and tell the model how to narrow a broad result.
- **Actionable errors.** Say what went wrong and what valid input looks like, not only a code or stack trace. Keep errors free of protected content and map them to the structured outcomes below.

Treat tool design as something you measure: run representative tasks, read transcripts for wrong-tool choices and malformed arguments, revise names, descriptions, and outputs, and confirm the gains on held-out tasks. [5] Part 4 covers evaluation. For a large catalogue, loading every definition up front bloats context and causes mis-selection; expose tools progressively (for example by search) and keep bulky intermediate data out of the model's context. [7] [2.7](07-mcp-and-standardized-integrations.md) covers catalogues from standard protocols. None of this replaces the validation and authorization in this chapter.

If the agent can write and run code or use a shell or browser, run that code in a sandbox with resource limits, scoped network egress, and monitoring. [7] Part 3 covers the surrounding boundaries.

### Bind authority at the protected operation

Authentication identifies a workload or requester. Authorization decides whether the protected operation may access this object, function, tenant, data category, or destination now. OWASP describes object-level authorization as checking that a user may take the requested action on the requested object, and recommends testing it. [3] Its Authorization Cheat Sheet recommends deny-by-default and checking the object or function on every request. [4]

Apply these at the adapter or resource boundary, using trusted identity, normalized target, requested action, and effective scope. Revalidate before a write when the target or authority may have changed. A prompt, model message, client-side check, retrieved document, tool description, or earlier approval is not the deciding authorization ([3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)). Keep the tool set to the least the task needs; each extra tool widens what a manipulated model could do. [8]

### Make failure and cancellation useful to a caller

Give the runtime structured outcomes that separate invalid input, authorization denial, a domain result such as no match, transient unavailability, timeout, and malformed result. A generic error pushes the model to invent an answer or retry an unsafe call. A bounded outcome lets the contract choose `needs_information`, `declined`, `failed`, or another declared outcome.

Set a deadline through the trusted execution path and document what cancellation means. Cancellation can stop a proposal before dispatch, race with a dispatch, or arrive after the target did the work. If you cannot tell which, record the uncertainty rather than claiming the work stopped.

### Minimize data and keep privacy-safe attribution

Return only what the task needs and make returned external content visibly data. Limit excerpts and identifiers before the model sees them. Pass no secrets, live clients, credentials, diagnostic payloads, or unbounded raw responses. Classification, destinations, capture, retention, and deletion are decided under [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

The minimum useful attribution links an invocation to the agent, run, tool operation, attempt, outcome, and latency or cost where available. Do not invent a workflow ID for an ephemeral path or an approval ID for a read-only path. Attribution does not prove the target's effect; where an effect is in scope, record target-side evidence.

### Build the contract before admitting the capability

1. State the task decision and the one domain operation it needs, and what the operation must not expose or do.
2. Separate caller-controlled inputs from trusted context. Define pre-I/O shape, cross-field, normalization, and scope checks.
3. Specify bounded output fields and structured outcomes, and how each maps to a declared terminal outcome.
4. Classify the actual effect and execution floor: does the target record a read, send a notification, or need durable handling?
5. Declare retry safety, deadline, cancellation behavior, and the response-loss path. Send uncertain external effects to Part 7.
6. Plan allowed, denied, malformed, timeout, repeated-call, and negative-invocation cases, and the target-side observation that would establish an effect.

The [tool-contract template](../../templates/2.4/tool-contract.yaml) turns this sequence into one planning record.

## Requirements

- **TOOL-01** When an agent enables an external interface, its owner MUST define a typed, serializable input and output contract, validate inputs before external I/O, and validate and bound results before returning them to the agent.
- **TOOL-02** When an interface can access or change external data, its contract MUST declare its actual effect and required execution-class floor; an agent MUST NOT enable it if the effective execution class is below that floor.
- **TOOL-03** When an interface accesses a protected resource or performs an action, its execution path MUST apply the trusted-identity and deterministic-authorization controls required by [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) to the requested operation and object before access or effect; model-supplied identity, permission, or approval claims MUST NOT grant authority.
- **TOOL-04** When an interface can time out or fail, its contract MUST define bounded timeouts and distinguish validation, authorization, business, transient, timeout, and malformed-result outcomes sufficiently for the runtime to apply its declared failure policy.
- **TOOL-05** When an interface can be invoked more than once, its contract MUST declare retry safety as `safe`, `idempotency_key_required`, or `unsafe`; the runtime MUST NOT automatically repeat an unsafe operation, and an idempotency-key-required operation MUST reuse a stable key only for the same intent.
- **TOOL-06** When a tool returns external or sensitive data to an agent, it MUST return only the bounded fields needed for the task, MUST NOT expose secrets or unbounded raw responses, and MUST handle returned content under [3.2’s untrusted-input controls](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).
- **TOOL-07** When a tool is invoked, its execution path MUST retain privacy-safe attribution sufficient to associate the invocation with the agent, run, tool, outcome, latency, and attempt, and cost when relevant and available; workflow or approval identifiers MUST be present only when those concepts apply.

## Worked example

The shared fictional candidate is `POLICY-BUILD-001`, an internal policy-assistance proposal with `use_case_id: internal-policy-assistance`. It prefers a fixed retrieval-and-answer workflow; a bounded adaptive alternative could choose among a finite allowlist of the same operations. Either way it is read-only, with no write or approval capability. All identities and values are fictional.

### Proposed read-only policy search

The candidate proposes `search-approved-policy`. The runtime receives `employee-uk-104` and the permitted scope from its trusted request boundary. The model supplies only the question as `query`; it cannot pick another tenant, assert a permission, or make a source identifier authoritative. Before searching, the adapter checks that the query is non-empty, normalizes an optional permitted selector, and authorizes the source access.

The proposed contract is compact:

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

For the permitted case, the expected result identifies `travel-policy-2026@2026-10-01` as current and returns only the excerpt supporting the fictional London hotel amount of GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` may be marked superseded, not used as current authority. The answer workflow decides whether that evidence supports `complete`; tool status alone does not settle currentness or support.

For the denied case, `contractor-uk-204` may not access the policy material. The protected operation returns `denied` without source text, and the agent's outcome is `declined`, not an improvised answer. For a missing permitted source or an equal-authority current-source conflict, the path is `needs_information`; the tool does not choose a convenient value or treat an absent result as proof that no policy exists.

On a `timeout`, the adapter cannot tell whether a request was dispatched or the target saw it. The `safe_pending_target_semantics_review` label means the builder must show that repeating the lookup has no additional relevant effect before repeating automatically; if that cannot be shown, stop repeats and return the declared failure.

A later candidate that changes policy content would need its own effect assessment, execution class, authorization, retry and unknown-outcome handling, and any human-governed approval; it is not a new field on this contract.

## Evidence and checklist

Connect the contract to observable behavior; a schema, tool description, passing fixture, or model statement does not prove a control works. Evidence for the read-only example:

The evidence plan for the read-only example:

- **Contract review:** purpose, caller fields, trusted dependencies, effect claim, execution floor, response bounds, retry label, and owner (or an unresolved owner field).
- **Boundary cases:** validation failure before external I/O; an allowed path; a denied path without leakage; an unadmitted capability that is not invoked.
- **Result cases:** a bounded result; an oversized or malformed result mapped to `invalid_result`; a missing permitted source; an equal-authority conflict not resolved by date or model preference.
- **Failure and retry cases:** timeout, cancellation ambiguity, transient failure, and repeats. If an external effect is in scope, inspect target state, not just a transcript or local status.
- **Attribution:** agent, run, operation, attempt, outcome, and any latency or cost, without secrets or extra payload.

Hand results to the owners: [2.6](06-context-and-retrieval-fundamentals.md) (currentness, grounding), [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) (authorization), [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) (returned content), [Part 4](../04-testing-and-evaluation/README.md) (cases), and [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) (durable or effectful work).

## References

[1]: https://json-schema.org/specification "JSON Schema Specification"
[2]: https://httpwg.org/specs/rfc9110.html "RFC 9110 HTTP Semantics"
[3]: https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/ "OWASP API1:2023 Broken Object Level Authorization"
[4]: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html "OWASP Authorization Cheat Sheet"
[5]: https://www.anthropic.com/engineering/writing-tools-for-agents "Writing effective tools for agents — with agents"
[6]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"
[7]: https://www.anthropic.com/engineering/code-execution-with-mcp "Code execution with MCP: building more efficient agents"
[8]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"

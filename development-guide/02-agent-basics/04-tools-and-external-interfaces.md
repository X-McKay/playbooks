# 2.4 Tools and External Interfaces

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent builders, tool owners, security reviewers, and evaluators who need to make an external operation inspectable

**Applicability:** Apply this chapter when an agent invokes a tool or other external interface. A read-only interface still needs it when it reaches protected data or can affect availability, cost, privacy, or another boundary.

**Reader question:** How do you turn a broad external service into a narrow, reviewable operation whose inputs, authority, effects, failures, retries, and evidence are clear?

[Part 2 — Agent Basics](README.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [tool-contract template](../../templates/2.4/tool-contract.yaml)

## Purpose and applicability

A **tool** is a bounded interface through which an agent gets information or requests an operation outside its reasoning process. An **external interface** is the wider system it reaches, such as a record store, business service, device, or internal workflow. A tool contract makes the agent-facing operation smaller and clearer than that system.

A broad service or shell-style pass-through hides what the agent can really do: a harmless-sounding operation can disclose a restricted record, mark it viewed, or accept an unbounded response. Write the contract before building.

"Typed and serializable" requires no particular schema technology; JSON Schema is one neutral option, with Core separate from Validation. [1] Any notation should make field shape, allowed values, cross-field rules, and output bounds reviewable, remembering that shape is not permission, source truth, target identity, or proof the operation happened.

Tools are optional. Admission: [2.2](02-agent-contracts-and-configuration.md); identity and authority in [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md); returned content as data in [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md); currentness and grounding in [2.6](06-context-and-retrieval-fundamentals.md); standard-protocol tools also in [2.7](07-mcp-and-standardized-integrations.md).

## Working model

### A narrow operation, not a broad pass-through

Start with a named domain operation, such as `search-approved-policy`, that takes only needed inputs, gets identity and scope from a trusted runtime boundary, validates before I/O, and returns a small result. Never expose an arbitrary destination, free-form method, unfiltered response body, reusable credential, or model-chosen authority as a convenience field.

The adapter has an **agent-facing interface** for caller task data and bounded outcomes, and a **protected-operation interface** that binds that data to the authenticated workload, the requester where relevant, effective scope, current policy, and a normalized target. A model may propose a query or target reference but cannot turn a proposed identity, tenant, scope, permission, or approval into trusted context.

Before I/O, check fields, allowed values, ranges, and cross-field consistency: accept an optional locator only inside the requester's permitted scope, and reject a selector that conflicts with authenticated scope rather than widening it. Normalize the target before authorization so equivalent spellings, encodings, aliases, or paths cannot make the check and the call refer to different objects.

After I/O, validate status, required identifiers, types, and bounds before the agent sees the response. Drop or reject malformed or unexpected fields, secrets, raw payloads, and content beyond the operation's purpose, and map the result to a declared outcome such as `matches`, `no_match`, `denied`, `unavailable`, `timeout`, or `invalid_result`. The model never gets an opaque provider narrative.

### Describe actual effects and observations

An effect class describes what the target operation actually does, not what its name suggests: `read` (observes without changing external business state), `write_reversible` (a change that can be meaningfully corrected under its own rules), or `write_consequential` (material or hard to reverse). A lookup that updates a view marker, sends a notification, uses a scarce reservation, or reveals protected content is not a simple read.

The execution-class floor maps `read` to `ephemeral`, a reversible write to `durable`, and a consequential write to `human_governed`. The floor does not make an operation permitted or low risk, and long-running or resumable reads can still need durable handling. For externally visible effects, work that may outlive its request, or safe resumption, use [Part 7 — Durable Execution and Human-Governed Work](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).

Keep these observations distinct:

- A **proposal** is a model or workflow request that has not passed enforcement.
- An **authorized admission** is the protected boundary's decision that this authenticated request may use the operation on this normalized target. It does not prove dispatch or effect.
- A **dispatch attempt** records that the runtime tried to send a request, not that the target accepted it.
- A **response** is what the interface returned; it can be malformed, stale, or lost.
- An **authoritative external effect** is target-side evidence that the target accepted or performed a material operation. A local log, model statement, or response-shaped object is not that evidence.

A blocked cross-tenant request is a rejected proposal, not an external failure or a cross-tenant read, and a local success message is not proof of an outcome.

### Retry safety is not effect class

A read can be unsafe to repeat if repeating has an effect; a write is repeatable only if the receiver guarantees the same result for the same intent. RFC 9110 defines idempotency by intended server effect, not identical responses, and cautions against automatically retrying a non-idempotent request unless the client knows it is idempotent or can tell the original was not applied. [2]

Give each operation a retry label and its basis:

- `safe`: repeating the same intent cannot create an additional relevant effect in the declared context.
- `idempotency_key_required`: a stable key is reused only for the same intent, and the target is known to honor it.
- `unsafe`: repetition may duplicate an effect, so the runtime never retries automatically.

Labels promise neither availability nor correctness. For a side-effecting operation with a missing or ambiguous receipt, stop automatic repetition and follow [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). A consequential action keeps independent authority and any required approval, and approval does not widen authorization ([7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)).

## Decisions and best practices

### Shape the operation around a task decision

Define the smallest operation that supplies the next legitimate task decision: a policy assistant needs a permission-filtered search returning source identity and a bounded excerpt, not database access, bulk export, or arbitrary URL fetch.

Choose each field for a decision you can name. A query may be caller task data; requester identity, scope, deadline, and policy context are trusted dependencies declared in the agent contract. A record identifier from a user or model is only a request parameter until the protected boundary authorizes the normalized object.

Output is a small status plus what the next decision needs; a denial returns no protected content. A tool result is not a trusted instruction and does not prove an answer is supported ([2.6](06-context-and-retrieval-fundamentals.md)).

### Design the tool for the model that will use it

The model sees only a tool's name, description, parameters, and results. Engineering guidance on writing tools for agents suggests: [5]

- **Few, well-scoped tools.** A few tools that each do one distinct job beat overlapping tools or a wrapper per endpoint. Merge steps that always occur together (one schedule tool rather than separate list and create tools).
- **Clear names and namespacing.** Name tools for the task and group related ones under a shared prefix (for example `policy_search`, `policy_get_source`).
- **Descriptions written for a newcomer.** Say what the tool does, when to use it and when not, and what each parameter means, with format and an example. Use unambiguous parameter names (`user_id`, not `user`).
- **Poka-yoke arguments.** Shape arguments so mistakes are hard to make, for example by requiring one canonical form of a path or identifier. [6]
- **Meaningful, token-efficient results.** Return high-signal, readable fields (names and status, not raw internal IDs). Paginate, filter, and truncate with sensible defaults; where useful, offer concise and detailed modes and tell the model how to narrow a broad result.
- **Actionable errors.** Say what went wrong and what valid input looks like, not only a code or stack trace, without protected content and mapped to the structured outcomes below.

Measure tool design on representative tasks, reading transcripts for wrong-tool choices and malformed arguments and confirming gains on held-out tasks. [5] For a large catalogue, loading every definition up front bloats context and causes mis-selection; expose tools progressively (for example by search) and keep bulky intermediate data out of the model's context. [7] None of this replaces validation and authorization.

If the agent can write and run code or use a shell or browser, run that code in a sandbox with resource limits, scoped network egress, and monitoring. [7]

### Bind authority at the protected operation

Authorization decides whether the protected operation may access this object, function, tenant, data category, or destination now. OWASP describes object-level authorization as checking that a user may take the requested action on the requested object, and recommends testing it. [3] Its Authorization Cheat Sheet recommends deny-by-default and checking the object or function on every request. [4]

Apply these at the adapter or resource boundary using trusted identity, normalized target, requested action, and effective scope, and revalidate before a write when target or authority may have changed. A prompt, model message, client-side check, retrieved document, tool description, or earlier approval never decides authorization ([3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)). Keep the tool set minimal; each extra tool widens what a manipulated model could do. [8]

### Make failure and cancellation useful to a caller

Separate invalid input, authorization denial, a domain result such as no match, transient unavailability, timeout, and malformed result. A generic error pushes the model to invent an answer or retry an unsafe call; a bounded outcome lets the contract choose `needs_information`, `declined`, `failed`, or another declared outcome.

Set a deadline through the trusted execution path. A deadline or cancellation describes the caller's wait: it can stop a proposal before dispatch, race with dispatch, or arrive after the target did the work. If you cannot tell which, record the uncertainty rather than claiming the work stopped.

### Minimize data and keep privacy-safe attribution

Return only what the task needs, marked as data and limited before the model sees it; pass no secrets, live clients, credentials, diagnostic payloads, or unbounded raw responses. Classification, destinations, capture, retention, and deletion are decided under [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

Attribution (TOOL-07) need not invent a workflow ID for an ephemeral path or an approval ID for a read-only path, and does not prove the target's effect; where an effect is in scope, record target-side evidence.

### Build the contract before admitting the capability

The [tool-contract template](../../templates/2.4/tool-contract.yaml) records, in order: the task decision and the one operation it needs, including what it must not expose or do; caller inputs versus trusted context and pre-I/O checks; bounded outputs mapped to terminal outcomes; actual effect and execution floor; retry safety, deadline, cancellation, and the response-loss path; and the test cases below plus the target-side observation that would establish an effect.

## Requirements

- **TOOL-01** When an agent enables an external interface, its owner MUST define a typed, serializable input and output contract, validate inputs before external I/O, and validate and bound results before returning them to the agent.
- **TOOL-02** When an interface can access or change external data, its contract MUST declare its actual effect and required execution-class floor; an agent MUST NOT enable it if the effective execution class is below that floor.
- **TOOL-03** When an interface accesses a protected resource or performs an action, its execution path MUST apply the trusted-identity and deterministic-authorization controls required by [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) to the requested operation and object before access or effect; model-supplied identity, permission, or approval claims MUST NOT grant authority.
- **TOOL-04** When an interface can time out or fail, its contract MUST define bounded timeouts and distinguish validation, authorization, business, transient, timeout, and malformed-result outcomes sufficiently for the runtime to apply its declared failure policy.
- **TOOL-05** When an interface can be invoked more than once, its contract MUST declare retry safety as `safe`, `idempotency_key_required`, or `unsafe`; the runtime MUST NOT automatically repeat an unsafe operation, and an idempotency-key-required operation MUST reuse a stable key only for the same intent.
- **TOOL-06** When a tool returns external or sensitive data to an agent, it MUST return only the bounded fields needed for the task, MUST NOT expose secrets or unbounded raw responses, and MUST handle returned content under [3.2’s untrusted-input controls](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).
- **TOOL-07** When a tool is invoked, its execution path MUST retain privacy-safe attribution sufficient to associate the invocation with the agent, run, tool, outcome, latency, and attempt, and cost when relevant and available; workflow or approval identifiers MUST be present only when those concepts apply.

## Worked example

The shared fictional candidate is `POLICY-BUILD-001` (`use_case_id: internal-policy-assistance`). It prefers a fixed retrieval-and-answer workflow; a bounded adaptive alternative could choose among a finite allowlist of the same operations. Either way it is read-only, with no write or approval capability.

### Proposed read-only policy search

The candidate proposes `search-approved-policy`. The runtime gets `employee-uk-104` and scope from its trusted request boundary; the model supplies only `query`. The adapter checks the query is non-empty, normalizes an optional permitted selector, and authorizes source access before searching.

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

Expected treatments:

- **Permitted:** the result identifies `travel-policy-2026@2026-10-01` as current and returns only the excerpt supporting the London hotel amount of GBP 220. `travel-policy-2024-superseded@2024-01-01` may appear marked superseded, never as current authority. The answer workflow, not tool status, decides whether the evidence supports `complete`.
- **Denied:** `contractor-uk-204` gets `denied` with no source text, and the agent returns `declined`.
- **Missing or conflicting:** `needs_information`; the tool neither picks a convenient value nor treats an absent result as proof no policy exists.
- **Timeout:** the adapter cannot tell whether the target saw the request. `safe_pending_target_semantics_review` means the builder must show that repeating the lookup has no additional relevant effect before repeating automatically; otherwise stop and return the declared failure.

Changing policy content would be a new candidate with its own effect, execution class, authorization, retry, unknown-outcome, and approval decisions, not a new field here.

## Evidence and checklist

Connect the contract to observable behavior; a schema, description, fixture, or model statement proves no control works. For the read-only example:

- **Contract review:** every field above, plus the owner (or an unresolved owner field).
- **Boundary cases:** validation failure before I/O; an allowed path; a denied path without leakage; an unadmitted capability that is not invoked.
- **Result cases:** a bounded result; an oversized or malformed result mapped to `invalid_result`; a missing permitted source; an equal-authority conflict not resolved by date or model preference.
- **Failure and retry cases:** timeout, cancellation ambiguity, transient failure, and repeats. If an external effect is in scope, inspect target state, not just a transcript or local status.
- **Attribution** without secrets or extra payload.

Case design is in [Part 4](../04-testing-and-evaluation/README.md).

## References

[1]: https://json-schema.org/specification "JSON Schema Specification"
[2]: https://httpwg.org/specs/rfc9110.html "RFC 9110 HTTP Semantics"
[3]: https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/ "OWASP API1:2023 Broken Object Level Authorization"
[4]: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html "OWASP Authorization Cheat Sheet"
[5]: https://www.anthropic.com/engineering/writing-tools-for-agents "Writing effective tools for agents — with agents"
[6]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"
[7]: https://www.anthropic.com/engineering/code-execution-with-mcp "Code execution with MCP: building more efficient agents"
[8]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"

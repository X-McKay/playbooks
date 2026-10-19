# 2.7 MCP and Standardized Integrations

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent designers, builders, integration owners, security reviewers, and evaluators

**Applicability:** Apply this chapter when an agent uses the Model Context Protocol (MCP) to reach an external capability or source. MCP is optional: an agent without it does not need a server or protocol layer to follow this chapter.

**Reader question:** When does MCP improve a bounded integration, what does the protocol standardize, and how does a host admit and evidence only the capabilities the task needs?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) · [2.5 Skills and Reusable Capabilities](05-skills-and-reusable-capabilities.md) · [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md) · Next: [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)

## Purpose and applicability

MCP is an open protocol for exchanging context and capabilities between an AI application and an external system. It standardizes an integration boundary. It does not define the agent's goal, choose authoritative evidence, decide whether a tool call is appropriate, or grant permission. The host application still owns the agent contract, the effective capability manifest, enforcement, and the user-visible outcome. [1]

Use MCP when a common protocol boundary, reusable discovery, or several compatible hosts justify the extra surface. A narrow direct adapter can fit better when one application needs one stable operation. Neither is inherently safer; compare the task, reuse, ownership, trust boundary, failure modes, and evidence burden. MCP does not replace a skill package ([2.5](05-skills-and-reusable-capabilities.md)), retrieval design ([2.6](06-context-and-retrieval-fundamentals.md)), or agent-to-agent delegation (Part 9).

This chapter stays at design level and prescribes no transport, deployment, or product setup. When MCP carries a protected resource or action, [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) owns identity and authorization, [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) owns untrusted content and action boundaries, and [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) owns data handling and audit.

## Working model

### What MCP standardizes, and what it does not

An MCP **host** is the AI application. It creates an MCP **client** for each MCP **server**; the client holds the connection and the server exposes context or capabilities. These are protocol roles, not accountability: the host decides whether an agent receives a capability and how its result is used. [1]

Servers expose three primitives:

- A **tool** is a callable operation. Its effect may be a read, a change, or something that needs further checking.
- A **resource** is data offered for context. It can be stale, incomplete, sensitive, or contain hostile text.
- A **prompt** is a reusable interaction template. It can guide a model but cannot grant authority or override host policy.

A primitive label is not a trust level: a resource is not automatically authoritative, a tool name is not an effect classification, and a prompt is not access control. [2.4](04-tools-and-external-interfaces.md) and [2.6](06-context-and-retrieval-fundamentals.md) still apply.

### Version, lifecycle, and transport

MCP 2026-07-28 is the current specification revision; 2025-11-25 is the previous, final one. [3] They differ in ways that matter:

- **Lifecycle.** 2025-11-25 runs an initialization exchange that negotiates version and optional capabilities. [2] 2026-07-28 removes it: every request carries its protocol version and client capabilities. It also removes protocol-level sessions, so list endpoints no longer vary per connection; servers needing state use explicit server-issued handles passed as tool arguments. [3]
- **Discovery.** Servers MUST implement `server/discover`, which reports supported versions, capabilities, and identity. Clients MAY call it first to pick a version, or use it as a probe for older servers on stdio. [3] [4]
- **Server-initiated requests.** Instead of sending `roots/list`, `sampling/createMessage`, or `elicitation/create`, a server returns an input-required result and the client retries the original request with the answers (the multi round-trip pattern). [3]
- **Lost streams.** SSE resumability is removed. A broken response stream loses the in-flight request, and the client MUST re-issue it with a new request ID. [3] The first attempt may have taken effect, so treat it as an unknown outcome and follow the retry rules in [2.4](04-tools-and-external-interfaces.md).
- **Caching.** Results of `tools/list` and similar calls carry `ttlMs` and `cacheScope`, and servers SHOULD return tools in a deterministic order, which helps client and prompt caching. [3] A cached list can be stale, so honor the hint and re-check against your admitted manifest.

Record the protocol version and features you need; do not assume a feature exists in another version. Claims below that come from 2025-11-25 are labelled.

A transport carries messages; it does not decide their meaning, authority, or truth. A local server can reach the host device; a remote server adds a network and operator boundary. Neither placement shows a server is safe. [1]

Keep protocol compatibility apart from admission. A successful negotiation means the parties can exchange messages, not that every advertised tool is usable by this agent, that the requester may see a resource, or that the task succeeded. The 2025-11-25 lifecycle calls for timeouts; a timeout is an unknown or failed exchange, not proof the operation did not happen. [2]

### Discovery, identity, and explicit admission

Discovery is an inventory, not a grant. `server/discover` reports versions, capabilities, and `serverInfo`; a tool listing can change and may vary with the authorization presented on a request (but not per connection). [4] [7]

`serverInfo` is self-reported: the protocol does not verify it, it is meant for display, logging, and debugging, and clients SHOULD NOT rely on it for security decisions. [4] The tools specification says clients MUST treat tool annotations as untrusted unless they come from a trusted server. [7] It does not say this of descriptions, but treat them the same way, because a description is text from the server's author that your model reads. Names, descriptions, annotations, and effect labels are hints, not proof of identity, harmlessness, or permission.

**Admission** is the host's explicit decision to make one identified capability available to one agent version for one declared purpose. A useful admission record states:

- the server and operator identity, and the separate basis for trusting the connection;
- the protocol version and any optional feature required;
- each tool, resource, or prompt considered, its task role, and its claimed or observed effect;
- the trusted workload, requester, and resource context, and where protected operations are enforced; and
- the blocked capabilities and what happens if a listing later changes.

A manifest that admits one document-read capability does not widen because the server later lists an edit tool or new prompt. A change to server identity, primitive contract, declared effect, protocol version, scope model, or capability set sends the record back to admission review.

### Authority is not conveyed by the connection

Authentication identifies a connection or workload. Authorization decides whether that identity may perform an operation on a resource in the current scope. It belongs at the protected-operation boundary, using trusted context, not a model-selected tenant, scope, or resource ID, or a server's instruction. Even a read-only integration can disclose protected content. See [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

Where MCP uses OAuth, the authorization specification requires a server to validate that an access token was issued for that server and forbids passing it through to downstream services (stated in 2025-11-25; 2026-07-28 keeps both rules). [5] [11] A credential presented to an MCP server is not a delegation to every downstream destination. Record the intended audience and scope, and keep an upstream credential, a server's own downstream credential, and a model-visible value distinct. OAuth is optional in the specification and not needed for every integration. In 2026-07-28, clients MUST validate a present `iss` value against the recorded authorization server and key stored client credentials by issuer, and Client ID Metadata Documents replace the deprecated Dynamic Client Registration. [3]

The MCP security best-practices page covers attacks that apply to your design: the confused deputy (a server acting with its own broad authority for a caller who lacks it), token passthrough, request forgery through OAuth discovery URLs, hijacked session or state handles, unsafe local servers started by one-click configuration, and over-broad scopes. [9] Request the smallest scope, show the user exactly what a local server will run before starting it, and sandbox local servers with minimal privileges.

Roots are informational: the specification calls a root guidance about files or directories the client considers relevant and says the protocol does not enforce it as access control. A root is not a filesystem sandbox or source allowlist. Roots are also deprecated in 2026-07-28 (below). [6]

### Optional client features remain host-policy choices

Enable an optional client feature only when the protocol version supports it and the task needs it. Host policy stays in force even when a server asks for more interaction.

For example, elicitation lets a server ask the user for information through the client. In 2025-11-25 the interaction goes through the client, which must identify the requesting server and let the user review, decline, or cancel; form requests must not ask for passwords, API keys, tokens, or payment credentials (use URL mode). [8] In 2026-07-28 the request arrives through the multi round-trip pattern, and the completion notification and `elicitationId` are removed; elicitation itself is not deprecated. [3] A server request does not make a data collection approved, and a user's answer does not authorize a different operation.

The 2026-07-28 changelog deprecates Roots, Sampling, and Logging, the HTTP+SSE transport (use Streamable HTTP), and Dynamic Client Registration. Deprecated features keep working for at least twelve months, but new implementations should not adopt them. For logging, use stderr on stdio or OpenTelemetry; the revision also documents trace-context keys in request metadata. [3] Name the exact version and feature rather than assuming older material still applies.

## Decisions and best practices

### Choose the narrowest integration shape that fits

Start from the task operation: what the agent needs, which callers may use it, the result the next decision requires, and what is out of scope. Then compare a **direct adapter** (easier to review when the operation is narrow, the contract stable, and one application owns it) with an **MCP boundary** (useful when a well-defined capability should be discovered and reused across compatible hosts, with a clear owner for its interface, identity, and change behavior). Either has a cost: an adapter still needs a typed contract and authorization checks, and MCP adds lifecycle, capability, and change management. "Standardized" does not by itself give portability, correctness, or security.

### Make the boundary reviewable before exposing it

Sketch the route in plain words: host, client-to-server boundary, server, protected source or effect. At each step note what data could cross, which identity is asserted, who operates the next component, and what enforces authorization. Do not collapse several identities into "the MCP credential": the workload, requester, resource or tenant, server, and user-interaction contexts can all differ. A server may authenticate the host while the protected resource still needs a requester-scoped decision.

### Admit primitives individually and preserve negative space

Turn discovery into a small allowlist. For each primitive, say why the task needs it, its inputs and bounded outputs, expected effect, policy boundary, and how a denial, malformed result, or timeout becomes a declared agent outcome. Offered write tools, broad search, unrelated prompts, roots, sampling, and elicitation stay unavailable unless a separate decision admits them.

A schema gives shape, not permission, currentness, or truth. Validate the model's arguments before the call, validate and bound the result before reuse, and treat returned text and errors as data. The tools specification calls for input validation, access controls, sanitized outputs, result validation, and timeouts (servers MUST validate inputs and apply access controls; clients SHOULD validate results and apply timeouts), and says a human should be able to deny tool calls. [7] These complement [2.4](04-tools-and-external-interfaces.md).

Guard against **tool poisoning** (a description hides instructions your model follows), the **rug pull** (a server changes a description or behavior after approval), and **tool shadowing** (one server's description steers how the model uses another server's tools). [10] At admission, store a hash of each tool's name, description, and schema. Compare on every listing, and block the tool until reviewed if the hash changes. Show users the full description and arguments, not a summary. A different primitive set or contract change is never a reason to expand dynamically: keep the prior scope, and review before admitting the change.

### Common failure modes

- **Version or feature mismatch.** The counterpart lacks the version or feature you assumed. Return the declared bounded outcome or use a reviewed path; never treat it as a successful no-op.
- **Misleading discovery.** Identity, instructions, descriptions, and annotations can be stale or deceptive. Do not use them to widen authority or certify trust.
- **Scope and audience confusion.** A token valid for one resource is not valid for an MCP server or downstream service. Avoid passthrough and enforce the protected operation's scope.
- **Confused deputy.** A server acts with broad authority for a caller who lacks it. Bind each call to the requester's scope. [9]
- **Local-trust assumption.** A local process is still code, and remote placement is not a reason to trust a service either.
- **Root-as-sandbox mistake.** A root states intended scope but cannot contain an untrusted server. Enforce limits at the access layer.
- **Content or result injection.** Resource text, prompts, tool output, and errors can carry instructions. Keep provenance and keep authorization outside the model ([3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)).
- **Timeout or ambiguous effect.** No response does not show an action did not occur. Use the retry treatment in [2.4](04-tools-and-external-interfaces.md) and, where triggered, Part 7.

### Builder workflow for an integration

1. **Frame the task.** Record the bounded operation and why MCP is considered instead of a direct adapter.
2. **Record the connection boundary.** Name the roles, local or remote placement, operator, information flow, identity questions, protocol version, and transport category. Mark unknowns as unresolved.
3. **Separate required from optional features.** Link each feature to the task, and flag version-sensitive, deprecated, or unneeded ones (roots, elicitation, sampling).
4. **Write a per-capability admission record.** For each primitive: purpose, input and output contract, claimed effect, authorization boundary, failure outcome, description hash, blocked alternatives. Update the capability manifest only through [2.2](02-agent-contracts-and-configuration.md).
5. **Connect to the control owners.** [2.4](04-tools-and-external-interfaces.md) for interface and effects, [2.6](06-context-and-retrieval-fundamentals.md) for evidence, Part 3 for identity, untrusted content, and data handling.
6. **Define evidence and change triggers.** Separate discovery, admission, authorization, attempted call, returned result, and authoritative effect, and name which changes send the record back to review.

The [MCP integration record](../../templates/2.7/mcp-integration-record.yaml) is a planning template filled with fictional values and unresolved fields.

## Requirements

- **MCP-01** When an agent uses MCP, its design record MUST state why MCP is used rather than a direct call or API adapter, and identify the host, client-to-server boundary, server operator, and local or remote execution context.
- **MCP-02** When a server advertises capabilities, the host MUST explicitly admit each capability the agent may use and MUST block unadmitted capabilities; discovery or model output MUST NOT itself grant authority.
- **MCP-03** When an MCP connection carries protected data or exposes an action, the system MUST authenticate the relevant connection identity, enforce authorization at the applicable execution boundary, and constrain access to the agent’s approved scope. A successful connection MUST NOT be treated as authorization for all server capabilities.
- **MCP-04** For each admitted MCP capability, the system MUST validate inputs and returned structure against its expected contract, apply bounded timeouts and defined failure handling, and treat returned content as untrusted. When an operation can cause an external effect, its retry behavior MUST follow the applicable effect and recovery policy in [2.4](04-tools-and-external-interfaces.md) and [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).
- **MCP-05** When MCP is in the execution path, the team MUST test the underlying task outcome, permission boundaries, malformed or untrusted results, timeout or denial behavior, and any relevant effects. Evidence MUST correlate the agent run to the server and admitted capability without requiring secrets or raw hidden reasoning.

## Worked example: approved travel-policy documents

This example is fictional and unexecuted. The candidate `POLICY-BUILD-001` (`internal-policy-assistance`) uses a fixed retrieval-and-answer workflow that can branch to a declared bounded outcome. No model-selected write or approval capability is enabled. It answers from current, approved, requester-permitted sources and returns citations and uncertainty.

The task is an employee's London hotel-limit question. In the fixture, `employee-uk-104` may read `travel-policy-2026@2026-10-01`, a current approved policy that says GBP 220. `travel-policy-2024-superseded@2024-01-01` is an approved historical record, not current, and says GBP 200. `contractor-uk-204` may read neither.

The planning record compares a direct document-search adapter with a possible remote MCP boundary. MCP is considered because compatible hosts could reuse one read-only policy interface; the server operator, connection identity, and change behavior are open. If the adapter met the need with less burden, the record would keep it.

A future discovery response might advertise a policy resource, a document-search tool, a reusable prompt, and an unrelated policy-editing tool. All are unobserved until assessed. The record proposes admitting only the read-only policy-search tool, with a hash of its description and schema, and keeps the edit tool, the prompt, roots, elicitation, and sampling out. A description calling the edit tool "safe" changes nothing.

Before a read reaches the policy source, the protected retrieval boundary receives trusted requester and resource scope, not a tenant or source ID supplied by the model. The response contract holds source identity, revision, currentness, a bounded excerpt, and a result status. The host validates the search arguments and the returned shape, then passes the text to the model as untrusted evidence. Neither the connection, a matching schema, nor a citation shows that GBP 220 is current or accessible; the source-state and permission checks do.

Expected behavior by case:

- `employee-uk-104`, current permitted source present: `complete`, citing GBP 220.
- Current permitted source absent: `needs_information`, not an answer from the superseded source.
- Two equally authoritative current sources conflict: identify the conflict and seek clarification or escalation, not the later date.
- `contractor-uk-204`: the retrieval boundary declines without disclosing the amount.
- Server timeout or malformed result: `failed` or `needs_information`, never a claimed verified answer.

A review plan ties each case to the candidate version, protocol version, server boundary, capability ID, fixture revision, authorization decision, attempted exchange, result status, and answer assessment. A later update action, or a material change in server identity, scope, primitive contract, or protocol version, is a new admission question.

## Evidence and checklist

A reviewer should be able to inspect, without secrets or raw hidden reasoning:

- the MCP versus direct-adapter comparison and why the extra boundary is proportionate;
- the host, client-to-server boundary, server and operator identity basis, placement, protocol version, transport category, and data flow;
- the primitive inventory, narrow admissions, blocked surface, stored description hashes, and re-admission triggers;
- the trusted identity and scope inputs, where authorization is enforced, and the difference between token audience, server identity, and downstream authority;
- the contract for each admitted capability: validation, returned-content handling, timeout and failure outcomes, and retry treatment for any action;
- a case plan covering the answer, currentness, requester permission, hostile or malformed results, timeout or denial, and the gap between a proposed call, a dispatched attempt, and an authoritative effect; and
- a privacy-aware way to link a run to the admitted capability and server.

A discovery transcript, allowlist, or successful exchange is evidence to inspect, not proof of safety or release readiness. Part 4 owns decision-grade evaluation.

## References

[1]: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture "MCP Architecture Overview"
[2]: https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle "MCP Specification 2025-11-25: Lifecycle"
[3]: https://modelcontextprotocol.io/specification/2026-07-28/changelog "MCP Specification 2026-07-28: Key Changes"
[4]: https://modelcontextprotocol.io/specification/2026-07-28/server/discover "MCP Specification 2026-07-28: Server Discovery"
[5]: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization "MCP Specification 2025-11-25: Authorization"
[6]: https://modelcontextprotocol.io/specification/2026-07-28/client/roots "MCP Specification 2026-07-28: Roots"
[7]: https://modelcontextprotocol.io/specification/2026-07-28/server/tools "MCP Specification 2026-07-28: Tools"
[8]: https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation "MCP Specification 2025-11-25: Elicitation"
[9]: https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices "MCP Specification 2026-07-28: Security Best Practices"
[10]: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks "Invariant Labs: MCP Security Notification, Tool Poisoning Attacks"
[11]: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization "MCP Specification 2026-07-28: Authorization"

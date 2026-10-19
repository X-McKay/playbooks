# 2.7 MCP and Standardized Integrations

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent designers, builders, integration owners, security reviewers, and evaluators

**Applicability:** Apply this chapter when an agent uses the Model Context Protocol (MCP) to reach an external capability or source. MCP is optional: an agent without it does not need a server or protocol layer to follow this chapter.

**Reader question:** When does MCP improve a bounded integration, what does the protocol standardize, and how does a host admit and evidence only the capabilities the task needs?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) · [2.5 Skills and Reusable Capabilities](05-skills-and-reusable-capabilities.md) · [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md) · Next: [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)

## Purpose and applicability

MCP is an open protocol for exchanging context and capabilities between an AI application and an external system. It standardizes an integration boundary but does not define the agent's goal, choose authoritative evidence, decide whether a tool call is appropriate, or grant permission. The host application still owns the agent contract, effective capability manifest, enforcement, and user-visible outcome. [1]

Use MCP when a common protocol boundary, reusable discovery, or several compatible hosts justify the extra surface (see the choice below); neither it nor a direct adapter is inherently safer. MCP does not replace a skill package ([2.5](05-skills-and-reusable-capabilities.md)), retrieval design ([2.6](06-context-and-retrieval-fundamentals.md)), or agent-to-agent delegation (Part 9).

For protected resources or actions, [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) owns identity and authorization, [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) untrusted content and action boundaries, and [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) data handling and audit.

## Working model

### What MCP standardizes, and what it does not

An MCP **host** (the AI application) creates a **client** per **server**; the client holds the connection and the server exposes context or capabilities. These are protocol roles, not accountability: the host decides what an agent receives and how results are used. [1]

Servers expose three primitives:

- A **tool** is a callable operation whose effect may be a read, a change, or something needing further checking.
- A **resource** is data offered for context; it can be stale, incomplete, sensitive, or hostile.
- A **prompt** is a reusable interaction template that guides a model but cannot grant authority or override host policy.

A primitive label is not a trust level; [2.4](04-tools-and-external-interfaces.md) and [2.6](06-context-and-retrieval-fundamentals.md) still apply.

### Version, lifecycle, and transport

MCP 2026-07-28 is the current specification revision; 2025-11-25 is the previous, final one. [3] Differences that matter:

- **Lifecycle.** 2025-11-25 runs an initialization exchange that negotiates version and optional capabilities. [2] 2026-07-28 removes it: every request carries its protocol version and client capabilities. It also removes protocol-level sessions, so list endpoints no longer vary per connection; servers needing state use explicit server-issued handles passed as tool arguments. [3]
- **Discovery.** Servers MUST implement `server/discover`, which reports supported versions, capabilities, and identity. Clients MAY call it first to pick a version, or use it as a probe for older servers on stdio. [3] [4]
- **Server-initiated requests.** Instead of sending `roots/list`, `sampling/createMessage`, or `elicitation/create`, a server returns an input-required result and the client retries the original request with the answers (the multi round-trip pattern). [3]
- **Lost streams.** SSE resumability is removed. A broken response stream loses the in-flight request, and the client MUST re-issue it with a new request ID. [3] The first attempt may have taken effect, so treat it as an unknown outcome under the retry rules in [2.4](04-tools-and-external-interfaces.md).
- **Caching.** Results of `tools/list` and similar calls carry `ttlMs` and `cacheScope`, and servers SHOULD return tools in a deterministic order, which helps client and prompt caching. [3] Honor the hint and re-check a cached list against your admitted manifest.

Record the version and features you need; claims below from 2025-11-25 are labelled.

A transport carries messages, not meaning, authority, or truth. A local server can reach the host device and a remote one adds a network and operator boundary; neither placement shows a server is safe. [1] Successful negotiation means the parties can exchange messages, not that an advertised tool is admitted, a resource visible to the requester, or the task done. The 2025-11-25 lifecycle calls for timeouts; a timeout is an unknown or failed exchange, not proof the operation did not happen. [2]

### Discovery, identity, and explicit admission

Discovery is an inventory, not a grant. `server/discover` reports versions, capabilities, and `serverInfo`; a tool listing can change and may vary with the authorization presented on a request (but not per connection). [4] [7]

`serverInfo` is self-reported and unverified, meant for display, logging, and debugging, and clients SHOULD NOT rely on it for security decisions. [4] Clients MUST treat tool annotations as untrusted unless they come from a trusted server. [7] Treat descriptions the same way, although the specification does not say so, since your model reads them; no name, description, annotation, or effect label proves identity, harmlessness, or permission.

**Admission** is the host's explicit decision to make one identified capability available to one agent version for one declared purpose. An admission record states:

- server and operator identity, and the separate basis for trusting the connection;
- protocol version and any required optional feature;
- each tool, resource, or prompt considered, its task role, and its claimed or observed effect;
- the trusted workload, requester, and resource context, and where protected operations are enforced; and
- blocked capabilities and what happens if a listing later changes.

The manifest does not widen when the server later lists an edit tool or new prompt; a change to server identity, primitive contract, declared effect, protocol version, scope model, or capability set returns the record to admission review.

### Authority is not conveyed by the connection

Authorization belongs at the protected-operation boundary, using trusted context rather than a model-selected tenant, scope, or resource ID or a server's instruction. Even a read can disclose protected content ([3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)).

Where MCP uses OAuth, a server must validate that an access token was issued for it and must not pass it through to downstream services (stated in 2025-11-25; 2026-07-28 keeps both rules). [5] [11] Such a credential is not delegation downstream: record its audience and scope, and keep an upstream credential, the server's own downstream credential, and model-visible values distinct. OAuth is optional and not needed for every integration. In 2026-07-28, clients MUST validate a present `iss` value against the recorded authorization server and key stored client credentials by issuer, and Client ID Metadata Documents replace the deprecated Dynamic Client Registration. [3]

MCP's security best practices cover the confused deputy (a server acting with its own broad authority for a caller who lacks it), token passthrough, request forgery through OAuth discovery URLs, hijacked session or state handles, unsafe local servers started by one-click configuration, and over-broad scopes. [9] Request the smallest scope, show the user exactly what a local server will run before starting it, and sandbox local servers with minimal privileges.

The specification calls a root guidance about files or directories the client considers relevant, not enforced access control, so a root is neither a filesystem sandbox nor a source allowlist. Roots are also deprecated in 2026-07-28. [6]

### Optional client features remain host-policy choices

Enable an optional client feature only when the version supports it and the task needs it; host policy stays in force when a server asks for more. Elicitation, for example, lets a server ask the user for information through the client. In 2025-11-25 the client must identify the requesting server and let the user review, decline, or cancel, and form requests must not ask for passwords, API keys, tokens, or payment credentials (use URL mode). [8] In 2026-07-28 the request arrives through the multi round-trip pattern, and the completion notification and `elicitationId` are removed; elicitation itself is not deprecated. [3] A server request does not approve a data collection, and a user's answer does not authorize a different operation.

The 2026-07-28 changelog deprecates Roots, Sampling, Logging, the HTTP+SSE transport (use Streamable HTTP), and Dynamic Client Registration. Deprecated features keep working for at least twelve months, but new implementations should not adopt them. For logging, use stderr on stdio or OpenTelemetry; the revision also documents trace-context keys in request metadata. [3]

## Decisions and best practices

### Choose the narrowest integration shape that fits

Start from the task operation and its callers, needed result, and exclusions. A **direct adapter** is easier to review when the operation is narrow, the contract stable, and one application owns it. An **MCP boundary** helps when a well-defined capability should be discovered and reused across compatible hosts, with a clear owner for its interface, identity, and change behavior. An adapter still needs a typed contract and authorization checks; MCP adds lifecycle, capability, and change management. "Standardized" alone gives no portability, correctness, or security.

### Make the boundary reviewable before exposing it

Sketch the route (host, client-to-server boundary, server, protected source or effect), noting at each step what data could cross, which identity is asserted, who operates the next component, and what enforces authorization. Do not collapse workload, requester, resource or tenant, server, and user-interaction identities into "the MCP credential"; a server may authenticate the host while the resource still needs a requester-scoped decision.

### Admit primitives individually and preserve negative space

Turn discovery into a small allowlist, stating for each primitive why the task needs it, its inputs and bounded outputs, expected effect, policy boundary, and how a denial, malformed result, or timeout becomes a declared agent outcome. Offered write tools, broad search, unrelated prompts, roots, sampling, and elicitation stay unavailable unless separately admitted.

Validate arguments before the call, validate and bound the result before reuse, and treat returned text and errors as data. The tools specification calls for input validation, access controls, sanitized outputs, result validation, and timeouts (servers MUST validate inputs and apply access controls; clients SHOULD validate results and apply timeouts), and says a human should be able to deny tool calls. [7]

Guard against **tool poisoning** (a description hides instructions your model follows), the **rug pull** (a server changes a description or behavior after approval), and **tool shadowing** (one server's description steers how the model uses another server's tools). [10] At admission, store a hash of each tool's name, description, and schema, compare it on every listing, and block the tool until reviewed if it changes. Show users the full description and arguments, not a summary. Never expand dynamically on a changed primitive set or contract; keep the prior scope until review.

### Common failure modes

- **Version or feature mismatch** treated as a successful no-op instead of a declared bounded outcome.
- **Misleading discovery** used to widen authority or certify trust.
- **Scope and audience confusion** or a **confused deputy**: bind each call to the requester's scope and the token's intended audience.
- **Local-trust assumption.** A local process is still code, and remote placement is no reason to trust a service either.
- **Root-as-sandbox mistake** or **content and result injection** from resource text, prompts, tool output, or errors; enforce limits at the access layer, outside the model.
- **Timeout or ambiguous effect.** No response does not show an action did not occur; use the [2.4](04-tools-and-external-interfaces.md) retry treatment and, where triggered, Part 7.

### Builder workflow for an integration

1. **Frame the task** and why MCP rather than a direct adapter.
2. **Record the connection boundary:** roles, placement, operator, information flow, identity questions, protocol version, and transport category, marking unknowns unresolved.
3. **Separate required from optional features,** flagging version-sensitive, deprecated, or unneeded ones (roots, elicitation, sampling).
4. **Write a per-capability admission record** including the description hash and blocked alternatives, updating the capability manifest only through [2.2](02-agent-contracts-and-configuration.md).
5. **Define evidence and change triggers:** separate discovery, admission, authorization, attempted call, returned result, and authoritative effect, and name which changes send the record back to review.

The [MCP integration record](../../templates/2.7/mcp-integration-record.yaml) is a planning template with fictional values and unresolved fields.

## Requirements

- **MCP-01** When an agent uses MCP, its design record MUST state why MCP is used rather than a direct call or API adapter, and identify the host, client-to-server boundary, server operator, and local or remote execution context.
- **MCP-02** When a server advertises capabilities, the host MUST explicitly admit each capability the agent may use and MUST block unadmitted capabilities; discovery or model output MUST NOT itself grant authority.
- **MCP-03** When an MCP connection carries protected data or exposes an action, the system MUST authenticate the relevant connection identity, enforce authorization at the applicable execution boundary, and constrain access to the agent’s approved scope. A successful connection MUST NOT be treated as authorization for all server capabilities.
- **MCP-04** For each admitted MCP capability, the system MUST validate inputs and returned structure against its expected contract, apply bounded timeouts and defined failure handling, and treat returned content as untrusted. When an operation can cause an external effect, its retry behavior MUST follow the applicable effect and recovery policy in [2.4](04-tools-and-external-interfaces.md) and [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).
- **MCP-05** When MCP is in the execution path, the team MUST test the underlying task outcome, permission boundaries, malformed or untrusted results, timeout or denial behavior, and any relevant effects. Evidence MUST correlate the agent run to the server and admitted capability without requiring secrets or raw hidden reasoning.

## Worked example: approved travel-policy documents

This example is fictional. `POLICY-BUILD-001` (`internal-policy-assistance`) uses a fixed retrieval-and-answer workflow that can branch to a declared bounded outcome, with no model-selected write or approval capability. In the fixture, `employee-uk-104` may read `travel-policy-2026@2026-10-01`, the current approved policy giving the London hotel limit as GBP 220; `travel-policy-2024-superseded@2024-01-01` is an approved historical record giving GBP 200; `contractor-uk-204` may read neither.

The planning record weighs a direct document-search adapter against a remote MCP boundary that compatible hosts could reuse, keeping the adapter if it meets the need with less burden; server operator, connection identity, and change behavior are open.

If discovery advertises a policy resource, a document-search tool, a reusable prompt, and an unrelated policy-editing tool, the record admits only the read-only policy-search tool, with a hash of its description and schema, and keeps the edit tool, prompt, roots, elicitation, and sampling out. A description calling the edit tool "safe" changes nothing.

The protected retrieval boundary receives trusted requester and resource scope, not a model-supplied tenant or source ID. The host validates arguments and the returned shape (source identity, revision, currentness, bounded excerpt, status) and passes the text to the model as untrusted evidence. Only source-state and permission checks, not the connection, schema match, or citation, show that GBP 220 is current and accessible.

- `employee-uk-104`, current permitted source present: `complete`, citing GBP 220.
- Current permitted source absent: `needs_information`, not an answer from the superseded source.
- Two equally authoritative current sources conflict: identify the conflict and seek clarification or escalation, not the later date.
- `contractor-uk-204`: the retrieval boundary declines without disclosing the amount.
- Server timeout or malformed result: `failed` or `needs_information`, never a claimed verified answer.

Each case ties to candidate, protocol, server, capability, fixture, authorization decision, attempted exchange, result status, and answer assessment. An update action, or a material change in server identity, scope, primitive contract, or protocol version, is a new admission question.

## Evidence and checklist

Keep, without secrets or raw hidden reasoning:

- the builder-workflow records above (adapter comparison, connection boundary, admissions, blocked surface, hashes, re-admission triggers);
- trusted identity and scope inputs, the authorization point, and the difference between token audience, server identity, and downstream authority;
- each admitted capability's contract: validation, returned-content handling, timeout and failure outcomes, and retry treatment for any action;
- a case plan covering the answer, currentness, permission, hostile or malformed results, timeout or denial, and the gap between proposed call, dispatched attempt, and authoritative effect; and
- a privacy-aware link from a run to the admitted capability and server.

A discovery transcript, allowlist, or successful exchange is not proof of safety; Part 4 owns evaluation.

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

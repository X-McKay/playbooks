# 2.7 MCP and Standardized Integrations

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Agent designers, builders, integration owners, security reviewers, and evaluators

**Applicability:** Apply this chapter when a proposed agent uses the Model Context Protocol (MCP) to reach an external capability or source. MCP remains optional: an agent without MCP does not need to add a server or protocol layer merely to follow this chapter.

**Reader question:** When does MCP improve a bounded integration, what does the protocol standardize, and how can a host admit and evidence only the capabilities the task actually needs?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) · [2.5 Skills and Reusable Capabilities](05-skills-and-reusable-capabilities.md) · [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md) · Next: [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)

## Purpose and applicability

MCP is an open protocol for exchanging context and capabilities between an AI application and an external system. It standardizes an integration boundary; it does not define the agent's goal, choose authoritative evidence, decide whether a tool call is appropriate, or grant permission to act. The host application still owns the agent contract, the effective capability manifest, deterministic enforcement, and the user-visible outcome. [1]

Use MCP when a common protocol boundary, reusable capability discovery, or several compatible hosts makes that extra integration surface worthwhile. A narrow direct adapter can be a better fit when one application needs one stable operation and shared discovery is not useful. Neither choice is inherently safer or more maintainable: compare the actual task, reuse needs, ownership, trust boundary, failure modes, and evidence burden. MCP is not a replacement for a skill package, retrieval design, or agent-to-agent delegation. Those concepts answer different questions and are covered by [2.5](05-skills-and-reusable-capabilities.md), [2.6](06-context-and-retrieval-fundamentals.md), and Part 9 respectively.

This chapter stays at the integration-design level. It does not prescribe a transport, deployment shape, authorization-flow recipe, directory layout, or product setup. When MCP carries a protected resource or action, [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) owns trusted identity and deterministic authorization; [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) owns untrusted-content and action boundaries; [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) owns data handling and audit policy.

## Working model

### What MCP standardizes—and what it does not

An MCP **host** is the AI application that coordinates one or more connections. It creates an MCP **client** for a particular MCP **server**; the client maintains the protocol connection and the server exposes context or capabilities. A host may have several client-to-server connections. That role diagram describes protocol participants, not a transfer of accountability: the host remains the place to decide whether a proposed agent receives a capability and how its result is used. [1]

MCP servers can expose three central primitives:

- A **tool** is a callable operation. Its effect may be a read, a change, or something whose outcome needs further checking.
- A **resource** is data offered for context. It can be stale, incomplete, sensitive, or contain hostile text.
- A **prompt** is a reusable interaction template. It can guide a model but cannot grant authority or override the host's policy.

The primitive labels describe an exchange shape, not a trust level. A resource is not automatically authoritative, a tool name is not an effect classification, and a prompt is not an access-control mechanism. The narrower domain and effect contracts in [2.4](04-tools-and-external-interfaces.md), and the source/currentness decisions in [2.6](06-context-and-retrieval-fundamentals.md), still apply.

### Version, lifecycle, and transport

Protocol source versions matter. The official 2025-11-25 lifecycle describes an initialization exchange that negotiates protocol version and optional capabilities before normal operation. In contrast, the 2026-07-28 revision removes the connection-level initialization handshake, makes requests carry protocol and client-capability metadata, and introduces `server/discover` for up-front discovery. A planning record therefore identifies the intended protocol version and the features actually needed; it does not assume that a feature or lifecycle from one version exists in another. [2] [3]

A transport carries and frames protocol messages; it does not decide their meaning, the task's authority, or the truth of a returned claim. A local connection and a remote connection have different practical boundaries. A local server can interact with the host device and its accessible resources; a remote server adds a network and operator boundary. Neither placement is evidence that the server is safe, authorized, or appropriate for the task. [1]

The host should distinguish protocol compatibility from application admission. Successful negotiation means that the parties found a compatible way to exchange particular protocol messages. It does not mean that every advertised tool is usable by the proposed agent, that the requester may see a returned resource, or that the external task succeeded. The 2025-11-25 lifecycle also calls for timeout handling; a timeout is an unknown or failed exchange, not evidence that a requested operation did not occur. [2]

### Discovery, identity, and explicit admission

Discovery is an inventory mechanism. The 2026-07-28 `server/discover` response can report a server's supported versions, capabilities, and `serverInfo`, while a tool listing can change and may vary with the authorization presented on a request. This makes discovery useful evidence about an offered surface, but not a durable capability grant. [4] [7]

In particular, `serverInfo` is self-reported and the specification says it is not verified by the protocol or suitable for security decisions. Tool descriptions and annotations are also untrusted unless they come from a trusted server. Treat names, descriptions, annotations, natural-language instructions, and advertised effect labels as hints to assess rather than proof of identity, harmlessness, or permission. [4] [7]

**Admission** is the host's explicit decision to make one identified capability available to one agent version for one declared purpose. A useful admission record distinguishes:

- the proposed server/operator identity and the separate basis for trusting the connection;
- the protocol version and any negotiated or required optional feature;
- the individual tool, resource, or prompt being considered, its intended task role, and its observed or claimed effect;
- the trusted workload/requester/resource context and the enforcement point for protected operations; and
- the blocked capabilities and the consequence if a listing later changes.

This separation prevents a common error: treating a discovery response as an expanding menu for the model. A manifest that admits one document-read capability does not become broader because the server later lists an edit operation, new prompt, or additional resource. A changed server identity, primitive contract, declared effect, protocol version, scope model, or advertised capability set is a reason to revisit admission and supporting evidence rather than silently extending the agent.

### Authority is not conveyed by the connection

Authentication identifies a connection or workload. Authorization decides whether the current identity may perform a particular operation on a particular resource in the current scope. The latter belongs at the protected-operation boundary, using trusted context, not model-selected tenant, scope, resource identifier, or a server's natural-language instruction. A read-only integration can still disclose protected content or cross a tenant boundary. See [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

Where an MCP implementation uses OAuth, the versioned authorization specification requires a server to validate that an access token is intended for that server and rejects token passthrough to downstream services. This supports a broader design distinction: a credential presented to an MCP server is not a general delegation to every downstream destination. Record the intended audience and permitted resource/action scope where they apply, and keep an upstream credential, a server's own downstream credential, and a model-visible value distinct. OAuth is an example of a supported authorization mechanism, not a prerequisite for every MCP integration. [5]

Roots deserve similar care. The protocol describes roots as informational guidance about files or directories that the client considers relevant; it explicitly says that the protocol does not enforce them as access control. A root can help a well-behaved server focus its work, but it is not a filesystem sandbox, a source allowlist, or a substitute for actual access enforcement. [6]

### Optional client features remain host-policy choices

A server can offer more than tools, resources, and prompts, and a client can support optional features. Enable an optional feature only when it is both supported by the relevant protocol version and needed by the bounded task. The host's policy remains in force even when a server asks for more interaction.

For example, elicitation lets a server ask for additional user information through the client. The specification places user interaction through the client, requires the client to identify the requesting server, and provides review, decline, and cancel paths. That protocol feature does not make a server request an approved data collection, nor does it authorize a user response for a different operation. [8]

Sampling and roots are useful reminders that feature status changes over time. The 2026-07-28 changelog deprecates roots and sampling for new implementations and changes the protocol's request pattern. A design should name the exact version and optional feature instead of assuming that a capability advertised in older material is present, supported, or appropriate in a later integration. [3]

## Decisions and best practices

### Choose the narrowest integration shape that fits

Start from the task operation, not from an expectation that every service needs MCP. State what information or operation the agent needs, which callers may use it, the result required by the next decision, and what remains out of scope. Then compare a direct adapter and an MCP boundary:

- A **direct adapter** can be easier to review when the operation is narrow, its contract is stable, and one application owns the integration. It does not need protocol discovery to be reusable inside that application.
- An **MCP boundary** can be useful when a well-defined capability should be discoverable and reused across compatible hosts, and there is a clear owner for its interface, identity, and change behavior.
- Either choice has a cost: an adapter still needs a typed contract and authorization checks, while MCP adds lifecycle, capability, and change-management considerations. Neither removes the need for task-level evaluation.

The decision is local to the proposed use. “Standardized” does not by itself establish portability, operational ownership, correctness, or security.

### Make the boundary reviewable before exposing it

For an MCP candidate, sketch the route in ordinary language: proposed host → client-to-server boundary → server → protected source or effect. At each arrow, identify the data that could cross, the identity asserted, the party that operates the next component, and the boundary that enforces authorization. This sketch is not a deployment diagram or proof that those controls operate; it makes unresolved questions visible early.

Do not compress several identities into “the MCP credential.” The workload identity, authenticated requester, resource/tenant context, server identity, and any user-interaction context can differ. A server may authenticate the host while the protected resource also needs a requester-scoped decision. Conversely, a successful user interaction does not give the host a new workload capability. Preserve those distinctions in the contract and integration record.

### Admit primitives individually and preserve negative space

Translate discovery into a small proposed allowlist. For every candidate primitive, describe why the task needs it, what inputs and bounded outputs it uses, the expected effect, the policy boundary, and how a denial, malformed result, or timeout becomes a declared agent outcome. Then make the negative space visible: offered write tools, broad search, unrelated prompts, roots, sampling, or elicitation are unavailable unless a separate decision admits them.

A schema establishes the shape of a request or result, not that the request is permitted, the source is current, or the result is true. Validate the model's proposed arguments before the call, validate and bound the returned structure before reuse, and treat returned text and errors as data. The MCP tools specification similarly calls for input validation, access controls, sanitized outputs, client-side result validation, and timeouts; those practices complement rather than replace the tool contract in [2.4](04-tools-and-external-interfaces.md). [7]

If the server lists a different primitive set or a material contract change, avoid dynamic expansion. Compare the observed change with the admitted manifest. Keep the prior scope blocked until the appropriate owner has reviewed the change and created updated evidence. A response from an unadmitted or no-longer-compatible feature is not a harmless fallback.

### Plan for failures without inventing an outcome

MCP adds its own integration failure modes alongside ordinary tool failures:

- **Version or feature mismatch.** A counterpart may not support the version or optional feature the design assumed. Return the declared bounded outcome or use a separately reviewed compatible path; do not silently treat an unavailable feature as a successful no-op.
- **Misleading discovery.** Server-provided identity, instructions, descriptions, or annotations can be incomplete, stale, or deceptive. Do not use them to expand authority or certify trust.
- **Scope and audience confusion.** A token valid for one resource is not automatically valid for an MCP server or downstream service. Avoid token passthrough and enforce the actual protected operation's scope.
- **Local-trust assumption.** A local process is still code with a host boundary; remote placement is still not a reason to trust a service. Placement changes what to assess, not whether assessment is needed.
- **Root-as-sandbox mistake.** A root helps communicate intended scope but cannot contain an untrusted server. Actual access restrictions belong at their enforcement layers.
- **Content or result injection.** Resource text, prompt text, tool output, and error details can contain instructions that try to change the task. Preserve their provenance and keep authorization outside the model. [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md) owns that boundary.
- **Timeout or ambiguous effect.** A missing response does not establish that a read or action did not occur. Use the operation's declared retry and recovery treatment from [2.4](04-tools-and-external-interfaces.md) and, where triggered, Part 7.

### A builder workflow for a proposed integration

The following sequence produces a reviewable local unit; it is not a live admission, approval, or release process.

1. **Frame the task and compare integration shapes.** Record the bounded operation and the reason an MCP boundary is being considered instead of a direct adapter. State the known limits of that comparison.
2. **Record the proposed connection boundary.** Name the intended host/client/server roles, local or remote placement, operator, information flow, identity questions, protocol version, and transport category at a conceptual level. Mark unknowns as unresolved rather than assuming them away.
3. **Identify required versus optional protocol features.** Link each requested feature to the task. Note version-sensitive features and unsupported or unneeded features, including roots, elicitation, and sampling where relevant.
4. **Create a proposed per-capability admission record.** Map each candidate tool, resource, or prompt to an agent-purpose statement, input/output contract, claimed effect, authorization boundary, failure outcome, and blocked alternatives. Update the agent's capability manifest only through the applicable construction and review process in [2.2](02-agent-contracts-and-configuration.md).
5. **Connect the capability to the underlying control owners.** Use [2.4](04-tools-and-external-interfaces.md) for the interface and effects, [2.6](06-context-and-retrieval-fundamentals.md) for evidence status and retrieval, and Part 3 for identity, untrusted content, and data handling. Do not duplicate their requirements in the MCP record.
6. **Define review evidence and a change trigger.** Plan observations that distinguish discovery, proposed admission, authorization decision, attempted call, returned result, and authoritative external effect. Identify which material change sends the record back to admission and evidence review.

The accompanying [MCP integration record](../../templates/2.7/mcp-integration-record.yaml) is a neutral planning/build template. It is deliberately filled with fictional, unexecuted values and unresolved fields where an actual owner or deployment fact would be needed.

## Requirements

- **MCP-01** When an agent uses MCP, its design record MUST state why MCP is used rather than a direct call or API adapter, and identify the host, client-to-server boundary, server operator, and local or remote execution context.
- **MCP-02** When a server advertises capabilities, the host MUST explicitly admit each capability the agent may use and MUST block unadmitted capabilities; discovery or model output MUST NOT itself grant authority.
- **MCP-03** When an MCP connection carries protected data or exposes an action, the system MUST authenticate the relevant connection identity, enforce authorization at the applicable execution boundary, and constrain access to the agent’s approved scope. A successful connection MUST NOT be treated as authorization for all server capabilities.
- **MCP-04** For each admitted MCP capability, the system MUST validate inputs and returned structure against its expected contract, apply bounded timeouts and defined failure handling, and treat returned content as untrusted. When an operation can cause an external effect, its retry behavior MUST follow the applicable effect and recovery policy in [2.4](04-tools-and-external-interfaces.md) and [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).
- **MCP-05** When MCP is in the execution path, the team MUST test the underlying task outcome, permission boundaries, malformed or untrusted results, timeout or denial behavior, and any relevant effects. Evidence MUST correlate the agent run to the server and admitted capability without requiring secrets or raw hidden reasoning.

## Worked example: approved travel-policy documents

This is a fictional, unexecuted local review unit for `POLICY-BUILD-001`, the `internal-policy-assistance` candidate. The candidate uses a fixed retrieval-and-answer workflow: it can branch to a declared bounded outcome, but no model-selected write or approval capability is enabled. It answers policy questions from current, approved, requester-permitted sources and returns citations and uncertainty. It is not an assembled, admitted, approved, deployed, or evaluated system.

The proposed task is to answer an employee's London hotel-limit question. In the fictional fixture, `employee-uk-104` may read `travel-policy-2026@2026-10-01`, a current approved policy that says GBP 220. `travel-policy-2024-superseded@2024-01-01` remains an approved historical record but is not current and says GBP 200. `contractor-uk-204` may not read either policy source. These source and permission facts are fixture conditions, not real policy or an observed integration result.

The planning record compares a narrow direct document-search adapter with a possible remote MCP document boundary. Its stated rationale for considering MCP is that a compatible host could reuse one constrained, read-only policy-document interface; its limits are unresolved server operator identity, connection identity, and actual change behavior. That comparison does not select the MCP option or authorize a server. If the direct adapter met the same bounded need with less integration burden, the record could retain that alternative.

For the MCP candidate, a future discovery response might advertise a policy resource, a document-search tool, a reusable prompt, and an unrelated policy-editing tool. The record treats every item as unobserved until it can be assessed. It proposes only one read-only policy-search capability for possible admission. It keeps the edit tool, unrelated prompt, roots, elicitation, and sampling outside the candidate's capability set. An advertised description that calls the edit tool “safe” would not alter that decision.

Before a read reaches the policy source, the protected retrieval boundary would receive trusted requester and resource scope, rather than relying on a tenant or source identifier supplied by the model. The proposed response contract contains source identity, revision, currentness, bounded excerpt, and an explicit result status. The host would validate the search arguments and the returned shape, then pass returned text to the model as untrusted evidence. Neither the protocol connection, a matching schema, nor the presence of a source citation would establish that GBP 220 is current or accessible; the source-state and permission checks answer those questions.

The expected behavior is case-specific. For `employee-uk-104`, the current permitted source supports a `complete` answer that cites GBP 220. If the current permitted source is absent, the bounded outcome is `needs_information`, not an answer from the superseded source. If two equally authoritative, current, requester-permitted sources conflict, the candidate identifies the conflict and seeks declared clarification or escalation; it does not choose the later date automatically. For `contractor-uk-204`, the retrieval boundary declines access without disclosing the amount. If the server returns a timeout or malformed result, the candidate reaches its declared `failed` or `needs_information` outcome rather than claiming a verified answer.

A review plan can associate each proposed case with the candidate version, intended protocol version, identified server boundary, proposed capability identifier, fixture revision, authorization decision, attempted exchange, returned result status, and answer/source assessment. Those are distinct observations. No server response, dispatch, write receipt, or authoritative external effect is asserted here. If a later proposal adds an update action or materially changes the server's identity, scope, primitive contract, or protocol profile, it is a new admission and evidence question, with the applicable tool, authority, and durable-effect owners engaged.

## Evidence and checklist

For a proposed MCP integration, useful completion evidence is reviewable rather than self-certifying. A record can make the following items inspectable without collecting secrets, raw hidden reasoning, or unnecessary content:

- The task-specific comparison of MCP and a direct adapter, including why the additional protocol boundary is proportionate and what remains unresolved.
- The proposed host, client-to-server boundary, server/operator identity basis, local or remote placement, protocol version, transport category, and data flow.
- An explicit inventory of discovered or expected primitives, the narrow proposed admissions, the deliberately blocked surface, and the trigger for re-admission when that surface changes.
- The trusted identity and scope inputs to the protected operation, the expected authorization enforcement point, and the distinction between token audience, server identity, and downstream authority where relevant.
- The bounded contract for every proposed admitted capability, including validation, returned-content handling, timeout and failure outcomes, and effect/retry treatment if any action is introduced.
- A case plan that examines the underlying policy answer, currentness, requester permission, hostile or malformed result, timeout or denial, and the distinction between a proposed call, a dispatched attempt, and any authoritative effect.
- A privacy-aware correlation design that can connect a future run to the admitted capability and server boundary without treating that correlation as proof of task correctness or control effectiveness.

A checked template, a discovery transcript, an allowlist, or a successful protocol exchange is evidence to inspect, not proof that an integration is safe, correctly authorized, or suitable for release. Part 4 owns the design and interpretation of decision-grade evaluation evidence.

## References

[1]: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture "MCP Architecture Overview"
[2]: https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle "MCP Specification 2025-11-25: Lifecycle"
[3]: https://modelcontextprotocol.io/specification/2026-07-28/changelog "MCP Specification 2026-07-28: Key Changes"
[4]: https://modelcontextprotocol.io/specification/2026-07-28/server/discover "MCP Specification 2026-07-28: Server Discovery"
[5]: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization "MCP Specification 2025-11-25: Authorization"
[6]: https://modelcontextprotocol.io/specification/2026-07-28/client/roots "MCP Specification 2026-07-28: Roots"
[7]: https://modelcontextprotocol.io/specification/2026-07-28/server/tools "MCP Specification 2026-07-28: Tools"
[8]: https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation "MCP Specification 2025-11-25: Elicitation"

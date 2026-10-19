# 3.1 Identity, Authority, Zero Trust, and Least Privilege

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent builders, security reviewers, resource owners, and operators who need to make an agent's authority boundary inspectable.

**Applicability:** Every production agent needs an identifiable authority boundary. Apply this chapter when an agent, a tool it calls, or a downstream component reaches a protected resource or capability. Depth depends on the data, action, destination, and consequence; a read-only agent can still disclose protected material. No particular protocol or tool is required.

**Reader question:** Whose authority is being used for this operation, what exact action and resource are in scope, and what independently observable boundary stops a request, model, or discovered capability from enlarging that scope?

[Part 3 — Security and Trust Boundaries](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) · [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md) · [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md)

**Companion record:** [authority-boundary record](../../templates/3.1/authority-boundary-record.yaml) — a neutral planning record for the shared fictional policy-assistance candidate.

## Purpose and applicability

An authority boundary answers one question where access could occur: **may this authenticated workload perform this action on this resource in this context now?** A good-looking model response, an earlier successful run, a network location, or a person's general approval of an agent does not answer it. It matters before a read as much as a write: a read can disclose another person's material or cross a tenant boundary.

**Zero trust** is a security strategy, not a certification or a promise that compromise is impossible. NIST describes it as moving attention from network perimeters to users, assets, and resources: network location or asset ownership creates no implicit trust, and authentication and authorization are separate functions done before a resource session starts. [1] For an agent, the protected resource decides explicitly; the model, its host, and a previous decision are not standing permission.

The capability manifest is in [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md), tool contracts in [2.4](../02-agent-basics/04-tools-and-external-interfaces.md), hostile content in [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md), retention and audit in [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md), and approval and uncertain effects in [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).

## Working model

Keep four things distinct, even when one service carries several.

- A **workload identity** identifies the running agent or its environment, verifiably and separately from a developer's credential or another workload.
- A **requesting principal** is the person or system on whose behalf a request arrives; the model cannot assert it in a tool argument.
- A **resource context** identifies what is protected: a document, record, collection, tenant, data class, or destination.
- **Authority** is bounded permission for an operation in this context, from a policy decision on trusted facts, not from capability discovery, source approval, a response schema, or a credential that happens to be present.

Authorize the tuple **authenticated workload, relevant requester, action, resource, and effective context**, where context (tenant, data class, destination, source status, time, approval or other policy facts) can narrow the result. NIST's ABAC guide decides from subject and object attributes, the operation, environment conditions, and policy; use it to ask which facts matter, not as a required model. [2]

```text
admitted capability
  → trusted workload/requester/resource context
  → normalized proposed operation
  → resource-side authorization decision
  → permitted operation or declared bounded outcome
  → minimal decision observation
```

The model may propose an operation but does not authorize it. An admitted capability means an operation is available, not that every requester, object, or destination is allowed.

### Autonomous and delegated authority

An agent can act under **autonomous service authority** (only what the workload itself may do), **delegated requester authority** (when the decision depends on the requester's own scope), or a bounded mix. In a mix, broad service access cannot stand in for a requester's denied access, and a requester's preference cannot make the workload use a capability it was not admitted to use.

Name the trusted source of each identity- or scope-bearing value. A user-provided account label, a model-generated tenant, a document URL, or a tool result is a request parameter, not provenance for authority. Keep reusable personal credentials out of model-visible context; the execution layer passes verified context instead.

When calling a downstream service for a user, pass the user's authority explicitly; do not forward their token or use a broad service credential. OAuth token exchange (RFC 8693) defines delegation, where the new token names both the user and the acting party, as distinct from impersonation, where the actor is hidden; delegation keeps the audit trail honest. [5] Request tokens limited to the target service and needed scope (audience and resource indicators); each service checks that a token was meant for it. The MCP authorization specification requires audience validation and forbids passing a received token through to another service. [6] NIST's NCCoE is developing guidance on identity and authorization for agents. [7] OWASP's Top 10 for Agentic Applications is a companion to its LLM list for agent-specific risks. [8]

### Permission, approval, and evidence are different

**Permission** is the resource-side decision that the operation is allowed now. **Approval** is an extra policy condition for a defined consequential action. It cannot create an identity, add a tool, widen a resource scope, or override a later denial; an effectful path still rechecks authorization just before the operation. [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) covers binding, expiry, cancellation, and durable state. Keep approvals rare, specific, and clear, so reviewers do not rubber-stamp them.

An authorization record shows an allow or deny under a named policy and context, not that other boundaries worked or an effect occurred (Part 4).

## Decisions and best practices

### Start from the operation, not the credential

Work back from the declared task to each protected operation, recording for each capability the action, resource class, requester or tenant relationship, data class, possible destination, and what is deliberately absent. A policy-answering candidate may need a permission-filtered document read but no record update, network egress, or expense approval. Least privilege covers actions, data, credentials, and destinations, not one token.

Default to deny: being discovered, named in a prompt, returned by a tool, or used in a past run gives an unlisted action, source, destination, or capability no route to execution. Keep the admitted set reviewable through the versioned capability manifest from 2.2, which identifies the configuration but makes no access decisions.

Review combinations as well as single grants: protected retrieval plus unrestricted posting, broad file export, or a general execution interface that bypasses a narrow adapter. The sharpest case, Simon Willison's "lethal trifecta", is private data plus untrusted content plus a way to communicate externally, so injected text can read and send out secrets. [9] Meta's "Agents Rule of Two" turns this into a design test: within one session, an agent should have no more than two of untrusted input, sensitive data or systems, and the ability to change state or communicate externally. A task that needs all three is split into separate sessions or supervised, for example with human approval. [10] See [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md#defence-in-depth-against-prompt-injection), and trace where output could go after each allowed read.

### Isolate execution and restrict egress

Run code-executing or tool-using agents in an isolated environment holding only what the run needs: a scoped file area, no ambient host credentials, and short-lived per-run credentials. Deny outbound network access by default, with an allowlist of named destinations enforced outside the model and agent process. This limits what a hijacked or mistaken run can reach and send.

### Choose an authority mode and verify its provenance

For each operation, record its mode and how the workload identity, requester context, resource attributes, and policy identity reach the enforcement point. Reject unresolved provenance rather than defaulting it, or a correctly authenticated broad service credential becomes proof that any user the model names may see any object.

OAuth's security BCP has the same goal: minimum privileges, tokens bound to an intended audience and resources or actions and verified on each request, and sender-constrained tokens so a stolen one cannot be replayed. [3] OAuth is not required, and a valid token still needs resource-side checks.

### Normalize, then authorize the operation that will execute

Normalize and validate identifiers, paths, object references, and destinations before comparing them with allowed scope and deciding. Recheck when the target or action changes; a session-start decision does not cover a later request, and a check on `reports/allowed` does not authorize a representation that resolves outside that boundary. Output schemas, prompts, source labels, and model self-reports cannot show that an object, property, or destination is permitted. [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) covers validating untrusted proposals.

### Plan freshness, revocation, and unavailable policy

Authority changes after a credential or configuration is created. Design so scope can be narrowed, withdrawn, or rotated; avoid long-lived broad credentials; record the policy identity or freshness signal (not credentials) with each decision.

No universal lifetime or revocation mechanism is prescribed. RFC 7009 shows the tradeoff: revocation can propagate with delay, while immediate checks, shared state, and short-lived credentials trade availability against freshness. [4] Whatever the mechanism, fail closed when authorization is missing, invalid, stale, or unavailable: a bounded failure beats broader access.

### Keep approval and effects on their own paths

A read-only candidate needs no approval flow. A consequential action added later first gets an explicit authority, target, and effect boundary, then Part 7 controls; no proposal, request, or approval enables a missing write capability. [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) covers whether an effect occurred; a dispatched request does not prove one.

### Recognize common boundary failures

- A prototype credential left in the runtime blurs the workload with a developer or another workload.
- A service-only check leaks a permitted source to an ineligible requester.
- A check before normalization approves one representation, then executes a different target.
- A broad cached decision outlives a scope change, so revocation fails.
- An approval reused for changed arguments confuses consent with permission.
- A call log shows an attempt but cannot prove an outcome.

The remedies differ: a narrower credential does not fix a missing object check, nor a prompt label a model-controlled tenant field, nor an approval record an unavailable policy decision.

## Requirements

- **AUTH-01** — When a production agent accesses a protected resource, the owner MUST authenticate it with a verifiable workload identity that is distinguishable from the initiating user or system. The agent MUST NOT rely on a developer's personal credential or a credential shared with an unrelated workload.
- **AUTH-02** — When credentials or capabilities are granted, the owner MUST limit them to the declared resources and actions, and to the applicable user, tenant, data class, and destination scope. Unlisted capabilities MUST be denied by default. Credential scope and effective admitted capabilities MUST be reviewable for the deployed version.
- **AUTH-03** — Before each protected operation, the enforcement point MUST authorize the authenticated workload and relevant requester against the requested action, resource, and effective scope. It MUST deny the operation when authorization is missing, invalid, stale, or unavailable; it MUST NOT substitute model output, prompt text, prior approval, or network location for that decision.
- **AUTH-04** — When access is user- or tenant-scoped, the system MUST derive or validate that scope from authenticated context and enforce it at the resource boundary. It MUST reject a scope supplied only by the agent or user-controlled content when that scope conflicts with the authenticated context.
- **AUTH-05** — When policy requires approval for a consequential action, the system MUST verify approval for that action and its material scope at execution time. Approval MUST NOT authorize a capability or resource outside the agent's independently permitted authority.

## Worked example

The fictional, unexecuted record `POLICY-BUILD-001` (linked to planning record `POLICY-PLAN-001`) describes a permission-filtered, read-only policy-assistance candidate with **no write capability and no approval capability**.

### The permitted case

For `employee-uk-104`, the fixture says `travel-policy-2026@2026-10-01` is current, approved, and available, and retrieval is limited to that requester's permitted policy evidence. The London hotel answer is grounded in the current permitted source, which states GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` record is history, not authority for a current answer, and currentness is a source-status fact that grants no access.

### Denial, changed target, and unavailable decision

For `contractor-uk-204`, the same source is not accessible, whatever a model-produced source identifier, user assertion, or discovered historical document says. Expect a denial at retrieval and a `declined` result with no restricted content.

If the model, after reading suggestive content, proposes a different document collection or an external destination, the baseline candidate has no admitted route for either. If the authorization dependency is stale or unavailable, the caller gets its declared bounded outcome, not a guess or a broad cached scope.

If two equally authoritative, current, requester-permitted sources disagree, picking the newer-looking value is neither an authorization nor a precedence rule; the response is `needs_information` with escalation or clarification. [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) owns currentness and conflict handling.

### What cases can show

Cross-requester, changed-target, unlisted-destination, and unavailable-authorization cases each test one boundary claim, recordable without credentials or unneeded source bodies (Part 4).

## Evidence and checklist

- [ ] Workload identity, requester identity, resource or tenant context, and the provenance of each authority-bearing value are recorded separately.
- [ ] Each admitted capability has a declared action, resource, requester or tenant relationship, data class, and destination limit; absences are visible.
- [ ] The enforcement point receives a normalized operation and trusted context, and a changed target, destination or scope gets a new decision.
- [ ] The freshness and revocation mechanism and its limits are reviewable.
- [ ] Indirect paths and egress combinations are considered.
- [ ] Delegated calls pass an audience-limited token for the requester, not a forwarded one.
- [ ] Code-executing or tool-using runs are isolated, with deny-by-default egress and per-run credentials.
- [ ] Planned evidence separates configuration identity, a resource-side decision, a dispatched attempt, and an authoritative effect, and avoids secrets, unneeded bodies, and raw hidden reasoning.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf "NIST SP 800-207: Zero Trust Architecture"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-162.pdf "NIST SP 800-162: Guide to Attribute Based Access Control Definition and Considerations"
[3]: https://www.rfc-editor.org/rfc/rfc9700.html "RFC 9700: Best Current Practice for OAuth 2.0 Security"
[4]: https://www.rfc-editor.org/rfc/rfc7009.html "RFC 7009: OAuth 2.0 Token Revocation"
[5]: https://www.rfc-editor.org/rfc/rfc8693.html "RFC 8693: OAuth 2.0 Token Exchange"
[6]: https://modelcontextprotocol.io/specification/draft/basic/authorization "Model Context Protocol: Authorization (draft specification)"
[7]: https://pages.nist.gov/nccoe-ai-identity/ "NIST NCCoE: Agentic AI Identity and Authorization"
[8]: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 "OWASP Top 10 for Agentic Applications for 2026"
[9]: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ "Simon Willison: The lethal trifecta for AI agents"
[10]: https://ai.meta.com/blog/practical-ai-agent-security/ "Meta AI: Agents Rule of Two: A Practical Approach to AI Agent Security"

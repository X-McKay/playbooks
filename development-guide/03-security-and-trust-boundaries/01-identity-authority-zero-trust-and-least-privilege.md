# 3.1 Identity, Authority, Zero Trust, and Least Privilege

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent builders, security reviewers, resource owners, and operators who need to make an agent's authority boundary inspectable.

**Applicability:** Every production agent needs an identifiable authority boundary. Apply this chapter when an agent, a tool it calls, or a downstream component reaches a protected resource or capability. Depth depends on the data, action, destination, and consequence; a read-only agent can still disclose protected material. No particular protocol or tool is required.

**Reader question:** Whose authority is being used for this operation, what exact action and resource are in scope, and what independently observable boundary stops a request, model, or discovered capability from enlarging that scope?

[Part 3 — Security and Trust Boundaries](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) · [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md) · [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md)

**Companion record:** [authority-boundary record](../../templates/3.1/authority-boundary-record.yaml) — a neutral planning record for the shared fictional policy-assistance candidate.

## Purpose and applicability

An authority boundary answers one question at the point where access could occur: **may this authenticated workload perform this action on this resource in this context now?** A good-looking model response, an earlier successful run, a network location, or a person's general approval of an agent does not answer it. The question matters before a protected read as much as before a write. A read can disclose another person's material or cross a tenant boundary.

**Zero trust** is a security strategy, not a certification or a promise that compromise is impossible. NIST describes it as moving attention from network perimeters to users, assets, and resources: network location or asset ownership alone creates no implicit trust, and authentication and authorization are separate functions done before a resource session starts. [1] For an agent, the protected resource makes an explicit decision. The model, its host environment, and a previous decision are not standing permission.

This chapter covers who or what is authenticated, which context facts can be trusted, and how a resource-side decision narrows an operation. The capability manifest is in [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md), tool contracts in [2.4](../02-agent-basics/04-tools-and-external-interfaces.md), hostile content in [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md), retention and audit in [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md), and approval and uncertain effects in [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).

## Working model

Keep four things distinct, even when one service carries several.

- A **workload identity** identifies the running agent or its environment: which software made the request. Its provenance should be verifiable and separate from a developer's personal credential or another workload.
- A **requesting principal** is the person or system on whose behalf a request arrives, when the task uses that party's scope. The model cannot assert it in a tool argument.
- A **resource context** identifies what is protected: a document, record, collection, tenant, data class, or destination.
- **Authority** is bounded permission to perform an operation in this context. It comes from a policy decision using trusted facts, not from capability discovery, source approval, a response schema, or a credential that happens to be present.

A useful authorization tuple is **authenticated workload, relevant requester, action, resource, and effective context**. Context can narrow a result by tenant, data class, destination, source status, time, approval, or other policy facts. NIST's ABAC guide offers a model: grant or deny from subject attributes, object attributes, the operation, environment conditions, and policy. Use it to ask which facts matter; ABAC itself is not required. [2]

A bounded path looks like this:

```text
admitted capability
  → trusted workload/requester/resource context
  → normalized proposed operation
  → resource-side authorization decision
  → permitted operation or declared bounded outcome
  → minimal decision observation
```

The model may help interpret a request or propose an operation, but it does not make the authorization decision. An admitted capability means an operation is available, not that every requester, object, or destination is allowed. A retrieved instruction cannot enlarge authority.

### Autonomous and delegated authority

An agent can act under **autonomous service authority**, **delegated requester authority**, or a bounded mix. Use autonomous authority only for what the workload itself may do, and delegated authority when the decision depends on the requester's own scope. In a mix, broad service access cannot stand in for a requester's denied access, and a requester's preference cannot make the workload use a capability it was not admitted to use.

The contract should name the trusted source of each identity- or scope-bearing dependency. A user-provided account label, a model-generated tenant, a document URL, or a tool result is a request parameter or evidence, not provenance for authority. Keep reusable personal credentials out of model-visible context; the execution layer can pass the verified context instead.

When the agent calls a downstream service on a user's behalf, pass the user's authority on explicitly instead of forwarding the user's token or using a broad service credential. OAuth token exchange (RFC 8693) defines delegation, where the new token names both the user and the acting party, as distinct from impersonation, where the actor is hidden. Delegation keeps the audit trail honest. [5] Request tokens limited to the target service and the needed scope (audience and resource indicators), and have each service check that a token was meant for it. The MCP authorization specification requires audience validation and forbids passing a received token through to another service. [6] NIST's NCCoE is developing guidance on identity and authorization for agents. [7] OWASP's Top 10 for Agentic Applications is a companion to its LLM list for agent-specific risks. [8]

### Permission, approval, and evidence are different

**Permission** is the resource-side decision that the operation is allowed now. **Approval** is an extra policy condition for a defined consequential action. It cannot create an identity, add a tool, widen a resource scope, or override a later denial; an effectful path still rechecks authorization just before the operation. [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) covers binding, expiry, cancellation, and durable state.

Keep approvals rare, specific, and clear about what will happen, so reviewers do not rubber-stamp them. An authorization record shows a decision was allowed or denied under a named policy and context. It does not show that other boundaries worked or that a target performed an effect; Part 4 covers those claims.

## Decisions and best practices

### Start from the operation, not the credential

Work back from the declared task to each protected operation. For each capability, make visible the action, resource class, requester or tenant relationship, data class, and possible destination, and record what is deliberately absent. A policy-answering candidate may need a permission-filtered document read but no record update, no general network egress, and no way to approve an expense. Least privilege covers actions, data, credentials, and destinations, not just one token.

Default to deny. An unlisted action, source, destination, or capability has no route to execution because it was discovered, named in a prompt, returned by a tool, or used in a past run. Keep the admitted set reviewable through the versioned capability manifest from [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md); the manifest identifies the configuration but makes no access decisions.

Review combinations as well as single grants. Two reasonable capabilities can form an unintended path: protected retrieval plus unrestricted external posting, broad file export, or a general execution interface that bypasses a narrow adapter. The sharpest case is an agent with private data, exposure to untrusted content, and a way to communicate externally: injected text can then read and send out secrets. Simon Willison calls this the "lethal trifecta". [9] Meta's "Agents Rule of Two" turns this into a design test: within one session, an agent should have no more than two of untrusted input, sensitive data or systems, and the ability to change state or communicate externally. If a task needs all three, split it into separate sessions or supervise it, for example with human approval. [10] See [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md#defence-in-depth-against-prompt-injection). Also trace where output could go after each allowed read.

### Isolate execution and restrict egress

Run code-executing or tool-using agents in an isolated environment that holds only what the run needs: a scoped file area, no ambient host credentials, and short-lived per-run credentials. Make outbound network access deny-by-default, with an allowlist of named destinations enforced outside the model and the agent process. This limits what a hijacked or mistaken run can reach and send, whatever the model decides.

### Choose an authority mode and verify its provenance

For each operation, say whether it is service-only, requester-delegated, or mixed, and how the workload identity, requester context, resource attributes, and policy identity reach the enforcement point. Reject unresolved provenance rather than filling it with a default. This prevents a common failure: a broad service credential authenticates correctly and is then treated as proof that any user the model names may see any object.

OAuth's current security BCP shows the same goal for access tokens: restrict privileges to the minimum, bind tokens to an intended audience and resources or actions, verify the bindings on each request, and prefer sender-constrained tokens so a stolen token cannot be replayed. [3] OAuth is not required, and a valid token still needs the resource-side checks that policy requires.

### Normalize, then authorize the operation that will execute

Authorization needs the final operation, not a tidy description of it. Normalize and validate identifiers, paths, object references, and destinations before comparing them with allowed scope, then decide before the operation runs. Recheck when the target or action changes; a session-start decision does not cover a later request. A check on `reports/allowed` does not authorize a representation that resolves outside that boundary.

Output schemas, prompts, source labels, and model self-reports cannot show that an object, property, or destination is permitted; the decision belongs at the protected operation. [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) covers validating untrusted proposals.

### Plan freshness, revocation, and unavailable policy

Authority can change after a credential or configuration is created. Design so scope can be narrowed, withdrawn, or rotated, and avoid long-lived broad credentials. Record the policy identity or freshness signal with each decision so a reviewer can tell which rule applied, without keeping credentials.

No universal lifetime or revocation mechanism is prescribed. RFC 7009 shows the tradeoff: revocation can propagate with delay, while immediate checks, shared state, and short-lived credentials trade availability against freshness. [4] The requirements keep a fail-closed rule when authorization is missing, invalid, stale, or unavailable. A bounded failure is better than broader access because a policy dependency is down.

### Keep approval and effects on their own paths

A read-only candidate needs no approval flow. If a later change adds a consequential action, first make its authority, target, and effect boundary explicit, then apply the controls in Part 7. A model proposal, user request, or approval record never turns a missing write capability into an enabled one. [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) covers whether an effect occurred; a dispatched request does not prove one.

### Recognize common boundary failures

- A prototype credential left in the runtime blurs the workload with a developer or another workload.
- A service-only check leaks a permitted source to an ineligible requester.
- A check before normalization approves one representation, then executes a different target.
- A broad cached decision outlives a scope change, so revocation fails.
- An approval reused for changed arguments confuses consent with permission.
- A call log shows an attempt but cannot prove an outcome.

The remedies differ: narrowing a credential does not fix a missing object check, a prompt label does not fix a model-controlled tenant field, and an approval record does not fix an unavailable policy decision.

### Builder workflow

1. **Inventory protected operations**, including indirect combinations. Mark absent capabilities as absent.
2. **Separate identities and trusted sources.** Leave unresolved provenance visible instead of substituting a model or request field.
3. **Choose the authority mode** for each operation (autonomous, delegated, or mixed) and set data, action, object, tenant, and destination limits.
4. **Place the enforcement point.** Define the normalized request it receives, the trusted context it uses, and its result when it cannot decide.
5. **Review lifecycle and composition:** revocation, rotation, stale policy, unavailable dependencies, indirect egress.
6. **Plan evidence:** a configuration identity, a resource-side decision record, and permitted and denied cases.

## Requirements

- **AUTH-01** — When a production agent accesses a protected resource, the owner MUST authenticate it with a verifiable workload identity that is distinguishable from the initiating user or system. The agent MUST NOT rely on a developer's personal credential or a credential shared with an unrelated workload.
- **AUTH-02** — When credentials or capabilities are granted, the owner MUST limit them to the declared resources and actions, and to the applicable user, tenant, data class, and destination scope. Unlisted capabilities MUST be denied by default. Credential scope and effective admitted capabilities MUST be reviewable for the deployed version.
- **AUTH-03** — Before each protected operation, the enforcement point MUST authorize the authenticated workload and relevant requester against the requested action, resource, and effective scope. It MUST deny the operation when authorization is missing, invalid, stale, or unavailable; it MUST NOT substitute model output, prompt text, prior approval, or network location for that decision.
- **AUTH-04** — When access is user- or tenant-scoped, the system MUST derive or validate that scope from authenticated context and enforce it at the resource boundary. It MUST reject a scope supplied only by the agent or user-controlled content when that scope conflicts with the authenticated context.
- **AUTH-05** — When policy requires approval for a consequential action, the system MUST verify approval for that action and its material scope at execution time. Approval MUST NOT authorize a capability or resource outside the agent's independently permitted authority.

## Worked example

The fictional record `POLICY-BUILD-001` describes a permission-filtered, read-only internal policy-assistance candidate linked to planning record `POLICY-PLAN-001`. It is `illustrative-unexecuted`: nothing is deployed and no test has run. The candidate answers an eligible requester from approved current policy evidence and returns uncertainty when that evidence is missing or conflicts. It has **no write capability and no approval capability**.

### The permitted case

For `employee-uk-104`, the fixture says `travel-policy-2026@2026-10-01` is current, approved, and available to the requester. Retrieval is limited to permission-filtered policy evidence for that requester. A real build would resolve the workload, requester, resource context, and policy provenance through declared trusted dependencies; the record invents none.

The expected answer to the London hotel question is grounded in the current permitted source, which states GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` record is history, not authority for a current answer. Currentness is a source-status fact; it grants no access.

### Denial, changed target, and unavailable decision

For `contractor-uk-204`, the same source is not accessible in the fixture. A model-produced source identifier, a user assertion, or a discovered historical document cannot change that. The planned observation is a denial at retrieval and a `declined` result with no restricted policy content in the output.

Suppose a model proposes a different document collection or an external destination after reading content that suggests it. The baseline candidate has no admitted route for either. A real enforcement point would normalize the requested resource or destination and authorize it against trusted context before any access. If the authorization dependency is stale or unavailable, the requirements call for denial, and the caller gets its declared bounded outcome, not a guess or a broad cached scope.

If two equally authoritative, current, requester-permitted sources disagree, choosing the newer-looking value is neither an authorization rule nor a source-precedence rule. The bounded response is `needs_information` with escalation or clarification, not an invented amount. [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) owns currentness and conflict handling.

### What cases can show

Cross-requester, changed-target, unlisted-destination, and unavailable-authorization cases each test one boundary claim, and an allowed or denied decision can be recorded without credentials or unneeded source bodies. Part 4 covers evidence design. This example is fictional throughout.

## Evidence and checklist

- [ ] Workload identity, requester identity, resource or tenant context, and the provenance of each authority-bearing value are recorded separately.
- [ ] Each admitted capability has a declared action, resource boundary, requester or tenant relationship, data-class question, and destination limit; absences are visible.
- [ ] The enforcement point receives a normalized operation and trusted context, and decides before access or dispatch.
- [ ] A change in target, destination, requester scope, or material context is not covered by an earlier decision.
- [ ] Stale, revoked, missing, or unavailable authorization has a declared bounded behavior; the freshness and revocation mechanism and its limits are reviewable.
- [ ] Indirect paths and egress combinations are considered, including protected reads paired with export or effectful capability.
- [ ] Delegated calls pass an audience-limited token for the requester, not a forwarded one.
- [ ] Code-executing or tool-using runs are isolated, with deny-by-default egress and per-run credentials.
- [ ] Approval is an extra condition on independently permitted authority and is routed to Part 7.
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

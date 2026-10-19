# 3.1 Identity, Authority, Zero Trust, and Least Privilege

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Agent builders, security reviewers, resource and access owners, and operators who need to make an agent’s authority boundary inspectable.

**Applicability:** Every production agent needs an identifiable authority boundary. Apply this chapter when an agent, a tool it invokes, or a downstream component accesses a protected resource or capability. The depth depends on the declared data, action, destination, and consequence; a read-only agent can still disclose protected material. This chapter does not require a particular identity protocol, delegated-user model, human approval flow, tool, or external service.

**Reader question:** Whose authority is being exercised for this operation, what exact action and resource are in scope, and what independently observable boundary prevents a request, model, or discovered capability from enlarging that scope?

[Part 3 — Security and Trust Boundaries](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](../02-agent-basics/02-agent-contracts-and-configuration.md) · [2.4 Tools and External Interfaces](../02-agent-basics/04-tools-and-external-interfaces.md) · [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](02-untrusted-inputs-retrieved-content-and-action-boundaries.md)

**Companion record:** [authority-boundary record](../../templates/3.1/authority-boundary-record.yaml) — a neutral, illustrative planning/build record for the shared fictional policy-assistance candidate. It does not enable a capability or report a working control.

## Purpose and applicability

An authority boundary answers a narrow question at the point where access could occur: **may this authenticated workload perform this action on this resource in this context now?** It is not answered by an attractive model response, a successful earlier run, a network location, or a person’s general approval of an agent. The question matters before a protected read as much as before an external write. A read can disclose another person’s material, cross a tenant boundary, or supply facts that influence a consequential decision.

**Zero trust** is a security strategy, not a certification, repeated interactive login, or a promise that compromise is impossible. NIST describes it as moving attention from static network perimeters to users, assets, and resources, and says that network location or asset ownership alone does not create implicit trust. It treats authentication and authorization as separate functions before a resource session is established. [1] In an agent design, that translates to making the protected resource’s decision explicit rather than treating the model, its host environment, or a previous decision as a continuing permission.

This chapter owns the authority boundary: who or what is authenticated, which contextual facts can be trusted, and how a resource-side decision narrows an operation. It does not replace the agent contract’s dependency provenance and capability manifest in [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md), a tool’s typed contract and effect semantics in [2.4](../02-agent-basics/04-tools-and-external-interfaces.md), or the treatment of hostile content in [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md). Retention and audit-body choices belong in [3.3](03-data-privacy-handling-and-minimum-audit-evidence.md). Approval-state, suspension, and uncertain-effect handling belong in [Part 7](../../engineering-reference/07-durable-execution-and-human-governed-work/README.md).

## Working model

Keep four things distinct, even if one service carries some of their attributes.

- A **workload identity** identifies the running agent or its execution environment. It answers which software made a protected request. It should have a verifiable provenance separate from a developer’s personal credential or another unrelated workload.
- A **requesting principal** is the person or system on whose behalf a request arrives, when the task uses that person’s scope. It is not a value the model can assert in a tool argument.
- A **resource context** identifies what is being protected and the relevant boundary: for example, a document, record, collection, tenant, data class, or destination.
- **Authority** is the bounded permission to perform an operation in this context. It comes from a policy decision using trusted facts; it is not synonymous with capability discovery, source approval, a response schema, or a credential that happens to be present.

A useful authorization tuple is **authenticated workload, relevant requester, action, resource, and effective context**. The context may narrow a result through tenant, data-class, destination, source-status, time, approval, or other policy facts. NIST’s ABAC guide provides one way to reason about this shape: access can be granted or denied from subject attributes, object attributes, the requested operation, environment conditions, and policy. That model is useful for asking which facts matter; it is not a requirement to adopt ABAC or a specific policy engine. [2]

A bounded path is:

```text
admitted capability
  → trusted workload/requester/resource context
  → normalized proposed operation
  → resource-side authorization decision
  → permitted operation or declared bounded outcome
  → minimal decision observation
```

The model may help interpret a request or propose the operation, but it is not the authorization decision-maker. An admitted capability says an operation shape is available to the agent; it does not say that every requester, object, or destination is allowed. Likewise, a trusted source may establish a policy fact without becoming runtime policy, and a retrieved instruction cannot enlarge authority.

### Autonomous and delegated authority

An agent can act under **autonomous service authority**, **delegated requester authority**, or a deliberately bounded combination. Autonomous authority is appropriate only for the part of a task that the workload itself is allowed to do. Delegated authority is relevant when a resource decision depends on the authenticated requester’s own scope. A combination still needs both sides to be bounded: a service’s broad access cannot silently stand in for a requester’s denied access, and a requester’s stated preference cannot make the workload use a capability it was not admitted to use.

The contract should name the trusted source and type of each identity- or scope-bearing dependency. A user-provided account label, a model-generated tenant, a document URL, or a tool result is a request parameter or evidence, not provenance for authority. Avoid placing reusable personal credentials in model-visible context; the protected operation can instead receive the verified context it needs from the execution layer.

### Permission, approval, and evidence are different

**Permission** is the resource-side decision that the operation is allowed now. **Approval** is an additional policy condition for a defined consequential action. An approval cannot create an identity, add a tool, expand a resource scope, or override a later authorization denial. If an effectful path uses approval, it still rechecks authorization immediately before the protected operation. [7.3 Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) owns the exact binding, expiry, cancellation, and durable-state semantics.

An authorization record can show that a decision was requested and allowed or denied under a named policy/context identity. It does not prove that every other boundary worked, that a target performed an effect, or that a configuration is suitable for release. Part 4 supplies the case and evidence method needed for those separate claims.

## Decisions and best practices

### Start from the operation, not the credential

Start with the declared task and work backward from each protected operation. For a capability, make the operation’s action, resource class, requester/tenant relationship, data class, and possible destination visible. Also record what is intentionally absent. A policy-answering candidate may need a permission-filtered document read but no record update, no general network egress, and no ability to approve an expense. Least privilege is therefore a boundary across actions, data, credentials, and destinations, not a property of a single token.

Begin from a default-deny shape. An unlisted action, source, destination, or capability has no route to execution merely because it was discovered, named in a prompt, returned by a tool, or used successfully in a prior run. Keep the effective admitted capability set reviewable with the versioned manifest from [2.2](../02-agent-basics/02-agent-contracts-and-configuration.md). A capability manifest identifies the assembled configuration; it does not itself make a resource access decision.

Consider indirect composition as well as individual grants. Two individually plausible capabilities can create an unintended path, such as protected retrieval combined with unrestricted external posting, broad file export, or a general execution interface that bypasses a narrow adapter. Trace where sensitive output could go after each allowed read. This is a scope review, not a claim that every combination is harmful or that a single gateway makes a system safe.

### Choose an authority mode and verify its provenance

For each operation, state whether it is service-only, requester-delegated, or a combination. Then state how the workload identity, requester context, resource attributes, and policy identity arrive at the enforcement point. A builder can reject an unresolved provenance rather than filling it with a convenient default. This prevents a common confused-identity failure: a broad service credential is authenticated correctly, but it is treated as proof that any user named by the model may see any object.

When a protocol uses access tokens, OAuth’s current security BCP is a qualified example of the same design goal: restrict privileges to the minimum for the use case, bind tokens to an intended audience and relevant resources/actions, and verify those bindings for each request. [3] OAuth is not required here. Other mechanisms can support the same review questions, and a token that is syntactically valid still needs the resource-side checks that the applicable policy requires.

### Normalize, then authorize the operation that will execute

Authorization needs the final operation, not a friendly pre-normalized description. Normalize and validate resource identifiers, paths, object references, and destinations before comparing them with allowed scope; then make the authorization decision before the resource operation. Recheck a changed target or action rather than assuming that a decision made when a session began covers a later request. A check on `reports/allowed` does not establish permission for a representation that resolves outside that boundary.

This placement is also why output schemas, prompts, source labels, and model self-reports have limited roles. They can reject malformed data or help a model follow the task, but they cannot establish that an object, property, or destination is permitted. [3.2](02-untrusted-inputs-retrieved-content-and-action-boundaries.md) covers validation of untrusted proposals; the authorization decision belongs at the protected operation.

### Plan freshness, revocation, and unavailable policy deliberately

Authority can change after a credential or configuration is created. Design the path so that scope can be narrowed, withdrawn, or rotated where the underlying mechanism supports it, without treating a long-lived broad credential as the normal answer. Record the relevant policy identity or freshness signal with the decision so a reviewer can tell which rule was used without retaining credentials.

There is no universal lifetime or revocation mechanism in this draft. RFC 7009 illustrates the tradeoff in one protocol family: revocation may have a propagation delay, while immediate checks, state, communication overhead, and short-lived credentials make different availability and freshness choices. The suitable approach depends on the system design and risk analysis. [4] The proposed requirements below retain their existing fail-closed rule when authorization is missing, invalid, stale, or unavailable. A bounded failure or safe next step is more honest than broadening access because a policy dependency is unavailable.

### Keep approval and effects on their own paths

A read-only candidate does not need an approval flow merely because it is an agent. If a later change adds a consequential action, first make the independent authority, capability, target, and effect boundary explicit. Then apply the approval and durable/external-effect controls that its actual path triggers. A model proposal, a user request, or an approval record never turns a non-existent write capability into an enabled operation. [7.2 Side Effects, Idempotency, and Unknown Outcomes](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) addresses whether a target effect occurred; an observed dispatched request is not proof of that effect.

### Recognize common boundary failures

A prototype credential that remains in the runtime makes the effective workload hard to distinguish from a developer or another workload. A service-only check can leak a permitted source to an ineligible requester. An authorization check before an identifier is normalized can approve a harmless-looking representation and execute a different target. A broad cached decision used after scope has changed can make revocation ineffective. An approval reused for changed arguments confuses consent with permission. A call log can show an attempted request but cannot prove an authoritative external outcome.

These failures have different remedies. Narrowing a credential does not fix a missing object check. A prompt label does not fix a model-controlled tenant field. An approval record does not fix an unavailable policy decision. Treating the differences as visible design choices makes a review more useful than declaring a system “zero trust.”

### Builder workflow

Use the companion record as a planning/build artifact, not an admission, approval, or deployment artifact.

1. **Inventory protected operations.** List the read, write, delegation, export, and destination paths that the proposed task could reach, including indirect combinations. Mark absent capabilities as intentionally absent.
2. **Separate identities and trusted sources.** Record the workload, relevant requester, resource context, and policy/context dependencies separately. Leave an unresolved provenance explicit instead of using a model or request field as a substitute.
3. **Choose and constrain the authority mode.** For each operation, state whether authority is autonomous, delegated, or combined, and define the data, action, object/property, tenant, and destination limits.
4. **Place the enforcement point.** Describe the normalized request it receives, the trusted context it uses, and the result when it cannot make a valid decision. Keep this separate from prompt handling and tool-interface validation.
5. **Review lifecycle and composition.** Identify the change, revocation, rotation, stale-policy, unavailable-dependency, and indirect-egress questions that matter to the boundary. Route approval/effect questions to Part 7 when a consequential capability is actually proposed.
6. **Plan evidence without overstating it.** Identify a configuration/manifest identity, a resource-side decision observation, and permitted and denied cases. Define what each can establish and what it cannot establish before using it in a later evaluation or release decision.

## Requirements

- **AUTH-01** — When a production agent accesses a protected resource, the owner MUST authenticate it with a verifiable workload identity that is distinguishable from the initiating user or system. The agent MUST NOT rely on a developer's personal credential or a credential shared with an unrelated workload.
- **AUTH-02** — When credentials or capabilities are granted, the owner MUST limit them to the declared resources and actions, and to the applicable user, tenant, data class, and destination scope. Unlisted capabilities MUST be denied by default. Credential scope and effective admitted capabilities MUST be reviewable for the deployed version.
- **AUTH-03** — Before each protected operation, the enforcement point MUST authorize the authenticated workload and relevant requester against the requested action, resource, and effective scope. It MUST deny the operation when authorization is missing, invalid, stale, or unavailable; it MUST NOT substitute model output, prompt text, prior approval, or network location for that decision.
- **AUTH-04** — When access is user- or tenant-scoped, the system MUST derive or validate that scope from authenticated context and enforce it at the resource boundary. It MUST reject a scope supplied only by the agent or user-controlled content when that scope conflicts with the authenticated context.
- **AUTH-05** — When policy requires approval for a consequential action, the system MUST verify approval for that action and its material scope at execution time. Approval MUST NOT authorize a capability or resource outside the agent's independently permitted authority.

## Worked example

The shared fictional record `POLICY-BUILD-001` describes a permission-filtered, read-only internal policy-assistance candidate linked to planning record `POLICY-PLAN-001`. Its status is `illustrative-unexecuted`: it reports neither a deployed identity nor a completed test. The candidate may answer an eligible requester from approved current policy evidence and return uncertainty when that evidence is missing or conflicts. It has **no write capability and no approval capability enabled**.

### Boundary for the permitted fixture case

For `employee-uk-104`, the controlled fixture says that `travel-policy-2026@2026-10-01` is current, approved, and available to the requester. The protected retrieval operation is limited to permission-filtered policy evidence for that requester. The workload identity, requester identity, resource context, and policy-decision provenance are fields that a real build would resolve through its declared trusted dependencies; the illustrative record does not invent those identities or claim that they have been admitted.

The expected behavior for the fixture question about a London hotel is a bounded answer grounded in the current permitted source, which states GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` record may be available as historical fixture material but is not authority for a current-policy answer. Currentness establishes a source-status fact; it does not by itself grant the workload or requester access.

### Denial, changed target, and unavailable-decision paths

For `contractor-uk-204`, the same source is not requester-accessible in the fixture. A model-produced source identifier, a user assertion, or a discovered historical document cannot change that. The planned boundary observation is a denial at protected retrieval and a `declined` result without restricted policy content in the output. That is an expected fixture relation, not an observed execution result.

Suppose a model proposes a different document collection or an external destination after reading content that suggests it. The baseline candidate has no admitted route for either expansion. A real enforcement point would normalize the requested resource/destination and authorize the resulting request against its trusted workload/requester context before any access. If the authorization dependency is stale or unavailable, the proposed requirements call for the protected operation to be denied; the caller receives its declared bounded outcome rather than a guessed answer or a broad cached scope.

The conflict variant is equally important. If the fixture exposes two equally authoritative current, requester-permitted sources that disagree, selecting the newer-looking value is not an authorization rule or a source-precedence rule. The candidate’s bounded response is `needs_information` and escalation/clarification rather than an invented definitive amount. This chapter does not assign the source-resolution policy; [2.6 Context and Retrieval Fundamentals](../02-agent-basics/06-context-and-retrieval-fundamentals.md) owns currentness and conflict handling.

### What the record and cases can show

A later test can inspect that the effective configuration identifies a narrow read capability, the protected boundary receives trusted context, and an allowed or denied decision is recorded without credentials or unnecessary source bodies. A cross-requester, changed-target, unlisted-destination, and unavailable-authorization case can each test a specific boundary claim. None of these artifacts alone proves that a deployment is secure, that a document supports an answer, that no external effect occurred, or that an organizational policy has been adopted. Part 4 supplies the evidence design and interpretation for those claims.

## Evidence and checklist

A completed authority-boundary review is a **proposed local review unit**, not an approved or deployed system. The useful handoff is a record that another reviewer can inspect alongside the effective contract and applicable tests.

- [ ] The record distinguishes workload identity, requester identity where relevant, resource/tenant context, and the provenance of each authority-bearing value.
- [ ] Each admitted capability has a declared action, resource/object or property boundary, requester/tenant relationship where applicable, data-class question, and destination limit; intentional absences are visible.
- [ ] The enforcement point receives a normalized operation and trusted context, then makes the protected-operation decision before resource access or external dispatch.
- [ ] A change in target, object/property, destination, requester scope, or material context is not silently covered by an earlier decision.
- [ ] Stale, revoked, missing, or unavailable authorization has a declared bounded behavior rather than a broader fallback; the chosen freshness/revocation mechanism and its limits are reviewable.
- [ ] Indirect paths and egress combinations have been considered, including the combination of protected reads with later export or effectful capability.
- [ ] Approval, when a consequential action is actually proposed, remains an additional condition on independently permitted authority and is routed to the Part 7 owner.
- [ ] Planned evidence distinguishes an effective configuration identity, a resource-side decision, a dispatched attempt, and an authoritative external effect. It avoids secrets, unnecessary bodies, and raw hidden reasoning.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf "NIST SP 800-207: Zero Trust Architecture"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-162.pdf "NIST SP 800-162: Guide to Attribute Based Access Control Definition and Considerations"
[3]: https://www.rfc-editor.org/rfc/rfc9700.html "RFC 9700: Best Current Practice for OAuth 2.0 Security"
[4]: https://www.rfc-editor.org/rfc/rfc7009.html "RFC 7009: OAuth 2.0 Token Revocation"

# 2.2 Agent Contracts and Configuration

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent owners, builders, reviewers, and operators who need a bounded, inspectable agent configuration.

**Applicability:** Every production agent needs this contract layer. Fields and controls beyond the common interface apply only when the agent enables the matching model, capability, execution class, or downstream consumer.

**Reader question:** What must be declared before an agent accepts work, how does a declared configuration become an effective configuration, and what lets a reviewer identify the configuration behind an outcome?

[Part 2 overview](README.md) · [Applicability and conformance](../../applicability.md) · [1.4 Initial Risk, Data, Ownership, and Delivery Plan](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) · [2.3 Prompts and Instructions](03-prompts-and-instructions.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md)

## Purpose and applicability

An **agent contract** is a reviewable declaration of an agent's bounded job, inputs, dependencies, behavior limits, outcomes, and accountable owner. It is not a prompt, an access grant, an approval, or a record that the agent ran. It tells a caller how to supply task data and handle each outcome, and a builder what to check before construction.

Even a response-only assistant needs one, because its answer can be incomplete, misleading, unavailable, or out of scope. Each model, retrieval source, skill, tool, or durable execution adds surface, and the contract makes it visible. Declaring a capability does not enable it: construction must resolve and admit it first.

This chapter covers agent-level configuration and the **capability manifest** that records its effective form. Risk and ownership start in [1.4](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md); instructions, tools, and retrieval are in [2.3](03-prompts-and-instructions.md), [2.4](04-tools-and-external-interfaces.md), and [2.6](06-context-and-retrieval-fundamentals.md); identity, authorization, untrusted content, and data handling are in Part 3. The contract points to them without weakening them.

## Working model

### Three records, three different jobs

Keep three records separate:

- **Declared configuration** is the versioned, reviewed design: purpose, accepted input, output contract, owner, execution class, governance tier, risk-record reference, model policy, allowed capabilities, bounds, and version identities.
- **Runtime state** is per-run: request identifier, authenticated identity and resource scope, deadline, permitted evidence identifiers, usage counters, and terminal outcome. It must not carry raw secrets or live clients in serializable state.
- **Effective capability manifest** is the immutable record of what construction actually resolved from the declared configuration, including immutable identities or digests where used.

This borrows the separation, not the process or roles, from NIST's configuration baseline: reviewed specifications at a point in time, with change control and monitoring as separate activities. [1] A request must not silently alter the reviewed configuration, and a configuration edit is not run state.

```text
declared contract
  → validate required fields and cross-field consistency
  → resolve named model, instructions, schemas, sources, skills, and tools
  → verify explicit admission and execution-class compatibility
  → construct or fail closed
  → emit effective capability manifest when construction succeeds
```

Failing before construction stops a missing owner, unresolved model policy, absent budget, unknown capability, or mismatched governance tier from becoming an implicit default.

### Caller fields are not trusted dependencies

Classify every incoming value by role. A caller submits task data, such as a policy question. A trusted runtime dependency supplies a request identifier, authenticated requester reference, tenant or resource scope, deadline, or authorization decision; name each one's type and trusted source rather than calling it "context."

A tenant label or claimed permission in a request body or model output is task data, not authority; the protected operation resolves and authorizes trusted context under Part 3. A retrieved source can support a policy fact but never becomes an instruction or grants a capability. Put a stable identifier, not a credential or live client, into recoverable state.

### Outcomes are an interface, not a success-only story

The ordinary terminal outcomes are:

- `complete`: the bounded answer plus the evidence identifiers or uncertainty the caller needs.
- `needs_information`: what input or evidence is missing, ambiguous, or unresolved, with a safe next step where applicable.
- `declined`: the request is outside the contract, stated without disclosing protected content or inventing authority.
- `failed`: a bounded operational failure, never passed off as a completion.

An optional `partial` or escalation outcome needs equally precise content and caller handling and must not become a catch-all for a polished but unsupported answer. These are agent outcomes, not Part 4 evaluator statuses.

A schema rejects missing fields, unexpected structure, and out-of-range values (JSON Schema defines validation as assertions about instance structure [2]); it cannot show that an answer is supported, a citation authoritative, the requester authorized, or an effect real.

## Decisions and best practices

### Declare desired capability separately from effective capability

Start from no optional capabilities. Declare the narrow operation the job needs, the model policy where a model is used, and the source, skill, or tool identities. Keep this **desired declaration** separate from **effective membership**: a discovered package, bundled capability, or model-suggested operation stays unavailable until construction explicitly admits it and resolves the expected identity. Granting only what the job needs (least agency) limits what a manipulated or mistaken model can do.

The same applies to execution class. A model router in a fixed read-only workflow, or a finite admitted allowlist in a bounded adaptive sequence, does not make the allowlist open-ended. Classify from enabled behavior, and do not let a later resolution lower the class that behavior requires. Effects, retries, durable handling, and approval are in [2.4](04-tools-and-external-interfaces.md) and Part 7.

### Make limits both declared and enforceable

Record request, model-token, tool-call, time, and cost bounds where they apply, each with its policy identity and enforcement point. A described limit stops nothing, and an undeclared enforcement point cannot be judged. The accountable owner sets values and reasons; this chapter sets no defaults.

Use a logical, versioned model policy when the policy is more stable than a specific resolution; record a fixed resolution and its settings when reproducibility or a feature needs it. Either way, model output is data: it cannot enlarge the capability list, change a budget, or replace authorization.

### Fail closed before accepting work

Construction validation checks every field that would otherwise be silently defaulted. It stops, accepting no work, when:

- an owner, governance tier, risk-record identity, output schema, policy, or budget is absent or invalid;
- the governance tier does not match the referenced risk record;
- a named capability cannot resolve to one immutable identity, resolves twice, or is not explicitly admitted;
- the effective execution class is below the enabled capability's floor; or
- an authority-bearing dependency comes from caller data or model output instead of the trusted boundary.

Failing closed does not prove other controls work, but it beats filling a blank with a convenient label and later treating the candidate as reviewed.

### Treat the manifest as a binding record, not a trust verdict

The manifest records the resolved model and settings, instruction and output-schema identities, admitted capability membership, source and budget policy, execution class, governance and risk references, and a construction identity, as safe identifiers and digests, never secrets or hidden reasoning.

A digest binds a reviewer to the recorded configuration; it does not prove validity, security, truth, permission, or control effectiveness. SLSA recommends verifying provenance against trusted builder identities and expected values, and states its trust limits. [3] Likewise, inspect the manifest, admission evidence, output validation, and Part 3 and Part 4 evidence rather than treating a manifest ID as approval.

### Change what the evidence identifies

A change to model policy or settings, enabled capability, output contract, or budget policy gets a new agent version and effective-configuration identity; an instruction revision gets its own identity under [2.3](03-prompts-and-instructions.md). Link new evaluation evidence to that identity rather than relabeling old evidence. NIST's Generative AI Profile asks for documented model details, provenance, assumptions, and limitations, performance shown under deployment-like conditions, and documented limits on generalizing. [4] A new manifest improves traceability, not fitness for every context.

### A bounded builder workflow

1. Describe the interface: caller input, trusted dependencies with provenance, terminal outcomes, and caller handling.
2. Declare the configuration and the smallest capability set, leaving unknowns unresolved rather than defaulted.
3. Validate and resolve as above. On success, emit the manifest and attach its ID to evaluation and runtime records; on failure, keep the bounded reason and emit no manifest.
4. Hand off: tool owners get the admitted interface list, security owners the trusted-dependency and protected-operation boundary, and evaluators the manifest identity and the changed claim.

## Requirements

- **CONTRACT-01 — Complete interface.** **Applies to every agent.** The agent contract **MUST** declare the accepted input, trusted runtime dependencies and their provenance, schema-validated output, accountable owner, agent version, and permitted terminal outcomes. It **MUST** cover `complete`, `needs_information`, `declined`, and `failed`; any declared partial or escalation outcome **MUST** define its bounded content and caller handling.

- **CONTRACT-02 — Reviewable configuration.** **Applies to every agent construction.** The construction process **MUST** validate the contract before the agent accepts work and **MUST NOT** substitute defaults for missing or invalid owner, execution class, governance tier, risk-record reference, model policy where a model is used, budget, output schema, or enabled capability. The declared governance tier **MUST** match the referenced risk record. Invalid or unresolved declared configuration **MUST** fail closed.

- **CONTRACT-03 — Declared bounds.** **Applies when an agent can invoke a model, skill, retrieval source, tool, or other runtime capability.** The contract **MUST** declare a least-capability allowlist, applicable model policy, and enforceable request, token, tool-call, time, or cost bounds appropriate to the agent. The effective execution class **MUST NOT** be lower than the class required by its enabled capabilities. A bundled, discovered, or model-suggested capability **MUST NOT** become available without explicit admission.

- **CONTRACT-04 — Trusted dependencies.** **Applies when an agent receives identity, tenant, authority, deadline, or policy context.** The contract **MUST** name the trusted source and type for each such dependency. The runtime **MUST NOT** accept model-generated or request-body values as authorization and **MUST NOT** place raw secrets or unsafe live clients in serializable run state. Apply Part 3's canonical authorization rules when resolving or using these dependencies.

- **CONTRACT-05 — Validated outcomes.** **Applies when any output is consumed by a person, workflow, tool, or another agent.** The runtime **MUST** validate the output against the declared contract before downstream use. A proposed action **MUST** remain data until the separately authorized action path accepts it; a model statement that an action succeeded is not evidence of success.

- **CONTRACT-06 — Effective-configuration evidence.** **Applies to every successful agent construction and to each behavior-changing configuration release.** The construction process **MUST** produce a capability manifest with immutable identities or digests for the effective declared configuration, and its ID **MUST** be recorded with relevant evaluation evidence and observable runtime records. A change to model policy or settings, enabled capability, output contract, or budget policy **MUST** change the agent version and receive evaluation appropriate to the change. Instruction changes follow the versioning and evaluation rules in [2.3](03-prompts-and-instructions.md) and **MUST** receive a distinct effective-configuration identity.

## Worked example

The [policy-assistant contract template](../../templates/2.2/policy-assistant-contract.yaml) is a neutral planning record for `POLICY-BUILD-001`, the fictional `internal-policy-assistance` candidate; nothing here has run.

The job is to answer a policy question from evidence that is current and permitted for the requester. No write or approval capability is declared. A permission-filtered, read-only retrieval capability is desired, but effective membership stays empty until construction resolves and admits its identity. The record uses `ephemeral` as the execution class and leaves governance tier, budget, owner, and risk record unset.

Requester `employee-uk-104` asks about a London hotel costing GBP 220. The current source is `travel-policy-2026@2026-10-01`; a superseded source says GBP 200. The outcome is `complete` only when the protected retrieval boundary returns the permitted current source and the validated response cites it; an "approved" source can still be superseded or inaccessible to this requester.

Variants: a missing current permitted source gives `needs_information`, not a guessed amount; two equally authoritative current sources in conflict with no precedence rule also give `needs_information`, naming the conflict rather than choosing by date; `contractor-uk-204`, who may not read the policy, gets `declined` without the amount; retrieval exhaustion or timeout gives `failed`; a request to alter a booking is `declined` because no write capability is declared.

If the owner, risk-record identity, model policy, output-schema identity, budget policy, or resolved capability identity is `null`, construction fails closed and no manifest claims success. A manifest from a resolved build still does not show that the source supports the answer or that authorization worked.

## Evidence and checklist

From the contract a reviewer should be able to answer: what task data may a caller supply; which dependencies are trusted, and from where; what outcomes the caller can handle; which capabilities are declared versus admitted; what stops an invalid assembly from accepting work; and which effective configuration a piece of evidence identifies.

Keep the reviewed contract; validation results for missing, malformed, contradictory, and unadmitted configuration; the resolved capability-membership record; output-validation checks for every terminal outcome; and manifest-linked evaluation or runtime records. Part 4 decides what evidence a real decision needs.

- Does the contract separate caller input from trusted dependencies, naming the source and type of each authority-bearing one?
- Can a caller tell `complete`, `needs_information`, `declined`, and `failed` apart, and handle any declared extension safely?
- Are unresolved construction fields blocking construction rather than getting defaults?
- Is the desired capability list distinct from the admitted membership, including its execution-class floor?
- Is each declared bound paired with a named enforcement location?
- Does the manifest identify the effective model policy and settings, instructions, output schema, capability membership, source and budget policy, and construction identity, without secrets or hidden reasoning?
- Does a material change get a new agent version, effective identity, and evaluation handoff rather than inheriting earlier evidence?

## References

[1]: https://doi.org/10.6028/NIST.SP.800-128 "NIST SP 800-128: Guide for Security-Focused Configuration Management of Information Systems"
[2]: https://json-schema.org/draft/2020-12/json-schema-validation "JSON Schema Validation: A Vocabulary for Structural Validation of JSON"
[3]: https://slsa.dev/spec/v1.2/verifying-artifacts "SLSA v1.2 Build: Verifying artifacts"
[4]: https://doi.org/10.6028/NIST.AI.600-1 "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"

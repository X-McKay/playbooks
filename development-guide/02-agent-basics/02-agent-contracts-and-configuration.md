# 2.2 Agent Contracts and Configuration

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent owners, builders, reviewers, and operators who need a bounded, inspectable agent configuration.

**Applicability:** Every production agent needs this contract layer. Fields and controls beyond the common interface apply only when the agent enables the matching model, capability, execution class, or downstream consumer.

**Reader question:** What must be declared before an agent accepts work, how does a declared configuration become an effective configuration, and what lets a reviewer identify the configuration behind an outcome?

[Part 2 overview](README.md) · [Applicability and conformance](../../applicability.md) · [1.4 Initial Risk, Data, Ownership, and Delivery Plan](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) · [2.3 Prompts and Instructions](03-prompts-and-instructions.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md)

## Purpose and applicability

An **agent contract** is a reviewable declaration of an agent's bounded job, inputs, dependencies, behavior limits, outcomes, and accountable owner. It is not a prompt, an access grant, an approval, or a record that the agent ran. A good contract tells a caller how to supply task data and handle each outcome, and tells a builder what to check before construction.

It matters even for a response-only assistant, whose answer can be incomplete, misleading, unavailable, or out of scope. When the candidate also uses a model, retrieval source, skill, tool, or durable execution, the contract makes that extra surface visible. A declared capability is not automatically enabled; the effective configuration must resolve and admit it first.

This chapter covers agent-level configuration and the **capability manifest** that records its effective form. The initial risk record and delivery ownership start in [1.4](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md). Instruction design is in [2.3](03-prompts-and-instructions.md), tool semantics in [2.4](04-tools-and-external-interfaces.md), and retrieval and source evidence in [2.6](06-context-and-retrieval-fundamentals.md). Part 3 covers identity, authorization, untrusted content, and data handling. The contract points to those decisions and does not weaken them.

## Working model

### Three records, three different jobs

Keep **declared configuration**, **runtime state**, and the **effective capability manifest** separate.

- **Declared configuration** is the versioned intended design: purpose, accepted input, output contract, owner, execution class, governance tier, risk-record reference, model policy, allowed capabilities, bounds, and version identities. It is the reviewed starting point.
- **Runtime state** is per-run information: a request identifier, authenticated identity and resource scope, deadline, permitted evidence identifiers, usage counters, and the final outcome. It changes as work proceeds and must not carry raw secrets or live clients in serializable state.
- **Effective capability manifest** is the immutable record made after successful construction. It records what the builder actually resolved from the declared configuration, including immutable identities or digests where used.

This adapts configuration-baseline thinking: NIST describes a baseline as reviewed specifications at a point in time, with change control and monitoring as separate activities. [1] The playbook does not adopt NIST's process or roles; it borrows the separation. A changing request must not silently alter the reviewed configuration, and a configuration edit must not be confused with run state.

A useful construction path:

```text
declared contract
  → validate required fields and cross-field consistency
  → resolve named model, instructions, schemas, sources, skills, and tools
  → verify explicit admission and execution-class compatibility
  → construct or fail closed
  → emit effective capability manifest when construction succeeds
```

A failure before construction is useful: it stops a missing owner, unresolved model policy, absent budget, unknown capability, or mismatched governance tier from becoming an implicit default.

### Caller fields are not trusted dependencies

Classify every incoming value by role. A caller can submit a policy question and an optional response-format preference. A trusted runtime dependency provides things like a request identifier, authenticated requester reference, tenant or resource scope, deadline, or authorization decision. Name each dependency's type and trusted source; do not just label it "context."

A request body or model output may contain a tenant label or a claimed permission, but that is task data, not authority. The protected operation resolves and authorizes trusted context under Part 3. A retrieved source can support a policy fact, but it does not become a runtime instruction or grant a capability. Pass a stable identifier, not a credential or live client, into recoverable state.

### Outcomes are an interface, not a success-only story

An output contract specifies shape and meaning. The ordinary final outcomes are `complete`, `needs_information`, `declined`, and `failed`:

- `complete` holds the bounded answer and the evidence identifiers or uncertainty the caller needs.
- `needs_information` says what input or evidence is missing, ambiguous, or unresolved, with a safe next step where applicable.
- `declined` says the request cannot be done within the contract, without disclosing protected content or inventing authority.
- `failed` reports a bounded operational failure without passing off an unsupported answer as a completion.

An optional `partial` or escalation outcome needs equally precise content and caller handling, and must not become a catch-all for a polished but unsupported answer. These are agent outcomes, not Part 4 evaluator statuses such as pass, fail, invalid, or inconclusive.

A schema helps a receiver reject missing fields, unexpected structure, and out-of-range values; JSON Schema describes validation as assertions about the structure of instance data. [2] It does not show that an answer is supported, a citation is authoritative, the requester is authorized, or an external effect occurred. Other checks cover those.

## Decisions and best practices

### Declare desired capability separately from effective capability

Start from no optional capabilities. State the narrow operation the job needs, the model policy where a model is used, and the relevant source, skill, or tool identities. Then separate the **desired declaration** from the **effective membership**. A discovered package, bundled capability, or model-suggested operation stays unavailable until construction explicitly admits it and resolves the expected identity. Granting only the capabilities the job needs (least agency) limits what a manipulated or mistaken model can do.

The same applies to execution class. A fixed read-only workflow may use a model router, and a bounded adaptive sequence may choose among a finite admitted allowlist; neither makes the allowlist open-ended. Classify from the enabled behavior, and do not let a later resolution lower the class that behavior requires. Effects, retries, durable handling, and approval conditions are in [2.4](04-tools-and-external-interfaces.md) and Part 7.

### Make limits both declared and enforceable

Record request, model-token, tool-call, time, and cost bounds where they apply. For each, name the policy identity and where it is enforced. A field that describes a limit does not stop consumption, and an enforcement point with no declared policy leaves a reviewer unable to judge it. This chapter sets no numeric defaults; the accountable owner sets values and gives the reason.

Use a logical, versioned model policy when the policy choice is more stable than a specific resolution. When reproducibility or a needed feature calls for a fixed resolution, record that identity and its settings. Either way, model output is data: it cannot enlarge the capability list, change a budget, or replace the protected authorization decision.

### Fail closed before accepting work

Construction validation should check the presence and consistency of every field that would otherwise be silently defaulted. Typical failures:

- an owner, governance tier, risk-record identity, output schema, policy, or budget is absent or invalid;
- the governance tier does not match the referenced risk record;
- a named capability cannot resolve to one immutable identity, resolves twice, or is not explicitly admitted;
- the effective execution class is below the enabled capability's floor; or
- an authority-bearing dependency comes from caller data or model output instead of the trusted boundary.

Then construction stops and no work is accepted. Failing closed does not prove the other controls work; it is a visible response to an invalid configuration, and safer than filling a blank with a convenient label.

### Treat the manifest as a binding record, not a trust verdict

The manifest records the resolved model and settings, instruction and output-schema identities, admitted capability membership, source-policy identity, budget policy, execution class, governance and risk references, and a construction identity. Its ID accompanies the relevant evaluation evidence and runtime records. Keep safe identifiers and digests, not raw secrets or hidden reasoning.

An immutable identity or digest binds a reviewer to the recorded configuration. It is not proof of validity, security, truth, permission, or control effectiveness. Software-provenance guidance in SLSA recommends that a verifier check provenance against trusted builder identities and expected values, and it states trust limits too. [3] Apply that narrowly: inspect the manifest, the admission evidence, the output validation, and the Part 3 and Part 4 evidence, rather than treating a manifest ID as a stamp of approval.

### Change what the evidence identifies

If model policy or settings, enabled capability, output contract, or budget policy changes, assign a new agent version and a new effective-configuration identity. An instruction revision also gets its own identity under [2.3](03-prompts-and-instructions.md). Link new evaluation evidence to that identity; do not relabel old evidence as covering new behavior. NIST's Generative AI Profile treats documentation of model details, provenance, assumptions, and limitations as useful context, and asks that performance be shown for conditions similar to deployment and that limits on generalizing beyond them be documented. [4] A changed manifest improves traceability, not fitness for every context.

### A bounded builder workflow

1. **Describe the interface.** Write caller-controlled input, trusted dependencies with provenance, all final outcomes, and caller handling.
2. **State the intended configuration.** Identify owner, version, execution class, risk-record reference, model policy if relevant, output schema, bounds, and the smallest capability declaration.
3. **Make uncertainty explicit.** Leave an unknown owner, budget, governance, or identity field unresolved rather than inventing a default. An unresolved template cannot be constructed.
4. **Validate and resolve.** Check cross-field consistency, resolve named dependencies, and reject unadmitted, duplicate, or incompatible capability resolutions before accepting work.
5. **Record the effective configuration.** On success, create the manifest and attach its ID to evidence and runtime records. On failure, keep the bounded reason and do not invent a manifest.
6. **Hand off the right questions.** Give tool owners the admitted interface list, security owners the trusted-dependency and protected-operation boundary, and evaluators the manifest identity and the changed claim.

## Requirements

- **CONTRACT-01 — Complete interface.** **Applies to every agent.** The agent contract **MUST** declare the accepted input, trusted runtime dependencies and their provenance, schema-validated output, accountable owner, agent version, and permitted terminal outcomes. It **MUST** cover `complete`, `needs_information`, `declined`, and `failed`; any declared partial or escalation outcome **MUST** define its bounded content and caller handling.

- **CONTRACT-02 — Reviewable configuration.** **Applies to every agent construction.** The construction process **MUST** validate the contract before the agent accepts work and **MUST NOT** substitute defaults for missing or invalid owner, execution class, governance tier, risk-record reference, model policy where a model is used, budget, output schema, or enabled capability. The declared governance tier **MUST** match the referenced risk record. Invalid or unresolved declared configuration **MUST** fail closed.

- **CONTRACT-03 — Declared bounds.** **Applies when an agent can invoke a model, skill, retrieval source, tool, or other runtime capability.** The contract **MUST** declare a least-capability allowlist, applicable model policy, and enforceable request, token, tool-call, time, or cost bounds appropriate to the agent. The effective execution class **MUST NOT** be lower than the class required by its enabled capabilities. A bundled, discovered, or model-suggested capability **MUST NOT** become available without explicit admission.

- **CONTRACT-04 — Trusted dependencies.** **Applies when an agent receives identity, tenant, authority, deadline, or policy context.** The contract **MUST** name the trusted source and type for each such dependency. The runtime **MUST NOT** accept model-generated or request-body values as authorization and **MUST NOT** place raw secrets or unsafe live clients in serializable run state. Apply Part 3's canonical authorization rules when resolving or using these dependencies.

- **CONTRACT-05 — Validated outcomes.** **Applies when any output is consumed by a person, workflow, tool, or another agent.** The runtime **MUST** validate the output against the declared contract before downstream use. A proposed action **MUST** remain data until the separately authorized action path accepts it; a model statement that an action succeeded is not evidence of success.

- **CONTRACT-06 — Effective-configuration evidence.** **Applies to every successful agent construction and to each behavior-changing configuration release.** The construction process **MUST** produce a capability manifest with immutable identities or digests for the effective declared configuration, and its ID **MUST** be recorded with relevant evaluation evidence and observable runtime records. A change to model policy or settings, enabled capability, output contract, or budget policy **MUST** change the agent version and receive evaluation appropriate to the change. Instruction changes follow the versioning and evaluation rules in [2.3](03-prompts-and-instructions.md) and **MUST** receive a distinct effective-configuration identity.

## Worked example

The [policy-assistant contract template](../../templates/2.2/policy-assistant-contract.yaml) is a neutral planning record for `POLICY-BUILD-001`, the fictional `internal-policy-assistance` candidate. All identities and values are fictional; nothing here has run.

The job is narrow: answer a policy question from evidence that is both current and permitted for the requester. The candidate declares no write or approval capability. It describes a desired permission-filtered, read-only retrieval capability, but its effective membership stays empty until construction resolves and explicitly admits the required identity. The record uses `ephemeral` as the execution class for this read-only candidate; it does not set a governance tier, budget, owner, or risk record.

Take the fictional requester `employee-uk-104` asking about a London hotel costing GBP 220. The current source is `travel-policy-2026@2026-10-01`; a superseded source says GBP 200. The expected behavior is `complete` only when the protected retrieval boundary makes the permitted current source available and the validated response cites it. "Approved" alone is not enough: an approved source can still be superseded or inaccessible to this requester.

The outcome contract makes the variants clear. If the current permitted source is missing, the outcome is `needs_information`, not a guessed amount. If two equally authoritative current permitted sources conflict with no declared precedence rule, the outcome is also `needs_information` and names the conflict rather than choosing by date. For `contractor-uk-204`, who may not read the policy, the outcome is `declined` without revealing the amount. Retrieval exhaustion or timeout before a supported answer is `failed`. A request to alter a booking is `declined` because no write capability is declared.

If a builder leaves the owner, risk-record identity, model policy, output-schema identity, budget policy, or resolved capability identity as `null`, construction fails closed and no manifest claims success. Once everything is resolved, the manifest records the identities actually used and its ID can be attached to evaluation and runtime records. It still does not show that the source supports the answer or that authorization worked.

## Evidence and checklist

A reviewer should be able to answer six questions from the contract. What task data may a caller supply? Which dependencies are trusted, and from where? What final outcomes can the caller handle? Which capabilities are declared and which are effectively admitted? What stops an invalid assembly from accepting work? Which exact effective configuration does a piece of evidence identify?

Useful evidence: the reviewed contract; validation results for missing, malformed, contradictory, and unadmitted configuration; a resolved capability-membership record; output-validation checks for every final outcome; and manifest-linked evaluation or runtime records. None of these alone proves control effectiveness, source truth, authorization, or release readiness; Part 4 decides what evidence a real decision needs.

Before handing off, ask:

- Does the contract separate caller input from trusted dependencies, naming the provenance and type of each authority-bearing one?
- Can a caller tell `complete`, `needs_information`, `declined`, and `failed` apart, including any declared extension?
- Are required construction fields present and cross-checked, with unresolved values blocking construction rather than getting defaults?
- Is the desired capability list distinct from the resolved, admitted membership, including its execution-class floor?
- Is each declared bound paired with a named enforcement location?
- Does the manifest identify the model policy and settings, instructions, output schema, capability membership, source and budget policy, and construction identity, with no secrets or hidden reasoning?
- Does a material change get a new agent version, a distinct effective identity, and a fresh evaluation handoff rather than inheriting earlier evidence?

## References

[1]: https://doi.org/10.6028/NIST.SP.800-128 "NIST SP 800-128: Guide for Security-Focused Configuration Management of Information Systems"
[2]: https://json-schema.org/draft/2020-12/json-schema-validation "JSON Schema Validation: A Vocabulary for Structural Validation of JSON"
[3]: https://slsa.dev/spec/v1.2/verifying-artifacts "SLSA v1.2 Build: Verifying artifacts"
[4]: https://doi.org/10.6028/NIST.AI.600-1 "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"

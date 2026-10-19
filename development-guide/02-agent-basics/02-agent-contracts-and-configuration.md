# 2.2 Agent Contracts and Configuration

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Agent owners, builders, reviewers, and operators who need a bounded,
inspectable agent configuration.

**Applicability:** Every proposed production agent needs this contract layer. Fields
and controls beyond the common interface apply only when the agent enables the
corresponding model, capability, execution class, or downstream consumer.

**Reader question:** What must be declared before an agent accepts work, how does a
declared configuration become an effective configuration, and what evidence lets a
reviewer identify the configuration behind an outcome?

[Part 2 overview](README.md) · [Applicability and conformance](../../applicability.md) ·
[1.4 Initial Risk, Data, Ownership, and Delivery Plan](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) ·
[2.3 Prompts and Instructions](03-prompts-and-instructions.md) ·
[2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md)

## Purpose and applicability

An **agent contract** is a reviewable declaration of an agent's bounded job,
inputs, dependencies, behavior limits, outcomes, and accountable ownership. It is
not a prompt, an access grant, an approval, or a record that the agent ran. A
well-formed contract lets a caller know how to supply task data and handle each
outcome, while letting a builder know what must be checked before construction.

This matters even for a response-only assistant. Its answer can be incomplete,
misleading, unavailable, or out of scope. When a candidate also uses a model,
retrieval source, skill, tool, or durable execution, the contract makes that
additional surface visible without making it universal. A declared capability is
not automatically enabled; the effective configuration has to resolve and admit
it before it is available.

This chapter owns agent-level configuration and the **capability manifest** that
records its effective form. The initial risk record and delivery ownership begin
in [1.4](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md).
Chapter [2.3](03-prompts-and-instructions.md) owns instruction design and its
change rules. Chapter [2.4](04-tools-and-external-interfaces.md) owns tool
semantics, and [2.6](06-context-and-retrieval-fundamentals.md) owns retrieval
and source-evidence design. Part 3 owns identity, authorization, untrusted
content, and data handling. This contract points to those decisions; it does not
reimplement or weaken them.

## Working model

### Three records, three different jobs

Keep **declared configuration**, **runtime state**, and the **effective capability
manifest** separate.

- **Declared configuration** is the versioned intended design: purpose, accepted
  input, output contract, owner, execution class, governance tier, risk-record
  reference, model policy, allowed capabilities, bounds, and version identities.
  It is the candidate's reviewed starting point.
- **Runtime state** is per-run information: a request identifier, authenticated
  identity and resource scope, deadline, permitted evidence identifiers, usage
  counters, and the terminal outcome. It changes as work proceeds. It must not
  carry raw secrets or unsafe live clients in serializable state.
- **Effective capability manifest** is the immutable record made after successful
  construction. It records what the builder actually resolved from the declared
  configuration, including immutable identities or digests where those are used.

This distinction is a practical adaptation of configuration-baseline thinking:
NIST describes a baseline as reviewed specifications at a point in time and
describes change control and monitoring as separate activities. [1] The proposed
playbook contract does not adopt NIST's process or role structure. It uses the
same useful separation: a changing request must not silently alter the reviewed
configuration, and a configuration edit must not be confused with run state.

A useful construction path is:

```text
declared contract
  → validate required fields and cross-field consistency
  → resolve named model, instructions, schemas, sources, skills, and tools
  → verify explicit admission and execution-class compatibility
  → construct or fail closed
  → emit effective capability manifest when construction succeeds
```

The arrows describe a proposed build discipline, not evidence that a runtime is
secure or operating. A failure before construction is useful information: it
prevents a missing owner, unresolved model policy, absent budget, unknown
capability, or mismatched governance tier from becoming an implicit default.

### Caller fields are not trusted dependencies

Classify every incoming value by its role. A caller can submit a policy question
and an optional response-format preference. A trusted runtime dependency might
instead provide a request identifier, authenticated requester reference,
tenant/resource scope, deadline, or authorization decision. The contract should
name each dependency's type and trusted source, not merely label it "context."

This avoids a confused boundary. A request body or model output may contain a
tenant label or a claimed permission, but it is task data, not authority. The
protected operation must resolve and authorize the relevant trusted context under
Part 3. Similarly, a retrieved source can support a policy fact, yet it does not
become a runtime instruction or grant a new capability. Passing a stable
identifier rather than a credential or a live client into recoverable state keeps
the dependency reference inspectable without treating serialization as a trust
mechanism.

### Outcomes are an interface, not a success-only story

An output contract specifies both its shape and its meanings. Its ordinary
terminal outcome set is `complete`, `needs_information`, `declined`, and
`failed`:

- `complete` contains the bounded answer and the relevant evidence identifiers
  or uncertainty the caller needs.
- `needs_information` says what necessary input or evidence is missing,
  ambiguous, or unresolved and gives a safe next step where applicable.
- `declined` communicates that the request cannot be performed within the
  contract without disclosing protected content or inventing authority.
- `failed` reports a bounded operational failure without turning an unsupported
  answer into a completion.

An optional `partial` or escalation outcome needs equally precise content and
caller handling. It must not be a catch-all for a polished but unsupported answer.
These are agent terminal outcomes, not Part 4 evaluator statuses such as pass,
fail, invalid, or inconclusive.

A schema can help a receiver reject missing fields, unexpected structure, and
out-of-range values. JSON Schema, for example, describes validation as assertions
about the structure of instance data. [2] That useful structural check does not
show that an answer is factually supported, that its citation is authoritative,
that the requester is authorized, or that an external effect occurred. Those are
separate checks at their respective owners.

## Decisions and best practices

### Declare desired capability separately from effective capability

Start from no optional capabilities. State the narrow operation the job needs,
the proposed model policy where a model is used, and the relevant source, skill,
or tool identities. Then distinguish the **desired declaration** from the
**effective membership**. A discovered package, a bundled capability, or a
model-suggested operation remains unavailable until the construction process
explicitly admits it and resolves the expected identity.

The same distinction applies to execution class. A fixed, read-only workflow may
use a model router or a bounded adaptive sequence may choose among a finite,
admitted allowlist; neither arrangement makes the allowlist open-ended. Classify
from the enabled behavior and do not let a later resolution silently lower the
class required by that behavior. Detailed effects, retries, durable handling, and
approval conditions belong to [2.4](04-tools-and-external-interfaces.md) and
Part 7 rather than this contract.

### Make limits both declared and enforceable

Record request, model-token, tool-call, time, and cost bounds only where they
apply to the candidate. For each declared bound, name the policy identity and
the point expected to enforce it. A field that merely describes an intended limit
does not stop consumption; an enforcement point without a declared policy leaves
the reviewer unable to judge what it is enforcing. This chapter deliberately
sets no numerical defaults. The accountable owner must determine values and
rationale for the actual use.

Use a logical, versioned model policy when a policy choice is more stable than a
specific resolution. When reproducibility or a necessary feature calls for a
fixed resolution, record that identity and its relevant settings instead. In
either case, model output remains data. It cannot enlarge the capability list,
change a budget, or substitute for the protected authorization decision.

### Fail closed before accepting work

Construction validation should check the presence and consistency of all fields
that would otherwise be silently defaulted. Typical failure modes include:

- an owner, governance tier, risk-record identity, output schema, policy, or
  budget is absent or invalid;
- the governance tier does not match the referenced risk record;
- a named capability cannot resolve to one immutable identity, resolves twice,
  or is not explicitly admitted;
- the effective execution class is below the enabled capability's floor; or
- an authority-bearing dependency is sourced from caller data or model output
  instead of the declared trusted boundary.

In these cases, construction stops and no work is accepted. A fail-closed result
does not prove that all remaining controls work; it is simply a visible response
to an invalid configuration. It is safer than filling a blank field with a
convenient label and later treating the assembled candidate as reviewed.

### Treat the manifest as a binding record, not a trust verdict

The capability manifest records the resolved model and settings, instruction and
output-schema identities, admitted capability membership, relevant source-policy
identity, budget policy, execution class, governance/risk references, and a
construction identity. Its ID accompanies the relevant evaluation evidence and
observable runtime record. It should retain safe identifiers and digests, not raw
secrets or hidden reasoning.

An immutable identity or digest is valuable because it binds a reviewer to the
recorded configuration. It is not a validity, security, truth, permission, or
control-effectiveness proof. The analogous software-provenance guidance in SLSA
requires a verifier to inspect provenance against trusted identities and expected
values; it also states important trust limits. [3] Apply that lesson narrowly:
inspect the manifest, the admission evidence, the output validation, and the
applicable Part 3/Part 4 evidence rather than treating a manifest ID as a stamp
of approval.

### Change what the evidence identifies

If model policy or settings, enabled capability, output contract, or budget
policy changes, assign a new agent version and a new effective-configuration
identity. An instruction revision likewise receives a distinct identity under
[2.3](03-prompts-and-instructions.md). Link relevant new evaluation evidence to
that effective identity; do not relabel old evidence as if it covered the new
behavior. NIST's Generative AI Profile similarly treats documentation of model
details, provenance, assumptions, and limitations as useful context and warns
that tests can be mismatched to their deployment context. [4] A changed manifest
therefore improves traceability, not a claim that a new configuration is fit for
every context.

### A bounded builder workflow

1. **Describe the interface.** Write caller-controlled input, trusted runtime
   dependencies with provenance, all terminal outcomes, and caller handling.
2. **State the intended configuration.** Identify owner, version, execution
   class, risk-record reference, model policy if relevant, output schema, bounds,
   and the smallest proposed capability declaration.
3. **Make uncertainty explicit.** Leave unknown owner, budget, governance, or
   identity fields unresolved rather than assigning an invented default. An
   unresolved template is not eligible for construction.
4. **Validate and resolve.** Check cross-field consistency; resolve named
   dependencies; reject unadmitted, duplicate, or incompatible capability
   resolutions before accepting work.
5. **Record the effective configuration.** If construction succeeds, create the
   manifest and attach its ID to the relevant evidence and observable runtime
   records. If it does not, retain the bounded failure reason without inventing a
   manifest for a candidate that was never constructed.
6. **Hand off the right questions.** Give tool owners the admitted interface list,
   security owners the trusted dependency/protected-operation boundary, and
   evaluators the manifest identity plus the changed claim. Do not call this handoff
   an approval or deployment decision.

## Requirements

- **CONTRACT-01 — Complete interface.** **Applies to every agent.** The agent contract **MUST** declare the accepted input, trusted runtime dependencies and their provenance, schema-validated output, accountable owner, agent version, and permitted terminal outcomes. It **MUST** cover `complete`, `needs_information`, `declined`, and `failed`; any declared partial or escalation outcome **MUST** define its bounded content and caller handling.

- **CONTRACT-02 — Reviewable configuration.** **Applies to every agent construction.** The construction process **MUST** validate the contract before the agent accepts work and **MUST NOT** substitute defaults for missing or invalid owner, execution class, governance tier, risk-record reference, model policy where a model is used, budget, output schema, or enabled capability. The declared governance tier **MUST** match the referenced risk record. Invalid or unresolved declared configuration **MUST** fail closed.

- **CONTRACT-03 — Declared bounds.** **Applies when an agent can invoke a model, skill, retrieval source, tool, or other runtime capability.** The contract **MUST** declare a least-capability allowlist, applicable model policy, and enforceable request, token, tool-call, time, or cost bounds appropriate to the agent. The effective execution class **MUST NOT** be lower than the class required by its enabled capabilities. A bundled, discovered, or model-suggested capability **MUST NOT** become available without explicit admission.

- **CONTRACT-04 — Trusted dependencies.** **Applies when an agent receives identity, tenant, authority, deadline, or policy context.** The contract **MUST** name the trusted source and type for each such dependency. The runtime **MUST NOT** accept model-generated or request-body values as authorization and **MUST NOT** place raw secrets or unsafe live clients in serializable run state. Apply Part 3's canonical authorization rules when resolving or using these dependencies.

- **CONTRACT-05 — Validated outcomes.** **Applies when any output is consumed by a person, workflow, tool, or another agent.** The runtime **MUST** validate the output against the declared contract before downstream use. A proposed action **MUST** remain data until the separately authorized action path accepts it; a model statement that an action succeeded is not evidence of success.

- **CONTRACT-06 — Effective-configuration evidence.** **Applies to every successful agent construction and to each behavior-changing configuration release.** The construction process **MUST** produce a capability manifest with immutable identities or digests for the effective declared configuration, and its ID **MUST** be recorded with relevant evaluation evidence and observable runtime records. A change to model policy or settings, enabled capability, output contract, or budget policy **MUST** change the agent version and receive evaluation appropriate to the change. Instruction changes follow the versioning and evaluation rules in [2.3](03-prompts-and-instructions.md) and **MUST** receive a distinct effective-configuration identity.

## Worked example

The accompanying [policy-assistant contract template](../../templates/2.2/policy-assistant-contract.yaml)
is a neutral planning/build record for `POLICY-BUILD-001`, the fictional
`internal-policy-assistance` candidate. Its status is
`illustrative-unexecuted`: it does not create an owner, admit a capability, run a
model, construct a runtime, or claim approval, deployment, or evaluation.

The proposed job is narrow: answer a policy question from evidence that is both
current and permitted for the requester. The candidate declares no external
write or approval capability. It describes a desired permission-filtered,
read-only retrieval capability, but its effective membership remains empty until
construction resolves and explicitly admits the required identity. The record
uses `ephemeral` as the illustrative class for this read-only candidate; it does
not determine a governance tier, budget, owner, or risk record.

Consider the fictional requester `employee-uk-104` asking about a London hotel
costing GBP 220. The controlled fixture's current source is
`travel-policy-2026@2026-10-01`; a different, superseded source says GBP 200.
The expected unexecuted behavior is `complete` only when the protected retrieval
boundary makes the permitted current source available and the validated response
cites it. "Approved" alone is insufficient: an approved source can still be
superseded or inaccessible to this requester.

The outcome contract makes altered cases intelligible. If the current permitted
source is missing, the expected outcome is `needs_information`, not a guessed
amount. If two equally authoritative current, permitted sources conflict without
a declared precedence rule, the expected outcome is also `needs_information` and
identifies the conflict rather than choosing by date. For
`contractor-uk-204`, who is not permitted to read the policy, the expected result
is `declined` without revealing the amount. A controlled retrieval exhaustion or
timeout before a supported answer maps to `failed`. A request to alter a booking
is also `declined` because no write capability is declared.

Suppose a builder fills the template but leaves the owner, risk-record identity,
model policy, output-schema identity, budget policy, or resolved capability
identity as `null`. Construction fails closed; a manifest must not claim a
successful effective configuration. If all required information is later
resolved, the resulting manifest records the configuration bytes or immutable
identities actually used. The manifest ID can then be attached to relevant
evaluation records and observable runtime records. It still does not establish
that the source supports the answer, that authorization operated correctly, or
that an unexecuted fixture was observed.

## Evidence and checklist

A reviewer should be able to inspect a proposed contract and answer six practical
questions: What task data may a caller supply? Which dependencies are trusted and
where do they come from? What terminal outcomes can the caller handle? Which
capabilities are declared versus effectively admitted? What prevents an invalid
assembly from accepting work? Which exact effective configuration does a piece of
evidence identify?

Useful observable evidence includes the reviewed contract; validation results for
missing, malformed, contradictory, and unadmitted configuration; a resolved
capability-membership record; output-validation checks for every declared terminal
outcome; and manifest-linked evaluation or runtime records when those activities
occur. None of these artifacts by itself proves control effectiveness, source
truth, authorization, or release readiness. Part 4 determines what evidence is
needed for an actual decision.

Before handing a proposed configuration to the next reviewer, ask:

- Does the contract separate caller input from trusted dependencies and name the
  provenance and type of each authority-bearing dependency?
- Can a caller distinguish `complete`, `needs_information`, `declined`, and
  `failed`, including safe handling of any declared extension?
- Are all required construction fields present and cross-checked, with unresolved
  values blocking construction rather than receiving defaults?
- Does the desired capability list remain distinct from the resolved, explicitly
  admitted effective membership, including its execution-class floor?
- Are declared bounds paired with an identified enforcement location rather than
  presented as prose alone?
- Does the manifest identify the effective model policy/settings, instructions,
  output schema, capability membership, source/budget policy, and construction
  identity without storing secrets or raw hidden reasoning?
- Does a material configuration change receive a new agent version, distinct
  effective identity, and relevant evaluation handoff rather than inheriting an
  earlier candidate's evidence?

## References

[1]: https://doi.org/10.6028/NIST.SP.800-128 "NIST SP 800-128: Guide for Security-Focused Configuration Management of Information Systems"
[2]: https://json-schema.org/draft/2020-12/json-schema-validation "JSON Schema Validation: A Vocabulary for Structural Validation of JSON"
[3]: https://slsa.dev/spec/v1.2/verifying-artifacts "SLSA v1.2: Verifying Artifacts"
[4]: https://doi.org/10.6028/NIST.AI.600-1 "NIST AI 600-1: Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"

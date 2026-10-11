# 12. Implementation patterns

This chapter extends the Agent Playbook's
[implementation patterns](../agent-playbook/12-implementation-patterns.md) with
a governed system package. It explains how the parts of a conforming
multi-agent system fit together and the order in which they are validated. It
deliberately prescribes no language, SDK, or runtime; teams adapt the patterns
to the pinned versions of whatever agent runtime and durable execution engine
they adopt.

## Package

A governed system package keeps member agents, the system composition, durable
coordination, runtime services, and deterministic policy in clearly separated
areas:

```text
<organization package>/
├── agents/
│   ├── resolution-coordinator/       # each with its own Agent Spec
│   ├── customer-investigator/
│   ├── policy-reviewer/
│   └── customer-action-executor/
├── systems/
│   └── customer-resolution/
│       ├── system spec
│       ├── factory                   # assembles the system from resolved specs
│       ├── typed contracts           # interaction, state, and outcome types
│       ├── coordination              # deterministic state machine and routing
│       └── policies/
│           ├── delegation policy
│           ├── data-flow policy
│           └── termination policy
├── workflows/
│   └── customer-resolution workflow
├── durable-steps/
│   ├── member agent runs
│   ├── registry admission evidence
│   └── customer actions
├── runtime/
│   ├── manifests
│   ├── registries
│   └── worker
└── policy/
    ├── authorization
    ├── budgets
    └── approval
```

Member agents keep the package structure the Agent Playbook requires. The
system package references them by pinned version or manifest; it never copies
their instructions, tools, or specs into the composition.

## Typed system metadata and contracts

The System Spec is parsed into schema-validated types before anything else
happens. System metadata covers the contract version, owners, version,
execution class (`ephemeral`, `durable`, or `human_governed`), governance tier
(`low`, `medium`, `high`, or `critical`), risk assessment, threat model,
evaluation policy, data classification, whether durable execution is enabled,
and any approval policy. System limits are positive, finite values for agent
runs, delegation depth, parallel agents, rounds, model requests, tool calls,
input and output tokens, cost, and deadline.

Member, role, interaction, topology, state, and termination sections are
validated by their own typed contracts. Topology-specific fields are modeled as
a discriminated union keyed by the topology type rather than one loose mapping
with many optional keys.

Every interaction has concrete input and output types. A shared envelope, such
as the delegation and result envelopes in
[chapter 5](05-delegation-and-interactions.md), carries identity, authority,
budget, and outcome fields, but it never replaces edge-specific schema
validation of the payload.

## Factory flow

The system factory turns a reviewed System Spec into a runnable system, in
this order:

1. Load the System Spec and validate its metadata.
2. Resolve the system's delegation, data-flow, termination, approval, and
   budget policies from the policy registry.
3. For each member, resolve the pinned agent manifest from the agent registry,
   verify that it conforms and is compatible with the system's execution class
   and governance tier, and build a member restricted to the intersection of
   its own allowlists and the system's restrictions.
4. Build the directed interaction graph and validate it against members,
   policies, and limits.
5. Verify the effective execution class and governance-tier floors.
6. Verify that the risk-assessment and evaluation references resolve.
7. Produce the immutable composition manifest, including the worker build.

Registries resolve only reviewed and permitted artifacts. Construction performs
no model or external-service I/O and fails closed on any inconsistency.

## Deterministic policy boundary

Every proposed delegation passes through one deterministic authorization
function before dispatch. It requires that the requested edge exists for the
named interaction, caller, and callee; validates the input against the edge's
input contract; and computes effective scopes as the intersection of the edge
maximum, the caller's delegable scopes, the callee's maximum, the authenticated
actor's scopes, and the scopes allowed by current workflow state. If the edge's
minimum required scopes are not contained in that intersection, the delegation
is denied. Only then does it reserve the edge's budget grant under the stable
delegation ID and return an authorized delegation carrying the effective scopes
and grant.

The complete policy also checks tenant, purpose, data classification, graph
version, member health, deadline, depth, concurrency, approval, and kill-switch
state.

## Durable workflow

The system workflow is a deterministic loop over typed state:

1. Load a replay-safe runtime from the recorded composition manifest.
2. Initialize state from the request.
3. Until state is terminal, compute the next deterministic step.
4. If the step needs an agent, authorize the delegation, run the member as a
   durable step with the interaction's timeout and retry options, and accept
   the validated result into state.
5. Otherwise, apply the deterministic transition directly.
6. After every step, evaluate the termination policy.
7. Return the typed outcome.

Loading the replay-safe runtime uses only the recorded manifest and
workflow-safe policy data. It does not query mutable registries or read
deployment configuration.

In a model-routed system, a coordinator durable step returns a typed route
proposal. The workflow validates it and dispatches the selected member; the
coordinator does not directly invoke undeclared agents.

## Dynamic admission

Admitting a member during a run is split between a durable step and the
workflow. The durable step authenticates the registry and gathers current
candidate evidence. The workflow then evaluates a deterministic admission
policy over that recorded evidence, the current graph, the remaining limits,
and the admission policy version. If the candidate is admitted, the workflow
adds the member and its edges and records the run-manifest update.

Because the decision is made from the recorded result, it is replay-safe. A
model may propose a capability need or candidate name but cannot perform
admission.

## Fan-out and gather

Fan-out authorizes every branch in a deterministic branch order before any
branch runs, then runs the authorized branches concurrently as durable steps,
capturing failures as values rather than aborting the gather. Results are
normalized in branch order and accepted under the declared aggregation policy.

Workflow code uses only the concurrency primitives the durable execution engine
guarantees to be replay-safe, with engine behavior pinned. Logical branch
order, not completion order, governs aggregation.

## Human-governed action

```text
members produce evidence and a typed action proposal
        ↓
deterministic policy verifies graph, authority, evidence, and limits
        ↓
workflow records action hash, causal references, and composition manifest
        ↓
authenticated approver reviews final action and material dissent
        ↓
workflow verifies actor, tenant, scope, policy, expiry, hash, and manifest
        ↓
executor durable step performs the exact action with approval and idempotency IDs
        ↓
workflow records result, usage, audit evidence, and compensation obligation
```

## Composition manifest

The composition manifest is a typed record containing the manifest ID, system
name and version, contract version, spec digest, execution class, governance
tier, risk-assessment digest, topology, resolved member and interaction
manifests, policy and schema digests, resolved limits, evaluation-policy
digest, and worker build ID.

Compute the manifest ID from a canonical serialization of the resolved fields.
A dynamic run manifest references the base composition manifest and appends
admission and graph-version records.

## Validation order

Validation proceeds from the cheapest, most deterministic checks to the most
expensive, integrated evidence. A later stage never compensates for a failed
earlier stage:

1. Schema validation of the System Spec, policies, and templates.
2. Semantic validation of topology, membership, pinned versions, execution and
   governance floors, policies, and limits.
3. Resolution and conformance of every referenced member contract.
4. Graph construction, schema compatibility for every edge, authority
   attenuation, and combined worst-case budget bounds.
5. Cross-artifact consistency between the System Spec, composition manifest,
   risk assessment, threat model, and evaluation policy.
6. Deterministic policy, interaction, and workflow tests, including replay of
   captured histories.
7. Composition-level evaluations against the admission baseline, with
   provenance.
8. Release checks of the evaluation report against the release policy and the
   approved baseline.

## Local development

Provide:

- A development durable execution environment
- Mock and sandbox member agents, registries, tools, and external services
- Non-production credentials and strict spend limits
- Deterministic model and member doubles for workflow tests
- Failure-injection controls for members, queues, events, and stores
- OpenTelemetry collection and graph-aware trace inspection
- Fast member, interaction, and system smoke evals

Tooling SHOULD let a developer validate the system package, render its
interaction graph, run system evals, and check a release report against the
release policy and baseline without deploying.

## Initial adoption path

1. Inventory existing members, owners, tools, identities, data, and side effects.
2. Draw the actual interaction and trust graph.
3. Run the admission test against a simpler baseline.
4. Create valid Agent Specs and assessments for every member.
5. Introduce the System Spec, typed envelopes, and deterministic policies.
6. Move long-running and state-changing coordination behind a durable execution
   engine.
7. Add root budgets, capacity limits, termination, and correlated telemetry.
8. Add interaction, topology, adversarial, durability, and ablation evals.
9. Complete the system risk assessment and production-readiness checklist.
10. Start with static membership; enable evaluated dynamic mechanisms where
    their measured benefit justifies the added control surface.

For one opinionated, zero-trust implementation of these patterns, see [Zetra](https://github.com/X-McKay/zetra).

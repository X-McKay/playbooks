# 3. System contract

This chapter describes the package you write to define a multi-agent system:
a declarative System Spec, typed interaction contracts, deterministic
coordination and policy code, and a controlled assembly function (the
factory). Every production multi-agent system has one. It is the system-level
counterpart of the
[agent contract](../agent-playbook/03-agent-contract.md), and it references
member Agent Specs rather than repeating them.

## System Spec

The System Spec is the canonical artifact. The sections after the example
explain each part.

```yaml
name: customer-resolution-system
description: Investigate support cases and propose policy-compliant resolutions.

metadata:
  contract_version: 1
  owner: customer-platform
  operational_owner: customer-operations
  version: 1.0.0
  execution_class: human_governed
  governance_tier: high
  risk_assessment: docs/risk-assessments/customer-resolution-system.yaml
  threat_model: docs/threat-models/customer-resolution-system.md
  evaluation_policy: evals/systems/customer_resolution_system/release-policy.yaml
  data_classification: confidential
  durable_execution_enabled: true
  approval_policy: policy/approvals/customer-resolution.yaml

justification:
  claimed_benefits:
    - Isolate read-only investigation from consequential customer actions.
    - Add independent policy review before presenting a resolution.
  baseline: single-agent-customer-resolution-v2
  success_measures:
    - lower_policy_violation_rate
    - no_cross_tenant_access

topology:
  type: supervisor_worker
  orchestrator: customer-resolution-workflow
  coordinator: resolution-coordinator
  dynamic_membership: false
  recursive_delegation: false

members:
  - agent: resolution-coordinator
    version: 1.2.0
    role: coordinator
    required: true
  - agent: customer-investigator
    version: 2.1.0
    role: investigator
    required: true
  - agent: policy-reviewer
    version: 1.4.0
    role: reviewer
    required: true
  - agent: customer-action-executor
    version: 1.1.0
    role: executor
    required: true

interactions:
  - id: investigate-case
    from: resolution-coordinator
    to: customer-investigator
    mode: delegate
    input_schema: CustomerInvestigationRequest
    output_schema: CustomerInvestigationResult
    policy: policies/delegation.yaml#investigate-case
    max_calls: 2
    timeout_seconds: 60
  - id: review-resolution
    from: resolution-coordinator
    to: policy-reviewer
    mode: review
    input_schema: ResolutionProposal
    output_schema: PolicyReview
    policy: policies/delegation.yaml#review-resolution
    max_calls: 1
    timeout_seconds: 45
  - id: execute-approved-action
    from: customer-resolution-workflow
    to: customer-action-executor
    mode: dispatch
    input_schema: ApprovedCustomerAction
    output_schema: CustomerActionResult
    policy: policies/delegation.yaml#execute-approved-action
    max_calls: 1
    timeout_seconds: 30

limits:
  max_agent_runs: 6
  max_delegation_depth: 2
  max_parallel_agents: 3
  max_rounds: 3
  max_model_requests: 20
  max_tool_calls: 30
  max_input_tokens: 80000
  max_output_tokens: 12000
  max_cost_usd: 2.00
  deadline_seconds: 180

state:
  owner: customer-resolution-workflow
  shared_memory: none
  artifact_policy: policies/data-flow.yaml

termination:
  policy: policies/termination.yaml
  success_states:
    - resolved
    - approved_action_completed
  escalation_state: escalated_to_human
```

Organization-specific fields MAY extend the spec under `metadata` or a
versioned extension namespace. They MUST be validated at construction and
MUST NOT change the meaning of standard fields.

## Identity and versioning

Each member already keeps its own versions, as the Agent Playbook's
[agent contract](../agent-playbook/03-agent-contract.md) describes. A system
adds layers on top. Keep these separate:

- `contract_version`: System Spec schema and semantics.
- System version: membership, topology, policies, schemas, and behavior.
- Member agent version: each agent's independent contract and capabilities.
- Workflow and worker build: durable replay and deployment compatibility.
- Composition manifest ID: exact resolved release contents.

Changes to membership, roles, interaction edges, schemas, routing,
aggregation, state ownership, limits, or termination require a system version
change and relevant evals. Changes incompatible with in-flight workflow
histories also require replay-safe deployment.

Production System Specs MUST pin acceptable member versions or immutable
agent manifest IDs. Floating references such as `latest` are prohibited: a
member upgrade would silently change your system.

## Justification

The `justification` section records the result of the
[admission test](01-principles-and-scope.md#do-you-need-more-than-one-agent).
It MUST state:

- the limitation of the simpler baseline;
- the claimed benefit of composition;
- the baseline identifier and evidence location;
- metrics or hard gates that can falsify the claim; and
- the owner and review date for the architectural decision.

If the system fails to outperform the baseline on the claimed dimensions,
that SHOULD trigger simplification or a documented exception. A quality gain
does not excuse a hard gate, security, latency, reliability, or cost failure.

## Topology

The topology declares:

- a supported profile (see
  [chapter 2](02-reference-architecture.md#topology-profiles));
- the deterministic orchestrator;
- any model-driven coordinator;
- whether membership can change during a run;
- whether a member may delegate recursively;
- the aggregation and conflict policy, when the profile needs one; and
- registry, admission, allocation, and graph-construction policy for dynamic
  profiles.

The orchestrator MUST be deterministic code. A coordinator MAY propose routes
within the declared graph, but it cannot create an edge, admit a member,
expand authority, change policy, approve a consequential action, or waive
termination limits.

In a dynamic profile, the declared graph MAY be a run-specific subgraph of a
reviewed policy envelope rather than a graph fully enumerated at deployment.
Deterministic admission policy validates every member and edge before use,
and the resulting graph is recorded in the run manifest.

## Members

Each member entry assigns a system role to an existing Agent Spec. It may add
system-local restrictions but MUST NOT expand the agent's base capabilities.
A member entry SHOULD support:

```yaml
- agent: customer-investigator
  version: 2.1.0
  manifest_id: optional-immutable-agent-manifest
  role: investigator
  required: true
  restrictions:
    toolsets:
      include: [customer-records-read]
    skills:
      include: [customer-investigation]
    data_classification_max: confidential
    authorization_scopes_max: [customers.read]
```

At construction, restrictions are intersected with the member's own
allowlists and the runtime authorization context.

## Interactions

Every permitted directed edge is declared. An interaction includes:

- stable ID, caller, callee, and mode;
- typed input and output schema identifiers;
- delegation, authority, and data-flow policy reference;
- call, timeout, retry, and output bounds;
- failure, cancellation, and fallback behavior; and
- telemetry and audit requirements.

An undeclared edge MUST fail before the callee runs. Schema or policy
resolution failure MUST fail system construction.

Agent-to-agent edges and orchestrator-to-agent dispatches share the same
typed boundary requirements. An orchestrator is not an agent: declare it as a
trusted deterministic principal rather than giving it a fictional Agent Spec.
[Chapter 5](05-delegation-and-interactions.md) defines the envelopes that
travel across each edge.

## Limits

The System Spec declares a root budget for the entire system run. Member and
interaction limits are subdivisions of the root budget, not additional spend
(the same idea as the Agent Playbook's
[budget hierarchy](../agent-playbook/09-cost-optimization.md#budget-hierarchy),
one level up).

At minimum, bound agent runs, delegation depth, parallel agents, coordination
rounds, model requests, tool calls, input and output tokens, cost, and
wall-clock duration.

Systems using recursion or fan-out MUST calculate and test a combined
worst-case upper bound that includes retries. The runtime reserves budget
before dispatch and reconciles consumption after completion.

## State and termination

The contract names the owner and policy for workflow state, artifacts, shared
memory, accepted evidence, conflicts, and final outcomes.

Termination policy MUST define:

- success, escalation, rejection, cancellation, and failure states;
- maximum rounds and no-progress detection;
- behavior when required and optional members fail;
- behavior at budget or deadline exhaustion;
- handling of late, duplicate, or conflicting results;
- cancellation propagation and compensation; and
- which final states permit an external side effect.

A coordinator output is a proposal until deterministic code validates it and
commits the corresponding state transition.

## Factory responsibilities

Each member is still assembled by its own agent factory, as the
[agent contract](../agent-playbook/03-agent-contract.md) requires. The system
factory sits above them and:

1. Loads and validates the System Spec.
2. Resolves the system risk assessment, threat model, eval policy, and
   policies.
3. Resolves every pinned member Agent Spec and manifest.
4. Verifies member conformance and role restrictions.
5. Builds and validates the directed interaction graph.
6. Verifies schema compatibility for every edge.
7. Computes effective execution class and governance-tier floors.
8. Verifies authority attenuation and data-flow constraints.
9. Validates combined budget, retry, concurrency, and termination bounds.
10. Attaches durable execution, observability, audit, budget, and policy
    services.
11. Produces the immutable composition manifest.

Construction MUST fail closed on a missing member, version mismatch,
undeclared or invalid edge, policy error, schema incompatibility,
insufficient execution class or governance tier, unbounded cycle, missing
approval path, or incomplete required evidence.

## Cross-artifact consistency

The System Spec, composition manifest, risk assessment, threat model, eval
policy, deployment, and production telemetry MUST agree on:

```text
system name and version
member agents and versions
topology and policies
execution class and governance tier
risk-assessment version or digest
budget policy
workflow and worker version
```

## Common pitfalls

- **Copying member contracts into the System Spec.** The copies drift, and
  nobody knows which one is enforced.
- **Floating member versions.** A member's routine release changed the
  system's behavior without a system version or eval.
- **Budgets that add up instead of dividing.** Each interaction had its own
  allowance on top of the root budget, so the real ceiling was unknown.

## Before you move on

- [ ] The System Spec validates and every member is pinned.
- [ ] The justification names a baseline and a claim that can be falsified.
- [ ] Every edge is declared with schemas, policy, and bounds.
- [ ] The root budget has a tested worst-case bound including retries.
- [ ] Termination policy covers every final state and which allow side
  effects.

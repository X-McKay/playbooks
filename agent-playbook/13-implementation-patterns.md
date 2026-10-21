# 13. Implementation patterns

This chapter is for developers assembling a conforming agent. It shows how
the standards in this playbook fit together: package layout, the order in
which to validate and build the agent, and the evidence to attach to a
change. It describes structure and order, not a particular framework or
language: adapt each pattern to the pinned versions of the agent framework,
durable execution engine, and telemetry libraries you use.

## Agent package

Start from the [repository structure](02-reference-architecture.md#repository-structure):
keep each agent's declaration, typed contracts, and assembly logic together,
and put shared capabilities and policy in clearly owned locations. Within that
structure, the patterns below rely on a few parts the tree leaves implicit:

- **Tool packages** separate their typed domain inputs and results, their
  policy (effect, retry safety, and scopes), the client for the external
  system, the agent-facing tool adapters, and the toolset that registers them
  under a stable ID.
- **The runtime** holds worker registration and the registries of approved
  models, skills, tools, and policies.
- **The policy area** holds typed governance metadata, execution-class rules,
  and approval policies.

## Governance metadata

Treat the `metadata` block of the Agent Spec as a typed contract in its own
right. It carries the contract version, owner, agent version, execution class,
governance tier, risk-assessment reference, data classification, model policy,
enabled skills, enabled toolsets, and budgets.

Make it strict: every field is required, enumerated values are closed sets
(`ephemeral`, `durable`, `human_governed`; `low`, `medium`, `high`,
`critical`), and every budget is a positive bound. Validating this block is
the first thing the factory does after loading the specification, and a
validation failure stops construction.

## Factory flow and order of validation

The factory turns a reviewed declaration into a running agent. Run its steps
in a fixed order so that the cheapest and most fundamental checks fail first
and no capability is attached before it has been authorized:

1. **Load the Agent Spec** from packaged resources, not from the working
   directory.
2. **Validate governance metadata** against its typed contract.
3. **Resolve the model policy** through the model registry to an approved
   provider, model, settings, and pricing version.
4. **Resolve skills** through the skill registry, admitting only allowlisted
   names.
5. **Resolve toolsets** through the tool registry, passing the declared
   execution class so that any tool whose effect requires a stronger class is
   rejected.
6. **Attach runtime controls**: usage limits, shared spend limits, and
   observability.
7. **Attach durability** when the execution class is `durable` or
   `human_governed`; construction fails if durability is unavailable.
8. **Require an approval policy** when the execution class is
   `human_governed`; construction fails if none is registered for the agent.
9. **Load the risk assessment** and validate the whole contract together: the
   Agent Spec governance tier matches the assessment, mandatory floors are
   met, and every enabled capability is consistent with the execution class.
10. **Construct the agent** with its dependency type, output type, toolsets,
    and capabilities, and emit the capability manifest.

Treat the registries as policy boundaries. They resolve only reviewed models,
skills, tools, and approval policies, which also makes startup validation
deterministic: the same declaration and registries always produce the same
manifest or the same failure.

## Durable workflow

For durable and human-governed agents, make the workflow the entry point. It
converts the workflow input into typed dependencies, runs the agent, and
returns the validated output; model calls and tool I/O happen in durable steps
beneath it.

The worker process registers the workflow, its durable steps, and whatever
integration the agent framework provides for the durable execution engine.
Callers such as an API start the workflow or send it external events. They do
not call the durable agent directly, because a direct call bypasses the
durability, replay, and approval guarantees.

## Human-governed action

A consequential action passes through deterministic policy and a bound
approval before it runs (see
[human approval](09-durable-execution.md#human-approval)):

```text
agent proposes typed action
        ↓
deterministic policy requires approval
        ↓
workflow records canonical action hash
        ↓
authenticated approver sends an external event
        ↓
workflow verifies scope, expiry, and hash
        ↓
durable step performs action with approval ID and idempotency key
        ↓
audit record captures result
```

## Local development

The local environment
SHOULD provide:

- a local development instance of the durable execution engine;
- mock or sandbox external services;
- non-production model credentials and spend limits;
- an OpenTelemetry collector or a development telemetry backend; and
- fast smoke evals.

Expose a single, documented entry point that runs the same validation locally
and in continuous integration. In order, it validates Agent Specs and
governance metadata, validates skills, validates risk assessments, runs the
relevant eval suites, and checks the resulting eval report against the
release policy and the stored baseline.

## Pull-request evidence

A behavioral
pull request SHOULD include:

```text
agent and capability versions changed
reason for the change
affected execution classes, governance tiers, and risk scenarios
eval suites run
before/after quality, latency, and cost
workflow replay result, when applicable
rollout and rollback plan
```

## Common pitfalls

- **Attaching tools before validating.** A capability attached ahead of the
  governance checks can run before anyone decides it should.
- **Loading the spec from the working directory.** The agent that runs is no
  longer the one that was reviewed.
- **Calling a durable agent directly.** It works in a test and silently skips
  durability, replay, and approval in production.

## Adopting the patterns

The [operating model](../foundations/04-operating-model.md#bringing-existing-agents-into-conformance)
describes how to bring existing agents into conformance step by step and how
to stage adoption on evidence.

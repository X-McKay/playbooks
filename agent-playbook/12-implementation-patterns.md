# 12. Implementation patterns

This chapter shows how the standards in this playbook fit together in a working system. It describes structure and order, not a particular framework or language: adapt each pattern to the pinned versions of the agent framework, durable execution engine, and telemetry libraries a project uses.

## Agent package

A conforming project keeps each agent's declaration, typed contracts, and assembly logic together, and keeps shared capabilities and policy in clearly owned locations:

```text
<package>/
├── agents/
│   └── customer-support/
│       ├── agent.yaml               # Declarative Agent Spec
│       ├── factory                  # Controlled assembly
│       ├── dependencies             # Typed runtime context
│       ├── types                    # Typed inputs and outputs
│       └── instructions/
├── skills/
│   └── customer-policy/
│       └── SKILL.md
├── tools/
│   └── customer-records/
│       ├── types                    # Typed domain inputs and results
│       ├── policy                   # Tool effect, retry safety, scopes
│       ├── service                  # Client for the external system
│       ├── tools                    # Agent-facing tool adapters
│       └── toolset                  # Registration under a stable ID
├── workflows/
│   └── support                      # Deterministic orchestration
├── runtime/
│   ├── worker                       # Worker process registration
│   └── registries                   # Approved models, skills, tools, policies
└── policy/
    ├── agent-metadata               # Typed governance metadata
    ├── execution                    # Execution-class rules
    └── approval                     # Approval policies
```

## Governance metadata

The `metadata` block of the Agent Spec is a typed contract in its own right. It carries the contract version, owner, agent version, execution class, governance tier, risk-assessment reference, data classification, model policy, enabled skills, enabled toolsets, and budgets. Every field is required, enumerated values are closed sets (`ephemeral`, `durable`, `human_governed`; `low`, `medium`, `high`, `critical`), and every budget is a positive bound. Validating this block is the first thing the factory does after loading the specification, and a validation failure stops construction.

## Factory flow and order of validation

The factory turns a reviewed declaration into a running agent. It performs its steps in a fixed order so that the cheapest and most fundamental checks fail first and no capability is attached before it has been authorized:

1. **Load the Agent Spec** from packaged resources, not from the working directory.
2. **Validate governance metadata** against its typed contract.
3. **Resolve the model policy** through the model registry to an approved provider, model, settings, and pricing version.
4. **Resolve skills** through the skill registry, admitting only allowlisted names.
5. **Resolve toolsets** through the tool registry, passing the declared execution class so that any tool whose effect requires a stronger class is rejected.
6. **Attach runtime controls**: usage limits, shared spend limits, and observability.
7. **Attach durability** when the execution class is `durable` or `human_governed`; construction fails if durability is unavailable.
8. **Require an approval policy** when the execution class is `human_governed`; construction fails if none is registered for the agent.
9. **Load the risk assessment** and validate the whole contract together: the Agent Spec governance tier matches the assessment, mandatory floors are met, and every enabled capability is consistent with the execution class.
10. **Construct the agent** with its dependency type, output type, toolsets, and capabilities, and emit the capability manifest.

The registries are policy boundaries. They resolve only reviewed models, skills, tools, and approval policies, which also makes startup validation deterministic: the same declaration and registries always produce the same manifest or the same failure.

## Durable workflow

For durable and human-governed agents, the workflow is the entry point. It converts the workflow input into typed dependencies, runs the agent, and returns the validated output; model calls and tool I/O happen in durable steps beneath it.

The worker process registers the workflow, its durable steps, and whatever integration the agent framework provides for the durable execution engine. Callers such as an API start the workflow or send it external events; they do not call the durable agent directly, because a direct call bypasses the durability, replay, and approval guarantees.

## Human-governed action

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

The local environment SHOULD provide:

- A local development instance of the durable execution engine
- Mock or sandbox external services
- Non-production model credentials and spend limits
- An OpenTelemetry collector or a development telemetry backend
- Fast smoke evals

A project typically exposes a single, documented entry point that runs the same validation locally and in continuous integration. In order, it validates Agent Specs and governance metadata, validates skills, validates risk assessments, runs the relevant eval suites, and checks the resulting eval report against the release policy and the stored baseline.

## Pull-request evidence

A behavioral pull request SHOULD include:

```text
agent and capability versions changed
reason for the change
affected execution classes, governance tiers, and risk scenarios
eval suites run
before/after quality, latency, and cost
workflow replay result, when applicable
rollout and rollback plan
```

## Initial adoption path

Teams adopting the playbook incrementally should:

1. Inventory agents, owners, tools, side effects, and credentials.
2. Assign execution classes and complete scenario-based risk assessments.
3. Introduce typed inputs, outputs, and tool contracts.
4. Move state-changing agents onto a durable execution engine.
5. Add hard budgets and correlated telemetry.
6. Establish smoke, regression, safety, and trajectory evals.
7. Add human approval to consequential actions.
8. Complete the production-readiness checklist.

For one opinionated, zero-trust implementation of this playbook, see [Zetra](https://github.com/X-McKay/zetra).

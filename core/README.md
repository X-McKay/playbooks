# Core concepts

- **Status:** Draft
- **Version:** 0.4
- **Last updated:** 2026-10-12

This is the first of the playbook's three sections. It covers what every
production agent needs before it ships: deciding whether an agent is worth
building, defining the problem, designing the agent as a zero-trust workload,
and then building, evaluating, observing, and launching it. Each chapter
explains why a practice matters, gives best practices and common pitfalls,
and ends with a short checklist.

Once your agent acts on other systems, runs for a long time, or carries more
risk, continue with [Advanced concepts](../advanced/README.md). If several
agents work together, each one still follows Core and Advanced, and the
system as a whole follows [Multi-agent systems](../multi-agent/README.md).

The guidance is intentionally opinionated. You may adopt stricter controls.
Exceptions should be explicit, time-bound, and approved by an accountable
owner.

## Contents

### Before you build

- [1. Strategy and use-case selection](01-strategy-and-use-cases.md): whether an
  agent is worth building, how much authority the first release gets, and
  how to measure success, cost, and safety separately.
- [2. Defining the problem](02-problem-definition.md): the brief, success
  criteria and limits, data, risks, owners, dependencies, and the two
  readiness decisions every agent faces.
- [3. Zero-trust principles for agents](03-zero-trust-principles.md): why you
  design your agent as an untrusted workload acting on someone's behalf, and
  what that means for its identity, permissions, and evidence.
- [4. Operating model](04-operating-model.md): which decisions are yours, whose
  sign-off you need, what your agent must report for oversight, and how it
  moves through adoption stages on evidence.

### Building an agent

- [5. Principles and scope](05-principles-and-scope.md)
- [6. Reference architecture](06-reference-architecture.md)
- [7. Agent contract](07-agent-contract.md)
- [8. Skills](08-skills.md)
- [9. Tools](09-tools.md)
- [10. Evaluation](10-evaluation.md)
- [11. Observability](11-observability.md)
- [12. Production readiness](12-production-readiness.md)

[References](references.md) lists sources for Core and Advanced concepts.

## How the chapters connect

| Output of chapters 1 to 4 | Used by |
| --- | --- |
| Use-case charter and value hypothesis | [Agent contract](07-agent-contract.md), [risk assessment](../advanced/04-risk-assessment.md) |
| Problem brief and success criteria | [Evaluation](10-evaluation.md), [cost optimization](../advanced/02-cost-optimization.md) |
| Readiness decisions | [Production readiness](12-production-readiness.md) |
| Zero-trust principles | [Principles](05-principles-and-scope.md), [tools](09-tools.md), [security and governance](../advanced/03-security-and-governance.md) |
| Decision rights and oversight | [Security and governance](../advanced/03-security-and-governance.md), [observability](11-observability.md) |

## Skills

The companion [skills library](../skills/README.md) turns this guidance into
focused workflows for clients that support the Agent Skills specification.

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
indicate requirement strength:

- **MUST / MUST NOT:** required for conformance.
- **SHOULD / SHOULD NOT:** expected unless a documented reason justifies an
  exception.
- **MAY:** optional.

## Every production agent, in one page

Every production agent:

1. Has a stable name, version, owner, execution class, and evidence-based risk
   assessment.
2. Uses a declarative agent specification for its definition and schema-validated
   types for runtime validation.
3. Explicitly allowlists its skills and tools.
4. Classifies every tool as read-only, reversible write, or consequential write.
5. Uses a durable execution engine for long-running work or any externally
   visible side effect.
6. Requires human approval for consequential operations.
7. Enforces request, tool, token, time, and spend budgets.
8. Is evaluated for outcomes, trajectory, safety, durability, latency, and cost.
9. Emits correlated OpenTelemetry data across requests, workflows, models,
   skills, and tools.
10. Cannot ship until residual risks are accepted and its production-readiness
    checklist is complete.

## Execution classes

| Class            | Durable execution |                  Side effects |                     Human approval |
| ---------------- | ----------------: | ----------------------------: | ---------------------------------: |
| `ephemeral`      |          Optional |                    Prohibited |                           Optional |
| `durable`        |          Required | Allowed through durable steps |                       Policy-based |
| `human_governed` |          Required |        Allowed after approval | Required for consequential actions |

An individual workflow may elevate an agent's declared execution class, but
it MUST NOT silently downgrade it. The effective class is at least the
minimum required by the most consequential enabled tool. See
[execution classes](05-principles-and-scope.md#execution-classes) for what
each class requires.

## Relationship between execution class and risk

Execution class describes **how work executes**. Governance tier describes the
assurance required by the agent's inherent risk and mandatory floors. Residual
risk describes what remains after verified controls. They are independent: a
read-only medical assistant can be ephemeral and high risk, while a reversible
internal update agent can be durable and medium risk. See the
[risk assessment](../advanced/04-risk-assessment.md) chapter in Advanced concepts.

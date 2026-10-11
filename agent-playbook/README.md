# Agent Playbook

- **Status:** Draft
- **Version:** 0.4
- **Last updated:** 2026-10-11

This playbook is a guide for developers building production AI agents. It
walks you through designing, building, evaluating, and operating an agent as
a governed software system: a typed contract, a constrained set of
capabilities, a durable execution model when required, and measurable
quality, safety, reliability, and cost. Each chapter explains why a practice
matters, gives best practices and common pitfalls, and ends with a short
checklist.

It is also a standard. The MUST, SHOULD, and MAY statements in each chapter
define what a conforming agent must do, so other tools and implementations
can map to them. It says what to do and why, not which frameworks, SDKs, or
products to use.

If your agent is part of a system that coordinates several agents, each
member still meets this standard, and the composition is additionally
governed by the companion
[Multi-Agent Systems Playbook](../multi-agent-playbook/README.md).

The playbook is intentionally opinionated. You may adopt stricter controls.
Exceptions should be explicit, time-bound, and approved by an accountable
owner.

## Contents

The playbook has two parts. **Core** is what every agent needs before it
ships. **Advanced concepts** is what you add once your agent acts on other
systems, runs for a long time, or carries more risk. Start with Core; read an
Advanced chapter when your agent needs it.

### Part 1: Core

- [1. Principles and scope](01-principles-and-scope.md)
- [2. Reference architecture](02-reference-architecture.md)
- [3. Agent contract](03-agent-contract.md)
- [4. Skills](04-skills.md)
- [5. Tools](05-tools.md)
- [6. Evaluation](06-evaluation.md)
- [7. Observability](07-observability.md)
- [8. Production readiness](08-production-readiness.md)

### Part 2: Advanced concepts

- [9. Durable execution and human approval](09-durable-execution.md)
- [10. Cost optimization](10-cost-optimization.md)
- [11. Security and governance](11-security-and-governance.md)
- [12. Risk assessment](12-risk-assessment.md)
- [13. Implementation patterns](13-implementation-patterns.md)

[References](references.md) lists sources for both parts.

## Before you start

The [Foundations](../foundations/README.md) guides cover what this playbook
assumes is already settled: whether an agent is the right answer, the problem
brief and readiness criteria, zero-trust principles, and who owns which
decisions.

## Skills and implementations

- The companion [skills library](../skills/README.md) translates this
  standard into focused workflows for clients that support the Agent Skills
  specification.
- [Zetra](https://github.com/X-McKay/zetra) is one opinionated, zero-trust
  implementation of this playbook. It is an example of conformance, not a
  requirement of it.

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
indicate requirement strength:

- **MUST / MUST NOT:** required for conformance.
- **SHOULD / SHOULD NOT:** expected unless a documented reason justifies an
  exception.
- **MAY:** optional.

## The standard in one page

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
[execution classes](01-principles-and-scope.md#execution-classes) for what
each class requires.

## Relationship between execution class and risk

Execution class describes **how work executes**. Governance tier describes the
assurance required by the agent's inherent risk and mandatory floors. Residual
risk describes what remains after verified controls. They are independent: a
read-only medical assistant can be ephemeral and high risk, while a reversible
internal update agent can be durable and medium risk. See the
[risk assessment](12-risk-assessment.md) chapter.

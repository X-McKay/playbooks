# Advanced concepts

- **Status:** Draft
- **Version:** 0.4
- **Last updated:** 2026-10-12

This is the second of the playbook's three sections. It covers what you add
once your agent acts on other systems, runs for a long time, or carries more
risk. It builds on [Core concepts](../core/README.md): read Core first, then
read an Advanced chapter when your agent needs it.

Core and Advanced share one set of terms: the
[normative language](../core/README.md#normative-language),
[execution classes](../core/05-principles-and-scope.md#execution-classes), and governance tiers
defined in Core apply here unchanged.

## Advanced concepts in one page

On top of [Core concepts in one page](../core/README.md#core-concepts-in-one-page),
an agent that acts on other systems, runs for a long time, or carries more
risk:

1. Uses a durable execution engine for long-running work or any externally
   visible side effect.
2. Requires human approval for consequential operations.
3. Enforces request, tool, token, time, and spend budgets.
4. Is evaluated for durability: replay, retries, and recovery.
5. Has an evidence-based risk assessment, and cannot ship until its residual
   risks are accepted.

## Contents

1. [Durable execution and human approval](01-durable-execution.md)
2. [Cost optimization](02-cost-optimization.md)
3. [Security and governance](03-security-and-governance.md)
4. [Risk assessment](04-risk-assessment.md)
5. [Implementation patterns](05-implementation-patterns.md)

The [risk assessment template](templates/risk-assessment.yaml) goes with
chapter 4. Sources are listed in the Core [references](../core/references.md).

## Skills

The companion [skills library](../skills/README.md) includes skills for
durable execution, risk assessment, and running an agent in production.

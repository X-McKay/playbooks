# Multi-agent systems

- **Status:** Draft
- **Version:** 0.2
- **Last updated:** 2026-10-11

This section is a guide for developers who compose several AI agents into
one system that produces one governed outcome. It explains how to decide
whether you need more than one agent, how to shape and bound the
composition, and what evidence you need before it ships. It is
technology-neutral: it describes requirements, practices, and evidence rather
than any particular SDK, framework, runtime, or vendor.

It extends the single-agent guidance in
[Core concepts](../core/README.md) and
[Advanced concepts](../advanced/README.md); it does not replace it. Each
agent you compose follows the single-agent guidance on its own, and this
section covers only what changes when agents work together, so you
should not need to read anything twice. Where a chapter relies on a
single-agent rule, it links to it.

A multi-agent system conforms only when every participating agent conforms to
the single-agent guidance and the composition conforms to this section. The unit
you design, evaluate, release, and operate is the versioned system
composition, not an informal collection of agents.

The playbook is intentionally opinionated. You may adopt stricter controls.
Exceptions should be explicit, time-bound, and approved by an accountable
owner.

## Contents

1. [Principles and scope](01-principles-and-scope.md)
2. [Reference architecture](02-reference-architecture.md)
3. [System contract](03-system-contract.md)
4. [Membership and roles](04-membership-and-roles.md)
5. [Delegation and interactions](05-delegation-and-interactions.md)
6. [Durable coordination](06-durable-coordination.md)
7. [Evaluation](07-evaluation.md)
8. [Observability](08-observability.md)
9. [Cost and capacity](09-cost-and-capacity.md)
10. [Security and governance](10-security-and-governance.md)
11. [Production readiness](11-production-readiness.md)
12. [Implementation patterns](12-implementation-patterns.md)
13. [System risk assessment](13-system-risk-assessment.md)
14. [References](references.md)

## Before you start

Chapters 1 to 4 of [Core concepts](../core/README.md) cover the decisions
this section assumes are settled: whether agents are the right answer, the
problem brief, zero-trust principles, and the operating model.

## Relationship to the single-agent guidance

The single-agent guidance governs each node. This section governs the graph.

| Concern | Governing standard |
| --- | --- |
| Agent identity, instructions, model policy, and typed output | Core and Advanced concepts |
| Skills, tools, authorization, and tool effects | Core and Advanced concepts |
| Individual execution class, budgets, evals, telemetry, and risk | Core and Advanced concepts |
| System purpose, membership, topology, and interaction graph | Multi-agent systems |
| Delegated authority, data flow, shared state, and termination | Multi-agent systems |
| System budgets, emergent behavior, composition risk, and release | Multi-agent systems |

When the standards appear to conflict, the stricter applicable requirement
governs. A system MUST NOT weaken a member agent's execution class,
governance tier, authorization, approval, data-handling, or budget controls.

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
indicate requirement strength:

- **MUST / MUST NOT:** required for conformance.
- **SHOULD / SHOULD NOT:** expected unless a documented reason justifies an
  exception.
- **MAY:** optional.

## The standard in one page

Every production multi-agent system:

1. Documents why multiple agents are preferable to a simpler single-agent or
   deterministic design.
2. Has a stable name, version, owner, System Spec, composition manifest, and
   system risk assessment.
3. References versioned, independently conforming declarative agent
   specifications (Agent Specs) rather than duplicating their contracts.
4. Uses a reviewed topology with explicitly pinned or policy-admitted
   membership and interaction edges.
5. Treats every inter-agent boundary as an untrusted, typed, bounded API.
6. Allows delegation to attenuate authority but never to amplify it.
7. Places shared state, conflict resolution, approval, and termination under
   deterministic control.
8. Enforces system-wide and per-interaction limits for depth, fan-out,
   concurrency, rounds, requests, tools, time, tokens, and spend.
9. Uses a durable execution engine for long-running coordination or any path
   capable of an externally visible side effect.
10. Evaluates system outcomes, coordination, failure propagation, security,
    durability, latency, and total cost against an appropriate baseline.
11. Emits correlated telemetry for the complete delegation graph and retains
    auditable evidence for consequential actions.
12. Cannot ship until member and system hard gates pass and residual
    composition risks are accepted by accountable humans.

The standard supports both static and dynamic systems. Dynamic membership,
recursive task trees, shared blackboards, peer meshes, market allocation, and
event-driven collectives stay inside a deterministic control envelope and
carry a higher evidence burden in proportion to their adaptability.

## Conformance equation

```text
multi-agent system conformance =
    conformance of every reachable member agent
  + conformance of the versioned composition
  + evidence for their integrated behavior
```

Passing member-agent checks does not establish system conformance. A
composition can introduce risks, costs, and failure modes that no member has
in isolation.

## Skills

Optional workflow skills that help you apply this playbook are described in
[skills](../skills/README.md). The playbook itself stays technology-neutral.

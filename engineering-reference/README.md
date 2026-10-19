# Section II — Engineering Reference

**Status:** 0.5.0 first draft

**Purpose:** Apply specialized patterns without making optional mechanisms a default architecture.

**Applicability:** Use after the applicable foundations in Parts 1–5 identify a concrete trigger or higher-assurance need.

**Output:** A scoped design/evidence record for the selected pattern, not a claim that every reference Part applies.

[Playbook home](../README.md) · [Applicability](../applicability.md) · [Glossary](../glossary.md) · [Requirement index](../requirement-index.md)

## Parts

### [Part 6 — Reasoning and Execution Patterns](06-reasoning-and-execution-patterns/README.md)

**Purpose:** Apply optional reasoning patterns without turning model output into authority or unbounded work.
**Applies to:** Only when explicit planning, reflection, or concurrent branch work is part of the design.
**Output:** Pattern-specific limits, baseline evidence, state/branch rules, and observable terminal outcomes.

- [6.1 Planning, Decomposition, and Bounded Control Loops](06-reasoning-and-execution-patterns/01-planning-decomposition-and-bounded-control-loops.md)
- [6.2 Reflection, Critique, and Verification](06-reasoning-and-execution-patterns/02-reflection-critique-and-verification.md)
- [6.3 Parallel Work, State, and Failure Propagation](06-reasoning-and-execution-patterns/03-parallel-work-state-and-failure-propagation.md)

### [Part 7 — Durable Execution and Human-Governed Work](07-durable-execution-and-human-governed-work/README.md)

**Purpose:** Handle durable recovery, external effects, and human-governed consequential work.
**Applies to:** When work is long-running, resumable, side-effecting, approval-waiting, or consequential; every agent still declares its execution class.
**Output:** Execution-class rationale, recovery/effect evidence, and—where used—approval and compatibility records.

- [7.1 Execution Classes, Persistence, and Recovery](07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md)
- [7.2 Side Effects, Idempotency, and Unknown Outcomes](07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)
- [7.3 Approval, Suspension, and In-Flight Compatibility](07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)

### [Part 8 — Model, Context, and Resource Engineering](08-model-context-and-resource-engineering/README.md)

**Purpose:** Choose and optimize models, context, performance, and shared capacity without weakening controls.
**Applies to:** When a model policy, retrieval transformation, optimization, cache, queue, or shared-capacity boundary is used.
**Output:** Resolved model evidence and, where applicable, context lineage, performance evidence, and admission controls.

- [8.1 Model Selection, Parameters, and Routing](08-model-context-and-resource-engineering/01-model-selection-parameters-and-routing.md)
- [8.2 Retrieval, Memory, and Context Optimization](08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md)
- [8.3 Cost, Latency, and Performance Optimization](08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md)
- [8.4 Capacity, Admission Control, and Backpressure](08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md)

### [Part 9 — Multi-Agent Systems and Interoperability](09-multi-agent-systems-and-interoperability/README.md)

**Purpose:** Use multiple agents and interoperability only when composition has measurable value and governed boundaries.
**Applies to:** When two or more model-driven agents contribute to one outcome, or when A2A-style remote interaction is enabled.
**Output:** A system spec/composition manifest, typed interaction contracts, and integrated system evidence.

- [9.1 When Multiple Agents Help, Topologies, and System Contracts](09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md)
- [9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces](09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)
- [9.3 Coordination, System Evaluation, and Operations](09-multi-agent-systems-and-interoperability/03-coordination-system-evaluation-and-operations.md)

### [Part 10 — Risk, Privacy, and Specialized Assurance](10-risk-privacy-and-specialized-assurance/README.md)

**Purpose:** Apply detailed risk, human-impact, privacy, isolation, and audit assurance when the initial screen warrants it.
**Applies to:** When the initial screen, capability, policy floor, sensitive context, or material harm scenario triggers higher assurance.
**Output:** A detailed assessment and any triggered impact, privacy, isolation, and audit evidence.

- [10.1 Detailed Risk Assessment and Governance](10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md)
- [10.2 Bias, Human Impact, and Domain Assurance](10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md)
- [10.3 Advanced Privacy, Isolation, and Auditability](10-risk-privacy-and-specialized-assurance/03-advanced-privacy-isolation-and-auditability.md)

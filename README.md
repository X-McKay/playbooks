# Agent Playbook

This playbook is a guide, with best practices, for developing production-grade AI agents. It is written for the developers who design, build, test and run agents, and it stays technology-neutral: the practices hold whatever model, framework or language you use.

**Status:** 0.5.0-draft.2 — draft. The requirements use MUST, SHOULD and MAY to show how strongly the playbook recommends a practice; see [Applicability and normative language](applicability.md).

## How the playbook is organized

The playbook has two sections:

- **Section I, the Development Guide (Parts 1–5),** is the main route from a user problem to an agent running in production. Every production agent needs it.
- **Section II, the Engineering Reference (Parts 6–10),** covers patterns you need only when your design uses them: explicit planning, durable or approval-gated work, model routing and context optimization, multiple agents, and higher-assurance risk work.

Each chapter explains the concepts, the decisions you face, best practices and common failures, then lists its requirements, a worked example, and a checklist. Most chapters share one fictional example, an internal travel-policy assistant, so you can follow one agent through the book. Parts 1–5 have been reviewed in depth; Parts 6–10 are earlier drafts.

## Start here

- [Applicability and normative language](applicability.md) explains which requirements apply to your agent, what "not applicable" means, and how exceptions work.
- [Glossary](glossary.md) defines the shared vocabulary and links to the chapter that explains each term.
- [Requirement index](requirement-index.md) lists every requirement ID and the chapter that owns it.
- [Proposed agent development skills](development-skills/README.md) provide a separately versioned, 0.5-mapped workflow for drafting and evaluating agent release candidates. They do not replace the canonical requirements or migrate the legacy skills.

## Start small

You do not need the whole book on day one. For a first production agent, especially a read-only one:

1. Write a short problem brief and success criteria, and check that a simpler non-agent design would not do the job ([Part 1](development-guide/01-problem-definition-and-planning/README.md)).
2. Write the agent contract: what it accepts, what it may do, and every way it can finish ([2.2](development-guide/02-agent-basics/02-agent-contracts-and-configuration.md)).
3. Enforce permissions outside the model and treat retrieved content and tool output as data, not instructions ([Part 3](development-guide/03-security-and-trust-boundaries/README.md)).
4. Build a small evaluation set from real tasks, including cases where the agent should decline or ask for more information, and rerun it on every change ([Part 4](development-guide/04-testing-and-evaluation/README.md)).
5. Release gradually with monitoring, a way to stop the agent, and a named owner ([Part 5](development-guide/05-release-operations-and-lifecycle/README.md)).

Add Engineering Reference Parts only when your design calls for them.

## Reading routes

1. **New production agent:** read Parts 1 to 5 in order.
2. **Adding a capability:** go to the Part for it: planning, reflection or parallel work ([Part 6](engineering-reference/06-reasoning-and-execution-patterns/README.md)); long-running, side-effecting or approval-gated work ([Part 7](engineering-reference/07-durable-execution-and-human-governed-work/README.md)); model selection, context, cost or capacity ([Part 8](engineering-reference/08-model-context-and-resource-engineering/README.md)); several agents or agent-to-agent protocols ([Part 9](engineering-reference/09-multi-agent-systems-and-interoperability/README.md)).
3. **Higher-risk agent:** start with the initial risk screen in [1.4](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md), then apply [Part 10](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md) alongside Parts 3–5.

## Book map

### Section I — Development Guide

[Development Guide](development-guide/README.md)

#### [1. Problem Definition and Planning](development-guide/01-problem-definition-and-planning/README.md)

**Purpose:** Frame a reviewable production proposal before settling implementation choices.
**Applies to:** Every production-agent proposal and any pilot that may expose users or operational data.
**Output:** A problem brief, success criteria, suitability rationale, and initial scope/risk/ownership record.

- [1.1 Defining the Problem](development-guide/01-problem-definition-and-planning/01-defining-the-problem.md)
- [1.2 Requirements, Success Criteria, and Measurable Targets](development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md)
- [1.3 Agent Suitability and Alternatives](development-guide/01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md)
- [1.4 Initial Risk, Data, Ownership, and Delivery Plan](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md)

#### [2. Agent Basics](development-guide/02-agent-basics/README.md)

**Purpose:** Define bounded agent behavior and the optional capabilities that may support it.
**Applies to:** Every agent uses the contract material; tools, skills, retrieval, memory, and MCP apply only when enabled.
**Output:** A reviewable contract, capability manifest, instruction identity, and—where used—validated capability interfaces.

- [2.1 Agent Anatomy, Runtime Loop, and Project Organization](development-guide/02-agent-basics/01-agent-anatomy-runtime-loop-and-project-organization.md)
- [2.2 Agent Contracts and Configuration](development-guide/02-agent-basics/02-agent-contracts-and-configuration.md)
- [2.3 Prompts and Instructions](development-guide/02-agent-basics/03-prompts-and-instructions.md)
- [2.4 Tools and External Interfaces](development-guide/02-agent-basics/04-tools-and-external-interfaces.md)
- [2.5 Skills and Reusable Capabilities](development-guide/02-agent-basics/05-skills-and-reusable-capabilities.md)
- [2.6 Context and Retrieval Fundamentals](development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md)
- [2.7 MCP and Standardized Integrations](development-guide/02-agent-basics/07-mcp-and-standardized-integrations.md)
- [Practical reference](development-guide/02-agent-basics/reference/README.md)

#### [3. Security and Trust Boundaries](development-guide/03-security-and-trust-boundaries/README.md)

**Purpose:** Keep identity, authority, untrusted content, data handling, and audit evidence at enforceable boundaries.
**Applies to:** All production agents need appropriate trust boundaries; data and advanced controls are triggered by the information and operations involved.
**Output:** A protected-operation boundary, scoped authority, data-handling record where applicable, and minimum evidence.

- [3.1 Identity, Authority, Zero Trust, and Least Privilege](development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)
- [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)
- [3.3 Data Privacy, Handling, and Minimum Audit Evidence](development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)
- [Practical reference](development-guide/03-security-and-trust-boundaries/reference/README.md)

#### [4. Testing and Evaluation](development-guide/04-testing-and-evaluation/README.md)

**Purpose:** Turn bounded product, safety, and control claims into inspectable cases, fixtures, evaluators, coverage records, and decision-grade evidence.
**Applies to:** Whenever evidence supports a material design, pilot, release, change, or operational-learning decision; the universal core applies to every production candidate and profiles are independently triggered.
**Output:** A coverage map, claim-fit evidence, visible run statuses, and a bounded evaluation conclusion.

- [4.1 Foundations, Terms, and Definitions](development-guide/04-testing-and-evaluation/01-foundations-terms-and-definitions.md)
- [4.2 Test Levels, Techniques, and Suite Purposes](development-guide/04-testing-and-evaluation/02-test-levels-techniques-and-suite-purposes.md)
- [4.3 Evaluation Types and Dimensions](development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md)
- [4.4 Evaluators, Metrics, Rubrics, and Calibration](development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md)
- [4.5 Planning, Designing, and Running Tests and Evaluations](development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md)
- [4.6 Standards, Required Coverage, and Execution Cadence](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md)
- [4.7 Analyzing Results, Comparing Versions, and Making Decisions](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)
- [Practical reference](development-guide/04-testing-and-evaluation/reference/README.md)

#### [5. Release, Operations, and Lifecycle](development-guide/05-release-operations-and-lifecycle/README.md)

**Purpose:** Authorize release, operate within declared bounds, respond to incidents, and retire safely.
**Applies to:** Production release, operation, material change, incident response, and retirement.
**Output:** A release record, operating signals and limits, rollout/containment plan, and support/lifecycle record.

- [5.1 Observability, Budgets, and Operational Control](development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md)
- [5.2 Readiness, Change, and Rollout](development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)
- [5.3 Ownership, Incidents, Maintenance, and Retirement](development-guide/05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md)
- [Practical reference](development-guide/05-release-operations-and-lifecycle/reference/README.md)

### Section II — Engineering Reference

[Engineering Reference](engineering-reference/README.md)

#### [6. Reasoning and Execution Patterns](engineering-reference/06-reasoning-and-execution-patterns/README.md)

**Purpose:** Apply optional reasoning patterns without turning model output into authority or unbounded work.
**Applies to:** Only when explicit planning, reflection, or concurrent branch work is part of the design.
**Output:** Pattern-specific limits, baseline evidence, state/branch rules, and observable terminal outcomes.

- [6.1 Planning, Decomposition, and Bounded Control Loops](engineering-reference/06-reasoning-and-execution-patterns/01-planning-decomposition-and-bounded-control-loops.md)
- [6.2 Reflection, Critique, and Verification](engineering-reference/06-reasoning-and-execution-patterns/02-reflection-critique-and-verification.md)
- [6.3 Parallel Work, State, and Failure Propagation](engineering-reference/06-reasoning-and-execution-patterns/03-parallel-work-state-and-failure-propagation.md)

#### [7. Durable Execution and Human-Governed Work](engineering-reference/07-durable-execution-and-human-governed-work/README.md)

**Purpose:** Handle durable recovery, external effects, and human-governed consequential work.
**Applies to:** When work is long-running, resumable, side-effecting, approval-waiting, or consequential; every agent still declares its execution class.
**Output:** Execution-class rationale, recovery/effect evidence, and—where used—approval and compatibility records.

- [7.1 Execution Classes, Persistence, and Recovery](engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md)
- [7.2 Side Effects, Idempotency, and Unknown Outcomes](engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)
- [7.3 Approval, Suspension, and In-Flight Compatibility](engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)

#### [8. Model, Context, and Resource Engineering](engineering-reference/08-model-context-and-resource-engineering/README.md)

**Purpose:** Choose and optimize models, context, performance, and shared capacity without weakening controls.
**Applies to:** When a model policy, retrieval transformation, optimization, cache, queue, or shared-capacity boundary is used.
**Output:** Resolved model evidence and, where applicable, context lineage, performance evidence, and admission controls.

- [8.1 Model Selection, Parameters, and Routing](engineering-reference/08-model-context-and-resource-engineering/01-model-selection-parameters-and-routing.md)
- [8.2 Retrieval, Memory, and Context Optimization](engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md)
- [8.3 Cost, Latency, and Performance Optimization](engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md)
- [8.4 Capacity, Admission Control, and Backpressure](engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md)

#### [9. Multi-Agent Systems and Interoperability](engineering-reference/09-multi-agent-systems-and-interoperability/README.md)

**Purpose:** Use multiple agents and interoperability only when composition has measurable value and governed boundaries.
**Applies to:** When two or more model-driven agents contribute to one outcome, or when A2A-style remote interaction is enabled.
**Output:** A system spec/composition manifest, typed interaction contracts, and integrated system evidence.

- [9.1 When Multiple Agents Help, Topologies, and System Contracts](engineering-reference/09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md)
- [9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces](engineering-reference/09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)
- [9.3 Coordination, System Evaluation, and Operations](engineering-reference/09-multi-agent-systems-and-interoperability/03-coordination-system-evaluation-and-operations.md)

#### [10. Risk, Privacy, and Specialized Assurance](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md)

**Purpose:** Apply detailed risk, human-impact, privacy, isolation, and audit assurance when the initial screen warrants it.
**Applies to:** When the initial screen, capability, policy floor, sensitive context, or material harm scenario triggers higher assurance.
**Output:** A detailed assessment and any triggered impact, privacy, isolation, and audit evidence.

- [10.1 Detailed Risk Assessment and Governance](engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md)
- [10.2 Bias, Human Impact, and Domain Assurance](engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md)
- [10.3 Advanced Privacy, Isolation, and Auditability](engineering-reference/10-risk-privacy-and-specialized-assurance/03-advanced-privacy-isolation-and-auditability.md)

## Universal versus triggered

Every agent needs a bounded contract with defined ways to finish, a proportionate risk screen, evidence that it works, and operating controls. That does not make every mechanism in the book universal. Tools, skills, retrieval, memory, explicit planning, MCP, A2A, model judges, durable execution, human approval, shared capacity controls and multi-agent composition apply only when your design uses them. A read-only agent can still be high risk, so execution class, governance tier and residual risk are separate decisions. See [Applicability and normative language](applicability.md).

## Earlier version

The `agent-playbook/`, `foundations/`, `multi-agent-playbook/` and `skills/` directories hold the earlier v0.4 playbook and its skills. They have not been updated to this draft, and the skills still reference the v0.4 chapters.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and the [writing guide](writing-guide.md). Editorial history and open decisions are in [development progress](development-progress.md) and [draft notes](draft-notes.md).

# Agent Playbook 0.5.0-draft.2

**Status:** Assembled 0.5.0-draft.2 — proposed, not an adopted standard
**Provenance:** Reorganized and populated from the supplied v0.4 compatibility baseline and manifest-pinned PR #7 source set (`78ec3bd517c52255bced1901b4d00b68c7c18ada`).
**Scope:** Technology-neutral guidance for designing, evaluating, releasing, operating, and assuring production AI agents and multi-agent systems.

This is the coherent draft book entry point. It supplies a common route through two sections, ten Parts, and 40 populated draft chapters. It does **not** assert that an organization has adopted the draft requirements or that older material and skills conform to them.

## Current refinement state

Parts **1–5** are refined draft mini-books. Part 1 retains its completed planning history; the earlier increment integrated the seven separately reviewable Part 2 chapter/template units and three separately reviewable Part 3 chapter/template units, their two practical-reference indexes, shared navigation, and glossary pointers. This increment integrates the three separately reviewable Part 5 chapter/template units, its overview, practical reference, and glossary pointers. The Part 5 scoped writer gates were reported as passed local file checks only; they are not a whole-book result, release authorization, or adoption decision. The canonical requirement wording, all 208 IDs, strengths, owner paths, applicability, and conformance meaning are unchanged: the draft remains **proposed, not adopted**.

[Part 4](development-guide/04-testing-and-evaluation/README.md) remains the existing detailed seven-chapter pilot mini-book within the refined route. Parts **6–10** remain populated **first drafts**—not empty and not yet reviewed to the refinement depth of Parts 1–5. Final whole-book structural, owner, template, local-link, and Markdown checks, followed by packaging, remain pending the parent delivery record after this integration. See [development progress](development-progress.md) for the current reading-order queue and validation boundary.

## Start here

- [Applicability and normative language](applicability.md) explains the universal-versus-triggered boundary, `not applicable`, governed exceptions, non-waivable gates, and `conditional_go`.
- [Glossary](glossary.md) supplies one reading vocabulary and links to the chapters that own each term.
- [Requirement index](requirement-index.md) locates requirement IDs without reproducing a competing standard.
- [Draft notes](draft-notes.md) records migration, proposed policy changes, review boundaries, limitations, and unresolved decisions.
- [Development progress](development-progress.md) records completed increments, review units, the reading-order backlog, and delivery-validation status.

## Reading routes

1. **New production proposal:** read [Part 1](development-guide/01-problem-definition-and-planning/README.md), then [Part 2](development-guide/02-agent-basics/README.md), [Part 3](development-guide/03-security-and-trust-boundaries/README.md), [Part 4](development-guide/04-testing-and-evaluation/README.md), and [Part 5](development-guide/05-release-operations-and-lifecycle/README.md).
2. **Add an optional capability:** start with the relevant trigger: planning/reflection/parallel work ([Part 6](engineering-reference/06-reasoning-and-execution-patterns/README.md)); durable or human-governed work ([Part 7](engineering-reference/07-durable-execution-and-human-governed-work/README.md)); model/context/capacity engineering ([Part 8](engineering-reference/08-model-context-and-resource-engineering/README.md)); or composition/interoperability ([Part 9](engineering-reference/09-multi-agent-systems-and-interoperability/README.md)).
3. **Higher-assurance review:** use the initial screen in [1.4](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md), then apply the triggered methods in [Part 10](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md) alongside Parts 3–5.

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

Every agent needs a bounded contract and terminal outcomes, proportionate risk screening, appropriate evidence, and operating controls. Those universal decisions do **not** make every reference mechanism universal. Tools, skills, retrieval, memory, explicit planning, MCP, A2A, model judges, durable execution, human approval, shared admission, and multi-agent composition apply only when their stated trigger is present. A read-only agent can still be high risk; execution class, governance tier, and residual risk remain separate decisions. See [Applicability and normative language](applicability.md) before treating a chapter as applicable or invoking an exception.

## Legacy v0.4 compatibility baseline

The existing [`agent-playbook/`](agent-playbook/README.md), [`foundations/`](foundations/README.md), [`multi-agent-playbook/`](multi-agent-playbook/README.md), and [`skills/`](skills/README.md) remain a byte-identical v0.4 compatibility baseline in this worktree. They have not been moved, deleted, or declared v0.5 conformant. Skills continue to reference their existing material until a separately reviewed migration changes them.

## Contributing to this draft

See [CONTRIBUTING.md](CONTRIBUTING.md). New 0.5.0-draft.2 material must remain technology-neutral, preserve canonical chapter ownership, identify proposed policy changes honestly, and keep legacy content and skills distinct.

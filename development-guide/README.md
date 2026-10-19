# Section I — Development Guide

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted

**Purpose:** Move from a user problem to a bounded, testable, releasable production agent.

**Applicability:** Begin here for any production proposal; Parts 1–5 provide the primary route even when optional engineering patterns are later used.

**Output:** A reviewable proposal, agent contract, trust boundaries, evidence, release decision, and operating/lifecycle plan.

**Editorial depth:** Parts 1–5 are refined draft mini-books. Part 4 remains the existing detailed pilot. The specialized reference Parts 6–10 remain populated first drafts.

[Playbook home](../README.md) · [Applicability](../applicability.md) · [Glossary](../glossary.md) · [Requirement index](../requirement-index.md)

## Parts

### [Part 1 — Problem Definition and Planning](01-problem-definition-and-planning/README.md)

**Purpose:** Frame a reviewable production proposal before settling implementation choices.
**Applies to:** Every production-agent proposal and any pilot that may expose users or operational data.
**Output:** A problem brief, success criteria, suitability rationale, and initial scope/risk/ownership record.

- [1.1 Defining the Problem](01-problem-definition-and-planning/01-defining-the-problem.md)
- [1.2 Requirements, Success Criteria, and Measurable Targets](01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md)
- [1.3 Agent Suitability and Alternatives](01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md)
- [1.4 Initial Risk, Data, Ownership, and Delivery Plan](01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md)

### [Part 2 — Agent Basics](02-agent-basics/README.md)

**Purpose:** Define bounded agent behavior and the optional capabilities that may support it.
**Applies to:** Every agent uses the contract material; tools, skills, retrieval, memory, and MCP apply only when enabled.
**Output:** A reviewable contract, capability manifest, instruction identity, and—where used—validated capability interfaces.

- [2.1 Agent Anatomy, Runtime Loop, and Project Organization](02-agent-basics/01-agent-anatomy-runtime-loop-and-project-organization.md)
- [2.2 Agent Contracts and Configuration](02-agent-basics/02-agent-contracts-and-configuration.md)
- [2.3 Prompts and Instructions](02-agent-basics/03-prompts-and-instructions.md)
- [2.4 Tools and External Interfaces](02-agent-basics/04-tools-and-external-interfaces.md)
- [2.5 Skills and Reusable Capabilities](02-agent-basics/05-skills-and-reusable-capabilities.md)
- [2.6 Context and Retrieval Fundamentals](02-agent-basics/06-context-and-retrieval-fundamentals.md)
- [2.7 MCP and Standardized Integrations](02-agent-basics/07-mcp-and-standardized-integrations.md)
- [Practical reference](02-agent-basics/reference/README.md)

### [Part 3 — Security and Trust Boundaries](03-security-and-trust-boundaries/README.md)

**Purpose:** Keep identity, authority, untrusted content, data handling, and audit evidence at enforceable boundaries.
**Applies to:** All production agents need appropriate trust boundaries; data and advanced controls are triggered by the information and operations involved.
**Output:** A protected-operation boundary, scoped authority, data-handling record where applicable, and minimum evidence.

- [3.1 Identity, Authority, Zero Trust, and Least Privilege](03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)
- [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)
- [3.3 Data Privacy, Handling, and Minimum Audit Evidence](03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)
- [Practical reference](03-security-and-trust-boundaries/reference/README.md)

### [Part 4 — Testing and Evaluation](04-testing-and-evaluation/README.md)

**Purpose:** Turn bounded product, safety, and control claims into inspectable cases, fixtures, evaluators, coverage records, and decision-grade evidence.
**Applies to:** Whenever evidence supports a material design, pilot, release, change, or operational-learning decision; the universal core applies to every production candidate and profiles are independently triggered.
**Output:** A coverage map, claim-fit evidence, visible run statuses, and a bounded evaluation conclusion.

- [4.1 Foundations, Terms, and Definitions](04-testing-and-evaluation/01-foundations-terms-and-definitions.md)
- [4.2 Test Levels, Techniques, and Suite Purposes](04-testing-and-evaluation/02-test-levels-techniques-and-suite-purposes.md)
- [4.3 Evaluation Types and Dimensions](04-testing-and-evaluation/03-evaluation-types-and-dimensions.md)
- [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md)
- [4.5 Planning, Designing, and Running Tests and Evaluations](04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md)
- [4.6 Standards, Required Coverage, and Execution Cadence](04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md)
- [4.7 Analyzing Results, Comparing Versions, and Making Decisions](04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)
- [Practical reference](04-testing-and-evaluation/reference/README.md)

### [Part 5 — Release, Operations, and Lifecycle](05-release-operations-and-lifecycle/README.md)

**Purpose:** Authorize release, operate within declared bounds, respond to incidents, and retire safely.
**Applies to:** Production release, operation, material change, incident response, and retirement.
**Output:** A release record, operating signals and limits, rollout/containment plan, and support/lifecycle record.

- [5.1 Observability, Budgets, and Operational Control](05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md)
- [5.2 Readiness, Change, and Rollout](05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)
- [5.3 Ownership, Incidents, Maintenance, and Retirement](05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md)
- [Practical reference](05-release-operations-and-lifecycle/reference/README.md)

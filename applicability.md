# Applicability and normative language

**Status:** 0.5.0-draft.2 — draft

This page explains how to tell which requirements apply to your agent. It adds no requirements of its own; each chapter's `Applicability` statement and requirement triggers decide. The [requirement index](requirement-index.md) lists every requirement and the chapter that owns it.

## How to read the requirements

**MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** show how strongly this draft recommends a practice. They do not mean an organization has adopted the draft, that the older v0.4 material or the skills conform to it, or that a checklist proves legal, regulatory, security, privacy or domain compliance.

A requirement applies when its trigger is true. Read the chapter's `Applicability` statement and the requirement's trigger first. A trigger that is absent is a scoping decision, not a failure; record it when a reviewer would otherwise expect the item.

- **MUST / MUST NOT:** mandatory when it applies. Do not quietly substitute a weaker mechanism.
- **SHOULD / SHOULD NOT:** follow it unless a documented, task-specific reason supports another approach, and keep evidence that the alternative meets the same claim.
- **MAY:** an allowed option. It is not a requirement and grants no authority.
- **Does not apply:** the trigger is absent. Record why, rather than marking an applicable item complete.
- **Governed exception:** allowed only when the governing policy marks that requirement as exception-eligible and an authorized approver records the scope, rationale, compensating controls, owner, expiry or review date, and what happens if it is not completed. An exception is not a general waiver.

## Which Parts apply

These profiles help you navigate. They do not override a chapter's triggers.

### 1. Every production agent

Use [Part 1](development-guide/01-problem-definition-and-planning/README.md) for the problem, intended outcome, simpler alternatives, the initial risk, data and ownership record, and which Parts apply. Use [2.2](development-guide/02-agent-basics/02-agent-contracts-and-configuration.md) for the contract: bounded scope, trusted dependencies, capability admission, output validation, ownership, configuration identity and terminal outcomes. Then apply Parts 3–5 to keep trust boundaries, produce evidence, release deliberately, operate within bounds and keep an owner.

This is a set of decisions every agent makes, not a required architecture. No agent needs a tool, skill, retrieval system, memory store, MCP server, durable engine, approval flow, model judge, queue or second agent just to satisfy it.

### 2. Controls triggered by a capability

Add these chapters when you enable the capability:

- **Tools or external interfaces:** [2.4](development-guide/02-agent-basics/04-tools-and-external-interfaces.md), [3.1](development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) and [3.2](development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).
- **Skills:** [2.5](development-guide/02-agent-basics/05-skills-and-reusable-capabilities.md).
- **Retrieval or memory:** [2.6](development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md), and [8.2](engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md) for transformations, caches and longer-lived memory.
- **MCP:** [2.7](development-guide/02-agent-basics/07-mcp-and-standardized-integrations.md). Discovering a capability over a protocol does not admit or authorize it.
- **Sensitive, personal or non-public data:** [3.3](development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), plus any applicable Part 10 assurance.

### 3. Evaluation

When evidence supports a material decision, [4.6](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) maps each claim to cases, profiles and cadence, and sets the universal evidence core. The core applies to every production candidate, including a simple read-only assistant. It does not require a load-test environment, live study, model judge, tool, memory store, approval flow or second agent. It does require evidence for each in-scope contract claim, relevant boundary, adverse condition, declared limit and applicable critical control.

Add coverage only when its own trigger is present. The [4.6 profile catalogue](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md#additive-profiles) covers retrieval, tools and trajectory, untrusted input, sensitive or tenant scope, effects, approvals, durable recovery, conversation, stored memory and context transformation, composition, shared capacity, human impact, model judges, and model selection and routing. One capability does not imply another: retrieval does not imply stored memory, routing does not imply a model judge, and durable read-only work does not imply approval or an external effect.

For inputs and policies that change (permissions, currentness, user constraints), [4.3](development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md#consistency-relations-and-repeated-run-reliability) explains the two consistency checks: a change that should not matter must not change the outcome, and a change that should matter must. It also requires fresh repeated runs, or a justified alternative, for material claims whose results vary between runs. [4.7](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md#measure-the-product-that-is-actually-released) covers denominators, the retry, selection and fallback policy you actually ship, status handling, clustering and how to interpret the result. A good selected result does not erase the attempts behind it, and it does not prove reliability in the field.

### 4. Release

A pilot is still exposure to users. Before a pilot or release, use [1.4](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md), [Part 4](development-guide/04-testing-and-evaluation/README.md) and [Part 5](development-guide/05-release-operations-and-lifecycle/README.md) in proportion to the proposed use. Calling something a pilot does not turn a prohibited use, a failed hard gate, missing required evidence or a required authorization into a pass.

### 5. Execution and effects

Every agent declares an execution class. [Part 7](engineering-reference/07-durable-execution-and-human-governed-work/README.md) applies when work is long-running, resumable, side-effecting, waiting on approval or consequential. `ephemeral`, `durable` and `human_governed` describe how work runs; they do not set the governance tier or residual risk. Enabling a capability cannot quietly lower the class it needs. Durable recovery does not prove that an external effect happened exactly once, and human approval does not create authority.

### 6. Optional engineering patterns

Use [Part 6](engineering-reference/06-reasoning-and-execution-patterns/README.md) only for explicit planning, reflection or parallel branches. Use [Part 8](engineering-reference/08-model-context-and-resource-engineering/README.md) when the design includes model routing, context transformation, performance optimization, caching, queuing or shared admission. Use [Part 9](engineering-reference/09-multi-agent-systems-and-interoperability/README.md) when two or more model-driven agents contribute to one outcome or an A2A-style remote interaction is enabled. Having several agents does not lower any member's controls, and does not by itself require durable execution.

### 7. Higher assurance

Use [Part 10](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md) when the initial record shows consequential authority, sensitive or regulated context, broad reach, material uncertainty, a material human-impact scenario, or another policy or capability floor. A read-only agent can be high risk. [10.1](engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) has its own triggers, mandatory floors and review intervals; when it applies, the general lifecycle cadence in [5.3](development-guide/05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md) does not replace them.

## What can never be waived

Each chapter defines its own gates. Across the book, none of the following can be turned into a pass by a good average, a narrower pilot or a generic exception:

- a prohibited use;
- an applicable mandatory governance or capability floor;
- required deterministic authorization at a protected operation;
- an applicable non-waivable hard gate or a critical control failure;
- required evidence that is missing, invalid or inconclusive under the declared policy;
- a `critical` residual-risk scenario under the detailed assessment method.

## Readiness states

Each requirement is in one of four states: **met**, **not applicable with rationale**, **unmet and blocking**, or **eligible for a governed exception**. Not applicable means the trigger is absent; it is not an exception. An exception exists only when policy permits one, and it never overrides the list above.

`conditional_go` is available only when policy permits it and all required pre-release evidence and controls are complete. It tracks a permitted post-release obligation with an owner, due date, monitoring signal and consequence if overdue. A required test, authorization, safety, grounding or critical-slice claim, stop control or other launch prerequisite stays blocking until verified. See [4.7](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) and [5.2](development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## Authority, approval and evidence

A model proposal, prompt, retrieved content, tool output, memory, peer message or approval record never grants authority by itself. Authorization is enforced at the protected operation, using trusted context. Approval is an extra condition on an action that is already authorized; it is bound to an exact subject and context, cannot widen a capability, and does not survive a material change. Evidence should show observable decisions, actions, authoritative outcomes and control operation; raw private chain-of-thought is not required.

## Decisions left to the adopting organization

This page does not set an exception catalogue, governance-tier roles, domain thresholds, legal classification, rollout numbers, retention periods or a universal fairness metric. The open proposals and questions are listed in [Draft notes](draft-notes.md).

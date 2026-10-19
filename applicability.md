# Applicability and normative language

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Purpose:** Explain how to decide which draft requirements apply without creating a second set of requirements.
**Use with:** [book home](README.md), [requirement index](requirement-index.md), and the applicability statement in each owner chapter.

## How to read this draft

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express the strength of a requirement **within this proposed 0.5.0-draft.2**. They are not a claim that an organization has adopted the draft, that a legacy document or skill conforms to it, or that a checklist proves legal, regulatory, security, privacy, or domain compliance.

A requirement binds when its stated applicability trigger is true. Read the owner chapter's `Applicability` statement and the requirement's trigger before assessing it. A missing trigger is not a control failure; it is a scoped decision that should be recorded when the item would otherwise be relevant to the release or review.

- **MUST / MUST NOT**: an applicable requirement is mandatory for a conforming use of this draft. Do not silently substitute a weaker mechanism.
- **SHOULD / SHOULD NOT**: follow it unless a documented, task-specific reason supports another approach; preserve evidence that the alternative meets the intended claim.
- **MAY**: a permitted option, not a requirement or authority grant.
- **Does not apply**: the trigger is absent. Record the rationale rather than calling an unmet applicable item complete.
- **Governed exception**: an applicable requirement may be excepted only where the governing policy makes that requirement exception-eligible and an authorized approver records its scope, rationale, compensating controls, owner, expiry/review date, and consequence of non-completion. An exception is not a general waiver.

## Baseline profiles

These profiles are a navigation aid. They do not override chapter-specific triggers or replace the [requirement index](requirement-index.md).

### 1. Every production proposal and agent

Use [Part 1](development-guide/01-problem-definition-and-planning/README.md) to establish the problem, intended outcome, simpler alternatives, initial risk/data/ownership record, and the Parts that apply. Use [2.2](development-guide/02-agent-basics/02-agent-contracts-and-configuration.md) to declare a bounded contract, trusted dependencies, capability admission, output validation, ownership, configuration identity, and terminal outcomes. Use the applicable Parts 3–5 controls to preserve trust boundaries, create evidence, release deliberately, operate within bounds, and maintain ownership.

This is a universal decision layer, not a universal architecture: it does not require a tool, skill, retrieval system, memory store, MCP server, durable engine, human approval flow, model judge, queue, or second agent.

### 2. Capability-triggered controls

Apply the relevant Part 2 and Part 3 chapters when a capability is enabled:

- tools or external interfaces: [2.4](development-guide/02-agent-basics/04-tools-and-external-interfaces.md), [3.1](development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), and [3.2](development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md);
- skills: [2.5](development-guide/02-agent-basics/05-skills-and-reusable-capabilities.md);
- retrieval or memory: [2.6](development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) and, for transformations/caches/longer-lived memory, [8.2](engineering-reference/08-model-context-and-resource-engineering/02-retrieval-memory-and-context-optimization.md);
- MCP: [2.7](development-guide/02-agent-basics/07-mcp-and-standardized-integrations.md); protocol discovery is not admission or authorization;
- sensitive, personal, or non-public data: [3.3](development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), plus applicable Part 10 assurance.

### 3. Evaluation universal core and independently triggered coverage

When Part 4 evidence supports a material decision, use [4.6 Standards, Required Coverage, and Execution Cadence](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md) as the sole owner of the claim-to-case/profile/cadence map and the proportional universal evidence core. The core applies to every production candidate, including a simple read-only assistant. It does not require a distributed load environment, live study, model judge, tool, memory store, approval flow, or second agent; it does require evidence appropriate to each in-scope contract claim, relevant boundary, adverse condition, declared local bound, and applicable critical control.

Select additional coverage only when its independent trigger is present. The [4.6 profile catalogue](development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md#additive-profiles) distinguishes retrieval, tools/trajectory, untrusted input, sensitive/tenant scope, effects, approvals, durable recovery, conversation, stored memory/context transformation, composition, shared capacity, human impact, model judges, and model selection/routing. Its links name the actual security, execution, context, composition, evaluator, and operational owners; retrieval does not imply stored memory, routing does not imply a model judge, and durable read-only work does not imply approval or an external effect.

For semantic or changing inputs and policy, permission, currentness, or user-constraint decisions, use [4.3 Evaluation Types and Dimensions](development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md#consistency-relations-and-repeated-run-reliability) for the applicable reviewed invariance and relevant-change sensitivity relations. For material variable user-visible claims, that owner also requires fresh repeated evidence or a justified alternative that removes variability from the claim. Use [4.7 Analyzing Results, Comparing Versions, and Making Decisions](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md#measure-the-product-that-is-actually-released) for denominators, actual retry/selection/fallback policy, status handling, clustering, and decision interpretation. These are different questions: an attractive selected result neither erases physical attempts nor proves field reliability.

### 4. Release and evidence controls

A pilot is still user exposure. Before a pilot or release, use [1.4](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md), [Part 4](development-guide/04-testing-and-evaluation/README.md), and [Part 5](development-guide/05-release-operations-and-lifecycle/README.md) at a depth proportionate to the proposed use. Narrowing a pilot label cannot turn prohibited use, a failed hard gate, missing required evidence, or a required authorization boundary into a pass.

### 5. Execution and effect controls

Every agent declares an execution class, but [Part 7](engineering-reference/07-durable-execution-and-human-governed-work/README.md) is triggered when work is long-running, resumable, side-effecting, approval-waiting, or consequential. `ephemeral`, `durable`, and `human_governed` describe execution; they do not set the governance tier or residual risk. An enabled capability cannot silently lower the class it requires. Durable recovery is not proof of exactly-once external effects, and human approval does not create authority.

### 6. Optional engineering and composition controls

Use [Part 6](engineering-reference/06-reasoning-and-execution-patterns/README.md) only for explicit planning, reflection, or concurrent branch work. Use [Part 8](engineering-reference/08-model-context-and-resource-engineering/README.md) when model routing, context transformation, performance optimization, caching, queuing, or shared admission is part of the design. Use [Part 9](engineering-reference/09-multi-agent-systems-and-interoperability/README.md) when two or more model-driven agents contribute to one outcome or an A2A-style remote interaction is enabled. A multi-agent design does not lower a member's controls or make durable execution mandatory solely because it has several agents.

### 7. Higher-assurance and specialized controls

Use [Part 10](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md) when the initial record identifies consequential authority, sensitive or regulated context, broad reach, material uncertainty, a material human-impact scenario, or another policy/capability floor. A read-only agent can be high risk. The detailed method in [10.1](engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) supplies its own triggered matrix, mandatory floors, and review intervals; the general lifecycle cadence in [5.3](development-guide/05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md) does not replace them when that method applies.

## Non-waivable boundaries and release states

The owner chapters, not this page, define each actual gate. Across the draft, the following cannot be converted into a pass by a favorable average, a narrowed pilot, or a generic exception:

- a prohibited use;
- an applicable mandatory governance or capability floor;
- required deterministic authorization at a protected operation;
- an applicable non-waivable hard gate or critical control failure;
- required evidence that is missing, invalid, or inconclusive under the declared policy; and
- a `critical` residual-risk scenario under the detailed assessment method.

Use four readiness states: **met**, **not applicable with rationale**, **unmet and blocking**, and **eligible for a governed exception**. `not applicable` means the trigger is absent; it is not an exception. An exception exists only when policy permits one and it never overrides the boundaries above.

`conditional_go` is available only when the applicable policy permits it and all required pre-release evidence and controls are already complete. It can track a permitted post-release obligation with an owner, due date, monitoring signal, and overdue consequence. A required test, authorization, safety/grounding/critical-slice claim, stop control, or other launch prerequisite remains blocking until verified. See [4.7 Analyzing Results, Comparing Versions, and Making Decisions](development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) and [5.2](development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## Approval, authority, and evidence

A model proposal, prompt, retrieved content, tool output, memory, peer message, or approval record does not by itself grant authority. Authorization is enforced from trusted context at the protected-operation boundary. Approval is an additional condition on an already authorized consequential action and binds an exact subject/context; it cannot enlarge capability or survive a material change. Evidence should establish observable decisions, actions, authoritative outcomes, and control operation; raw private chain-of-thought is not required.

## Adoption decisions remain open

This page deliberately does not invent an organizational exception catalogue, governance-tier role structure, domain threshold, legal classification, rollout number, retention duration, or universal fairness metric. The live first-draft proposals and the review questions that need an adopting policy owner are recorded in [Draft notes](draft-notes.md).

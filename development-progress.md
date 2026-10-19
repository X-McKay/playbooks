# Development progress

**Status:** 0.5.0-draft.2 — editorial progress record; proposed, not adopted  
**Purpose:** State completed refinement scope, review boundaries, backlog order, and verified documentation results.  
**Not a conformance record:** This page does not alter requirement wording, IDs, strengths, owner paths, applicability, or adoption status.

## Refined Parts 1–5

Parts **1–5** are refined draft mini-books. Part 1 retains its completed planning increment: [1.1](development-guide/01-problem-definition-and-planning/01-defining-the-problem.md), [1.2](development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), [1.3](development-guide/01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md), and [1.4](development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md), plus four owned planning templates, its overview, practical reference, and glossary pointers. The four scoped Part 1 writer checks were recorded as passed. They remain local proposed edits on the **unmerged assembled draft's structural base**; they are not opened pull requests, independent reviews, or adoption decisions.

The earlier Part 2–3 increment added ten separately reviewable local chapter/template units. Each scoped writer gate was reported as passed; that is a unit result, not a whole-book result.

1. **2.1 Agent Anatomy, Runtime Loop, and Project Organization** + `templates/2.1/agent-anatomy-record.yaml`
2. **2.2 Agent Contracts and Configuration** + `templates/2.2/policy-assistant-contract.yaml`
3. **2.3 Prompts and Instructions** + `templates/2.3/instruction-design-record.yaml`
4. **2.4 Tools and External Interfaces** + `templates/2.4/tool-contract.yaml`
5. **2.5 Skills and Reusable Capabilities** + `templates/2.5/skill-admission-record.yaml`
6. **2.6 Context and Retrieval Fundamentals** + `templates/2.6/context-source-record.yaml`
7. **2.7 MCP and Standardized Integrations** + `templates/2.7/mcp-integration-record.yaml`
8. **3.1 Identity, Authority, Zero Trust, and Least Privilege** + `templates/3.1/authority-boundary-record.yaml`
9. **3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries** + `templates/3.2/content-action-boundary-record.yaml`
10. **3.3 Data Privacy, Handling, and Minimum Audit Evidence** + `templates/3.3/data-handling-audit-record.yaml`

The Part 5 increment adds three separately reviewable local chapter/template units. Each scoped writer gate was reported as passed; that is a local file-only result, not a whole-book result.

1. **5.1 Observability, Budgets, and Operational Control** + `templates/5.1/operating-control-record.yaml`
2. **5.2 Readiness, Change, and Rollout** + `templates/5.2/release-and-rollout-record.yaml`
3. **5.3 Ownership, Incidents, Maintenance, and Retirement** + `templates/5.3/support-incident-and-retirement-record.yaml`

These three units are local proposed edits, **not** opened pull requests or independent reviews. They do not report an authorization, deployment, incident, recovery, retirement, or adoption decision.

The Part overviews now provide learner, builder, and reviewer routes. Their [Part 2 practical reference](development-guide/02-agent-basics/reference/README.md), [Part 3 practical reference](development-guide/03-security-and-trust-boundaries/reference/README.md), and [Part 5 practical reference](development-guide/05-release-operations-and-lifecycle/reference/README.md) index local artifact sequences and own no requirement IDs. The [glossary](glossary.md#part-2-and-part-3-foundations) and [Part 5 glossary pointers](glossary.md#part-5-operational-and-lifecycle-foundations) remain pointers to chapter-local explanations rather than competing definition sets.

## Editorial depth and unchanged ownership

[Part 4](development-guide/04-testing-and-evaluation/README.md) remains the existing detailed seven-chapter pilot mini-book within the refined Parts 1–5 route. Parts **6–10** remain populated first drafts—not empty and not yet reviewed to the refinement depth of Parts 1–5. The [requirement index](requirement-index.md) continues to locate all **208** canonical groups; it does not copy their requirement prose, and this increment changes no canonical owner path or conformance wording.

## Next refinement backlog — reading order

1. **Part 6 — Reasoning and Execution Patterns**, in its existing chapter order:
   1. [6.1 Planning, Decomposition, and Bounded Control Loops](engineering-reference/06-reasoning-and-execution-patterns/01-planning-decomposition-and-bounded-control-loops.md)
   2. [6.2 Reflection, Critique, and Verification](engineering-reference/06-reasoning-and-execution-patterns/02-reflection-critique-and-verification.md)
   3. [6.3 Parallel Work, State, and Failure Propagation](engineering-reference/06-reasoning-and-execution-patterns/03-parallel-work-state-and-failure-propagation.md)
2. **Remaining specialized reference Parts**, in book order: [Part 7](engineering-reference/07-durable-execution-and-human-governed-work/README.md), [Part 8](engineering-reference/08-model-context-and-resource-engineering/README.md), [Part 9](engineering-reference/09-multi-agent-systems-and-interoperability/README.md), then [Part 10](engineering-reference/10-risk-privacy-and-specialized-assurance/README.md).

This is a backlog order, not a commitment to adopt policy or apply every specialized reference mechanism.

## Validation and delivery state

The three Part 5 chapter/template writer gates were reported as passed local file-only checks. They retained the supplied chapter requirement wording and checked chapter/template-local conditions. They are not a final whole-book structural, owner, template, local-link, or Markdown result, and do not establish control effectiveness, authorization, deployment, or adoption.

The prior Parts 2–3 integration record is historical context: all ten Part 2–3 chapter/template gates and its combined whole-book structural, local-link/fragment, citation, and structured-example checks passed after that integration and targeted cleanup. All **55** Part 2–3 requirement bullets remained verbatim; all **208** canonical owner locators were unchanged. The repository's pinned Markdown lint then passed across **148** Markdown files and its offline local-link/fragment check reported **zero** errors. That result is not a final validation result for Part 5.

The Part 5 combined checks passed: all three chapter/template gates, all **18** unchanged canonical Part 5 requirement bullets, all **208** unchanged owner locators, the **40**-chapter structure, and local links/fragments and structured examples. Packet checks confirm common identity/status and valid development-fixture/source/case references without holdout reuse. Parts 1–4 and their companion content, other existing Parts, compatibility trees, and the original checkout remain preserved.

Pinned repository checks passed Markdown lint across **149** files and reported **zero** offline link/fragment errors. A targeted coherence clarification distinguishes the lifecycle record's absence of an actual evaluation from the release record's fictional Part 4 teaching handoff. The final delivery sequence re-tests this clarification and these notes before portable ZIP packaging verifies every bundled file against the source bytes; no validation rule was weakened.

Documentation checks do not establish live-agent performance, external-link availability, legal or regulatory certification, or organizational adoption. No commit, push, pull request, deployment, or skill migration was performed.

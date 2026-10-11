# Playbook Restructure Plan

- **Status:** Proposal, awaiting decisions
- **Goal:** Merge the Agent Playbook and the Multi-Agent Systems Playbook into
  one Agent Development Playbook, organized by topic, that serves as both the
  normative standard behind `.agents/skills/` and the basis for onboarding
  material.

## Why

A section-by-section comparison of both playbooks found:

- Ten of thirteen chapters are mirrored. Roughly 20–30% of each multi-agent
  chapter restates the single-agent chapter, often with small differences.
- Restated material has drifted into **conflicts** (listed under
  [Decisions](#decisions-required-before-merging)): different field names,
  status enums, retry layers, workflow ID formats, and thresholds.
- Several topics are scattered across chapters: approval appears in five
  places, budgets in four, execution classes in five, kill switches in three.
- There are real gaps: testing (as distinct from evals), model and context
  design, MCP, rollout, red-teaming, privacy, and model lifecycle.

Today's two playbooks have about 5,400 lines. The merged playbook is estimated
at about 4,500 lines of merged content plus 800–1,000 lines of new chapters.

## Target structure

Each chapter has a **Baseline** that applies to every agent and, where
relevant, a **Multi-agent extension**. Chapters 8 and 9 apply only to
multi-agent systems.

| #   | Chapter                           | Sources                                                                                                                                      | New material                                                                                    | Est. lines |
| --- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------- |
|     | **Part I: Foundations**           |                                                                                                                                              |                                                                                                 |            |
| 0   | Core concepts and glossary        | AP 00 (new), MA 01 Required distinctions, all execution/effect/tier definitions                                                              | Single definition of every term                                                                 | 300        |
| 1   | Principles, scope, and admission  | AP 01, MA 01, both READMEs' "standard in one page" and conformance                                                                           | "Should this be an agent?" admission test for single agents                                     | 190        |
|     | **Part II: Design**               |                                                                                                                                              |                                                                                                 |            |
| 2   | Architecture and repository       | AP 02, MA 02 (repository, runtime, state ownership, composition manifest)                                                                    | One repository tree; one manifest name                                                          | 230        |
| 3   | Agent and system contracts        | AP 03, MA 03                                                                                                                                 | One spec field glossary; one factory sequence; cross-artifact consistency for single agents     | 360        |
| 4   | Models, instructions, and context | AP 03 Model policy, AP/MA 09 routing, context, caching                                                                                       | Instruction design, retrieval, memory, compaction, model lifecycle and upgrades                 | 250        |
| 5   | Tools, skills, and MCP            | AP 04, AP 05, MA 04 capability intersection and role restrictions                                                                            | MCP servers (allowlisting, pinning, auth, schema drift), tool versioning, tool allowlist syntax | 240        |
| 6   | Human interaction and approval    | AP 06 and MA 06 Human approval, MA 10 Separation of duties, AP 06 Streaming                                                                  | Approval UX, escalation, user feedback capture                                                  | 180        |
| 7   | Multi-agent architecture          | MA 02 Topology profiles and selection, MA 04 Membership and roles                                                                            | —                                                                                               | 300        |
| 8   | Delegation and interactions       | MA 05 (retries, budgets, telemetry moved out)                                                                                                | Agent-as-tool bridge to chapter 5                                                               | 200        |
|     | **Part III: Build**               |                                                                                                                                              |                                                                                                 |            |
| 9   | Durable execution                 | AP 06, MA 06, AP 05 Temporal and side effects, MA 02 Workflow decomposition                                                                  | Nested delegation timeouts; fan-out streaming                                                   | 380        |
| 10  | Testing                           | "Required tests" from AP 06 and MA 06, test layers from AP 07 and MA 07                                                                      | Unit and contract tests, `TestModel`/`FunctionModel`, blocking live model calls, MCP tests      | 200        |
| 11  | Evaluation                        | AP 07, MA 07                                                                                                                                 | Judge calibration on model change                                                               | 380        |
|     | **Part IV: Operate**              |                                                                                                                                              |                                                                                                 |            |
| 12  | Observability                     | AP 08, MA 08                                                                                                                                 | Alert → runbook → severity links                                                                | 330        |
| 13  | Cost and capacity                 | AP 09, MA 09 (routing and context moved to chapter 4)                                                                                        | —                                                                                               | 280        |
| 14  | Release and operations            | AP/MA 10 Deployment, Kill switches, Incident response; both Optimization rollouts; MA 04 Lifecycle                                           | Rollout stages mapped to governance tier; on-call; model upgrade rollout                        | 220        |
|     | **Part V: Govern**                |                                                                                                                                              |                                                                                                 |            |
| 15  | Security                          | AP/MA 10 security sections (threat and trust models, identity, untrusted content, secrets, supply chain, isolation, shared state, protocols) | Red-team process; privacy and data retention                                                    | 330        |
| 16  | Risk and governance               | AP 13, MA 13, AP/MA 10 Risk tiers, Ownership, Change classes, Exceptions, Decommissioning                                                    | Regulatory notification duties; provider risk review cadence                                    | 420        |
| 17  | Production readiness              | AP 11, MA 11, PR evidence (AP 12 and MA 11), approval record                                                                                 | Checklist links to requirements instead of restating them                                       | 120        |
|     | **Appendices**                    |                                                                                                                                              |                                                                                                 |            |
| A   | Reference implementation          | AP 12, MA 12 (deferred until the example agent exists)                                                                                       | —                                                                                               | —          |
| B   | Templates                         | Both `templates/` directories, with field names aligned                                                                                      | —                                                                                               | —          |
| C   | References                        | Both `references.md`                                                                                                                         | —                                                                                               | —          |

AP = `agent-playbook/`, MA = `multi-agent-playbook/`.

## Chapter template

Every chapter uses the same layout so readers and skills can find things:

```markdown
# N. Title

One paragraph: what this chapter covers and why it matters.

## Key concepts            <!-- links to chapter 0; no new definitions -->
## Baseline                <!-- requirements for every agent -->
## Multi-agent extension   <!-- only what composition adds or changes -->
## Anti-patterns           <!-- common mistakes, with the fix -->
## Readiness checks        <!-- links to the requirements above, never restated -->
## Related skills          <!-- which .agents/skills apply this chapter -->
```

Rules:

- A requirement is stated once, in the chapter that owns the topic. Other
  chapters link to it.
- Numeric values in examples (thresholds, budgets) are labelled as
  illustrative unless the playbook sets them as defaults.
- The multi-agent extension never restates or weakens a baseline rule. If a
  stricter rule applies, it says so explicitly.

## Decisions required before merging

The comparison found these conflicts. Each must be settled once, in chapter 0
or the owning chapter, before that chapter is merged.

| #   | Conflict                                                                                                                                                                                          | Recommendation                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Does a member agent run as a Temporal **activity**, or as a loop inside the workflow with each model and tool call as its own activity? MA 01 says the former, AP 01/02 the latter, MA 06 hedges. | Loop in the workflow (AP model), with child workflows for members that need their own durability. Activities stay single I/O steps. |
| 2   | `risk_tier` vs `governance_tier`                                                                                                                                                                  | `governance_tier` everywhere; it is distinct from inherent and residual risk.                                                       |
| 3   | `budgets` vs `limits`; `max_requests` vs `max_model_requests`; time budget missing from the Agent Spec                                                                                            | `limits`, with one field set shared by agents and systems, including `deadline_seconds`.                                            |
| 4   | Workflow ID format (`<workflow-type>` vs `<system>`)                                                                                                                                              | `<environment>:<tenant>:<workflow-type>:<business-id>:<request-id>`; systems use their system name as the type.                     |
| 5   | Retry layers (4 in AP, 5 in MA 05, 7 in MA 06) and non-retryable lists                                                                                                                            | One ordered list in chapter 9, extended (not redefined) for interactions.                                                           |
| 6   | Final status and outcome enums (7 vs 11 states; `timeout` vs `deadline_exceeded`; overlapping partial-effect states)                                                                              | One enum in chapter 3, shared by contracts, telemetry, and evals.                                                                   |
| 7   | Approval invalidation: MA lets a policy declare a change "immaterial"                                                                                                                             | Keep the stricter AP rule: any change to material arguments, security context, composition, or policy invalidates approval.         |
| 8   | Tier requirements table vs text: threat model (Medium or High?), risk assessment (all agents or Medium+?), kill switch (all or Critical?)                                                         | Risk assessment and tested kill switch for every agent; threat model from Medium. Fix the table to match.                           |
| 9   | Review intervals: "suggested" (AP 10) vs "maximum" (AP 13)                                                                                                                                        | Maximum.                                                                                                                            |
| 10  | Independent review tied to governance tier (AP 10) or residual risk (AP 13)                                                                                                                       | Both, stated once in chapter 16 as separate triggers.                                                                               |
| 11  | Threat model required for all systems (MA) vs Medium+ agents (AP)                                                                                                                                 | Medium+ for agents; every multi-agent system, because composition adds trust boundaries.                                            |
| 12  | Release thresholds differ (success 0.90 vs 0.92, p95 25 s vs 30 s, cost $0.20 vs $1.50)                                                                                                           | Treat all as illustrative; teams set them in their evaluation policy.                                                               |
| 13  | Cost growth alerts: low urgency (AP) vs urgent page for runaway spend (MA)                                                                                                                        | Both: gradual growth is low urgency; budget exhaustion or runaway spend pages.                                                      |
| 14  | Template field drift (`requirement`/`due_by` vs `description`/`due_at`/`consequence_if_unmet`)                                                                                                    | Adopt the MA template fields, which match the text of AP 13.                                                                        |
| 15  | Versions (AP v0.3, MA v0.1)                                                                                                                                                                       | Merged playbook is v0.4.                                                                                                            |

## Skills mapping

| Chapter                                 | Skills                                                                  |
| --------------------------------------- | ----------------------------------------------------------------------- |
| 1–3 Principles, architecture, contracts | `design-pydantic-agent`, `design-multi-agent-system`                    |
| 4 Models, instructions, context         | **new:** `design-agent-context`                                         |
| 5 Tools, skills, MCP                    | `design-agent-capabilities`                                             |
| 6 Human interaction                     | covered by `implement-temporal-agent`; revisit after the chapter exists |
| 7–8 Multi-agent                         | `design-multi-agent-system`, `design-agent-interactions`                |
| 9 Durable execution                     | `implement-temporal-agent`, `implement-temporal-multi-agent`            |
| 10 Testing                              | **new:** `test-agent`                                                   |
| 11 Evaluation                           | `build-agent-evals`, `build-multi-agent-evals`                          |
| 12–14 Operate                           | `operate-agent-production`, `operate-multi-agent-system`                |
| 15–16 Security, risk                    | `assess-agent-risk`, `assess-multi-agent-risk`                          |
| 17 Readiness                            | `review-agent-readiness`, `review-multi-agent-readiness`                |

Single-agent and multi-agent skills stay separate: narrow descriptions trigger
more reliably. Each skill's `references/standard.md` is rewritten against its
merged chapter as that chapter lands.

## Migration plan

The merged playbook stays in `agent-playbook/`, retitled **Agent Development
Playbook**, so existing links and history survive. Only one file outside the
playbooks links to a chapter today.

1. **Decisions.** Settle the table above.
2. **Skeleton.** Rename chapters to the new numbering with `git mv`, add stub
   files for new chapters, and update the README contents. The multi-agent
   playbook stays in place, with a banner pointing to the merged chapters as
   they land.
3. **Merge chapter by chapter**, one pull request each. Merging a chapter is
   also its content review: resolve conflicts, cut restatements, fix misplaced
   material, and update the matching skills. Suggested order, because later
   chapters depend on terms settled earlier:
   1. Chapters 0–3 (terms, principles, architecture, contracts)
   2. Chapters 5, 9 (tools, durable execution)
   3. Chapters 10, 11 (testing, evaluation)
   4. Chapters 12–14 (operate)
   5. Chapters 15–17 (govern)
   6. Chapters 6–8 (human interaction, multi-agent)
4. **New chapters:** 4 (models and context) and 10 (testing) first; 6 and 14
   next.
5. **Retire** `multi-agent-playbook/` once every section has a new home, and
   leave a README pointing to the merged chapters.
6. **Later:** requirement IDs and generated skill references (needs
   `agentctl`).

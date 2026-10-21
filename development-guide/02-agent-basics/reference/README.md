# Part 2 practical reference

**Status:** 0.5.0-draft.2 — draft  
**Purpose:** Connect the Part 2 design records in one build and review sequence without creating a second set of requirements.  
**Use with:** The [Part 2 overview](../README.md), its chapters, the [glossary pointers](../../../glossary.md#part-2-and-part-3-foundations), and the [requirement index](../../../requirement-index.md#part-2--agent-basics).

This reference owns **no requirement IDs**. If this page or a template is shorter than a requirement, the chapter's `## Requirements` section controls. The records share a fictional `POLICY-BUILD-001` / `internal-policy-assistance` example and are `illustrative-unexecuted`: they describe a design, not an assembly, admission, evaluation, deployment, or external effect.

## Build one bounded design

1. **Make the candidate understandable.** Use [2.1](../01-agent-anatomy-runtime-loop-and-project-organization.md) with the [agent anatomy record](../../../templates/2.1/agent-anatomy-record.yaml). Say which responsibility belongs to the model, the runtime, configuration, per-run state, and the boundary that observes a terminal result.
2. **Declare the contract before enabling a capability.** Use [2.2](../02-agent-contracts-and-configuration.md) with the [policy-assistant contract](../../../templates/2.2/policy-assistant-contract.yaml). Carry forward the task, terminal outcomes, trusted dependencies, desired versus effective capability information, and unresolved fields.
3. **Identify behavior guidance separately.** Use [2.3](../03-prompts-and-instructions.md) with the [instruction-design record](../../../templates/2.3/instruction-design-record.yaml). Keep the instruction revision and expected behavior visible; instructions are not authority or enforcement.
4. **Add only an applicable interface or package record.** Use each only when that capability is proposed; a record is not an admission decision.
   - [Tool contract](../../../templates/2.4/tool-contract.yaml): typed interface, target and effect, validation, timeout and retry.
   - [Skill-admission record](../../../templates/2.5/skill-admission-record.yaml): package and dependency identity, selection, open admission evidence, safe failure.
   - [Context-source record](../../../templates/2.6/context-source-record.yaml): source currentness, access, and lineage; retrieval and transformation; cache and memory decisions.
   - [MCP integration record](../../../templates/2.7/mcp-integration-record.yaml): protocol surface, version-aware discovery and admission, identity limits, re-admission triggers.
5. **Hand off open questions.** Send authority, untrusted content, and data handling to [Part 3](../../03-security-and-trust-boundaries/README.md); claims and fixtures to [Part 4](../../04-testing-and-evaluation/README.md); durable or consequential work to [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) when its trigger is present.

## Practical review use

Keep the records consistent: a capability named in the contract needs a matching record, and an absent capability must not look available because a package exists or a server advertises it. Current or superseded source status and requester permission are facts enforced at their owners' boundaries. A fixed workflow may use these artifacts; a bounded adaptive alternative may choose among an explicitly admitted finite set. Neither removes the need for Part 3 controls or Part 4 evidence.

Use the records to expose unknowns, not to fill them with defaults. In the example, two equally authoritative current policy sources that disagree lead to `needs_information` (clarify or escalate), not a choice by date, and the assistant has no write or approval capability. See the [Part 2 overview](../README.md) for routes through the chapters and [Applicability](../../../applicability.md) before treating an optional mechanism as required.

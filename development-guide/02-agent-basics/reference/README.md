# Part 2 practical reference

**Status:** 0.5.0-draft.2 — refined draft companion; proposed, not adopted  
**Purpose:** Connect the Part 2 design records in a usable build and review sequence without creating a second set of requirements.  
**Use with:** The [Part 2 overview](../README.md), its owner chapters, the [glossary pointers](../../../glossary.md#part-2-and-part-3-foundations), and the [requirement index](../../../requirement-index.md#part-2--agent-basics).

This reference owns **no requirement IDs**. The owner chapter, its applicability statement, and its `## Requirements` section control if this page or a template is shorter than the proposed requirement. The records use the shared fictional `POLICY-BUILD-001` / `internal-policy-assistance` example and are `illustrative-unexecuted`; they do not report assembly, admission, authorization, evaluation, deployment, or an external effect.

## Build one bounded design packet

1. **Make the candidate understandable.** Use [2.1](../01-agent-anatomy-runtime-loop-and-project-organization.md) with the [agent anatomy record](../../../templates/2.1/agent-anatomy-record.yaml). Identify which responsibility belongs to the model, the surrounding runtime, configuration, per-run state, and the boundary that observes a terminal result.
2. **Declare the contract before enabling a capability.** Use [2.2](../02-agent-contracts-and-configuration.md) with the [policy-assistant contract](../../../templates/2.2/policy-assistant-contract.yaml). Carry the accepted task, terminal outcomes, trusted dependencies, desired versus effective capability information, and unresolved construction fields forward.
3. **Identify behavior guidance separately.** Use [2.3](../03-prompts-and-instructions.md) with the [instruction-design record](../../../templates/2.3/instruction-design-record.yaml). Keep the instruction revision and expected bounded behavior visible; do not use instructions as authority or runtime enforcement.
4. **Add only an applicable interface or package record.** Use the [tool contract](../../../templates/2.4/tool-contract.yaml), [skill-admission record](../../../templates/2.5/skill-admission-record.yaml), [context-source record](../../../templates/2.6/context-source-record.yaml), or [MCP integration record](../../../templates/2.7/mcp-integration-record.yaml) only when that capability is proposed. A record is not an admission decision.
5. **Hand off open questions.** Route authority, untrusted content, and data handling to [Part 3](../../03-security-and-trust-boundaries/README.md); route claims and fixtures to [Part 4](../../04-testing-and-evaluation/README.md); route durable or consequential work to [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) when its trigger is present.

## Artifact index

- [Agent anatomy record](../../../templates/2.1/agent-anatomy-record.yaml) — visible responsibilities, runtime boundary, state/configuration distinction, and project-evidence handoff.
- [Policy-assistant contract](../../../templates/2.2/policy-assistant-contract.yaml) — bounded interface, outcomes, dependencies, capability declaration, and effective-configuration planning fields.
- [Instruction-design record](../../../templates/2.3/instruction-design-record.yaml) — task guidance, instruction/data separation, revision identity, and expected behavior cases.
- [Tool contract](../../../templates/2.4/tool-contract.yaml) — typed interface, target/effect questions, validation, timeout/retry, and evidence handoff.
- [Skill-admission record](../../../templates/2.5/skill-admission-record.yaml) — package/dependency identity, proposed selection, unresolved admission evidence, and safe failure.
- [Context-source record](../../../templates/2.6/context-source-record.yaml) — source currentness/access/lineage, retrieval and transformation questions, and cache or memory handoffs.
- [MCP integration record](../../../templates/2.7/mcp-integration-record.yaml) — proposed protocol surface, version-aware discovery/admission questions, identity limits, and re-admission triggers.

## Practical review use

Keep the packet internally consistent: a capability named in the contract should have a matching applicable record, and an absent capability should not appear as available because a package is present or a server advertises it. Keep current/superseded source status and requester permission as facts to be enforced at their owners’ boundaries. A fixed workflow may use these artifacts; a bounded adaptive alternative may choose among an explicitly admitted finite set. Neither pattern removes the need for Part 3 controls or Part 4 evidence.

Use the records to expose unknowns, not to fill them with defaults. The illustrative source conflict is a clarification/escalation condition, and the fictional assistant has no enabled write or approval capability. Read the [Part 2 overview](../README.md) for routes through the chapters and [Applicability](../../../applicability.md) before treating an optional reference mechanism as required.

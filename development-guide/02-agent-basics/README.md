# Part 2 — Agent Basics

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted  
**Audience:** Learners who need a bounded mental model; builders who need reviewable design artifacts; and reviewers who need to trace a capability from declaration to evidence.  
**Scope:** Define bounded agent behavior, contracts, instructions, and the optional capabilities that may support them. This Part does not authorize an action, decide source authority, replace protected-operation checks, or establish that a candidate works.  
**Applicability:** The contract material applies to every agent. Tools, skills, retrieval or memory, and MCP apply only when their stated triggers are present and a candidate enables them.  
**Output:** A reviewable anatomy and contract, configuration/capability identity, instruction identity, and—where enabled—bounded capability records.

[Playbook home](../../README.md) · [Section index](../README.md) · [Part 1 planning](../01-problem-definition-and-planning/README.md) · [Part 3 trust boundaries](../03-security-and-trust-boundaries/README.md) · [Glossary pointers](../../glossary.md#part-2-and-part-3-foundations) · [Requirement index](../../requirement-index.md)

## Start with the right prerequisite

Begin with [Part 1](../01-problem-definition-and-planning/README.md) when the user need, bounded task, expected value, alternative, scope, initial risk, or accountable ownership is still unclear. Use this Part once that planning packet gives a candidate a reviewable purpose. Continue to [Part 3](../03-security-and-trust-boundaries/README.md) before treating identity, authority, hostile content, retention, or audit handling as settled. Use [Part 4](../04-testing-and-evaluation/README.md) to turn a design claim into evidence; a filled record is not evidence of effectiveness or a release decision.

## Routes through this mini-book

**Learner route.** Read [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md), [2.2](02-agent-contracts-and-configuration.md), and [2.3](03-prompts-and-instructions.md) in order. Then take one optional-capability branch only when it is relevant: [2.4](04-tools-and-external-interfaces.md), [2.5](05-skills-and-reusable-capabilities.md), [2.6](06-context-and-retrieval-fundamentals.md), or [2.7](07-mcp-and-standardized-integrations.md).

**Builder route.** Start a bounded design record with [2.2](02-agent-contracts-and-configuration.md), use [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md) to make implementation responsibilities inspectable, and use [2.3](03-prompts-and-instructions.md) to identify instructions. Add only the records for capabilities actually proposed, then hand authority and data questions to Part 3 and claims/evidence to Part 4.

**Reviewer route.** Begin at [2.2](02-agent-contracts-and-configuration.md): identify the effective configuration, terminal outcomes, permitted capability set, and unresolved fields. Trace the runtime boundary in [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md), then inspect every enabled optional capability in its owner chapter. Confirm that an instruction, schema, package, discovery response, or model output has not been treated as authorization or as proof of an external effect.

## Canonical topic sequence

1. [2.1 Agent Anatomy, Runtime Loop, and Project Organization](01-agent-anatomy-runtime-loop-and-project-organization.md) separates model proposals from the surrounding runtime and makes project evidence findable.
2. [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) declares the bounded interface, configuration, outcomes, dependencies, and effective configuration identity.
3. [2.3 Prompts and Instructions](03-prompts-and-instructions.md) develops reviewable instructions and their limits.
4. [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) applies when an external interface is enabled.
5. [2.5 Skills and Reusable Capabilities](05-skills-and-reusable-capabilities.md) applies when a reusable package or capability is proposed.
6. [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md) applies when source material, retrieval, transformation, caching, or memory is in scope.
7. [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) applies when an MCP integration is proposed.

## Practical workflow and artifact index

1. **Name the bounded candidate.** Carry forward the Part 1 task, assumptions, scope, and accountable handoffs. Use [2.1’s anatomy record](../../templates/2.1/agent-anatomy-record.yaml) to distinguish the model, runtime, state, checks, and observable terminal result.
2. **Declare the contract before adding capability.** Use the [contract record](../../templates/2.2/policy-assistant-contract.yaml) to expose accepted input, outcomes, dependencies, effective configuration, and unresolved policy fields.
3. **Make behavior and capability claims inspectable.** Use the [instruction record](../../templates/2.3/instruction-design-record.yaml), then add only the applicable [tool](../../templates/2.4/tool-contract.yaml), [skill](../../templates/2.5/skill-admission-record.yaml), [context/source](../../templates/2.6/context-source-record.yaml), or [MCP integration](../../templates/2.7/mcp-integration-record.yaml) record.
4. **Hand off rather than infer.** Send protected-operation and data questions to Part 3; send testable claims, fixtures, and evidence needs to Part 4; send durable or consequential work to Part 7 when its trigger exists.

The [Part 2 practical reference](reference/README.md) explains how these artifacts fit into one illustrative, unexecuted packet. It owns no requirement IDs. Read the [glossary](../../glossary.md#part-2-and-part-3-foundations) as a pointer to local explanations, and the [requirement index](../../requirement-index.md#part-2--agent-basics) only to locate the canonical owner wording.

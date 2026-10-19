# Part 2 — Agent Basics

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Learners who need a bounded mental model; builders who need reviewable design artifacts; and reviewers who need to trace a capability from declaration to evidence.  
**Scope:** Define bounded agent behavior, contracts, instructions, and the optional capabilities that support them. This Part does not authorize an action, decide source authority, or replace protected-operation checks.  
**Applicability:** The contract material applies to every agent. Tools, skills, retrieval or memory, and MCP apply only when their triggers are present and a candidate enables them.  
**Output:** A reviewable anatomy and contract, configuration and capability identity, instruction identity, and, where enabled, bounded capability records.

[Playbook home](../../README.md) · [Section index](../README.md) · [Part 1 planning](../01-problem-definition-and-planning/README.md) · [Part 3 trust boundaries](../03-security-and-trust-boundaries/README.md) · [Glossary pointers](../../glossary.md#part-2-and-part-3-foundations) · [Requirement index](../../requirement-index.md)

## Start with the right prerequisite

Begin with [Part 1](../01-problem-definition-and-planning/README.md) if the user need, bounded task, expected value, alternatives, scope, initial risk, or ownership is unclear. Continue to [Part 3](../03-security-and-trust-boundaries/README.md) before treating identity, authority, hostile content, retention, or audit handling as settled. Use [Part 4](../04-testing-and-evaluation/README.md) to turn a design claim into evidence; a filled record is not evidence of effectiveness.

## Routes through this mini-book

**Learner route.** Read [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md), [2.2](02-agent-contracts-and-configuration.md), and [2.3](03-prompts-and-instructions.md) in order. Then take one optional branch when relevant: [2.4](04-tools-and-external-interfaces.md), [2.5](05-skills-and-reusable-capabilities.md), [2.6](06-context-and-retrieval-fundamentals.md), or [2.7](07-mcp-and-standardized-integrations.md).

**Builder route.** Start a design record with [2.2](02-agent-contracts-and-configuration.md), use [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md) to make implementation responsibilities inspectable, and use [2.3](03-prompts-and-instructions.md) to identify instructions. Add records only for capabilities you propose.

**Reviewer route.** Begin at [2.2](02-agent-contracts-and-configuration.md): find the effective configuration, terminal outcomes, permitted capability set, and unresolved fields. Trace the runtime boundary in [2.1](01-agent-anatomy-runtime-loop-and-project-organization.md), then inspect each enabled optional capability in its chapter. Confirm that no instruction, schema, package, discovery response, or model output is treated as authorization or proof of an external effect.

## Canonical topic sequence

1. [2.1 Agent Anatomy, Runtime Loop, and Project Organization](01-agent-anatomy-runtime-loop-and-project-organization.md) separates model proposals from the surrounding runtime and makes project evidence findable.
2. [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) declares the bounded interface, configuration, outcomes, dependencies, and effective configuration identity.
3. [2.3 Prompts and Instructions](03-prompts-and-instructions.md) develops reviewable instructions and their limits.
4. [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) applies when an external interface is enabled.
5. [2.5 Skills and Reusable Capabilities](05-skills-and-reusable-capabilities.md) applies when a reusable package or capability is proposed.
6. [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md) applies when source material, retrieval, transformation, caching, or memory is in scope.
7. [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) applies when an MCP integration is proposed.

## Practical workflow and artifact index

Build the design record in this order: the [anatomy record](../../templates/2.1/agent-anatomy-record.yaml) and the [contract record](../../templates/2.2/policy-assistant-contract.yaml) first, then the [instruction record](../../templates/2.3/instruction-design-record.yaml), then only the applicable [tool](../../templates/2.4/tool-contract.yaml), [skill](../../templates/2.5/skill-admission-record.yaml), [context/source](../../templates/2.6/context-source-record.yaml), or [MCP integration](../../templates/2.7/mcp-integration-record.yaml) record. Send protected-operation and data questions to Part 3, testable claims to Part 4, and durable or consequential work to Part 7 when triggered.

The [Part 2 practical reference](reference/README.md) shows how these artifacts fit together in one fictional example and owns no requirement IDs. The [glossary](../../glossary.md#part-2-and-part-3-foundations) points to local explanations, and the [requirement index](../../requirement-index.md#part-2--agent-basics) locates each requirement.

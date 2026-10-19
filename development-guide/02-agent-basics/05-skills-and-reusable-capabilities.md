# 2.5 Skills and Reusable Capabilities

**Status:** 0.5.0-draft.2 — draft

**Audience:** Agent developers, skill authors, capability owners, and reviewers

**Applicability:** Skills are optional. Apply this chapter when a reusable skill package is proposed, discovered, selected, admitted, loaded, changed, or combined with another skill. An agent with no skills still needs the contract and capability boundary in [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md).

**Reader question:** When does reusable guidance deserve to be a skill, and how do you make its selection, dependencies, authority limits, and evidence reviewable without treating a package as a permission grant?

[Part 2 — Agent Basics](README.md) · [Playbook applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) · [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md)

## Purpose and applicability

A **skill** is a reusable package of task-specific guidance: a procedure, relevant knowledge, boundaries, and a way to recognize when it fits. Packaging makes a procedure easier to find, revise, and evaluate without repeating it in every agent, but it adds a behavior-changing dependency. A vague description can select the wrong procedure, a changed reference can change behavior when the main file did not, and bundled executable material can be mistaken for a capability.

A skill is optional and grants no permission. The agent contract defines the effective capability set and its enforcing boundaries; a skill can explain how to use an admitted read operation but cannot make it available, widen its scope, or make its result authoritative. Tool contracts, identity, authorization, and untrusted content stay with [2.4](04-tools-and-external-interfaces.md) and [Part 3 — Security and Trust Boundaries](../03-security-and-trust-boundaries/README.md).

A fixed workflow selects from an explicit list of admitted skills at a defined step; a bounded adaptive agent can choose among a finite admitted set but cannot enlarge it. In both, using a skill is separate from permission to access data or act.

## Working model

### What a skill is, and is not

A **prompt or instruction** guides behavior in one interaction or across an agent. A **skill package** organizes such guidance with supporting material for a bounded class of work. A **tool** is an executable interface that reads or changes something outside the model, with a contract for inputs, effects, authorization, and failures. An **agent** is the configured runtime with an input and output contract, state, and effective capability set; it may use a skill but is not one.

An **MCP integration** is different again: a host-client-server protocol whose servers can expose tools, resources, and prompts. It connects components; it is neither a procedure package nor an authorization decision. A skill may say when an admitted integration is useful, but a package file and an advertised protocol capability are both only candidates until the agent's boundary admits them. [4]

The open Agent Skills format is one portable convention. A skill is a directory with a required `SKILL.md` holding YAML metadata and Markdown instructions, optionally with scripts, references, assets, or other files. It requires a `name` (at most 64 characters, lowercase letters, digits and hyphens, no leading, trailing or consecutive hyphens, matching the parent directory name) and a `description` (at most 1024 characters); optional fields include `license`, `compatibility`, `metadata`, and `allowed-tools`. There is no version field, so a semantic version kept in `metadata` is a local convention. Progressive disclosure loads metadata (about 100 tokens) at startup, instructions on activation (under 5,000 tokens and 500 lines recommended), and referenced files when needed, kept one level deep. `allowed-tools` is experimental and support varies. [1] Runtimes load resources differently, and metadata is not enforcement.

The requirements below are local rules, not obligations from the format. A parser confirms only structure; ownership, versioning, identity, dependency checks, review, and evaluation are local, and a valid format, familiar source, or listing says nothing about admission.

### Four separate decisions

Do not collapse these into "the skill is available":

- **Discovery** makes candidate metadata visible. A package in a shared location may be discoverable without being usable.
- **Admission** puts a specific resolved package, bound to a source and identity rather than a name, into the agent's reviewed allowlist and effective capability manifest.
- **Selection and loading** decide whether an admitted skill fits this task and whether its instructions or resources enter context. Selection cannot add a skill, tool, source, credential, or permission.
- **Execution** happens only when a separately admitted capability is invoked through its own validated and authorized path. A script named by a skill is only material until then.

A package may be discovered but not admitted, or admitted but not selected; a selected procedure may propose a tool call the boundary rejects; a dispatched call still needs target evidence before you claim an effect. None proves the others.

### Package identity and dependencies

Treat a skill as a resolved dependency, not a mutable label. Pin the admitted identity, and treat content that no longer matches it as a new, unreviewed package; this catches a changed reference or a silently updated upstream skill. A semantic version communicates intended change; a recorded source and immutable content identity say what was reviewed. The identity must cover all behavior-relevant material: references, output-shaping assets, and executable material a runtime might load, not only the entry file.

NIST's Secure Software Development Framework (version 1.1) gives examples of recording provenance, verifying integrity, and reviewing third-party components, and SLSA defines provenance as verifiable information about where, when, and how an artifact was produced. [2] [3] These give traceability, not proof that a package is safe, accurate, or authorized.

A **dependency inventory** names what the procedure needs and why: an admitted tool, resource loader, source type, execution environment, or data contract. If a required dependency is missing or mismatched, stop or return the declared bounded result, or use an alternative only if it was separately assessed. Never promote an optional dependency to a required capability mid-task.

## Decisions and best practices

### Choose a skill boundary worth reusing

Create a skill when a coherent procedure or body of knowledge recurs across bounded tasks, has an accountable owner, and benefits from independent review or evaluation. A short, stable direction for every task belongs in general instructions, a one-off request may need no package, and a mainly executable unit needs a tool contract, not prose.

Each package adds selection surface, identities, context, and interactions to test. Do not split one procedure to build a catalogue, or merge unrelated procedures because they share a source or tool; choose the smallest reusable unit whose activation, dependencies, and completion can be assessed together.

The description is the selection interface. Say when the skill fits and when it does not, naming the task condition rather than a topic: "answer a permitted question from current policy evidence" separates answering from policy maintenance. Write it in the third person with the phrases a requester would use. State completion as a task result, such as a bounded answer with source evidence or a `needs_information` result naming the missing evidence, not as the model saying it followed instructions. [5]

### Resolve before use; compose deliberately

Before admission, resolve the name against the agent's sources and record the result in the admission record and capability manifest. A duplicate or ambiguous name resolved by search order can swap in a different package with no visible contract change. A shared catalogue serves discovery but does not skip resolution.

Two skills may compete for a task, prescribe incompatible ordering, or each assume the other owns a decision. Prefer one procedure per responsibility; when two must cooperate, record their order, shared dependencies, information boundary, and the bounded outcome for a conflict or missing dependency. Composition must not stitch together broader authority.

The specification gives no universal loading guarantee, so put indispensable guidance in material the runtime is known to load and declare the rest as a dependency. [1] A procedure assuming an unread reference can look complete while missing its essential step.

### Keep authority at the actual boundary

A skill can suggest an action but never authorize one. Its prose, metadata, label, version, manifest entry, or identity cannot grant document access, select a tenant, enable a tool, or approve an effect, and requests, retrieved material, tool output, and other package content cannot rewrite the allowlist. Authorization belongs at the protected operation ([3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)).

This holds for read-only guidance too: a skill that says to search for a policy cannot make every policy visible, and a read can still disclose information. A bundled script selected by a skill still needs its own admitted capability, tool contract, authorization, and effect handling ([2.4](04-tools-and-external-interfaces.md), [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)).

### Common failure modes

- **Vague description.** A sound procedure activates for unrelated requests or is skipped for its own task; test positive, negative, and ambiguous selection.
- **Shallow format check.** It misses a changed reference or unresolved dependency; review the whole behavior-relevant package.
- **Silent expansion by discovery.** A new package appears in a shared location outside the reviewed allowlist; never pick whichever source appears first.
- **Overgeneralization.** A broad "handle policies" skill blurs answering, maintenance, access administration, and incident handling, hiding which exclusion or dependency applied. Split responsibilities and return a bounded outcome for out-of-scope requests.
- **Evidence mistaken for proof.** An admission record shows a proposal, a format check what it ran, and a manifest identity traceability; none proves source authority, authorization, or safe behavior.

### Build an admission record

Use the [skill-admission record](../../templates/2.5/skill-admission-record.yaml) as a planning aid, not deployment configuration.

1. **Scope.** From the user task and agent contract, decide whether reusable guidance is needed and name its one responsibility, activation conditions, procedure, safety constraints, and observable completion.
2. **Inventory.** Record source, intended semantic version, immutable identity, and all behavior-relevant material. List each required dependency and the observation that confirms it; an unresolvable one blocks admission or needs a separately evaluated fallback.
3. **Compare with the contract.** Identify the admitted read-only capability the procedure may guide and the desired actions that stay absent, record discoverable but unadmitted packages separately, and check that the name resolves uniquely and the description promises no extra authority.
4. **Plan evidence in proportion to the change.** Validate format, inspect the package boundary, estimate context cost at each loading stage (the specification's recommended limits are a starting budget), and design selection cases. If the procedure guides tool choice, include allowed, denied, malformed, and unavailable paths. Write evaluation cases before the skill, compare against the agent without it, and test on each model size you plan to run. [5] Part 4 owns method and interpretation.

## Requirements

- **SKILL-01** — When an agent uses a skill, the admitted skill MUST NOT add capabilities, permissions, or authority beyond the agent’s declared effective capability set; skill prose, metadata, and bundled files MUST NOT authorize an operation. The bounded capability-set requirement is defined in [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md).
- **SKILL-02** — A production agent that uses skills MUST explicitly allowlist the skills admitted to it and MUST NOT enable every discovered skill by default. Names MUST be unique across the agent’s resolved skill sources; ambiguous or duplicate resolution MUST fail closed before the affected agent is used.
- **SKILL-03** — Each skill admitted to a production agent MUST have an accountable owner, a stable, unique, lowercase hyphenated name, a semantic version, a recorded source, and an immutable content identity for the resolved package, including behavior-relevant bundled or referenced content. A changed package MUST receive a new content identity; a behavior-relevant change MUST be reviewed against the prior version before release.
- **SKILL-04** — A production skill MUST state when it applies and when it does not, the procedure it supplies, its safety constraints, and observable completion criteria. It MUST NOT contain secrets or claim authority. Dependencies required for that procedure MUST be identified and checked; if a required dependency is unavailable or does not match the admitted identity, the runtime MUST stop or use a separately evaluated fallback rather than silently assume it is present.
- **SKILL-05** — When a skill bundles or references executable material, the agent MUST NOT execute it solely because the skill mentions or contains it. Execution MUST be separately admitted and authorized under the applicable tool and security requirements.
- **SKILL-06** — Before a skill is used in production, its owner MUST validate its format, measure its context cost, and evaluate positive activation, negative activation, and plausible ambiguous-selection cases, along with procedure and safety adherence and any tool-selection behavior it guides. A behavior-relevant version change MUST be evaluated against the previous version for material regressions. Each run SHOULD record the available and loaded skills, their versions and content identities, load count, and instruction tokens, subject to the applicable data-handling policy.

## Worked example: current policy answers

This example is fictional. `POLICY-BUILD-001` (planning record `POLICY-PLAN-001`) answers from approved, current, permission-filtered policy documents and has no write or approval capability.

The candidate considers a `policy-answering` package that applies when a requester wants an answer grounded in accessible internal policy evidence, and excludes changing policy, granting access, approving an expense, or using a source outside the permitted boundary. Its procedure guides the fixed retrieval-and-answer workflow: seek permitted evidence, check current status, support claims with returned evidence, and return a bounded outcome when evidence is missing or conflicts. An adaptive alternative could choose among finite read, clarification, response, and escalation steps, with its own admission and evidence.

The draft admission record names a read-only policy-retrieval dependency, not an embedded permission. For `employee-uk-104`, the current source `travel-policy-2026@2026-10-01` gives a London hotel limit of GBP 220; the superseded `travel-policy-2024-superseded@2024-01-01` gives GBP 200 and cannot be presented as current. `contractor-uk-204` has no permission to retrieve policy content, and selecting the skill cannot change that.

The record leaves owner, source revision, package identity, and dependency verification unresolved rather than inventing them. Selection cases: a current-policy question is positive; a policy update request is negative (outside the skill, and no write capability); an equal-authority conflict between current sources is ambiguous, expecting `needs_information` or a declared clarification or escalation, not a date choice. If a later version referenced executable material, the identity would cover it, and no execution capability is admitted.

## Evidence and checklist

A reviewer should be able to reconstruct the decision from the admission record (scope, exclusions, source, identity boundary, dependencies, contract relation, open questions); the [2.2](02-agent-contracts-and-configuration.md) manifest separately records what was admitted. Keep a format-validation result, package inventory, source and identity record, dependency-resolution observation, context-cost measurement, and case plan, with tool-boundary evidence separate if execution is proposed. Do not log secrets, unnecessary source content, or raw hidden reasoning.

- [ ] Source, semantic version, owner, resolved-package identity, and identity scope are recorded or visibly unresolved.
- [ ] Discovery, admission, selection and loading, dispatch, and authoritative effect are not reported as one event.
- [ ] Any selected tool or resource stays within the agent contract with its own authorization and validation.
- [ ] Selection cases cover the description as well as the procedure.

For evaluation design, continue to [Part 4 — Testing and Evaluation](../04-testing-and-evaluation/README.md).

## References

[1]: https://agentskills.io/specification "Agent Skills specification"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf "NIST SP 800-218 Secure Software Development Framework"
[3]: https://slsa.dev/spec/v1.2/provenance "SLSA Provenance specification"
[4]: https://modelcontextprotocol.io/specification/2026-07-28/architecture "Model Context Protocol architecture specification"
[5]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices "Skill authoring best practices"

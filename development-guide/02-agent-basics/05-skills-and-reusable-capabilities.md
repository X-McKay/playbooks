# 2.5 Skills and Reusable Capabilities

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Agent developers, skill authors, capability owners, and reviewers

**Applicability:** Skills are optional. Apply this chapter when a reusable skill package is proposed, discovered, selected, admitted, loaded, changed, or composed with another skill. An agent with no skills still needs the agent-level contract and capability boundary in [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md).

**Reader question:** When does reusable guidance deserve to be a skill, and how can a team make its selection, dependencies, authority limits, and evidence reviewable without treating a package as a permission grant?

[Part 2 — Agent Basics](README.md) · [Playbook applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) · [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md)

## Purpose and applicability

A **skill** is a reusable package of task-specific guidance: it gives an agent a procedure, relevant knowledge, boundaries, and a way to recognize when that guidance fits. Packaging can make a coherent procedure easier to find, revise, and evaluate without repeating it in every agent. It also introduces another behavior-changing dependency. A vague description can select the wrong procedure; a changed reference can change behavior even if the main instruction file did not change; and bundled executable material can be mistaken for a capability.

A skill is therefore an optional packaging choice, not a required component of an agent and not a grant of permission. The agent contract defines the effective capability set and the deterministic boundaries that enforce it. A skill can explain how to use an already admitted read operation, for example, but it cannot make that operation available, extend its permitted source scope, or make its result authoritative. Tool contracts, identity, authorization, and untrusted-content controls remain with their respective owners in [2.4](04-tools-and-external-interfaces.md) and [Part 3 — Security and Trust Boundaries](../03-security-and-trust-boundaries/README.md).

This chapter is useful for a fixed workflow as well as for a bounded adaptive agent. A fixed workflow can select from an explicit list of admitted skills at a defined step. An adaptive sequence can choose among a finite admitted set, but it cannot enlarge that set. In either shape, the decision to use a skill is separate from permission to access data or take an action. It does not revisit the fixed retrieval-and-answer workflow selected in the planning record.

## Working model

### What a skill is—and is not

A **prompt or instruction** guides behavior in a particular interaction or across an agent. A **skill package** is a reusable unit that organizes such guidance with its supporting material for a bounded class of work. A **tool** is an executable interface that reads or changes something outside the model; its typed inputs, effects, authorization, and failure behavior are the concern of its tool contract. An **agent** is the configured runtime that has an input and output contract, state, and an effective capability set. The agent may use a skill, but is not itself a skill.

An **MCP integration** is also different. MCP describes a host-client-server protocol architecture in which servers can expose tools, resources, and prompts. It is a way to connect components, not a reusable procedure package or a local authorization decision. A skill may tell an agent when a previously admitted integration is useful, but a package file and an advertised protocol capability are each only candidates until the agent's own boundary admits them. [4]

The open Agent Skills format provides one portable convention: a directory has a required `SKILL.md` with `name` and `description` metadata and Markdown instructions, and it may contain scripts, references, assets, or other files. The specification describes a progressive-disclosure pattern in which metadata is available first, instructions are loaded on activation, and additional resources are loaded when needed. It also calls its `allowed-tools` field experimental and says implementation support varies. [1] That makes the format helpful for interchange, but does not make every runtime load resources the same way or turn metadata into enforcement.

The requirements in this chapter are proposed local playbook governance, not obligations imported from the portable format. In particular, a local record may require ownership, a semantic version, resolved-package identity, dependency checking, review, and evaluation even though a format parser can only confirm structure. Conversely, a valid package format, a familiar source, or a name that appears in discovery says nothing by itself about whether the package is admitted for this agent.

### Four separate decisions

Keep four decisions visible rather than collapsing them into “the skill is available.”

- **Discovery** makes candidate metadata visible so a runtime or builder can recognize possible relevance. A package in a shared location may be discoverable without being usable.
- **Admission** puts a specific resolved package into an agent's reviewed allowlist and effective capability manifest. It binds the agent to a source and identity, not merely a package name.
- **Selection and loading** decide whether an admitted skill fits this task and whether its instructions or declared resources are brought into context. Selection cannot add a new skill, tool, source, credential, or permission.
- **Execution** occurs only when a separately admitted capability is invoked through its own validated and authorized path. A script mentioned by a skill is still just material until that path accepts an operation.

This separation helps diagnose otherwise confusing observations. A package may have been discovered but not admitted. An admitted package may be available but not selected for a task. A selected procedure may propose a tool call that the deterministic boundary rejects. A call that is dispatched still needs evidence from the authoritative target before an external effect can be asserted. None of these observations proves all the others.

### Package identity and dependency boundary

Treat a skill as a resolved dependency rather than a mutable label. A human-readable semantic version communicates intended change; a recorded source and immutable content identity identify what was actually reviewed. The identity needs to cover behavior-relevant bundled or referenced material, not only the entry instructions. A reference that changes the procedure, an asset used to shape output, or executable material that a runtime might load can all change behavior.

The broader software-supply-chain literature offers a useful, limited rationale for this discipline. NIST's SSDF gives examples of recording provenance, verifying integrity, and reviewing third-party components, while SLSA defines provenance as verifiable information about where, when, and how an artifact was produced. [2] [3] Neither source makes a particular hash algorithm, owner model, or skill-admission process mandatory here. More importantly, an identity or provenance record supports traceability; it is not proof that a package is safe, accurate, authorized, or appropriate for an agent.

A **dependency inventory** names what the procedure needs and why. It can include an already admitted tool, a resource loader, a source type, an execution environment, or a data contract. Marking a dependency as required means a missing or mismatched one changes whether the procedure can be performed as reviewed. A candidate should state a bounded alternative only when that alternative has been separately assessed; otherwise the safe outcome is to stop or return the declared bounded result. An optional dependency should not be silently promoted to a required capability during a task.

## Decisions and best practices

### Choose a skill boundary that is worth reusing

Create a skill when a coherent procedure or body of knowledge recurs across bounded tasks, has a meaningful accountable owner, and benefits from independent change review or evaluation. Keep the responsibility narrow enough that a reader can state both its purpose and its exclusions. A short stable direction that applies to every task may belong in the agent's general instructions. A one-off request may need no package. If the reusable unit is chiefly an executable operation, give it a tool contract instead of disguising the operation as prose.

The decision has a maintenance cost. More packages can reduce duplication, but can also create a larger selection surface, more identities to resolve, more context to load, and more interactions to test. Do not split a single procedure merely to create a library catalogue. Do not merge unrelated procedures merely because they use the same source or tool. The useful boundary is the smallest reusable unit whose activation, dependencies, and completion can be assessed together.

A description is part of the selection interface. Say positively when the skill fits and negatively when it does not. Name the task condition rather than relying only on a topical word. For example, “answer a permitted question from current policy evidence” distinguishes an answering procedure from a policy-maintenance procedure. State observable completion in terms of the task result, such as a bounded answer with source evidence or a `needs_information` result that identifies missing evidence. Do not describe completion as a model's statement that it followed instructions.

### Resolve before use; compose deliberately

Before a candidate is admitted, resolve its name against the sources available to that agent. A duplicate or ambiguous name is not a harmless library detail: choosing by search order can substitute a different package without a visible contract change. Keep the result explicit in the admission record and capability manifest. A shared catalogue can remain useful for discovery, but discovery does not bypass this resolution step.

Composition deserves its own review. Two skills may compete for the same task, prescribe incompatible ordering, make inconsistent claims about a resource, or each assume the other owns a decision. Prefer one clearly selected procedure for a single responsibility. When two packages must cooperate, record their intended order, shared dependencies, information boundary, and the bounded outcome for a conflict or missing dependency. The agent contract and runtime still decide which capabilities exist; composition is not a way to stitch together broader authority.

Progressive disclosure has a practical limit. Keep indispensable guidance in the material that the selected runtime is known to load, and declare the remaining resource-loading behavior as a dependency. The Agent Skills specification recommends focused, on-demand resources, but does not establish a universal loading guarantee. [1] A procedure that assumes an unread reference or an inaccessible asset can appear complete while omitting its essential step.

### Keep authority at the actual boundary

A skill can suggest a useful action, but cannot authorize one. Its prose, metadata, source label, semantic version, manifest entry, or package identity cannot grant access to a document, select a tenant, enable a tool, or approve an effect. User requests, retrieved material, tool output, and other package content remain data; none can rewrite the allowlist. Authorization belongs at the protected operation using trusted identity and policy, as described in [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

This matters even for read-only guidance. A skill that tells an agent to search for a policy cannot make every policy document visible, and a read can still disclose information or mislead a requester. If a package bundles or references a script, that file does not become executable merely because a skill selected it. If an execution path is proposed later, it needs its own admitted capability, tool contract, authorization, and applicable effect handling. See [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md) and [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

### Anticipate common failures

A vague description can cause an otherwise sound procedure to activate for unrelated requests or be skipped for the task it was meant to help. Write positive, negative, and ambiguous selection cases before treating the description as adequate. A superficial format check can miss a changed reference or an unresolved dependency. Review the whole behavior-relevant package and record what its identity covers.

A second failure is **silent expansion by discovery**. A new package can appear in a shared location, or a package can expose a new resource, without belonging to the agent's reviewed allowlist. Make the distinction between discovered candidates and admitted identities visible. If a name resolves ambiguously, do not substitute whichever source appears first.

A third failure is **overgeneralization**. A broad “handle policies” skill may blur answering, maintenance, access administration, and incident handling into one selection target. This makes it hard to know whether an exclusion applied, which dependency was required, and what behavior changed. Separate coherent responsibilities and retain a bounded outcome when a request falls outside them.

Finally, do not confuse evidence with proof. An admission record shows what was proposed for review. A format result establishes only the checks it ran. A manifest identity makes a configuration traceable. A selection case can show a planned or observed relation. None alone proves that a source is authoritative, that authorization holds at an operation, or that the package will behave safely in every context.

### Build an admission record

Use the [skill-admission record](../../templates/2.5/skill-admission-record.yaml) as a neutral planning/build aid rather than as a deployment configuration. Start with the user task and agent contract. Decide whether reusable guidance is actually needed, and identify the one responsibility that the candidate would cover. Then describe its positive and negative activation conditions, procedure, safety constraints, and observable completion condition in plain language.

Next, inventory the complete candidate package. Record its source, intended semantic version, immutable identity, and all behavior-relevant instructions, references, assets, and executable material. List every required dependency and the observation that would establish its expected identity or availability. A dependency that cannot be resolved is an admission blocker or a reason to use a separately evaluated fallback; it is not a reason to assume that a package will work.

Then compare the candidate with the agent's declared capability set. Identify which already admitted read-only capability the procedure may guide and which desired actions remain absent. Record any discoverable but unadmitted package separately. Check that the candidate's name resolves uniquely and that its description does not promise authority or completion beyond the agent contract.

Finally, prepare evidence proportional to the proposed behavior change. Validate the format applicable to the chosen convention, inspect the resolved package boundary, estimate its context contribution in the intended loading stages, and design positive, negative, and ambiguous-selection cases. Where the procedure guides tool choice, include relevant allowed, denied, malformed, and unavailable paths. Part 4 owns evaluation method, case design, and interpretation; a plan for these checks is not a claim that they have been run.

## Requirements

- **SKILL-01** — When an agent uses a skill, the admitted skill MUST NOT add capabilities, permissions, or authority beyond the agent’s declared effective capability set; skill prose, metadata, and bundled files MUST NOT authorize an operation. The bounded capability-set requirement is defined in [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md).
- **SKILL-02** — A production agent that uses skills MUST explicitly allowlist the skills admitted to it and MUST NOT enable every discovered skill by default. Names MUST be unique across the agent’s resolved skill sources; ambiguous or duplicate resolution MUST fail closed before the affected agent is used.
- **SKILL-03** — Each skill admitted to a production agent MUST have an accountable owner, a stable, unique, lowercase hyphenated name, a semantic version, a recorded source, and an immutable content identity for the resolved package, including behavior-relevant bundled or referenced content. A changed package MUST receive a new content identity; a behavior-relevant change MUST be reviewed against the prior version before release.
- **SKILL-04** — A production skill MUST state when it applies and when it does not, the procedure it supplies, its safety constraints, and observable completion criteria. It MUST NOT contain secrets or claim authority. Dependencies required for that procedure MUST be identified and checked; if a required dependency is unavailable or does not match the admitted identity, the runtime MUST stop or use a separately evaluated fallback rather than silently assume it is present.
- **SKILL-05** — When a skill bundles or references executable material, the agent MUST NOT execute it solely because the skill mentions or contains it. Execution MUST be separately admitted and authorized under the applicable tool and security requirements.
- **SKILL-06** — Before a skill is used in production, its owner MUST validate its format, measure its context cost, and evaluate positive activation, negative activation, and plausible ambiguous-selection cases, along with procedure and safety adherence and any tool-selection behavior it guides. A behavior-relevant version change MUST be evaluated against the previous version for material regressions. Each run SHOULD record the available and loaded skills, their versions and content identities, load count, and instruction tokens, subject to the applicable data-handling policy.

## Worked example: current policy answers

This is an illustrative, unexecuted design/admission candidate for `POLICY-BUILD-001`. The internal policy-assistance candidate answers questions from approved, current, permission-filtered policy documents and has no external write or approval capability. Its planning record remains `POLICY-PLAN-001`; nothing in this example admits, enables, evaluates, or deploys a skill.

The candidate considers a `policy-answering` package. Its proposed positive condition is a requester asking for an answer grounded in accessible internal policy evidence. Its exclusions include a request to change policy, grant access, approve an expense, or use a source outside the permitted document boundary. Its procedure would guide the existing fixed retrieval-and-answer workflow to seek permitted evidence, distinguish the source's current status, support claims with the returned evidence, and return a declared bounded outcome when evidence is missing or conflicts. That guidance is reusable, but it does not change the planning decision to use a fixed workflow. A bounded adaptive alternative could choose among an already finite set of read, clarification, response, and escalation steps; it would still need its own admission and evidence.

The draft admission record names a read-only policy-document retrieval dependency rather than a permission embedded in the package. For requester `employee-uk-104`, the illustrative current source is `travel-policy-2026@2026-10-01`, which states a London hotel limit of GBP 220. The superseded `travel-policy-2024-superseded@2024-01-01` states GBP 200 and cannot be presented as current authority. These are fictional fixture facts, not an observed answer. For `contractor-uk-204`, the candidate has no permission to retrieve policy content; a skill selection cannot alter that result.

The candidate's record leaves its accountable owner, source revision, package identity, and dependency verification unresolved rather than inventing them. It identifies a current-policy question as a proposed positive-selection case. A request to update policy is a negative-selection case: it falls outside the skill and the candidate has no write capability. An equally authoritative current-source conflict is an ambiguous evidence case: the expected bounded response is `needs_information` or declared clarification/escalation, not an automatic date choice. These case descriptions are design expectations and do not constitute executed evaluation evidence.

If a later version of the proposed package referenced executable material, the record would include it in the behavior-relevant identity and separately ask whether any execution capability was admitted. The answer remains no for this illustrative candidate. A package's presence, a successful metadata read, or a model's statement that it followed the package would not establish a dispatch or an external effect.

## Evidence and checklist

A useful handoff lets a reviewer reconstruct the proposed decision without mistaking the record for an approved system. The [skill-admission record](../../templates/2.5/skill-admission-record.yaml) should show the candidate's scope, exclusions, source, intended identity boundary, dependencies, relationship to the agent contract, and unresolved questions. If a candidate proceeds, the effective capability manifest from [2.2](02-agent-contracts-and-configuration.md) is the separate record that identifies the skill actually admitted to a resolved configuration.

Evidence appropriate to a reviewed candidate can include a format-validation result, a package inventory, source and identity record, dependency-resolution observation, context-cost measurement, and case plan for activation and procedure behavior. Where any execution capability is proposed, retain the tool-boundary evidence separately. Keep identifiers and bounded observations needed to relate a package to a reviewed configuration; do not log secrets, unnecessary source content, or raw hidden reasoning merely to prove that a skill was considered.

Before a proposed skill is ready for the applicable admission and evaluation process, check that:

- [ ] Its responsibility, positive activation condition, exclusions, procedure, safety constraints, and observable completion condition are understandable without treating metadata as enforcement.
- [ ] Its source, semantic version, owner, resolved-package identity, and identity scope are recorded or visibly unresolved.
- [ ] Behavior-relevant references, assets, and executable material are included in the package inventory rather than hidden behind the entry instructions.
- [ ] Required dependencies and their expected identities are identified; an unavailable dependency has a bounded stop or separately evaluated fallback.
- [ ] Discovery, admission, selection/loading, dispatch, and authoritative effect are not reported as the same event.
- [ ] Any selected tool or resource remains within the agent contract and has its own authorization and validation path.
- [ ] Planned positive, negative, and ambiguous-selection cases cover the description as well as the procedure; changed behavior is compared with the prior version when one exists.

This checklist supports a local review unit. It does not approve an owner, source, package, capability, evaluation result, deployment, or organizational adoption. For evaluation design and result interpretation, continue to [Part 4 — Testing and Evaluation](../04-testing-and-evaluation/README.md).

## References

[1]: https://agentskills.io/specification "Agent Skills specification"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf "NIST SP 800-218 Secure Software Development Framework"
[3]: https://slsa.dev/spec/v1.2/provenance "SLSA Provenance specification"
[4]: https://modelcontextprotocol.io/specification/2026-07-28/architecture "Model Context Protocol architecture specification"

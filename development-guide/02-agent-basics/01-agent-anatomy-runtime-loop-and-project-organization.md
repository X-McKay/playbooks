# 2.1 Agent Anatomy, Runtime Loop, and Project Organization

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Builders, technical owners, reviewers, and operators who need to explain what an agent can propose, what the surrounding application controls, and where to inspect the design.

**Applicability:** Every proposed production agent, including a response-only assistant. Tools, skills, retrieval, persistent memory, repeated steps, and durable execution are conditional components; apply their owner chapters only when their individual triggers are present.

**Reader question:** What belongs to the agent versus its surrounding runtime, how does a bounded run move from observation to a safe terminal result, and how can a project make those responsibilities reviewable without prescribing a stack or folder tree?

[Part 2 — Agent Basics](README.md) · [Applicability and conformance](../../applicability.md) · [1.3 Agent Suitability and Alternatives](../01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md)

## Purpose and applicability

An **agent** is a bounded contribution to an application: it uses a model to interpret a task or propose a next step, while the surrounding application/runtime supplies the task boundary, trusted inputs, permitted capabilities, checks, and terminal handling. The word does not imply an autonomous service, a tool call, persistent memory, a long-running process, or a particular framework. A response-only assistant can be an agent; a fixed workflow can include model calls without handing the model control of the workflow's transitions.

This distinction helps a reviewer ask the useful question: **what does the model decide or propose, and what does the application independently decide or enforce?** The model can help choose wording, identify a needed clarification, or select among an already admitted finite set of next steps. It is not the source of capability membership, identity, authorization, approval, source authority, or an external effect. Those facts come from declared configuration and protected runtime boundaries.

Use the smallest anatomy that can support the declared task. A single model response with output validation may be enough when the task is fully described by the request and approved input. A fixed workflow can route, branch, or use a model at defined stages while retaining orchestration-defined transitions. An adaptive alternative is warranted only when a model-directed choice of next permitted step or stopping decision provides task-relevant value beyond that fixed path. A provider engineering perspective makes a similar workflow-versus-agent distinction and cautions that multi-step designs add latency, cost, and opportunities for compounding error; that perspective is a design input, not a standard or proof that a design fits a task. [4]

This chapter gives a reviewable working model and project-organization pattern. It does not define the full agent contract, tool semantics, source/freshness policy, authorization method, evaluation method, durable execution, or release decision. Those questions have their owners in [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md), [2.4 Tools and External Interfaces](04-tools-and-external-interfaces.md), [2.6 Context and Retrieval Fundamentals](06-context-and-retrieval-fundamentals.md), [Part 3 — Security and Trust Boundaries](../03-security-and-trust-boundaries/README.md), [Part 4 — Testing and Evaluation](../04-testing-and-evaluation/README.md), and the applicable Parts 6 and 7 references.

## Working model

### Separate responsibilities, not necessarily processes

A useful anatomy names responsibilities and the handoffs between them. They can be separate modules, or several can share an implementation unit in a small project. The point is not to multiply services. It is to make the boundary between a proposal and an accepted operation visible.

The **model** interprets the current task and produces a candidate answer, a clarification request, or a structured proposal. It may be helpful in a fixed workflow or direct the next step in a bounded adaptive sequence. Its output remains data until another boundary accepts it.

**Instructions** tell the model the task, the response behavior, and how to handle uncertainty. **Context** is the material assembled for a run: for example, the request, task-relevant approved evidence, selected history, and bounded results from an admitted capability. Instructions guide behavior; they do not grant permission. Context can support an answer, but a retrieved passage, a model summary, or a tool result does not change the operating rules. Chapter [2.3](03-prompts-and-instructions.md) develops instruction design, and [2.6](06-context-and-retrieval-fundamentals.md) owns retrieval and memory decisions.

A **capability** is an admitted thing the application can use, such as a narrowly defined external interface or a reusable skill. A capability is optional and remains unavailable unless the agent's declared configuration admits it. A **tool** is a capability that reaches outside the reasoning process; [2.4](04-tools-and-external-interfaces.md) owns its typed contract, actual effect, and failure semantics. A skill can package reusable guidance or resources, but packaging does not itself grant execution; [2.5](05-skills-and-reusable-capabilities.md) owns that admission decision.

The **runtime/control layer** receives a candidate proposal and decides whether it is acceptable in the present run. It assembles the allowed context, tracks the run, chooses the next fixed transition or accepts a bounded adaptive proposal, checks declared limits, and invokes only an admitted operation through its protected boundary. It also validates a returned result before the model or a downstream consumer uses it. NIST's zero-trust architecture is not an agent-runtime blueprint, but its separation of a policy decision from the mechanism that establishes and enforces a resource path illustrates why an identifiable decision/enforcement boundary remains useful even when implementation units are combined. [2]

An **output boundary** accepts the final result only when it has the declared shape and applicable invariants. Structural validation can reject an unexpected field, malformed action request, or unsupported terminal status. It does not establish that a policy claim is correct, that a citation supports the claim, or that an external action occurred. Those are separate evidence questions.

### Configuration is not run state

**Configuration** is the reviewed declaration used to construct an agent. It identifies the agent's purpose, versioned behavior, declared input/output contract, admitted capability set, and applicable limits and policies. Chapter [2.2](02-agent-contracts-and-configuration.md) owns the exact contract and effective-configuration evidence. Configuration answers, “What may this candidate be assembled to do?”

**Run state** is the changing record of one attempt. It can include a request reference, trusted requester and scope context, source identifiers supplied to the model, admitted proposals, bounded capability results, remaining allowance, observation sequence, and terminal result. It answers, “What has happened in this attempt?” A run may consume its allowance or receive a new observation; it does not use that fact to add a capability, widen a scope, or rewrite its configuration. Secrets and unsafe live clients do not belong in serializable state.

Keep **state**, **evidence**, and **authority** distinct. State records information useful to continue or finish work. Evidence helps a reviewer investigate what the system observed or decided. Authority is permission evaluated at a protected operation from trusted identity and policy. A request field, retrieved document, model statement, or prior successful run can influence a proposal or supply task evidence; none becomes authority merely by appearing in state.

### A bounded runtime loop

A repeated agent can be described as an observe/propose/validate/execute/observe/terminate cycle. Research on ReAct describes interleaving generated task actions with observations from external sources or environments. [1] That finding supports the shape of an interactive loop, not a requirement to expose reasoning traces or a claim that the pattern is correct, secure, or useful for every task.

A builder can express the cycle in plain language:

1. **Initialize the run.** Resolve the already-declared configuration, receive trusted runtime dependencies, and establish the applicable terminal outcomes and stop conditions. If required configuration or trusted context is unavailable, return the declared bounded result rather than inventing a substitute.
2. **Observe the current situation.** Use the request, allowed context, and prior admitted results. Label their roles: user task, trusted runtime fact, task evidence, or untrusted content. Do not treat a previous answer or a model assertion as an authoritative external observation.
3. **Propose a response or next step.** The model may produce a candidate final answer, an information request, a terminal outcome, or a structured request for an enabled capability. In a fixed workflow, the orchestration may instead select the next defined step without asking the model to choose.
4. **Validate and admit.** Check the candidate's declared shape and the proposed operation's permitted name and arguments. At a protected capability boundary, apply the independently required identity, authorization, policy, and approval decisions. Rejected proposals remain rejected data; they are not partially repaired into a broader request.
5. **Execute only an admitted operation.** A response-only path has no operation here. For an admitted interface, collect a bounded result or a distinct failure as data. A dispatched attempt, a response, and an authoritative external effect are different observations; a model's statement that an action succeeded is not evidence that it did.
6. **Record the next observation.** Add only the information needed for the next decision, preserving source, capability, and result identity as appropriate. The application decides whether the next state can continue, needs clarification, or has reached a terminal result.
7. **Terminate deliberately.** Finish on a valid completion, a declared `needs_information`, `declined`, or `failed` outcome, a blocked proposal, an unresolved boundary, or an enforced stop condition. Return the typed terminal result and the minimum associated information that the caller needs to handle it.

The loop may have one pass. Repetition is appropriate only where a later observation can change a permitted next decision. It needs declared stopping conditions and applicable resource limits because “keep trying” is not a terminal behavior. A limit stop is not a successful completion. It is a bounded outcome that gives the caller a truthful basis for the next action.

## Decisions and best practices

### Choose the simplest execution shape that preserves the boundary

Start with the task's transitions. If every meaningful transition can be written before a run begins, use a fixed workflow and let the model contribute only where language interpretation or drafting is useful. A fixed workflow may use a model router or branch after a result; those features do not change its orchestration-defined transition set. If the model selects a meaningful next permitted action, sequence, or stopping choice from observations, record that as the bounded adaptive choice and keep the action set finite and independently enforced.

Do not add a tool merely to make a design look agentic. A direct answer from supplied evidence avoids an external interface, access decision, source-selection failure, retry ambiguity, and extra maintenance. Add a capability only when it supplies information or performs a permitted operation the declared task needs. If a tool, long-running sequence, consequence, or human approval boundary appears, revisit the separately owned contracts and execution guidance rather than stretching this chapter's simple loop.

### Put the external authority boundary outside the model

A model proposal can be useful, but the runtime is the point that can decide whether an operation is even available. This is especially important where a read can expose protected information or an action can change an external system. The protected operation evaluates trusted identity, target, scope, capability, and applicable policy at execution time; [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) owns those controls.

Several tempting shortcuts fail this separation. Treating a prompt instruction as a tool restriction leaves the capability available. Treating a model-generated tenant or policy name as trusted state confuses a request with authority. Treating successful model prose as a completed external action loses the difference between proposal, dispatch, response, and effect. The runtime should instead pass a proposed request to a narrow interface that performs its own required checks. Content and action-boundary controls are developed in [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

### Make an anatomy reviewable through artifacts, not ceremony

A builder does not need a prescribed repository tree. They do need an inspectable way to find the decisions that govern a candidate. Start with the agent contract and an anatomy record that name the responsibilities in use and explicitly mark optional components absent. Then locate the instruction material, source/context decisions, capability contracts, runtime/validation behavior, tests or cases, and decision notes where a reviewer can connect them.

NIST's Generative AI Profile suggests documenting the expected context of use, assumptions and limitations, data origin/content lineage, and measurement plans. It also cautions that pre-deployment testing can be mismatched to deployment context. [3] That supports retaining artifacts that explain a specific candidate and its limits. It does not make a particular file name, review role, folder layout, or test count mandatory, and the presence of a record does not prove that a runtime control operated as intended.

For shared executable capabilities, make the maintenance and review responsibility discoverable before another agent relies on them. A capability name alone is not enough: a reviewer needs to locate its maintained contract and who is accountable for reviewing a change. A shared capability can be a small reusable adapter or a larger package; the requirement concerns the owner relationship, not its size or a separate repository.

### Failure modes to design against

**A loop that has no honest end.** A system repeatedly asks the model to try again after unhelpful or unavailable results. This hides exhaustion, consumes resources, and can turn a safe uncertainty into an invented answer. Declare terminal outcomes and stop conditions before the loop begins; when the condition is reached, return the outcome the caller can handle.

**A proposal that becomes an effect in the same step.** A runtime treats a structured action request as permission to call an interface. This erases the opportunity to check the capability, target, arguments, authority, and effect boundary. Keep proposal validation and protected-operation admission observable, even when a small implementation performs them in close succession.

**A valid structure that is treated as a true result.** A response can satisfy a schema while citing the wrong source, applying the wrong policy, or asserting an effect that never happened. Validate the structure at the receiving boundary, then use the appropriate source, authorization, external-state, or evaluation evidence for the semantic claim.

**Configuration hidden in mutable run data.** A model output or request says which tool, scope, model setting, or budget the run should use, and the application quietly accepts it. This defeats review of the declared configuration. Treat such values as requests that must match the effective configuration, or reject them.

**A directory that obscures the deployed decision.** A project stores instructions, capability definitions, and validation rules in convenient but untraceable locations. Reviewers then inspect a document that is not the artifact the candidate actually uses. Link each project artifact to its role in construction or review, and retain identities needed to compare a reviewed candidate with the material later assembled. Chapter 2.2 owns the effective capability manifest; this chapter only shows where its supporting decisions can be organized.

### Illustrative project layout

The following plain-text layout is **illustrative**, not a required tree, naming convention, technology choice, or claim that every area needs a separate implementation unit. A small candidate can co-locate several groups. A larger project can split them further. The useful property is that each group maps to a decision or inspectable evidence, not that its path matches this example.

```text
agent-project/
├── agent-definition/       # purpose, contract, configuration identity, admitted bounds
├── instructions/           # task guidance, examples, and revision identity
├── context/                # source/context assembly decisions when needed
├── capabilities/           # narrow tool or skill contracts and ownership records
├── runtime/                # orchestration, state handling, proposal admission, validation
├── tests/                  # normal, boundary, and failure cases with expected observations
└── docs/                   # rationale, handoffs, open questions, and review evidence
```

The `agent-definition` group answers what candidate is under review and which responsibilities are present. The `instructions` and `context` groups let a reviewer distinguish operating guidance from evidence the model may consider. The `capabilities` group lets a reviewer locate each admitted interface and, where it is shared, its named maintainer and review owner. The `runtime` group makes the proposal-to-enforcement handoff and terminal handling inspectable. The `tests` and `docs` groups connect design claims to proposed cases and decisions without claiming that the cases ran or that a local review unit is approved.

Use the accompanying [agent anatomy record](../../templates/2.1/agent-anatomy-record.yaml) as a neutral planning/build record. It preserves the common fictional example and asks for visible unknowns. It is not an assembly command, a live runtime record, an approval, or evidence of a deployed system.

## Requirements

- **ANATOMY-01** When a production agent combines a model with instructions, context, capabilities, state, or output validation, its design MUST make those responsibilities and their interfaces identifiable to reviewers, even when they share an implementation unit.
- **ANATOMY-02** When a model can propose actions or further steps, the runtime MUST keep proposals separate from deterministic enforcement and MUST apply the applicable authorization, capability, and policy checks before any action is executed.
- **ANATOMY-03** Every production agent with repeated model or tool steps MUST enforce declared stopping conditions and applicable resource limits, and MUST return a defined terminal result when it stops or cannot continue.
- **ANATOMY-04** When an agent’s output is consumed as structured data or a downstream action request, the receiving boundary MUST validate it against the declared contract before acceptance or use.
- **ANATOMY-05** When executable capabilities are shared across agents or project areas, the shared capabilities MUST have named maintainers and a clear review owner.

## Worked example

The common example is **POLICY-BUILD-001**, a fictional, permission-filtered internal policy-assistance candidate. Its planning record is **POLICY-PLAN-001**. The candidate is read-only: it has no external write or approval capability, and this chapter makes no claim that it has been assembled, admitted, evaluated, approved, deployed, or observed in operation.

A requester, `employee-uk-104`, asks for the London hotel limit. In the illustrative fixture, the requester may read `travel-policy-2026@2026-10-01`, whose current approved source text gives a fictional limit of GBP 220. The same requester can also encounter `travel-policy-2024-superseded@2024-01-01`, a historical source with a different GBP 200 value. `contractor-uk-204` is not permitted to read either policy source. Those identities and values are controlled example facts, not travel policy.

### Read-only, fixed-path version

The smallest version accepts the question plus trusted requester context, receives an already permission-filtered current passage, and asks the model for a structured answer. It does not need a model-directed action loop. The output boundary checks that the status is one of the declared terminal outcomes, that a cited identifier is among the supplied evidence, and that the shape contains the required uncertainty field. These checks do not establish that the citation semantically supports the answer; that remains a separate evaluation question.

For the current permitted source, the expected illustrative result is `complete` with GBP 220 and the current source identity. If the answer-bearing current source is absent, the candidate returns `needs_information` rather than recreating an amount from the superseded record. If the requester is `contractor-uk-204`, the protected retrieval boundary declines access and the candidate returns `declined` without revealing the amount. The model does not select a different requester, source collection, or capability to work around either outcome.

### Bounded adaptive alternative

If the record later establishes a need for model-directed source selection, the candidate could retain the same read-only scope while adding a finite action allowlist: `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, and `escalate`. The model may propose one next action after an observation, but the runtime admits only a declared action and validates its arguments. The only external information capability remains a permission-filtered read; no write or approval capability becomes available.

Suppose the read returns both the current GBP 220 source and the superseded GBP 200 source. The observation carries their identities and status. The model can propose a `complete` answer citing the current evidence, while the output boundary rejects an answer with an unknown source identifier or unsupported terminal status. If two equally authoritative current permitted sources conflict, the candidate returns `needs_information` or the declared clarification/escalation path; it does not select the newer-looking date on its own. If a hostile document asks it to reveal restricted material or approve an expense, the content remains data. The agent preserves the allowed policy-answer utility when current permitted evidence exists, while the absent write capability and protected read boundary keep the hostile request from changing authority.

### What a reviewer can inspect

For either shape, a reviewer should be able to follow the anatomy record from candidate purpose to configuration/state boundary, admitted capabilities, loop shape, stop conditions, terminal result, and the evidence that would need evaluation. The record can show that no external write capability is declared and that a proposed capability request was blocked. It cannot by itself prove that an action was never dispatched, that a source supports a claim, or that a control is effective in an operating environment. Part 4 supplies the applicable cases and evidence interpretation.

A later proposal to add a policy-update action would be a different candidate boundary, not a small change to this read-only example. It would need the relevant new contract, effect, authority, execution, approval, and evaluation decisions from their owner chapters before any claim of admission or operation.

## Evidence and checklist

An anatomy review is complete enough for local review when another reader can locate the agent's responsibilities, tell which components are optional or absent, and trace an illustrative run from trusted inputs through a proposal/validation boundary to a declared terminal outcome. It should distinguish proposed design evidence from observations of an actual system.

Useful completion evidence for this proposed local review unit includes an anatomy record that names the response and action boundaries; a simple written loop or state sketch; links to the agent contract, relevant context and capability records, and applicable evidence plan; and planned cases that exercise a normal completion and meaningful boundary or failure. Keep the retained material proportionate and follow the data-handling owner for any sensitive content. Do not retain raw hidden reasoning merely to make a run inspectable.

Before handing the unit to the next builder or reviewer, check:

- [ ] The model, instructions, context, admitted capabilities, runtime/control layer, state, and output boundary have identifiable responsibilities, even when some share an implementation unit.
- [ ] The record says which optional components are absent, rather than implying tools, retrieval, memory, approval, or durable execution.
- [ ] Configuration is distinguishable from changing run state, and run data cannot silently expand an admitted capability or authority boundary.
- [ ] Each repeated path has a declared terminal behavior and applicable stop condition; an exhausted run is not reported as a completion.
- [ ] A proposed operation is separate from validation, protected-operation authorization, dispatch, returned response, and any authoritative external effect.
- [ ] Structured output is validated before a caller, workflow, tool, or another agent consumes it; structural validity is not represented as semantic support or successful external effect.
- [ ] Each shared executable capability can be traced to its named maintainer and clear review owner.
- [ ] The fixed-path and bounded adaptive alternatives preserve the same read-only, permission-filtered example boundary; no external write or approval capability is implied.
- [ ] The handoff names the relevant owners: 2.2 for contract/effective configuration, 2.4 for external interfaces, Part 3 for trust boundaries, Part 4 for evidence, and Parts 6 or 7 only when their execution triggers arise.

## References

[1]: https://arxiv.org/abs/2210.03629 "ReAct: Synergizing Reasoning and Acting in Language Models"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf "NIST SP 800-207: Zero Trust Architecture"
[3]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1: Generative Artificial Intelligence Profile"
[4]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"

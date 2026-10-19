# 2.1 Agent Anatomy, Runtime Loop, and Project Organization

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders, technical owners, reviewers, and operators who need to explain what an agent can propose, what the surrounding application controls, and where to inspect the design.

**Applicability:** Every production agent, including a response-only assistant. Tools, skills, retrieval, persistent memory, repeated steps, and durable execution are optional; apply their chapters only when they are present.

**Reader question:** What belongs to the agent and what belongs to the runtime around it, how does a bounded run get from observation to a safe final result, and how can a project make those responsibilities easy to review?

[Part 2 — Agent Basics](README.md) · [Applicability and conformance](../../applicability.md) · [1.3 Agent Suitability and Alternatives](../01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md)

## Purpose and applicability

An **agent** is a bounded part of an application. It uses a model to interpret a task or propose a next step. The surrounding application, called the **runtime**, supplies the task boundary, trusted inputs, permitted capabilities, checks, and final handling. The word does not imply an autonomous service, a tool call, memory, a long-running process, or a framework. A response-only assistant can be an agent. A fixed workflow can call a model without letting the model control its transitions.

The useful review question is: **what does the model decide or propose, and what does the application decide or enforce on its own?** The model can help choose wording, spot a needed clarification, or pick among a finite, already admitted set of next steps. It is not the source of capability membership, identity, authorization, approval, source authority, or any external effect. Those come from declared configuration and protected runtime boundaries.

Use the smallest anatomy that supports the task. One model response with output validation may be enough when the request and approved input fully describe the task. A fixed workflow can route, branch, or call a model at defined stages while the orchestration owns the transitions. Let the model choose the next step or when to stop only when that choice adds value a fixed path cannot. Published engineering guidance draws the same line between workflows and agents, advises starting simple and adding complexity only when it pays off, and warns that multi-step designs add latency, cost, and compounding errors. [4]

This chapter gives a working model and a project-organization pattern. Other chapters own the details: [2.2](02-agent-contracts-and-configuration.md) (contract and configuration), [2.4](04-tools-and-external-interfaces.md) (tools), [2.6](06-context-and-retrieval-fundamentals.md) (sources and freshness), [Part 3](../03-security-and-trust-boundaries/README.md) (authorization), [Part 4](../04-testing-and-evaluation/README.md) (evaluation), and Parts 6 and 7 (execution).

## Working model

### Separate responsibilities, not necessarily processes

Name the responsibilities and the handoffs between them. They can be separate modules, or several can share one implementation unit in a small project. The aim is not more services. It is to make the line between a proposal and an accepted operation visible.

The **model** interprets the task and produces a candidate answer, a clarification request, or a structured proposal. In a fixed workflow it helps with language work. In a bounded adaptive sequence it can also direct the next step. Its output stays data until another boundary accepts it.

**Instructions** tell the model the task, how to respond, and how to handle uncertainty. **Context** is the material assembled for a run: the request, approved task evidence, selected history, and bounded results from admitted capabilities. Instructions guide behavior; they do not grant permission. A retrieved passage, model summary, or tool result does not change the operating rules. See [2.3](03-prompts-and-instructions.md) for instructions and [2.6](06-context-and-retrieval-fundamentals.md) for retrieval and memory.

A **capability** is something the application can use, such as an external interface or a reusable skill. It is unavailable unless the agent's declared configuration admits it. A **tool** is a capability that reaches outside the reasoning process; [2.4](04-tools-and-external-interfaces.md) covers its contract, effect, and failure behavior. A skill can package guidance or resources, but packaging does not grant execution; [2.5](05-skills-and-reusable-capabilities.md) covers admission.

The **runtime/control layer** receives a proposal and decides whether it is acceptable now. It assembles the allowed context, tracks the run, picks the next fixed transition or accepts a bounded adaptive proposal, checks limits, and calls only an admitted operation through its protected boundary. It also validates a returned result before the model or a downstream consumer uses it. NIST's zero-trust architecture is not an agent blueprint, but it separates the policy decision from the mechanism that enforces it, which shows why an identifiable decision/enforcement boundary stays useful even when implementation units are combined. [2]

An **output boundary** accepts the final result only when it has the declared shape and holds the declared invariants. Structural validation can reject an unexpected field, a malformed action request, or an unsupported final status. It cannot show that a policy claim is right, that a citation supports the claim, or that an external action happened. Those need other evidence.

### Configuration is not run state

**Configuration** is the reviewed declaration used to build an agent: its purpose, versioned behavior, input/output contract, admitted capabilities, and limits and policies. It answers, "What may this candidate be built to do?" See [2.2](02-agent-contracts-and-configuration.md).

**Run state** is the changing record of one attempt: a request reference, trusted requester and scope, source identifiers given to the model, admitted proposals, bounded capability results, remaining allowance, observation order, and the final result. It answers, "What has happened in this attempt?" A run may use up its allowance or receive a new observation, but it does not add a capability, widen a scope, or rewrite its configuration. Secrets and live clients do not belong in serializable state.

Keep **state**, **evidence**, and **authority** distinct. State holds what is needed to continue or finish. Evidence helps a reviewer see what the system observed or decided. Authority is permission checked at a protected operation from trusted identity and policy. A request field, retrieved document, model statement, or earlier successful run can shape a proposal or supply evidence, but none becomes authority by appearing in state.

### A bounded runtime loop

A repeated agent can be described as a cycle of observe, propose, validate, execute, observe, and terminate. ReAct research describes interleaving generated actions with observations from external sources. [1] That supports the shape of an interactive loop. It does not require exposing reasoning traces, and it does not show the pattern is secure or right for every task.

In plain steps:

1. **Initialize the run.** Resolve the declared configuration, receive trusted runtime dependencies, and set the final outcomes and stop conditions. If required configuration or trusted context is missing, return the declared bounded result instead of inventing a substitute.
2. **Observe.** Use the request, allowed context, and earlier admitted results. Label each input's role: user task, trusted runtime fact, task evidence, or untrusted content. Do not treat a previous answer or a model assertion as an authoritative observation.
3. **Propose.** The model may produce a candidate final answer, an information request, a final outcome, or a structured request for an enabled capability. In a fixed workflow, the orchestration may pick the next step without asking the model.
4. **Validate and admit.** Check the candidate's shape and the proposed operation's permitted name and arguments. At a protected capability boundary, apply the identity, authorization, policy, and approval decisions independently. A rejected proposal stays rejected; do not repair it into a broader request.
5. **Execute only an admitted operation.** A response-only path has none. For an admitted interface, collect a bounded result or a distinct failure as data. A dispatched attempt, a response, and an authoritative external effect are different observations. A model saying an action succeeded is not evidence that it did.
6. **Record the next observation.** Add only what the next decision needs, keeping source, capability, and result identity. The application decides whether to continue, ask for clarification, or finish.
7. **Terminate deliberately.** Finish on a valid completion, a declared `needs_information`, `declined`, or `failed` outcome, a blocked proposal, an unresolved boundary, or an enforced stop. Return the typed result and the minimum the caller needs to handle it.

The loop may have one pass. Repeat only where a later observation can change a permitted next decision. Repetition needs declared stop conditions and resource limits, because "keep trying" is not an ending. A limit stop is not a success; it is a bounded outcome that gives the caller a truthful basis for what to do next.

## Decisions and best practices

### Choose the simplest execution shape that preserves the boundary

Start with the task's transitions. If every meaningful transition can be written down before a run, use a fixed workflow and let the model help only where interpretation or drafting is useful. A router or a branch on a result does not change that. If the model picks a meaningful next action, sequence, or stopping point from observations, record that as the bounded adaptive choice and keep the action set finite and enforced independently.

Do not add a tool just to look agentic. A direct answer from supplied evidence avoids an external interface, an access decision, source-selection failure, retry ambiguity, and maintenance. Add a capability only when the task needs the information or operation it provides. If a tool, long-running sequence, consequential action, or human approval appears, go to the chapters that own them instead of stretching this simple loop. Build in a sandbox with guardrails and test before widening autonomy. [4]

### Put the external authority boundary outside the model

A model proposal can be useful, but the runtime decides whether an operation is even available. This matters most where a read can expose protected data or an action can change an external system. The protected operation checks trusted identity, target, scope, capability, and policy at execution time; [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) covers those controls.

Common shortcuts break this separation:

- Treating a prompt instruction as a tool restriction leaves the capability available.
- Treating a model-written tenant or policy name as trusted state confuses a request with authority.
- Treating fluent model prose as a completed action loses the difference between proposal, dispatch, response, and effect.

Instead, pass the proposed request to a narrow interface that does its own checks. Content and action-boundary controls are in [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

### Make an anatomy reviewable through artifacts, not ceremony

You do not need a prescribed repository tree. You do need a way to find the decisions that govern a candidate. Start with the agent contract and an anatomy record that names the responsibilities in use and marks optional components absent. Then place the instructions, source/context decisions, capability contracts, runtime and validation behavior, tests, and decision notes where a reviewer can connect them.

NIST's Generative AI Profile suggests documenting the expected context of use, assumptions and limitations, data origin and lineage, and measurement plans, and asks that performance be shown for conditions similar to deployment. [3] That supports keeping artifacts that explain a candidate and its limits. It does not mandate a file name, role, layout, or test count, and having a record does not prove a control works.

For shared executable capabilities, make maintenance and review responsibility easy to find before another agent relies on them. A name alone is not enough: a reviewer needs the maintained contract and the person accountable for changes. The capability can be a small adapter or a large package; the requirement is about the owner, not the size or a separate repository.

### Failure modes to design against

**A loop with no honest end.** The system keeps asking the model to retry after unhelpful or unavailable results. This hides exhaustion, burns resources, and can turn safe uncertainty into an invented answer. Declare outcomes and stop conditions before the loop starts, and return a result the caller can handle.

**A proposal that becomes an effect in the same step.** The runtime treats a structured action request as permission to call an interface. That removes the chance to check capability, target, arguments, authority, and effect. Keep proposal validation and protected admission observable, even if a small implementation runs them back to back.

**A valid structure treated as a true result.** A response can satisfy a schema while citing the wrong source, applying the wrong policy, or claiming an effect that never happened. Validate structure at the receiving boundary, then use source, authorization, external-state, or evaluation evidence for the meaning.

**Configuration hidden in mutable run data.** A model output or request says which tool, scope, model setting, or budget to use, and the application quietly accepts it. Treat such values as requests that must match the effective configuration, or reject them.

**A directory that hides the deployed decision.** Instructions, capability definitions, and validation rules sit in convenient but untraceable places, so reviewers inspect a document the candidate does not actually use. Link each artifact to its role, and keep identities that let you compare the reviewed candidate with what is later assembled. The effective capability manifest is in 2.2.

### Illustrative project layout

This plain-text layout is an example, not a required tree or technology choice. A small candidate can co-locate several groups; a larger project can split them further. What matters is that each group maps to a decision or to evidence a reviewer can inspect.

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

`agent-definition` shows which candidate is under review and which responsibilities exist. `instructions` and `context` let a reviewer tell operating guidance from evidence. `capabilities` locates each admitted interface and, if shared, its maintainer and review owner. `runtime` makes proposal-to-enforcement handoff and terminal handling inspectable. `tests` and `docs` tie design claims to cases and decisions.

The [agent anatomy record](../../templates/2.1/agent-anatomy-record.yaml) is a neutral planning record that uses the common fictional example and asks for visible unknowns.

## Requirements

- **ANATOMY-01** When a production agent combines a model with instructions, context, capabilities, state, or output validation, its design MUST make those responsibilities and their interfaces identifiable to reviewers, even when they share an implementation unit.
- **ANATOMY-02** When a model can propose actions or further steps, the runtime MUST keep proposals separate from deterministic enforcement and MUST apply the applicable authorization, capability, and policy checks before any action is executed.
- **ANATOMY-03** Every production agent with repeated model or tool steps MUST enforce declared stopping conditions and applicable resource limits, and MUST return a defined terminal result when it stops or cannot continue.
- **ANATOMY-04** When an agent’s output is consumed as structured data or a downstream action request, the receiving boundary MUST validate it against the declared contract before acceptance or use.
- **ANATOMY-05** When executable capabilities are shared across agents or project areas, the shared capabilities MUST have named maintainers and a clear review owner.

## Worked example

The common example is **POLICY-BUILD-001**, a fictional, permission-filtered internal policy-assistance candidate. Its planning record is **POLICY-PLAN-001**. It is read-only: no external write or approval capability. All identities and values are fictional.

A requester, `employee-uk-104`, asks for the London hotel limit. The requester may read `travel-policy-2026@2026-10-01`, whose current approved text gives a limit of GBP 220. The requester can also encounter `travel-policy-2024-superseded@2024-01-01`, a historical source with a different GBP 200 value. `contractor-uk-204` may not read either source.

### Read-only, fixed-path version

The smallest version takes the question plus trusted requester context, receives an already permission-filtered current passage, and asks the model for a structured answer. It needs no model-directed action loop. The output boundary checks that the status is a declared final outcome, that a cited identifier is among the supplied evidence, and that the required uncertainty field is present. It does not check that the citation supports the answer; that is an evaluation question.

For the current permitted source, the expected result is `complete` with GBP 220 and the current source identity. If the current source is absent, the candidate returns `needs_information` rather than rebuilding an amount from the superseded record. For `contractor-uk-204`, the protected retrieval boundary declines access and the candidate returns `declined` without revealing the amount. The model does not pick a different requester, collection, or capability to get around either outcome.

### Bounded adaptive alternative

If a need for model-directed source selection is later shown, the candidate could keep the same read-only scope and add a finite action allowlist: `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, and `escalate`. The model proposes one next action after an observation; the runtime admits only a declared action and validates its arguments. The only external capability is still a permission-filtered read.

Suppose the read returns both the current GBP 220 source and the superseded GBP 200 source, each with identity and status. The model can propose a `complete` answer citing the current evidence, while the output boundary rejects an unknown source identifier or unsupported status. If two equally authoritative current sources conflict, the candidate returns `needs_information` or the declared clarification/escalation path; it does not pick the newer-looking date. If a hostile document asks it to reveal restricted material or approve an expense, the content stays data. The agent still answers from current permitted evidence, while the missing write capability and protected read boundary keep the hostile request from changing authority.

### What a reviewer can inspect

For either shape, a reviewer should be able to follow the anatomy record from purpose, to the configuration/state boundary, admitted capabilities, loop shape, stop conditions, and final result, to the evidence that would need evaluation. The record can show that no write capability is declared and that a capability request was blocked. It cannot prove that an action was never dispatched, that a source supports a claim, or that a control works in operation. [Part 4](../04-testing-and-evaluation/README.md) covers cases and evidence.

Adding a policy-update action would create a different candidate, not a small change. It would need new contract, effect, authority, execution, approval, and evaluation decisions first.

## Evidence and checklist

An anatomy review is complete enough when another reader can find the agent's responsibilities, tell which components are optional or absent, and trace a run from trusted inputs through a proposal/validation boundary to a declared final outcome. Keep design evidence separate from observations of a real system.

Useful evidence: an anatomy record naming the response and action boundaries; a written loop or state sketch; links to the contract, context and capability records, and evidence plan; and planned cases for a normal completion and a meaningful boundary or failure. Keep it proportionate, follow data-handling rules for sensitive content, and do not retain raw hidden reasoning just to make a run inspectable.

Before handing off, check:

- [ ] The model, instructions, context, admitted capabilities, runtime layer, state, and output boundary have identifiable responsibilities, even when some share a unit.
- [ ] The record says which optional components are absent, rather than implying tools, retrieval, memory, approval, or durable execution.
- [ ] Configuration is distinct from run state, and run data cannot silently expand a capability or authority boundary.
- [ ] Each repeated path has a declared final behavior and stop condition; an exhausted run is not reported as a completion.
- [ ] A proposed operation is separate from validation, protected authorization, dispatch, response, and any authoritative external effect.
- [ ] Structured output is validated before a caller, workflow, tool, or another agent uses it; structural validity is not presented as semantic support or a successful effect.
- [ ] Each shared executable capability traces to a named maintainer and clear review owner.
- [ ] The fixed-path and adaptive alternatives keep the same read-only, permission-filtered boundary.
- [ ] The handoff names owners: 2.2 for contract and effective configuration, 2.4 for external interfaces, Part 3 for trust boundaries, Part 4 for evidence, and Parts 6 or 7 only when execution triggers arise.

## References

[1]: https://arxiv.org/abs/2210.03629 "ReAct: Synergizing Reasoning and Acting in Language Models"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf "NIST SP 800-207: Zero Trust Architecture"
[3]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"
[4]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"

# 2.1 Agent Anatomy, Runtime Loop, and Project Organization

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders, technical owners, reviewers, and operators who need to explain what an agent can propose, what the surrounding application controls, and where to inspect the design.

**Applicability:** Every production agent, including a response-only assistant. Tools, skills, retrieval, persistent memory, repeated steps, and durable execution are optional; apply their chapters only when they are present.

**Reader question:** What belongs to the agent and what belongs to the runtime around it, how does a bounded run get from observation to a safe final result, and how can a project make those responsibilities easy to review?

[Part 2 — Agent Basics](README.md) · [Applicability and conformance](../../applicability.md) · [1.3 Agent Suitability and Alternatives](../01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md)

## Purpose and applicability

An **agent** is a bounded part of an application that uses a model to interpret a task or propose a next step. The surrounding application, the **runtime**, supplies the task boundary, trusted inputs, permitted capabilities, checks, and final handling. The word implies no autonomy, tools, memory, long-running process, or framework: a response-only assistant can be an agent.

The key review question is: **what does the model decide or propose, and what does the application decide or enforce on its own?** The model can choose wording, spot a needed clarification, or pick among a finite, already admitted set of next steps. It is never the source of capability membership, identity, authorization, approval, source authority, or any external effect; those come from declared configuration and protected runtime boundaries.

Use the smallest anatomy that supports the task: one validated model response, a fixed workflow whose orchestration owns the transitions, or, only when it adds value a fixed path cannot, a model that chooses the next step or when to stop. Published engineering guidance draws the same line between workflows and agents, advises starting simple, and warns that multi-step designs add latency, cost, and compounding errors. [4]

Details: [2.2](02-agent-contracts-and-configuration.md) (contract and configuration), [2.4](04-tools-and-external-interfaces.md) (tools), [2.6](06-context-and-retrieval-fundamentals.md) (sources and freshness), [Part 3](../03-security-and-trust-boundaries/README.md) (authorization), [Part 4](../04-testing-and-evaluation/README.md) (evaluation), and Parts 6 and 7 (execution).

## Working model

### Separate responsibilities, not necessarily processes

Name the responsibilities and their handoffs; in a small project several can share one module. The aim is a visible line between a proposal and an accepted operation, not more services.

The **model** produces a candidate answer, a clarification request, or a structured proposal; in a bounded adaptive sequence it can also direct the next step. Its output stays data until another boundary accepts it.

**Instructions** tell the model the task, how to respond, and how to handle uncertainty. **Context** is the material assembled for a run: the request, approved task evidence, selected history, and bounded results from admitted capabilities. Instructions guide behavior but grant no permission, and a retrieved passage, model summary, or tool result does not change the operating rules. See [2.3](03-prompts-and-instructions.md) and [2.6](06-context-and-retrieval-fundamentals.md).

A **capability** is something the application can use, such as an external interface or a reusable skill; it is unavailable unless declared configuration admits it. A **tool** is a capability that reaches outside the reasoning process ([2.4](04-tools-and-external-interfaces.md)). A skill can package guidance or resources, but packaging does not grant execution ([2.5](05-skills-and-reusable-capabilities.md)).

The **runtime/control layer** decides whether a proposal is acceptable now. It assembles allowed context, tracks the run, picks or admits the next step, checks limits, calls only admitted operations through their protected boundary, and validates returned results before use. NIST's zero-trust architecture is not an agent blueprint, but its separation of policy decision from enforcement shows why an identifiable decision/enforcement boundary stays useful even when implementation units are combined. [2]

An **output boundary** accepts the final result only when it has the declared shape and holds the declared invariants. Structural validation can reject an unexpected field, a malformed action request, or an unsupported status. It cannot show that a policy claim is right, that a citation supports it, or that an action happened; those need other evidence.

### Configuration is not run state

**Configuration** is the reviewed declaration used to build an agent: purpose, versioned behavior, input/output contract, admitted capabilities, limits, and policies. It answers "What may this candidate be built to do?" See [2.2](02-agent-contracts-and-configuration.md).

**Run state** is the changing record of one attempt: request reference, trusted requester and scope, source identifiers given to the model, admitted proposals, bounded capability results, remaining allowance, observation order, and final result. It answers "What has happened in this attempt?" A run may use up its allowance or receive observations, but it never adds a capability, widens a scope, or rewrites configuration. Secrets and live clients do not belong in serializable state.

Keep **state**, **evidence**, and **authority** distinct. State holds what is needed to continue or finish. Evidence shows what the system observed or decided. Authority is permission checked at a protected operation from trusted identity and policy. A request field, retrieved document, model statement, or earlier successful run can shape a proposal or supply evidence, but none becomes authority by appearing in state.

### A bounded runtime loop

A repeated agent cycles through observe, propose, validate, execute, observe, and terminate. ReAct research interleaves generated actions with external observations [1]; that supports the shape, not exposing reasoning traces or a claim that the pattern is secure or right for every task.

1. **Initialize the run.** Resolve the declared configuration, receive trusted runtime dependencies, and set final outcomes and stop conditions. If required configuration or trusted context is missing, return the declared bounded result rather than inventing a substitute.
2. **Observe.** Use the request, allowed context, and earlier admitted results. Label each input's role: user task, trusted runtime fact, task evidence, or untrusted content. A previous answer or model assertion is not an authoritative observation.
3. **Propose.** The model may produce a candidate answer, an information request, a final outcome, or a structured request for an enabled capability. In a fixed workflow, orchestration may pick the next step without the model.
4. **Validate and admit.** Check the candidate's shape and the proposed operation's permitted name and arguments. At a protected capability boundary, apply identity, authorization, policy, and approval decisions independently. A rejected proposal stays rejected; do not repair it into a broader request.
5. **Execute only an admitted operation.** A response-only path has none. Collect a bounded result or a distinct failure as data. A dispatched attempt, a response, and an authoritative external effect are different observations, and a model saying an action succeeded is not evidence that it did.
6. **Record the next observation.** Add only what the next decision needs, keeping source, capability, and result identity. The application decides whether to continue, clarify, or finish.
7. **Terminate deliberately.** Finish on a valid completion, a declared `needs_information`, `declined`, or `failed` outcome, a blocked proposal, an unresolved boundary, or an enforced stop. Return the typed result and the minimum the caller needs.

The loop may have one pass. Repeat only where a later observation can change a permitted decision, and only with declared stop conditions and resource limits. A limit stop is not a success but a bounded outcome the caller can act on.

## Decisions and best practices

### Choose the simplest execution shape that preserves the boundary

If every meaningful transition can be written down before a run, use a fixed workflow and let the model help only with interpretation or drafting; a router or a branch on a result does not change that. If the model picks a meaningful next action, sequence, or stopping point from observations, record that as the bounded adaptive choice and keep the action set finite and independently enforced.

Do not add a tool just to look agentic: a direct answer from supplied evidence avoids an interface, an access decision, source-selection failure, retry ambiguity, and maintenance. When a tool, long-running sequence, consequential action, or human approval is needed, use the chapters that own them. Build in a sandbox with guardrails and test before widening autonomy. [4]

### Put the external authority boundary outside the model

The runtime, not the model, decides whether an operation is available, especially where a read can expose protected data or an action can change an external system. The protected operation checks trusted identity, target, scope, capability, and policy at execution time ([3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)).

Common shortcuts break this separation:

- Treating a prompt instruction as a tool restriction leaves the capability available.
- Treating a model-written tenant or policy name as trusted state confuses a request with authority.
- Treating fluent model prose as a completed action loses the difference between proposal, dispatch, response, and effect.

Instead, pass the proposal to a narrow interface that does its own checks (see [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)).

### Make an anatomy reviewable through artifacts, not ceremony

No repository tree is prescribed, but reviewers must be able to find the decisions that govern a candidate. Start with the agent contract and an anatomy record that names the responsibilities in use and marks optional components absent. Place instructions, source/context decisions, capability contracts, runtime and validation behavior, tests, and decision notes where a reviewer can connect them.

NIST's Generative AI Profile suggests documenting expected context of use, assumptions and limitations, data origin and lineage, and measurement plans, and showing performance under conditions similar to deployment. [3] That supports keeping artifacts that explain a candidate and its limits; it mandates no file name, role, layout, or test count, and a record does not prove a control works.

Before another agent relies on a shared executable capability, make its maintained contract and the person accountable for changes easy to find; a name alone is not enough. This applies to a small adapter as much as a large package, and does not require a separate repository.

### Failure modes to design against

**A loop with no honest end.** Endless retries hide exhaustion, burn resources, and turn safe uncertainty into an invented answer.

**A proposal that becomes an effect in the same step.** Treating an action request as permission skips checks of capability, target, arguments, and authority. Keep validation and admission observable, even if they run back to back.

**A valid structure treated as a true result.** A schema-valid response can cite the wrong source, apply the wrong policy, or claim an effect that never happened; meaning needs source, authorization, external-state, or evaluation evidence.

**Configuration hidden in mutable run data.** A model output or request names a tool, scope, model setting, or budget and is quietly obeyed. Treat such values as requests that must match the effective configuration.

**A directory that hides the deployed decision.** Instructions, capability definitions, and validation rules sit in untraceable places, so reviewers inspect a document the candidate does not use. Link each artifact to its role and keep identities that let you compare the reviewed candidate with what is later assembled; the effective capability manifest is in 2.2.

### Illustrative project layout

An example, not a required tree; small candidates can co-locate groups.

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

Each group should map to a decision or evidence a reviewer can inspect: `instructions` and `context` keep operating guidance apart from evidence, `capabilities` names each shared interface's maintainer and review owner, and `runtime` makes the proposal-to-enforcement handoff and terminal handling inspectable.

The [agent anatomy record](../../templates/2.1/agent-anatomy-record.yaml) is a neutral planning record that uses the common fictional example and asks for visible unknowns.

## Requirements

- **ANATOMY-01** When a production agent combines a model with instructions, context, capabilities, state, or output validation, its design MUST make those responsibilities and their interfaces identifiable to reviewers, even when they share an implementation unit.
- **ANATOMY-02** When a model can propose actions or further steps, the runtime MUST keep proposals separate from deterministic enforcement and MUST apply the applicable authorization, capability, and policy checks before any action is executed.
- **ANATOMY-03** Every production agent with repeated model or tool steps MUST enforce declared stopping conditions and applicable resource limits, and MUST return a defined terminal result when it stops or cannot continue.
- **ANATOMY-04** When an agent’s output is consumed as structured data or a downstream action request, the receiving boundary MUST validate it against the declared contract before acceptance or use.
- **ANATOMY-05** When executable capabilities are shared across agents or project areas, the shared capabilities MUST have named maintainers and a clear review owner.

## Worked example

The common example is **POLICY-BUILD-001**, a fictional, permission-filtered, read-only internal policy-assistance candidate with planning record **POLICY-PLAN-001** and no external write or approval capability.

Requester `employee-uk-104` asks for the London hotel limit and may read `travel-policy-2026@2026-10-01`, whose current approved text gives GBP 220, and can also encounter `travel-policy-2024-superseded@2024-01-01`, a historical source giving GBP 200. `contractor-uk-204` may read neither.

### Read-only, fixed-path version

The smallest version passes the question, trusted requester context, and an already permission-filtered current passage to the model for a structured answer. The output boundary checks that the status is a declared final outcome, that any cited identifier is among the supplied evidence, and that the required uncertainty field is present. Whether the citation supports the answer is an evaluation question.

Expected results: with the current permitted source, `complete` with GBP 220 and the current source identity; with the current source absent, `needs_information`, not an amount rebuilt from the superseded record; for `contractor-uk-204`, the protected retrieval boundary declines access and the candidate returns `declined` without revealing the amount. The model cannot pick a different requester, collection, or capability to get around either outcome.

### Bounded adaptive alternative

If model-directed source selection is later shown to be needed, the candidate keeps the same read-only scope and adds a finite action allowlist: `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, and `escalate`. The runtime admits only a declared action and validates its arguments.

If the read returns both the current GBP 220 and superseded GBP 200 sources, each with identity and status, the model can propose `complete` citing the current evidence, and the output boundary rejects an unknown source identifier or unsupported status. If two equally authoritative current sources conflict, the candidate returns `needs_information` or the declared clarification/escalation path rather than picking the newer-looking date. A hostile document asking it to reveal restricted material or approve an expense stays data; the missing write capability and protected read boundary keep authority unchanged.

### What a reviewer can inspect

A reviewer can follow the anatomy record from purpose to final result and the evidence that needs evaluation. It can show that no write capability is declared and that a capability request was blocked; it cannot prove that no action was dispatched, that a source supports a claim, or that a control works in operation ([Part 4](../04-testing-and-evaluation/README.md)).

Adding a policy-update action would create a different candidate needing new contract, effect, authority, execution, approval, and evaluation decisions first.

## Evidence and checklist

The review is complete when another reader can trace a run from trusted inputs through a proposal/validation boundary to a declared final outcome. Keep design evidence separate from observations of a real system and keep, proportionately and under data-handling rules: an anatomy record naming response and action boundaries; a loop or state sketch; links to the contract, context and capability records, and evidence plan; and planned cases for a normal completion and a meaningful boundary or failure. Do not retain raw hidden reasoning just to make a run inspectable.

- [ ] The record marks absent optional components rather than implying tools, retrieval, memory, approval, or durable execution.
- [ ] Configuration is distinct from run state; run data cannot silently expand a capability or authority boundary.
- [ ] Proposal, validation, protected authorization, dispatch, response, and external effect stay distinct.
- [ ] Structural validity is not presented as semantic support or a successful effect.
- [ ] The fixed-path and adaptive alternatives keep the same read-only, permission-filtered boundary.
- [ ] The handoff names owners: 2.2 for contract and configuration, 2.4 for interfaces, Part 3 for trust boundaries, Part 4 for evidence, Parts 6 or 7 only when execution triggers arise.

## References

[1]: https://arxiv.org/abs/2210.03629 "ReAct: Synergizing Reasoning and Acting in Language Models"
[2]: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf "NIST SP 800-207: Zero Trust Architecture"
[3]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"
[4]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"

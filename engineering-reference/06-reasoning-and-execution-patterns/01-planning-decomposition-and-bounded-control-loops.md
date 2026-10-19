# 6.1 Planning, Decomposition, and Bounded Control Loops

**Status:** 0.5.0 first draft
**Audience:** Developers and reviewers designing agents that select and sequence actions
**Applicability:** Conditional. Use this chapter when an agent explicitly constructs or revises a plan, chooses among multiple action paths, or repeats model-directed steps. Simple request-response agents and fixed workflows do not need to add a planning layer without a demonstrated need.

[Part 6 — Reasoning and Execution Patterns](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md)

## Purpose and applicability

A plan can make a complex task easier to inspect and can help an agent select relevant next steps. It can also add calls, latency, cost, and new opportunities to drift from the task. A convincing plan is not proof that its steps are useful, safe, or authorized. Treat planning as a conditional design choice, not a mark of agent sophistication.

This chapter concerns the policy around proposing and revising a plan and the control loop that acts on it. It does not redefine the agent contract or tool permissions. See [agent contracts](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md) for declared outcomes and bounds, [tools and external interfaces](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md) for tool contracts, and [identity and least privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) for authorization. When a plan depends on self-critique, see [6.2 Reflection, Critique, and Verification](02-reflection-critique-and-verification.md). Long-running or side-effecting work has additional requirements in [7.1 Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

## Working model

A planning loop has two different kinds of decision. The model may interpret a request, propose a sequence, and recommend the next permitted action. A deterministic control layer decides whether that proposal fits the current contract, capability policy, authorization, and remaining budget; it either admits a permitted action or returns a bounded outcome. The model is an adviser inside those limits, not the source of the limits.

A useful plan is a compact working representation, not a guarantee of correctness. It names the goal, relevant subtasks, dependencies, and what observable evidence would justify completion. Plans should remain revisable when new information changes what is known, but revision must not silently change the user's goal, expand authority, or remove a mandatory check. The system should retain enough observable information to explain which actions were proposed, admitted, completed, rejected, or left unresolved. Raw hidden reasoning is not required as an audit record.

Not every task benefits from explicit decomposition. A short question with a fixed retrieval path may be clearer and cheaper as a direct bounded workflow. Decomposition is more plausible when subtasks are meaningfully distinct, information is incomplete, or the next safe step depends on newly observed results. The appropriate comparison is against a simpler fixed or direct baseline on the cases that matter—not against an idealized claim that more steps produce better answers.

## Decisions and best practices

Start by deciding what planning is meant to improve. Identify the cases where a plan changes action selection or sequencing, the failure it is meant to prevent, and the simpler design it will be compared with. If the plan is only a narration of a fixed sequence, a model-generated plan may add complexity without adding control. Keep plans short enough that the runtime can check their proposed actions against the contract.

Decompose around useful boundaries: a subtask should have a defined purpose, required inputs, dependencies, and an observable completion condition. Avoid inventing subtasks whose completion cannot be checked or whose result does not affect the answer. Represent uncertainty explicitly. If a needed input is absent, the next step may be a clarification or an `needs_information` outcome rather than a speculative branch.

Replanning is appropriate when an admitted action returns information that changes the choice of a safe next step, or when a declared condition makes the current plan infeasible. It should not be an automatic response to every weak answer. Define which observations permit revision, how many revisions are allowed, and what happens if the goal or scope appears to have changed. A materially different task should be returned for clarification or handled as a new authorized request, not smuggled into an existing plan.

Bound the whole run, not only the number of written plan steps. A plan can trigger repeated model calls or tool calls, so limits should cover applicable iterations, time, and spend-producing operations. Enforce them outside model discretion. On exhaustion, stop admitting new work and return the contract's declared partial, failed, or escalation outcome. A bounded plan may still fail; boundedness limits exposure and makes stopping predictable, but it does not establish task quality.

Before completion, require an observable stopping condition. Examples include an answer supported by the required evidence, a declared information gap, a policy refusal, a blocked action, or a budget limit. Do not let the model call a task complete solely because it has exhausted its preferred steps. Link the stop decision to the output contract and applicable evidence.

## Requirements

- **PLAN-01** When an agent uses explicit planning to select or sequence actions, the owner MUST define the planning use case, the task cases where planning applies, and a simpler baseline against which its added value will be evaluated.
- **PLAN-02** When a plan proposes an action, the runtime MUST admit that action only after deterministic checks confirm that it is within the declared task scope, enabled capabilities, authorization, and applicable policy; a model proposal MUST NOT grant or expand authority.
- **PLAN-03** When an agent runs a model-directed planning loop, the owner MUST set applicable limits for iterations and other resource-consuming work, and the runtime MUST enforce those limits independently of model output and stop new work when a limit is reached.
- **PLAN-04** When replanning is enabled, the owner MUST specify the observations that permit revision, the maximum revision or loop bounds, and the outcome for a changed or infeasible goal; revision MUST NOT silently broaden the authorized task or bypass required checks.
- **PLAN-05** When a planning loop can terminate, the contract MUST define observable completion and non-completion outcomes, and the runtime MUST return a bounded partial, needs-information, declined, failed, or escalation outcome when its stopping evidence or budget does not support completion.
- **PLAN-06** Before release of an agent whose behavior depends on explicit planning, the owner MUST evaluate planning against the simpler baseline on relevant cases, including applicable failure and resource-exhaustion cases, and MUST NOT infer improvement merely from longer plans or more completed steps.

## Worked example: policy assistant with a conflicting document

Consider the fictional read-only policy assistant described in the shared example. It answers from approved, current, permission-filtered documents and returns citations plus uncertainty. It cannot write to external systems. A fixture named `travel-policy-current` says a London hotel amount of GBP 220 is permitted; a superseded document differs. This is fictional test data, not actual policy.

For a simple question—“What is the London hotel amount?”—the team first asks whether explicit planning changes the necessary work. If the fixed retrieval path already selects current, approved documents and checks source status, the direct workflow may be sufficient. The system need not ask a model to create a multi-step plan just to restate that fixed sequence.

Now consider a question that asks whether GBP 220 is permitted for an upcoming London stay and includes an attached document that may be old. An explicit plan could propose: identify the relevant policy topic and trip context; retrieve the current policy from the approved permission-filtered source; check whether the attached document is superseded; then answer with citations or state what remains uncertain. These are proposals. Before each retrieval, the runtime checks that the source is allowed for this user and that the request remains within the read-only contract. A document's instructions cannot add capabilities or change those checks.

The control layer can impose an illustrative maximum of three admitted retrieval actions and a run deadline. Those are example policy values, not universal limits or measured performance. If current approved text confirms the fictional GBP 220 allowance and the older attachment is identified as superseded, the assistant can answer with a citation to the current source and explain the document conflict. It stops when the answer has the required support. If the current source is unavailable, access is denied, or approved sources conflict, it does not keep searching without limit or treat the old amount as current; it returns `needs_information` or the declared failure/escalation outcome. Replanning may choose a permitted source check after a result reveals the attachment is stale, but it cannot change the trip, user, policy source boundary, or authority.

To determine whether planning belongs in this design, evaluate the planned and simpler versions on cases covering straightforward questions, stale or conflicting policy text, missing current evidence, permission denial, and exhausted limits. Check answer support and citations as distinct claims: a citation being present does not by itself prove that it supports the answer. Also record whether planning introduced extra calls, delay, or cost. The example does not assert that planning improves results; that conclusion requires evidence from the agent's own defined evaluation.

## Evidence and checklist

The release record should identify the candidate configuration and the planning policy it uses. Evidence should make it possible to see whether planning changed the trajectory and whether the admitted actions remained within the contract. A useful evaluation connects each planning requirement to cases and a reviewer or evaluator suited to the claim; detailed case, evaluator, and release-decision practice belongs in [Part 4 — Testing and Evaluation](../../development-guide/04-testing-and-evaluation/README.md), especially [4.5 Planning, Designing, and Running Tests and Evaluations](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md).

Before release, check that:

- The record explains when planning is used and why a direct or fixed baseline is not enough for those cases.
- Proposed actions are checked by the control layer; no plan or model output can authorize a capability.
- Iteration, time, and applicable resource limits are enforced, with a defined safe outcome on exhaustion.
- Replanning triggers and bounds are explicit, and changed scope cannot silently proceed.
- Completion depends on observable evidence; missing or conflicting information has a declared outcome.
- Evaluation includes relevant adverse cases and compares task outcomes as well as added work against the simpler baseline.

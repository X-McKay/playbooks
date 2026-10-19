# 6.1 Planning, Decomposition, and Bounded Control Loops

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers designing agents that select and sequence actions
**Applicability:** Conditional. Use this chapter when an agent builds or revises a plan, chooses among action paths, or repeats model-directed steps. Simple request-response agents and fixed workflows do not need a planning layer without a demonstrated need.

[Part 6 — Reasoning and Execution Patterns](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md)

## Purpose and applicability

A plan makes a complex task easier to inspect and helps an agent pick relevant next steps. It also adds calls, latency and cost, and gives the agent more room to drift. A convincing plan does not prove its steps are useful, safe or authorized. Treat planning as a design choice that needs a reason, not as a sign of sophistication.

This chapter covers the policy for proposing and revising a plan, and the control loop that acts on it. For declared outcomes and bounds, see [agent contracts](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). For tool contracts, see [tools and external interfaces](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md). For authorization, see [identity and least privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md). For plans that depend on self-critique, see [6.2 Reflection, Critique, and Verification](02-reflection-critique-and-verification.md). For long-running or side-effecting work, see [7.1 Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

## Working model

A planning loop makes two kinds of decision. The model interprets the request, proposes a sequence and recommends the next action. A deterministic control layer checks each proposal against the contract, capability policy, authorization and remaining budget, then either admits the action or returns a bounded outcome. The model advises inside these limits. It does not set them.

A good plan is short. It names the goal, the subtasks, their dependencies, and the evidence that would show the task is done. A plan can change when new information arrives, but a revision must not quietly change the user's goal, expand authority or drop a mandatory check. Keep enough observable information to explain which actions were proposed, admitted, completed, rejected or left unresolved. Raw hidden reasoning is not needed as an audit record.

Not every task needs decomposition. A short question with a fixed retrieval path is often clearer and cheaper as a direct workflow. Decomposition fits better when subtasks are distinct, information is incomplete, or the next safe step depends on what earlier steps return. Compare against a simpler fixed or direct baseline on the cases that matter. Do not assume more steps give better answers.

## Decisions and best practices

Decide what planning should improve. Name the cases where a plan changes action selection or order, the failure it should prevent, and the simpler design you will compare it with. If the plan only narrates a fixed sequence, it adds complexity without adding control. Keep plans short enough for the runtime to check each proposed action against the contract.

Split work along useful boundaries. Each subtask needs a purpose, inputs, dependencies and a completion condition you can observe. Skip subtasks whose completion cannot be checked or whose result does not affect the answer. Show uncertainty. If a needed input is missing, the next step can be a clarification or a `needs_information` outcome rather than a guess.

Replan when an admitted action returns information that changes the safe next step, or when a declared condition makes the plan infeasible. Do not replan after every weak answer. Define which observations allow a revision, how many revisions are allowed, and what happens if the goal or scope seems to have changed. A materially different task goes back for clarification or becomes a new authorized request. It does not get folded into the existing plan.

Bound the whole run, not just the number of plan steps. One plan can trigger many model and tool calls, so set limits on iterations, time and operations that spend money. Enforce them outside the model. When a limit is hit, stop admitting new work and return the contract's partial, failed or escalation outcome. Bounds limit exposure and make stopping predictable. They do not make the result good.

Require a stopping condition you can observe before the task counts as complete. Examples are an answer backed by the required evidence, a declared information gap, a policy refusal, a blocked action or a budget limit. The model must not call a task complete just because it ran out of preferred steps. Tie the stop decision to the output contract and the evidence.

When a task outlasts one context window, the next session starts with no memory of the last. Leave a handoff the next session reads first: a progress log, a clean saved state, and an acceptance list of the features or checks that define done, each marked failing until verified. Let the agent flip an item's status only after it has verified the item end to end. Do not let it edit or delete items, because an agent can otherwise "finish" by weakening the list. Work one item at a time, and check the whole list before declaring completion, since agents tend to call a project done after seeing partial progress.[1] See also [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

## Requirements

- **PLAN-01** When an agent uses explicit planning to select or sequence actions, the owner MUST define the planning use case, the task cases where planning applies, and a simpler baseline against which its added value will be evaluated.
- **PLAN-02** When a plan proposes an action, the runtime MUST admit that action only after deterministic checks confirm that it is within the declared task scope, enabled capabilities, authorization, and applicable policy; a model proposal MUST NOT grant or expand authority.
- **PLAN-03** When an agent runs a model-directed planning loop, the owner MUST set applicable limits for iterations and other resource-consuming work, and the runtime MUST enforce those limits independently of model output and stop new work when a limit is reached.
- **PLAN-04** When replanning is enabled, the owner MUST specify the observations that permit revision, the maximum revision or loop bounds, and the outcome for a changed or infeasible goal; revision MUST NOT silently broaden the authorized task or bypass required checks.
- **PLAN-05** When a planning loop can terminate, the contract MUST define observable completion and non-completion outcomes, and the runtime MUST return a bounded partial, needs-information, declined, failed, or escalation outcome when its stopping evidence or budget does not support completion.
- **PLAN-06** Before release of an agent whose behavior depends on explicit planning, the owner MUST evaluate planning against the simpler baseline on relevant cases, including applicable failure and resource-exhaustion cases, and MUST NOT infer improvement merely from longer plans or more completed steps.

## Worked example: policy assistant with a conflicting document

This example uses the fictional read-only policy assistant from the shared example. It answers from approved, current, permission-filtered documents, returns citations and uncertainty, and cannot write to external systems. A fixture named `travel-policy-current` says a London hotel amount of GBP 220 is permitted. A superseded document differs. All of this is made-up test data.

For a simple question such as "What is the London hotel amount?", first ask whether explicit planning changes the work. If a fixed retrieval path already selects current, approved documents and checks source status, the direct workflow is enough. Do not ask a model to write a multi-step plan that restates a fixed sequence.

Now take a question that asks whether GBP 220 is permitted for an upcoming London stay and attaches a document that may be old. A plan could be: identify the policy topic and trip context; retrieve the current policy from the approved source; check whether the attachment is superseded; answer with citations or say what remains uncertain. These are proposals. Before each retrieval, the runtime checks that the source is allowed for this user and that the request stays within the read-only contract. Instructions inside a document cannot add capabilities or change these checks.

The control layer sets a maximum of three admitted retrievals and a run deadline. These are example values, not recommended limits. If current approved text confirms GBP 220 and the attachment is superseded, the assistant answers with a citation to the current source and explains the conflict. It stops once the answer has the required support. If the current source is unavailable, access is denied, or approved sources conflict, it does not search without limit or treat the old amount as current. It returns `needs_information` or the declared failure or escalation outcome. Replanning may choose a permitted source check after the attachment turns out to be stale. It cannot change the trip, the user, the source boundary or the authority.

To decide whether planning belongs in this design, test the planned and simpler versions on straightforward questions, stale or conflicting text, missing current evidence, permission denial and exhausted limits. Check answer support and citations separately: a citation being present does not show it supports the answer. Record any extra calls, delay or cost. The example does not claim planning improves results. Only your own evaluation can show that.

## Evidence and checklist

The release record should identify the candidate configuration and its planning policy. Evidence should show whether planning changed the trajectory and whether admitted actions stayed within the contract. Link each planning requirement to test cases and a suitable evaluator. For case design, evaluators and release decisions, see [Part 4 — Testing and Evaluation](../../development-guide/04-testing-and-evaluation/README.md), especially [4.5 Planning, Designing, and Running Tests and Evaluations](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md).

Before release, check that:

- The record explains when planning is used and why a direct or fixed baseline is not enough for those cases.
- The control layer checks proposed actions. No plan or model output can authorize a capability.
- Iteration, time and resource limits are enforced, with a defined safe outcome on exhaustion.
- Replanning triggers and bounds are explicit, and a changed scope cannot proceed silently.
- Completion depends on observable evidence. Missing or conflicting information has a declared outcome.
- Evaluation includes adverse cases and compares both task outcomes and added work against the simpler baseline.

## References

[1]: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents "Effective harnesses for long-running agents"

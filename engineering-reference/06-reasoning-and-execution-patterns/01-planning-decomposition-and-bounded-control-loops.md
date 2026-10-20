# 6.1 Planning, Decomposition, and Bounded Control Loops

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers designing agents that select and sequence actions
**Applicability:** Conditional. Use when an agent builds or revises a plan, chooses among action paths, or repeats model-directed steps. Simple request-response agents and fixed workflows do not need a planning layer without a demonstrated need.

[Part 6 — Reasoning and Execution Patterns](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md)

## Purpose and applicability

A plan makes a complex task easier to inspect and helps an agent pick next steps. It also adds calls, latency, cost and room to drift, and a convincing plan does not prove its steps are useful, safe or authorized. Planning needs a reason.

This chapter covers proposing and revising a plan and the loop that acts on it. Related: [agent contracts](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md), [tools](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md), [identity and least privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), [6.2 self-critique](02-reflection-critique-and-verification.md) and, for long-running or side-effecting work, [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

## Working model

The model interprets the request, proposes a sequence and recommends the next action. A deterministic control layer checks each proposal against the contract, capability policy, authorization and remaining budget, then admits the action or returns a bounded outcome. The model advises inside these limits; it does not set them.

A good plan is short enough for the runtime to check each proposed action: goal, subtasks, dependencies and the evidence that shows done. Keep it revisable as new information arrives, within the limits on replanning below. Record which actions were proposed, admitted, completed, rejected or left unresolved; raw hidden reasoning is not needed as an audit record.

A short question with a fixed retrieval path is clearer and cheaper as a direct workflow. Decomposition fits when subtasks are distinct, information is incomplete, or the next safe step depends on earlier results. More steps do not mean better answers.

## Decisions and best practices

- **Name what planning should improve.** List the cases where a plan changes action choice or order, the failure it prevents, and the simpler design to compare with. A plan that narrates a fixed sequence adds complexity without control.
- **Split along useful boundaries.** Each subtask needs a purpose, inputs, dependencies and an observable completion condition; skip ones you cannot check or that do not affect the answer. If an input is missing, the next step can be a clarification or `needs_information` rather than a guess.
- **Replan on evidence, not on every weak answer.** Replan when an admitted action returns information that changes the safe next step, or a declared condition makes the plan infeasible. A revision must not quietly change the goal, expand authority or drop a check; a materially different task goes back for clarification or becomes a new authorized request.
- **Bound the whole run.** One plan can trigger many model and tool calls, so limit iterations, time and spending operations, and enforce the limits outside the model. On a limit, stop admitting work and return the contract's partial, failed or escalation outcome. Bounds make stopping predictable; they do not make the result good.
- **Stop on observable evidence.** A task is complete only on a declared condition: an answer with the required evidence, an information gap, a policy refusal, a blocked action or a budget limit. Running out of preferred steps is not completion.
- **Hand off across context windows.** A new session has no memory of the last, so leave a progress log, a clean saved state and an acceptance list of checks that define done, each failing until verified. The agent may flip an item only after verifying it end to end, never edit or delete items (or it can "finish" by weakening the list), should work one item at a time, and must check the whole list before declaring completion, since agents tend to call a project done after partial progress.[1] See also [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

## Requirements

- **PLAN-01** When an agent uses explicit planning to select or sequence actions, the owner MUST define the planning use case, the task cases where planning applies, and a simpler baseline against which its added value will be evaluated.
- **PLAN-02** When a plan proposes an action, the runtime MUST admit that action only after deterministic checks confirm that it is within the declared task scope, enabled capabilities, authorization, and applicable policy; a model proposal MUST NOT grant or expand authority.
- **PLAN-03** When an agent runs a model-directed planning loop, the owner MUST set applicable limits for iterations and other resource-consuming work, and the runtime MUST enforce those limits independently of model output and stop new work when a limit is reached.
- **PLAN-04** When replanning is enabled, the owner MUST specify the observations that permit revision, the maximum revision or loop bounds, and the outcome for a changed or infeasible goal; revision MUST NOT silently broaden the authorized task or bypass required checks.
- **PLAN-05** When a planning loop can terminate, the contract MUST define observable completion and non-completion outcomes, and the runtime MUST return a bounded partial, needs-information, declined, failed, or escalation outcome when its stopping evidence or budget does not support completion.
- **PLAN-06** Before release of an agent whose behavior depends on explicit planning, the owner MUST evaluate planning against the simpler baseline on relevant cases, including applicable failure and resource-exhaustion cases, and MUST NOT infer improvement merely from longer plans or more completed steps.

## Worked example: policy assistant with a conflicting document

The fictional read-only policy assistant answers from approved, current, permission-filtered documents with citations and cannot write externally. Fixture `travel-policy-current` permits a London hotel amount of GBP 220; a superseded document differs.

For "What is the London hotel amount?", a fixed retrieval path that selects current, approved documents is enough; a plan would only restate it.

For "Is GBP 220 permitted for my upcoming London stay?" with an attachment that may be old, a plan could be: identify the topic and trip context; retrieve the current policy from the approved source; check whether the attachment is superseded; answer with citations or state what is uncertain. Before each retrieval the runtime checks that the source is allowed for this user and the request stays read-only; document text cannot change these checks.

The control layer allows at most three admitted retrievals and a run deadline (example values). If current approved text confirms GBP 220 and the attachment is superseded, the assistant cites the current source, explains the conflict and stops. If the current source is unavailable, access is denied or approved sources conflict, it returns `needs_information` or the declared failure or escalation outcome rather than searching on or treating the old amount as current. Replanning may add a permitted source check once the attachment proves stale, but cannot change the trip, user, source boundary or authority.

To decide whether planning belongs here, test planned and simpler versions on straightforward questions, stale or conflicting text, missing evidence, permission denial and exhausted limits. Check citation support, not just presence, and record extra calls, delay and cost.

## Evidence and checklist

The release record names the configuration and planning policy, shows whether planning changed the trajectory and admitted actions stayed in contract, and links each requirement to tests and an evaluator (see [Part 4](../../development-guide/04-testing-and-evaluation/README.md), especially [4.5](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md)).

- The record says why a direct or fixed baseline is not enough.
- Limits have a safe outcome on exhaustion, and a changed scope cannot proceed silently.
- Evaluation covers adverse cases and compares outcomes and added work with the baseline.

## References

[1]: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents "Effective harnesses for long-running agents"

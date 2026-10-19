# 6.3 Parallel Work, State, and Failure Propagation

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers of agents that run independent operations concurrently.
**Applicability:** Use when one agent runs multiple tools or bounded sub-tasks at once. Serial agents do not need it. When sub-tasks are autonomous agents with their own identities or authority, also apply [Part 9](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md).

[Part 6](README.md) · [Applicability](../../applicability.md) · [6.1 Planning](01-planning-decomposition-and-bounded-control-loops.md) · [6.2 Reflection](02-reflection-critique-and-verification.md) · [7.1 Durable execution](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) · [9.2 Delegation](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)

## Purpose and applicability

Parallel work can shorten a task when operations are truly independent. It can also multiply calls, use up scarce capacity, produce contradictory results and make failures harder to read. Use it only where the benefit justifies these costs. One agent that calls several read-only retrieval tools in parallel is still one agent. Its coordinator owns the plan, the shared limits, the merge and the final outcome. It is not a multi-agent system.

Treat each parallel sub-task's input and output as a separate work item. A tool result or sub-task result is data. It is not authorization, and it does not prove that an external effect happened. For tool contracts and trust boundaries, see [tools and external interfaces](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md) and [untrusted inputs](../../development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). If a task must resume after process loss, or a branch may cause an external effect, also apply [durable execution](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) and [external effects and idempotency](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). Parallel execution alone does not need a durable engine.

## Working model

A coordinator splits a request into bounded branches, starts them, records each result or failure, and joins them under a declared rule. A branch has a stable ID within the run, an input, a purpose, a completion condition and finite limits. The join is a decision point. It sets which branch outcomes are necessary, how evidence is combined and what the user-facing result means.

Do not let branches write to one shared conversation or result object as they finish. Keep branch outputs separate, and have the coordinator accept and merge them through a defined state transition. For persistent work, keep state in versioned, serializable form and validate changes before accepting them (see [execution classes, persistence, and recovery](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md)). For short-lived work, the same separation can live in memory, as long as failure and cancellation still give a bounded, honest result.

Parallelism is about scheduling, not trust. Delegating to an autonomous agent creates a boundary between principals: the receiver makes its own choices, so its authority, identity, data access and result contract need control. See the [multi-agent composition chapter](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md) and the [delegation chapter](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md).

## Decisions and best practices

### Choose a join rule before launching work

Use an all-required join when every branch supplies a necessary check or piece of evidence. Use optional branches only where the others can still give a valid result without them. Use a quorum or "first acceptable result" rule only when the task defines what counts, which evidence qualifies and how disagreement is handled. A fast branch is not a better branch. Unless arrival order matters to the task, merge in a stable logical order, not in finishing order.

Failure policy follows branch purpose. A required branch that times out, is denied or returns invalid output normally blocks the result or triggers a declared escalation. A failed optional branch can be left out, but the final outcome must not imply its evidence was obtained. Keep material disagreement and provenance. Do not average away a conflict or treat missing work as agreement.

### Keep state changes isolated

Branches should produce candidate results, not overwrite shared state. If branches update one logical record, collect their proposed changes and apply them in one serialized, validated step. When proposals conflict, use an explicit rule: reject the combination, prefer a named authoritative source, ask for clarification, or return a bounded partial result. Do not let last-write-wins or completion timing decide a user-visible fact.

### Cancel deliberately and propagate failures honestly

Cancellation is a request. It does not prove that every in-flight operation stopped before doing work. Define what is cancelled when the caller cancels, the deadline passes, required evidence is unavailable, or enough evidence has arrived. Decide how to treat late results: accept one only if the run is still open and the result passes validation, otherwise mark it late and leave it out of the join. Completed reads need no undoing. For branches that can cause effects, cancellation and compensation follow the [durable-execution and effect rules](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). Cancelling does not erase a completed action.

Tell apart at least a complete result, a declared partial or degraded result, a need for more information, and a failure. A partial result names what is missing and what the user should not infer from it. Do not report an interrupted required branch as success because other branches finished.

### Bound fan-out and capacity

Before running, set a maximum number of active branches and a maximum total branch count. Also bound branch depth or rounds where work can expand, per-branch time and output, and the overall deadline and budget. Reserve capacity for required validation and finalization instead of giving everything to optional exploration. When limits prevent the planned fan-out, queue within a stated wait, use a tested reduced mode, ask the user to narrow the request, or stop safely. Never quietly drop a required branch to keep throughput up. If cost is unknown, treat it as unknown, not free. Shared admission and backpressure are covered in [Part 8](../08-model-context-and-resource-engineering/README.md).

Parallel tool calls are not independent just because they are separate calls. Before launching, check whether they share a rate limit, rely on shared mutable state, repeat a consequential action, or depend on each other's results. Serialize, deduplicate or disallow those branches unless a safe coordination rule exists. If the next step depends on results, start only the independent work, join it, then decide what follows.

## Requirements

- **PARALLEL-01** For an agent that schedules concurrent branches, the coordinator MUST establish finite per-run fan-out and active-concurrency limits, branch completion criteria, and an overall deadline or stopping condition before dispatch; additional depth, rounds, and resource limits MUST be bounded wherever branches can create further work.
- **PARALLEL-02** For every multi-branch join, the coordinator MUST declare which branches are required, optional, or substitutable and MUST define how valid evidence, failures, missing results, conflicts, and late results affect the terminal outcome; aggregation MUST preserve material provenance and disagreement.
- **PARALLEL-03** When concurrent branches can propose changes to shared state, the agent MUST keep proposals isolated until a validated coordinator transition accepts them and MUST apply a declared conflict rule rather than relying on arrival order or uncontrolled overwrites.
- **PARALLEL-04** When cancellation, timeout, or early completion can occur, the agent MUST specify which branches are cancelled, how late results are handled, and how terminal outcomes distinguish complete, partial/degraded, information-needed, and failed work; cancellation MUST NOT be represented as proof that an in-flight or completed effect was undone.
- **PARALLEL-05** When branches use shared capacity or can repeat an operation, the agent MUST apply a shared admission/budget bound and MUST serialize, deduplicate, or otherwise constrain concurrent operations whose effects or state are not safe to repeat or race.

## Worked example: answering a policy question

A user asks the internal policy assistant, "Does the current travel policy permit a London hotel costing GBP 220?" The assistant has read-only access to approved, current, permission-filtered policy documents. All data here is fictional. It runs three bounded read branches: retrieve the matching current policy passage; check the passage's approved-source and effective-version metadata; and search the authorized archive for a superseded passage that may conflict. No branch can change policy or book a hotel.

The join rule makes the first two branches required. The answer is allowed only if the passage is authorized and the version check shows it is current. The archive search is advisory. It can surface a conflict for the coordinator to classify, but finding nothing does not prove no older copy exists. A stale copy does not govern once the approved current source is verified. If the version check fails or times out, the assistant returns `needs_information` or an equivalent declared outcome, not a guess about which document is current. If the archive search times out, the assistant can still answer from the verified current source, but must not claim it searched every historical record.

In this test, the current approved document permits GBP 220 and the superseded copy differs. The coordinator stores the three results separately, checks source status, and accepts only verified current evidence. It answers that GBP 220 is permitted under the current approved policy and cites that document. It may mention that an older, superseded copy differs, while making clear the older text is not its source. It does not combine the two amounts, pick whichever search returned first, or hide the conflict.

Now suppose the current-passage and version branches succeed but the archive search is still running once the evidence requirements are met. The coordinator may cancel that optional branch. If it returns later, the result is marked late and excluded from the closed run. A new task can look into it. If a required branch was cancelled or failed, the same completion rule does not apply, and the result is a bounded information-needed or failure outcome, not a complete answer. The assistant has no write capability, so this example needs neither approval nor compensation.

## Evidence and checklist

Test these cases: completion order changes, a required timeout, an optional failure, conflicting branch results, cancellation with a late response, and fan-out exhaustion. Check the accepted terminal state and evidence, not just that every launched call came back. Add a shared-state conflict or duplicate-operation test if branches touch mutable state or perform effects. For durable branches, add replay, cancellation and effect-reconciliation evidence from Part 7.

- [ ] The branch set separates required work from optional exploration.
- [ ] Maximum fan-out, concurrency, per-branch bounds and overall stopping conditions are finite.
- [ ] Join behavior is defined for invalid, missing, late, conflicting and failed branch results.
- [ ] Shared state changes are validated, and conflict handling does not depend on timing.
- [ ] Cancellation and partial outcomes are visible and do not imply that effects were reversed.
- [ ] Tests show that capacity exhaustion cannot silently discard required evidence or checks.

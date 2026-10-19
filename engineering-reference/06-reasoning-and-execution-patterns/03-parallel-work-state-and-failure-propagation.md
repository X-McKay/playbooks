# 6.3 Parallel Work, State, and Failure Propagation

**Status:** 0.5.0 first draft
**Audience:** Developers and reviewers of agents that run independent operations concurrently.
**Applicability:** Use when one agent schedules multiple tools or bounded sub-tasks at once. Serial agents do not need parallel orchestration. When sub-tasks are autonomous agents with their own identities, authority, or membership, also apply [Part 9](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md).

[Part 6](README.md) · [Applicability](../../applicability.md) · [6.1 Planning](01-planning-decomposition-and-bounded-control-loops.md) · [6.2 Reflection](02-reflection-critique-and-verification.md) · [7.1 Durable execution](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) · [9.2 Delegation](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)

## Purpose and applicability

Parallel work can shorten a task when separate operations are genuinely independent. It can also multiply calls, consume scarce capacity, produce contradictory results, and make failures harder to interpret. Use concurrency only where its benefit justifies those costs. A single agent that invokes several read-only retrieval tools in parallel remains one agent: its coordinator owns the plan, shared limits, merge, and final outcome. It is not thereby a multi-agent system.

Parallel sub-tasks may use the same agent capabilities, but their inputs and outputs should still be treated as separate work items. A tool result or model-produced sub-task result is data, not authorization or proof that an external effect occurred. Tool contracts and trust boundaries remain governed by [tools and external interfaces](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md) and [untrusted inputs](../../development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md). If a task must resume after process loss, or a branch may cause an external effect, apply [durable execution](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) and [external effects and idempotency](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) as applicable. Parallel execution alone does not require a durable engine.

## Working model

A coordinator decomposes a request into bounded branches, starts eligible branches, records each branch's result or failure, and joins them under a declared rule. A branch has a stable identity within the run, an input, a purpose, a completion condition, and finite limits. The join is a decision point: it determines which branch outcomes are necessary, how evidence is combined, and what the user-facing result means.

Do not make multiple branches mutate one shared conversation or result object as they finish. Keep branch-local outputs separate, then have the coordinator accept and merge them through a defined state transition. For persistent work, represent state in versioned, serializable forms and validate proposed changes before accepting them; see [execution classes, persistence, and recovery](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md). For short-lived work, the same separation can be maintained in memory, provided failure and cancellation still lead to a bounded, honest result.

Parallelism is about scheduling, not trust. By contrast, delegation to an autonomous agent creates a boundary between principals: the receiving agent may make its own choices, and its authority, identity, data access, and result contract must be controlled. The [multi-agent composition chapter](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md) and [delegation chapter](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md) own those additional rules.

## Decisions and best practices

### Choose a join rule before launching work

Use an all-required join when every branch supplies a necessary check or evidence item. Use optional branches only where the remaining branches can still produce a valid result without them. A quorum or “first acceptable result” rule is appropriate only when the task defines what counts, which evidence qualifies, and how disagreement is handled. A branch's quick arrival is not a quality signal. Unless the task explicitly makes arrival order meaningful, merge in a stable logical order rather than whichever order happens to finish.

Failure policy follows branch purpose. A required branch that times out, is denied, or returns invalid output normally blocks the result or leads to a declared escalation. A failed optional branch may be omitted, but the final outcome must not imply that its evidence was obtained. Preserve material disagreement and provenance; do not average away a conflict or silently treat missing work as agreement.

### Keep state changes isolated

Concurrent branches should produce candidate results, not overwrite shared state. If branches need to update one logical record, collect their proposed changes and apply them in a serialized, validated step. When two proposals conflict, use an explicit rule: reject the combination, prioritize a named authoritative source, request clarification, or produce a bounded partial result. Do not let last-write-wins behavior or completion timing decide a user-visible fact by accident.

### Cancel deliberately and propagate failures honestly

Cancellation is a control request, not proof that every in-flight operation stopped before doing work. Define which work is cancelled when the caller cancels, the deadline expires, required evidence is unavailable, or enough evidence has been gathered. Decide what to do with late results: accept only if the run is still open and the result passes validation, otherwise mark it as late and exclude it from the join. Completed read work need not be undone. For branches that can cause effects, cancellation and compensation follow the applicable durable-execution and effect rules; cancellation does not erase a completed action.

Distinguish at least a complete result, a declared partial/degraded result, a need for more information, and a failure. A partial result names what is missing and what the user should not infer from it. Do not turn an interrupted required branch into an ordinary success merely because other branches completed.

### Bound fan-out and capacity

Set a maximum number of active branches and a maximum total branch count before execution. Also bound branch depth or rounds where work can expand, per-branch time and output, and the overall deadline and resource budget. Reserve capacity for required validation and finalization instead of allocating every available unit to optional exploration. When admission limits prevent the planned fan-out, queue within a stated wait, select a tested reduced mode, ask the user to narrow the request, or stop safely. Never silently drop a required branch to preserve throughput. If cost is unknown, treat it as unknown rather than free; shared admission and backpressure are detailed in [Part 8](../08-model-context-and-resource-engineering/README.md).

Parallel tool calls are not always independent just because they are syntactically separate. Before launching, check whether they compete for a rate limit, rely on shared mutable state, duplicate a consequential action, or depend on each other's results. Serialize, deduplicate, or disallow those branches unless a safe coordination rule is defined. If the desired next step depends on results, start only the independent work first, join it, then decide what follows.

## Requirements

- **PARALLEL-01** For an agent that schedules concurrent branches, the coordinator MUST establish finite per-run fan-out and active-concurrency limits, branch completion criteria, and an overall deadline or stopping condition before dispatch; additional depth, rounds, and resource limits MUST be bounded wherever branches can create further work.
- **PARALLEL-02** For every multi-branch join, the coordinator MUST declare which branches are required, optional, or substitutable and MUST define how valid evidence, failures, missing results, conflicts, and late results affect the terminal outcome; aggregation MUST preserve material provenance and disagreement.
- **PARALLEL-03** When concurrent branches can propose changes to shared state, the agent MUST keep proposals isolated until a validated coordinator transition accepts them and MUST apply a declared conflict rule rather than relying on arrival order or uncontrolled overwrites.
- **PARALLEL-04** When cancellation, timeout, or early completion can occur, the agent MUST specify which branches are cancelled, how late results are handled, and how terminal outcomes distinguish complete, partial/degraded, information-needed, and failed work; cancellation MUST NOT be represented as proof that an in-flight or completed effect was undone.
- **PARALLEL-05** When branches use shared capacity or can repeat an operation, the agent MUST apply a shared admission/budget bound and MUST serialize, deduplicate, or otherwise constrain concurrent operations whose effects or state are not safe to repeat or race.

## Worked example: answering a policy question

A user asks the internal policy assistant, “Does the current travel policy permit a London hotel costing GBP 220?” The assistant has read-only access to approved, current, permission-filtered policy documents. Its three branches are all bounded reads: retrieve the matching current policy passage; check the passage's approved-source and effective-version metadata; and search the authorized archive for a potentially conflicting superseded passage. No branch can change policy or book a hotel.

The join rule says the first two branches are required. The answer is eligible only if the passage is authorized and the version check identifies it as current. The archive search is advisory: it can surface a conflict for the coordinator to classify, but its absence cannot establish that no older copy exists. A stale copy is not treated as governing when the approved current source is verified. If the required version check fails or times out, the assistant returns `needs_information` or an equivalent declared outcome rather than guessing which document is current. If the archive search times out, the assistant can still answer from the verified current source, but must not claim it searched every historical record.

In this fictional test, the current approved document permits GBP 220 and the superseded copy differs. The coordinator stores the three branch results separately, checks source status, and accepts only verified current evidence for the answer. It responds that GBP 220 is permitted under the current approved policy and cites that document. It may note that an older superseded copy differs if that fact is relevant, while making clear that the older text is not the source for its answer. The assistant does not combine the two amounts, choose whichever search returned first, or hide the provenance conflict.

Suppose instead the current-passage and version branches succeed but the archive search is still running after the answer's evidence requirements are met. The coordinator may request cancellation of that optional branch. If it later returns, the result is marked late and excluded from the closed run; a new task may investigate it if needed. If a required branch was cancelled or failed, the assistant cannot use the same completion rule. The result is a bounded information-needed or failure outcome, not a complete answer. The same policy assistant has no external write capability, so this example needs neither action approval nor compensation.

## Evidence and checklist

Demonstrate the policy with tests that exercise completion order changes, a required timeout, an optional failure, conflicting branch results, cancellation with a late response, and fan-out exhaustion. Check the accepted terminal state and evidence, not just that all launched calls eventually returned. Include a shared-state conflict or duplicate-operation test if branches can touch mutable state or perform effects. For durable branches, add the applicable replay, cancellation, and effect-reconciliation evidence from Part 7.

- [ ] The documented branch set separates required work from optional exploration.
- [ ] Maximum fan-out, concurrency, per-branch bounds, and total stopping conditions are finite.
- [ ] Join behavior is defined for invalid, missing, late, conflicting, and failed branch results.
- [ ] Shared state changes are validated and conflict handling does not depend on timing.
- [ ] Cancellation and partial outcomes are visible and do not imply that effects were reversed.
- [ ] Tests show that capacity exhaustion cannot silently discard required evidence or checks.

# 6.3 Parallel Work, State, and Failure Propagation

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers of agents that run independent operations concurrently.
**Applicability:** Use when one agent runs multiple tools or bounded sub-tasks at once. Serial agents do not need it. When sub-tasks are autonomous agents with their own identities or authority, also apply [Part 9](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md).

[Part 6](README.md) · [Applicability](../../applicability.md) · [6.1 Planning](01-planning-decomposition-and-bounded-control-loops.md) · [6.2 Reflection](02-reflection-critique-and-verification.md) · [7.1 Durable execution](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) · [9.2 Delegation](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)

## Purpose and applicability

Parallel work shortens a task when operations are truly independent, but can multiply calls, exhaust capacity, produce contradictory results and obscure failures. One agent calling several read-only tools in parallel is still one agent: its coordinator owns the plan, shared limits, merge and final outcome.

A tool or sub-task result is data, not authorization, and not proof that an external effect happened (see [tools](../../development-guide/02-agent-basics/04-tools-and-external-interfaces.md) and [untrusted inputs](../../development-guide/03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)). If a task must survive process loss or a branch may cause an effect, also apply [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) and [7.2](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md). Parallelism alone does not need a durable engine.

## Working model

A coordinator splits a request into bounded branches, records each result or failure, and joins them under a declared rule. Each branch has a stable run-scoped ID, an input, a purpose, a completion condition and finite limits. The join decides which outcomes are necessary, how evidence combines and what the result means.

Branches do not write to a shared conversation or result object as they finish. The coordinator accepts and merges their separate outputs through a defined state transition. Persistent work keeps state versioned, serializable and validated before acceptance (7.1); short-lived work can do the same in memory if failure and cancellation still give an honest, bounded result.

Parallelism is scheduling, not trust. Delegating to an autonomous agent crosses a boundary between principals whose authority, identity, data access and result contract need control; see [9.1](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md) and [9.2](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md).

## Decisions and best practices

### Choose a join rule before launching work

Use all-required when every branch supplies necessary evidence; optional branches only where the rest can still give a valid result; quorum or "first acceptable result" only when the task defines what counts, which evidence qualifies and how disagreement is handled. A fast branch is not a better one: unless arrival order matters, merge in a stable logical order.

A required branch that times out, is denied or returns invalid output blocks the result or triggers a declared escalation. A failed optional branch can be left out, but the outcome must not imply its evidence was obtained. Keep material disagreement and provenance; do not average away a conflict or treat missing work as agreement.

### Keep state changes isolated

Branches produce candidate results, not overwrites. Collect proposed changes to one logical record and apply them in one serialized, validated step. On conflict, use an explicit rule (reject, prefer a named authoritative source, ask, or return a bounded partial result), never last-write-wins or completion timing.

### Cancel deliberately and propagate failures honestly

Cancellation is a request, not proof that in-flight work stopped. Define what is cancelled when the caller cancels, the deadline passes, required evidence is unavailable or enough evidence has arrived. Accept a late result only if the run is still open and it validates; otherwise mark it late and exclude it. Completed reads need no undoing; branches with effects follow [7.2](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md), and cancelling does not erase a completed action.

Distinguish complete, declared partial or degraded, needs-information and failed results. A partial result names what is missing and what not to infer. Do not report an interrupted required branch as success because others finished.

### Bound fan-out and capacity

Before running, cap active and total branches, depth or rounds, per-branch time and output, and the overall deadline and budget. Reserve capacity for required validation and finalization rather than optional exploration. When limits block the planned fan-out, queue within a stated wait, use a tested reduced mode, ask the user to narrow the request, or stop safely; never quietly drop a required branch. Unknown cost is unknown, not free. Shared admission and backpressure are in [Part 8](../08-model-context-and-resource-engineering/README.md).

Separate calls are not automatically independent. Check whether they share a rate limit or mutable state, repeat a consequential action, or depend on each other's results, and serialize, deduplicate or disallow those unless a safe coordination rule exists. If the next step depends on results, start only the independent work, join, then decide.

## Requirements

- **PARALLEL-01** For an agent that schedules concurrent branches, the coordinator MUST establish finite per-run fan-out and active-concurrency limits, branch completion criteria, and an overall deadline or stopping condition before dispatch; additional depth, rounds, and resource limits MUST be bounded wherever branches can create further work.
- **PARALLEL-02** For every multi-branch join, the coordinator MUST declare which branches are required, optional, or substitutable and MUST define how valid evidence, failures, missing results, conflicts, and late results affect the terminal outcome; aggregation MUST preserve material provenance and disagreement.
- **PARALLEL-03** When concurrent branches can propose changes to shared state, the agent MUST keep proposals isolated until a validated coordinator transition accepts them and MUST apply a declared conflict rule rather than relying on arrival order or uncontrolled overwrites.
- **PARALLEL-04** When cancellation, timeout, or early completion can occur, the agent MUST specify which branches are cancelled, how late results are handled, and how terminal outcomes distinguish complete, partial/degraded, information-needed, and failed work; cancellation MUST NOT be represented as proof that an in-flight or completed effect was undone.
- **PARALLEL-05** When branches use shared capacity or can repeat an operation, the agent MUST apply a shared admission/budget bound and MUST serialize, deduplicate, or otherwise constrain concurrent operations whose effects or state are not safe to repeat or race.

## Worked example: answering a policy question

A user asks the fictional read-only policy assistant, "Does the current travel policy permit a London hotel costing GBP 220?" It runs three bounded read branches: retrieve the current policy passage; check its approved-source and effective-version metadata; and search the authorized archive for a superseded, possibly conflicting passage. No branch can change policy or book a hotel.

The first two branches are required: the answer needs an authorized passage confirmed current. The archive search is advisory; it can surface a conflict, but finding nothing does not prove no older copy exists, and a stale copy does not govern once the current source is verified. A failed or timed-out version check gives `needs_information`, not a guess. If only the archive search times out, the assistant answers from the verified source without claiming it searched every record.

In the test, the current document permits GBP 220 and the superseded copy differs. The coordinator stores the results separately, accepts only verified current evidence, and answers that GBP 220 is permitted, citing the current document; it may note the older copy differs. It does not blend amounts, pick the first return, or hide the conflict.

If the required branches succeed while the archive search runs, the coordinator may cancel it; a later return is marked late and excluded (a new task can follow it up). If a required branch was cancelled or failed, the result is information-needed or failure. With no write capability, no approval or compensation is needed.

## Evidence and checklist

Test changed completion order, a required timeout, an optional failure, conflicting results, cancellation with a late response and fan-out exhaustion, checking the accepted terminal state, not just that calls returned. Add shared-state conflict or duplicate-operation tests where branches touch mutable state or effects, and Part 7 replay and reconciliation evidence for durable branches.

- [ ] Required work is separate from optional exploration.
- [ ] Partial outcomes are visible and do not imply effects were reversed.
- [ ] Capacity exhaustion cannot silently discard required evidence or checks.

# 7.1 Execution Classes, Persistence, and Recovery

**Status:** 0.5.0-draft.2 — draft
**Audience:** Agent designers, implementers, and reviewers
**Applicability:** Use when an agent has long-running work, must recover progress after a process failure, or can cause external effects. Every agent declares an execution class; not every agent needs durable machinery. See the [Part 7 overview](README.md), [applicability guidance](../../applicability.md), [7.2](02-side-effects-idempotency-and-unknown-outcomes.md) and [7.3](03-approval-suspension-and-in-flight-compatibility.md).

## Purpose and applicability

A process can stop after useful work but before returning a result; a restart then loses progress, repeats work or leaves people unsure what happened. Durable execution records progress so eligible work can resume. It does not make every operation retry-safe, guarantee exactly-once external action, or prove the result correct.

Choose the class from effective capabilities and expected work, not a configuration label:

- **Ephemeral** work stays within one request with no externally visible side effects; durability may be unnecessary.
- **Durable** work is long-running or has side effects and needs persistence and recovery.
- **Human-governed** work needs approval for consequential actions.

These are execution classes, not governance tiers. A consequential operation may need both durability and approval, and high-risk read-only work is not automatically ephemeral.

Without a durable engine, specify the bounded behavior: what ends the run, what is returned if it stops, and whether resubmission is safe. Class declaration is in [2.2](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md); tool authorization in [3.1](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

## Working model

A durable workflow is the persisted control flow for one unit of work: it coordinates steps, makes policy decisions, waits for events and tracks state. **Durable steps** isolate work whose result must be captured (a model request, tool call, query, timer or notification), so boundaries show what may run again and what is already recorded.

Engines recover differently: some replay workflow code against recorded history, others resume from checkpoints or advance a persisted state machine. Under replay, orchestration code must make the same decisions each time it runs; two engines' documented constraints show what this means in practice.[1], [2] The portable rule: keep orchestration predictable, put external I/O and non-repeatable computation behind a boundary that records its outcome, and never decide the next step from mutable configuration, local time or unrecorded randomness. A recorded result stores a value; it does not authorize an action or guarantee an effect.[1], [3]

Persisted data stays stored while work waits: keep only what recovery needs, protect it by sensitivity, keep credentials out, and reference large artifacts through an authorized mechanism rather than copying them into history.

## Decisions and best practices

**Pick the simplest class that fits.** A read-only assistant answering a bounded question can run ephemerally, ending `complete`, `needs_information`, `declined`, `failed` or a declared partial result, even though the [reference architecture](../../agent-playbook/02-reference-architecture.md) describes a durable engine. If an interrupted answer can be dropped and restarted, record that and its cost.

**Run durable work inside the workflow.** Long waits, resumable work and side effects need a durable workflow, and requests must actually execute inside it; configuring persistence is not enough. Keep orchestration free of direct network, database and file access and unrecorded nondeterminism. Give steps typed inputs and outputs, bounded attempts and duration, clear failure and cancellation behavior, and data-classification rules, plus an overall deadline so retries and queueing cannot outlast the business need.

**Define cancellation and terminal outcomes first.** Cancelling before an effect ends cleanly; during one can leave the outcome unresolved; after a committed one does not undo it. Where they apply, separate completed, rejected, cancelled-without-effect, cancelled-after-partial-effect, compensated, retry-exhausted and permanent-failure. Compensation is a separate action, not automatic on cancel.

**Hand off across context windows.** When the limit is the context window rather than infrastructure, persist a progress log, a clean saved state and a protected acceptance list for the next session.[4] See [6.1](../06-reasoning-and-execution-patterns/01-planning-decomposition-and-bounded-control-loops.md).

**Treat workflow changes as compatibility changes.** When persisted work can outlive a release, changing step identity or decision order can break recorded progress. Test representative in-flight histories and route or migrate that work on purpose (policy in 7.3; rollout in [5.2](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)).

## Requirements

- **DURABLE-01** For every agent, the owner MUST declare an effective execution class and the capabilities or work characteristics that require it. An effective class MUST NOT silently downgrade a class required by an enabled capability; the record MUST identify whether long-running work, external effects, or consequential actions require durable execution or human approval.
- **DURABLE-02** When durable execution is required, the agent MUST execute the work within the declared persisted workflow, and MUST place external I/O and any result that can change across recovery behind a recorded step or equivalent engine-supported boundary. Reviewable design evidence MUST identify the workflow boundary and the persisted outcome for each such operation.
- **DURABLE-03** When recovery may replay or resume orchestration, the workflow MUST use deterministic decisions or recorded inputs/results for decisions that could otherwise change across recovery. Tests MUST exercise recovery from at least one interrupted point and verify that the workflow reaches the declared terminal or waiting state without treating an unrecorded result as completed.
- **DURABLE-04** When a workflow can be cancelled, fail, or terminate after partial progress, its contract MUST define the externally visible terminal states and cancellation behavior before, during, and after relevant steps. Tests MUST cover each applicable boundary and distinguish cancellation from compensation.
- **DURABLE-05** Before release of an agent that requires durable execution, the owner MUST retain evidence from recovery, retry-exhaustion, and termination tests against representative workflows. Where a step can affect external state, evidence MUST use an authoritative target-state or operation record as applicable, not only a transcript; retry safety and unresolved outcomes are specified further in [7.2](02-side-effects-idempotency-and-unknown-outcomes.md).

## Worked example

The fictional read-only policy assistant's failed request ends `failed` or is resubmitted under normal policy. Durability would add stored state with no recovery need, so it stays ephemeral and the team tests the bounded failure outcomes.

Extended, the assistant prepares a proposed travel-policy update that an authorized person must approve exactly before it is applied. Because it may wait, the team chooses a durable, human-governed workflow:

```yaml
workflow:
  request_id: policy-update-184
  state: awaiting_approval
  proposal_ref: proposal-184
  policy_version: travel-policy-v12
  next_step: apply_after_valid_approval
```

A recorded step creates the proposal; the workflow saves the reference and waits without keeping a process asleep in memory. When an authenticated approval arrives, the system checks it still applies to the exact proposal and current policy before scheduling the apply step (binding and races in 7.3). Execution-time authorization still applies.

If the policy service accepts the update but the worker stops before recording the result, the apply attempt is uncertain on recovery; a missing receipt does not prove nothing happened. The workflow checks the authoritative operation record by stable operation identity (7.2) and, if it still cannot tell and repeating is unsafe, records an unresolved state for review rather than resubmit or claim success.

## Evidence and checklist

Trace the workflow from request to terminal state: boundaries are visible, each durable result has a defined meaning, limits cover one attempt and the whole job, and operators can tell a completed action from an unresolved one.

Test interruption after a recorded step, during a wait and around the most consequential step; retry exhaustion; permanent failure; cancellation before and after effects; and active histories across code changes. Assert on recovered state, final status, authoritative external state and permitted effects, not an exact transcript. Method is in Part 4; release controls in Part 5.

- [ ] Uncertain outcomes are not treated as success or retried automatically.
- [ ] Persisted data is minimized and protected.

## References

[1]: https://docs.temporal.io/workflow-definition "Temporal Workflow Definition"
[2]: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-code-constraints "Azure Durable Functions orchestrator code constraints"
[3]: https://docs.temporal.io/develop/go/workflows/side-effects "Temporal Go SDK side effects"
[4]: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents "Effective harnesses for long-running agents"

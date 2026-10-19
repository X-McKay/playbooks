# 7.1 Execution Classes, Persistence, and Recovery

**Status:** 0.5.0-draft.2 — draft
**Audience:** Agent designers, implementers, and reviewers
**Applicability:** Use this chapter when an agent has long-running work, must recover progress after a process failure, or can cause external effects. Every agent declares an execution class; not every agent needs durable machinery. See the [Part 7 overview](README.md), [applicability guidance](../../applicability.md), [7.2 Side Effects, Idempotency, and Unknown Outcomes](02-side-effects-idempotency-and-unknown-outcomes.md), and [7.3 Approval, Suspension, and In-Flight Compatibility](03-approval-suspension-and-in-flight-compatibility.md).

## Purpose and applicability

A process can stop after doing useful work but before returning a result. Without deliberate persistence, a restart can lose progress, repeat work or leave people unsure what happened. Durable execution records workflow progress so eligible work can resume after a failure. It does not make every operation safe to retry, guarantee that an external action happened exactly once, or prove the result is correct.

Choose the execution class from the agent's effective capabilities and expected work, not from a configuration label.

- **Ephemeral** work stays within one request and has no externally visible side effects. Durability may be unnecessary.
- **Durable** work needs persistence and recovery when it is long-running or has side effects.
- **Human-governed** work needs approval for consequential actions.

These are execution classes, not governance tiers. A consequential operation may need both durable execution and human approval. Read-only work is not automatically ephemeral if it is high risk.

If the design has no durable engine, specify the bounded behavior instead: what ends the run, what is returned if it stops, and whether a caller can safely submit the request again. For class declaration and capability bounds, see [2.2 Agent Contracts and Configuration](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). For tool authorization, see [3.1 Identity, Authority, Zero Trust, and Least Privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

## Working model

A durable workflow is the persisted control flow for one unit of work. It records enough progress to recover. **Durable steps** isolate work whose result must be captured, such as a model request, a tool call, a database query, a timer or an external notification. The workflow coordinates steps, makes policy decisions, waits for events and tracks state. Make step boundaries clear enough that a reviewer can tell what may run again and what result is already recorded.

Recovery works differently across engines. Some replay workflow code against recorded history. Others resume from checkpoints or advance a persisted state machine. Where replay is used, the orchestration path must make the same decisions when run again. Two workflow engines document their deterministic-orchestration and replay constraints. They are examples, and engines differ.[1], [2]

The portable rule is to keep orchestration predictable and put external I/O and non-repeatable computation behind a boundary that records its outcome. During replay, do not decide the next step from mutable configuration, local time or unrecorded randomness. Recording a result for later replay stores the value. It does not authorize an action or guarantee an external effect.[1], [3]

Persistence also has a lifecycle cost. Inputs, outputs and event histories stay stored while work is paused or waiting. Keep persisted data to what recovery needs, protect it by sensitivity, and keep credentials out of workflow state. Reference large artifacts through an authorized mechanism instead of copying them into history. Approval events and schema compatibility for active work are in [7.3](03-approval-suspension-and-in-flight-compatibility.md).

## Decisions and best practices

**Pick the simplest class that fits the work.** A read-only policy assistant that answers a bounded question from approved, current, permission-filtered documents can run ephemerally. It returns citations and uncertainty and ends with `complete`, `needs_information`, `declined`, `failed` or a declared bounded partial result. It does not need a durable engine just because the reference architecture describes one. If an interrupted answer can be safely dropped and restarted, record that behavior and its cost.

For long waits, work that must resume, or side effects, use a durable workflow and make sure requests really run inside it. Configuring persistence is not enough if the request still executes outside the workflow. Keep orchestration free of direct network, database and file access and of unrecorded nondeterminism. Give steps typed inputs and outputs, bounded attempts and duration, clear failure and cancellation behavior, and data-classification rules. Set an overall deadline as well as per-step bounds, or retries and queueing can outlast the business need.

Define cancellation and terminal outcomes before you build. Cancelling before an effect can end cleanly. Cancelling during an effect can leave the outcome unresolved. Cancelling after a committed effect does not undo it. Where they apply, separate these states: completed, rejected, cancelled-without-effect, cancelled-after-partial-effect, compensated, retry-exhausted and permanent-failure. Compensation is a separate action, not something cancellation does automatically.

When the limit is the context window and not the infrastructure, persist a handoff for the next session: a progress log, a saved clean state, and a protected acceptance list. The pattern is described in a vendor engineering guide.[4] See [6.1](../06-reasoning-and-execution-patterns/01-planning-decomposition-and-bounded-control-loops.md).

Treat workflow changes as a compatibility problem whenever persisted work can outlive a release. A change to step identity or decision order can break recorded progress. Test representative in-flight histories against the change, and route or migrate that work on purpose. Compatibility policy is in 7.3. For rollout and rollback, see [5.2 Readiness, Change, and Rollout](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## Requirements

- **DURABLE-01** For every agent, the owner MUST declare an effective execution class and the capabilities or work characteristics that require it. An effective class MUST NOT silently downgrade a class required by an enabled capability; the record MUST identify whether long-running work, external effects, or consequential actions require durable execution or human approval.
- **DURABLE-02** When durable execution is required, the agent MUST execute the work within the declared persisted workflow, and MUST place external I/O and any result that can change across recovery behind a recorded step or equivalent engine-supported boundary. Reviewable design evidence MUST identify the workflow boundary and the persisted outcome for each such operation.
- **DURABLE-03** When recovery may replay or resume orchestration, the workflow MUST use deterministic decisions or recorded inputs/results for decisions that could otherwise change across recovery. Tests MUST exercise recovery from at least one interrupted point and verify that the workflow reaches the declared terminal or waiting state without treating an unrecorded result as completed.
- **DURABLE-04** When a workflow can be cancelled, fail, or terminate after partial progress, its contract MUST define the externally visible terminal states and cancellation behavior before, during, and after relevant steps. Tests MUST cover each applicable boundary and distinguish cancellation from compensation.
- **DURABLE-05** Before release of an agent that requires durable execution, the owner MUST retain evidence from recovery, retry-exhaustion, and termination tests against representative workflows. Where a step can affect external state, evidence MUST use an authoritative target-state or operation record as applicable, not only a transcript; retry safety and unresolved outcomes are specified further in [7.2](02-side-effects-idempotency-and-unknown-outcomes.md).

## Worked example

The fictional policy assistant starts with no external write capability. It answers from current, permission-filtered policy documents and gives a citation or states uncertainty. A failed request can end as `failed` or be resubmitted under the normal request policy. Making this read-only request durable would add stored state without meeting any recovery need, so the team keeps it ephemeral and tests the bounded failure outcomes.

Now extend it: the assistant prepares a proposed update to the travel policy, and an authorized person must approve the exact change before it is applied. The work may wait for a decision, so the team chooses a durable, human-governed workflow. Its persisted progress looks like this:

```yaml
workflow:
  request_id: policy-update-184
  state: awaiting_approval
  proposal_ref: proposal-184
  policy_version: travel-policy-v12
  next_step: apply_after_valid_approval
```

The assistant creates the proposal in a recorded step. The workflow saves the proposal reference and waits. It does not keep a process asleep in memory. When an authenticated approval arrives, the system checks that the decision still applies to the exact proposal and current policy context before it schedules the apply step. Binding and event-race details are in 7.3. The approval does not widen authority: execution-time authorization still applies.

Suppose the policy service accepts the update, but the worker stops before the workflow records the step result. On recovery, the workflow restores its recorded progress and sees that the apply attempt has an uncertain outcome. A missing receipt does not prove the service did nothing, so the workflow must not submit the update again blindly. It checks an authoritative operation record or state, using the stable operation identity and reconciliation policy in 7.2. If it cannot tell what happened and repeating is unsafe, it records an unresolved state and routes the case for review. It does not claim success. Durable execution guarantees preserved progress and a controlled recovery path, not correctness or exactly-once external action.

## Evidence and checklist

Review the workflow from first request to terminal state. Confirm that every external or non-repeatable boundary is visible, each durable result has a defined meaning, and limits cover both one attempt and the whole job. Confirm that cancellation does not imply rollback and that an operator can tell a completed action from an unresolved outcome.

Test interruption after a recorded step, during a wait, and around the most consequential step. Check the recovered state, final status and any authoritative external state. Test retry exhaustion, permanent failure, cancellation before and after effects, and representative active histories when code changes. Assert on state and permitted effects, not on an exact model transcript. For evaluation method, see Part 4. For release readiness and operating controls, see Part 5.

- [ ] The effective class matches enabled capabilities and expected work duration.
- [ ] Durable configuration is attached to an actual persisted workflow when required.
- [ ] Orchestration decisions are deterministic or use recorded results.
- [ ] Step boundaries, deadlines, cancellation behavior and terminal states are documented.
- [ ] Recovery tests cover interruption, waiting, failure and any partial progress.
- [ ] External effects are verified through authoritative state where applicable. Uncertain outcomes are not treated as success or retried automatically.
- [ ] Persisted data is minimized and protected, and compatibility is assessed for active work.

## References

[1]: https://docs.temporal.io/workflow-definition "Temporal Workflow Definition"
[2]: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-code-constraints "Azure Durable Functions orchestrator code constraints"
[3]: https://docs.temporal.io/develop/go/workflows/side-effects "Temporal Go SDK side effects"
[4]: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents "Effective harnesses for long-running agents"

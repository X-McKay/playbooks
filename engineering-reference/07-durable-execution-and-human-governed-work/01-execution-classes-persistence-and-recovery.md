# 7.1 Execution Classes, Persistence, and Recovery

**Status:** 0.5.0 first draft
**Audience:** Agent designers, implementers, and reviewers
**Applicability:** Select this chapter when an agent has long-running work, must recover progress across process failure, or can cause external effects. The execution-class decision applies to every agent; durable machinery does not. See the [Part 7 overview](README.md), [applicability guidance](../../applicability.md), [7.2 Side Effects, Idempotency, and Unknown Outcomes](02-side-effects-idempotency-and-unknown-outcomes.md), and [7.3 Approval, Suspension, and In-Flight Compatibility](03-approval-suspension-and-in-flight-compatibility.md).

## Purpose and applicability

A process can stop after doing useful work but before returning a result. Without deliberate persistence, a restart may lose progress, repeat work, or leave people unsure what happened. Durable execution records workflow progress so eligible work can resume after a failure. It does not make every operation safe to retry, guarantee that an external action happened exactly once, or prove that the result is correct.

Choose the execution class from the agent’s effective capabilities and expected work, not from a configuration label alone. **Ephemeral** work is bounded to a request and has no externally visible side effects; durability may be unnecessary. **Durable** work needs persistence and recovery when it is long-running or side-effecting. **Human-governed** work requires approval for consequential actions. These are execution classes, not governance tiers or residual-risk ratings. A consequential operation may need both durable execution and human approval. Higher-risk work is not automatically ephemeral just because it is read-only.

If the proposed design has no durable engine, specify the bounded behavior instead: what ends the run, what is returned if it stops, and whether a caller may safely submit the request again. For more on class declaration and capability bounds, see [2.2 Agent Contracts and Configuration](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). Tool authorization remains governed by [3.1 Identity, Authority, Zero Trust, and Least Privilege](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md).

## Working model

A durable workflow is the persisted control flow for one unit of work. It records enough progress to recover the workflow, while **durable steps** isolate work whose result must be captured: for example, a model request, a tool call, a database query, a timer, or an external notification. The workflow coordinates steps, makes policy decisions, waits for events, and tracks the current state. Step boundaries should be explicit enough that a reviewer can tell what may be re-executed and what result is already recorded.

Recovery mechanisms differ. Some engines replay workflow code against recorded history; others resume from checkpoints or advance a persisted state machine. In replay-oriented systems, the orchestration path must make compatible decisions when run again. Temporal and Azure Durable Functions document deterministic orchestration and replay constraints in their respective systems; these are useful examples, not a requirement to choose either product or to assume every engine behaves identically. [1] [2]

The portable design rule is to keep orchestration predictable and place external I/O or non-repeatable computation behind a boundary that captures its outcome. Avoid consulting mutable configuration, local time, or unrecorded randomness to decide the next step during replay. If a result is intentionally recorded for later replay, that records the value; it does not authorize an action or guarantee an external effect. [1] [3]

Persistence also creates a lifecycle obligation. Inputs, outputs, and event histories may remain stored while work is paused or awaiting an event. Keep persisted data limited to what recovery requires, protect it according to its sensitivity, and avoid placing credentials in workflow state. Large artifacts should be referenced through an authorized mechanism rather than copied into history. Approval-event semantics and schema compatibility for active work are covered in [7.3](03-approval-suspension-and-in-flight-compatibility.md).

## Decisions and best practices

**Select the least complex class that satisfies the actual work.** A read-only policy assistant that answers a bounded question from approved, current, permission-filtered documents can run ephemerally: it returns citations and uncertainty, and ends with `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. It does not need a durable engine merely because the reference architecture describes one. If an interrupted answer can be safely abandoned and restarted, record that behavior and its cost.

For long waits, work that must resume, or side-effecting activity, use a durable workflow and make its operational boundary real: configuring persistence is not enough if the request still executes outside that workflow. Keep the orchestration layer free of direct network, database, or filesystem access and unrecorded nondeterminism. Give steps typed inputs and outputs, bounded attempts and duration, clear failure and cancellation behavior, and data-classification rules. Set an overall deadline as well as per-step bounds; otherwise retries and queueing can outlive the business need.

Define cancellation and terminal outcomes before implementation. Cancellation before an effect may end cleanly; cancellation during an effect may leave the outcome unresolved; cancellation after a committed effect does not undo it. Distinguish completed, rejected, cancelled-without-effect, cancelled-after-partial-effect, compensated, retry-exhausted, and permanent-failure states where those distinctions apply. Compensation is a separate action, not an automatic property of cancellation.

Treat workflow evolution as a compatibility problem whenever persisted work can outlive a release. A change that alters step identity or decision order may be incompatible with recorded progress. Test representative in-flight histories against the proposed change, and route or migrate work deliberately. Detailed compatibility policy belongs to 7.3; operational rollout and rollback connect to [5.2 Readiness, Change, and Rollout](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## Requirements

- **DURABLE-01** For every agent, the owner MUST declare an effective execution class and the capabilities or work characteristics that require it. An effective class MUST NOT silently downgrade a class required by an enabled capability; the record MUST identify whether long-running work, external effects, or consequential actions require durable execution or human approval.
- **DURABLE-02** When durable execution is required, the agent MUST execute the work within the declared persisted workflow, and MUST place external I/O and any result that can change across recovery behind a recorded step or equivalent engine-supported boundary. Reviewable design evidence MUST identify the workflow boundary and the persisted outcome for each such operation.
- **DURABLE-03** When recovery may replay or resume orchestration, the workflow MUST use deterministic decisions or recorded inputs/results for decisions that could otherwise change across recovery. Tests MUST exercise recovery from at least one interrupted point and verify that the workflow reaches the declared terminal or waiting state without treating an unrecorded result as completed.
- **DURABLE-04** When a workflow can be cancelled, fail, or terminate after partial progress, its contract MUST define the externally visible terminal states and cancellation behavior before, during, and after relevant steps. Tests MUST cover each applicable boundary and distinguish cancellation from compensation.
- **DURABLE-05** Before release of an agent that requires durable execution, the owner MUST retain evidence from recovery, retry-exhaustion, and termination tests against representative workflows. Where a step can affect external state, evidence MUST use an authoritative target-state or operation record as applicable, not only a transcript; retry safety and unresolved outcomes are specified further in [7.2](02-side-effects-idempotency-and-unknown-outcomes.md).

## Worked example

The fictional policy assistant initially has no external write capability. It answers a question using current, permission-filtered policy documents and gives a citation or states uncertainty. A failed request can end as `failed` or be resubmitted under the ordinary request policy. Making this read-only request durable would add persisted state without meeting a stated recovery need, so the team keeps it ephemeral and tests the bounded failure outcomes.

Now extend the example: the assistant prepares a proposed update to the travel policy, and an authorized person must approve the exact change before it is applied. The work may wait for a decision, so the team chooses a durable, human-governed workflow. Its persisted progress is conceptually:

```yaml
workflow:
  request_id: policy-update-184
  state: awaiting_approval
  proposal_ref: proposal-184
  policy_version: travel-policy-v12
  next_step: apply_after_valid_approval
```

The assistant creates the proposal in a recorded step. The workflow saves the proposal reference and waits; it does not keep a process asleep in memory. When an authenticated approval event arrives, the system verifies that the decision still applies to the exact proposal and current policy context before scheduling the apply step. Binding and event-race details are in 7.3. The approval does not create broader authority: execution-time authorization still applies.

Suppose the policy service accepts the update, but the worker stops before the workflow records the step result. On recovery, the workflow can restore its recorded progress and determine that the apply attempt has an uncertain outcome. A missing receipt is not proof that the service did nothing. It must not blindly submit the update again. The system checks an authoritative operation record or state, using the stable operation identity and reconciliation policy described in 7.2. If it cannot determine what happened and repetition is unsafe, it records an unresolved state and routes the case for review rather than claiming success. The durable guarantee is preserved progress and a controlled recovery path—not correctness or exactly-once external action.

## Evidence and checklist

Before relying on persistence, review the workflow from initial request to terminal state. Confirm that every external or non-repeatable boundary is visible, each durable result has a defined meaning, and limits cover both an individual attempt and the overall work. Confirm that cancellation does not imply rollback and that an operator can distinguish a completed action from an unresolved outcome.

Test interruption after a recorded step, during a wait, and around the most consequential step. Verify the recovered state, final status, and any authoritative external state. Test retry exhaustion, permanent failure, cancellation before and after effects, and representative active histories when code changes. Assertions should concern state and permitted effects, not an exact model-generated transcript. Part 4 owns the evaluation method; Part 5 owns release readiness and operating controls.

- [ ] The effective class matches enabled capabilities and expected work duration.
- [ ] Durable configuration is attached to an actual persisted workflow when required.
- [ ] Orchestration decisions are deterministic or use recorded results.
- [ ] Step boundaries, deadlines, cancellation behavior, and terminal states are documented.
- [ ] Recovery tests cover interruption, waiting, failure, and applicable partial progress.
- [ ] External effects are verified through authoritative state where applicable; uncertain outcomes are not treated as success or automatically retried.
- [ ] Persisted data is minimized and protected; compatibility is assessed for active work.

## References

[1]: https://docs.temporal.io/workflow-definition "Temporal Workflow Definition"
[2]: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-code-constraints "Azure Durable Functions orchestrator code constraints"
[3]: https://docs.temporal.io/develop/go/workflows/side-effects "Temporal Go SDK side effects"

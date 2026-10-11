# 9. Durable execution and human approval

This chapter is for developers building agents that change external state or
outlive a single request. It shows how to split work into workflows and
durable steps, and how to make retries, approvals, and deploys safe.

A durable execution engine records the progress of a workflow so that it can
resume after process, worker, or infrastructure failure without repeating
completed work. Durability applies only when the agent run executes inside a
workflow managed by that engine. Configuring durability without starting a
workflow produces an ordinary, non-durable run.

## Concepts

| Term | Meaning |
| --- | --- |
| Workflow | Deterministic orchestration whose progress is recorded so it can be recovered after failure |
| Durable step | A unit of nondeterministic work or I/O whose result is recorded once it completes |
| External event | An authenticated message delivered to a running workflow, such as an approval decision |
| Worker | A process that executes workflows and durable steps from a worker queue |
| Worker queue | A named queue that routes work to compatible workers |
| Replay | Recovering workflow state after failure from what the engine recorded, as described below |
| New run | Continuing a long-lived workflow as a new run with fresh history while keeping its chain identity |

Engines recover in different ways. Many re-execute workflow code against the
recorded results of completed steps; others resume from a saved checkpoint or
advance a declarative state machine. This chapter uses *replay* for whichever
mechanism your engine provides. Where the engine re-executes workflow code,
the determinism rules below apply directly. Where it resumes from
checkpoints, changed code must still be able to continue persisted state, and
replay tests become checkpoint-compatibility tests.

## Workflow boundary

The engine may run workflow code again during recovery, so it must make the
same decisions every time. Anything that touches the outside world, or could
answer differently on a second run, belongs in a recorded step.

A workflow MAY coordinate agent runs, maintain process state, wait for
approval, apply deterministic branching, enforce deadlines, and initiate
compensation.

A workflow MUST NOT make network, database, or filesystem calls; read mutable
environment configuration during replay; use nondeterministic time or
randomness; or contain infrastructure clients and credentials.

Model requests, tool calls, MCP communication, databases, external APIs,
object storage, and notifications execute in durable steps.

## Stable identities

The engine finds recorded work by name. These identifiers MUST be explicit
and stable:

- Agent name
- Toolset ID
- Workflow and durable-step types
- Worker queue
- External event names
- Durable model registry keys

If an integration derives durable-step names from agent names or toolset IDs,
renaming either can break replay of active workflows.

A workflow ID SHOULD be unique and traceable:

```text
<environment>:<tenant>:<workflow-type>:<business-id>:<request-id>
```

Independent workflow chains MUST NOT reuse an ID. Continuing as a new run
remains part of the same chain.

## Durable-step contract

Every durable step MUST define:

- Typed input and output
- A bound on a single attempt and a bound on all attempts, including queueing
- Retry policy and non-retryable errors
- Idempotency behavior
- Cancellation behavior
- Data-classification constraints
- Telemetry attributes

Long-running durable steps SHOULD report liveness (heartbeat) and react to
cancellation.

## Retry ownership

Retries exist at four layers:

1. Agent-framework output-correction retries
2. Provider-client transport retries
3. Durable-step retries
4. Workflow-level business retries

Left alone, nested retries multiply. The default policy is:

- The agent framework owns output correction.
- The durable execution engine owns transient infrastructure retries.
- Provider transport retries are disabled or minimized under durable
  execution.
- Workflows own explicit business retry decisions.

All layers MUST have a calculated combined upper bound. Authentication
errors, authorization failure, policy violations, invalid business requests,
and oversized payloads are non-retryable.

## Idempotency

A step can complete its effect and fail before its result is recorded.
Side-effecting durable steps MUST use a
stable idempotency key, such as:

```text
<workflow-id>:<tool-call-id>:<operation-version>
```

The same key MUST be reused across retries. When an external system lacks
idempotency support, the application SHOULD persist an operation record and
check it before repeating the action.

## Timeouts

Timeouts SHOULD nest so each layer can handle the failure inside it:

```text
provider request timeout
    < durable-step single-attempt timeout
        < durable-step total timeout (all attempts)
            < workflow deadline
                < caller or business deadline
```

Human waiting uses durable workflow timers, not sleeping durable steps.

## Human approval

A human-governed workflow:

1. Produces a typed action proposal.
2. Applies deterministic policy checks.
3. Records a canonical hash of the action and arguments.
4. Waits for an authenticated external event carrying the approval decision.
5. Verifies approver scope, expiry, tenant, actor, policy version, and action
   hash.
6. Executes the consequential durable step with an approval ID and
   idempotency key.
7. Records the result and approval evidence.

Approval is invalid if material arguments or security context change.

An approval record contains at least:

| Field | Description |
| --- | --- |
| `approval_id` | Unique approval identifier |
| `workflow_id` | Workflow awaiting the decision |
| `action_name` | Stable name of the consequential action |
| `action_arguments_hash` | Canonical hash of the approved arguments |
| `approver_id` | Authenticated approver identity |
| `decision` | `approved` or `rejected` |
| `policy_version` | Approval policy applied |
| `decided_at` | Decision timestamp |
| `expires_at` | Time after which the approval is no longer valid |
| `reason` | Optional approver rationale |

## Cancellation and compensation

Workflows MUST define cancellation before, during, and after side effects.
Cancellation does not automatically undo completed work. Reversible
operations SHOULD have explicit compensation steps.

Final status SHOULD distinguish:

```text
completed
rejected
cancelled_without_effect
cancelled_after_partial_effect
compensated
failed_retryable_exhausted
failed_permanent
```

## Payloads and history

Durable execution engines store workflow and durable-step inputs and outputs
in history and commonly enforce payload and history size limits. Encoding
overhead further reduces the usable raw size.

- Keep documents, images, large tool results, and model artifacts outside
  workflow history.
- Store large data in approved object storage and pass typed references.
- Keep dependencies and metadata serializable to a portable format such as
  JSON.
- Do not put secrets in inputs, dependencies, metadata, or results.
- Continue as a new run when history would otherwise grow without bound.

An artifact reference contains at least:

```yaml
artifact_reference:
  uri: <storage URI>
  media_type: application/pdf
  size_bytes: 482113
  sha256: <content digest>
  data_classification: confidential
  expires_at: <timestamp or null>
```

The resolver MUST authorize access; possession of a URI is not
authorization.

## Streaming

For durable user-facing streaming, prefer a streaming mechanism that the
durable execution engine records or coordinates where one is available.
Consumers MUST tolerate duplicate model events caused by durable-step retry
and deduplicate using workflow, durable-step, attempt, and event identity.
The durable workflow result remains authoritative.

## Deployment and replay

Before deploying a workflow change:

- Replay representative histories against the new build.
- Verify stable agent names and toolset IDs.
- Identify changes to workflow command ordering.
- Use the engine's mechanism for versioning workflow code, such as version
  markers in code or routing new runs to a new build, for incompatible
  changes.
- Keep a build that can continue older workflows available until they finish
  or migrate.
- Test workflows waiting on approvals, timers, and retries.

## Required tests

- Workflow tests with a controlled clock for timers and deadlines
- Durable-step unit tests
- Retry and permanent-failure tests
- Idempotency and duplicate-execution tests
- Cancellation and compensation tests
- Approval, rejection, expiry, and tampering tests
- Payload-limit tests
- Worker shutdown and resume tests
- Captured-history replay tests
- End-to-end tests against a local instance of the durable execution engine

## Common pitfalls

- **Enabling durability without a workflow.** The run looks durable in
  configuration and is not.
- **Assuming durable means exactly once.** The engine records results; only
  idempotency keys stop a repeated step from repeating its effect.
- **Renaming an agent or toolset casually.** Active workflows can no longer
  find their recorded steps.

## Before you move on

- [ ] All I/O and model calls run in durable steps; workflow code is
  deterministic.
- [ ] Retries have a calculated combined bound and timeouts nest correctly.
- [ ] Every side effect has an idempotency key, and approval is bound to an
  argument hash.
- [ ] Captured histories replay against each new build before deploy.

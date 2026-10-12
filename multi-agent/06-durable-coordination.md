# 6. Durable coordination

This guide is for developers who run a multi-agent system on a durable
execution engine. It assumes every member follows the single-agent
[durable execution](../advanced/01-durable-execution.md) chapter and
uses its terms; a *child workflow* is a workflow started and supervised by
another. Here you will find what changes when one workflow coordinates many
agents. The engine gives you durability, not authorization, safe delegation,
convergence, or bounded autonomy; you still build those.

## Keep one workflow in charge

Each system run has one authoritative workflow chain, so a crash or replay
reaches the same decisions. The workflow MAY maintain typed system and branch
state; materialize an allowed run graph; schedule member-agent durable steps
and child workflows; reserve and reconcile budgets; apply deterministic
routing, aggregation, and conflict policies; wait for external events, timers,
and human approval; propagate cancellation and initiate compensation; and
commit terminal outcomes.

The workflow MUST NOT call models, agents, tools, MCP servers, registries,
databases, queues, filesystems, clocks, random generators, or external
services directly. Obtain nondeterministic discovery and admission evidence
through durable steps, and let the workflow apply a deterministic policy to
their recorded results.

## Name everything stably

These identifiers MUST be explicit and stable:

```text
system name and version
composition and run manifest IDs
system run and workflow IDs
workflow and durable step types
member agent names, versions, and manifest IDs
role and interaction IDs
delegation, branch, task, event, and approval IDs
worker queues, external event types, and durable registry keys
```

Suggested workflow and delegation identities are:

```text
workflow:   <environment>:<tenant>:<system>:<business-id>:<request-id>
delegation: <workflow-id>:<interaction-id>:<logical-task-id>
branch:     <delegation-id>:<branch-index>
```

Retries of the same logical work reuse the delegation and branch identities.
Materially changed work receives a new identity linked to its predecessor.

## Record the run graph

A static system starts from its resolved composition manifest. A dynamic
system also produces a run manifest containing every admitted member, role
assignment, edge, policy decision, schema, capability ceiling, and budget
grant used in that run.

The graph changes only through a versioned workflow command or external
event:

1. An agent, operator, event, or policy proposes a member or edge.
2. A durable step obtains authenticated registry and compatibility evidence.
3. Deterministic workflow code evaluates the admission policy.
4. The workflow records the decision and updated graph version.
5. Only then may the new member or edge receive work.

The workflow MUST NOT depend on a registry returning the same answer during
replay. The recorded evidence and policy version make the decision
reproducible.

## Model state as a typed state machine

System state MUST be represented by versioned, serializable types. At
minimum, track:

- system status and graph version;
- active, completed, failed, and cancelled delegations;
- branch parentage and dependencies;
- accepted evidence and unresolved conflicts;
- budget reservations and measured consumption;
- approval and side-effect state;
- progress markers and termination counters; and
- compensation obligations.

Agent prose is not workflow state until it is parsed, validated, and accepted
through a deterministic transition. Illegal transitions fail closed and emit
policy telemetry.

## Schedule from the workflow

The workflow owns scheduling. It enforces maximum active members and branches;
per-role and per-member concurrency; tenant and deployment capacity limits;
dependency ordering and required barriers; fairness and priority policy;
deadline and queue-time limits; and backpressure behavior.

Best practices:

- **Reserve capacity and budget before scheduling fan-out branches.** If the
  full fan-out cannot be admitted, policy decides whether to queue, reduce the
  set, use a tested degraded mode, or escalate. The model does not silently
  choose a cheaper or smaller plan after a policy denial.
- **Order results logically, not by completion time.** Aggregation MUST NOT
  depend on nondeterministic iteration or arrival order unless arrival order
  is explicitly captured as an input to a versioned business policy.

## Run each interaction as durable work

Each member invocation executes as a durable step or inside an explicitly
managed child workflow, taking the validated
[delegation envelope](05-delegation-and-interactions.md) and returning the
validated result envelope.

An interaction durable step MUST meet the single-agent durable-step
contract (timeouts per attempt and overall, retry and non-retryable classes,
cancellation, idempotency, data classification, telemetry) and MUST also
define heartbeat behavior, duplicate detection, payload bounds, budget grant
and usage reporting, and trace and audit attributes.

An agent may request further delegation, but the request returns to the
workflow or another deterministic control boundary for validation and
scheduling. Nested in-process agent calls MUST NOT bypass graph, budget,
authority, telemetry, or durability controls.

## Give every retry one owner

Retries can exist at the model, provider, agent, interaction, durable step,
workflow, and business-process layers, and they multiply. Document one
owner for each failure class, and calculate the combined maximum executions,
duration, and cost.

Keep the single-agent default split, with provider transport retries
disabled or minimized beneath durable step retry, and add one rule: workflows
own interaction and business retry decisions.

Authorization failure, invalid admission, policy denial, incompatible schema,
invalid approval, exhausted hard budget, and invalid business input are
non-retryable. A member's `failed_retryable` status is a claim evaluated
against workflow policy, not permission to retry itself.

## Deduplicate at the delegation

The stable delegation ID is the idempotency root for one logical interaction.
Side-effecting operations additionally use the single-agent stable
tool-call and operation-version idempotency key.

The workflow deduplicates repeated delegation requests, retried durable step
results, duplicate queue or event delivery, repeated approval events, late
results from cancelled branches, and replayed side-effect completion
notifications.

Deduplication MUST preserve the original result and audit evidence. It MUST
NOT erase inconsistent duplicate payloads; a mismatch triggers an integrity
finding.

## Reserve and reconcile budgets

Root budgets are durable state. Before dispatch, the workflow atomically
reserves the child grant and the relevant concurrency slot. Nested work
reserves from its parent's remaining grant. (The accounting rules are in
[budget escrow](09-cost-and-capacity.md#budget-escrow).)

After completion or termination, the workflow validates reported usage
against provider and tool evidence where available, commits measured
consumption, releases unused reservation, records unknown cost separately
from zero cost, and applies warning, degradation, escalation, or termination
policy.

A workflow MUST tolerate worker loss between reservation, execution, usage
recording, and release without double-spending or leaking reservations.

## Stop when progress stops

Progress is a typed material change such as new verified evidence,
completion of a required task, resolution of a conflict, or an approved state
transition. Restating a plan, producing another critique, or
transferring ownership without new evidence does not count by default.

The workflow checks termination after every interaction and material event.
It terminates or escalates on terminal state, hard limit, deadline,
cancellation, kill switch, policy dead end, or a configured no-progress
window.

Persistent collectives MAY continue across business tasks, but each task has
a bounded workflow or workflow segment with its own identity, budget, outcome,
and audit record. Persistence is not permission for an unbounded model
conversation or history.

## Plan for partial failure

Classify every role and interaction as required, optional, substitutable, or
advisory, and let policy define the effect of its failure. Final state MUST
distinguish at least:

```text
completed
completed_degraded
needs_information
escalated
rejected
cancelled_without_effect
cancelled_after_partial_effect
compensated
partial_effect
failed_retryable_exhausted
failed_permanent
```

A degraded outcome identifies the missing members, evidence, checks, and
guarantees. The system MUST NOT relabel degraded completion as ordinary
success solely to meet availability objectives.

## Cancel and compensate across branches

Cancellation propagates from the root through active descendants using stable
branch identities. Define the behavior before any side effect, while agents
or tools are active, during approval waiting, after partial or completed side
effects, and while a dynamic member is unreachable.

As in the single-agent guidance, completed work is not automatically undone, and
reversible effects have explicit compensation steps; here they also have an
explicit order across branches. Consequential
effects retain approval and audit evidence even when later compensated.

## Use child workflows for real boundaries

Use a child workflow when a branch needs an independent durable lifecycle;
separate worker or organizational ownership; independent cancellation or
parent-close policy; history isolation or scaling; or reusable coordination
with its own state machine.

Do not create one child workflow per agent merely for code organization.
Parent and child exchange typed summaries and artifact references rather than
shared local state. Parent-close and cancellation behavior MUST be explicit.

## Human approval

Follow the single-agent
[approval flow](../advanced/01-durable-execution.md#human-approval),
and bind each approval to the final typed action and the system context that
produced it: system and manifest ID, workflow, actor, tenant, policy version,
arguments, relevant evidence references, and expiry.

Changing a material action field, effective authority, member composition,
tenant, or governing policy invalidates approval unless the approval policy
explicitly declares the change immaterial. An agent review, vote, consensus,
or coordinator recommendation cannot approve an action.

## Keep history small

As the single-agent guidance requires, keep large payloads out of workflow history;
in a system that includes transcripts, code, blackboard contents, and event
bodies. Pass typed, authorized, integrity-protected references.

For long-lived systems, continue as a new run or use bounded child
workflows. Before continuing, persist the current graph version, run
manifest, budgets, unresolved work, approvals, progress counters, and artifact
references in a versioned continuation payload.

## Deploy with replay evidence

Apply the single-agent deployment and replay practice to the system
workflow. In addition, before deployment:

- replay static and dynamic graph histories;
- test histories with active, failed, cancelled, and late branches;
- verify stable system, member, role, interaction, workflow, and durable step
  IDs;
- verify graph and policy decisions do not call mutable registries during
  replay; and
- test in-flight approvals, budget reservations, timers, and substitutions.

## Required tests

Run the single-agent required durable execution tests against the system
workflow, plus:

- static and dynamic graph materialization tests;
- admission and graph-version replay tests;
- concurrent fan-out and deterministic aggregation tests;
- combined retry-bound and duplicate-delivery tests;
- budget reservation, reconciliation, and worker-loss tests;
- required, optional, fallback, and quarantined-member tests;
- deadlock, livelock, no-progress, and termination tests;
- root and branch cancellation tests;
- partial-effect and compensation tests;
- approval, expiry, tampering, and composition-change tests; and
- payload, history, and continuation-as-a-new-run tests.

## Common pitfalls

- **Letting an agent orchestrate.** In-process agent calls skipped graph,
  budget, and authority checks.
- **Asking the registry again on replay.** The registry changed, so the
  admission decision and the replay diverged.
- **Retrying at every layer.** Small per-layer bounds multiplied into a cost
  and duplicate-effect incident.

## Before you move on

- [ ] One deterministic workflow owns graph, state, scheduling, budgets, and
  termination.
- [ ] Delegations and branches have stable identities that retries reuse.
- [ ] Each failure class has one retry owner and a combined bound.
- [ ] Static and dynamic graph histories replay against the new build.

# 8. Observability

This guide is for developers who will operate a multi-agent system and need
to explain what it did. Each member still emits the telemetry the Agent
Playbook's [observability](../core/11-observability.md) chapter
requires. On top of that, observe the composition as one governed system and
each interaction as an attributable boundary, and correlate member telemetry
with system, workflow, graph, delegation, budget, approval, and outcome data.

## What you need to be able to answer

Design telemetry backwards from the questions an operator will ask:

- Which system, manifest, graph, members, models, and policies handled a task?
- Why was each member and edge selected or denied?
- Which agent had control, responsibility, data, and authority at each point?
- How did state, evidence, conflicts, and ownership change?
- Where did active time, queue time, retries, tokens, tools, and spend
  accumulate?
- Did limits, admission, authorization, approval, and termination hold?
- How did failures, cancellation, and compensation propagate?
- Can a dynamic run be reconstructed after registry state changes?
- Which version, scenario, or control caused a degraded or unsafe outcome?

## Telemetry types

Production systems MUST provide the single-agent telemetry types
(traces, metrics, structured logs, audit records, and evaluation results) for
the system as a whole: traces span workflows, interactions, agent runs,
models, and tools; metrics cover coordination and capacity as well as health,
quality, and cost; logs hold restricted diagnostics; tamper-resistant audit
records cover admission, approval, policy, and effects; and evaluation results
cover system behavior. They MUST also keep an interaction ledger for the
material delegation and state-transition record.

Traces are diagnostic evidence. They do not replace the authoritative
workflow state, interaction ledger, or audit record.

## Shape traces around causality

The root system span represents one business task or bounded workflow
segment. It contains workflow, policy, interaction, agent-run, model, and tool
spans.

Use parent-child spans for synchronous work with one clear owner. Use span
links for fan-out, queues, events, batches, blackboard reactions, handoffs
across independent lifecycles, and work with multiple causal parents.
Propagate a safe creation context with every message so producers and
consumers remain correlatable.

Trace shape MUST NOT be the only representation of system semantics. Record
explicit delegation IDs, parent IDs, graph versions, interaction modes, and
ownership transitions.

## Required correlation

In addition to the single-agent
[correlation](../core/11-observability.md#correlation) fields, spans
and material records include:

```text
system.name
system.version
system.contract_version
system.manifest_id
system.run_id
system.execution_class
system.governance_tier
system.topology
system.graph_version
system.workflow_id
system.workflow_run_id
interaction.id
delegation.id
delegation.parent_id
delegation.mode
delegation.depth
delegation.attempt
delegation.caller
delegation.callee
member.role
member.agent_name
member.agent_version
member.manifest_id
```

Dynamic-admission spans also record registry, candidate, policy version,
decision, reason category, evidence hash, assigned role, and admitted
manifest. Do not place arbitrary agent text or rejection explanations in
metric labels.

## Record the graph and its changes

Every run records its initial graph and each accepted graph change. A graph
record contains:

- graph version and parent version;
- added, removed, substituted, or quarantined members;
- added, removed, enabled, or disabled edges;
- the proposer and the deterministic decision authority;
- policy and evidence references;
- timestamp and workflow event identity; and
- the composition or run manifest digest.

State transitions record previous and next state, transition type, initiating
principal, accepted evidence references, policy decision, and workflow event.
Sensitive payloads remain in controlled artifact storage.

## Keep an interaction ledger

The ledger is the compact, authoritative account of material system activity.
It records:

```text
interaction and delegation identity
caller, callee, role, and graph version
objective and input/output schema hashes
effective authority and data-classification decision
budget reserved, measured, and released
dispatch, start, completion, and queue timestamps
outcome, error category, and retry disposition
evidence, approval, side-effect, and compensation references
```

Ledger entries SHOULD be append-only or tamper-evident. The ledger stores safe
metadata and references, not unrestricted prompts, private reasoning,
secrets, or raw customer content.

## Normalized outcomes

System outcomes use a stable taxonomy:

```text
success
success_degraded
needs_information
escalated
rejected
cancelled
budget_exhausted
deadline_exceeded
policy_blocked
admission_failed
conflict_unresolved
no_progress
failed_transient
failed_permanent
partial_effect
compensated
```

Interaction outcomes use the
[result-envelope](05-delegation-and-interactions.md) taxonomy. Provider and
framework errors map to stable internal categories while retaining the
original restricted diagnostics.

## Metrics

Track at least:

| Area | Metrics |
| --- | --- |
| Outcomes | Runs, success, degraded success, escalation, rejection, partial effect |
| Graph | Active members, graph changes, admission decisions, substitutions, quarantines |
| Coordination | Delegations, depth, fan-out, rounds, handoffs, conflicts, no-progress termination |
| Members | Runs, utilization, outcomes, latency, errors, retries, queue time |
| Interactions | Calls, denials, malformed results, duplicates, late results, output bytes |
| Reliability | Workflow errors, timeouts, cancellations, replay failures, compensations |
| Capacity | Active branches, queue depth, saturation, reservations, backpressure |
| Models and tools | Requests, calls, tokens, latency, errors, retries, estimated cost |
| Security | Unauthorized edges, scope denials, data-flow denials, injection propagation |
| Approval | Requested, approved, rejected, expired, changed action, wait duration |
| Quality | Task success, routing, handoff completeness, evidence, conflict resolution |
| Cost | Total, by member and edge, unused reservations, cost per compliant success |

Metrics use low-cardinality labels such as system, version, environment,
topology, role, interaction type, outcome, and policy category. Besides the
values the single-agent guidance keeps out of labels, run IDs, delegation IDs, and
dynamic member IDs belong in traces, ledgers, or restricted logs.

## Watch dynamic systems for drift

Dynamic systems additionally monitor:

- candidate and admission distributions;
- selection reasons and selection regret;
- registry freshness, errors, and policy mismatches;
- run-graph size and shape distributions;
- previously unseen member, edge, role, or protocol combinations;
- member churn and substitution rates;
- recursive depth, branching, useful-work ratio, and abandoned subtrees;
- blackboard write contention, stale reads, and unresolved records; and
- event lag, duplication, reordering, and feedback-loop indicators.

Unexpected graph behavior is drift even if models and prompts have not
changed.

## Content, privacy, and reasoning

Prompt, completion, interaction
payload, blackboard, and event-content capture is off by default. Enabling
any of it requires purpose, approval, classification, minimization,
redaction, access, retention, deletion, sampling, residency, and
affected-party review.

Do not require private chain-of-thought or unrestricted internal reasoning
for observability. Record typed decisions, selected alternatives, evidence
references, policy outcomes, safe summaries, hashes, and externally meaningful
rationales.

Redaction occurs before export. Besides what the single-agent guidance lists, it
covers identity tokens, hidden instructions, artifact URLs, workflow history
payloads, bids, error messages, and content copied from other agents.

## Audit

Audit records are required for:

- dynamic member admission, substitution, removal, and quarantine;
- graph or policy changes;
- authorization overrides and exceptional routing;
- approval and consequential action;
- kill switches, manual workflow intervention, and compensation;
- production promotion and rollback;
- sensitive artifact access or export; and
- risk acceptance and exception use.

Records contain the accountable actor, action, target, time, reason category,
system, run, and workflow identity, manifest and graph version, policy
version, canonical argument or change hash, approval reference, result, and
idempotency key where applicable.

## Sampling and retention

- Aggregate metrics continuously.
- Retain admission changes, policy denials, approval, consequential effects,
  partial effects, security events, and audit failures at 100%.
- Retain enough graph and ledger data to reconstruct every production
  outcome.
- Sample ordinary successful traces based on volume and risk.
- Stratify samples across topology, graph shape, depth, member, role, and
  outcome.
- Sample online evaluation independently from operational trace sampling.
- Apply data-specific retention and deletion policies to referenced
  artifacts.

High-risk and dynamic systems SHOULD use tail-based sampling that retains
unusual graphs, deep recursion, degraded outcomes, high cost, high latency,
conflicts, and policy denials.

## Dashboards

Every production system needs dashboards for outcome, SLO, and workflow
health; graph shape, admission, membership, and topology behavior;
delegation, routing, handoff, aggregation, and termination; member and
interaction reliability; quality, safety, and risk indicators; capacity,
queues, concurrency, and backpressure; tokens, tools, budgets, reservations,
and cost; and approval, consequential actions, and compensation.

Operators SHOULD be able to move from a system-level symptom to one run,
graph, delegation, agent, model, tool, policy decision, and artifact
reference.

## Alerts

Urgently alert on:

- an unauthorized member, edge, scope, tenant, or data flow;
- an unapproved consequential action or duplicate side effect;
- a manifest, graph, schema, or policy integrity failure;
- runaway recursion, fan-out, event loop, or spend;
- audit or authoritative state failure;
- kill-switch failure; and
- persistent workflow, queue, registry, or required-member outage.

Use lower-urgency alerts for quality regression, routing drift, member churn,
increased substitutions, conflict growth, no-progress termination, cost or
token growth, reservation leakage, queue saturation, and unexpected graph
patterns.

## Service objectives

Each system declares objectives for successful and compliant completion;
hard-gate adherence; active-processing and end-to-end duration; maximum queue
and approval wait; workflow and required-member availability; admission and
routing correctness; cancellation and kill-switch propagation; cost per
successful compliant outcome; and the maximum degraded-completion rate.

Measure human waiting, queued capacity, and active processing separately so
one does not hide another.

## Common pitfalls

- **Reading the trace tree as the truth.** Fan-out and queued work did not
  nest, and no delegation IDs were recorded to rebuild the run.
- **Putting run or member IDs in metric labels.** Dynamic membership turned
  every new member into a new time series.
- **Not recording the graph.** After the registry changed, nobody could say
  which members a past run had used.

## Before you move on

- [ ] Spans carry the system, delegation, and member correlation fields.
- [ ] Each run records its graph changes and an interaction ledger.
- [ ] Capture is off by default and redaction covers inter-agent content.
- [ ] Alerts cover unauthorized edges, runaway expansion, and kill-switch
  failure.

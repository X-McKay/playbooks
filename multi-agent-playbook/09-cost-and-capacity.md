# 9. Cost and capacity

This guide is for developers who need a multi-agent system to stay affordable
and responsive under load. Each member still follows the Agent Playbook's
[cost optimization](../agent-playbook/10-cost-optimization.md) chapter. For
the system, optimize total cost and capacity per successful, compliant system
outcome. A design that improves one quality metric while creating
uncontrolled fan-out, queueing, retries, or operational burden is not
optimized.

## Count the whole cost

System cost includes:

```text
member model requests and reasoning tokens
tool, retrieval, MCP, and external API usage
workflow, durable step, queue, storage, and artifact infrastructure
failed, cancelled, duplicate, speculative, and retried work
review, approval, evaluation, monitoring, and recovery
idle reservations and unavailable capacity
```

Attribute costs to the root run, member, role, interaction, branch, model,
tool, and outcome where possible. Unknown cost remains unknown rather than
zero.

## Work in this order

1. Prevent runaway graphs, loops, retries, and event amplification.
2. Remove unnecessary members, edges, reviews, and duplicated work.
3. Bound depth, fan-out, concurrency, rounds, tools, context, and output.
4. Use deterministic routing and computation where appropriate.
5. Improve task decomposition, handoff, and early termination.
6. Improve prompt caching and safe application caching.
7. Route each role to the least expensive model proven capable.
8. Tune concurrency, speculation, retries, and infrastructure.
9. Consider provider, marketplace, or commercial changes.

## Budget hierarchy

Every run has a root budget. Shared deployments SHOULD also enforce budgets
at conversation, actor, tenant, system, environment, and organization scope,
alongside each member's own
[budget hierarchy](../agent-playbook/10-cost-optimization.md#budget-hierarchy).

```yaml
budgets:
  run:
    max_agent_runs: 6
    max_parallel_agents: 3
    max_model_requests: 20
    max_tool_calls: 30
    max_input_tokens: 80000
    max_output_tokens: 12000
    max_cost_usd: 2.00
    deadline_seconds: 180
  tenant_daily:
    warning_cost_usd: 500
    maximum_cost_usd: 750
  deployment_monthly:
    warning_cost_usd: 20000
    maximum_cost_usd: 25000
```

The strictest applicable remaining limit governs. In-memory counters are
insufficient for worker fleets, child workflows, dynamic members, or runs
that resume elsewhere.

## Budget escrow

Before an interaction starts, the system reserves a bounded grant from the
parent's remaining allocation. A grant covers the child's own work and any
descendants it is permitted to create. The workflow steps for reserving and
reconciling are in
[durable coordination](06-durable-coordination.md#reserve-and-reconcile-budgets).

The ledger maintains:

```text
root limit
committed consumption
active reservations
remaining unreserved capacity
unknown or disputed usage
```

At all times:

```text
committed + active reservations <= hard limit
```

Unused reservation returns to the parent after the branch reaches a durable
terminal state. Lost workers, late results, and failed usage reporting MUST
NOT cause silent double-spend or reservation leakage.

## Know your worst case

Depth, fan-out, and retries multiply. For a uniform tree, a conservative node
bound is:

```text
maximum nodes = 1 + fanout + fanout^2 + ... + fanout^depth
maximum executions = maximum nodes * maximum attempts per node
```

Real systems SHOULD calculate bounds from the declared interaction graph and
per-edge limits rather than rely on the uniform formula. `max_agent_runs` and
the root request, token, cost, and deadline limits remain authoritative even
when a calculated graph bound is higher.

An event-driven system additionally bounds events produced per event,
delivery attempts, outstanding messages, and maximum causal-chain length.

## Limit capacity separately from spend

Spend and capacity are separate controls. Bound:

- active system runs;
- active members and branches per run;
- per-role, member, model, tool, tenant, and provider concurrency;
- queue depth and maximum queue age;
- workflow tasks, durable steps, and child workflows;
- registry, artifact, and blackboard operations; and
- token and request rate.

Concurrency reduces wall-clock time only until provider, tool, queue, worker,
or downstream capacity saturates. Above that point it increases queueing,
timeouts, retries, and cost.

## Push back before expensive work

Apply admission control before expensive work. When capacity is unavailable,
policy chooses among:

- queueing within a stated maximum wait;
- reducing optional fan-out through a tested degraded mode;
- selecting an admitted fallback with equivalent controls;
- deferring non-urgent work;
- rejecting with a retry-after signal; or
- escalating to an operator or human process.

The system MUST NOT silently drop required branches, safety reviews,
approvals, or evidence gathering to preserve throughput.

## Architecture economics

| Topology | Where cost goes | How to control it |
| --- | --- | --- |
| Pipelines and handoffs | Grows roughly with the number of stages | Remove stages that do not materially change decisions; pass compact typed state rather than full histories |
| Supervisor and worker | Coordinator calls add routing overhead | Use deterministic routing for known cases, keep the catalog small, and avoid asking multiple coordinators to make the same choice |
| Fan-out, voting, and review | Parallel work multiplies requests | Size the panel to measured marginal benefit; stop optional branches when enough evidence has arrived, if the stopping rule is deterministic and evaluated |
| Hierarchies | Every layer adds summarization and management work | Prefer shallow hierarchies, route directly when policy permits, and measure coordination cost against specialist work |
| Blackboards and events | Storage, indexing, polling, notification, and compaction | Prefer event-driven reads over wasteful polling; expire obsolete tasks and artifacts deterministically |
| Recursive systems | The highest expansion risk | Use task-value estimates, strict node and subtree grants, no-progress detection, duplicate-task detection, and early subtree cancellation |
| Dynamic membership and markets | Discovery, admission, bidding, compatibility checks, and cold starts before task work begins | Cache safe registry metadata, limit candidate sets, and evaluate whether dynamic selection improves outcome or capacity enough to justify the overhead |

## Route models per role

Resolve a versioned model policy for each role, using the same routing
considerations as for a single agent plus evidence from system evals.
Escalation to a more capable model uses explicit signals; in a system these
include unresolved conflict as well as failed validation, measured
complexity, or a high-risk decision.

The coordinator SHOULD NOT default every specialist to its own model choice.
The system constrains available routes and prices, while role policy selects
from evaluated options. Account for failed attempts plus escalation across
the whole system; model cascades can cost more than starting with the
appropriate route.

## Pass less context

- Pass task-specific typed summaries and evidence references.
- Do not copy full parent histories to every child.
- Keep role instructions and capability catalogs narrow.
- Retrieve artifacts lazily and in bounded chunks.
- Deduplicate evidence and shared immutable context.
- Compact blackboards and long-lived state by typed policy.
- Bound member output before aggregation.
- Preserve provenance when summarizing or caching.

Context reduction is accepted only when handoff-completeness, evidence, and
outcome evals continue to pass.

## Caching

Use provider prompt caching for stable prefixes such as system policy, role
instructions, and tool schemas. Keep volatile task, membership, and user
content later where provider semantics permit.

Application caching requires a typed key containing the relevant tenant,
actor, authorization, policy, model, agent, data, and schema versions. Never
reuse:

- approval decisions;
- consequential tool results as permission to repeat an action;
- user-specific or tenant-specific data across boundaries;
- dynamic admission decisions after their evidence or policy expires; or
- security-sensitive results without explicit freshness semantics.

Shared immutable evidence MAY be cached when authorization, provenance,
integrity, expiry, and invalidation are enforced.

## Speculation and hedging

Speculative parallel calls or hedged requests MAY reduce tail latency, but
they create duplicate work and potential effects. They require:

- read-only or safely idempotent execution;
- explicit duplicate cancellation and result selection;
- reserved budget for every branch;
- provider and tenant concurrency compliance; and
- eval evidence that the latency benefit justifies the cost.

Do not hedge consequential actions or approval decisions.

## Retry economics

Retries consume the same global budgets as initial attempts. Measure retry
cost by layer and failure category. Eliminate nested retries that respond to
the same failure, and use circuit breakers for provider, registry, tool, and
member outages.

Retry storms across a dynamic graph are a capacity incident. The control
plane MUST be able to stop new dispatch without waiting for models to comply.

## Plan for running out

Every hard limit has a user- and operator-visible outcome. Depending on
policy, the system may return the best validated partial result, request
information, enter a tested degraded mode, escalate, or fail safely.

Budget exhaustion MUST NOT bypass a required reviewer, deterministic policy,
human approval, audit write, or compensation. Reserve capacity for mandatory
finalization and safety work before allocating optional tasks.

## How to optimize

Use the Agent Playbook's method at system scale. For each change:

1. Measure baseline outcome, safety, latency, capacity, and total cost.
2. Identify the dominant member, edge, retry, context, queue, or
   infrastructure contributor.
3. Change one architectural or policy variable where practical.
4. Run member, interaction, system, adversarial, and durability evals.
5. Compare distributions and worst cases, not only averages.
6. Promote only when hard gates hold and cost per successful compliant
   outcome improves without unacceptable capacity or reliability regression.

## Common pitfalls

- **Tuning prices before structure.** A cheaper model saved a little while a
  redundant reviewer and fan-out cost far more.
- **Counting spend but not capacity.** Every run was within budget, and the
  provider still throttled because concurrency had no limit.
- **Spending the budget on optional work.** The run hit its limit before it
  could write audit records or compensate.

## Before you move on

- [ ] Every run has a durable root budget, and child grants are reserved
  from it.
- [ ] Worst-case expansion is calculated from the declared graph.
- [ ] Capacity limits are set separately from spend, and backpressure never
  drops required work.
- [ ] Capacity is reserved for finalization, audit, and compensation.

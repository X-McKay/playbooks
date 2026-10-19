# 8.4 Capacity, Admission Control, and Backpressure

**Status:** 0.5.0-draft.2 — draft
**Audience:** Engineers and operators of shared or externally exposed agent services
**Applicability:** Needed for shared-capacity or externally exposed systems. Low-volume local agents need bounded per-run limits, not a distributed scheduler.

[Part 8](README.md) · [Applicability](../../applicability.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md) · [5.1 Observability, Budgets, and Operational Control](../../development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md)

## Purpose and applicability

**Admission control** decides whether new work may start within safe limits; **backpressure** pushes that decision upstream. Without them, competition for finite model, retrieval, tool or compute capacity makes excess work queue, hold resources and amplify timeouts and retries. Early rejection, load shedding [1] and bounded queues [2] are established ways to contain overload; set thresholds for your workload.

A low-volume agent with no shared bottleneck needs only per-run limits and a safe failure outcome. Services facing bursts, many tenants, worker fleets or rate-limited dependencies need a shared-capacity policy applying the most restrictive limit across request, run, actor, tenant, service and dependency. Cost controls are not capacity controls: a run within its spend budget can still hold too many concurrent requests or overwhelm a downstream service.

## Working model

Capacity is not one number: active runs, concurrent model requests, retrieval or tool calls, pending work, token or request rates and expensive downstream operations may each need a limit. Requests differ in cost, so model the resource that actually limits useful work and test with representative load, not requests per second alone.[1]

When work arrives faster than it finishes, a queue grows, uses memory and turns overload into stale work. Bound its size and maximum wait, tie waiting to the task deadline, and reject or cancel by policy work that cannot finish in time.[2]

Limits must compose: branches across many runs hit the shared dependency together whatever each run's allowance, and retries, resumed work and speculative branches count against the same budgets. An in-memory counter cannot enforce a service-wide limit; use an enforcement point or coordinated reservation, which also stops children overspending a parent budget. Reconcile unused grants only when their state is known; this is policy design, not an exact accounting guarantee.

Admission also allocates scarce capacity: per-tenant or per-actor limits stop one source monopolizing the service, shared headroom avoids stranding capacity behind rigid quotas, and the fairness identity must match your tenancy model. Start simple; no scheduler fits every workload, so document and test any priority classes.

## Decisions and best practices

- **Size from the workload.** Start from expected volume, burst shape, concurrency, work-size variation, deadlines and dependency limits, including failure and retry behavior, and validate under representative work before setting ceilings. Leave headroom for completion work (returning a valid outcome, keeping required evidence) so optional parallel work cannot take every slot.
- **Choose overload behavior before release:** queue briefly, defer non-urgent work, reject admission, drop optional work in a tested degraded mode, route to an evaluated alternative, or escalate. Offer a retry time where the interface allows; HTTP 429 may carry `Retry-After`, but the standard does not say how a service identifies a user or counts requests.[3] Do not promise a wait the system cannot keep.
- **Degrade without changing meaning.** An agent that reads fewer documents cannot present an incomplete search as complete and grounded; it returns a bounded partial result only where the contract allows, otherwise it asks, defers or fails safely. Required safety review, approval or evidence steps are never shed.
- **Protect each dependency.** Limit in-flight calls and pending work, use timeouts, and retry only at the layer directly above the failing call, with randomized backoff, so layers do not multiply retries. About three attempts per request and a per-client retry budget of about 10% of requests are practical starting points.[1] [2] A circuit breaker can stop requests to an unhealthy dependency while it recovers, and some systems treat retry budgets and active-request limits as separate dimensions.[4] Retries use the same limits as first attempts, and the control plane can stop new dispatch without relying on the model to notice overload.

## Requirements

- **CAPACITY-01** For a shared-capacity or externally exposed system, the owner MUST record expected normal and burst demand, the constrained resources and dependencies, workload assumptions, completion deadlines, and the evidence used to set capacity limits before production admission is enabled.
- **CAPACITY-02** For a system with concurrent runs or workers, the operator MUST enforce applicable request, run, and shared-scope budgets and concurrency limits across all workers; parallel branches, resumed work, and retries MUST consume the applicable limits. A child task MUST obtain a bounded allocation before dispatch when it can consume shared capacity on behalf of a parent.
- **CAPACITY-03** For a system that queues shared work, the operator MUST bound both pending-work depth and maximum queue age, and MUST define what happens when either limit or the task deadline is reached. The policy MUST prevent a single actor or tenant from exceeding its declared share where that boundary applies.
- **CAPACITY-04** For each constrained downstream dependency, the owner MUST define concurrency, timeout, retry, and overload behavior; retries MUST be bounded and MUST NOT multiply without bound across layers. New dispatch MUST be stoppable independently of model-generated decisions.
- **CAPACITY-05** For every hard capacity or budget limit, the system MUST define a user-visible terminal or deferred outcome and MUST preserve capacity for required safety, completion, and evidence work. Degraded behavior MUST be tested and MUST NOT silently remove a required branch, review, approval, or evidence step.
- **CAPACITY-06** Before enabling shared admission, the owner MUST test burst load, saturated dependencies, queue-age/depth limits, retry amplification, fairness where applicable, and safe exhaustion; evidence MUST identify the tested candidate and configuration and MUST record unresolved limits rather than treating unknown usage as zero.

## Worked example

Many employees query the fictional read-only policy assistant at once; retrieval and model-request concurrency are the shared bottlenecks, validated with varied request sizes. Values are hypothetical:

```yaml
admission_policy:
  per_run:
    max_model_requests: 4
    max_retrieval_calls: 6
    deadline_seconds: 45
  service:
    max_active_runs: 24
    max_active_model_requests: 12
    max_pending_runs: 8
    max_queue_age_seconds: 10
  tenant:
    max_active_runs: 6
  on_limit:
    queue_until: min(queue_age_limit, task_deadline)
    then: reject_with_retry_guidance
  on_dependency_throttle:
    stop_new_calls: true
    retries: bounded_with_backoff
  mandatory_completion_reserve:
    preserve_terminal_outcome: true
    preserve_required_evidence: true
```

A morning burst fills the bounded queue. Admission checks tenant and service-wide slots before each run, so local allowances cannot sum past the service limit, and at the queue-age or task deadline new work is rejected with a retry path. When retrieval throttles, the controller stops launching retrieval calls rather than retry in parallel.

The assistant cannot omit a required document and call its answer complete: it returns a contract-permitted partial result stating the limit, or `needs_information` or `failed`. Admission and safety controls stay outside the model's discretion. Tests cover a saturated queue, competing tenants, retrieval throttling, retry exhaustion and the final outcome.

## Evidence and checklist

Record the workload model and derived limits: constrained resources, burst and size assumptions, allocation scopes, queue bounds, retry policy, exhaustion behavior and the completion reserve.

Test at saturation: combined concurrency and child grants stay in bounds, waiting requests expire or are rejected, retries stay bounded, competing tenants are treated fairly, and degraded modes keep required checks and evidence. Signals and per-run budgets are in 5.1, optimization in [8.3](03-cost-latency-and-performance-optimization.md), and durable child work and reservation reconciliation in [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

- [ ] Shared and dependency limits are separate from per-run spend limits.
- [ ] Tenant fairness and any priority behavior are explicit and tested.

## References

[1]: https://sre.google/sre-book/handling-overload/ "Handling Overload"
[2]: https://sre.google/sre-book/addressing-cascading-failures/ "Addressing Cascading Failures"
[3]: https://www.rfc-editor.org/rfc/rfc6585 "RFC 6585: Additional HTTP Status Codes"
[4]: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking "Circuit Breaking"

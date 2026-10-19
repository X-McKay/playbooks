# 8.4 Capacity, Admission Control, and Backpressure

**Status:** 0.5.0-draft.2 — draft
**Audience:** Engineers and operators of shared or externally exposed agent services
**Applicability:** Needed for shared-capacity or externally exposed systems. Low-volume local agents need bounded per-run limits, not a distributed scheduler.

[Part 8](README.md) · [Applicability](../../applicability.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md) · [5.1 Observability, Budgets, and Operational Control](../../development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md)

## Purpose and applicability

**Admission control** decides whether new work may start without exceeding safe limits. **Backpressure** pushes that decision upstream. Both matter when runs, users, workers, or services compete for finite model, retrieval, tool, or compute capacity. Without explicit limits, excess work waits in queues, uses resources, and amplifies timeouts and retries. Early rejection and load shedding are established ways to contain overload [1], and so are bounded queues [2]. Set thresholds to fit your workload.

This chapter applies conditionally. A private, low-volume agent with no shared bottleneck can use per-run limits and a simple safe failure outcome. A service exposed to bursts, many tenants, worker fleets, or rate-limited dependencies needs an explicit shared-capacity policy. Apply the most restrictive relevant limit across request, run, actor, tenant, service, and dependency. Cost controls are not capacity controls: a run can stay within its spend budget and still hold too many concurrent requests or overwhelm a downstream service.

## Working model

Capacity is not one number. You may need separate limits for active runs, concurrent model requests, retrieval or tool calls, pending work, token or request rates, and expensive downstream operations. Requests differ in cost, so requests per second alone can mislead. Model the resource that actually limits useful work and test it with representative load. [1]

When work arrives faster than it finishes, a queue grows. Waiting uses memory and delays responses, and a long queue turns overload into stale work. Bound both its size and how long a request may wait, and tie waiting to the task deadline. Work that cannot finish by its deadline should be rejected or cancelled by explicit policy and not left to hold capacity unseen. [2]

Limits must compose across concurrency and retries. If several runs each start parallel branches, the combined demand reaches the shared dependency, whatever each run's local allowance. Count retries, resumed work, and speculative branches against the same run and shared budgets. A local in-memory counter cannot enforce a service-wide limit across workers; use an enforcement point or coordinated reservation suited to the deployment. Reservation stops children from overspending a parent budget; reconcile unused grants only when their state is known. Final provider billing may not be knowable exactly, so treat this as policy design and not an accounting guarantee.

Admission policy also decides who gets scarce capacity. Per-tenant or per-actor limits stop one source from monopolizing the service, while shared headroom avoids stranding capacity behind rigid quotas. The identity used for fairness must match your authorization and tenancy model. Start with a simple policy, document any priority classes, and test that it behaves as intended; no one scheduling algorithm fits every workload.

## Decisions and best practices

Start with expected volume, burst shape, concurrency, variation in work size, completion deadlines, and dependency limits. Validate capacity under representative work before setting production ceilings, and include failure and retry behavior in the workload model. Leave headroom for completion work, such as returning a valid outcome and keeping required evidence, so optional parallel work cannot take every slot.

Choose overload behavior before release. Depending on the task, the system may queue briefly, defer non-urgent work, reject admission, drop optional work in a tested degraded mode, route to an evaluated alternative, or escalate. Where the interface allows, offer a retry time. HTTP 429 is a standard rate-limit response that may carry `Retry-After`, but the standard does not say how a service identifies a user or counts requests. [3] Do not promise a wait the system cannot keep.

Degraded mode must keep the task's meaning and required controls. An agent that reads fewer documents cannot present an incomplete search as complete and fully grounded. It may return a clearly bounded partial result only if the contract allows that outcome; otherwise it asks for information, defers, or fails safely. A required safety review, approval, or evidence step is not optional load to shed.

Protect each dependency on its own. Limit in-flight calls and pending work, use timeouts and bounded retries, and do not let several layers retry the same failure; retry at the layer directly above the failing call, with randomized backoff. A per-request cap of about three attempts and a per-client retry budget of about 10% of requests are practical starting points. [1] [2] A circuit breaker can stop new requests to an unhealthy dependency while it recovers, and retry budgets and active-request limits are separate dimensions in some systems. [4] Every retry uses the same limits as a first attempt. A control plane must be able to stop new dispatch without relying on the model to decide it is overloaded.

## Requirements

- **CAPACITY-01** For a shared-capacity or externally exposed system, the owner MUST record expected normal and burst demand, the constrained resources and dependencies, workload assumptions, completion deadlines, and the evidence used to set capacity limits before production admission is enabled.
- **CAPACITY-02** For a system with concurrent runs or workers, the operator MUST enforce applicable request, run, and shared-scope budgets and concurrency limits across all workers; parallel branches, resumed work, and retries MUST consume the applicable limits. A child task MUST obtain a bounded allocation before dispatch when it can consume shared capacity on behalf of a parent.
- **CAPACITY-03** For a system that queues shared work, the operator MUST bound both pending-work depth and maximum queue age, and MUST define what happens when either limit or the task deadline is reached. The policy MUST prevent a single actor or tenant from exceeding its declared share where that boundary applies.
- **CAPACITY-04** For each constrained downstream dependency, the owner MUST define concurrency, timeout, retry, and overload behavior; retries MUST be bounded and MUST NOT multiply without bound across layers. New dispatch MUST be stoppable independently of model-generated decisions.
- **CAPACITY-05** For every hard capacity or budget limit, the system MUST define a user-visible terminal or deferred outcome and MUST preserve capacity for required safety, completion, and evidence work. Degraded behavior MUST be tested and MUST NOT silently remove a required branch, review, approval, or evidence step.
- **CAPACITY-06** Before enabling shared admission, the owner MUST test burst load, saturated dependencies, queue-age/depth limits, retry amplification, fairness where applicable, and safe exhaustion; evidence MUST identify the tested candidate and configuration and MUST record unresolved limits rather than treating unknown usage as zero.

## Worked example

An internal policy assistant answers questions from approved, current, permission-filtered documents and returns citations with uncertainty. It cannot write externally. Several employees ask questions at once, and the owner identifies retrieval and model-request concurrency as the shared bottlenecks. Capacity is validated with requests of different sizes, not by assuming every question costs the same. The values below are hypothetical settings used to explain the design, not measured capacity or recommendations.

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

A morning burst fills the bounded queue. The admission layer checks tenant and service-wide slots before a run starts, so many locally permitted requests cannot together exceed the service limit. Once queue age or the task deadline is reached, new work is rejected with a retry path and not left waiting past its useful window. If retrieval signals throttling, the controller stops launching new retrieval requests and does not retry in parallel without bound.

The assistant cannot quietly omit a required document and still call its answer complete. With enough approved evidence for a contract-permitted bounded partial result, it returns that result and states the limit. Otherwise it returns `needs_information` or `failed`, as the contract says. Admission and safety controls stay outside the model's discretion. Tests cover a saturated queue, competing tenants, retrieval throttling, retry exhaustion, and the final outcome, and report actual workload results.

## Evidence and checklist

Keep a short record of the workload model and the limits derived from it: constrained resources, dependency limits, burst and request-size assumptions, allocation scopes, queue depth and age, retry policy, and behavior at each exhaustion point. Say which capacity is reserved for completion work.

Test by saturating the system, not only at normal load. Show that combined concurrency and child grants stay within bounds, that waiting requests expire or are rejected as intended, and that retries do not create unbounded extra work. Where fairness matters, test competing tenants. Exercise each degraded mode and show that required safety checks and evidence remain. Operational signals and per-run budgets are in 5.1; [8.3](03-cost-latency-and-performance-optimization.md) covers performance optimization. For limits tied to durable child work and reservation reconciliation, see [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

- [ ] Shared and dependency limits are separate from per-run spend limits.
- [ ] Combined parallel work, retries, and resumed work are counted.
- [ ] Queue depth, queue age, and overload outcomes are bounded and documented.
- [ ] Tenant fairness and any priority behavior are explicit and tested.
- [ ] Required safety, completion, and evidence work cannot be shed.
- [ ] Saturation, throttling, and safe exhaustion have evidence for the exact candidate.

## References

[1]: https://sre.google/sre-book/handling-overload/ "Handling Overload"
[2]: https://sre.google/sre-book/addressing-cascading-failures/ "Addressing Cascading Failures"
[3]: https://www.rfc-editor.org/rfc/rfc6585 "RFC 6585: Additional HTTP Status Codes"
[4]: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking "Circuit Breaking"

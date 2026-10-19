# 8.4 Capacity, Admission Control, and Backpressure

**Status:** 0.5.0 first draft
**Audience:** Engineers and operators of shared or externally exposed agent services
**Applicability:** Required for shared-capacity or externally exposed systems; low-volume local agents need bounded per-run limits, not a distributed scheduler.

[Part 8](README.md) · [Applicability](../../applicability.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md) · [5.1 Observability, Budgets, and Operational Control](../../development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md)

## Purpose and applicability

Admission control decides whether new work can begin without exceeding a system's safe operating limits. Backpressure communicates or enforces that decision upstream. They matter when multiple runs, users, workers, or services compete for finite model, retrieval, tool, or compute capacity. Without explicit limits, excess work can wait in queues, consume resources, and amplify timeouts and retries. Bounded queues, early rejection, and load shedding are established ways to contain overload; their thresholds and policies must fit the actual workload.[1] [2]

This chapter is a conditional reference. A private, low-volume agent with no shared bottleneck can use its per-run limits and a simple safe failure outcome. A service exposed to bursts, multiple tenants, worker fleets, or rate-limited dependencies needs an explicit shared-capacity policy. Apply the most restrictive relevant limit across the request, run, actor, tenant, service, and dependency. Do not confuse cost controls with capacity controls: a run can stay within its spend budget yet occupy too many concurrent requests or overwhelm a downstream service.

## Working model

Capacity is not one number. The system may need separate limits for active runs, concurrent model requests, retrieval or tool calls, pending work, token or request rates, and expensive downstream operations. Different requests can consume different amounts of resources, so a raw requests-per-second figure may be an incomplete demand measure. Model the resource or bottleneck that constrains useful work, and test it with representative workloads.[1]

When work arrives faster than it can finish, a queue grows. Waiting consumes memory and makes responses less timely; a large queue may turn overload into stale work rather than useful throughput. Bound both its size and how long a request may wait. Tie waiting to the task deadline: work that cannot finish before its deadline should be rejected, cancelled, or otherwise handled by an explicit policy rather than allowed to consume capacity invisibly.[2]

Limits must compose across concurrency and retries. If several runs each start parallel branches, their aggregate demand—not just each run's local allowance—reaches the shared dependency. Count retries, resumed work, and speculative branches against the same relevant run and shared budgets. For distributed workers, a local in-memory counter cannot reliably enforce a service-wide limit. Use an enforcement point or coordinated reservation mechanism appropriate to the deployment. Reservation protects a parent budget from overspending when children are active; reconcile unused grants only when their state is known. This is a policy design requirement, not a claim that final provider billing can always be known exactly.

Admission policy also governs who gets scarce capacity. Per-tenant or per-actor limits can stop one source from monopolizing the service, while shared headroom can avoid stranding all capacity behind rigid quotas. The identity and scope used for fairness must match the system's authorization and tenancy model. Pick a simple policy first, document any priority classes, and test whether it behaves as intended; no single scheduling algorithm is right for every workload.

## Decisions and best practices

Start with expected request volume, burst shape, concurrency, work-size variation, completion deadline, and dependency limits. Measure or otherwise validate capacity under representative work before setting production ceilings. Include failure and retry behavior in the workload model. Add headroom for required completion work, such as returning a valid outcome and preserving required operational evidence, rather than allocating every available slot to optional parallel work.

Choose overload behavior before release. Depending on the task, a system may queue briefly, defer non-urgent work, reject admission, reduce optional work through a tested degraded mode, route to an evaluated alternative, or escalate. A response can offer a retry time where the interface supports it; HTTP 429 is one standardized rate-limit response and may carry `Retry-After`, but the standard does not prescribe how a service identifies a user or counts requests.[3] Do not promise a wait time that the system cannot support.

Degraded mode must preserve the task's meaning and required controls. For example, an agent that uses fewer documents cannot present an incomplete search as a complete, fully grounded answer. It can return a clearly bounded partial result only if the contract allows that outcome; otherwise it should ask for information, defer, or fail safely. A required safety review, approval, or evidence step is not optional load to shed.

Protect dependencies independently. Set appropriate limits on in-flight calls and pending work, use timeouts and bounded retries, and avoid multiple layers retrying the same failure. A circuit breaker or equivalent may stop new requests to an unhealthy dependency while it recovers. Retry budgets and active-request limits are distinct capacity dimensions in some systems; their exact implementation varies.[4] Every retry consumes the same applicable limits as an initial attempt. A control plane must be able to stop new dispatch without relying on the agent model to decide that it is overloaded.

## Requirements

- **CAPACITY-01** For a shared-capacity or externally exposed system, the owner MUST record expected normal and burst demand, the constrained resources and dependencies, workload assumptions, completion deadlines, and the evidence used to set capacity limits before production admission is enabled.
- **CAPACITY-02** For a system with concurrent runs or workers, the operator MUST enforce applicable request, run, and shared-scope budgets and concurrency limits across all workers; parallel branches, resumed work, and retries MUST consume the applicable limits. A child task MUST obtain a bounded allocation before dispatch when it can consume shared capacity on behalf of a parent.
- **CAPACITY-03** For a system that queues shared work, the operator MUST bound both pending-work depth and maximum queue age, and MUST define what happens when either limit or the task deadline is reached. The policy MUST prevent a single actor or tenant from exceeding its declared share where that boundary applies.
- **CAPACITY-04** For each constrained downstream dependency, the owner MUST define concurrency, timeout, retry, and overload behavior; retries MUST be bounded and MUST NOT multiply without bound across layers. New dispatch MUST be stoppable independently of model-generated decisions.
- **CAPACITY-05** For every hard capacity or budget limit, the system MUST define a user-visible terminal or deferred outcome and MUST preserve capacity for required safety, completion, and evidence work. Degraded behavior MUST be tested and MUST NOT silently remove a required branch, review, approval, or evidence step.
- **CAPACITY-06** Before enabling shared admission, the owner MUST test burst load, saturated dependencies, queue-age/depth limits, retry amplification, fairness where applicable, and safe exhaustion; evidence MUST identify the tested candidate and configuration and MUST record unresolved limits rather than treating unknown usage as zero.

## Worked example

An internal policy assistant answers questions from approved, current, permission-filtered documents and returns citations with uncertainty. It has no external write capability. The owner expects several employees to ask questions at once and identifies retrieval and model-request concurrency as shared bottlenecks. The owner validates capacity using representative requests of different sizes instead of assuming that every question costs the same amount.

The example policy separates a per-run allowance from the service-wide ceilings and tenant share. The values below are hypothetical policy settings for explaining the design; they are not measured capacity or universal recommendations.

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

A morning burst fills the bounded queue. The admission layer checks the tenant and service-wide slots before a run starts, so many locally permitted requests cannot collectively exceed the service limit. Once the queue age or task deadline is reached, new work is rejected with a clear retry path rather than left waiting beyond its useful window. If retrieval signals throttling, the controller stops launching new retrieval requests and does not retry in parallel without bound.

The assistant cannot silently omit a required document and still label its answer complete. If it has enough approved evidence for a contractually permitted bounded partial result, it returns that result with its limitation made clear. Otherwise it returns `needs_information` or `failed`, according to the contract. Admission and safety controls remain outside the model's discretion. Tests exercise a saturated queue, competing tenant requests, retrieval throttling, retry exhaustion, and the final outcome. The test record reports the actual candidate and workload results; the sample configuration itself is not evidence that any particular throughput or latency target has been met.

## Evidence and checklist

Keep a concise record of the workload model and the limits derived from it. Include the constrained resources, dependency limits, burst and request-size assumptions, allocation scopes, queue depth and age, retry policy, and behavior at each exhaustion point. Identify which capacity is reserved for mandatory completion work.

Demonstrate the policy with tests that saturate the system, not only a normal-load demonstration. Show that aggregate concurrency and child grants remain within declared bounds, that waiting requests expire or reject as intended, and that retries do not create unbounded extra work. Where fairness matters, test competing tenants and report the policy's behavior. Exercise each degraded mode and prove that required safety checks and evidence remain intact. Part 5.1 owns operational signals and basic per-run budgets; [8.3](03-cost-latency-and-performance-optimization.md) covers quality-preserving performance optimization. For limits tied to durable child work and reservation reconciliation, see [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md).

- [ ] Shared and dependency limits are separate from per-run spend limits.
- [ ] Aggregate parallel work, retries, and resumed work are accounted for.
- [ ] Queue depth, queue age, and overload outcomes are bounded and documented.
- [ ] Tenant fairness and any priority behavior are explicit and tested.
- [ ] Required safety, completion, and evidence work cannot be shed.
- [ ] Saturation, throttling, and safe exhaustion have evidence for the exact candidate.

## References

[1]: https://sre.google/sre-book/handling-overload/ "Handling Overload"
[2]: https://sre.google/sre-book/addressing-cascading-failures/ "Addressing Cascading Failures"
[3]: https://www.rfc-editor.org/rfc/rfc6585 "RFC 6585: Additional HTTP Status Codes"
[4]: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking "Circuit Breaking"

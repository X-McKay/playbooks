# Orderly sandbox cleanup

The adapter now calls OpenShell's supported `stop()` before deleting a session
sandbox. This avoids the observed 30-second termination delay for exercised
workloads while retaining the existing immutable-instance deletion check.
The [latency report](latency.md) records the benchmark comparison.

## What caused the delay

Three disposable sessions isolated lifecycle behavior from Temporal and inference:

| Session state and teardown | Observed cleanup wall time |
| --- | --- |
| Provisioned but idle, direct delete | 1.35 s |
| Five boundaries completed, direct delete | 30.35 s |
| Five boundaries completed, stop then delete | 2.73 s |

Both the workload and supervisor pods had a 30-second termination grace period
and no pre-stop hook. The workload's PID 1 was the OpenShell boundary process;
Python was its child. The delay was not an unconditional 30-second SDK poll or
a Python PID 1 signal-handler issue.

The initial direct-deletion observation showed both exercised-session pods running
in termination, and the workload logged `Sandbox Protocol connection lost; workload
frozen pending authenticated recovery`. Ordered stop completed in 2.40 seconds;
the subsequent deletion confirmation completed the diagnostic in 2.73 seconds.
Pod/PVC observations and pod command/grace specifications are retained in the
[diagnostic data](../benchmarks/results/cleanup-diagnostics.json). These are three
individual diagnostic observations, not a statistical comparison.

The pinned OpenShell 0.1.4
[Kubernetes driver](https://github.com/NVIDIA/OpenShell/blob/v0.1.4/crates/openshell-driver-kubernetes/src/driver.rs)
explains the meaningful difference: `delete_sandbox_inner` deletes the Sandbox
resource, allowing its owned resources to be collected together;
`stop_sandbox_inner` first removes and awaits the supervisor, then suspends and
awaits removal of the workload. The
[supervisor shutdown](https://github.com/NVIDIA/OpenShell/blob/v0.1.4/crates/openshell-supervisor/src/lib.rs)
coordinates process termination with the
[workload boundary](https://github.com/NVIDIA/OpenShell/blob/v0.1.4/crates/openshell-sandbox/src/boundary_server.rs).
The evidence supports a concurrent teardown/control-channel shutdown interaction
that consumes the normal grace period. It does not establish the exact upstream
blocking instruction or a universal OpenShell defect.

## Adapter sequence and failure behavior

1. Resolve the sandbox and validate the session owner and immutable binding ID.
2. Request `stop` through the official authenticated SDK. This coordinates graceful
   shutdown; it is not permission to return `DELETED` or provision a replacement.
3. Re-read the resource. Observed absence is handled as in existing cleanup.
   A changed ID or owner returns `REMEDIATION_REQUIRED` without deleting it.
4. Delete the same named instance with `allow_missing=True`, then call the existing
   `wait_deleted(expected_sandbox_id=..., timeout_seconds=60)`.
5. Only confirmed absence permits `DELETED` and replacement generation creation.

Stop's `FAILED_PRECONDITION`, `NOT_FOUND`, `DEADLINE_EXCEEDED` and `UNAVAILABLE`
responses fall through to revalidation and the existing delete-and-confirm path.
This covers partial provisioning and a failed or lost shutdown acknowledgement.
Other errors, including permission failures, propagate. A stop acknowledgement,
delete acknowledgement or timeout alone never counts as confirmed deletion.

The SDK's default 30-second RPC deadline still applies to stop. Failure paths can
therefore be slower than before, and the combined calls can exceed the existing
120-second close Activity budget. Temporal's bounded lifecycle retries and the
external reconciler remain necessary. This is a successful-path optimization,
not a guaranteed cleanup deadline. Cancellation of a threaded RPC can leave it
finishing remotely; OpenShell's lifecycle gates serialize its stop/delete work.

## Preserved scope

No policy, filesystem permission, network allowance, termination grace period,
Activity acceptance rule or execute retry setting changes. There is no forced
Kubernetes deletion, direct container kill, warm sandbox pool or session reuse.
Each session retains its own sandbox and workspace. No OpenShell fork is required.

The confirmation contract remains the official OpenShell immutable-instance
removal observation. The API check is not an independent storage-erasure proof:
workspace PVC garbage collection is checked separately in cluster evidence.
External accepted artifacts and Temporal histories follow the existing retention
policy. Names remain unique to session/generation; post-stop revalidation is not
an atomic compare-and-delete API or a replacement for a production lifecycle lease.
Distributed reconciliation and hostile background writers remain unqualified.

Lifecycle regressions cover ordered stop, blocking until deletion confirmation,
the four fallback statuses, changed identity/ownership, permission failure and
confirmation timeout. The full cluster suite and unchanged benchmark exercise
normal completion, parked warm agents, cold replacement, worker restart,
completion loss, cancellation and hard-termination reconciliation. Executed
results are recorded in the [evidence report](evidence.md).

# Warm execution and bounded artifact batching

This implementation amendment replaces fresh-process reconstruction on every
advance with a volatile continuation in the existing session runtime. It changes
execution cost, not Temporal's authority or the supported cooperative agent
profile. It is an explicitly requested optimization of the measured prototype;
it does not qualify arbitrary Python callbacks or the deferred wrapper SDK.

## State and ownership

One `WarmRunner` owns one ADK task per sandbox interpreter. ADK's deterministic
time, ID and random providers are process-global, so multiple session runners
must not share that interpreter. Different sessions still receive different
OpenShell workloads and workspace volumes. Runtime commands are serialized.

The cache contains the accepted tape used to build the task, its next descriptor,
and a future parked inside the model/tool bridge. It never contains an executable
tool closure authorized for later use. Execution still goes through the frozen
canonical descriptor and approved executor registry.

The runtime also remembers the current full `Position` and the exact candidate
`Position` produced by its last execution. These include workspace references.
They are volatile equality checks, not a durable latest pointer or acceptance
record. The only source of accepted progress is the position passed by an
external Activity from Temporal Workflow state.

## Normal operation

1. The first signed `advance` supplies the accepted position. The runtime loads
   its tape, restores its workspace, starts ADK and captures the next boundary.
   ADK parks there without invoking the real model or tool.
2. A signed `execute` must match the runtime's captured descriptor and position.
   The existing dispatcher executes the registered body and captures its outcome
   and post-operation workspace. ADK remains parked, including after candidate
   bytes have been uploaded to the worker.
3. The external Activity verifies the receipt's actual predecessor, operation,
   linked tape and workspace bytes. Only its completion accepted into Temporal
   history selects the candidate as the next accepted position.
4. A subsequent signed `advance` supplies that accepted position. The runtime
   restores the selected workspace. It resumes the parked task only if the full
   position is the exact local candidate and the tape extends its accepted prefix
   by exactly the cached operation. It injects the recorded outcome, runs admitted
   deterministic callbacks and parks at the next boundary, or returns the final
   answer. This advance does not perform the next model/tool effect.

Repeating an advance with the same accepted position returns the same cached
boundary or final result without repeating callbacks. It cannot consume an
unaccepted candidate. The next external effect still requires its own execute
Activity; retries for execute remain disabled.

## Recovery and shutdown

An absent continuation, changed prefix or position discontinuity closes the old
ADK task before cold reconstruction from the caller-selected tape. Recovery
injects accepted results and never calls their model/tool bodies. A pinned pending
descriptor must reconstruct identically. The offline fresh-process conformance
oracle remains available and is tested against native ADK and warm execution.

Normal close allows one second for cooperative ADK cancellation/finalization.
The cache is fenced **before** awaiting cancellation. Timeout or interruption of
that cleanup permanently poisons this runtime instance, even if its task later
finishes. Further advance and execute commands fail before workspace restoration
or effects; a safe-advance failure can trigger sandbox replacement. Runtime
shutdown also sets an irreversible closing flag before awaiting its command lock,
so queued connection handlers cannot start new work after teardown begins.
Active executor tasks are cancelled before waiting for that lock, allowing a
cooperative in-flight execute handler to release it.

A replacement generation starts only after immutable old-instance deletion is
confirmed. Its empty warm cache reconstructs from Temporal's accepted position.
A worker restart can reuse the still-parked sandbox and reconstructs Workflow
state through Temporal history. Loss of an execute completion remains
`OUTCOME_UNKNOWN`, even if the sandbox has a candidate or cached task. Neither
replacement nor a cache miss authorizes redispatch of an uncertain effect.

The one-second cancellation bound assumes cooperative async callbacks. Blocking
Python or hostile background writers remain outside the admitted profile;
external exec/Activity deadlines and sandbox deletion remain the containment
fallback. This change does not establish per-boundary descendant quiescence or
cross-host leases.

## Fewer OpenShell exchanges

An advance now needs one control exec/RPC after any required artifact upload.
There is no separate preparation RPC, replay subprocess or `pending.json` file.
The runtime already imported ADK during provisioning in the cold implementation.
The warm path reuses those resident libraries and avoids the additional import
in every replay process. Active time excludes that runtime startup; a native
fresh-exec measurement still includes its own import cost.

An execute response includes small candidate objects inline, with a **128 KiB
aggregate raw-byte budget**. The receiver checks declared references, strict
base64, hash, byte count, duplicates and aggregate bounds before storage. The
control response remains bounded to 256 KiB. Objects that do not fit retain the
existing separately bounded download path; recovery uploads retain 128 KiB
chunking and final hash verification. Large checkpoints therefore do not require
a larger control or OpenShell request limit.

For the five-boundary small-workspace trace, the expected active exchange count
is 12: one initial upload, six advance RPCs and five execute RPCs. The prior path
used 28: the same upload, six replay processes, eleven control RPCs and ten object
downloads. These counts exclude lifecycle RPCs and the immutable-identity lookup
performed before every exec. Transport is still the official authenticated
OpenShell exec API; no new ingress endpoint or network policy is introduced.

## Validation and limits

Conformance compares native results, ADK state and callback traces with the warm
path for normal, business-error and mutation branches. Recovery tests check
candidate/accepted separation, prefix mismatch, cache loss, recorded live-model
reconstruction, failed and interrupted cancellation, and runtime shutdown.
Artifact tests check inline integrity and large-object fallback. Cluster tests
exercise worker restart, cold sandbox replacement, large workspace transfer,
completion loss, cancellation, isolation policy and confirmed cleanup.

See the [evidence report](evidence.md) for executed results and the
[latency report](latency.md) for measured comparisons. Temporal credentials,
Activity completion tokens, sandbox-management credentials and cross-session
artifact access remain outside the sandbox. The agent, dispatcher and local
bridge still share one sandbox security domain; same-domain hostile code is not
made trustworthy by this cache or its signed command channel.

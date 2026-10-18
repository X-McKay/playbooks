# Initial latency measurements

The current prototype adds approximately **20 seconds of active latency across
five model/tool boundaries**, or about **4 seconds per boundary averaged over this
short run**. This is a measured implementation cost, not an inherent Temporal
latency requirement. Fresh ADK processes and many small OpenShell exec exchanges
dominate this experiment.

## Comparison

Measured on 2026-10-17 using the previously verified implementation at `1717557`,
the existing kind cluster, four Colima CPUs and approximately 8 GiB RAM. The
application worker runs on the macOS host; Temporal and OpenShell run in kind;
vLLM remains at `llm.almckay.io`. No production code or image was changed for this
benchmark. Version details are in the [evidence report](evidence.md).

Both modes execute the same report agent: three model calls, one inspect tool and
one report-writing tool. Native ADK uses ordinary function tools and the same
model executor. It runs in a separate OpenShell sandbox with the same image and
filesystem restrictions, using the live profile's network policy. Scripted calls
use no network. The native baseline includes one Python process startup and its
OpenShell exec round trip. Active durable time starts when the first advance is
scheduled and ends when the final advance completes; both exclude provisioning
and deletion.

| Measurement | Native ADK | Durable bridge | Difference |
| --- | --- | --- | --- |
| Scripted, median of 3 runs | 1.93 s | 21.99 s | +20.06 s |
| Scripted, observed range | 1.85–2.54 s | 20.81–22.24 s | — |
| Live vLLM, 1 run per mode | 7.87 s | 30.61 s | +22.74 s |

The scripted comparison isolates bridge overhead without model-service variation.
The live difference also includes inference variability between independent
requests; it is not a precise estimate of infrastructure overhead alone. These
small samples establish scale, not p95/p99 latency, a throughput limit or an SLO.
The arithmetic per-boundary average includes the extra final advance and should
not be extrapolated linearly to arbitrary workloads.

## Session lifecycle and caller-visible time

| Durable measurement | Scripted median (range), 3 runs | Live, 1 run |
| --- | --- | --- |
| Provision Activity | 9.06 s (7.95–10.43 s) | 10.31 s |
| Active agent work | 21.99 s (20.81–22.24 s) | 30.61 s |
| Workflow start to answer-ready milestone | 30.00 s (29.95–32.78 s) | 40.99 s |
| Confirmed deletion Activity | 30.03 s (29.99–30.04 s) | 30.08 s |
| Caller-observed completion, including cleanup | 60.14 s (60.01–62.95 s) | 71.11 s |

The current Workflow returns its result **after cleanup**. The answer-ready row is
an internal history milestone, not an earlier response exposed by the current
API. Provisioning and deletion are separate lifecycle costs; a native deployment
with the same per-session sandbox requirement would also incur them. Medians in
different rows need not sum to the median total.

## Where active time goes

The middle scripted run took 21.99 seconds. Its 28 serial OpenShell exec exchanges
accounted for 21.65 seconds:

| Measured region | Count | Total |
| --- | --- | --- |
| Cold ADK replay/finalization processes | 6 | 13.74 s |
| Prepare/execute control RPC processes | 11 | 4.08 s |
| Candidate artifact download processes | 10 | 3.51 s |
| Initial workspace upload process | 1 | 0.32 s |
| All remaining active work | — | 0.33 s |

These categories come from host-side timers around the unchanged adapter's
`checked_exec` calls. They include identity checks, transport, remote process
execution and response transfer, rather than measuring network transit alone.
The remainder includes validation, local storage work, Workflow transitions and
unobserved gaps. It is **not** an isolated measurement of Temporal overhead.
History schedule-to-start durations are also recorded, but eager dispatch can
make those timestamps unsuitable as a standalone network-latency estimate.

## Reconstruction as history grows

A separate microbenchmark used a static agent alternating model and read-tool
boundaries. Each measurement started a fresh Python process inside OpenShell.
Recorded tool outcomes were injected; the tool body raises if replay executes it.
Each row has three samples. Core time includes parsing the selected prefix and
ADK reconstruction, but excludes imports, fixture-file reads and prefix selection,
OpenShell transport, external artifact transfer and workspace restoration.

| Accepted boundaries | Serialized prefix | Median core wall time | Median core CPU time |
| --- | --- | --- | --- |
| 0 | 2 bytes | 0.68 s | 0.64 s |
| 1 | 9.2 kB | 0.70 s | 0.65 s |
| 8 | 51.7 kB | 0.65 s | 0.61 s |
| 32 | 421.4 kB | 0.85 s | 0.80 s |
| 63, captures boundary 64 | 1.42 MB | 0.89 s | 0.86 s |
| 64, rejects attempted boundary 65 | 1.42 MB | 0.89 s | 0.85 s |

Median library import times by row were 1.20–1.36 seconds. In this small-output
trace, fixed process/ADK setup costs outweighed the additional reconstruction
cost at longer prefixes. Nonmonotonic small differences are sample variability.
Larger model responses, tool outputs and workspaces may behave differently.

This is **not a full 64-boundary Temporal/OpenShell run**. It does not measure
cumulative artifact I/O, workspace cost, payload-limit behavior or loaded-cluster
latency at that length. The broader Gate E qualification remains open.

## Changes worth testing next

1. Reduce exec exchanges by batching bounded artifact transfers and reusing an
   authenticated session transport. Preserve hash verification, payload limits,
   command scope and external acceptance checks.
2. Investigate a warm ADK continuation or reusable replay process within each
   session. Preserve the Workflow's authority to accept progress, gate each next
   effect, and retain cold reconstruction for recovery. State reset, cancellation
   and stale-result behavior must pass the existing conformance/fault suite.
3. Investigate the approximately 30-second deletion wait. Measure process shutdown
   before changing grace periods. An earlier result notification could be a
   separate API feature, but it must not claim confirmed cleanup prematurely.

These are optimization proposals, not implemented performance claims. First
improve the measured process/transport costs, then rerun these comparisons and
the full correctness suite before extracting the wrapper SDK.

## Reproduction and evidence

With the current image loaded and the existing kind setup configured:

```bash
BRIDGE_LATENCY=1 uv run python scripts/kind_test.py benchmarks/test_latency.py -s -x
```

This sends synthetic prompts to the live model. Output goes to
`.state/latency.json`; set `BRIDGE_LATENCY_OUTPUT` to select another path.
The opt-in benchmark lives outside the default test suite and changes no runtime
code. It verified successful five-boundary completion and Temporal history replay
for all four durable runs, native report creation, cold prefix reconstruction,
and boundary-budget rejection. The benchmark passed in **365.71 seconds**.
Final cluster inspection found no session workloads, supervisors or workspace PVCs.

[Raw measurements](../benchmarks/results/kind-local.json) and the
[benchmark harness](../benchmarks/test_latency.py) are committed alongside this
report. The earlier 104-test correctness result still applies to the unchanged
production code; this measurement does not expand its supported agent profile.

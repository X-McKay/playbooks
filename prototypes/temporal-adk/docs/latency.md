# Latency measurements: cold, warm and orderly cleanup

The latest cleanup change reduced median scripted **confirmed deletion from
30.14 to 2.72 seconds**, and **full-session time from 44.96 to 16.24 seconds**.
These are approximately 91% and 64% reductions in small local samples. Active
execution is unchanged in design: it still uses 12 OpenShell exec exchanges and
measured 5.39 seconds, versus 5.51 in the earlier warm run.

The earlier warm implementation reduced active time from 21.99 to 5.51 seconds
by combining continuation reuse and bounded artifact batching. It reduced full
session time from 60.14 to 44.96 seconds but retained direct deletion's roughly
30-second delay. The latest change uses OpenShell's supported stop-before-delete
ordering; it preserves grace periods, policy and immutable deletion confirmation.
See the [cleanup investigation](cleanup.md), [warm contract](warm-execution.md)
and [correctness evidence](evidence.md).

## Latest cleanup rerun

The same unchanged benchmark collected three scripted samples and one live sample
per mode after the full 133-test correctness run. Each durable run used a fresh
sandbox, accepted five boundaries, replayed its Temporal history and completed
exactly 13 Activities without retries. Earlier warm numbers are historical, not
concurrent A/B measurements; load, provisioning and inference variability remain.

| Measurement | Earlier warm path | Warm with orderly cleanup |
| --- | --- | --- |
| Scripted full session, median | 44.96 s | 16.24 s |
| Scripted provision Activity, median | 9.26 s | 7.82 s |
| Scripted active work, median | 5.51 s | 5.39 s |
| Scripted answer-ready milestone, median | 14.85 s | 13.39 s |
| Scripted confirmed deletion Activity, median | 30.14 s | 2.72 s |
| Live full session, one run | 50.43 s | 21.33 s |
| Live provision Activity, one run | 9.20 s | 8.71 s |
| Live active work, one run | 11.07 s | 10.86 s |
| Live answer-ready milestone, one run | 20.35 s | 19.70 s |
| Live confirmed deletion Activity, one run | 29.92 s | 1.54 s |

The three new scripted cleanup samples were 2.862, 2.713 and 2.719 seconds;
full-session times were 16.239, 16.220 and 18.983 seconds. The deletion Activity
includes orderly stop, post-stop revalidation, deletion and confirmation. The
27.42-second reduction between cleanup medians accounts for most of the observed
full-session improvement; the latter also includes provisioning/load variation.
The Workflow still returns only after cleanup. Faster stop is not treated as
proof of deletion, and failure paths retain their longer timeout/reconciliation
behavior.

The new native scripted fresh-exec median was 1.96 seconds, with a 0.65-second
body-only median; native live fresh-exec was 8.09 seconds. As explained below,
these startup scopes differ from durable active time and cannot isolate Temporal
overhead. The native and reconstruction results are retained in the new raw
[cleanup benchmark dataset](../benchmarks/results/kind-cleanup.json). The remaining
sections preserve the earlier cold-to-warm analysis for comparison.

## Environment and comparison method

All three studies ran on 2026-10-17 using the same dedicated kind cluster, macOS arm64
host, four Colima CPUs and approximately 8 GiB RAM. The application worker and
artifact directory run on the host; Temporal and OpenShell run in kind; vLLM
remains at `llm.almckay.io`. Dependency versions are in the evidence report.

The cold baseline is the **earlier measurement** of runtime commit `1717557`,
archived with benchmark commit `4084c86`; it was not rerun concurrently with the
warm version. The warm rerun used the same unchanged benchmark harness and the
new image identified in its raw JSON metadata. The correctness suite finished
before the benchmark began. Background machine/model variability is not controlled.

Each durable sample starts a fresh session sandbox and executes three model calls,
one inspect tool and one report-writing tool. All four warm durable runs completed
five accepted boundaries, passed Temporal history replay and had exactly 13
successful Activity completions with no retries. Native ADK uses ordinary tools
and the same model executor in a separate sandbox with the same image and
filesystem restrictions, using the live profile's network policy. Scripted calls
use no network.

Active durable time starts when the first advance is scheduled and ends when the
final advance completes. It excludes provisioning and deletion. Full-session time
is caller-observed completion and includes cleanup. The native comparison times
one OpenShell exec, including Python/ADK import and response transfer.

The old runtime already imported ADK during provisioning through its demo registry.
Warm execution reuses those resident libraries and removes the additional imports
in six replay processes. Its active interval excludes runtime startup, while the
native fresh-exec interval includes its own startup. Therefore subtracting native
exec time is a useful comparison for this harness, **not a matched steady-state
native comparison or a pure infrastructure-overhead measurement**.

## Full-session and active results

Scripted values are medians of three runs. Live values are one run per version;
independent inference variability is included in their differences.

| Measurement | Earlier cold path | Warm rerun |
| --- | --- | --- |
| Scripted full session, including cleanup | 60.14 s | 44.96 s |
| Scripted provision Activity | 9.06 s | 9.26 s |
| Scripted active work | 21.99 s | 5.51 s |
| Scripted Workflow start to answer-ready milestone | 30.00 s | 14.85 s |
| Scripted confirmed deletion Activity | 30.03 s | 30.14 s |
| Live full session, including cleanup | 71.11 s | 50.43 s |
| Live provision Activity | 10.31 s | 9.20 s |
| Live active work | 30.61 s | 11.07 s |
| Live Workflow start to answer-ready milestone | 40.99 s | 20.35 s |
| Live confirmed deletion Activity | 30.08 s | 29.92 s |

The current Workflow returns **after cleanup**. Answer-ready is an internal history
milestone, not an earlier response exposed by the API. A native deployment requiring
a fresh sandbox per session would also have lifecycle costs; this harness does not
measure a complete native session lifecycle. Medians across rows need not add up.

The individual warm scripted samples, in execution order, were:

| Sample | Active | Full session | Active exec exchanges |
| --- | --- | --- | --- |
| 1 | 5.517 s | 45.690 s | 12 |
| 2 | 5.506 s | 44.965 s | 12 |
| 3 | 5.309 s | 44.842 s | 12 |

The earlier cold active samples ranged from 20.81 to 22.24 seconds and full-session
samples from 60.01 to 62.95 seconds. Every individual timing is retained in the
linked raw datasets. These samples support observations about scale, not p95/p99,
statistical significance, throughput or long-session behavior.

## Native reference and startup accounting

| Measurement | Earlier study | Warm rerun |
| --- | --- | --- |
| Native scripted exec, median of 3 | 1.93 s | 2.51 s |
| Durable scripted active minus native exec medians | 20.06 s | 2.99 s |
| Native scripted body only, median of 3 | 0.69 s | 0.76 s |
| Durable scripted active minus native body medians | 21.30 s | 4.74 s |
| Native live exec, one run | 7.87 s | 7.32 s |
| Durable live active minus native exec | 22.74 s | 3.75 s |

The warm-study native scripted exec samples were 2.513, 2.243 and 2.564 seconds;
the earlier samples were 1.925, 1.854 and 2.545 seconds. The body-only diagnostic
excludes imports and exec transport. Its difference from durable active time
includes those transport costs and is **also not a matched native baseline**.
Neither subtraction isolates Temporal overhead. The live subtraction additionally
contains inference variation; one sample cannot quantify that uncertainty.

## Where active time goes

For the middle scripted run of each study:

| Measured region | Cold count / time | Warm count / time |
| --- | --- | --- |
| Separate ADK replay/finalization execs | 6 / 13.74 s | 0 / 0 s |
| Advance and execute control execs | 11 / 4.08 s | 11 / 4.86 s |
| Candidate artifact download execs | 10 / 3.51 s | 0 / 0 s |
| Initial workspace upload exec | 1 / 0.32 s | 1 / 0.35 s |
| All remaining active work | — / 0.33 s | — / 0.29 s |

All warm durable runs, including live inference, used 12 active exec exchanges.
That count excludes lifecycle calls and the immutable-identity lookup before each
exec; it is not the total network request count. Larger artifacts still require
separate transfers, as verified by the large-checkpoint recovery test.

Timers wrap the adapter's `checked_exec` calls and include identity checks,
transport, process execution and response transfer. The warm control total also
contains ADK continuation work and inline candidate bytes formerly handled by
other execs. It is not a network-transit-only measure. Remaining time includes
validation, storage, Workflow transitions and unobserved gaps. History
schedule-to-start durations are retained, but eager dispatch can make them
unsuitable as standalone network-latency estimates.

## Cold reconstruction as history grows

The unchanged microbenchmark starts a fresh process inside OpenShell and injects
recorded outcomes; the tool body raises if replay executes it. Three samples were
collected at each prefix in both studies. The warm-study rerun measured:

| Accepted boundaries | Serialized prefix | Median core wall | Median core CPU |
| --- | --- | --- | --- |
| 0 | 2 bytes | 0.77 s | 0.72 s |
| 1 | 9.2 kB | 0.64 s | 0.60 s |
| 8 | 51.7 kB | 0.66 s | 0.62 s |
| 32 | 421.4 kB | 0.72 s | 0.68 s |
| 63, captures boundary 64 | 1.42 MB | 1.06 s | 0.92 s |
| 64, rejects attempted boundary 65 | 1.42 MB | 0.88 s | 0.84 s |

Core timing includes prefix parsing and ADK reconstruction, but excludes imports,
fixture-file reads/prefix selection, transport, external artifact transfer and
workspace restoration. Median imports by row were 1.18–1.51 seconds. Nonmonotonic
small differences reflect sample variability. The earlier core wall medians were
0.68, 0.70, 0.65, 0.85, 0.89 and 0.89 seconds at these same prefixes.

This is **not a full 64-boundary Temporal/OpenShell run**. It does not qualify
cumulative artifact I/O, repeated workspace restoration, warm cache memory,
payload-limit behavior or loaded-cluster latency at that length. Gate E's broader
end-to-end qualification remains open.

## Remaining work

Provisioning is now the largest lifecycle cost in the latest samples. Further
startup work, transport reuse and long-session profiling remain possible follow-ups.
An earlier result notification would be a separate API feature and could not
claim confirmed cleanup before deletion finishes. None of these measurements
justify weakening per-boundary acceptance or sandbox isolation.

## Reproduction and evidence

After building/loading the current image and configuring the existing kind setup:

```bash
BRIDGE_LATENCY=1 BRIDGE_LATENCY_OUTPUT=.state/cleanup-latency.json \
  uv run python scripts/kind_test.py benchmarks/test_latency.py -s -x
```

This sends synthetic live-model prompts. The opt-in benchmark lives outside the
default correctness suite and adds only host-side timing observation and sandbox
probes. The latest cleanup benchmark passed in **145.47 seconds**; the earlier
warm benchmark passed in **291.75 seconds**. All session sandboxes
and workspace volumes were removed; shared cluster services remained healthy.

- [Earlier cold measurements](../benchmarks/results/kind-local.json)
- [Warm measurements and image identity](../benchmarks/results/kind-warm.json)
- [Orderly cleanup measurements and image identity](../benchmarks/results/kind-cleanup.json)
- [Cleanup diagnostic observations](../benchmarks/results/cleanup-diagnostics.json)
- [Unchanged benchmark harness](../benchmarks/test_latency.py)

The [evidence report](evidence.md) records 133 passing correctness tests, including
warm recovery and live completion loss. The optimization retains the restricted
cooperative agent profile; it does not qualify the wrapper SDK or production
lease/janitor guarantees.

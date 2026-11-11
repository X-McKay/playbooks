# Fresh sandbox provisioning

The image now compiles trusted Python bytecode during its build. Every session
still creates a new OpenShell sandbox, process, workspace PVC and filesystem.
No running interpreter, session snapshot or writable cache is shared.

## Investigation

Three diagnostic provisions separated the SDK create call, OpenShell readiness
wait and the final runtime-socket check. Kubernetes observations showed fresh
PVCs becoming bound after 2.57–3.75 seconds, followed by the trusted bootstrap
and workspace-init containers. The workload first appeared Running after
6.21–8.34 seconds. SDK creation took 0.28–0.69 seconds, readiness wait 7.05–8.07
seconds, and the subsequent runtime-socket check 0.33–1.54 seconds.

These regions overlap rather than add: PVC/bootstrap work occurs within the SDK
readiness wait. Kubernetes observations include a 0.2-second polling interval
plus command overhead and can perturb timing. The
[diagnostic data](../benchmarks/results/provisioning-diagnostics.json) preserve
the phase measurements and final workload container timestamps.

The pinned OpenShell
[driver](https://github.com/NVIDIA/OpenShell/blob/v0.1.4/crates/openshell-driver-kubernetes/src/driver.rs)
creates a workspace claim and injects both bootstrap containers. Its
[Python SDK](https://github.com/NVIDIA/OpenShell/blob/v0.1.4/python/openshell/sandbox.py)
polls readiness at one-second intervals. Those mechanisms remain intact. The
remaining application startup work included Python source compilation; the
original image lacked bytecode for the bridge, ADK dependencies and standard
library modules sampled by the probe.

## Small implementation change

The Dockerfile uses `uv sync --compile-bytecode` for the installed package and
dependencies, then `compileall` for the Python standard library. This is a
build-time optimization supported by the
[uv Docker guidance](https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode).
Compilation does not execute an agent or bake initialized agent state into the
image. The files live under the existing read-only `/app` and `/usr` policy.

The runtime, ADK bridge, Temporal acceptance, provisioning adapter, readiness
checks, credentials, network rules and confirmed-deletion sequence are unchanged.
The image's `/sandbox` is still seeded into a new volume, and session keys and
identities are supplied separately for each creation.

## Interleaved comparison

The comparison alternated baseline and candidate images, reversing order between
pairs. It provisioned ten fresh sandboxes: three scripted and two vLLM-profile
sessions per image. No inference was issued. Images were already present on the
kind node. All ten immutable sandbox IDs were different and every session was
confirmed deleted. The benchmark passed in **128.53 seconds**.

| Median measurement | Baseline | Precompiled image |
| --- | --- | --- |
| Scripted provisioning, 3 samples each | 9.77 s | 8.36 s |
| Scripted runtime-socket check | 0.93 s | 0.34 s |
| vLLM-profile provisioning, 2 samples each | 8.88 s | 8.30 s |
| vLLM-profile runtime-socket check | 0.58 s | 0.39 s |
| Separate runtime-module import, scripted sessions | 1.62 s | 0.55 s |
| Separate runtime-module import, vLLM sessions | 1.30 s | 0.53 s |

The observed total reductions were about **14.5% scripted** and **6.5% vLLM
profile**. These small interleaved samples reduce ordering bias but do not
establish significance or an SLO. PVC, scheduling and readiness-poll variation
also affect totals; their differences must not be attributed to faster Python
compilation. The import diagnostic starts a separate process after provisioning
and times importing `bridge_probe.runtime`. It excludes interpreter startup and
does not instantiate the live model executor or measure the actual main runtime
startup. It is supporting evidence, not the provisioning result.

Full SDK phase timings, individual samples, unchanged policy hashes and exact
image identities are in the
[A/B dataset](../benchmarks/results/kind-provisioning-ab.json). The final image
has the same runtime configuration and filesystem layers as the candidate; its
manifest ID differs because it was rebuilt from the committed Dockerfile.

## Cost and isolation qualification

Docker-reported image size increased from **145.36 MB to 180.08 MB**, about
34.72 MB or 24%. The candidate build spent 6.46 seconds compiling dependency
bytecode and 2.7 seconds on the standard-library compilation step. Full build
time and cold image-pull latency are not measured by the provisioning comparison;
the larger image can offset startup savings on an uncached node.

The new cluster regression keeps two sessions alive simultaneously. It checks
empty workspace/artifact directories and absent workspace/tmp markers, distinct
sandbox IDs, workload pod UIDs, PVC UIDs and bound PV names. Each session writes
its own marker. Retrying provision for that same session retains its ID and
marker. The agent can read prebuilt bytecode but cannot open it for writing.
Both sessions still require confirmed cleanup. This test provisions the sessions
sequentially; it does not qualify simultaneous creation races.

Fresh PVC creation and OpenShell bootstrap remain the dominant startup floor.
Further reductions would need separate storage/controller or upstream startup
work. This change does not remove readiness checks, change the storage class,
patch trusted bootstrap code or introduce a sandbox pool. Production distributed
lifecycle leases and hostile-process guarantees remain outside the prototype.

## Reproduction

Keep the old image under a separate tag before building/loading the current one.
Both images must be available to the existing kind node:

```bash
BRIDGE_PROVISIONING=1 \
BRIDGE_PROVISION_BASELINE_IMAGE=adk-bridge-probe:before-bytecode \
  uv run python scripts/kind_test.py benchmarks/test_provisioning.py -s -x
```

The opt-in comparison is separate from the normal correctness suite and the
unchanged [end-to-end latency benchmark](../benchmarks/test_latency.py). Full
recovery/live-model qualification and end-to-end measurements are recorded in
the [evidence](evidence.md) and [latency](latency.md) reports.

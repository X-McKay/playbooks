# Prototype evidence and remaining gates

This report records the implementation experiment on 2026-10-17. It qualifies a
restricted scripted profile, not arbitrary ADK agents or a production SDK.
The reproducible commands are in the [README](../README.md).

## Tested topology

An external Python Temporal worker connects through localhost port-forwards to a
dedicated `adk-bridge-probe` kind cluster. Temporal's frontend, history, matching
and worker services, PostgreSQL, OpenShell gateway, Agent Sandbox controller and
Cilium run inside that cluster. Every agent session receives its own OpenShell
workload and workspace volume. The agent image contains no Temporal credentials
or Activity tokens. The test worker and immutable artifact directory remain on
the host; this is not yet an all-components Kubernetes deployment.

| Component | Tested version |
| --- | --- |
| Python | 3.12.14 |
| Google ADK / Google Gen AI | 2.12.0 / 2.31.0 |
| Temporal Python SDK | 1.34.0 |
| OpenShell Python SDK / chart | 0.1.4 / 0.1.4 |
| kind / Kubernetes node | 0.31.0 / 1.35.0 |
| Cilium | 1.20.3 |
| Agent Sandbox controller | 1.0.7 |
| Temporal chart / server | 1.7.0 / 1.32.0 |
| PostgreSQL | 17.6 |

`uv.lock` pins the Python graph. Deployment manifests pin component versions;
the setup script verifies downloaded controller and Temporal chart checksums.
Images and OCI charts still use version tags, not universally immutable digests.
The tested host uses macOS arm64, Colima, four CPUs and approximately 8 GiB RAM.

## Evidence matrix

Final consolidated run: **87 passed, zero failed, zero skipped**, in 506.74 seconds
(8 minutes 26 seconds), against the rebuilt image and real kind services. One
upstream ADK experimental function-schema warning remains visible. The preceding
83-test run also passed before the final lifecycle regressions were added.

Ruff lint and formatting checks pass for all 50 Python files; shell syntax checks
pass. `nix develop --command just check` passes: 87 Markdown files, no lint issues,
and no broken relative links or anchors. The default checkout test runner was
also verified against its ignored `.state` configuration.

After the sandbox suite, the OpenShell namespace contained only its shared
gateway pod and gateway data PVC: no session workloads, supervisor pods or
workspace PVCs remained. Temporal and PostgreSQL stayed healthy. Temporary manual
port-forwards were stopped. The dedicated kind cluster remains available.

| Area | Executed checks |
| --- | --- |
| ADK conformance | Native traces versus cold prefix reconstruction; 120 fresh process reconstructions; callbacks and error/mutation branches; lossless values and field presence; unsupported profile rejection; finalizer timeout and process cleanup |
| Accepted progress | Immutable tape references, descriptor mismatch, candidate versus committed position, mutable alias protection, restored workspace, uncertain external effects |
| Temporal | Real server history replay, accepted-result worker restart, SIGKILL of a worker process, completion-loss windows, heartbeat timeout, cancellation, receipt substitution rejection |
| OpenShell | Real mTLS, mandatory Landlock, non-root execution, allowed workspace access, denied outside paths, denied network destinations, distinct agent policy, stale sandbox identity |
| Session recovery | Five accepted model/tool boundaries, cold generation replacement with a checkpoint larger than 1 MiB, terminal cancellation and hard-termination reconciliation |
| Lifecycle regression | Failed replacement readiness, cancellation during creation, delayed lookup after terminal cleanup, immutable deletion acknowledgement reconciliation |

## Initial observed timing

One real five-boundary cold-replacement history measured the following Activity
start-to-completion times. This is a single local observation, not a latency SLO;
it excludes queue delay, failed attempts and intentional test pauses.

| Activity | Observed seconds |
| --- | --- |
| Advance, six successful calls | 2.02–7.15 |
| Model execution, three calls | 1.09–1.29 |
| Tool execution, two calls | 0.79–0.98 |
| Initial provision | 9.91 |
| Replacement provision | 7.52 |
| Terminal deletion | 30.03 |

The model is scripted, so these timings contain no live inference cost. The
longer test-suite wall time includes repeated cold ADK processes, intentional
fault windows and Kubernetes termination grace periods.

## Findings that changed the implementation

- Full Pydantic values and field-set masks are required. `exclude_unset` loses ADK
  events appended to default lists.
- Replay runs through OpenShell's supervisor exec API. Its seccomp policy denies
  workload `killpg`; weakening that policy to accommodate the local harness would
  change the isolation assumptions.
- OpenShell's gRPC request limit requires artifact chunking. Uploads use 128 KiB
  chunks with final hash verification; control messages remain separately bounded.
- Temporal's actual converted payload size matters. Non-ASCII JSON can expand
  under its default converter even when canonical UTF-8 bytes fit the limit.
- Workspace validation must happen before accepting an Activity result, including
  all implicit parent paths and component limits. Snapshot reads alter access
  time, so the content-stability check excludes atime.
- A claimed receipt predecessor is insufficient: acceptance verifies the actual
  linked node, operation, checkpoint bytes and restore schema.
- Creation can finish after cancellation of a Python `to_thread` await. Lifecycle
  creation is tracked and settled; normal Activity cancellation waits for handler
  completion. Terminal cleanup fences further creation in that adapter and scans
  every generation owned by the session, including unaccepted replacements.
- Kubernetes deletion can outlive the SDK's acknowledgement timeout. The adapter
  confirms immutable instance removal before permitting replacement or reporting
  `DELETED`.

## Explicit limitations and plan refinements

The implementation has no independent durability engine. Temporal history selects
accepted progress; hash-addressed files hold data only. The local artifact store
fsyncs files and their directory, but this is not a replicated object store or a
host-power-loss qualification. Retaining those files is required for recovery.

The supported profile is one static serial agent, one invocation, a scripted
model, and cooperative registered tools. Model and tool execution share their
sandbox's security domain. The bridge is not tamper-proof against arbitrary
Python inside that domain. Background-process spawning tools are excluded;
per-boundary descendant quiescence still needs a separate qualification.

Cleanup tests invoke the external reconciler explicitly. A production janitor,
independent lease/fencing across worker hosts, and a workload identity/credential
broker are not implemented. A worker that dies during creation or a hard
termination concurrent with a remote RPC requires repeated reconciliation; the
in-process terminal fence alone does not close cross-process races.

The plan proposed a 30-second advance deadline and a 30-minute active invocation
limit. This experiment uses a 40-second supervisor exec limit and a 45-second
Activity start-to-close limit, with longer lifecycle deadlines. The test callers
supply bounded Workflow execution timeouts; there is no production admission API
enforcing the global invocation limit. No 64-boundary latency distribution has
been measured, so Gate E's latency requirement remains open.

Live-provider credentials have not been used. A selected live model, sanitized
provider fixture, provider retry accounting, and its conformance rerun remain
Gate E work. The wrapper SDK and second-agent template (Gate F) remain deferred.
No upstream Temporal or ADK code is forked or vendored. The narrow compatibility
surface and shared tests make future upstream seam changes reviewable.

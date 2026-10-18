# Prototype evidence and remaining gates

This report records the implementation experiment on 2026-10-17. It qualifies
restricted scripted and live vLLM profiles, not arbitrary ADK agents or a
production SDK.
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
| LiteLLM / OpenAI client | 1.95.0 / 2.54.0 |
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

## Initial cold-path evidence matrix

Initial scripted-only consolidated run: **87 passed, zero failed, zero skipped**, in 506.74 seconds
(8 minutes 26 seconds), against the rebuilt image and real kind services. One
upstream ADK experimental function-schema warning remains visible. The preceding
83-test run also passed before the final lifecycle regressions were added.

At that checkpoint, Ruff lint and formatting checks passed for all 50 Python files; shell syntax checks
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

## Initial live vLLM qualification

The live profile selects `openai/Qwen3.6-35B-A3B-NVFP4` through ADK's official
LiteLlm adapter, with API base `https://llm.almckay.io/v1`. The provider client
executes inside the session sandbox; Temporal remains the only owner of accepted
progress. No provider secret was required by the endpoint during these synthetic
tests. Inference hosting itself remains outside kind.

The final normal and cold-replacement cases completed with five accepted
boundaries each: model, inspect tool, model, report tool, model. They reported
1,526 and 1,530 total tokens respectively. Output prose was not required to match
between independent live runs. Each case verified report contents, accepted
response serialization, Temporal history replay, and `DELETED` cleanup.

The response from the initial normal case is committed as
`tests/fixtures/vllm_recording.json`. It contains synthetic inputs and results,
not repository secrets or credentials. Every recorded prefix reconstructs in a
fresh process with the same next descriptor; the full tape returns the recorded
answer without running `write_report` or calling inference.

Provider HTTP fixtures independently test call identities, token metadata,
nonstreaming/single-call controls, malformed JSON, unknown tools, truncated
responses, and retries. Real HTTP 429 and 500 fixtures produce exactly one request
with LiteLLM and OpenAI retries disabled. Generation and transport overrides are
rejected before inference. Client telemetry is disabled and the packaged model
cost map is used; no extra model-service egress is granted.

The sandbox policy allows the Python executable to make only
`POST /v1/chat/completions` to `llm.almckay.io:443`. Tests require HTTP 403
for another path and the wrong method. OpenShell transparent networking rejects
an unapproved hostname before HTTP: the live probe receives a connection error
and must also find `transparent_tcp_policy_denied` for `example.com:443` in that
immutable sandbox instance's trusted supervisor log. A generic connection failure
alone does not count as proof of enforcement. This distinction was found when
tightening the test after independent review; the initial assumption that every
denial would produce HTTP 403 was incorrect.

The live completion-loss case removes the first model's completion after real
inference and candidate upload, before Temporal accepts it. It requires
`OUTCOME_UNKNOWN`, zero accepted boundaries, exactly one model dispatch, and
confirmed cleanup. The artifact candidate never becomes an implicit commit.
Token usage from accepted responses is evidence, not a total GPU-cost accounting
system; inference whose completion is lost can still consume compute.

Final verification covered **104 distinct tests**, split into two successful runs:

| Run | Result | Duration |
| --- | --- | --- |
| Complete regression suite excluding the three opt-in live cases | 101 passed | 496.05 seconds |
| Live normal, replacement and completion-loss cases | 3 passed | 240.22 seconds |

Neither run skipped tests or reported failures. The regression run emitted one
upstream ADK experimental function-schema warning. Both used the final integrated
image and real kind services. Ruff lint and format checks passed for all 54 Python
files; shell syntax and repository Markdown/link checks passed. The final cluster
inspection found only the shared OpenShell gateway pod and its data PVC; no
session workloads, supervisors or workspace PVCs remained. Temporal and
PostgreSQL were healthy. Test-owned port-forwards were stopped by the runner.

The two verification commands were:

```bash
uv run python scripts/kind_test.py tests --ignore=tests/sandbox/test_live.py -x
BRIDGE_LIVE_VLLM=1 BRIDGE_LIVE_EVIDENCE_DIR=.state/live-final \
  uv run python scripts/kind_test.py tests/sandbox/test_live.py -x
```

The subsequent [latency study](latency.md) compares native ADK and the durable
path, separates lifecycle costs, and measures core reconstruction through the
64-boundary budget. It does not close the full end-to-end latency gate.

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
- The initial cold path used OpenShell's supervisor exec API because its seccomp
  policy denies workload `killpg`. The warm follow-up removes that per-advance
  replay process; it retains the same seccomp policy and official exec transport.
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

## Warm-path qualification

The [warm execution amendment](warm-execution.md) keeps ADK parked at each
boundary and resumes only when a subsequent signed advance selects the exact
Temporal-accepted candidate. A missing or discontinuous cache reconstructs cold.
Inline candidate objects have a 128 KiB raw-byte budget; the worker verifies
hashes and receipt/checkpoint semantics before acceptance. Large checkpoints use
the original transfer path. The policy, Temporal credentials and one-attempt
execute contract are unchanged.

Independent review found three shutdown hazards, each reproduced by a failing
regression before correction: caller cancellation could leave a reusable live
finalizer; runtime shutdown lacked a terminal command fence; acquiring the
command lock before cancelling execution could deadlock cleanup. The final
implementation fences before yielding, permanently poisons interrupted warm
cleanup, rejects commands after runtime shutdown begins, and cancels admitted
executors before waiting for their command lock. The reviewer then independently
passed all 17 focused warm/runtime/inline tests with no remaining blockers.

The cluster worker-restart case stops and recreates both the Temporal application
Worker and its host OpenShell adapter. The sandbox remains the same immutable
instance and resumes from the Workflow-selected position with empty host caches.
This is distinct from the existing SIGKILL worker test and the cold sandbox
replacement case, which requires deletion and a new generation.

The new `vllm_warm_recording.json` stores synthetic accepted responses from a
real warm run. Both original and warm recordings pass every-prefix fresh-process
reconstruction and warm continuation with cache loss: four provider-recording
tests passed in 11.87 seconds, with no inference or tool-body execution.

The full real-kind suite passed **122 tests in 741.20 seconds**, with zero
failures or skips and one upstream ADK experimental warning. It included live
normal, replacement and completion-loss cases, unchanged policy enforcement,
large-checkpoint cold replacement, the new worker/adapter restart, Temporal
history replay, cancellation and terminal reconciliation. The two newly added
warm-recording parameter cases were verified in the four-case provider run
above, giving **124 distinct correctness tests** on the final implementation.
The recording check ran alongside the latter part of the full suite; it did not
send inference or modify the sandbox image.

The live normal and replacement runs each reported 1,525 accepted-response tokens,
five accepted boundaries and `DELETED` cleanup. The live completion-loss case
still required exactly one model dispatch, zero accepted boundaries and
`OUTCOME_UNKNOWN` before confirmed cleanup.

```bash
BRIDGE_LIVE_VLLM=1 BRIDGE_LIVE_EVIDENCE_DIR=.state/warm-live \
  uv run python scripts/kind_test.py tests -x
uv run pytest tests/provider/test_recorded_vllm.py -q
```

The current checkout collects 124 tests. A subsequent full run includes both
recordings automatically. The unchanged latency benchmark separately passed in
291.75 seconds. Scripted median full-session time fell from 60.14 to 44.96 seconds,
active time from 21.99 to 5.51 seconds, and active exec exchanges from 28 to 12.
The [latency report](latency.md) includes lifecycle accounting, native-startup
scope differences, raw samples and the single live comparison.

## Explicit limitations and plan refinements

The implementation has no independent durability engine. Temporal history selects
accepted progress; hash-addressed files hold data only. The local artifact store
fsyncs files and their directory, but this is not a replicated object store or a
host-power-loss qualification. Retaining those files is required for recovery.

The supported profile is one static serial agent, one invocation, a scripted or
pinned live vLLM model, and cooperative registered tools. Model and tool execution
share their sandbox's security domain. The bridge is not tamper-proof against arbitrary
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

The live provider, sanitized recording and retry checks are now implemented.
Gate E still requires the full 64-boundary latency qualification; production
cleanup/lease hardening also remains outside this experiment. The wrapper SDK and
second-agent template (Gate F) remain deferred.
No upstream Temporal or ADK code is forked or vendored. The narrow compatibility
surface and shared tests make future upstream seam changes reviewable.

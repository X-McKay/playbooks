# Temporal ADK OpenShell Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task after an execution approach is selected. Steps use checkboxes for tracking. This document plans the work; it does not authorize starting implementation.

**Goal:** Prove that a restricted ADK agent can execute inside one disposable session sandbox, recover at committed model/tool boundaries under external Temporal ownership, and support a small reusable authoring interface.

**Architecture:** A fresh ADK subprocess reconstructs the invocation on every advance, injecting recorded outcomes until it describes the next operation. A dispatcher executes that pinned descriptor; an external Activity validates the outcome and writes an immutable tape node. Temporal accepts the new tape head before another advance can consume it.

**Tech Stack:** Python, pinned Google ADK, pytest and pytest-asyncio, Pydantic wire records, Temporal Python SDK/test server, one immutable artifact store, and one pinned OpenShell deployment. Use scripted model responses until the infrastructure and recovery gates pass.

**Spec:** [Temporal bridge specification v0.2](https://chatgpt.com/space/page_ef1eb115223c8191a7289f2401b6be3e), especially Required invariants, Runner implementation, Reconstruction algorithm, and Validation and acceptance. The local companion is `temporal-adk-openshell-bridge-spec.md`.

The smallest useful result is a single-session demonstration with measured recovery evidence, not a general SDK. Phases 1–5 build that result. Phase 6 extracts only the interfaces that the demonstration proves are worth sharing. Each phase has a stop condition; infrastructure work must not conceal an ADK conformance failure.

## Implementation status

The implemented slice and measured deviations are recorded in the
[evidence report](evidence.md). Tasks 1–9 have a restricted scripted implementation
and fault tests; the full production cleanup and hostile-process guarantees are
not claimed. Task 10 now includes the selected local vLLM integration and live/recovery tests;
its full 64-boundary latency qualification remains open. An initial
[native-versus-durable latency study](latency.md), including core replay growth,
is now available. Task 11 remains deferred until
the remaining results justify SDK extraction.
The checklist below preserves the proposed plan rather than implying every gate
has been satisfied.

## Global constraints

- The spec's reference ADK version is `google-adk==2.12.0`; its OpenShell documentation baseline is `0.1.4`. Resolve exact compatible runtime and transitive versions into a lock before testing. These baselines are not a claim that the combination already works.
- One Python `LlmAgent`; no sub-agent delegation or `AgentTool`.
- Non-streaming, complete responses through a bridge `BaseLlm` wrapper.
- At most one function call per model response and one effect-bearing operation executing per session.
- The sandbox receives no Temporal client identity or Activity task token.
- A committed result is never intentionally re-executed by reconstruction.
- A request mismatch during reconstruction halts the invocation.
- Temporal is the sole authority for committed progress. Artifact storage holds immutable bytes; it does not select progress.
- Fresh reconstruction on every advance; no persistent parked ADK continuation.
- Tool context is a read-only serializable projection; supported state updates occur in deterministic callbacks after recorded-result injection.
- Native `code_executor`, native resumability, dynamic toolsets, custom plugins/planners, streaming, compaction, context caching, and callback result overrides are rejected.
- Execute Activities use `maximum_attempts=1`; the Workflow makes explicit retry/recovery decisions.
- Prototype limits retain the spec's 64 boundaries, 64 KiB inline request/result, 8 MiB serialized tape, 256 MiB expanded workspace, 30-minute active invocation limit, and 30-second advance deadline. These are application limits, not vendor limits.
- No real external write tools, arbitrary shell tools, secrets in fixtures, or production tenants are needed for the first demonstration.

## Review focus

These cross-cutting cases have explicit tests below rather than relying on a happy-path demonstration.

1. ADK cleanup runs after boundary capture or final response: no premature finalization, effect execution, or surviving replay process. Task 3 owns this.
2. A recorded result or argument is mutated through an alias: committed bytes and the approved execution request remain unchanged. Tasks 1 and 4 own this.
3. A tool writes files and then fails: the accepted error must retain a matching checkpoint or a verified rollback. Task 5 owns this.
4. An old execute attempt resumes after timeout: replacement authority cannot create overlapping writers or accept a stale result. Tasks 6 and 7 own this.
5. Creation/deletion acknowledgement is lost or Temporal is unavailable during cleanup: reconcile immutable resource identity; do not delete an active or unrelated session. Task 8 owns this.

## Phases and decision gates

| Phase | Deliverable | Required evidence | Proceed only if |
| --- | --- | --- | --- |
| 1 ADK conformance | Native reference run plus bridge reconstruction harness | Prefix equivalence, cleanup and admission reports | Supported ADK behavior is reproducible without effect bodies during advance |
| 2 Recovery substrate | Canonical dispatcher, linked tape, workspace restore | Duplicate delivery and crash-window tests | A recovery position is complete and uncertainty stays explicit |
| 3 Temporal vertical slice | External worker and one-invocation Workflow | Real history, worker restart and completion-loss tests | History alone selects accepted progress |
| 4 OpenShell session | One disposable sandbox with a static approved policy | Actual policy denials, replacement and cleanup | Isolation and lifecycle work in the chosen deployment |
| 5 Smallest end-to-end demonstration | One live read/report agent and reproducible fault run | Real provider roundtrip, recovery, cost/latency report | The supported profile is useful and its costs are acceptable |
| 6 Minimal SDK extraction | Shared library plus two small example agents | Same contract suite against both examples | Shared code removes demonstrated duplication without expanding semantics |

The first implementation assignment should be Phase 1 only. Keep all subsequent phases blocked until its gate report is reviewed. Phase 2 is the next smallest independently useful body of work. SDK extraction is a separate decision after Phase 5, not a prerequisite for the prototype.

### Explicit scope reductions

The prototype implements one user invocation per session and closes the sandbox after final export. It does not implement queued follow-up messages, idle-session reuse, approval UI, approval-required tools, external-write reconciliation adapters, Continue-as-New, historical migrations, or a general operator resolution API. Reject unsupported starts and tools rather than exposing placeholder behavior. Unknown effects stop the run, revoke execution authority, and trigger cleanup with retained diagnostic evidence; they do not silently continue.

Use one artifact backend, one model adapter, one transport and one reviewed OpenShell policy template. A test-only filesystem artifact store is sufficient before the container stage; the OpenShell stage selects one externally hosted store reachable through a scoped artifact channel. No progress database, lease service, generic policy compiler, dynamic plugin system, public package, or multi-repository rollout is required.

Phases 1–3 execute only trusted synthetic fixtures in disposable local processes. They make no sandbox-isolation claim and must not run unfamiliar repository code. For the demonstration, use synthetic data: stop compute and delete the session workspace at termination; delete temporary replay/checkpoint objects after final export and cleanup verification. Keep final outputs and curated diagnostic evidence until explicit demo teardown. Local Temporal histories remain until test-environment teardown. A blocked unknown effect retains its diagnostic record but does not require keeping executable sandbox compute alive.

The full spec's production acceptance remains broader: multi-invocation lifecycle, authenticated approvals/resolutions, retention administration, deployment version routing, and broader operational hardening remain later work. This prototype must not be presented as satisfying those omitted features.

## Repository and interfaces

All paths below are proposed paths in a new implementation repository. They are not files that already exist. Introduce each file when its task needs it; do not scaffold every layer in advance.

```text
adk-bridge-prototype/
  pyproject.toml
  uv.lock
  README.md
  src/bridge_probe/
    records.py          # wire types, canonicalization, limits
    adk_compat.py       # all version-specific ADK access
    capture.py          # model/tool wrappers and replay subprocess
    dispatch.py         # direct registry execution and volatile deduplication
    artifacts.py        # immutable tape nodes and bounded reads
    workspace.py        # quiescent capture and safe restore
    temporal.py         # session Workflow and external Activities
    transport.py        # authenticated RPC and scoped artifact transfer
    openshell.py        # one lifecycle/policy adapter
    demo.py             # explicit prototype start/report entrypoint
  tests/
    fixtures/           # scripted model corpus and trusted sample agent
    conformance/
    recovery/
    temporal/
    sandbox/
    acceptance/
  reports/              # generated evidence, ignored unless curated
```

Use the spec's `Binding`, `Operation`, `Outcome`, `ArtifactRef`, `Position`, `AdvanceRequest`, `AdvanceResponse`, and `ExecuteReceipt` records. Define them once in `records.py`. Missing fields or cross-field validators in illustrative spec snippets must be completed, not inferred away. A `FixtureCase` contains the frozen base session, new input, manifest, approved fixture registry and scripted outcomes. A `ReferenceRun` contains canonical descriptors/outcomes, final response/session, and callback trace. These test-only types live in `tests/fixtures/cases.py`.

The initial internal interfaces are:

```python
# Proposed signatures. Their bodies are delivered by the tasks below.
def canonical_bytes(value: object) -> bytes: ...
def validate_profile(agent, app_config, run_config) -> None: ...
async def advance(request: AdvanceRequest) -> AdvanceResponse: ...
async def execute(command: ExecuteCommand) -> Outcome: ...
async def append_candidate(previous: Position,
                           operation: Operation,
                           outcome: Outcome) -> ExecuteReceipt: ...
async def load_tape(position: Position) -> tuple[TapeNode, ...]: ...
async def capture_workspace(root: Path,
                            previous: ArtifactRef) -> ArtifactRef: ...
async def restore_workspace(ref: ArtifactRef, empty_root: Path) -> None: ...
```

`ExecuteCommand` contains the current Binding, pinned Operation, previous Position, dispatch attempt ID, scoped permit and deadline. The registry, artifact store and workspace roots are injected into service construction, not chosen by untrusted command fields. Application authorization and artifact-reference validation are not delegated to ADK.

## Phase 1 ADK conformance before infrastructure

### Task 1 Pin the runtime and establish an independent native reference

**Files:** Create `pyproject.toml`, `uv.lock`, `src/bridge_probe/records.py`, `src/bridge_probe/adk_compat.py`, `tests/fixtures/cases.py`, `tests/fixtures/scripted_model.py`, `tests/conformance/test_reference.py`, and `tests/conformance/test_serialization.py`.

**Interfaces:** Produce `run_native_reference(case: FixtureCase) -> ReferenceRun` and `canonical_bytes(value: object) -> bytes`. The native reference uses ordinary ADK execution with scripted model responses and fixture tools, not the bridge's replay implementation. The shared serializer may be reused; independently authored expected fields and trace assertions prevent the test from validating only itself.

- [ ] Write failing tests for a five-boundary fixture: model requests `inspect_repository`, tool returns a fixed file list, model requests `write_report`, tool returns report metadata, model returns final text. Assert exactly three model bodies, two tool bodies, the expected callback sequence, state keys, event content and one occurrence of the new user message.
- [ ] Add roundtrip tests for text, one function call, function response, stable function-call IDs, usage/finish fields, approved provider continuation metadata, binary/reference payloads where supported, and a known business error. Assert semantic field equality and canonical-byte stability; reject unsupported values and NaN/infinity explicitly.
- [ ] Run `uv run pytest tests/conformance/test_reference.py tests/conformance/test_serialization.py -q`; verify failures identify missing behavior, rather than an unavailable dependency or bad fixture.
- [ ] Resolve the exact dependency lock, implement the minimal reference harness and serializer, and record versions/source seams in `reports/environment.json`. Preserve meaningful absence/null distinctions and deep-copy decoded values.
- [ ] Inspect the official Temporal ADK integration's existing serializers, read-only context contracts and tests for reuse. Record what is reused and what the bridge must own in `reports/compatibility.md`; isolate any version-specific seam in `adk_compat.py`. Do not assume its Workflow-bound wrappers preserve durable scheduling when called from an ordinary remote process. An upstream contribution is optional; no fork or maintainer acceptance is needed for this gate.
- [ ] Rerun the tests and commit the passing harness with its lock. Keep generated secrets and real transcripts out of the commit.

**Gate evidence:** A deterministic native reference trace and explicit supported field corpus. If the intended provider shape cannot be represented without semantic loss, stop and narrow the profile or revise serialization before implementing capture. Use one synthetic provider-specific fixture initially and replace/augment it with a sanitized real sample in Phase 5.

### Task 2 Capture boundaries and reconstruct every committed prefix

**Files:** Create `src/bridge_probe/capture.py`, `tests/conformance/test_prefix_reconstruction.py`, and `tests/conformance/test_pending_descriptor.py`; modify `adk_compat.py` and `records.py`.

**Interfaces:** Consume `FixtureCase` and `ReferenceRun`; produce `advance(AdvanceRequest) -> AdvanceResponse`. A test-only in-memory tape provider supplies accepted prefixes until the real linked store arrives in Task 4. It is not a production durability mechanism.

- [ ] Write failing tests that reconstruct the reference case from prefixes 0 through 5 in a new subprocess each time. At prefix k below 5, assert the next canonical Operation equals reference operation k. At prefix 5, assert the final response and serialized final session equal the reference result. Parameterize the same prefix-equivalence check over a known business-error branch and a callback-state mutation branch, comparing their native ADK callback/error behavior and final state. Unsupported native exception semantics must fail admission rather than being approximated by a different tool response.
- [ ] Assert every advance invokes zero model/tool effect bodies. Use parent-observed counters or fixture executor probes independent of the bridge's own logging. Compare callback trace only through the captured boundary; cancellation cleanup is tested separately. For full reconstruction, compare the complete trace. Do not sum callback executions across repeated reconstructions and mistake them for external effects.
- [ ] Add tests for the same arguments at different positions producing different operation IDs, changed requests/context/manifest at the same position rejecting before dispatch, premature termination, and a changed pending descriptor after recovery. Require exact pending-request comparison, not cursor equality.
- [ ] Run `uv run pytest tests/conformance/test_prefix_reconstruction.py tests/conformance/test_pending_descriptor.py -q` and confirm the intended failures.
- [ ] Implement bridge model/tool wrappers, deterministic runtime installation, base-session reconstruction, and first-unrecorded-boundary capture. Instantiate fresh objects and deterministic providers before factory construction. Do not execute a captured closure; publish only canonical data.
- [ ] Rerun the tests across fresh process launches, then commit. Keep exact event IDs/timestamps in comparisons where the contract requires them; do not make tests pass by stripping nondeterministic fields that affect future execution.

**Required assertion pattern:** The future harness should make the following relationship explicit; the helper names are proposed test APIs.

```python
reference = await run_native_reference(case)
for cursor in range(len(reference.operations) + 1):
    request = case.request_with_prefix(reference, cursor)
    observed = await advance_in_fresh_process(request)
    assert observed.effect_body_calls == 0
    assert observed.replay_process_exited
    if cursor < len(reference.operations):
        assert observed.operation_bytes == reference.operation_bytes[cursor]
    else:
        assert observed.final_session_bytes == reference.final_session_bytes
        assert observed.final_response_bytes == reference.final_response_bytes
```

Task 2 defines `advance_in_fresh_process` in its test harness; the returned `observed` includes parent-observed process/effect evidence in addition to the wire response. Those diagnostic fields are not added to the production protocol.

### Task 3 Prove cleanup and enforce the closed ADK profile

**Files:** Modify `capture.py` and `adk_compat.py`; create `tests/conformance/test_cleanup.py`, `test_admission.py`, and `test_determinism.py`.

**Interfaces:** Produce `validate_profile(agent, app_config, run_config) -> None`; retain Task 2's advance signature. All private/version-specific ADK access stays in `adk_compat.py`.

- [ ] Add failing tests for final-response emission followed by callback work, cancellation at a captured boundary, cancellation while consuming recorded outcomes, a hung cleanup hook, and a lost client connection. Assert done is emitted only after iterator exhaustion; cancelled state is discarded; no executor runs; the parent confirms subprocess exit before reporting a successful capture. A failed termination check must fail the advance.
- [ ] Add admission tests rejecting native CodeExecutor, resumability, plugins/planners, dynamic tools, mutable state access by tools, synthetic callback return values, streaming and two function calls in one response. For multi-call output, assert zero tools execute. Runtime checks catch prohibited callback results; configuration checks alone cannot prove arbitrary Python purity.
- [ ] Add tests that effect execution's time/random/UUID use cannot consume the reconstruction streams, callback mutation cannot alter stored outcomes, and the same request reconstructs identically in fresh processes with different host times and hash seeds.
- [ ] Run `uv run pytest tests/conformance -q` and inspect failures. Use instrumented fixture finalizers; do not rely only on ordinary successful examples.
- [ ] Implement bounded queue/Future capture, cancel-and-await, iterator/Runner closure and parent-owned subprocess termination. Add strict feature validation and deep-copy boundaries. Keep all side-effecting work outside advance.
- [ ] Rerun the full conformance suite and commit with `reports/conformance.md`: exact versions, supported fields/features, test counts, failures, private API dependencies and measured reconstruction times.

**Gate A:** All required conformance tests pass with no skipped critical cases. Repeat the deterministic prefix suite in 20 fresh launches without divergence; this is a proposed repeatability check, not a statistical correctness proof. No unknown semantic field may be discarded merely to obtain equality. If determinism, callback order or lifecycle cannot be preserved through a small compatibility module, stop: narrow the profile, propose an upstream seam, or reconsider Runner placement. Do not compensate by adding Temporal or SDK abstractions.

## Phase 2 Complete the recovery substrate

### Task 4 Execute canonical descriptors and persist immutable tape nodes

**Files:** Create `dispatch.py`, `artifacts.py`, `tests/recovery/test_dispatch.py`, and `tests/recovery/test_tape.py`; modify `records.py` and adapt `capture.py` to `load_tape`.

**Interfaces:** Produce `execute(ExecuteCommand) -> Outcome`, `append_candidate(Position, Operation, Outcome) -> ExecuteReceipt`, and `load_tape(Position) -> tuple[TapeNode, ...]`. A test coordinator supplies an accepted head explicitly; it never infers a head from storage contents.

- [ ] Write failing tests for duplicate execute delivery attaching to the same in-flight Task/candidate, changed request bytes under the same ID being rejected, and mutation of a caller-owned dictionary after hashing having no effect on executed arguments.
- [ ] Test a linked tape with missing/corrupt/cyclic/wrong-manifest nodes, incorrect cursor/prefix, an uncommitted candidate object, and aggregate payloads at/above the declared limits. An existing candidate does not advance the accepted Position. Use references for individual payloads above 64 KiB and count referenced payload bytes in the 8 MiB invocation accounting.
- [ ] Run `uv run pytest tests/recovery/test_dispatch.py tests/recovery/test_tape.py -q` and confirm targeted failures.
- [ ] Implement fresh descriptor decoding through the immutable approved registry and one volatile deduplication entry per active operation. Write and hash-verify immutable candidate nodes before returning receipts. No mutable latest-head object or durable local receipt database.
- [ ] Rerun recovery and conformance tests. Kill the dispatcher between attempts and verify its missing cache is treated as lost execution knowledge, not proof that an operation did not occur. Commit the passing change.

### Task 5 Bind tool outcomes to recoverable workspace state

**Files:** Create `workspace.py`, `tests/recovery/test_workspace.py`, and `tests/recovery/test_uncertain_outcomes.py`; modify `dispatch.py` and `artifacts.py`.

**Interfaces:** Produce `capture_workspace(Path, ArtifactRef) -> ArtifactRef` and `restore_workspace(ArtifactRef, Path) -> None`. Initial empty workspace manifests are created during setup; tools never choose a host extraction path.

- [ ] Write failing tests for a report write followed by success, a report write followed by a known business error, archive upload failure, and loss of the dispatcher after a local mutation. Assert a committed outcome restores the exact accepted files; an incomplete checkpoint cannot become recoverable success.
- [ ] Test archive traversal, absolute paths, devices, unsafe links, expanded-size overflow and active background writers. The initial archive format rejects symlinks entirely. Capture fails until writers are quiescent; restoration targets an empty disposable root and never overlays runtime code.
- [ ] Use a fake external service with an independent effect counter to test mutation followed by response loss. For an unsafe contract, assert OUTCOME_UNKNOWN and zero automatic redispatches. The fake service is test infrastructure, not a bridge journal.
- [ ] Run `uv run pytest tests/recovery/test_workspace.py tests/recovery/test_uncertain_outcomes.py -q` and inspect the expected failures.
- [ ] Implement full bounded archives and explicit outcome classification. For accepted known errors, choose capture of the post-error workspace as the initial policy; if capture fails, block recovery instead of silently dropping changes. Local-only retry requires stopping old writers and restoring the previous committed workspace.
- [ ] Rerun `uv run pytest tests/conformance tests/recovery -q`, then commit the recovery matrix and evidence.

**Gate B:** Recreate the process, base session, tape and workspace from references alone. Verify the next descriptor matches its pin, no committed effect body repeats, and unknown external outcomes block. This validates bridge recovery logic; it does not yet establish Temporal durability or sandbox isolation.

## Phase 3 Add external Temporal ownership

### Task 6 Run the bounded invocation through a real Workflow

**Files:** Create `temporal.py`, `transport.py`, `tests/temporal/test_workflow.py`, and `tests/temporal/test_history.py`.

**Interfaces:** Register `SessionWorkflow.run(start: SessionStart) -> SessionResult` with Activities named `advance_runner`, `execute_model`, `execute_tool`, `provision_session`, and `close_session`. Define SessionStart/SessionResult in `records.py`; start includes frozen base/input/manifest references and an initial Position. Return final artifact references and a separate cleanup status, not a success flag that hides failed deletion.

- [ ] Write failing integration tests using a real local Temporal test environment and the trusted fixture dispatcher over one HTTP transport. Assert N=5 produces five accepted execute results and six successful advances, excluding lifecycle calls and retries. Inspect actual history rather than asserting an estimated event count.
- [ ] Test pinned pending requests, explicit terminal validation errors, an uncommitted candidate object, wrong-session/altered/expired commands, and a timed-out old request. Assert malformed protocol input does not cause an endless Workflow Task failure loop. Do not import agent modules into the external worker.
- [ ] Run `uv run pytest tests/temporal/test_workflow.py tests/temporal/test_history.py -q` and confirm missing implementation failures.
- [ ] Implement the one-invocation state machine, scoped authenticated transport, external artifact validation and compact receipts. Use explicit execute attempts; bounded automatic retries apply only to safe activities. Set a proposed 256 KiB encoded message ceiling with headroom below service limits, and measure after the configured converter/codec. Large bodies stay in immutable storage.
- [ ] Rerun tests and commit representative sanitized histories. Temporal's test environment and history Replayer cover Workflow behavior; ADK prefix reconstruction remains a separate suite. Time skipping is not a substitute for real Activity cancellation/heartbeat tests. [Temporal testing tools](https://docs.temporal.io/develop/python/best-practices/testing-suite)

### Task 7 Inject failures around the effect and commit boundary

**Files:** Create `tests/temporal/test_faults.py`; modify `temporal.py`, `transport.py`, and `dispatch.py` as failures require.

**Interfaces:** Add test-only named failpoints at before-dispatch, after-effect, after-candidate-upload, after-Temporal-completion, and before-next-advance. Production behavior must not expose arbitrary failure controls to the sandbox.

- [ ] Write failing tests for each failpoint using a parent supervisor and independent effect counters. Kill/restart the worker after accepted completion and assert no effect body repeats. Lose completion after upload and assert object existence alone does not commit the candidate.
- [ ] Test a silent long-running remote operation, heartbeat delivery, Activity timeout, cancellation, dispatcher restart, and delayed stale completion. Assert the same logical operation ID survives retry, stale bindings cannot publish results, and a replacement writer is not started before old work is confirmed stopped. Unknown unsafe effects remain blocked.
- [ ] Run `uv run pytest tests/temporal/test_faults.py -q` with actual timers for heartbeat/termination cases. Verify failures represent the selected crash window; a process killed before dispatch is not evidence about after-effect uncertainty.
- [ ] Implement the minimum recovery/rebinding paths and explicit terminal errors. Disable Workflow-execution retry; reject duplicate session starts and prohibit Reset in the prototype runbook/access policy. No administrative rewind recovery is implemented.
- [ ] Rerun all Phase 1–3 tests and history replay; commit the matrix with observed remote effects, accepted head, pending descriptor, next action and cleanup status for each injection.

**Gate C:** Temporal history is sufficient to select the next accepted Position after worker restart; only referenced immutable data is required externally. No second component chooses progress. Completion-loss tests distinguish committed-result reuse from potentially repeated uncommitted model cost and unresolved external effects.

## Phase 4 Put the runtime inside one OpenShell sandbox

### Task 8 Implement one lifecycle adapter and actual policy enforcement

**Files:** Create `openshell.py`, `tests/sandbox/test_policy.py`, `tests/sandbox/test_lifecycle.py`, and one reviewed policy fixture under `tests/fixtures/`; modify `transport.py` and lifecycle Activities.

**Interfaces:** Produce `ensure_session(start: SessionStart) -> Binding` and `delete_session(binding: Binding) -> CleanupResult`; define CleanupResult in `records.py`. Bind actual sandbox resource UUID, dispatcher instance, epoch, image digest and effective policy digest. Lifecycle calls reconcile by identity rather than a mutable display name.

- [ ] Write failing tests from code actually running inside the sandbox: allowed workspace read/write succeeds; outside-path access, Temporal endpoints, management endpoints, cloud metadata, host sockets, other-session RPC/artifacts and unapproved egress fail. Test ingress authentication even when routing is reachable.
- [ ] Test create acknowledgement loss, repeated deletion, name reuse with a different UUID, and Temporal unavailability during orphan inspection. Assert no blind duplicate creation and no deletion based only on absent local worker state.
- [ ] Run `uv run pytest tests/sandbox/test_policy.py tests/sandbox/test_lifecycle.py -q` against the selected deployment; unavailable infrastructure is an unmet gate, not a passing skip.
- [ ] Implement one static approved template and verify its effective policy. The sandbox contains the dispatcher, ADK and executors, but no Temporal credentials, task tokens or broad store credentials. Pick one externally hosted artifact backend and scoped transfer mechanism; keep worker/controller in one external deployment.
- [ ] Add a bounded cleanup reconciler in that deployment, authorized from Temporal status and resource identity. Rerun tests and commit observed denials and lifecycle receipts without tokens.

### Task 9 Demonstrate cold replacement and terminal destruction

**Files:** Create `tests/sandbox/test_replacement.py` and `tests/sandbox/test_cleanup.py`; modify `openshell.py`, `workspace.py`, and recovery Activities only where tests identify gaps.

**Interfaces:** Reuse accepted Position and pinned Operation. Rebinding changes generation/dispatcher identity but not the logical invocation/operation IDs or the approved semantic request.

- [ ] Write failing tests that remove the sandbox after several committed boundaries, restore into a new sandbox, and compare files, next descriptor and final output. Also lose the dispatcher while an unsafe fake operation is ambiguous; assert no automatic replacement execution.
- [ ] Test normal finish, failure, cancellation and hard Workflow termination. Assert old compute is stopped, capabilities revoked and session workspace removed, or cleanup remains visibly REMEDIATION_REQUIRED with retry/reconciliation evidence. Retain only declared final artifacts and diagnostic/history data under the prototype retention rule.
- [ ] Run `uv run pytest tests/sandbox/test_replacement.py tests/sandbox/test_cleanup.py -q` and confirm actual replacement UUIDs and process termination rather than mocking deletion success.
- [ ] Implement the missing stop/revoke/restore/delete paths, then rerun sandbox and Temporal fault suites and commit evidence.

**Gate D:** Exactly one authorized session sandbox exists during ordinary operation; replacements never overlap active writers. Cold replacement recovers committed files and progress, and session end removes the working environment. Demonstrate the expected limitation that tools in the same security domain may interfere with the runner; this architecture claims containment, not a tamper-proof runner.

## Phase 5 Demonstrate usefulness before packaging an SDK

### Task 10 Run one live agent and publish the prototype evidence

**Files:** Create `demo.py`, `tests/acceptance/test_live_reporter.py`, and `tests/acceptance/test_budget.py`; add a sanitized model fixture to `tests/fixtures/` and document invocation in README.

**Interfaces:** Expose a prototype command `python -m bridge_probe.demo --case repository-report --output reports/demo.json`. It starts a fresh session through the external runtime and returns final references, accepted operation summaries, usage, recovery state and cleanup status. It is not a public `agentctl` API.

- [ ] Write a failing acceptance test for one live model reading a small fixture repository through `inspect_repository`, producing `report.md` through `write_report`, and returning a final answer. Assert artifact existence/hash and required tool behavior; do not require the live model to generate identical prose or an identical new trajectory on separate runs.
- [ ] Add recorded-response roundtrip and prefix reconstruction tests using the actual provider fields. Add 1, 8, 32 and 64-boundary scripted benchmark cases, 65-boundary rejection, tape/payload limits and the 30-second advance deadline. Limit rejection must precede the next unauthorized effect.
- [ ] Run `uv run pytest tests/acceptance -q` with a scoped test identity and a proposed USD 5 spending cap. Treat the dollar cap as best-effort accounting/admission because providers may charge for unacknowledged requests; stop new dispatch when the limit is reached or usage is uncertain beyond the reserved budget.
- [ ] Implement only the selected model adapter and two approved tools. Disable or account for provider-internal retries. Fix any newly discovered serialization incompatibility and rerun Gate A before accepting the adapter.
- [ ] Rerun one normal case and one scripted cold-replacement case. Publish `reports/prototype-evidence.md` with version lock, sample history, failure matrix, policy results, artifact/cleanup receipts, Activity counts, reconstruction CPU/latency, artifact reads/bytes, workspace costs and model usage. Commit curated synthetic evidence and the runnable command.

**Gate E:** All prior gates pass for the pinned deployment. Every tested advance meets the 30-second deadline; report maximum and distribution, especially at 64 boundaries. If the bound is not practical, reduce the admitted profile or make a separate measured optimization proposal rather than quietly adding warm continuations. The user can reproduce the demonstration and identify exactly which features are supported. No production reliability claim follows from a small test sample.

## Phase 6 Extract only the SDK surface justified by evidence

### Task 11 Share the factory and tools without freezing the whole framework

**Files:** Create `src/bridge_probe/authoring.py`, `tests/acceptance/test_two_agents.py`, and `examples/repository_reporter/` plus `examples/change_summary/`, each with `agent.py`, `tools.py`, `instructions.md`, tests and small eval cases. Refactor existing wrappers/loader in place; do not create multiple independently versioned packages yet.

**Interfaces:** Introduce the spec's proposed `build(ctx: AgentContext) -> LlmAgent`, `@tool` declarations and read-only `ToolContext`. Keep their implementation in the shared prototype package. Factory/tool declarations remain the behavioral source of truth; a build descriptor supplies external workers with data without importing agent code there.

- [ ] Write failing contract tests loading both example factories through the same runtime. Assert neither example defines Temporal Workflows, RPC endpoints, checkpoint code, serializers, Dockerfiles, or policy enforcement code. Both must pass the same admission/reconstruction suite while having distinct prompts/tools/eval expectations.
- [ ] Add tests that fixture mode refuses an unexpected call, recorded replay performs no new effects, durable mode never falls back to local execution, and developer effect labels cannot grant retry/access authority. Separate quality assertions from durability/isolation assertions.
- [ ] Run `uv run pytest tests/acceptance/test_two_agents.py -q` and confirm missing authoring abstractions cause the expected failures.
- [ ] Extract only repeated factory loading, wrapped model/tools, asset handling and fixture harness code. Retain Python entrypoints for check/run/test initially. Add native ADK eval-format support only for criteria that can score the selected backend trace without a hidden local rerun; label unsupported criteria explicitly.
- [ ] Rerun all gates plus both example suites, commit the extraction, and produce a small developer README. Package publication, template generators, seven-command CLI polish, general plugins and multi-repo release automation remain separate follow-up work.

**Gate F:** Two agents use the same runtime and tests with only domain code, prompts, metadata and cases in their directories. Shared behavior stays identical after extraction. If one example needs a new runtime semantic, return to a conformance test and revise the profile; do not hide it behind an SDK escape hatch.

## Evidence and stop decisions

Every gate report records the exact command/environment, expected versus observed behavior, test failures/skips, relevant artifact/history references, and unresolved limitations. Critical tests must fail visibly when dependencies are unavailable. Use synthetic fixtures for committed evidence and restrict raw traces that contain private data.

| Failure | Required decision |
| --- | --- |
| Native ADK and reconstructed state or callback order differ | Stop before Temporal; fix the seam or narrow the profile |
| Provider continuation metadata cannot roundtrip | Reject that adapter until its codec passes conformance |
| Candidate existence can select progress | Fix authority model before adding OpenShell |
| Old execution cannot be confirmed stopped | Preserve unresolved state; do not start replacement writers |
| Effective policy cannot deny required access | Change deployment/policy or revise the security claim explicitly |
| Cold reconstruction exceeds the admitted deadline | Reduce the profile or approve a measured optimization |
| SDK requires new durability semantics | Add a new conformance case and design change first |

The first review package is Gate A, not a live model demo. The smallest end-to-end prototype is complete at Gate E. Gate F is the first SDK milestone and should begin only when the evidence supports maintaining this bridge.

## Suggested execution order

Implement Tasks 1–3 as one conformance milestone, with a test/review/commit boundary after each task. Review Gate A before Tasks 4–5; review Gate B before Tasks 6–7; review Gate C before Tasks 8–9. Run Task 10 only after actual sandbox policy and cleanup evidence exists. Decide on Task 11 from the prototype results.

For implementation, a fresh reviewer at each gate is more valuable than parallel work on speculative adapters. The tasks share evolving wire and lifecycle contracts, so keep the critical path sequential. Independent implementation/review agents can be used after an execution approach is selected, but there is no need to build SDK and infrastructure branches in parallel before conformance passes.

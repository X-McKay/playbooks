# Compatibility findings

## Pinned ADK contract

The first native run uses ADK 2.12.0 and its public time, ID and random provider
seams. The complete dependency graph is in `../uv.lock`.

A regression test exposed that `exclude_unset=True` silently loses session
`events` appended in place to a default list. The codec therefore retains all
field values plus recursive field-set metadata. The metadata preserves explicit
null versus absent fields. Binary continuation fields are encoded losslessly.
The codec excludes ADK-declared nonserialized execution objects such as
`tools_dict`; registry identity must independently bind their semantics.

ADK emits an experimental function-schema warning. The tests exercise that
version-specific declaration path; the warning is not suppressed.

## Official integration reuse assessment

Inspected temporalio/ai-integrations commit
`78e845a9e379ac18b4b69593d62b5dc3873700ab`.
The model wrapper requires Workflow context for Activity dispatch and falls back
to ordinary execution outside it. ToolContextSnapshot is a one-way read-only
contract. This prototype follows those contracts; it does not import the
Workflow-bound wrappers or claim upstream owns remote reconstruction.

The official schema preparation handles response-schema types. This initial
profile rejects those types and dynamic schemas rather than copying that broader
adapter. No upstream source is vendored. A future dispatch-seam contribution
can reuse the conformance corpus without making delivery depend on acceptance.

## Deployment target

The requested integration environment is a dedicated kind cluster running
Temporal and OpenShell. Its CNI must actually enforce ingress and egress
NetworkPolicy. Local ADK tests do not establish Kubernetes or sandbox behavior.

## Live vLLM connector

The live executor uses the installed ADK `LiteLlm` and its `LiteLLMClient` seam;
there is no vendored request/response converter. LiteLLM 1.95.0 and its transitive
OpenAI client are pinned in `uv.lock`. A small client subclass rejects truncated,
empty, parallel, unknown-tool and malformed-JSON responses before ADK conversion
can repair tool arguments. Request generation and transport overrides are rejected
so the pinned profile controls cannot be changed by a captured request.

Real HTTP fixture tests verify one request on 429 and 500 responses with both SDK
retry layers disabled. Accepted live responses are preserved as ADK LlmResponse
values, including call identities and usage. The committed synthetic recording
checks every prefix in a fresh process without inference or tool execution.

The manifest pins the endpoint, served model name and generation settings. A
served name is not an immutable weights digest; the operator must separately pin
the deployed model revision for reproducible future inference. Recorded outcomes
remain the source for replay even when new inference would differ.

## Warm continuation seam

`ContinuingBridge` reuses the cold `TapeBridge` descriptor, profile, budget and
pending checks. One `WarmRunner` owns one interpreter because the deterministic
ADK providers are process-global. Native, cold and warm traces must agree for the
admitted serial profile. The warm task reuses ADK already imported by runtime startup; no upstream
ADK or Temporal code is forked. See the [warm contract](warm-execution.md) for
acceptance, cancellation fences and the large-artifact fallback.

## OpenShell cleanup seam

The adapter uses the pinned 0.1.4 SDK's public `stop`, `get`, `delete` and
`wait_deleted` APIs. Supervisor-first stop avoids the measured concurrent
teardown delay. Stop alone never confirms deletion; the existing immutable-ID
check remains required. No driver or policy is patched. See the
[cleanup investigation](cleanup.md) for source references and failure semantics;
requalify ordering and latency when upgrading OpenShell.

## Precompiled image

The image build compiles installed application/dependency and standard-library
Python bytecode. These read-only files contain code, not initialized ADK state.
No bridge, provisioning SDK or readiness behavior changes. The
[provisioning qualification](provisioning.md) checks fresh workspace isolation
and records the cost of the larger preloaded image; cold image-pull performance
is outside those measurements.

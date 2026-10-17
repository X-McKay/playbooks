# Temporal + ADK + OpenShell prototype

An isolated implementation experiment requested for this repository. Existing
playbooks remain guidance-only. This prototype is not a production SDK.

The external Temporal worker owns accepted progress. One OpenShell sandbox holds
the entire ADK agent, model executor and tool executor for a session. Each advance
reconstructs ADK in a fresh process from the invocation input and accepted tape.
The scripted demo performs three model operations and two tool operations.

## Run

Prerequisites: Python 3.12, uv, Docker, kind 0.31.0, kubectl, Helm 3, curl and rg.
The tested host is macOS arm64 with Colima; the Linux VM must support mandatory
Landlock and OpenShell's seccomp requirements. Allocate at least 4 CPUs and 8 GiB
for this small single-node test.

From this directory:

```bash
uv sync --frozen
uv run pytest -m 'not cluster' -q
./scripts/kind-up.sh
uv run python scripts/kind_test.py
```

The setup script uses only the dedicated `adk-bridge-probe` cluster and an explicit
`.state/kubeconfig`. It installs an enforcing Cilium CNI, the Agent Sandbox
controller, authenticated OpenShell and PostgreSQL-backed Temporal. It builds and
loads the workload image. No model-provider credentials are needed for these tests.
Cluster tests are skipped by plain pytest unless explicit endpoint variables are
present; `kind_test.py` supplies them and creates its own temporary port-forwards.
A skipped test is not deployment evidence.

The local-cluster database password in the deployment manifest is a disposable
test fixture. Generated OpenShell client keys stay in ignored `.state/tls`; do not
commit or copy them into workload images. The external test worker runs on the
host, outside OpenShell. Temporal, PostgreSQL, Cilium and OpenShell run in kind.

To remove the dedicated cluster and its database/history volumes:

```bash
kind delete cluster --name adk-bridge-probe
```

Remove the local `.state` directory separately when its synthetic evidence and
client certificates are no longer needed. Sandbox tests remove their session
containers and workspace volumes; the shared cluster services stay available.

## Contracts

- `capture.py` admits a deliberately narrow, serial ADK profile and captures the
  first untaped operation. Replayed model/tool bodies never execute.
- `records.py` preserves full Pydantic values and field-set masks, including ADK
  session event lists mutated in place. Descriptors bind invocation, index,
  manifest, executor and canonical request.
- `dispatch.py` executes only registry functions from frozen descriptor bytes.
  Volatile duplicate delivery attaches to the same Task. Losing that cache does
  not authorize redispatch of an uncertain effect.
- `artifacts.py` stores immutable, hash-verified linked tape nodes. A candidate
  upload is not a commit. The Activity result accepted in Temporal history selects
  the next Position.
- `workspace.py` validates bounded link-free snapshots before acceptance and
  restores into empty directories. Known business errors retain their post-error
  files. Failed capture blocks completion.
- `activities.py` verifies the actual predecessor, operation, artifact bytes and
  workspace schema before returning a receipt. Execute Activities have one attempt.
- `openshell.py` uses official mTLS-authenticated lifecycle and exec APIs. Replay
  executes under OpenShell's supervisor because workload seccomp forbids `killpg`.
  The session-local service retains only volatile execution knowledge. Artifact
  transfer uses 128 KiB chunks below OpenShell's 1 MiB request limit.
- A failed safe advance can replace the sandbox only after old-instance deletion
  is confirmed. The new binding is a Temporal Activity result. Lost execution
  completion remains `OUTCOME_UNKNOWN`; it does not automatically replace/retry.
- `reconcile_closed` is an external cleanup primitive for hard Workflow termination,
  which bypasses Workflow `finally` blocks. It leaves running Workflows alone and
  refuses to infer terminal state when Temporal is unavailable.

## Scope and remaining gates

This slice uses one invocation, an empty base ADK session, static agent/tool
registration, a scripted model and plain text workspace files. It does not admit
streaming, parallel tools, arbitrary subprocess-spawning tools/callbacks, live
sessions, native ADK resumability, approval UI, external write tools, administrative
Reset or Workflow execution retries. Workspace metadata such as executable bits
and timestamps is outside this profile. Workload code is isolated from the host;
the bridge service and agent share a trust domain inside their session sandbox.

The tests validate cooperative admitted code, not arbitrary hostile Python
callbacks. A production release must qualify descendant-process quiescence at
individual boundaries, enforce a sandbox lease independent of worker availability,
and run the cleanup reconciler continuously. This prototype tests the reconciler
explicitly; it does not install a production janitor service.

The live-provider gate requires a selected provider and an existing scoped secret.
The wrapper SDK, developer template and second example agent remain deferred until
that gate and review are accepted. Shared platform code lives in this package;
agent-specific factory/tool definitions are illustrated in `demo.py`. No upstream
ADK or Temporal fork is maintained. See [compatibility](docs/compatibility.md) for
why the existing integration cannot simply move into an untrusted remote process.

The [design](docs/spec.md), [phased plan](docs/plan.md), and
[conformance findings](docs/conformance.md) record the intended architecture and
narrower tested profile. The [evidence report](docs/evidence.md) distinguishes observed checks from
remaining gates.

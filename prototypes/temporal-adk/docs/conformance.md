# ADK conformance gate

Gate A passed on 17 October 2026: **32 tests passed**, with one upstream
experimental function-schema warning, in 84.40 seconds.

Run from this directory's parent:

```bash
uv sync --locked
uv run pytest tests/conformance -q
```

## Evidence

- Real native ADK Runner reference with three scripted model calls and two tools.
- Every committed prefix reconstructs the exact next request or final session.
- Normal, business-error and callback-mutation branches use fresh processes.
- Twenty repetitions of all six prefixes preserve events, IDs, timestamps and
  state; no fields are removed to hide differences.
- Replay invokes no fixture effect bodies and rejects changed pending requests.
- Native CodeExecutor, unwrapped tools/models, task mode, custom planners,
  nested agents, plugin configuration and callback result overrides are rejected.
- Multiple model function calls fail before any tool body executes.
- Finalization drains the Runner; cancelled captures discard cleanup state.
- A real ADK finalizer that hangs is killed and reaped by its process owner.
- Client cancellation and excessive output also terminate and reap children.
- Lossless binary/provider fields and mutated default session lists roundtrip.

## Limits of this gate

The tests use trusted synthetic agent code and a scripted provider. They establish
neither containment nor Temporal commitment. Actual provider compatibility,
workspace recovery, Kubernetes enforcement and operational cleanup are later gates.
The adapter is cooperative: validation cannot prove arbitrary callback code has no
hidden I/O. The factory/configuration is trusted and version-bound.

The initial factory uses an empty base and one fixed fixture input. Parameterized
invocation identity, input and model selection must be wired before live execution.
The existing dependency lock includes the exact Python package versions.

# Offline producer/reviewer example

From the repository root:

```bash
uv run --locked python examples/multi-agent/main.py
```

An investigator returns typed evidence; a reviewer receives that evidence and
returns a typed proposal. Deterministic coordination checks tenant ownership,
shares a bounded request budget, and rejects a review for a different ticket.
The graph has exactly two calls and no mutation tools. Both agents use fixed
PydanticAI `TestModel` fixtures with provider requests disabled.

The [policy](release-policy.yaml) requires valid proposals, tenant isolation,
review identity checks, and budget admission. `just examples` exercises the
system scaffold and validator, runs the adapter, and proves failed gates block
release. The generated risk assessments remain draft by design.

The example demonstrates composition mechanics, not a claim that this use case
needs multiple agents or that independent fixtures measure real-model review
quality. Production adoption requires the playbook's baseline comparison and
readiness evidence. See [getting started](../../docs/getting-started.md).

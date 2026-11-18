# Offline single-agent example

From the repository root:

```bash
uv run --locked python examples/single-agent/main.py
```

This ephemeral agent returns a typed support-action proposal. A deterministic
boundary rejects cross-tenant requests before the model runs. It exposes no
mutation tool and never executes the proposed action. PydanticAI `TestModel`
returns a fixed fixture, with real provider requests disabled.

The report checks the expected ticket, proposed-action status, and denied tenant
access. The [policy](release-policy.yaml) requires those gates. Run
`just examples` to exercise scaffolding, validation, evaluation, and release
acceptance/rejection in temporary projects.

This is a testing and assembly example. It does not evaluate a real model or
establish production risk acceptance. See [getting started](../../docs/getting-started.md)
and [compatibility](../../docs/compatibility.md).

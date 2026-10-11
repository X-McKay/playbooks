# 5. Tool standard

Every tool has an explicit contract covering purpose, ownership, typed schemas, effects, authorization, retry safety, timeouts, data sensitivity, failure modes, telemetry, and cost.

## Effect classification

| Effect                | Definition                                           | Minimum execution class |
| --------------------- | ---------------------------------------------------- | ----------------------- |
| `read`                | Observes without modifying external state            | `ephemeral`             |
| `write_reversible`    | Creates a readily recoverable change                 | `durable`               |
| `write_consequential` | Creates a high-impact or difficult-to-reverse action | `human_governed`        |

The effective execution class of an agent MUST be at least the minimum required by its most consequential enabled tool.

## Retry classification

Every tool declares its retry safety alongside its effect:

| Retry safety               | Meaning                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `safe`                     | Repeating the call cannot create an additional effect        |
| `idempotency_key_required` | Repeating is safe only when a stable idempotency key is sent |
| `unsafe`                   | Repeating may duplicate an effect; no automatic retry        |

A tool policy is a typed, reviewable record:

```yaml
tool_policy:
  name: update-customer-address
  owner: customer-platform
  effect: write_reversible        # read | write_reversible | write_consequential
  retry_safety: idempotency_key_required # safe | idempotency_key_required | unsafe
  authorization_scopes:
    - customer.address.write
  timeout_seconds: 10
  data_classification: confidential
```

## Required behavior

Every tool MUST:

- Accept and return typed, serializable values.
- Validate input before performing I/O.
- Return structured domain results rather than model-oriented prose.
- Enforce authorization in application code.
- Distinguish transient failures, permanent failures, and business rejection.
- Use bounded timeouts and output sizes.
- Emit agent, workflow, tool, outcome, latency, attempt, and cost metadata.
- Minimize sensitive data returned to the model.

Tools MUST NOT depend on a persona, hide side effects behind a read-like name, interpret model text as approval, retry unsafe operations automatically, or return unbounded raw API responses.

## Recommended structure

```text
src/<package>/tools/
├── common/
│   ├── errors        # Shared error categories
│   ├── policy        # Shared policy enforcement
│   └── telemetry     # Shared span and metric helpers
└── crm/
    ├── types         # Typed domain inputs and results
    ├── service       # Client for the external system
    ├── tools         # Agent-facing tool adapters
    ├── toolset       # Registration under a stable toolset ID
    └── policy        # Tool policies for this domain
```

The service layer handles the external system. The tool layer adapts typed domain behavior for the agent. The toolset registers tools with a stable ID. This separation keeps infrastructure clients independently testable.

## Durable execution and side effects

For durable agents:

- Tool I/O executes in durable steps.
- Read tools SHOULD be safely retryable.
- Reversible writes require idempotency or a durable operation record.
- Consequential writes require valid approval and an idempotency key.
- Business rejection and authorization failure are non-retryable.
- The workflow owns orchestration, approval, compensation, and business retry policy.
- The tool owns validation and interaction with the external system.

## Quality gates

A production tool requires:

- Schema-validation tests
- Authorization and tenant-isolation tests
- Timeout and error-mapping tests
- Retry and idempotency tests appropriate to its effect
- Output-size tests
- Telemetry assertions
- Positive trajectory evals
- Negative evals proving when the tool must not be called

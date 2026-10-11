# 3. Canonical agent contract

Every production agent is represented by a reviewable package containing a declarative specification, typed runtime interfaces, and a controlled assembly function.

## Agent Spec

```yaml
name: customer-support
description: Investigate customer questions and propose policy-compliant resolutions.

instructions:
  - Resolve the request using verified customer and policy information.
  - Distinguish verified facts from assumptions and proposed actions.
  - Never claim an external action succeeded unless its tool result confirms success.

model_settings:
  temperature: 0.1
  max_tokens: 2000

retries: 2
tool_timeout: 20
instrument: true

metadata:
  contract_version: 1
  owner: customer-platform
  version: 1.0.0
  execution_class: durable
  risk_tier: medium
  risk_assessment: docs/risk-assessments/customer-support.yaml
  data_classification: confidential
  model_policy: balanced-v1
  enabled_skills:
    - customer-policy
  enabled_toolsets:
    - customer-records
    - knowledge-search
  budgets:
    max_requests: 8
    max_input_tokens: 30000
    max_output_tokens: 5000
    max_tool_calls: 12
    max_cost_usd: 0.50
```

Organization-specific fields belong under `metadata` and MUST be validated by application code during startup.

## Model policy

Production agents SHOULD select a versioned logical model policy rather than hard-code a provider model:

```text
fast-v1       -> low-latency, low-cost model
balanced-v1   -> default production model
reasoning-v1  -> high-complexity model with stricter budget
```

The resolved provider, exact model, settings, and pricing version MUST be recorded in telemetry and eval results. A model pin is permitted when reproducibility, certification, or a provider-specific feature requires it.

## Typed dependencies

Dependencies carry trusted runtime context and reconstructable service interfaces. They SHOULD be immutable for the duration of a run.

| Field                  | Type                 | Source                     |
| ---------------------- | -------------------- | -------------------------- |
| `request_id`           | UUID                 | Caller or gateway          |
| `tenant_id`            | UUID                 | Authenticated session      |
| `actor_id`             | UUID                 | Authenticated session      |
| `authorization_scopes` | Set of scope strings | Authorization service      |
| `deadline`             | Timestamp            | Caller or business process |

Dependencies SHOULD include authenticated identity, tenant context, authorization scopes, correlation identifiers, deadlines, and policy context.

They MUST NOT contain model-generated authorization, mutable global state, raw secrets, or objects that will be serialized unsafely into durable workflow history. Pass serializable identifiers across workflow boundaries and reconstruct infrastructure clients within durable steps.

## Typed output

Production agents SHOULD use a schema-validated output type. Expressed as JSON Schema:

```json
{
  "title": "SupportResolution",
  "type": "object",
  "required": ["status", "summary", "evidence", "confidence"],
  "properties": {
    "status": {
      "enum": ["answered", "action_proposed", "needs_information", "escalated"]
    },
    "summary": { "type": "string" },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "claim"],
        "properties": {
          "source": { "type": "string" },
          "claim": { "type": "string" }
        }
      }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "proposed_action": { "type": ["string", "null"] }
  }
}
```

A schema that only guides model output is not the same as runtime validation. Some declarative formats pass a schema to the model but hand back an unvalidated, untyped value. Production agents SHOULD validate output into a typed contract in application code before any downstream use. Typed, validated output is therefore the production default.

## Factory responsibilities

The factory:

1. Loads the Agent Spec.
2. Validates governance metadata.
3. Resolves the model policy.
4. Resolves and allowlists skills and toolsets.
5. Verifies tool effects against the execution class.
6. Attaches usage, spend, observability, and durable-execution capabilities.
7. Supplies dependency and output types.
8. Produces the capability manifest.

Construction MUST fail when an owner, execution class, risk tier, risk
assessment, model policy, budget, skill, or toolset is missing or invalid. The
Agent Spec risk tier MUST match the assessment's governance tier. Durable agents
MUST fail construction if durability is absent; human-governed agents MUST fail
if approval policy is absent.

## Versioning

Keep these versions separate:

- `contract_version`: organizational metadata schema.
- Agent version: behavioral configuration and capability set.
- Worker/build version: executable and workflow replay compatibility.

Behavior-changing edits to instructions, models, skills, tools, or outputs require an agent version change and relevant evals. Replay-incompatible workflow changes additionally require replay-safe deployment.

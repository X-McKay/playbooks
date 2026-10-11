# 3. Agent contract

This chapter is for the developer who owns an agent's definition. It
describes the package every production agent ships as: a declarative
specification, typed runtime interfaces, and a controlled assembly function
(the factory). Together they are the agent's contract. Reviewers read it to
see what the agent may do, and the runtime enforces it so the agent cannot
quietly do more.

## Agent Spec

The Agent Spec is the single reviewable description of your agent. Keep
behavior (instructions, model settings, retries) and governance (owner,
execution class, governance tier, capabilities, budgets) in one file, so a
change to either shows up in the same review.

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
  governance_tier: medium
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

Organization-specific fields belong under `metadata` and MUST be validated by
application code during startup. A field nothing checks is documentation, not
a control.

Best practices:

- **Write instructions the agent can verify.** "Never claim an external action
  succeeded unless its tool result confirms success" can be tested; "be
  careful" cannot.
- **Point to the risk assessment, do not summarize it.** The
  `risk_assessment` path keeps one source of truth (see
  [risk assessment](12-risk-assessment.md)).
- **Set budgets from measurement.** Start from what evaluation runs actually
  consume, then add headroom (see [cost optimization](10-cost-optimization.md)).

## Model policy

Production agents SHOULD select a versioned logical model policy rather than
hard-code a provider model. That lets you change the underlying model as a
reviewed release instead of an edit scattered across agents:

```text
fast-v1       -> low-latency, low-cost model
balanced-v1   -> default production model
reasoning-v1  -> high-complexity model with stricter budget
```

The resolved provider, exact model, settings, and pricing version MUST be
recorded in telemetry and eval results. You may pin a model when
reproducibility, certification, or a provider-specific feature requires it.

## Typed dependencies

Dependencies carry the trusted runtime context your agent needs: who is
asking, for which tenant, with what authority, and by when. They also carry
service interfaces that can be reconstructed. They SHOULD be immutable for
the duration of a run.

| Field                  | Type                 | Source                     |
| ---------------------- | -------------------- | -------------------------- |
| `request_id`           | UUID                 | Caller or gateway          |
| `tenant_id`            | UUID                 | Authenticated session      |
| `actor_id`             | UUID                 | Authenticated session      |
| `authorization_scopes` | Set of scope strings | Authorization service      |
| `deadline`             | Timestamp            | Caller or business process |

Dependencies SHOULD include authenticated identity, tenant context,
authorization scopes, correlation identifiers, deadlines, and policy context.

Dependencies MUST NOT contain model-generated authorization, mutable global
state, raw secrets, or objects that will be serialized unsafely into durable
workflow history. Pass serializable identifiers across workflow boundaries and
reconstruct infrastructure clients within durable steps. Note the Source
column: identity and scopes come from the authenticated session and the
authorization service, never from the model or the request body.

## Typed output

Production agents SHOULD use a schema-validated output type. Expressed as
JSON Schema:

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

A schema that only guides model output is not the same as runtime
validation. Some declarative formats pass a schema to the model but hand back
an unvalidated, untyped value. Production agents SHOULD validate output into a
typed contract in application code before any downstream use. Typed,
validated output is therefore the production default.

Best practices:

- **Make the outcome explicit.** A `status` such as `escalated` or
  `needs_information` lets callers handle "the agent did not finish" without
  parsing prose.
- **Separate evidence from claims.** An `evidence` array with sources makes
  answers checkable by evaluators and by people.
- **Keep proposed actions as data.** A `proposed_action` field is something
  you can show an approver; it is not an action taken.

## Factory responsibilities

The factory turns the spec into a running agent, and refuses to when the
spec is incomplete. It:

1. Loads the Agent Spec.
2. Validates governance metadata.
3. Resolves the model policy.
4. Resolves and allowlists skills and toolsets.
5. Verifies tool effects against the execution class.
6. Attaches usage, spend, observability, and durable-execution capabilities.
7. Supplies dependency and output types.
8. Produces the [capability manifest](02-reference-architecture.md#capability-manifest).

Construction MUST fail when an owner, execution class, governance tier, risk
assessment, model policy, budget, skill, or toolset is missing or invalid.
The Agent Spec governance tier MUST match the assessment's governance tier.
Durable agents MUST fail construction if durability is absent; human-governed
agents MUST fail if approval policy is absent.

Failing at startup is the point: a misconfigured agent that refuses to start
is a deploy problem, while one that starts anyway is an incident.

## Versioning

Keep these versions separate, because each answers a different question:

- `contract_version`: the organizational metadata schema.
- Agent version: behavioral configuration and capability set.
- Worker/build version: executable and workflow replay compatibility.

Behavior-changing edits to instructions, models, skills, tools, or outputs
require an agent version change and relevant evals. Replay-incompatible
workflow changes additionally require replay-safe deployment (see
[durable execution](09-durable-execution.md)).

## Common pitfalls

- **Trusting a model-filled tenant or actor.** If the model can set
  `tenant_id`, it can be talked into another tenant's data.
- **Schema in the prompt only.** The model was shown the schema, but nothing
  validated the answer before a downstream system used it.
- **Defaulting missing governance fields.** A factory that fills in a missing
  owner or tier hides exactly the gap construction should catch.
- **Prompt edits without a version bump.** A one-line instruction change is a
  behavior change, and it needs evals like any other.
- **Live clients in workflow state.** Serializing a connection or credential
  into workflow history breaks replay and can leak secrets.

## Before you move on

- [ ] The Agent Spec names owner, version, execution class, governance tier,
  risk assessment, model policy, skills, toolsets, and budgets.
- [ ] Custom `metadata` fields are validated at startup.
- [ ] Identity, tenant, and scopes come from trusted sources, not the model.
- [ ] Output is validated into a typed contract before use.
- [ ] Construction fails on any missing or invalid governance field.
- [ ] Behavior changes bump the agent version and rerun evals.

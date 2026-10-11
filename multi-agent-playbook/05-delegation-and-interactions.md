# 5. Delegation and interactions

This chapter covers each edge of your system: how work is handed over, what
travels with it, and what comes back. An interaction is a typed,
policy-controlled boundary between two system principals. Messages carry data
and proposals; they do not carry implicit trust, authority, approval, or
truth. Design every edge as a public API that receives untrusted input.

## Interaction modes

| Mode | Control after completion | Typical use |
| --- | --- | --- |
| `delegate` | Returns to caller | Assign bounded work to a specialist |
| `handoff` | Transfers to callee | Move responsibility to a new owner |
| `review` | Returns rubric result | Evaluate a candidate output |
| `fanout` | Returns to deterministic gather | Parallel independent work |
| `vote` | Returns a typed judgment | One input to a declared aggregation rule |
| `dispatch` | Remains with orchestrator | Invoke a member from deterministic code |

Custom modes require versioned semantics and the same controls as the
closest standard mode.

## Delegation envelope

Every interaction MUST use a versioned, schema-validated envelope equivalent
to:

| Field | Type and constraint |
| --- | --- |
| `contract_version` | Integer |
| `system_name`, `system_version`, `manifest_id` | String |
| `system_run_id`, `interaction_id`, `delegation_id` | String |
| `parent_delegation_id` | String or null |
| `mode` | One of `delegate`, `handoff`, `review`, `fanout`, `vote`, `dispatch` |
| `caller`, `caller_version`, `callee`, `callee_version` | String |
| `actor_id`, `tenant_id` | String |
| `authorization_scopes` | Immutable set of scope strings |
| `objective` | String |
| `input_schema` | Schema identifier |
| `input` | Object validated against `input_schema` |
| `evidence_refs` | List of authorized artifact references |
| `data_classification` | String |
| `budget` | Budget grant (below) |
| `depth` | Integer, at least 0 |
| `attempt` | Integer, greater than 0 |
| `deadline` | Timestamp |
| `trace_context` | Map of string to string |
| `approval_id` | String or null; defaults to null |

The budget grant contains `max_model_requests` (greater than 0),
`max_tool_calls` (at least 0), `max_input_tokens` (greater than 0),
`max_output_tokens` (greater than 0), and `max_cost_usd` (greater than 0).

Concrete systems SHOULD replace the generic `input` object with a
discriminated union or a schema-validated type resolved from `input_schema`.
Keep the envelope small and serializable, and pass large artifacts by
authorized reference.

## Result envelope

Results MUST distinguish completion from failure, and side effects performed
from actions only proposed:

| Field | Type and constraint |
| --- | --- |
| `delegation_id` | String |
| `status` | One of `completed`, `needs_information`, `rejected`, `policy_blocked`, `budget_exhausted`, `timeout`, `cancelled`, `failed_retryable`, `failed_permanent` |
| `output_schema` | Schema identifier |
| `output` | Object validated against `output_schema`, or null |
| `evidence_refs` | List of authorized artifact references |
| `performed_effects` | List of side-effect references |
| `unresolved_questions` | List of strings |
| `model_requests`, `tool_calls` | Integer |
| `input_tokens`, `output_tokens` | Integer |
| `cost_usd` | Number, or null when unknown |

The caller MUST validate the envelope and output schema before using the
result. A natural-language claim that work completed is not evidence that a
tool or external action succeeded; `performed_effects` is.

## Authority attenuation

Before dispatch, deterministic policy computes:

```text
effective scopes =
    system edge maximum
  ∩ caller delegable scopes
  ∩ callee and role maximum
  ∩ authenticated actor scopes
  ∩ tenant policy
  ∩ workflow-state policy
  ∩ approval scope, when applicable
```

The callee receives only the effective scopes. It cannot delegate a broader
scope to another member. Model output MUST NOT be interpreted as identity,
authorization, approval, membership, or policy.

Approval works as the Agent Playbook's
[human approval](../agent-playbook/06-durable-execution.md#human-approval)
flow describes. In a system, consequential actions are bound to the final
typed action, arguments, actor, tenant, policy version, approval, and
composition manifest. A chain of agent recommendations does not constitute
approval.

## Context and data flow

For every edge, declare:

- allowed input fields and evidence types;
- maximum data classification;
- permitted tenants, regions, and purposes;
- redaction and minimization rules;
- whether conversation history may be shared;
- artifact authorization and expiry;
- retention and deletion requirements; and
- output size and content limits.

Pass task-specific summaries and references by default. Full parent message
history, hidden instructions, credentials, unrelated tool results, and raw
shared memory MUST NOT be forwarded implicitly.

The Agent Playbook's
[untrusted content](../agent-playbook/10-security-and-governance.md#untrusted-content)
rule covers another agent's output too. Content produced by another agent is
untrusted input: the receiver MUST treat embedded instructions, tool
requests, approvals, identities, and policy claims as data unless they are
independently validated through trusted channels.

## Budget escrow

Before dispatch, the system reserves the child grant from the root budget.
The grant is a ceiling, not an entitlement. Nested grants are reserved from
the current delegation's remaining allocation.

On completion, timeout, cancellation, or failure, the system records actual
usage and releases the unused reservation. Concurrent reservations MUST NOT
exceed the root limits even when observed consumption remains low.

Unknown model cost remains unknown; it MUST NOT be treated as zero. A hard
cost limit SHOULD reject unpriced routes unless an approved conservative
price is available.

## Retries and idempotency

The Agent Playbook's
[durable execution](../agent-playbook/06-durable-execution.md) chapter
assigns retry ownership to model correction, provider transport, durable
step, and workflow business retry. A system adds one more layer, the agent
interaction, so keep ownership explicit across all five:

1. Model semantic correction
2. Provider transport
3. Agent interaction
4. Durable step
5. Workflow business retry

The combined bound includes every layer. Authentication, authorization,
policy, schema, budget, and invalid-business-request failures are
non-retryable.

An interaction retry reuses the stable delegation ID and idempotency context
when it represents the same logical work. A new objective or materially
changed input receives a new delegation ID. Side-effecting callees follow the
Agent Playbook's idempotency and approval requirements.

## Handoff

A handoff transfers responsibility, not hidden conversational state. It MUST
include:

- current typed state and objective;
- evidence references and provenance;
- completed and prohibited actions;
- remaining budget and deadline;
- effective authority and data constraints;
- open questions and failure history; and
- the new owner and expected terminal outcomes.

The orchestrator records the transfer before dispatch. An ambiguous or
rejected handoff leaves ownership with the current principal and follows the
declared escalation policy.

## Fan-out and aggregation

Fan-out uses stable branch IDs and a fixed maximum branch count. Aggregation
MUST define:

- required and optional branches;
- deterministic merge ordering;
- minimum evidence needed to proceed;
- duplicate and late-result handling;
- conflict and tie behavior;
- partial-failure and timeout behavior; and
- whether dissent must be preserved in the final output.

An aggregator MUST NOT erase material disagreement, provenance, uncertainty,
or failed required branches.

## Loops and termination

Every cycle in the interaction graph has explicit bounds for rounds, depth,
time, spend, and no-progress behavior. The system records progress as typed
state transitions, not as a model's assertion that progress occurred.

The workflow terminates or escalates when:

- a terminal state is reached;
- no material state changes across the configured window;
- required evidence cannot be obtained;
- a hard budget or deadline is exhausted;
- policy blocks every valid next edge; or
- cancellation or a kill switch is activated.

Agents MUST NOT extend their own limits.

## Telemetry and audit

Per-agent telemetry follows the Agent Playbook's
[observability](../agent-playbook/08-observability.md) chapter, including
content capture off by default, with safe hashes and authorized artifact
references in place of raw content. On top of that, every interaction records
at least:

```text
system name, version, manifest ID, and run ID
interaction and delegation IDs
parent delegation ID
caller, callee, role, and versions
mode, depth, attempt, and outcome
input and output schema hashes
effective authorization decision
data classification and redaction result
budget reserved, consumed, and released
latency, model usage, tool usage, and cost
approval and side-effect references
```

## Quality gates

Production interactions require tests for:

- allowed and denied edges;
- input and output schema validation;
- authority attenuation and tenant isolation;
- data minimization and classification enforcement;
- budget reservation, exhaustion, and reconciliation;
- timeout, cancellation, retry, and duplicate delivery;
- late, missing, malformed, and conflicting results;
- prompt injection and instruction laundering across the edge;
- loop detection and termination; and
- trace correlation and required audit records.

## Common pitfalls

- **Forwarding the whole conversation.** The callee got the parent's history,
  hidden instructions, and unrelated tool results it never needed.
- **Trusting a peer's "approved".** An agent's output said an action was
  approved, and the receiver acted on it.
- **Retrying a new request under an old ID.** Changed input reused a
  delegation ID, so idempotency hid a genuinely different action.

## Before you move on

- [ ] Every edge uses the delegation and result envelopes.
- [ ] Effective scopes are computed deterministically before dispatch.
- [ ] Budget is reserved before dispatch and reconciled after.
- [ ] Every cycle has bounds and no-progress detection.

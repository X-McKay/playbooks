# 5. Delegation and interaction standard

An interaction is a typed, policy-controlled boundary between two system
principals. Messages contain data and proposals; they do not carry implicit
trust, authority, approval, or truth.

## Interaction modes

| Mode | Control after completion | Typical use |
| --- | --- | --- |
| `delegate` | Returns to caller | Assign bounded work to a specialist |
| `handoff` | Transfers to callee | Move responsibility to a new owner |
| `review` | Returns rubric result | Evaluate a candidate output |
| `fanout` | Returns to deterministic gather | Parallel independent work |
| `vote` | Returns a typed judgment | One input to a declared aggregation rule |
| `dispatch` | Remains with orchestrator | Invoke a member from deterministic code |

Custom modes require versioned semantics and the same controls as the closest
standard mode.

## Delegation envelope

Every interaction MUST use a versioned, schema-validated envelope equivalent to:

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

Concrete systems SHOULD replace the generic `input` object with a discriminated
union or a schema-validated type resolved from `input_schema`. The envelope
remains small and serializable; large artifacts are passed by authorized
reference.

## Result envelope

Results MUST distinguish completion from failure and side effects from proposed
actions:

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

The caller MUST validate the envelope and output schema before using the result.
A natural-language claim that work completed is not evidence that a tool or
external action succeeded.

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

Consequential actions are bound to the final typed action, arguments, actor,
tenant, policy version, approval, and composition manifest. A chain of agent
recommendations does not constitute approval.

## Context and data flow

For every edge, declare:

- Allowed input fields and evidence types
- Maximum data classification
- Permitted tenants, regions, and purposes
- Redaction and minimization rules
- Whether conversation history may be shared
- Artifact authorization and expiry
- Retention and deletion requirements
- Output size and content limits

Pass task-specific summaries and references by default. Full parent message
history, hidden instructions, credentials, unrelated tool results, and raw
shared memory MUST NOT be forwarded implicitly.

Content produced by another agent is untrusted input. The receiver MUST treat
embedded instructions, tool requests, approvals, identities, and policy claims
as data unless independently validated through trusted channels.

## Budget escrow

Before dispatch, the system reserves the child grant from the root budget. The
grant is a ceiling, not an entitlement. Nested grants are reserved from the
current delegation's remaining allocation.

On completion, timeout, cancellation, or failure, the system records actual
usage and releases unused reservation. Concurrent reservations MUST NOT exceed
the root limits even when observed consumption remains low.

Unknown model cost remains unknown; it MUST NOT be treated as zero. A hard cost
limit SHOULD reject unpriced routes unless an approved conservative price is
available.

## Retries and idempotency

Keep retry ownership explicit across:

1. Model semantic correction
2. Provider transport
3. Agent interaction
4. Durable step
5. Workflow business retry

The combined bound includes every layer. Authentication, authorization, policy,
schema, budget, and invalid-business-request failures are non-retryable.

An interaction retry reuses the stable delegation ID and idempotency context
when it represents the same logical work. A new objective or materially changed
input receives a new delegation ID. Side-effecting callees follow the Agent
Playbook's idempotency and approval requirements.

## Handoff

A handoff transfers responsibility, not hidden conversational state. It MUST
include:

- Current typed state and objective
- Evidence references and provenance
- Completed and prohibited actions
- Remaining budget and deadline
- Effective authority and data constraints
- Open questions and failure history
- New owner and expected terminal outcomes

The orchestrator records the transfer before dispatch. Ambiguous or rejected
handoffs leave ownership with the current principal and follow the declared
escalation policy.

## Fan-out and aggregation

Fan-out uses stable branch IDs and a fixed maximum branch count. Aggregation
MUST define:

- Required and optional branches
- Deterministic merge ordering
- Minimum evidence needed to proceed
- Duplicate and late-result handling
- Conflict and tie behavior
- Partial-failure and timeout behavior
- Whether dissent must be preserved in the final output

An aggregator MUST NOT erase material disagreement, provenance, uncertainty, or
failed required branches.

## Loops and termination

Every cycle in the interaction graph has explicit bounds for rounds, depth,
time, spend, and no-progress behavior. The system records progress using typed
state transitions, not a model's assertion that progress occurred.

The workflow terminates or escalates when:

- A terminal state is reached.
- No material state changes across the configured window.
- Required evidence cannot be obtained.
- A hard budget or deadline is exhausted.
- Policy blocks every valid next edge.
- Cancellation or a kill switch is activated.

Agents MUST NOT extend their own limits.

## Telemetry and audit

Every interaction records at least:

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

Content capture remains off by default. Use safe hashes and authorized artifact
references when raw content cannot be retained.

## Quality gates

Production interactions require tests for:

- Allowed and denied edges
- Input and output schema validation
- Authority attenuation and tenant isolation
- Data minimization and classification enforcement
- Budget reservation, exhaustion, and reconciliation
- Timeout, cancellation, retry, and duplicate delivery
- Late, missing, malformed, and conflicting results
- Prompt injection and instruction laundering across the edge
- Loop detection and termination
- Trace correlation and required audit records

# Operating and lifecycle packet contract

Use this resource after selecting the skill and before filling the template.
It specifies a **planning and evidence handoff**, not a runtime protocol,
telemetry backend, incident system, authorization mechanism, or scheduler.

## Packet envelope

Preserve the common top-level envelope in `assets/packet-template.json`.
`run_id` identifies preparation of this packet; it is not a claimed production
run. Use the common evidence and applicability rules:

- `status` is one of `draft`, `needs_information`, `blocked`, or
  `candidate_evidenced`.
- `decision.recommendation` is one of `not_assessed`, `go`, `conditional_go`,
  or `no_go`; `decision.authorized` stays `false` because approval is external.
- An `applicability` entry has `requirement_id`, `status`, `rationale`, and
  `evidence_ids`. A `met` entry needs matching observed passing evidence.
- An observed evidence artifact is a normalized relative path confined to the
  approved workspace and carries its lowercase 64-hex digest. A planned item
  has empty artifact and digest fields.

Do not promote a design to `candidate_evidenced` merely because its fields are
filled. Preserve `draft`, `needs_information`, or `blocked` when material
implementation or observed evidence is absent.

## Required inputs

| Input field | Minimum content | Safe fallback |
| --- | --- | --- |
| `candidate_identity` | Agent ID, version, effective capability/configuration ID, and inventory reference. | Mark each unknown value `draft-unresolved`; block identity-dependent claims. |
| `agent_contract` | Contract artifact reference, terminal outcomes, success condition, permitted partial-result rule, and relevant exclusions. | `needs_information`; do not invent an outcome taxonomy. |
| `boundary_and_data_constraints` | Effect classification, authority limits, permitted correlation fields, content/retention limits, and external-effect reconciliation rule when applicable. | Exclude unpermitted fields and record the missing owner/constraint. |
| `execution_scope` | Ephemeral/resumable shape, operation types, worker/shared-budget scope, and expected in-flight behavior. | Describe only the known scope; do not imply durability or a shared ledger. |
| `operator_policy_context` | Owner contacts, stop/recovery/change authorities, escalation/communications routes, independent-review requirement, and local review policy references. | `blocked` when a reachable required operator or authority is unknown. |
| `lifecycle_context` | Consumers, outstanding-work model, dependencies, review triggers/cadence policy, access/registration inventory, data-copy classes, and inventory location. | Keep a retirement handoff draft and list each unknown as a blocker. |

## Required outputs

Populate the following `outputs` objects. A value may be planned or unresolved,
but its state and owner must be explicit.

| Output field | Minimum content |
| --- | --- |
| `operating_control_record` | Run/request/attempt identity rules; agent and effective capability/configuration identity; terminal outcomes; termination reasons; operation result categories; aggregate signals, decision owners, and bounded labels. |
| `event_schema` | Versioned common event envelope plus event-specific fields for lifecycle events. State which payload fields are permitted, redacted, omitted, or stored only in protected artifacts. |
| `attempt_trace_contract` | Trace layout for each applicable operation type, including command-line/file trace fields where a command is used. |
| `budget_and_timeout_plan` | Per-dimension unit, scope, ceiling, pre-dispatch control, charge/reservation timing, reconciliation, in-flight treatment, unknown-use rule, and exhaustion behavior. |
| `stop_and_recovery_plan` | Stop scope, operator, request record, suppression behavior, in-flight state, cancellation evidence, reconciliation, recovery authority, and prerequisite evidence to resume. |
| `support_incident_record` | Named/staffed roles, escalation, triage, containment, communications, minimum permitted evidence, factual separation, and recovery record. |
| `feedback_and_review_plan` | Feedback-item ledger, disposition/follow-up linkage, periodic cadence, triggered reassessment, required review coverage, and missed-review disposition. |
| `deprecation_retirement_handoff` | State distinction, consumer/outstanding-work inventory, work disposition, access/registration revocation, copy-specific data handling, retained evidence, and final inventory/manifest update. |

## Identity and event fields

Use stable opaque identifiers. Do not make a personal identity, raw request,
raw address, or free-form content part of an aggregate metric label.

### Common event envelope

| Field | Meaning |
| --- | --- |
| `event_id` | Unique immutable event identifier. |
| `schema_version` | Version of this event shape. |
| `recorded_at` | Timestamp when the recorder accepted the event, with declared time basis. |
| `sequence` | Monotonic per-run ordering value, or an ordering key with documented semantics. |
| `event_type` | Controlled category, such as `run_started`, `attempt_dispatched`, `attempt_finished`, `budget_reserved`, `budget_exhausted`, `stop_requested`, `stop_confirmed`, `incident_triaged`, `review_due`, or `retirement_state_changed`. |
| `run_id` | Stable bounded-work identifier; unchanged through resumptions. |
| `request_ref` | Permitted opaque initiator reference, when the initiating request concept exists. |
| `attempt_id` | Physical-operation identifier; absent only for events not tied to an attempt. |
| `parent_attempt_id` | Prior attempt only when a retry relationship exists. |
| `agent_id` and `agent_version` | Identity of the agent definition used for the run. |
| `effective_capability_configuration_id` | Resolved capability/configuration identity needed to interpret behavior. |
| `payload` | Event-specific structured values subject to the data-handling decision. |
| `telemetry_capture_status` | `captured`, `partial`, `failed`, or another controlled capture category; never task success. |

Keep these independent: `terminal_outcome`, `termination_reason`,
`operation_result`, `external_effect_status`, and `telemetry_capture_status`.
For example, a run may have terminal `failed`, termination reason
`elapsed_time_exhausted`, a timed-out attempt, an `unknown` external effect, and
partially captured telemetry.

## Attempt, command, output, and file-change trace

For every physical operation attempt, include the applicable fields below.
These fields define **what an implementation should record**, not a report of
an operation that happened.

| Field | Meaning |
| --- | --- |
| `operation_type` and `operation_identity` | Controlled kind and versioned or resolved identity of the invoked operation. |
| `attempt_id`, `run_id`, `parent_attempt_id` | Attribution and retry relation; a retry receives a fresh attempt ID. |
| `dispatch_at`, `finished_at`, `elapsed_ms` | Start/finish and monotonic elapsed measurement; distinguish waiting where it matters. |
| `command_identity` | Executable or command identity when an operation launches a command; otherwise omit. |
| `argv_representation` | Redacted canonical argument representation or digest, never secrets. |
| `working_location_ref` | Permitted approved-workspace reference, never an unreviewed host path by default. |
| `exit_code`, `exit_signal`, `operation_result` | Separate command result facts; non-command operations use a controlled result category. |
| `timeout_state` and `cancellation_state` | `not_requested`, `requested`, `confirmed`, `unresolved`, or applicable controlled state; request is not confirmation. |
| `stdout_bytes`, `stderr_bytes`, `output_capture_ref`, `output_truncated` | Measured output sizes and protected capture reference; capture failure is separately visible. |
| `error_category` | Bounded safe category, not raw error text as an aggregate label. |
| `resource_measurements` | Measured, estimated, or `unknown` use by dimension. |
| `input_files`, `output_files`, `file_changes` | File manifests using only normalized approved-workspace-relative paths. |

Each file-manifest entry contains `path`, `pre_exists`, `post_exists`,
`pre_size_bytes`, `post_size_bytes`, `pre_sha256`, `post_sha256`, and
`change_kind`. A missing value is explicit `unknown` or `not_collected`; do not
substitute an invented digest. Treat a raw output artifact as governed data, not
an automatically permitted event payload.

## Bounds, timeout, and exhaustion plan

Represent every applicable bound as an object with:

```json
{
  "dimension": "draft-example",
  "unit": "draft-example",
  "scope": "per_run",
  "ceiling": "draft-unresolved",
  "measurement_point": "pre_dispatch_and_reconciliation",
  "reservation_rule": "draft-unresolved",
  "charge_rule": "each_physical_attempt",
  "in_flight_treatment": "accounted_pending_reconciliation",
  "unknown_use_rule": "remain_unknown",
  "exhausted_behavior": "stop_new_work_and_return_contract_defined_non_success"
}
```

Use only dimensions the contract and execution scope support. A shared budget
must name the shared durable-accounting owner, reservation/reconciliation rule,
and concurrency boundary. A local attempt counter cannot substantiate a bound
across workers or runs. On exhaustion, emit the triggering dimension, remaining
or measured/estimated/unknown use, affected attempt reference, and a distinct
termination reason. Do not change the terminal outcome vocabulary merely to
name the exhausted resource.

## Stop, incident, and recovery records

### Stop record

Plan fields for `stop_id`, request time, requester/authorized operator reference,
scope, reason category, suppression rule, affected run/capability references,
in-flight attempt references, cancellation requests, confirmation evidence,
unresolved items, and state (`requested`, `active`, `confirmed`, `resumed`, or
`unresolved`). Stopping new work neither reverses a prior effect nor authorizes
resumption.

### Suspected-incident triage record

Plan fields for `incident_ref`, signal ID/source/time, suspected scope, impact
criteria reference, containment options considered/selected, incident
decision-maker, communications owner, permitted evidence references, facts,
hypotheses, investigation status, confirmed cause only when supported,
corrective-action reference, and remaining uncertainty. A signal or hypothesis
must not be stored as a confirmed incident or cause.

### Recovery record

Before a post-containment resumption can be externally authorized, the record
needs cause or remaining uncertainty, corrective action, applicable safeguards
and release-gate evidence references, an external authorization reference, and
unknown-external-effect reconciliation status. This packet identifies those
fields; it does not make the authorization.

## Feedback, review, deprecation, and retirement

A feedback item includes `feedback_id`, source category, received time,
classification, disposition, accountable follow-up, target/review reference,
materiality rationale, and links to corrective action, risk/evaluation evidence,
change, or retirement decision where relevant.

A periodic review identifies cadence policy/reference, next/reviewed time,
triggered-reassessment events, owner, contactability result, dependency status,
failure/feedback pattern, capability/data/consumer changes, control/evidence
fitness, findings, and missed-review disposition. Do not turn a cadence into
proof of ongoing safety.

For lifecycle state, keep `proposed`, `deprecated`, `disabled`, `retired`, and
`unresolved` distinct. The retirement handoff tracks new-work stop status,
consumer inventory, outstanding-work items and disposition, unneeded credential
revocation, unneeded capability-registration removal, copy-specific data
disposition policy/reference, evidence retention, inventory/manifest update,
and any unresolved exception. A `retired` claim needs matching observed evidence;
a plan remains draft.

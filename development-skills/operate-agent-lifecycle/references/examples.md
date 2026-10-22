# Illustrative planning patterns

These are **fictional planning patterns**, not observed run records, command
logs, incident findings, approvals, or retirement evidence. Replace all draft
values with candidate-specific material and keep a missing value unresolved.

## 1. Read-only candidate: operating-control design

A candidate answers from permitted material and has no external write capability.
Its packet can plan one stable `run_id` per bounded request, a new `attempt_id`
for every retrieval or model attempt, and the following controlled categories:

```json
{
  "terminal_outcomes": ["complete", "needs_information", "declined", "failed"],
  "termination_reasons": [
    "elapsed_time_exhausted",
    "retrieval_call_exhausted",
    "operator_stop_requested",
    "unresolved_in_flight_operation"
  ],
  "aggregate_labels": ["operation_type", "terminal_outcome", "termination_reason"],
  "draft_status": "no production run has been observed"
}
```

The design does not put a requester identity or raw request into an aggregate
label. It also does not call a successfully captured attempt `complete`; the
terminal outcome is assessed against the agent contract.

## 2. Command attempt trace: planned field shape

Where the implementation launches a command, its future trace can be designed
with this shape. Values are placeholders, not a claim that a command ran.

```json
{
  "event_type": "attempt_finished",
  "run_id": "draft-run-opaque-id",
  "attempt_id": "draft-attempt-002",
  "parent_attempt_id": "draft-attempt-001",
  "operation_type": "approved-operation-category",
  "command_identity": "draft-command-identity",
  "argv_representation": "redacted-or-digest-only",
  "dispatch_at": "draft-time",
  "finished_at": "draft-time",
  "elapsed_ms": "draft-measurement",
  "exit_code": "draft-unobserved",
  "exit_signal": "draft-unobserved",
  "timeout_state": "not_requested",
  "stdout_bytes": "draft-measurement",
  "stderr_bytes": "draft-measurement",
  "output_capture_ref": "draft-permitted-artifact-reference",
  "output_truncated": "draft-unobserved",
  "file_changes": [
    {
      "path": "draft-approved-workspace-relative-path",
      "pre_exists": "draft-unobserved",
      "post_exists": "draft-unobserved",
      "pre_sha256": "draft-unobserved",
      "post_sha256": "draft-unobserved",
      "change_kind": "draft-unobserved"
    }
  ]
}
```

An implementation records exit status, timeout/cancellation, and output capture
separately. A time-out after a potentially effecting operation is not evidence
that the effect failed or that another retry is safe.

## 3. Exhaustion and stop: separate planned facts

Suppose the contract permits `failed` after an elapsed-time ceiling. The packet
can plan a pre-dispatch check, physical-attempt charge, and stop-new-work rule:

```json
{
  "dimension": "elapsed_time",
  "scope": "per_run",
  "ceiling": "candidate-specific-under-approved-policy",
  "charge_rule": "each physical attempt is accounted",
  "on_exhaustion": {
    "terminal_outcome": "contract-defined-non-success",
    "termination_reason": "elapsed_time_exhausted",
    "new_work": "suppressed",
    "in_flight_operation": "unresolved_until_confirmed"
  },
  "evidence_state": "planned-only"
}
```

A separate stop request may cover one run or all new work for one capability.
It records a requested state, scope, authorized operator reference, suppression
rule, and in-flight references. It becomes confirmed only with cancellation or
completion evidence. It does not undo an effect or authorize a resumption.

## 4. Suspected incident: facts do not become a cause

A support record could state:

> **Signal:** A permitted operator reported an unexpected output. **Hypothesis:**
> Source selection may be incomplete. **Known facts:** None yet beyond the
> report. **Containment candidate:** Prevent new work on the suspected path while
> scope is assessed. **Status:** suspected incident, triage not complete.

The triage plan identifies local impact criteria, the incident decision-maker,
communications owner, permitted minimum evidence, and containment options. It
does not label the hypothesis a root cause or describe containment as recovery.
Before resumption, the distinct recovery record awaits remaining-uncertainty or
cause, corrective action, safeguard/release-gate evidence, and external recovery
authorization.

## 5. Feedback and review: a governed follow-up

A feedback item can be planned as follows:

```json
{
  "feedback_id": "draft-feedback-001",
  "source_category": "support_report",
  "classification": "recurring_uncertainty",
  "disposition": "investigate",
  "accountable_follow_up": "draft-named-owner",
  "linked_corrective_action": "draft-action-reference",
  "linked_evaluation_or_risk_record": "draft-record-reference",
  "state": "planning-only"
}
```

The review plan names policy-selected cadence plus early review triggers:
incident, changed behavior/permission/capability/data/source, dependency warning,
new consumer, ownership gap, or altered risk assumption. A missed review is
recorded with its disposition, not silently treated as complete.

## 6. Deprecation is not retirement

A lifecycle handoff can contain this draft state model:

```json
{
  "state": "proposed",
  "deprecation_notice": "draft-not-issued",
  "disabled_scope": "draft-none",
  "new_work_stop": "draft-not-executed",
  "consumer_inventory": "draft-not-complete",
  "outstanding_work": "draft-not-inventoried",
  "data_copies": ["active", "retained_evidence", "export", "backup", "third_party"],
  "retirement_evidence": "absent"
}
```

Only after new work, consumers, outstanding work, unneeded access and
registrations, every relevant data copy, required evidence, and inventory status
are handled under applicable policy can observed evidence support `retired`.
Disabling for containment leaves retirement open.

## 7. Conditional recovery and retirement: bounded non-trigger

This fictional snapshot is limited to a future policy-lookup candidate during a
planning review. It has no containment event that created a pending resumption,
and it is neither deprecated nor retired. The separate preparedness assessment
keeps planned ownership and runbooks visible without treating them as execution
evidence.

```json
{
  "case_scope": "Fictional policy-lookup candidate; bounded planning review only.",
  "preparedness_assessment": {
    "support_ownership": {
      "requirement_id": "LIFECYCLE-01",
      "status": "unmet",
      "rationale": "The fictional support owner, recovery authority, and reachable route are planned values; no support record is verified."
    },
    "recovery_runbook": {
      "status": "planned",
      "rationale": "The runbook design names the future recovery-record fields but does not claim containment, resumption, or authorization."
    },
    "retirement_handoff_runbook": {
      "status": "planned",
      "rationale": "The handoff design lists future consumer, work, access, data, evidence, and inventory checks but does not claim retirement."
    }
  },
  "applicability": [
    {
      "requirement_id": "LIFECYCLE-01",
      "status": "unmet",
      "rationale": "Future production support ownership is in scope, but the fictional support record remains planned and unverified.",
      "evidence_ids": ["planned-lifecycle-preparedness"]
    },
    {
      "requirement_id": "LIFECYCLE-03",
      "status": "not_applicable",
      "rationale": "In this fictional bounded planning case, no affected capability is pending resumption after containment. The planned recovery runbook is assessed separately and does not claim a recovery record or authorization.",
      "evidence_ids": []
    },
    {
      "requirement_id": "LIFECYCLE-06",
      "status": "not_applicable",
      "rationale": "In this fictional bounded planning case, the candidate is neither deprecated nor retired. The planned handoff runbook is assessed separately and does not claim a retirement.",
      "evidence_ids": []
    }
  ],
  "evidence": [
    {
      "id": "planned-lifecycle-preparedness",
      "kind": "planned",
      "status": "not_run",
      "artifact": "",
      "sha256": ""
    }
  ],
  "decision": {
    "recommendation": "not_assessed",
    "authorized": false
  }
}
```

If a bounded case instead identifies a pending post-containment resumption or a
deprecated/retired candidate, the corresponding entry is `unmet` until its
required record and handoff actions are verified. This fictional example reports
no operation, observation, authorization, or lifecycle execution.

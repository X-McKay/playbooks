# Trust-boundary packet contract

Use this reference after reading the owner map and before filling the JSON template. The packet is an implementation aid and planning record. It does not authenticate a caller, carry a credential, authorize an operation, or prove a live effect.

## Common envelope

Keep the template's top-level fields and their meanings unchanged.

| Field | Record here |
| --- | --- |
| `inputs` | Candidate identity, bounded task, supplied planning/contract records, known operating context, proposed channels, and declared approved workspace root. Do not include secrets or unneeded bodies. |
| `outputs` | The authority, content/action, and conditional data records below, plus open handoffs and safe outcomes. |
| `assumptions` | Explicitly draft assumptions that need confirmation; never place an inferred permission here. |
| `blockers` | Missing trusted provenance, scope, owner decision, data classification, destination rule, or enforcement point that prevents a readiness claim. |
| `applicability` | One row per Part 3 requirement ID using `met`, `not_applicable`, `unmet`, or `exception_proposed`, with a real trigger rationale and evidence IDs. |
| `evidence` | Planned or observed references. Observed evidence needs a normalized relative artifact path under the approved workspace and a lower-case 64-character SHA-256. |
| `decision` | An external readiness input only. Keep `authorized` false; authorization is made per operation at the protected boundary. |

A `met` applicability row needs at least one matching observed, passing evidence entry. Missing, failed, invalid, or inconclusive evidence cannot support `go` or `conditional_go`. A planned evidence item can leave `artifact` and `sha256` empty.

## Authority boundary record

Create `outputs.authority_boundary_record` with these fields.

| Field | Record here |
| --- | --- |
| `construction_boundary` | Candidate/version identity, admitted capability inventory, declared workspace root, and the fact that these are not runtime permission decisions. |
| `operation_register` | One row for every protected read, workspace write, live-service operation, export, communication, approval path, and explicit denial. |
| `trusted_context_sources` | Provenance for workload identity, requester/tenant, resource attributes, policy identity/currentness, approval when applicable, and destination. |
| `credential_constraints` | Workload-specific scope, audience/resource limit, lifetime, delivery outside model context, and prohibited ambient/personal/shared/forwarded credential modes. Never record the credential itself. |
| `execution_gate` | Normalization, trusted-context acquisition, current authorization, approval condition when required, dispatch boundary, failure outcome, and recheck trigger. |
| `denied_paths` | Unlisted tools, resources, destinations, data classes, workspace escapes, live-service routes, or authority-expansion paths with their bounded outcome. |
| `observations` | Separate construction, proposal, validation, authorization, dispatch, response, and authoritative-effect evidence needs. |

Use this operation-row shape:

```text
id
kind: workspace_write | protected_read | live_service | communication | export | approval | denied
purpose
proposed_by: trusted_request | untrusted_content | model | configuration
normalized_action_and_target
resource_and_data_class
requester_or_tenant_relation
destination
authority_mode
trusted_context_sources
admitted_at_construction: true | false
per_operation_decision: allow | deny | needs_information | not_assessed
credential_constraints
required_approval_binding
safe_outcome
denied_alternatives
```

A workspace row names a path under the user-approved workspace and may state the autonomous local deliverable. A live-service row names a distinct service action and must not inherit permission from the workspace row. An operation row with `admitted_at_construction: true` is still `not_assessed` until its per-operation gate receives trusted current facts.

## Content and action boundary record

Create `outputs.content_action_boundary_record` with the following maps.

| Field | Record here |
| --- | --- |
| `trusted_operating_context` | Task boundary, admitted capabilities, authenticated scope, output contract, and allowed destinations from named sources. |
| `untrusted_channels` | User content, retrieval, attachment, tool result, peer message, summary, or other content with source role and compact provenance. |
| `flow_map` | For each input-to-destination edge: allowed influence, transformation, retained provenance, receiver, validation sequence, and safe outcome. |
| `action_surface` | Finite admitted operations and destinations plus intentionally absent routes. |
| `injection_controls` | Controls that prevent content from changing capability, authority, execution class, approval state, tenant, target, or destination at the actual receiving operation. |
| `confused_deputy_controls` | How authenticated requester/tenant facts are obtained and checked at the protected operation rather than supplied by the model or broad service identity. |
| `validation_and_observations` | Structural, provenance, semantic, and protected-operation checks; proposal/decision/dispatch/effect observations remain separate. |

Do not treat a delimiter, citation, screen, classifier, model self-review, or source label as the action boundary. Record it only as a defense-in-depth signal when it exists.

## Conditional data-handling and audit record

Create `outputs.data_handling_audit_record` for the DATA trigger decision. When data is in scope, include:

| Field | Record here |
| --- | --- |
| `trigger_decision` | Whether non-public or personal data is processed, the evidence for that conclusion, and separately whether a consequential-event audit row is triggered. |
| `category_copy_map` | Each category and copy across request, model, retrieval, tool, output, state, diagnostics, evaluation, support, export, backup, and derived stores. |
| `destination_and_access_map` | Purpose, minimum useful representation, destination, access role, transformation, retention/deletion rule, and unresolved owner decision for every copy. |
| `capture_and_export_controls` | Default-disabled content capture, required exceptional-capture conditions, and redaction/exclusion before export. |
| `diagnostic_and_audit_lanes` | Separate purpose, access, retention/deletion, integrity, and derived-store treatment. |
| `consequential_event_audit` | Actor, action, target, time, candidate/run identity, policy/approval references, non-content argument binding, and result; omit raw hidden reasoning and unneeded content. |
| `privacy_harm_handoffs` | Plausible pathway, affected groups, material uncertainty, test implications, and accountable-owner/specialized-assessment handoff. |

Use `not_applicable` only after recording why the relevant trigger is absent. An unresolved category, destination, retention purpose, or consequential-event determination is a blocker or unmet item, not evidence of absence.

## Handoff and verification record

Add `outputs.handoffs` and `outputs.verification_plan` that name the accountable owner, open decision, required source, safe interim outcome, and planned evidence. Use harmless and minimized fixtures. Preserve failed attempts. If implementation changes are made in the approved workspace, record the required order: end-to-end safe-fixture test, cleanup of unique artifacts, full retest, then package/export review. None of those local observations constitute a live-service authorization or effect.

# Packet contract — Draft Agent Implementation

Use `assets/packet-template.json` as the starting record. It is a planning aid, not an authorization, a runtime configuration, or evidence that a control operated.

## Common envelope

The packet has exactly these common top-level fields:

```json
{
  "schema_version": "1.0",
  "skill": "draft-agent-implementation",
  "run_id": "string",
  "status": "draft|needs_information|blocked|candidate_evidenced",
  "source_commit": "151fca01fbc609c5550c563c902946db540c2f4c",
  "inputs": {},
  "outputs": {},
  "assumptions": [],
  "blockers": [],
  "applicability": [],
  "evidence": [],
  "decision": {"recommendation": "not_assessed|go|conditional_go|no_go", "authorized": false}
}
```

Keep `decision.authorized` **always `false`**. A recommendation is a handoff to the accountable decision-maker, not approval to expose, deploy, or effect a change.

## Required implementation inputs

Record these fields under `inputs` before implementation:

| Field | Required content |
| --- | --- |
| `problem_description` | Detailed bounded job and desired terminal outcomes. |
| `constraints` | Prohibited behavior, safety and data limits, quality expectations, and known dependencies. |
| `workspace_authority` | Caller-approved workspace path, source identity or revision, permitted local changes, owner, and explicit exclusions. |
| `implementation_profile` | Caller-provided profile identity, revision, availability check, and status. `unresolved` is allowed only before code work. |
| `build_budget` | Time/resource bounds, test scope, and a predeclared repair cap; propose `2` repairs per run unless the caller specifies another cap. |

A profile may be omitted for planning. It is then an explicit unresolved input and blocks the `implemented` transition; do not infer a default profile. An unavailable host or required construction capability is `needs_information`, not a reason to improvise or fetch an alternative.

## Required outputs and phase artifacts

Under `outputs`, retain named, workspace-relative paths or structured summaries for `implementation_state`, `plan_handoff`, `contract_handoff`, `trust_handoff`, `implementation_manifest`, `code`, `tests`, `operability_docs`, `test_ledger`, `cleanup_record`, `retest_ledger`, `package`, and `readiness_handoff`. Mark a not-triggered extension with an applicability record and rationale rather than leaving its status ambiguous.

`implementation_state` contains the current stage, a compact transition log, repair count, candidate identity, and hashes of the source and valid phase artifacts. Its only forward sequence is:

```text
initialized → planned → implemented → tested → cleaned → retested → packaged → review_ready
```

`blocked` and `failed` are recorded transition events and do not claim completion. A bounded repair after an attributable test failure returns the state to `implemented`. It preserves the failed trial and reason, increments the repair count, and may proceed only while the predeclared cap remains. A fixture, harness, or evaluator repair follows its predeclared rule; it does not erase an attributable candidate failure.

## Evidence and applicability

Each applicability record has exactly `requirement_id`, `status`, `rationale`, and `evidence_ids`; `status` is `met`, `not_applicable`, `unmet`, or `exception_proposed`. A `met` entry needs at least one matching observed pass evidence ID. An absent trigger needs a decision-specific rationale; it is not an unbuilt or unverified control.

Each evidence record has `id`, `kind`, `status`, `artifact`, and `sha256`:

- `kind` is `planned` or `observed`.
- `status` is `pass`, `fail`, `invalid`, `inconclusive`, or `not_run`.
- An observed artifact is a normalized relative path confined to the approved workspace, with a lowercase 64-character SHA-256 digest.
- A planned record has empty `artifact` and `sha256` fields.

Keep failed, invalid, and inconclusive records with their reasons in the relevant ledger. They are never passes and cannot support `go` or `conditional_go`.

## Invalidation and package boundary

Hash code, configuration, tests, and evidence before relying on them. Planned cleanup may update the active source identity; retain the historical first-test observation and require the complete fresh retest of the cleaned candidate. Unplanned behavior-affecting changes take the bounded repair path. A change after `retested` invalidates packaging and readiness eligibility; record the reason and return to `implemented`. Never mutate retained evidence or reuse stale passes or a prior archive.

Only after a successful end-to-end test, cleanup, and a **complete retest** may the package step create an archive. The package record identifies its contents, archive digest, source candidate identity, and the retest evidence it contains. Do not overwrite a prior archive or claim a ZIP was built when any prerequisite is missing.

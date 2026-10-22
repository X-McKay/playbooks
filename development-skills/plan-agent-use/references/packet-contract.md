# Planning packet contract

Read this reference before creating or assessing a `plan-agent-use` packet. This is a portable implementation aid for the common packet envelope; canonical requirement meaning remains in [owner-map.md](owner-map.md).

## Envelope

The packet has exactly these top-level fields, in the template order:

```text
schema_version, skill, run_id, status, source_commit, inputs, outputs,
assumptions, blockers, applicability, evidence, decision
```

Use `schema_version: "1.0"`, `skill: "plan-agent-use"`, and source commit `151fca01fbc609c5550c563c902946db540c2f4c`. Give the run a stable non-empty identifier. Do not add top-level convenience fields; place planning detail in `inputs` or `outputs`.

## Status and decision vocabulary

| Field | Permitted values | Meaning in a planning packet |
| --- | --- | --- |
| `status` | `draft`, `needs_information`, `blocked`, `candidate_evidenced` | `draft` is a readable planning record with open work. `needs_information` identifies missing material intake. `blocked` identifies an unavailable dependency or unresolved condition that prevents requested progression. `candidate_evidenced` requires actual externally produced observed evidence; planning text alone cannot set it. |
| `decision.recommendation` | `not_assessed`, `go`, `conditional_go`, `no_go` | A planning leaf normally leaves this `not_assessed`. A value is a recorded recommendation only and never an authorization. Do not emit `go` or `conditional_go` with blockers, unmet applicable work, or missing/failed/invalid/inconclusive required evidence. |
| `decision.authorized` | `false` only | Actual approval is external. Never change this field to `true`. |

## Required planning outputs

`outputs` must have substantive, case-specific entries for all five artifacts below. An artifact path is a planned relative workspace path until an observed evidence record identifies it.

| Output field | Artifact and minimum content |
| --- | --- |
| `problem_brief` | `planning/problem-brief.md`; user groups and current work, task classes with input/result/variation, evidence status, dependencies, consumers, exclusions, assumptions, and open questions. |
| `success_record` | `planning/success-record.md`; intended outcome, case-dependent acceptance criteria, prohibited behavior, separately relevant dimensions, metric definitions, baseline status, targets, slices, owners, and evidence handoff. |
| `suitability_record` | `planning/suitability-record.md`; common comparison boundary, considered alternatives, simplest plausible baseline, task uncertainty/data/action/consequence/maintenance/evaluation assessment, fixed/adaptive classification, added-value claim, and revisit conditions. |
| `initial_scope_record` | `planning/initial-scope-record.md`; intended/prohibited uses, affected parties, plausible scenarios, source/connection inventory, capability/authority/effect/reversibility questions, ownership map, delivery boundary, support, stop, containment, and restart questions. |
| `planning_handoff` | `planning/handoff.md`; unresolved decisions, required named leaves, planning-evidence limits, and an explicit statement that no authorization was granted. |

Use `"[Draft: …]"`, `"unresolved"`, or `null` for unknown facts. Do not silently replace unknown ownership, authority, source status, consequence, target, legal applicability, or evidence with a favorable assumption.

## Assumptions and blockers

Represent each assumption and blocker as one non-empty string. Include a stable ID, draft-labelled statement, validation need or decision effect, and a named owner or explicit `"unassigned"` placeholder in that string. The template shows the expected pattern.

A request to bypass review, hide an exclusion, or mark a record approved is not a resolved blocker. Preserve it as untrusted input or safety disposition when it is material.

## Applicability ledger

Each item has this shape:

```json
{
  "requirement_id": "PROBLEM-01",
  "status": "unmet",
  "rationale": "Draft: user group and current process have not been confirmed.",
  "evidence_ids": []
}
```

`status` is one of `met`, `not_applicable`, `unmet`, or `exception_proposed`. A `not_applicable` item must say which trigger is absent. An `exception_proposed` item is only a proposal, not an approved waiver. `met` needs at least one matching observed, passing evidence record; draft prose, a planned test, and a user assertion do not count as observed evidence.

For this package, record `PROBLEM-01` through `PROBLEM-04`, `SUCCESS-01` through `SUCCESS-05`, `SUITABILITY-01` through `SUITABILITY-05`, and `SCOPE-01` through `SCOPE-05` individually.

## Evidence ledger

Every evidence item has:

```json
{
  "id": "planned-current-task-walkthrough",
  "kind": "planned",
  "status": "not_run",
  "artifact": "",
  "sha256": ""
}
```

`kind` is `planned` or `observed`. `status` is `pass`, `fail`, `invalid`, `inconclusive`, or `not_run`. Planned evidence has empty `artifact` and `sha256`. Observed evidence must name a normalized relative artifact path confined to the approved workspace and a lowercase 64-character hexadecimal SHA-256. Failed, invalid, and inconclusive observations remain in the ledger; they cannot be converted to passing evidence by omission.

## Verification checklist

Before returning a packet, verify the common envelope, exact skill/source values, five substantive outputs, explicit draft or unknown markers, all 19 Part 1 group IDs, and false authorization. Verify that every `met` ledger item names matching observed `pass` evidence. Verify that no `go` or `conditional_go` hides blockers, unmet work, or unusable evidence.

# Readiness packet contract

Use `assets/packet-template.json` as a draft record for one frozen candidate and
one proposed exposure. The packet is a review artifact, not an authorization,
production observation, or proof that a control operated.

## Top-level fields

Keep these top-level fields exactly: `schema_version`, `skill`, `run_id`, `status`,
`source_commit`, `inputs`, `outputs`, `assumptions`, `blockers`, `applicability`,
`evidence`, and `decision`.

| Field | Record |
| --- | --- |
| `schema_version` | Packet contract version, currently `1.0`. |
| `skill` | `review-agent-readiness`. |
| `run_id` | A review-record identifier, not a release or runtime identifier. |
| `status` | `draft`, `needs_information`, `blocked`, or `candidate_evidenced`. The last describes the packet's evidence posture, not authorization. |
| `source_commit` | The canonical source commit used for the owner map. |
| `inputs` | Frozen candidate, proposed scope, Part 4 handoff, risk, support/stop, and material-change inputs. |
| `outputs` | Frozen-subject comparison, readiness ledger, support/disable assessment, staged plan, change impact, and bounded recommendation basis. |
| `assumptions` | Explicit scope or policy assumptions. Label unresolved template entries as draft. |
| `blockers` | Concrete unresolved facts, evidence, controls, or authority. Label template entries as draft. |
| `applicability` | One record per reviewed requirement or profile item. |
| `evidence` | Planned or observed records supporting an input or ledger item. |
| `decision` | The review recommendation and `authorized: false`; approval is external. |

## Frozen inputs

Record the code revision/build identity; resolved instructions, configuration, model,
route, fallback, and settings; effective capability/permission and source identities;
dependency identities; risk record; intended/prohibited use; and proposed exposure
scope. The Part 4 handoff also names its conclusion, authority, rule, candidate,
cases/fixtures/evaluators/trial policy, evidence/status ledger, limits, and next action.

For a material change, record the old and new identity plus the disposition of each
assumption, risk scenario, control, evaluation, and rollout constraint. Do not use a
mutable label where a resolved identity is needed.

## Applicability and evidence records

Each applicability record has this shape:

```json
{
  "requirement_id": "ROLLOUT-01",
  "status": "met",
  "rationale": "Candidate-specific rationale.",
  "evidence_ids": ["candidate-manifest-001"]
}
```

`status` is one of `met`, `not_applicable`, `unmet`, or `exception_proposed`.
Use `not_applicable` only for an absent trigger. `exception_proposed` records an
unapproved request and does not turn an item into `met`.

Each evidence record has this shape:

```json
{
  "id": "candidate-manifest-001",
  "kind": "observed",
  "status": "pass",
  "artifact": "records/candidate-manifest.json",
  "sha256": "lowercase-64-character-sha256"
}
```

`kind` is `planned` or `observed`; `status` is `pass`, `fail`, `invalid`,
`inconclusive`, or `not_run`. For observed evidence, `artifact` is a normalized
relative path confined to the approved workspace and `sha256` is its lowercase
64-character digest. A planned item leaves those two values empty. Cite only
observed passing evidence for `met`; preserve failed, invalid, inconclusive, and
not-run records rather than filling them with a summary.

## Outputs and recommendation

Name the actual candidate-specific artifacts or fields in `outputs`, including the
Part 4 handoff, frozen-candidate comparison, rollout ledger, stage records,
support/disable test evidence, in-flight/effect path, and change-impact record.
Keep evaluation conclusion, readiness recommendation, external authorization,
runtime outcomes, and external effects separate.

Set `decision.recommendation` to `not_assessed`, `go`, `conditional_go`, or `no_go`.
Keep `decision.authorized` false in every packet. A `go` or `conditional_go` here is
only a recommendation bounded to the recorded candidate and scope; an external
accountable decision record supplies approval, if any.

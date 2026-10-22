# Evidence packet contract

Use this contract to create a decision-ready **record**, not an approval, certificate, or
simulated result. Its packet shape is portable; evaluation artifacts remain in the approved
workspace named by the packet.

## Top-level packet fields

Use exactly these top-level fields from `assets/packet-template.json`:

| Field | Required content |
| --- | --- |
| `schema_version` | The packet schema version, currently `1.0`. |
| `skill` | `build-agent-evidence`. |
| `run_id` | A stable identifier for this evidence assembly, not a claim that execution occurred. |
| `status` | `draft`, `needs_information`, `blocked`, or `candidate_evidenced`. |
| `source_commit` | The immutable playbook source revision used by this package. |
| `inputs` | Candidate, baseline or first-release rationale, contract, approved workspace, scope, and authorities actually supplied. |
| `outputs` | Named, substantive workspace artifacts and fields described below. |
| `assumptions` | Explicit, material assumptions; mark unresolved assumptions as draft until verified. |
| `blockers` | Missing prerequisites, authority, evidence, or dependencies; mark template text as draft until replaced. |
| `applicability` | One record per considered requirement, with its status, rationale, and evidence IDs. |
| `evidence` | Planned or observed evidence records, defined below. |
| `decision` | A recommendation only. `authorized` is always `false`; approval remains external. |

Do not add a top-level field to represent an undocumented result. Put a substantive named
artifact in `outputs`, a status-bearing artifact in `evidence`, or a real obstacle in `blockers`.

## Required output artifacts

Name these records in `outputs` using normalized relative paths under the approved workspace:

| Output field | Artifact and minimum content |
| --- | --- |
| `coverage_map` | `evaluation/coverage-map.yaml`: each claim, prohibited outcome, risk, profile, test level, case, evaluator, stage, decision role, owner, and rerun trigger. |
| `case_register` | `evaluation/cases.json`: stable case identity, versioned input, origin, tags, purpose, terminal result, invariants, and allowed variation. |
| `fixture_manifest` | `evaluation/fixtures.json`: fixture identity, revision, initialization, unique per-test copy rule, isolation boundary, reset, reset verification, data classification, and authoritative observation. |
| `evaluator_records` | `evaluation/evaluators/`: claim-to-method records, known-pass and known-failure self-tests, fitness, limits, reviewer provenance, and calibration when required. |
| `trial_policy` | `evaluation/trial-policy.yaml`: trial unit, fresh-session reset, sources, time or resource bounds, attempt accounting, retry, selection, fallback, status, and uncertainty rules. |
| `decision_policy` | `evaluation/decision-policy.yaml`: dated must-pass gates, thresholds, critical slices, missing-evidence treatment, repair rule, authority, and distinction between controls, task metrics, and diagnostics. |
| `run_ledger` | `evaluation/runs/<run-id>/ledger.jsonl`: append-only physical attempt records and final-policy result records. |
| `comparison_report` | `evaluation/reports/<candidate-id>.md` and a machine-readable companion: candidate-baseline pairing, flips, denominators, status counts, limits, and holdout disposition. |
| `repair_record` | `evaluation/repairs/<repair-id>.yaml` when a declared repair occurs; otherwise state that no repair was used. |

The paths are a portable suggested layout, not a grant to create files outside the approved
workspace. An output field with a planned path is not an observed execution artifact.

## Applicability records

Each `applicability` record has exactly this object shape:

```json
{
  "requirement_id": "CASE-01",
  "status": "unmet",
  "rationale": "draft: the coverage map has not yet been completed",
  "evidence_ids": []
}
```

`status` is one of `met`, `not_applicable`, `unmet`, or `exception_proposed`.

- Set `met` only when at least one listed evidence ID resolves to **observed**, `pass` evidence
  that is sufficient for the requirement.
- Use `not_applicable` only with an objective absent-trigger rationale, not cost, convenience,
  rarity, a missing mechanism, or a desired conclusion.
- Use `unmet` for a requirement that applies but lacks valid evidence.
- Use `exception_proposed` to preserve an exception request; it is not evidence that the
  exception is accepted.

Map the precise `CASE`, `BEHAVIOR`, `EVALUATOR`, `COVERAGE`, and `RELEASE-EVIDENCE` groups using
`owner-map.md`. The packet must also retain an invalid or inconclusive required record rather
than changing its applicability entry to `met`.

## Evidence records and identity

Each evidence record has this shape:

```json
{
  "id": "case-current-candidate-attempt-01",
  "kind": "observed",
  "status": "pass",
  "artifact": "evaluation/runs/run-017/case-current-candidate-attempt-01/checker.json",
  "sha256": "lowercase-64-hex-content-digest"
}
```

Use `kind: "planned"`, `status: "not_run"`, and empty `artifact` and `sha256` fields for a
planned check. A fixture, case, template, proposed checker, or intended command is planned
material until an attributable execution emits evidence.

For `kind: "observed"`:

1. Use a normalized relative `artifact` path confined to the approved workspace; reject absolute
   paths, traversal, symlinks, mutable shared aliases, and missing files.
2. Use the lowercase 64-character content digest of that exact retained artifact.
3. Link the record to the candidate and resolved configuration, case and fixture revisions,
   evaluator version, trial conditions, fresh-session reset observation, terminal outcome,
   end-state verifier result, and status reason.
4. Retain only claim-sufficient events, source, boundary, state, or recipient observations.
   Never require hidden reasoning.

Identity has two parts. **Content identity** records the candidate source, configuration,
checker, fixture, reference, and artifact digests. **Semantic identity** records the stable
claim, case purpose, expected outcome or invariant, allowed variation, fixture meaning, and
risk scope. Equal names, paths, or version labels do not establish either identity alone.

## Emit test artifacts at the evidence boundary

For every physical attempt, create a unique run directory and emit the following immediately
when the attempt ends, whether it passes or fails:

1. `manifest.json`: candidate and baseline identities, resolved configuration, case, fixture,
   evaluator, checker, environment, and fresh-session/reset identifiers.
2. `events.jsonl`: material command, tool, boundary, source, state, stop, and trajectory events.
3. `end-state.json`: observable terminal outcome and the authoritative state or output verifier.
4. `checker.json`: evaluator result, version, inputs inspected, status, and reason.
5. `attempt.json`: physical attempt number, start/end time, resource or timeout observations,
   status, and links to the four artifacts above.

Hash each retained artifact and write an evidence record only after its verifier completes. The
ledger may add a declared final-policy result, but it must never overwrite physical attempts.
A successful final file with no valid end-state verifier is not passing evidence.

## Fresh trials, comparison, and holdouts

Initialize each trial in a fresh session and a unique fixture copy. Capture reset verification
before candidate execution. A dirty workspace, unverified reset, unavailable authoritative
observation, or harness ambiguity is `invalid` or `inconclusive` according to the predeclared
policy; retain the record and reason.

When comparing a candidate and a baseline, use the same applicable case, fixture semantics,
fixture revision, sources, test level, evaluator, reset, trial policy, and pass predicate.
Record the paired comparison unit and visible case or critical-slice flips. Identify a first
release instead of manufacturing a baseline.

Keep an independently authored holdout case and fixture separate from development and regression
materials. Do not inspect its expected result to tune the candidate, checker, rubric, threshold,
or repair. Report holdout results separately from development results.

When variability, selection, retry, fallback, or inference is material, predeclare denominator,
physical attempts, final-policy result, reset, fixed and varying sources, uncertainty method,
and dependence assumptions. Label first-attempt, multi-attempt, and final-policy measures
separately. Do not treat repeats within a case as independent population observations without a
justified design.

## Evaluator fitness

Use deterministic checkers or authoritative boundary/state observations for deterministic claims.
Use qualified independent review for material ambiguity or specialized interpretation. A model
judge is optional: use it only where the stated qualitative claim cannot be established by those
methods. Before it supports a decision-facing gate, calibrate the exact judge configuration on
independently human-reviewed heldout examples from relevant claim and risk classes; retain its
criteria, labels, false passes, false failures, disagreements, unknowns, and fitness decision.

Until that record exists, a model judge is diagnostic-only. It cannot be the sole evaluator for
an enforceable authorization, isolation, approval, schema, boundary, or effect claim.

## No retry-until-green; bounded repair instead

A candidate failure remains `fail`; do not rerun it silently or select a favorable transcript.
A timeout does not become a clean retry. Preserve invalid and inconclusive records as distinct
statuses with their reason, and do not exclude them from a denominator without the predeclared
policy.

A replacement run after a fixture, harness, or evaluator defect is permitted only when a
predeclared bounded repair rule specifies all of the following:

- a finite repair counter and stop condition;
- the retained original record and defect diagnosis;
- the candidate and semantic case purpose that remain fixed;
- the unchanged input scope, fixture meaning, invariant, threshold, gate, and decision policy;
- the repair identity, changed artifacts, and non-bias rationale; and
- rerun of every affected paired candidate-baseline evidence item.

A candidate behavior that independently establishes failure remains a candidate failure even if
the harness also needs repair. On repair-budget exhaustion, missing authority, changed claim
scope, or failed hard gate, stop and surface `blocked`, `needs_information`, or `no_go` as the
declared policy requires.

## Autonomous coding completion order

A user-approved workspace may be modified autonomously only within its stated boundary. Record
all code, checker, configuration, and fixture changes. For a completed coding cycle, enforce this
order:

> required end-to-end execution → cleanup specified by the fixture → full applicable retest from
> clean state → retained-artifact verification → evidence packaging

A repair changes the relevant identities and invalidates stale downstream test or package claims.
Rebuild the comparison and packet from the retained records; never package a pre-cleanup or
partially retested result as complete.

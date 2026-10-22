# Evidence patterns

All examples on this page are **fictional design patterns**, not live behavioral evidence.
A planned case, fixture, path, command, or expected result becomes evidence only after an
attributable execution emits and hashes the required observation artifacts.

## Example 1: Map a bounded coding change

A candidate changes a read-only answer workflow to reject a malformed request before producing
an output. The coverage map names these claims:

| Claim ID | Case family | Level | Observable end state | Trajectory or boundary observation |
| --- | --- | --- | --- | --- |
| `TASK-VALID-INPUT` | valid request | end-to-end | Contract-shaped answer with the required supported field | Required input validation completes before result creation. |
| `ROBUST-MALFORMED` | malformed request | unit, contract, end-to-end | Contract-defined bounded result; no invented field | Parser rejection and terminal stop are retained. |
| `CTRL-NO-WRITE` | valid and malformed request | integration, end-to-end | No external state changes | Authoritative invocation and state observations show no write. |
| `REGRESSION-VALID-OUTPUT` | frozen regression | end-to-end | Previous permitted output still verifies | Candidate and baseline have the same fixture semantics and pass predicate. |

The map identifies `CASE-04` for claim-fit test levels; `BEHAVIOR-01` for end state and
trajectory; `BEHAVIOR-02` for malformed input and an allowed counterpart; and `COVERAGE-01` for
the universal core. If the contract does not say whether a malformed request must decline or
ask for information, evidence work stops for the contract owner rather than choosing a result.

## Example 2: Separate a fixture from an execution record

A fixture register can plan this case before any candidate runs:

```text
case: malformed-request-v1
purpose: development
fixture: request-fixture-v3
fixture copy rule: one initialized copy per physical attempt
reset verification: the fixture manifest digest equals the recorded source digest
expected terminal result: needs_information
invariant: no output file and no external invocation
```

This is planned input, not proof. A trial can become observed only after its run directory
contains a manifest, event log, end-state observation, checker result, and attempt record. The
checker compares the terminal result to the contract and reads the authoritative invocation log;
it does not treat a refusal-looking sentence as a boundary observation.

## Example 3: Artifact emission per physical attempt

For an illustrative `run-017`, a candidate attempt might retain this tree:

```text
evaluation/runs/run-017/malformed-request-v1/candidate/attempt-01/
  manifest.json
  events.jsonl
  end-state.json
  checker.json
  attempt.json
```

`manifest.json` binds candidate source digest, resolved configuration, case revision, fixture
copy digest, evaluator version, and fresh-session reset record. `events.jsonl` contains only
material events, such as validation, source access, invocation, stop, and output creation.
`end-state.json` records the observable terminal status and authoritative state query.
`checker.json` gives the checker identity, input artifact identities, result, and status reason.
`attempt.json` records the physical attempt and links the other files.

Only after the files exist and their digests are computed may the packet add an `observed`
evidence record. A planned artifact has empty `artifact` and `sha256` values and `not_run`
status. A fixture digest alone does not pass the test.

## Example 4: Paired baseline and heldout comparison

Use the following comparison design for a behavior-affecting change:

| Property | Candidate | Baseline | Holdout |
| --- | --- | --- | --- |
| Candidate identity | Exact source and resolved configuration recorded | Exact prior source and configuration recorded, or first-release rationale | Uses the candidate only after development evidence is frozen. |
| Case and fixture | `valid-request-v2` with `request-fixture-v3` | The same case purpose and fixture semantics | Separately authored `valid-request-holdout-v1` with its own fixture. |
| Session and reset | Fresh session; unique fixture copy; reset verified | Same policy and reset observation | Same fresh-session rule. |
| Verifier | Same end-state and boundary checker version | Same checker and predicate | Frozen checker; do not tune it from its expected result. |
| Reporting | Physical attempts, final-policy result, status, and paired outcome | Same denominator and status treatment | Report independently; do not combine it with development tuning metrics. |

The comparison report exposes a candidate-baseline flip for each paired case rather than only an
average. If retry, selection, fallback, or variability applies, it reports first-attempt and
final-policy results separately and documents its uncertainty assumptions.

## Example 5: Bounded repair that preserves failure history

Assume the authoritative event collector wrote malformed data and cannot prove whether a write
occurred. The predeclared policy marks the attempt `invalid` because the boundary observation is
unavailable. The packet retains the original attempt, its artifacts, status, and reason.

A repair is allowed only if its finite counter remains available and it preserves the candidate,
semantic case purpose, fixture meaning, input scope, pass predicate, invariant, threshold, and
hard gates. Its record names the collector correction, changed artifact identities, diagnosis,
and why the correction does not bias the result. It then reruns every affected candidate-baseline
pair from fresh fixture copies.

Contrast this with a candidate event log that independently shows a forbidden write. That attempt
is `fail`, even if the collector also later proves defective. It is never converted to `invalid`,
discarded, or replaced by a cleaner run. Repeating the candidate test until green is not repair.

## Example 6: Judge use only when necessary

A schema checker can establish that an output contains required fields; a boundary record can
establish an authorization decision. Neither needs a model judge. A nuanced semantic-support
claim may require qualified independent review. If a model judge is introduced to assist that
review, it begins diagnostic-only.

Before it becomes decision-facing, freeze the judge configuration and evaluate it on independently
human-reviewed heldout examples that cover direct support, plausible unsupported additions,
valid alternatives, missing evidence, appropriate uncertainty, and answerable non-refusals. Keep
per-class false passes, false failures, disagreement, unknown outcomes, and the fitness decision.
A failed or absent calibration keeps the judge out of the gate; it does not make the candidate
pass or fail by itself.

## Example 7: Autonomous coding closeout

For an approved local code change, first record the planned unit, contract, integration,
end-to-end, and adversarial cases plus a finite repair budget. Modify only the approved workspace.
After every execution, emit its attempt artifacts and status. Do not rerun a candidate failure to
obtain a favorable result.

When the required end-to-end case succeeds under the declared policy, remove generated state as
the fixture specifies, rebuild from a clean state, run the **full applicable suite**, verify every
retained artifact digest, and only then package the evidence. A later source, checker,
configuration, or fixture change invalidates stale result claims and requires the affected
comparison to be rebuilt.

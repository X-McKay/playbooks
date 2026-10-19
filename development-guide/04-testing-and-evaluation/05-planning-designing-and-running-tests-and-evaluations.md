# 4.5 Planning, Designing, and Running Tests and Evaluations

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Agent builders, evaluation designers, reviewers, and accountable owners
**Applicability:** Production candidates and changes for which test or evaluation evidence will support a material design, pilot, release, or operational decision. Select methods and depth to fit the claims, capabilities, and risks in scope.
**Reader question:** How do I build and operate an evaluation process?

[Part 4 — Testing and Evaluation](README.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Practical reference](reference/README.md)

## From a claim to an interpretable result

A useful evaluation starts with a question that matters, not a convenient score. What must the agent do for its intended users? What must it never do? Which capability, dependency, or risk could change the answer? Keep each claim narrow enough that a case can exercise it and evidence can establish it. [4.6](06-standards-required-coverage-and-execution-cadence.md) owns the required coverage map and profile triggers; this chapter shows how to turn selected claims into executions.

Treat evidence as a lifecycle input rather than a one-time certificate: the NIST AI Risk Management Framework describes risk measurement and testing as ongoing, including before deployment and during operation [1]. This supports continuous learning, not any particular test count or pass threshold.

The working chain is:

1. **Map claim to case and profile.** Record the claim, its decision role, applicable risk or capability profile, case or case family, owner, stage, and reason for any relevant profile marked not applicable. A case may support several claims, but keep their expected outcomes and evidence distinguishable.
2. **Design cases with purpose.** Give each case a stable identity, versioned task and origin, expected observable outcome or invariant, permitted variation, and suite purpose. Include ordinary answerable work as well as relevant missing, stale, conflicting, denied, malformed, or otherwise adverse conditions. A refusal-only suite cannot establish useful behavior.
3. **Specify the fixture.** Define the controlled starting world: revisioned data and identity/permission state, dependencies, initialization, isolation, any permitted live boundary, reset and reset verification, and the authoritative source that can establish the outcome. Keep the fixture (what the case starts with) distinct from the reference or observation (what determines or demonstrates whether a claim holds).
4. **Choose evaluator and trials.** Select an evaluator capable of judging the claim, document its identity and rule, and establish its fitness for the intended use. Before running, state what counts as pass, fail, invalid or inconclusive, and how repeats, retries, variants, and missing observations will be treated. See [4.4](04-evaluators-metrics-rubrics-and-calibration.md) for evaluator selection and calibration, and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) for interpretation.
5. **Run and preserve evidence.** Identify the exact candidate and configuration, case and fixture revisions, evaluator version, trial conditions, outcome, status, and relevant observation. Preserve cost/resource evidence where those are claims. Do not equate identical wording with reproducibility: repeated episodes should begin from verified conditions, while acceptable response wording or safe routes may vary.
6. **Triage, learn, and hand off.** Separate candidate behavior from fixture, harness, dependency, or evaluator defects. Preserve every attempted run and its status. Fix an evaluation defect only under a predeclared, visible rule; retain invalid records and rerun affected evidence as required. A confirmed, privacy-reviewed production failure can become a regression case with a clear expected behavior. Send attributed results and evidence limits to the analysis and decision process rather than announcing a release conclusion here.

Best practice: make each record linkable through stable IDs, not by relying on filenames or a copied transcript. Keep the candidate, case, fixture, evaluator, trial, and evidence identities together so a reviewer can trace a result back to the conditions that produced it.

## Cases, suites, and independent holdouts

A case is a bounded probe, not just a prompt and a preferred response. Record why it exists, what it tests, what outcomes are acceptable, which path conditions matter, and what harmless variations are allowed. If the claim concerns current evidence, include the older or conflicting evidence that could trigger the failure; a current-only fixture cannot expose stale-source selection. If missing evidence should produce `needs_information`, make that the expected outcome rather than rewarding an invented complete answer.

Keep suite purpose explicit: development cases can guide iteration; regression cases preserve reviewed behavior; an acceptance set supports a specified stakeholder decision; a release holdout supplies evidence not used to tune the behavior being reported. A holdout must be separate in more than its label: preserve its access and use boundary, and use separately authored tasks and fixtures. Re-running development cases under a new suite name does not make an untouched holdout. If a holdout is exposed or used to change prompts, rules, rubrics, or case selection, record the loss of independence and establish a fresh holdout before making a claim that depends on independence.

For indirect prompt-injection cases, harmless marker content and instrumented destinations help expose whether attempted content reaches a boundary; a clean final answer alone does not establish that no disclosure or action occurred [3].

Cases should evolve from representative requirements, reviewed adverse scenarios, and resolved failures. A report or incident is not automatically a valid test case: first remove or transform sensitive material, establish the expected behavior with an accountable reviewer, and record provenance without retaining unnecessary raw user content. Keep the case's origin visible, but do not make raw transcripts the default source of truth.

## Fixtures, isolation, and safe data handling

A fixture controls the conditions necessary to interpret a trial; it does not guarantee that a stochastic agent will produce identical text. For an isolated read-only policy assistant, the controlled world might include a current approved document, a superseded version, a user with a defined permission, a fixed clock, and a per-run retrieval log. For a system with effects, fixture and outcome design must additionally capture the relevant boundary and authoritative state; a transcript is not proof that an external action did or did not occur.

Prefer fresh per-run namespaces or equivalent isolation over shared mutable state. Before each run, initialize from the declared fixture revision and verify the fields material to the claim: source identities and revisions, permissions, relevant state, and empty or correctly initialized event records. Afterward, reset and verify again before another trial. If the reset cannot be verified, do not describe the next trial as an independent fresh-world run. State any live services or mutable inputs explicitly; record the conditions they expose rather than implying that a fixture controlled them.

Use synthetic or appropriately minimized data where it can establish the claim. Restrict access to evaluation records, separate identifiers from user content when possible, and retain only evidence needed for the decision and later review under applicable policy. If real production-derived material is necessary, use an authorized handling and sanitation process before reuse. Do not place credentials, secrets, or unnecessary personal content in cases, fixtures, logs, or examples. These are practical safeguards; the privacy and retention rules applicable to a particular deployment remain owned by its governing policy.

Best practice: use a small, explicit fixture contract. A controlled dependency should represent the failure shapes relevant to the claim—such as denial, timeout, malformed or partial response—not only the happy path. Do not add a live dependency merely for realism if a controlled substitute can establish the claim safely; when the live boundary is essential, document why and how its variation is observed.

## Worked example: current policy, denied access, and a separate holdout

The example is fictional. The policy assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources and cites them. It has no persisted memory, external write, approval flow, or delegated agent. In the controlled development/regression fixture, the current London hotel value is GBP 220. A prior case included only the current document, so it could not reveal whether the assistant would select a superseded source when both were available. The revised case uses the shared identifiers and keeps the stale document visible as a plausible distractor.

```yaml
example_status: "illustrative only; not executed"
candidate: "policy-assistant@candidate-current-selection"
baseline: "policy-assistant@baseline-current-selection"
fixture:
  id: "travel-policy-current"
  revision: "fixture-2026-10-18.1"
  initialization:
    clock: "2026-10-18T09:00:00Z"
    user:
      id: "employee-uk-104"
      permissions: ["approved-policy-read"]
    documents:
      - id: "travel-policy-2026"
        revision: "2026-10-01"
        status: "current"
        text: "London hotel limit: GBP 220."
      - id: "travel-policy-2024-superseded"
        revision: "2024-01-01"
        status: "superseded"
        text: "A different London hotel limit applied under this superseded policy."
  isolation: "fresh document namespace and tool log per trial"
  permitted_live_boundary: "none"
  reset:
    action: "discard namespace and recreate from the named fixture revision"
    verify:
      - "document IDs, revisions, and current/superseded status match"
      - "user permission matches"
      - "per-trial tool log is empty"
  authoritative_observation: "fixture document store and per-trial tool log"
case:
  id: "POLICY-CURRENT-001"
  suite_purpose: "regression"
  origin: "reviewed stale-source-selection failure scenario"
  tags: ["approved-retrieval", "currentness", "permitted-user"]
  input: "What is the hotel limit for a trip to London?"
  expected:
    terminal_outcome: "complete"
    current_source: "travel-policy-2026@2026-10-01"
    answer_value: "GBP 220"
    must_not_use: "travel-policy-2024-superseded@2024-01-01"
    external_writes: 0
  allowed_variation: "Equivalent clear wording with the same supported value and citation"
evaluators:
  - "source-permission-check@v1"
  - "grounded-policy-human-rubric@v1"
  - "trajectory-boundary-check@v1"
  - "grounding-judge@v1 (diagnostic only unless fitness is established)"
trial_record:
  candidate: "policy-assistant@candidate-current-selection"
  case: "POLICY-CURRENT-001"
  fixture_revision: "fixture-2026-10-18.1"
  reset_verified: "record per trial"
  attempt: "record each physical attempt; do not hide retries"
  status: "pass | fail | invalid | inconclusive"
  observation: "response, cited source/revision, permission decision, and event log"
holdout:
  suite: "policy-release-holdout@v1"
  case: "POLICY-HOLDOUT-009"
  fixture: "separately authored and maintained holdout fixture"
  use: "not used to tune the candidate or evaluator reported on it"
```

For each run, initialize a fresh namespace and verify source revisions, permission, and the per-run log before exposing the question. Evaluate the answer against the fixture's current source and the claim-specific grounding rubric; inspect permission and boundary observations separately from the semantic judgment. Then discard and recreate the namespace and verify the reset before another trial. A correct value with an unsupported citation is not automatically a grounding pass; a blocked out-of-scope retrieval proposal and an actual unauthorized retrieval are distinct observations. No external-write check is implied by this read-only design.

The remaining shared cases give the suite meaningful contrasts: `POLICY-STALE-002`, `POLICY-MISSING-003`, `POLICY-CONFLICT-004`, `POLICY-DENIED-005`, `POLICY-INJECTION-006`, `POLICY-PARAPHRASE-007`, and `POLICY-EXHAUSTION-008`. `POLICY-HOLDOUT-009` remains independently authored with a separate task and fixture; do not substitute the development cases under that ID. Use a missing-evidence case to check for a bounded outcome, a current-policy conflict to check that the assistant does not invent a definitive amount, a denied case to observe permission enforcement and disclosure separately, and a paraphrase pair only after review establishes that the meaning is preserved. If the candidate's behavior is materially variable, predeclare fresh trials and their decision unit; the example specifies no universal count or adequacy claim.

A curated suite establishes results on the cases and conditions it contains; it does not automatically justify extrapolation to future users or broader contexts. NIST's Generative AI Profile cautions against generalizing capability from narrow or anecdotal assessment [2].

This example specifies test design, not executed results. It does not establish semantic grounding for arbitrary answers, all retrieval risks, population reliability, or release readiness. The reusable record structures belong to the [practical reference](reference/README.md), not this chapter.

## Requirements

- **CASE-02 — Case identity, purpose, and holdout independence.** When curated cases support a behavior, safety, or usefulness claim, each case **MUST** have a stable identity, versioned input, origin or rationale, applicable capability/risk tags, expected observable outcome or invariants, allowed variation, and stated suite purpose, with its trial records linkable to those identities. A release holdout used to support a claim of independence from tuning **MUST** remain separate from cases used to tune the reported behavior; it **MUST** use independently authored task/fixture material rather than development or regression cases relabelled as untouched. Teams **SHOULD** add confirmed failures to regression suites only after review establishes expected behavior and sensitive source material has been sanitized.

- **CASE-03 — Controlled fixture contract.** When a case depends on documents, identity or permission data, tools, external state, time, randomness, or another dependency, the fixture **MUST** identify its revision, initialization, per-run isolation boundary, permitted live boundary, reset method, reset verification, and authoritative outcome observation. The evaluation **MUST NOT** treat an unverified reset or mutable shared state as evidence that independent trials began in the same controlled world. Fixture and evidence handling **MUST** use only data authorized and proportionate to the claim, with sensitive material minimized or sanitized before case reuse.

- **CASE-05 — Execution evidence and failure intake.** Each case execution relied on as evidence **MUST** retain the evaluated candidate/configuration identity, case and fixture revisions, evaluator identity/version, trial conditions, outcome observations, and a status that distinguishes pass, fail, invalid, and inconclusive execution. Invalid and inconclusive executions **MUST** remain visible with their reason; neither is a pass or a basis for silently removing a result from the record. Production-derived cases **MUST** be sanitized and classified before reuse. A confirmed candidate failure **MUST NOT** be discarded or relabelled invalid because an aggregate score remains acceptable or an evaluation component also fails. A harness/evaluator defect may support a replacement run only under a predeclared repair rule that retains the invalid record, preserves the candidate and semantic claim/scope, records the repair rationale, and reruns affected evidence without relaxing criteria. Where the observed candidate behavior itself establishes a failure, it remains a candidate failure.

## Evidence and checklist

Retain the versioned claim/case map, case and fixture inventory, evaluator/trial policy, and attributed execution records needed to trace each reported result. Before handing results to analysis, check:

- [ ] Each case has a stable ID, versioned input, rationale, applicable tags, observable expectation, allowed variation, and suite purpose.
- [ ] A release holdout has its own protected use boundary and independently authored task/fixture; it was not used to tune the reported candidate or evaluator.
- [ ] Fixture revision, initialization, isolation, live boundaries, reset procedure, reset verification, and authoritative observation are explicit.
- [ ] Data is synthetic or minimized where practicable; production-derived material is authorized, sanitized, classified, and not more revealing than needed.
- [ ] Each trial identifies candidate/configuration, case, fixture, evaluator, relevant fixed/random conditions, observations, and visible status.
- [ ] Invalid or inconclusive runs have retained reasons; no rerun or repair hides a candidate failure or relaxes the claim.
- [ ] Evaluator and trial policy are fit for the stated claim; repeated runs are not described as independent when the relevant conditions were shared or reset was unverified.
- [ ] Confirmed, reviewed production failures are available for regression intake without unnecessary raw user data.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[3]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"

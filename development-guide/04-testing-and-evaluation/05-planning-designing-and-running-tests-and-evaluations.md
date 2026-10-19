# 4.5 Planning, Designing, and Running Tests and Evaluations

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Agent builders, evaluation designers, reviewers, and accountable owners  
**Applicability:** Production candidates and changes for which test or evaluation evidence supports a design, pilot, release, or operational decision. Pick methods and depth to fit the claims, capabilities, and risks in scope.  
**Reader question:** How do I build and operate an evaluation process?

[Part 4 — Testing and Evaluation](README.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Practical reference](reference/README.md)

## From a claim to an interpretable result

Start with a question that matters, not a convenient score. What must the agent do for its users? What must it never do? Which capability, dependency, or risk could change the answer? Keep each claim narrow enough that a case can exercise it and evidence can establish it. [4.6](06-standards-required-coverage-and-execution-cadence.md) owns the coverage map and profile triggers; this chapter turns selected claims into executions.

Treat evidence as an ongoing input, not a one-time certificate: the NIST AI Risk Management Framework says AI systems should be tested before deployment and regularly during operation.[1] That supports continuous learning, not any test count or pass threshold.

You do not need a large suite to begin. Start with around 20 realistic tasks drawn from real usage, real failures, and the manual checks you already do, then grow the suite as failures appear.[4] Early changes have large effects, so a small set already gives useful signal.

The working chain:

1. **Map claim to case and profile.** Record the claim, its decision role, applicable risk or capability profile, case or case family, owner, stage, and the reason for any profile marked not applicable. A case may support several claims, but keep their expected outcomes and evidence distinguishable.
2. **Design cases with purpose.** Give each case a stable identity, versioned task and origin, expected observable outcome or invariant, permitted variation, and suite purpose. Include ordinary answerable work as well as relevant missing, stale, conflicting, denied, malformed, or adverse conditions. A refusal-only suite cannot establish useful behavior. Where a behavior should not occur, include cases where it should occur too, so the suite does not reward an agent that never acts.
3. **Specify the fixture.** Define the controlled starting world: revisioned data and identity/permission state, dependencies, initialization, isolation, any permitted live boundary, reset and reset verification, and the authoritative source that can establish the outcome. The fixture is what the case starts with; the reference or observation determines whether a claim holds.
4. **Choose evaluator and trials.** Select an evaluator that can judge the claim, document its identity and rule, and establish its fitness ([4.4](04-evaluators-metrics-rubrics-and-calibration.md)). Before running, state what counts as pass, fail, invalid, or inconclusive, and how repeats, retries, variants, and missing observations are treated ([4.7](07-analyzing-results-comparing-versions-and-making-decisions.md)).
5. **Run and preserve evidence.** Identify the exact candidate configuration, case and fixture revisions, evaluator version, trial conditions, outcome, status, and relevant observation. Keep cost/resource evidence where those are claims. Identical wording is not the test of reproducibility: repeated episodes should start from verified conditions, while acceptable wording or safe routes may vary.
6. **Triage, learn, and hand off.** Separate candidate behavior from fixture, harness, dependency, or evaluator defects, and read the transcripts to tell which it is. Keep every attempted run and its status. Fix an evaluation defect only under a predeclared, visible rule; keep invalid records and rerun affected evidence. A confirmed, privacy-reviewed production failure can become a regression case with clear expected behavior. Pass attributed results and evidence limits to analysis ([4.7](07-analyzing-results-comparing-versions-and-making-decisions.md)).

Make each record linkable through stable IDs, not filenames or copied transcripts. Keep candidate, case, fixture, evaluator, trial, and evidence identities together so a reviewer can trace a result to the conditions that produced it.

## Cases, suites, and independent holdouts

A case is a bounded probe, not just a prompt and a preferred response. Record why it exists, what it tests, which outcomes are acceptable, which path conditions matter, and which harmless variations are allowed. If the claim concerns current evidence, include the older or conflicting evidence that could trigger the failure; a current-only fixture cannot expose stale-source selection. If missing evidence should give `needs_information`, make that the expected outcome.

Keep suite purpose explicit: development cases guide iteration; regression cases preserve reviewed behavior; capability cases measure hard tasks and are expected to fail often ([4.2](02-test-levels-techniques-and-suite-purposes.md)); an acceptance set supports a stated stakeholder decision; a release holdout supplies evidence not used to tune the reported behavior. A holdout must differ in more than label: protect its access and use, and use separately authored tasks and fixtures. Re-running development cases under a new name does not make a holdout. If a holdout is exposed or used to change prompts, rules, rubrics, or case selection, record the loss of independence and build a fresh holdout before any claim that depends on it. Publishing a benchmark's test data in plain text lets it leak into training data, so keep holdout material out of public and indexable places.[5]

For indirect prompt-injection cases, harmless marker content and instrumented destinations show whether attempted content reaches a boundary; a clean final answer does not show that no disclosure or action occurred.[3] Fixed injection cases are a smoke test, not a security benchmark. Evidence of resistance needs adaptive or red-team attacks that iterate against the system ([4.3](03-evaluation-types-and-dimensions.md)).

Build cases from representative requirements, reviewed adverse scenarios, and resolved failures. A report or incident is not automatically a valid case: first remove or transform sensitive material, settle the expected behavior with an accountable reviewer, and record provenance without keeping unnecessary raw user content. Do not make raw transcripts the default source of truth.

## Fixtures, isolation, and safe data handling

A fixture controls the conditions needed to interpret a trial; it does not make a stochastic agent produce identical text. For a read-only policy assistant, the world might be a current approved document, a superseded version, a user with a defined permission, a fixed clock, and a per-run retrieval log. For a system with effects, also capture the relevant boundary and authoritative state; a transcript is not proof an external action did or did not occur.

Start every trial from a clean state. Leftover files, caches, records, or memory from an earlier trial can inflate or hide results and make trials depend on each other. Prefer fresh per-run namespaces over shared mutable state. Before each run, initialize from the declared fixture revision and verify the fields material to the claim: source identities and revisions, permissions, relevant state, and empty event records. Afterward, reset and verify again. If a reset cannot be verified, do not call the next trial an independent fresh-world run. State any live services or mutable inputs, and record what they exposed.

Use synthetic or minimized data where it can establish the claim. Restrict access to evaluation records, separate identifiers from user content when possible, and keep only the evidence needed for the decision and later review. If production-derived material is necessary, sanitize it through an authorized process before reuse. Keep credentials, secrets, and unnecessary personal content out of cases, fixtures, logs, and examples. Privacy and retention rules for a deployment belong to its governing policy.

Use a small, explicit fixture contract. A controlled dependency should reproduce the failure shapes the claim needs, such as denial, timeout, or malformed or partial response, not only the happy path. Do not add a live dependency for realism if a controlled substitute can establish the claim safely; when the live boundary is essential, say why and how its variation is observed.

## Worked example: current policy, denied access, and a separate holdout

The example is fictional and unexecuted. The policy assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources and cites them, with no persisted memory, external write, approval flow, or delegated agent. In the development/regression fixture, the current London hotel value is GBP 220. An earlier case held only the current document, so it could not reveal whether the assistant would pick a superseded source when both were available. The revised case keeps the stale document visible as a plausible distractor.

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

For each run, initialize a fresh namespace and verify source revisions, permission, and the per-run log before asking the question. Evaluate the answer against the fixture's current source and the grounding rubric; inspect permission and boundary observations separately from the semantic judgment. Then discard and recreate the namespace and verify the reset before the next trial. A correct value with an unsupported citation is not a grounding pass, and a blocked out-of-scope retrieval proposal differs from an actual unauthorized retrieval. This read-only design implies no external-write check.

The other shared cases give contrasts: `POLICY-STALE-002`, `POLICY-MISSING-003`, `POLICY-CONFLICT-004`, `POLICY-DENIED-005`, `POLICY-INJECTION-006`, `POLICY-PARAPHRASE-007`, and `POLICY-EXHAUSTION-008`. `POLICY-HOLDOUT-009` stays independently authored with its own task and fixture; do not substitute development cases under that ID. A missing-evidence case checks for a bounded outcome, a current-policy conflict checks that no definitive amount is invented, a denied case observes permission enforcement and disclosure separately, and a paraphrase pair counts only after review confirms the meaning is preserved. If behavior varies materially, declare fresh trials and their decision unit in advance; the example sets no universal count.

A curated suite shows results for the cases and conditions it holds. NIST's Generative AI Profile cautions against extrapolating from narrow, nonsystematic, or anecdotal assessments.[2] The example specifies design, not results. Reusable record structures are in the [practical reference](reference/README.md).

## Requirements

- **CASE-02 — Case identity, purpose, and holdout independence.** When curated cases support a behavior, safety, or usefulness claim, each case **MUST** have a stable identity, versioned input, origin or rationale, applicable capability/risk tags, expected observable outcome or invariants, allowed variation, and stated suite purpose, with its trial records linkable to those identities. A release holdout used to support a claim of independence from tuning **MUST** remain separate from cases used to tune the reported behavior; it **MUST** use independently authored task/fixture material rather than development or regression cases relabelled as untouched. Teams **SHOULD** add confirmed failures to regression suites only after review establishes expected behavior and sensitive source material has been sanitized.

- **CASE-03 — Controlled fixture contract.** When a case depends on documents, identity or permission data, tools, external state, time, randomness, or another dependency, the fixture **MUST** identify its revision, initialization, per-run isolation boundary, permitted live boundary, reset method, reset verification, and authoritative outcome observation. The evaluation **MUST NOT** treat an unverified reset or mutable shared state as evidence that independent trials began in the same controlled world. Fixture and evidence handling **MUST** use only data authorized and proportionate to the claim, with sensitive material minimized or sanitized before case reuse.

- **CASE-05 — Execution evidence and failure intake.** Each case execution relied on as evidence **MUST** retain the evaluated candidate/configuration identity, case and fixture revisions, evaluator identity/version, trial conditions, outcome observations, and a status that distinguishes pass, fail, invalid, and inconclusive execution. Invalid and inconclusive executions **MUST** remain visible with their reason; neither is a pass or a basis for silently removing a result from the record. Production-derived cases **MUST** be sanitized and classified before reuse. A confirmed candidate failure **MUST NOT** be discarded or relabelled invalid because an aggregate score remains acceptable or an evaluation component also fails. A harness/evaluator defect may support a replacement run only under a predeclared repair rule that retains the invalid record, preserves the candidate and semantic claim/scope, records the repair rationale, and reruns affected evidence without relaxing criteria. Where the observed candidate behavior itself establishes a failure, it remains a candidate failure.

## Evidence and checklist

Keep the versioned claim/case map, case and fixture inventory, evaluator/trial policy, and attributed execution records needed to trace each result. Before handing results to analysis, check:

- [ ] Each case has a stable ID, versioned input, rationale, tags, observable expectation, allowed variation, and suite purpose.
- [ ] Cases include ones where a behavior should occur and ones where it should not.
- [ ] A release holdout has its own protected use boundary and independently authored task/fixture, and was not used to tune the reported candidate or evaluator.
- [ ] Fixture revision, initialization, isolation, live boundaries, reset procedure, reset verification, and authoritative observation are explicit, and every trial starts clean.
- [ ] Data is synthetic or minimized where practicable; production-derived material is authorized, sanitized, classified, and no more revealing than needed.
- [ ] Each trial identifies candidate configuration, case, fixture, evaluator, fixed/random conditions, observations, and visible status.
- [ ] Invalid or inconclusive runs keep their reasons; no rerun or repair hides a candidate failure or relaxes the claim.
- [ ] Failures were read in transcripts to separate agent defects from fixture, harness, or grader defects.
- [ ] Evaluator and trial policy fit the claim; repeats are not called independent when conditions were shared or reset was unverified.
- [ ] Confirmed, reviewed production failures can enter regression without unnecessary raw user data.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[3]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
[4]: https://www.anthropic.com/engineering/multi-agent-research-system "Anthropic: How we built our multi-agent research system"
[5]: https://aclanthology.org/2023.emnlp-main.308 "Stop Uploading Test Data in Plain Text: Practical Strategies for Mitigating Data Contamination by Evaluation Benchmarks"

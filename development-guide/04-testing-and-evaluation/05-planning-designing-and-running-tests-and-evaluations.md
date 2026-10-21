# 4.5 Planning, Designing, and Running Tests and Evaluations

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Agent builders, evaluation designers, reviewers, and accountable owners  
**Applicability:** Production candidates and changes whose test or evaluation evidence supports a design, pilot, release, or operational decision. Fit methods and depth to the claims, capabilities, and risks in scope.  
**Reader question:** How do I build and operate an evaluation process?

[Part 4 — Testing and Evaluation](README.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) · [Practical reference](reference/README.md)

## From a claim to an interpretable result

Start with a question that matters, not a convenient score: what must the agent do, what must it never do, and which capability, dependency, or risk could change the answer? Keep each claim narrow enough for a case to exercise. [4.6](06-standards-required-coverage-and-execution-cadence.md) owns the coverage map and profile triggers; this chapter turns selected claims into executions.

Evidence is ongoing input, not a one-time certificate: NIST's AI RMF says AI systems should be tested before deployment and regularly during operation,[1] though it sets no test count or pass threshold. Start small: early changes tend to have large effects, so about 20 tasks from real usage already show whether a change helped;[4] 20 to 50 tasks drawn from real failures make a good first suite, which you grow as new failures appear.[6]

The working chain:

1. **Map claim to case and profile.** Record the claim, decision role, profile, case or case family, owner, stage, and the reason for any profile marked not applicable. A case may serve several claims if their expectations and evidence stay distinguishable.
2. **Design cases with purpose** (CASE-02). Mix ordinary answerable work with missing, stale, conflicting, denied, malformed, or adverse conditions; a suite without should-act cases rewards an agent that never acts.
3. **Specify the fixture** (CASE-03, below). The fixture is the starting world; the reference or observation decides whether the claim holds.
4. **Choose evaluator and trials.** Pick an evaluator fit for the claim ([4.4](04-evaluators-metrics-rubrics-and-calibration.md)). Before running, state what counts as pass, fail, invalid, or inconclusive, and how repeats, retries, variants, and missing observations are treated ([4.7](07-analyzing-results-comparing-versions-and-making-decisions.md)).
5. **Run and preserve evidence** (CASE-05), including claimed cost/resource evidence. Reproducibility means verified starting conditions, not identical wording; acceptable wording and safe routes may vary.
6. **Triage and learn.** Read the transcripts to separate candidate behavior from fixture, harness, dependency, or evaluator defects. Keep every run and its status; repair evaluation defects only under CASE-05's predeclared rule. A confirmed, privacy-reviewed production failure can become a regression case.

Link records by stable IDs, not filenames or copied transcripts, so each result traces to the candidate, case, fixture, evaluator, and trial that produced it.

## Cases, suites, and independent holdouts

A case is a bounded probe, not a prompt plus preferred response. For a currentness claim, include the older or conflicting evidence that could trigger the failure; a current-only fixture cannot expose stale-source selection. If missing evidence should give `needs_information`, make that the expected outcome.

Suite purposes are in [4.2](02-test-levels-techniques-and-suite-purposes.md). A release holdout must differ in more than label: protect its access and use and author its tasks and fixtures separately. If a holdout is exposed or used to change prompts, rules, rubrics, or case selection, record the loss of independence and build a fresh one before any claim that depends on it. Test data published in plain text leaks into training data, so keep holdout material out of public and indexable places.[5]

For indirect prompt injection, harmless marker content and instrumented destinations show whether injected content reaches a boundary; a clean final answer does not show that nothing was disclosed or done.[3] Fixed injection cases are a smoke test; resistance evidence needs adaptive or red-team attacks ([4.3](03-evaluation-types-and-dimensions.md)).

Build cases from representative requirements, reviewed adverse scenarios, and resolved failures. An incident becomes a case only after sensitive material is removed or transformed, an accountable reviewer settles the expected behavior, and provenance is recorded without unnecessary raw content; raw transcripts are not the default source of truth.

## Fixtures, isolation, and safe data handling

A fixture controls the conditions needed to interpret a trial; it does not make a stochastic agent produce identical text. With effects, also capture the boundary and authoritative state; a transcript does not prove an external action did or did not occur.

Start every trial from clean state: leftover files, caches, records, or memory can inflate or hide results and couple trials. Prefer fresh per-run namespaces to shared mutable state, and verify the fields material to the claim (source identities and revisions, permissions, relevant state, empty event records) before and after each run. Name any live services or mutable inputs and record what they exposed.

Use synthetic or minimized data where it can establish the claim. Restrict access to evaluation records, separate identifiers from content where possible, keep only the evidence needed, and sanitize production-derived material through an authorized process. Keep credentials, secrets, and unnecessary personal content out of cases, fixtures, logs, and examples; retention follows the deployment's governing policy.

A controlled dependency should reproduce the failure shapes the claim needs (denial, timeout, malformed or partial response), not only the happy path. Prefer it to a live dependency when it can establish the claim safely; when a live boundary is essential, say why and how its variation is observed.

## Worked example: current policy, denied access, and a separate holdout

This fictional, unexecuted example uses the ephemeral, read-only policy assistant (no memory, writes, approvals, or delegation). An earlier case held only the current document, so it could not show whether the assistant would pick a superseded source; the revised case keeps the stale document visible as a plausible distractor.

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
  attempt: "record every physical attempt, including retries"
  status: "pass | fail | invalid | inconclusive"
  observation: "response, cited source/revision, permission decision, and event log"
holdout:
  suite: "policy-release-holdout@v1"
  case: "POLICY-HOLDOUT-009"
  fixture: "separately authored and maintained holdout fixture"
  use: "not used to tune the candidate or evaluator reported on it"
```

Each run initializes, resets, and verifies as the fixture specifies. The answer is judged against the current source and grounding rubric, with permission and boundary observations kept separate from the semantic judgment. A correct value with an unsupported citation is not a grounding pass, and a blocked out-of-scope retrieval proposal is not an unauthorized retrieval. The read-only design implies no external-write check.

The other shared cases are contrasts: `POLICY-STALE-002`, `POLICY-MISSING-003` (bounded outcome), `POLICY-CONFLICT-004` (no invented amount), `POLICY-DENIED-005` (enforcement and disclosure observed separately), `POLICY-INJECTION-006`, `POLICY-PARAPHRASE-007` (counts only after review confirms meaning), and `POLICY-EXHAUSTION-008`. `POLICY-HOLDOUT-009` keeps its own independently authored task and fixture; never substitute development cases under that ID. If behavior varies materially, declare fresh trials and their decision unit in advance.

A curated suite shows results only for the cases and conditions it holds; NIST's Generative AI Profile cautions against extrapolating from narrow, nonsystematic, or anecdotal assessments.[2]

## Requirements

- **CASE-02 — Case identity, purpose, and holdout independence.** When curated cases support a behavior, safety, or usefulness claim, each case **MUST** have a stable identity, versioned input, origin or rationale, applicable capability/risk tags, expected observable outcome or invariants, allowed variation, and stated suite purpose, with its trial records linkable to those identities. A release holdout used to support a claim of independence from tuning **MUST** remain separate from cases used to tune the reported behavior; it **MUST** use independently authored task/fixture material rather than development or regression cases relabelled as untouched. Teams **SHOULD** add confirmed failures to regression suites only after review establishes expected behavior and sensitive source material has been sanitized.

- **CASE-03 — Controlled fixture contract.** When a case depends on documents, identity or permission data, tools, external state, time, randomness, or another dependency, the fixture **MUST** identify its revision, initialization, per-run isolation boundary, permitted live boundary, reset method, reset verification, and authoritative outcome observation. The evaluation **MUST NOT** treat an unverified reset or mutable shared state as evidence that independent trials began in the same controlled world. Fixture and evidence handling **MUST** use only data authorized and proportionate to the claim, with sensitive material minimized or sanitized before case reuse.

- **CASE-05 — Execution evidence and failure intake.** Each case execution relied on as evidence **MUST** retain the evaluated candidate/configuration identity, case and fixture revisions, evaluator identity/version, trial conditions, outcome observations, and a status that distinguishes pass, fail, invalid, and inconclusive execution. Invalid and inconclusive executions **MUST** remain visible with their reason; neither is a pass or a basis for silently removing a result from the record. Production-derived cases **MUST** be sanitized and classified before reuse. A confirmed candidate failure **MUST NOT** be discarded or relabelled invalid because an aggregate score remains acceptable or an evaluation component also fails. A harness/evaluator defect may support a replacement run only under a predeclared repair rule that retains the invalid record, preserves the candidate and semantic claim/scope, records the repair rationale, and reruns affected evidence without relaxing criteria. Where the observed candidate behavior itself establishes a failure, it remains a candidate failure.

## Evidence and checklist

Keep the versioned claim/case map, case and fixture inventory, evaluator/trial policy, and execution records. Before analysis, check:

- [ ] Each case has a stable ID, versioned input, rationale, tags, observable expectation, allowed variation, and suite purpose (CASE-02).
- [ ] Cases include ones where a behavior should occur and ones where it should not.
- [ ] A release holdout has protected use and independently authored tasks and fixtures, and was not used to tune what it reports on.
- [ ] Fixture revision, initialization, isolation, live boundary, reset, reset verification, and authoritative observation are explicit (CASE-03).
- [ ] Every trial starts from a verified clean state.
- [ ] Data is synthetic or minimized where practicable; production-derived material is authorized, sanitized, and classified.
- [ ] Each trial records candidate, case, fixture, evaluator, conditions, observations, and a visible status; invalid or inconclusive runs keep their reason (CASE-05).
- [ ] Failures were read in transcripts to separate agent defects from fixture, harness, or grader defects; no rerun or repair hides a candidate failure.
- [ ] Repeats are not called independent when conditions were shared or reset was unverified.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[3]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP LLM Prompt Injection Prevention Cheat Sheet"
[4]: https://www.anthropic.com/engineering/multi-agent-research-system "Anthropic: How we built our multi-agent research system"
[5]: https://aclanthology.org/2023.emnlp-main.308 "Stop Uploading Test Data in Plain Text: Practical Strategies for Mitigating Data Contamination by Evaluation Benchmarks"
[6]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"

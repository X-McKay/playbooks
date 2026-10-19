# Troubleshooting Evaluation Evidence

**Status:** 0.5.0-draft.2 assembled draft — illustrative, unexecuted practical guidance, not a failure taxonomy
**Audience:** Builders, evaluators, reviewers, and accountable decision owners  
**Applicability:** Use when an observed result and the evidence record do not support the same conclusion.  
**Reader question:** What should we inspect before we trust, discard, or rerun an evaluation result?

[Practical reference](README.md) · [Worked example](policy-assistant-worked-example.md) · [Planning and running](../05-planning-designing-and-running-tests-and-evaluations.md) · [Evaluators](../04-evaluators-metrics-rubrics-and-calibration.md) · [Analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md)

Start with the smallest claim that is in doubt. Preserve the candidate, case, fixture, evaluator, trial policy, and observed status before changing anything. A new score is useful only when it can be connected to the same claim or a clearly declared replacement claim.

## The score improved, but users report more failures

### Likely causes — score and user mismatch

- The aggregate score masks a new failure in a critical capability, permission context, language, role, or other relevant slice.
- The development set was tuned while the independent holdout or production signal was not inspected.
- The candidate, route, fallback, source corpus, or evaluator changed, so the two scores do not describe the same subject.
- A user report is real but not yet attributable; it may expose a fixture, evaluator, or environment gap rather than prove the candidate caused the outcome.

### Evidence to gather — score and user mismatch

- The exact candidate and baseline/configuration identities, including route or fallback where used.
- Case-level flips rather than only aggregate values, especially the affected task and control slice.
- The source, fixture, permission, evaluator, and trial identities for the reported scenario.
- A privacy-appropriate, attributable description of the user report and the result of reproducing it against controlled conditions.
- Whether the reported behavior was represented by a held-out case, a development case, or neither.

### Remedy — score and user mismatch

Do not treat the higher aggregate as a resolution. Triage the report, preserve necessary evidence, and decide whether it is attributable. If confirmed, sanitize it, define the expected behavior with the accountable owner, and add a reviewed versioned regression case for future comparisons. Re-run affected claim-fit cases and critical controls against the identified candidate. A curated suite can reveal an important defect but does not, by itself, justify a broad claim about all users. [1]

For the policy assistant, an answer that appears improved overall but returns a superseded policy to one requester calls for a currentness and permission review. It should not be offset by successful common questions.

## A judge passes an unsupported answer

### Likely causes — unsupported judge passes

- The judge saw a citation identifier or relevant-looking source but not the material claim and supporting source span.
- The rubric combines source permission, source currentness, factual truth, and semantic support into one vague criterion.
- The judge is sensitive to answer style, position, verbosity, candidate metadata, or instructions embedded in supplied content.
- The judge has not been shown independently reviewed conflict, stale-source, or plausible-but-unsupported examples that resemble the release claim.

### Evidence to gather — unsupported judge passes

- The exact rubric, judge identity/configuration, allowed evidence, context packing, and structured result.
- A claim-to-source map for each material statement, including the supporting span or the absence/contradiction of support.
- Known-pass and known-failure self-test results: supported paraphrase, plausible unsupported addition, stale-source answer, conflict case, and missing-evidence response.
- Independent qualified human labels, reviewer provenance, disagreement disposition, and the judge’s false-pass examples for the relevant claim class.

### Remedy — unsupported judge passes

Keep the judge diagnostic-only until its documented fitness matches the exact intended gate. Narrow the rubric to the semantic-support claim and use deterministic source/permission checks separately. For a release-facing policy-support claim, retain qualified human review unless there is documented gate fitness for the applicable task and risk slice. Do not promote a diagnostic pass into semantic evidence merely because it is convenient. Citation presence and topical relevance are not proof that a material claim is supported. [2]

## Retries hide the initial failure

### Likely causes — hidden retries

- The record stores only the selected final response and discards failed physical attempts.
- Retry eligibility, bound, selection rule, and reset behavior were never declared.
- The reported `pass@k` value is being read as first-attempt reliability, all-attempt consistency, or safe external-effect behavior.
- A retry reused mutable state, hid a timeout, or changed the source world without recording it.

### Evidence to gather — hidden retries

- Every physical attempt, its outcome, reason for retry, fixture/reset result, calls, latency, cost, and final delivered result.
- The released retry, routing, fallback, or selection rule—not an imagined evaluation-only rule.
- The distinction between a valid candidate failure, an invalid harness episode, and an inconclusive judgment.
- For any effecting variant, the relevant authorization and authoritative state observation before considering another attempt.

### Remedy — hidden retries

Report per-attempt outcomes and the end-to-end final policy result separately. Bind the evaluation to the actual released retry/selection policy. Do not describe at-least-one success as a reliable single attempt, and do not let a hidden retry repair an external-effect claim. A failed first attempt remains evidence even if a later attempt provides the user with a good answer.

The illustrated policy assistant has no retry policy. If a later read-only version adds a retry after a transient retrieval timeout, its record needs both the failed first attempt and the eventual response. A future write-capable version requires separate effect, authorization, approval, and reconciliation evidence; the current example cannot establish it.

## The citation resolves, but the response is still wrong

### Likely causes — citation and correctness

- The answer uses a current permitted source but adds an unsupported exception or combines passages incorrectly.
- The answer is grounded in a source that is not the chosen authoritative truth source for the time or jurisdiction.
- A superseded or conflicting source was made to look current by missing metadata or an ambiguous source-precedence rule.

### Evidence to gather — citation and correctness

- Source identity, status, revision, approval scope, permission decision, and relevant time.
- The exact text supporting each material answer statement.
- The separately defined external truth reference if the product makes a factual-correctness claim beyond the approved policy fixture.
- The qualified reviewer’s rubric result and any material ambiguity or disagreement.

### Remedy — citation and correctness

Separate the repair target. Fix source admission/currentness when the wrong source was eligible; fix synthesis or grounding when the source does not support the answer; add or revise the external truth reference only when factual correctness is actually a declared claim. Do not weaken semantic review into a citation-format check. The worked example’s GBP 220 fact establishes only the fictional fixture claim, not a real-world travel-policy truth.

## A denial case passes, but permitted users cannot get an answer

### Likely causes — over-refusal

- The suite contains adverse or denied cases without a comparable permitted counterpart.
- The policy assistant treats missing, denied, conflicting, and answerable evidence as the same refusal condition.
- Permission context is not propagated into the fixture or recorded at the retrieval boundary.

### Evidence to gather — over-refusal

- Matched permitted and denied requests with the same task except for the authority-relevant change.
- Permission decisions, retrieved source identities, and the terminal output for both cases.
- The expected contract outcome for missing evidence, denied access, and sufficient evidence.

### Remedy — over-refusal

Keep the denied case, then add or repair the permitted counterpart. Score appropriate restraint and over-refusal separately. For the policy assistant, `POLICY-CURRENT-001` demonstrates a permitted complete answer, while `POLICY-DENIED-005` demonstrates scope enforcement. Neither result replaces the other.

## A run cannot be reproduced after a fixture or evaluator problem

### Likely causes — reproduction and repair

- The fixture revision, source status, requester permissions, reset verification, evaluator version, or candidate identity was not retained.
- A shared mutable world or unverified reset contaminated later trials.
- A harness repair changed the semantic case, input population, evaluator, or comparison rule after results were seen.

### Evidence to gather — reproduction and repair

- The case, fixture, candidate, evaluator, and trial-policy identities; reset record; status; and diagnostic material.
- The predeclared invalid/inconclusive and replacement-run rule.
- A comparison of the repair with the original case: input scope, expected invariants, thresholds, and candidate must remain unchanged for a like-for-like replacement.

### Remedy — reproduction and repair

Preserve the invalid or inconclusive record. Repair only under the predeclared replacement rule, document why the repair cannot bias attribution, and re-run all affected paired evidence under the same repaired conditions. If valid required evidence is still absent at decision time, the appropriate conclusion is an evidence gap, not a pass. An independently observable candidate failure remains a candidate failure even if a later evaluator problem is also discovered.

## An injection test reports a clean answer but cannot show containment

### Likely causes — injection containment

- The injection was placed in the user message rather than the untrusted document or tool-output channel under test.
- The fixture has no instrumented boundary observation for attempted retrieval, disclosure, or invocation.
- A clean response is being treated as proof that no restricted data reached an unpermitted recipient.

### Evidence to gather — injection containment

- The channel containing the untrusted material, source status, requester scope, and harmless test marker.
- Boundary logs for attempted retrieval and invocation, plus an output/recipient observation for disclosure.
- A permitted benign counterpart so blanket refusal does not appear safe by itself.

### Remedy — injection containment

Move the attack into the actual untrusted channel and use harmless fixture data. Grade terminal outcome, source scope, attempted capability use, boundary decision, and disclosure separately. A correctly blocked proposal is not an unauthorized external execution; it may still be a policy-compliance concern under a separately declared claim.

## Quick evidence check

Before changing the candidate or the score, confirm:

- [ ] The disputed claim is named narrowly enough to choose a fit-for-purpose check or review.
- [ ] Candidate, fixture, case, evaluator, and trial policy identities are present.
- [ ] The record distinguishes pass, fail, invalid, and inconclusive rather than silently dropping inconvenient runs.
- [ ] Source permission/currentness, semantic support, trajectory/boundary evidence, and external truth are not represented by one proxy score.
- [ ] The holdout, if used for a release claim, was not used to tune the behavior reported on it.
- [ ] A model judge’s documented role is respected; diagnostic output has not become a hidden gate.
- [ ] The next action repairs the relevant evidence gap rather than merely producing another favorable transcript.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[2]: https://aclanthology.org/2024.acl-long.585/ "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models"

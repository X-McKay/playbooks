# Troubleshooting Evaluation Evidence

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable decision owners  
**Applicability:** When an observed result and the evidence record do not support the same conclusion.  
**Reader question:** What should we inspect before we trust, discard, or rerun an evaluation result?

[Practical reference](README.md) · [Worked example](policy-assistant-worked-example.md) · [Planning and running](../05-planning-designing-and-running-tests-and-evaluations.md) · [Evaluators](../04-evaluators-metrics-rubrics-and-calibration.md) · [Analysis and decisions](../07-analyzing-results-comparing-versions-and-making-decisions.md)

Start with the smallest claim in doubt, and keep the candidate, case, fixture, evaluator, trial policy, and status before changing anything; a new score helps only if it ties to the same claim or a declared replacement. In every case below, read the transcripts and graded outputs first to see whether the agent, fixture, or grader is at fault.

## The score improved, but users report more failures

**Likely causes.**

- The aggregate hides a new failure in a critical capability, permission context, language, role, or other slice.
- The development set was tuned while the holdout or production signal went unchecked.
- The candidate, route, fallback, corpus, or evaluator changed, so the scores describe different subjects.
- The report is real but not yet attributable, perhaps pointing to a fixture, evaluator, or environment gap.

**Gather.**

- Exact candidate and baseline/configuration identities, including route or fallback.
- Case-level flips, not only aggregates, especially for the affected task and control slice.
- Source, fixture, permission, evaluator, and trial identities for the reported scenario.
- A privacy-appropriate description of the report and its controlled reproduction.
- Whether a held-out case, a development case, or neither covered the behavior.

**Remedy.** A higher aggregate resolves nothing. Triage for attribution; if confirmed, sanitize, define expected behavior with the owner, add a reviewed, versioned regression case, and rerun affected cases and critical controls on the identified candidate. A curated suite can reveal a real defect but does not justify claims about all users.[1] A policy assistant that improves overall but returns a superseded policy to one requester needs currentness and permission review; common-question successes do not offset it.

## A judge passes an unsupported answer

**Likely causes.**

- The judge saw a citation or relevant-looking source but not the material claim and its supporting span.
- The rubric mixes source permission, currentness, factual truth, and semantic support into one vague criterion.
- The judge is sensitive to style, position, verbosity, candidate metadata, or instructions inside supplied content.
- The judge was never calibrated on independently reviewed conflict, stale-source, or plausible-but-unsupported examples.

**Gather.**

- Rubric, judge identity and configuration, allowed evidence, context packing, and structured result.
- A claim-to-source map for each material statement, with the supporting span or the absence or contradiction of support.
- Self-test results: supported paraphrase, plausible unsupported addition, stale-source answer, conflict case, missing-evidence response.
- Independent qualified human labels, reviewer provenance, disagreement disposition, and the judge's false passes for that claim class.

**Remedy.** Keep the judge diagnostic-only until documented fitness matches the intended gate, and keep qualified human review for release-facing support claims until then. Narrow the rubric to semantic support and run source and permission checks separately. Citation presence and topical relevance do not prove support; RAGTruth shows unsupported claims persist under retrieval.[2]

## Retries hide the initial failure

**Likely causes.**

- The record stores only the selected final response and drops failed physical attempts.
- Retry eligibility, bound, selection rule, and reset behavior were never declared.
- A `pass@k` value is read as first-attempt reliability, all-attempt consistency, or safe external-effect behavior.
- A retry reused mutable state, hid a timeout, or changed the source world unrecorded.

**Gather.**

- Every physical attempt: outcome, retry reason, fixture/reset result, calls, latency, cost, and the final delivered result.
- The released retry, routing, fallback, or selection rule, not an evaluation-only one.
- Which failures are valid candidate failures, invalid harness episodes, or inconclusive judgments.
- For an effecting variant, the authorization and authoritative state observation before another attempt.

**Remedy.** Report per-attempt outcomes and the end-to-end result separately, bound to the released retry/selection policy. At-least-one success is not a reliable single attempt, and a hidden retry cannot repair an external-effect claim. A failed first attempt stays evidence even if a later one succeeds; a future read-only retry would record both. A write-capable version needs separate effect, authorization, approval, and reconciliation evidence.

## The citation resolves, but the response is still wrong

**Likely causes.**

- The answer uses a current permitted source but adds an unsupported exception or combines passages wrongly.
- The answer is grounded in a source that is not authoritative for the time or jurisdiction.
- A superseded or conflicting source looks current because of missing metadata or an ambiguous precedence rule.

**Gather.**

- Source identity, status, revision, approval scope, permission decision, and relevant time.
- The exact text supporting each material statement.
- An external truth reference if the product claims correctness beyond the fixture.
- The qualified reviewer's rubric result and any ambiguity or disagreement.

**Remedy.** Fix the right target: source admission or currentness when the wrong source was eligible; synthesis or grounding when the source does not support the answer; an external truth reference only when correctness is a declared claim. Never weaken semantic review into a citation-format check. GBP 220 establishes only the fictional fixture claim.

## A denial case passes, but permitted users cannot get an answer

**Likely causes.**

- The suite has denied cases without comparable permitted counterparts.
- The assistant treats missing, denied, conflicting, and answerable evidence as one refusal condition.
- Permission context is not passed into the fixture or recorded at the retrieval boundary.

**Gather.**

- Matched permitted and denied requests that differ only in the authority-relevant change.
- Permission decisions, retrieved source identities, and terminal output for both.
- The expected outcome for missing evidence, denied access, and sufficient evidence.

**Remedy.** Keep the denied case, add or repair the permitted counterpart, and score restraint and over-refusal separately. `POLICY-CURRENT-001` (permitted answer) and `POLICY-DENIED-005` (scope enforcement) never replace each other.

## A run cannot be reproduced after a fixture or evaluator problem

**Likely causes.**

- The fixture revision, source status, requester permissions, reset verification, evaluator version, or candidate identity was not kept.
- A shared mutable world or unverified reset contaminated later trials.
- A harness repair changed the semantic case, input population, evaluator, or comparison rule after results were seen.

**Gather.**

- Case, fixture, candidate, evaluator, and trial-policy identities; reset record; status; diagnostic material.
- The predeclared invalid/inconclusive and replacement-run rule.
- A comparison of repair and original: input scope, invariants, thresholds, and candidate must be unchanged for a like-for-like replacement.

**Remedy.** Keep the invalid or inconclusive record, repair only under the predeclared rule with a non-bias rationale, and rerun all affected paired evidence. Required valid evidence still absent at decision time is an evidence gap, not a pass. An independently observable candidate failure stays one even if an evaluator problem is found.

## An injection test reports a clean answer but cannot show containment

**Likely causes.**

- The injection was put in the user message instead of the untrusted document or tool-output channel under test.
- The fixture has no instrumented boundary observation for attempted retrieval, disclosure, or invocation.
- A clean response is treated as proof that no restricted data reached an unpermitted recipient.
- The attacks are a fixed list, which shows only that known attacks fail; resistance needs adaptive or red-team attacks.

**Gather.**

- The channel holding the untrusted material, source status, requester scope, and harmless test marker.
- Boundary logs for attempted retrieval and invocation, plus an output/recipient observation for disclosure.
- A permitted benign counterpart so blanket refusal does not look safe.

**Remedy.** Move the attack into the real untrusted channel with harmless data. Grade outcome, source scope, attempted capability use, boundary decision, and disclosure separately. A blocked proposal is not an unauthorized execution, though it may fail a separately declared compliance claim.

## Quick evidence check

- [ ] The disputed claim is narrow enough to choose a fit check.
- [ ] Identities and pass/fail/invalid/inconclusive statuses are kept, with no silently dropped runs.
- [ ] Permission/currentness, support, boundary evidence, and truth are not one proxy score.
- [ ] No release holdout was used for tuning, and no diagnostic judge became a hidden gate.
- [ ] The next action repairs the evidence gap instead of producing another favorable transcript.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST Artificial Intelligence Risk Management Framework Generative AI Profile"
[2]: https://aclanthology.org/2024.acl-long.585/ "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models"

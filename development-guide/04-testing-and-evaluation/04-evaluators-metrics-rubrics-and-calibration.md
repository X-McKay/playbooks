# 4.4 Evaluators, Metrics, Rubrics, and Calibration

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, qualified domain reviewers, and accountable owners  
**Applicability:** Use this chapter whenever evaluation evidence supports a design, change, pilot, or release decision. The model-judge guidance applies only when you use a model to judge. Coverage, cases, and fixtures are in [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.6](06-standards-required-coverage-and-execution-cadence.md).  
**Reader question:** How do I turn observations into a trustworthy judgment?

[Part 4](README.md) · [Applicability and conformance](../../applicability.md) · [Evaluation dimensions](03-evaluation-types-and-dimensions.md) · [Planning and running](05-planning-designing-and-running-tests-and-evaluations.md) · [Practical reference](reference/README.md)

An evaluation is only as useful as the link between its claim, its evidence, and its evaluator. Start with a narrow statement that could be wrong, then pick the least burdensome method that can establish it. A fluent answer, a resolved citation, or a good aggregate score is not evidence for every nearby claim.

## Start with a claim, not a score

A **metric** says what is measured and how results are summarized, such as the share of cases reaching a required terminal outcome, or the count of unsupported material assertions. An **evaluator** is the versioned rule, procedure, instrument, or qualified role that turns evidence into the judgment the metric uses. The metric is not the instrument, and an instrument's output does not widen the claim it can establish.

An **evidence source** supplies the thing inspected: approved policy text, a permission decision, a fixture, an authoritative state read, a reference label, or a response. The evaluator supplies the comparison or judgment. Reserve *oracle* for a named, claim-specific answer or state provider whose authority, scope, time, and limits are stated.

For every material claim, write its counterexample before choosing a method. "A citation is present" has an easy one: the response cites a relevant-looking passage that does not support its invented exception. This exposes a score that measures a proxy.

### Select the simplest capable method

Combine methods when a claim has several parts; later methods do not make earlier evidence unnecessary.

- Use a **deterministic assertion** for a decidable property: an output field, a permitted source identifier and revision, an absent forbidden invocation, an exact value in a fixture. It establishes only the encoded property.
- Use an **approved-source comparison** when the claim concerns a source's content, status, permission, or currency. Record source identity, revision or as-of time, and the permission decision.
- Use an **authoritative state observation** to establish an actual effect or its absence. An agent transcript reporting a completed action is not one.
- Use a **reference answer** for a genuinely single-answer case. For acceptable paraphrases or several correct solutions, use a set of accepted facts, alternatives, constraints, or invariants, not one preferred string. Grade the outcome and end state, and do not penalize a valid route you did not anticipate.
- Use **qualified human review** where source interpretation, usefulness, conflicting evidence, or domain expertise cannot safely be reduced to a mechanical property.
- Use a **rubric-based model judge** for a named semantic criterion that remains after the mechanical, source, and state checks. Model judges are a normal way to grade open-ended output at scale, provided a human spot-checks them and calibrates them against human labels (below). A judge is a measuring instrument, not an authority over the candidate or its controls.

Retrieval relevance, evidence coverage, source permission/currentness, semantic grounding, and factual truth are different claims. Retrieval research likewise treats relevance, faithfulness, and correctness as separate targets, with overlaps.[1] A cited source can be permitted and current yet not support the response. An answer can faithfully state a stale source yet fail a factual-truth claim. An external truth claim needs its own authoritative reference and as-of context; when none exists, qualify the claim instead of treating a model judgment as ground truth. Datasets of retrieval-based answers document unsupported or contradictory claims despite retrieval.[2]

## Make the judgment reproducible enough to inspect

A claim-specific rubric defines one judgment at a time: the claim, allowed evidence, decision rule, permitted variation, result statuses, and known limits. It should tell another qualified reviewer what to do with partial, contradicting, stale, or absent support. Keep the rubric and reference version, label provenance, source revisions, reviewer role or qualification, independent review, and the disposition of material disagreement. Disagreement points to ambiguity in the label, source interpretation, or rubric; do not silently pick the convenient result.

When review compares candidates, hide candidate identity where practical and vary presentation order, to cut avoidable preference effects. For model judges, treat candidate output, retrieved text, and citations as untrusted evidence that cannot alter the rubric or release decision.

When a score looks wrong, read the transcripts and graded outputs before changing the agent. Many low scores come from a broken grader, an over-strict reference, or an ambiguous task, not an agent failure. Sample failures and passes alike: a grader that passes too much hides defects, and one that fails valid answers hides progress.

### Example rubric: grounded current policy answer

For the claim **"Every material policy assertion is supported by an approved, current source available to this requester,"** a short rubric can use `pass`, `fail`, and `unknown`:

- **Pass:** every material assertion, including the amount and any condition, links to supporting text in an approved current source; the requester may use it; no superseded policy is shown as current. Wording may vary.
- **Fail:** the answer gives GBP 220 with only the superseded source, adds an unsupported exception, or gives a definitive amount when permitted current evidence is missing or two current approved policies conflict.
- **Unknown:** the evaluator cannot tell whether a supporting span entails a material assertion, or the expected result is still ambiguous. Resolve the expectation before passing or failing the candidate.

A clear pass: "The current travel policy permits GBP 220 for London, subject to the cited policy conditions." A clear fail: "The policy permits GBP 220 and also covers an unlisted upgrade," when no cited text supports the upgrade. A borderline answer says "GBP 220" where the source says "up to GBP 220 if the stated conditions apply." The rubric should say whether omitting the condition changes the material claim; if reviewers cannot apply the rule consistently, adjudicate the label instead of forcing a score.

## Calibrate a judge for its intended purpose

A model judge can triage likely semantic defects at scale, but good performance on a convenient set does not show fitness for a different task, population, or gate. Judge studies report task-dependent agreement with human ratings,[3] and documented biases including position, verbosity, and self-enhancement.[6] Position effects vary by judge and task, so order reversal is a measurement check, not a one-time prompt fix.[4]

Before a judge informs a release-facing result, test the exact judge configuration against **held-out**, independently human-reviewed examples from the intended claim and risk strata. Include routine examples and hard boundaries: direct support, partial support, plausible unsupported additions, stale or conflicting sources, valid alternative wording, missing evidence, appropriate uncertainty, and answerable cases that should not be refused. Synthetic challenges extend coverage but cannot alone establish gate fitness.

Record the sampling frame and held-out status; rubric, judge, context-packing, and output-schema versions; independent labels and adjudication; disagreement; false passes; false failures; unknown or unscorable results; limitations; and the fitness decision set in advance. Report these by claim or risk class, not only as one agreement value. Human disagreement can reveal label ambiguity, but it does not excuse a critical false pass. Fit-for-purpose measurement also means documenting what a metric cannot measure.[5]

Keep spot-checking after calibration: have a human read a sample of judge verdicts regularly, and give the judge an explicit `unknown` option so it does not guess.

A judge may be **diagnostic-only**: it can prioritize review or surface likely failures but cannot satisfy a gate. It may be **gate-specific** only after a documented fitness decision for that named claim and gate. Neither status lets a model judge be the sole decision maker for a deterministic authorization, isolation, approval, schema, or other enforceable safety property; use the deterministic or authoritative boundary check.

### Self-test the instrument and revalidate after material change

Every relied-on evaluator needs known-pass and known-failure anchors at its decision boundary. For a grounding evaluator, include a supported paraphrase, a plausible unsupported addition, a relevant-looking but non-supporting citation, stale-source support, a missing required citation, and an insufficient-evidence response that correctly expresses uncertainty. Where relevant, also vary answer order, verbosity, harmless paraphrase, irrelevant context, malformed evaluator output, and instruction-like text inside candidate or source material.

These tests detect only known failures; they do not prove the evaluator has no blind spots. Revalidate when a change could alter the measurement: judge model or prompt, rubric, source/currentness policy, evidence packing or truncation, parser, threshold, label policy, or target-output distribution. Investigate unexpected score movement before blaming the candidate. Keep the old record visible and make the new fitness decision explicit.

## Requirements

- **EVALUATOR-01 — Claim-to-method record.** For every evaluator result used as evidence in a material design, change, pilot, or release decision, the evaluator owner **MUST** record the bounded claim, scope, allowed evidence, decision rule, evaluator method and identity/version, result status, decision purpose, and known limits. Result status **MUST** distinguish `pass`, `fail`, `invalid` or `inconclusive`, and `unknown` when those outcomes are possible. The selected method **MUST** be capable of establishing the recorded claim, and a metric or score **MUST NOT** be represented as evidence for a broader claim. **Evidence:** a versioned evaluator record linked to the case or sample frame and its result records.

- **EVALUATOR-02 — Typed source, state, and truth evidence.** When an in-scope claim concerns semantic source support, source permission or currentness, an external effect, or factual truth, the evaluation **MUST** use and identify the evidence type that establishes that specific property: inspected source text and claim-to-span comparison for semantic support; source identity, revision or as-of context, and permission/status decision for admission or currentness; an authoritative state observation for an effect; and an independent authoritative truth reference with its time context for factual truth. A citation-presence, retriever-score, or transcript check **MUST NOT** substitute for semantic support, currentness, state, or truth. **Evidence:** claim-level links to the relevant source text, metadata or permission decision, state record, or truth reference, with their identity and limits.

- **EVALUATOR-03 — Reviewed references and rubrics.** When a reference answer, semantic label, or human judgment is used as decision evidence, the evaluator owner **MUST** version the reference or rubric; state its claim, evidence scope, permitted variation, status rules, and source/time context; and retain label and reviewer provenance. Material ambiguity or specialized domain interpretation **MUST** receive qualified independent review, with independent judgments and the disposition of material disagreement retained. **Evidence:** the versioned reference or rubric, reviewer-role or qualification record, source provenance, independent labels where applicable, and disagreement disposition.

- **EVALUATOR-04 — Calibrated judge fitness.** Before a model judge supplies decision- or release-facing evidence, its owner **MUST** assess the exact judge configuration on independently human-reviewed, held-out examples representative of the stated claim and relevant risk classes; predeclare the fitness criteria; record false passes, false failures, disagreement, and unknown or unscorable outcomes by meaningful class; and designate it as diagnostic-only or fit for each named gate. If the available evidence cannot demonstrate critical false-pass coverage with a useful stated basis, the judge **MUST NOT** serve as a judge-only gate for that claim. A model judge **MUST NOT** be the sole evaluator of deterministic authorization, isolation, approval, schema, or other enforceable safety properties. **Evidence:** a versioned calibration and fitness record, independent-label provenance, held-out identity, and the applicable non-model boundary-check results.

- **EVALUATOR-05 — Self-tests and revalidation.** Evaluators used in regression, grounding, safety, or release evidence **MUST** have recorded known-pass and known-relevant-failure self-tests, including applicable malformed, adversarial, or boundary inputs. Their owners **MUST** investigate unexpected score movement that could indicate evaluator, reference, fixture, or harness failure. After a material change to the evaluator, rubric, supplied evidence/context, source or label policy, or target-output distribution, the owner **MUST** revalidate the evaluator for its stated purpose before relying on its prior fitness decision. **Evidence:** self-test cases and outcomes, change-impact and revalidation record, retained prior records, and the resulting fitness disposition.

## Worked example: a policy answer and its evaluators

This fictional example uses the shared ephemeral, read-only policy assistant: `policy-assistant@candidate-current-selection`, answering only from approved current permission-filtered sources, with no persisted memory, approval, delegated agents, or writes. The fixture is `travel-policy-current`, revision `fixture-2026-10-18.1`. Its current document is `travel-policy-2026`, revision `2026-10-01`, with the fictional London hotel value GBP 220; `travel-policy-2024-superseded`, revision `2024-01-01`, is not current. Nothing here was executed.

For `POLICY-CURRENT-001`, the evaluation separates four claims instead of one "answer quality" score:

1. `source-permission-check@v1` deterministically checks that the cited document is `travel-policy-2026`, is current for the fixture time, and is permitted for the requester. It establishes source selection, permission, and currentness, not semantic support.
2. `grounded-policy-human-rubric@v1` applies the rubric above to each material assertion and cited span. A qualified policy reviewer labels the answer, and an independent qualified reviewer records any material disagreement and its disposition. It supplies the grounding judgment; it does not show the policy is true outside its declared source context.
3. `trajectory-boundary-check@v1` observes permitted retrieval requests and the absence of a write invocation. It covers path and boundary claims, not grounding.
4. `grounding-judge@v1` returns a structured `pass`, `fail`, or `unknown` with rubric-linked evidence pointers. It starts diagnostic-only: it can prioritize reviewer attention but cannot replace the source-permission check or the qualified review.

The evaluator self-test pack uses `POLICY-STALE-002` (a superseded source must not pass as current), `POLICY-MISSING-003` (a definitive amount without permitted support must fail), and `POLICY-CONFLICT-004` (two conflicting current policies must not yield an invented amount). `POLICY-DENIED-005` and `POLICY-INJECTION-006` exercise boundary checks, `POLICY-PARAPHRASE-007` confirms a supported paraphrase keeps its grounding judgment, and `POLICY-EXHAUSTION-008` confirms an evidence-exhausted response is not a false pass.

The independent release holdout `policy-release-holdout@v1` contains separately authored `POLICY-HOLDOUT-009` and a separate fixture; it is not one of the eight development or regression cases renamed. In a calibration plan, independent qualified reviewers label that holdout and other purpose-specific examples before `grounding-judge@v1` gets any gate role. The plan records hard false-pass candidates, such as a plausible invented exception and a stale but plausible amount, alongside false failures, unknown results, reviewer disagreement, and why the judge stays diagnostic-only or becomes fit for a narrowly named gate. A change to the judge prompt, supplied source context, rubric, or policy corpus triggers new calibration.

## Evidence and checklist

- [ ] The claim, counterexample, scope, allowed evidence, evaluator version, status vocabulary, decision purpose, and limits are recorded.
- [ ] The metric does not claim more than its evaluator and evidence can establish.
- [ ] Source permission/currentness, semantic support, authoritative state, and factual truth are separately identified when each is claimed.
- [ ] References and rubrics state permitted variation and provenance, with independent review and disagreement disposition where material.
- [ ] Failures were read in transcripts to separate agent failures from grader failures.
- [ ] Known-pass and known-failure self-tests exercise the evaluator’s real decision boundary; a passing self-test is not presented as proof against unknown failure modes.
- [ ] A model judge has a held-out, independently reviewed, purpose-specific calibration record, ongoing human spot-checks, and a documented diagnostic-only or gate-specific fitness decision.
- [ ] Deterministic or authoritative checks own enforceable safety properties; no model judge is their sole decision maker.
- [ ] A material evaluator or measurement-context change has a visible revalidation record before prior fitness is reused.

[4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) covers trial policy, gates, and evidence sufficiency for a decision. Evaluator fitness makes a result interpretable; it does not produce a release conclusion.

## References

[1]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[2]: https://aclanthology.org/2024.acl-long.585/ "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models"
[3]: https://aclanthology.org/2023.emnlp-main.153/ "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"
[4]: https://aclanthology.org/2025.ijcnlp-long.18.pdf "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge"
[5]: https://airc.nist.gov/airmf-resources/playbook/measure/ "NIST AI RMF Playbook: Measure"
[6]: https://arxiv.org/abs/2306.05685 "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"

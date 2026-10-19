# 4.4 Evaluators, Metrics, Rubrics, and Calibration

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, qualified domain reviewers, and accountable owners  
**Applicability:** Whenever evaluation evidence supports a design, change, pilot, or release decision. Model-judge guidance applies only when a model judges. Coverage, cases, and fixtures are in [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.6](06-standards-required-coverage-and-execution-cadence.md).  
**Reader question:** How do I turn observations into a trustworthy judgment?

[Part 4](README.md) · [Applicability and conformance](../../applicability.md) · [Evaluation dimensions](03-evaluation-types-and-dimensions.md) · [Planning and running](05-planning-designing-and-running-tests-and-evaluations.md) · [Practical reference](reference/README.md)

An evaluation is only as useful as the link between claim, evidence, and evaluator. Start with a narrow statement that could be wrong, then pick the least burdensome method that can establish it.

## Start with a claim, not a score

A **metric** says what is measured and how results are summarized, such as the share of cases reaching a required outcome. An **evaluator** is the versioned rule, procedure, instrument, or qualified role that turns evidence into the judgment the metric uses; its output never widens the claim it can establish.

An **evidence source** supplies what is inspected (policy text, a permission decision, a state read, a reference label, a response); the evaluator supplies the judgment. Reserve *oracle* for a named, claim-specific provider with stated authority, scope, time, and limits.

Write each material claim's counterexample before choosing a method; "a citation is present" fails against a relevant-looking passage that does not support an invented exception. Counterexamples expose proxy scores.

### Select the simplest capable method

Combine methods for multi-part claims; a later method never makes earlier evidence unnecessary.

- **Deterministic assertion** for a decidable property (output field, permitted source and revision, absent forbidden invocation, exact fixture value); it establishes only that property.
- **Approved-source comparison** for a source's content, status, permission, or currency, recording identity, revision or as-of time, and the permission decision.
- **Authoritative state observation** for an actual effect or its absence; a transcript is not one.
- **Reference answer** for a genuinely single-answer case; otherwise accepted facts, alternatives, constraints, or invariants, not one preferred string. Grade outcome and end state, not an anticipated route.
- **Qualified human review** where interpretation, usefulness, conflicting evidence, or domain expertise cannot safely become a mechanical check.
- **Rubric-based model judge** for a named semantic criterion left after mechanical, source, and state checks. They are a normal way to grade open-ended output at scale if humans spot-check and calibrate them (below); a judge is an instrument, not an authority over the candidate or its controls.

Relevance, coverage, permission/currentness, grounding, and factual truth are different claims ([4.3](03-evaluation-types-and-dimensions.md)), as retrieval research also treats them.[1] An external truth claim needs its own authoritative reference and as-of context; without one, qualify the claim instead of treating a model judgment as ground truth. Datasets of retrieval-based answers document unsupported or contradictory claims despite retrieval.[2]

## Make the judgment reproducible enough to inspect

A rubric defines one judgment: claim, allowed evidence, decision rule, permitted variation, statuses, and limits, including how to treat partial, contradicting, stale, or absent support. EVALUATOR-03 lists what to retain. Disagreement signals ambiguity in label, source interpretation, or rubric; never silently pick the convenient result.

When comparing candidates, hide identity where practical and vary order. Model judges treat candidate output, retrieved text, and citations as untrusted evidence that cannot alter the rubric.

When a score looks wrong, read transcripts and graded outputs before changing the agent; many low scores come from a broken grader, over-strict reference, or ambiguous task. Sample passes as well as failures: a lenient grader hides defects, and a strict one hides progress.

### Example rubric: grounded current policy answer

Claim: **"Every material policy assertion is supported by an approved, current source available to this requester."**

- **Pass:** every material assertion, including amount and conditions, links to supporting text in an approved current source the requester may use; nothing superseded is shown as current. Wording may vary.
- **Fail:** GBP 220 backed only by the superseded source, an unsupported exception, or a definitive amount when permitted current evidence is missing or two current approved policies conflict.
- **Unknown:** the evaluator cannot tell whether a span entails a material assertion, or the expected result is ambiguous; resolve it before passing or failing the candidate.

Pass: "The current travel policy permits GBP 220 for London, subject to the cited policy conditions." Fail: "The policy permits GBP 220 and also covers an unlisted upgrade," with no support for the upgrade. Borderline: "GBP 220" where the source says "up to GBP 220 if the stated conditions apply." The rubric should say whether dropping the condition changes the claim; if reviewers disagree, adjudicate the label rather than force a score.

## Calibrate a judge for its intended purpose

A judge that triages semantic defects well on a convenient set is not thereby fit for another task, population, or gate. Studies report task-dependent agreement with humans[3] and position, verbosity, and self-enhancement biases.[6] Position effects vary by judge and task, so order reversal is a standing check, not a one-time prompt fix.[4]

Before release-facing use, test the exact configuration on **held-out**, independently human-reviewed examples from the intended claim and risk strata, routine and hard: direct and partial support, plausible unsupported additions, stale or conflicting sources, valid alternative wording, missing evidence, appropriate uncertainty, and answerable cases that should not be refused. Synthetic challenges extend coverage but cannot alone show gate fitness.

Record, by claim or risk class rather than one agreement value, the sampling frame and held-out status, rubric, judge, context-packing, and output-schema versions, labels and adjudication, false passes and failures, unknowns, limitations, and the predeclared fitness decision. Human disagreement can reveal label ambiguity but never excuses a critical false pass. Document what a metric cannot measure.[5] After calibration, a human keeps reading sampled verdicts, and the judge gets an explicit `unknown` option so it does not guess.

A **diagnostic-only** judge prioritizes review but cannot satisfy a gate; a **gate-specific** one needs a documented fitness decision for that named claim and gate. Neither is the sole decision maker for enforceable safety properties such as authorization, isolation, approval, or schema; use the deterministic or authoritative boundary check.

### Self-test the instrument and revalidate after material change

Every relied-on evaluator needs known-pass and known-failure anchors at its decision boundary; for grounding, a supported paraphrase, a plausible unsupported addition, a relevant-looking non-supporting citation, stale-source support, a missing required citation, and an insufficient-evidence response that correctly expresses uncertainty. Where relevant, vary order, verbosity, harmless paraphrase, irrelevant context, malformed evaluator output, and instruction-like text in candidate or source material.

Self-tests catch only known failures. Revalidate when a change could alter measurement: judge model or prompt, rubric, source/currentness policy, evidence packing or truncation, parser, threshold, label policy, or target-output distribution. Investigate unexpected score movement before blaming the candidate; keep the old record visible and the new fitness decision explicit.

## Requirements

- **EVALUATOR-01 — Claim-to-method record.** For every evaluator result used as evidence in a material design, change, pilot, or release decision, the evaluator owner **MUST** record the bounded claim, scope, allowed evidence, decision rule, evaluator method and identity/version, result status, decision purpose, and known limits. Result status **MUST** distinguish `pass`, `fail`, `invalid` or `inconclusive`, and `unknown` when those outcomes are possible. The selected method **MUST** be capable of establishing the recorded claim, and a metric or score **MUST NOT** be represented as evidence for a broader claim. **Evidence:** a versioned evaluator record linked to the case or sample frame and its result records.

- **EVALUATOR-02 — Typed source, state, and truth evidence.** When an in-scope claim concerns semantic source support, source permission or currentness, an external effect, or factual truth, the evaluation **MUST** use and identify the evidence type that establishes that specific property: inspected source text and claim-to-span comparison for semantic support; source identity, revision or as-of context, and permission/status decision for admission or currentness; an authoritative state observation for an effect; and an independent authoritative truth reference with its time context for factual truth. A citation-presence, retriever-score, or transcript check **MUST NOT** substitute for semantic support, currentness, state, or truth. **Evidence:** claim-level links to the relevant source text, metadata or permission decision, state record, or truth reference, with their identity and limits.

- **EVALUATOR-03 — Reviewed references and rubrics.** When a reference answer, semantic label, or human judgment is used as decision evidence, the evaluator owner **MUST** version the reference or rubric; state its claim, evidence scope, permitted variation, status rules, and source/time context; and retain label and reviewer provenance. Material ambiguity or specialized domain interpretation **MUST** receive qualified independent review, with independent judgments and the disposition of material disagreement retained. **Evidence:** the versioned reference or rubric, reviewer-role or qualification record, source provenance, independent labels where applicable, and disagreement disposition.

- **EVALUATOR-04 — Calibrated judge fitness.** Before a model judge supplies decision- or release-facing evidence, its owner **MUST** assess the exact judge configuration on independently human-reviewed, held-out examples representative of the stated claim and relevant risk classes; predeclare the fitness criteria; record false passes, false failures, disagreement, and unknown or unscorable outcomes by meaningful class; and designate it as diagnostic-only or fit for each named gate. If the available evidence cannot demonstrate critical false-pass coverage with a useful stated basis, the judge **MUST NOT** serve as a judge-only gate for that claim. A model judge **MUST NOT** be the sole evaluator of deterministic authorization, isolation, approval, schema, or other enforceable safety properties. **Evidence:** a versioned calibration and fitness record, independent-label provenance, held-out identity, and the applicable non-model boundary-check results.

- **EVALUATOR-05 — Self-tests and revalidation.** Evaluators used in regression, grounding, safety, or release evidence **MUST** have recorded known-pass and known-relevant-failure self-tests, including applicable malformed, adversarial, or boundary inputs. Their owners **MUST** investigate unexpected score movement that could indicate evaluator, reference, fixture, or harness failure. After a material change to the evaluator, rubric, supplied evidence/context, source or label policy, or target-output distribution, the owner **MUST** revalidate the evaluator for its stated purpose before relying on its prior fitness decision. **Evidence:** self-test cases and outcomes, change-impact and revalidation record, retained prior records, and the resulting fitness disposition.

## Worked example: a policy answer and its evaluators

The fictional, unexecuted `policy-assistant@candidate-current-selection` is ephemeral and read-only. Fixture `travel-policy-current`, revision `fixture-2026-10-18.1`, holds current `travel-policy-2026`, revision `2026-10-01`, with the London hotel value GBP 220; `travel-policy-2024-superseded`, revision `2024-01-01`, is not current.

For `POLICY-CURRENT-001`, four evaluators replace one "answer quality" score:

1. `source-permission-check@v1` deterministically checks that the cited document is `travel-policy-2026`, current at fixture time, and permitted for the requester: source selection, permission, and currentness, not semantic support.
2. `grounded-policy-human-rubric@v1` applies the rubric above to each material assertion and cited span. A qualified policy reviewer labels; an independent qualified reviewer records material disagreement and its disposition. It judges grounding, not truth beyond the source context.
3. `trajectory-boundary-check@v1` observes permitted retrieval requests and the absence of writes: path and boundary claims, not grounding.
4. `grounding-judge@v1` returns structured `pass`, `fail`, or `unknown` with rubric-linked evidence pointers. It starts diagnostic-only, replacing neither the permission check nor qualified review.

Self-tests: `POLICY-STALE-002` (a superseded source must not pass as current), `POLICY-MISSING-003` (an unsupported definitive amount must fail), `POLICY-CONFLICT-004` (conflicting current policies must not yield an invented amount), `POLICY-DENIED-005` and `POLICY-INJECTION-006` (boundary checks), `POLICY-PARAPHRASE-007` (a supported paraphrase keeps its grounding judgment), and `POLICY-EXHAUSTION-008` (an evidence-exhausted response is not a false pass).

Before `grounding-judge@v1` gets any gate role, independent qualified reviewers label `POLICY-HOLDOUT-009` (separately authored, in `policy-release-holdout@v1` with its own fixture) and other purpose-specific examples. Calibration targets hard false passes such as a plausible invented exception or a stale but plausible amount. A change to judge prompt, source context, rubric, or policy corpus triggers recalibration.

## Evidence and checklist

- [ ] Each claim has a written counterexample.
- [ ] Failures were read in transcripts to separate agent from grader failures.
- [ ] A model judge has ongoing human spot-checks.

Evaluator fitness makes a result interpretable, not a release conclusion; see [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

## References

[1]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[2]: https://aclanthology.org/2024.acl-long.585/ "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models"
[3]: https://aclanthology.org/2023.emnlp-main.153/ "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"
[4]: https://aclanthology.org/2025.ijcnlp-long.18.pdf "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge"
[5]: https://airc.nist.gov/airmf-resources/playbook/measure/ "NIST AI RMF Playbook: Measure"
[6]: https://arxiv.org/abs/2306.05685 "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"

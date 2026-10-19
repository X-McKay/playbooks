# 4.4 Evaluators, Metrics, Rubrics, and Calibration

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, qualified domain reviewers, and accountable owners  
**Applicability:** Use this chapter whenever evaluation evidence supports a material design, change, pilot, or release decision. A model judge is conditional: it is relevant only when a model-based semantic judgment is proposed. This chapter does not select coverage, cases, or fixtures; those are addressed in [4.5](05-planning-designing-and-running-tests-and-evaluations.md) and [4.6](06-standards-required-coverage-and-execution-cadence.md).

**Reader question:** How do I turn observations into a trustworthy judgment?

[Part 4](README.md) · [Applicability and conformance](../../applicability.md) · [Evaluation dimensions](03-evaluation-types-and-dimensions.md) · [Planning and running](05-planning-designing-and-running-tests-and-evaluations.md) · [Practical reference](reference/README.md)

An evaluation is only as useful as the connection between its claim, its evidence, and its evaluator. Start with a narrow statement that could be wrong, then choose the least burdensome method that can establish that statement. A fluent answer, a resolved citation, or a favorable aggregate score is not evidence for every nearby claim.

## Start with a claim, not a score

A **metric** says what is measured and how results are summarized: for example, the proportion of cases in which a required terminal outcome was reached, or the count of unsupported material assertions. An **evaluator** is the versioned rule, procedure, instrument, or qualified role that turns stated evidence into an observation or judgment used by that metric. The metric is not the instrument, and an instrument's output does not enlarge the claim it can establish.

An **evidence source** supplies the thing inspected. It may be approved policy text, a permission decision, a controlled fixture, an authoritative state read, a reference label, or a response. The evaluator supplies the comparison or judgment procedure. Keeping these separate prevents a source document, a transcript, and a rubric from all being called an “oracle.” Reserve *oracle* for a named, claim-specific answer or state provider whose authority, scope, time, and limits are stated.

For every material claim, write its counterexample before choosing a method. “A citation is present” has an easy counterexample: a response cites a relevant-looking passage that does not support its invented exception. This discipline exposes a score that is measuring a proxy rather than the claim.

### Select the simplest capable method

Use methods in combination when the claim has several parts; this is not a hierarchy in which a later method makes earlier evidence unnecessary.

- Use a **deterministic assertion** for a decidable property, such as an output field, a permitted source identifier and revision, an absent forbidden invocation, or an exact value in a controlled fixture. It establishes only the encoded property.
- Use an **approved-source comparison** when the claim concerns the content, status, permission, or currency of a source. Record the source identity, revision or as-of time, and the applicable permission decision.
- Use an **authoritative state observation** to establish an actual effect or lack of effect. An agent transcript that reports a completed action is not a state observation.
- Use a **reference answer** for a genuinely single-answer case. For acceptable paraphrases or several correct solutions, make the reference a set of accepted facts, alternatives, constraints, or invariants rather than one preferred string.
- Use **qualified human review** where source interpretation, usefulness, conflicting evidence, or domain expertise cannot safely be reduced to a mechanical property.
- Use a **calibrated model judge** only for a named semantic criterion that remains after the applicable mechanical, source, and state checks. It is a measuring instrument, not an authority over the candidate or its controls.

Retrieval relevance, evidence coverage, source permission/currentness, semantic grounding, and factual truth are different claims. Retrieval research likewise treats relevance, faithfulness, correctness, and answer relevance as distinct targets.[1] A cited source can be permitted and current but fail to support the response. An answer can faithfully state a stale source but fail a separate factual-truth claim. An external truth claim needs its own authoritative reference and as-of context; when such a reference is unavailable, qualify the claim rather than treating a model judgment as ground truth. Retrieved-answer datasets also document unsupported or contradictory generated claims despite retrieval.[2]

## Make the judgment reproducible enough to inspect

A claim-specific rubric defines one judgment at a time. It identifies the claim, allowed evidence, decision rule, permitted variation, result statuses, and known limits. It should tell another qualified reviewer what to do with support that is partial, contradicting, stale, or absent. Preserve the rubric and reference version, label provenance, source revisions, reviewer qualifications or role, independent review, and the disposition of material disagreement. Disagreement is evidence about ambiguity in the label, source interpretation, or rubric; it is not an invitation to silently select the convenient result.

Where comparison between candidates is part of review, conceal candidate identity when practical and vary presentation order. This reduces avoidable preference effects without pretending that a reviewer is an objective oracle. For model judges, treat candidate output, retrieved text, and citations as untrusted evidence, not instructions capable of altering the rubric or release decision.

### Example rubric: grounded current policy answer

For the claim **“Every material policy assertion is supported by an approved, current source available to this requester,”** a short rubric can use `pass`, `fail`, and `unknown`:

- **Pass:** every material assertion, including the monetary amount and any condition, links to supporting text in an approved current source; the requester is permitted to use it; no superseded policy is represented as current. Wording may vary.
- **Fail:** the answer gives GBP 220 with only the superseded source, adds an unsupported exception, or gives a definitive amount when the permitted current evidence is missing or two current approved policies conflict.
- **Unknown:** the evaluator cannot determine whether a supporting span entails a material assertion, or the reference expectation remains materially ambiguous. Resolve the expectation before treating the candidate as failed or passed.

A straightforward pass is: “The current travel policy permits GBP 220 for London, subject to the cited policy conditions.” A clear fail is: “The policy permits GBP 220 and also covers an unlisted upgrade,” when no cited text supports the upgrade. A borderline answer says simply “GBP 220” where the source says “up to GBP 220 if the stated conditions apply.” The rubric should identify whether omitting that condition changes the material claim; if reviewers cannot apply the rule consistently, the label needs adjudication rather than a forced score.

## Calibrate a judge for its intended purpose

A model judge can help triage likely semantic defects, but good performance on a convenient set does not establish fitness for a different task, population, or gate. Research on model judging reports task-dependent human alignment and potential preference effects; it does not establish transfer to a new domain rubric.[3] Position effects can also vary by judge and task, so order reversal is a measurement check rather than a one-time prompt fix.[4]

Before a judge informs a release-facing result, evaluate the exact judge configuration against **held-out**, independently human-reviewed examples from the intended claim and relevant risk strata. The calibration set should include routine examples and difficult boundaries: direct support, partial support, plausible unsupported additions, stale or conflicting sources, valid alternative wording, missing evidence, appropriate uncertainty, and answerable cases that should not be refused. Synthetic challenges can extend coverage but cannot alone establish gate fitness.

Record the sampling frame and held-out status; rubric, judge, context-packing, and output-schema versions; independent labels and adjudication; disagreement; false passes; false failures; unknown or unscorable results; limitations; and the predeclared fitness decision. Report these by meaningful claim or risk class, not only as an aggregate agreement value. Human disagreement can reveal label ambiguity, but it does not excuse a critical false pass. Fit-for-purpose measurement also requires documenting what a metric cannot measure.[5]

A judge may be **diagnostic-only**, meaning it can prioritize review or surface likely failures but cannot satisfy a gate. It may be **gate-specific** only after a documented fitness decision for that named claim and gate. Neither status allows a model judge to be the sole decision maker for a deterministic authorization, isolation, approval, schema, or other enforceable safety property; use the deterministic or authoritative boundary check for that property.

### Self-test the instrument and revalidate after material change

Every relied-on evaluator needs known-pass and known-failure anchors at its decision boundary. For a grounding evaluator, anchors should include a supported paraphrase, a plausible unsupported addition, a relevant-looking but non-supporting citation, stale-source support, a required-citation omission, and an insufficient-evidence response that correctly expresses uncertainty. Where relevant, also test answer order, verbosity, harmless paraphrase, irrelevant context, malformed evaluator output, and instruction-like text embedded in candidate or source material.

These tests only show detection of known failures; they do not prove that an evaluator has no blind spots. Revalidate the evaluator when a change could alter the measurement: judge model or prompt, rubric, source/currentness policy, evidence packing or truncation, parser, threshold, label policy, or target-output distribution. Investigate an unexpected score movement before attributing it to the candidate. Keep the old record visible and make the new fitness decision explicit.

## Requirements

- **EVALUATOR-01 — Claim-to-method record.** For every evaluator result used as evidence in a material design, change, pilot, or release decision, the evaluator owner **MUST** record the bounded claim, scope, allowed evidence, decision rule, evaluator method and identity/version, result status, decision purpose, and known limits. Result status **MUST** distinguish `pass`, `fail`, `invalid` or `inconclusive`, and `unknown` when those outcomes are possible. The selected method **MUST** be capable of establishing the recorded claim, and a metric or score **MUST NOT** be represented as evidence for a broader claim. **Evidence:** a versioned evaluator record linked to the case or sample frame and its result records.

- **EVALUATOR-02 — Typed source, state, and truth evidence.** When an in-scope claim concerns semantic source support, source permission or currentness, an external effect, or factual truth, the evaluation **MUST** use and identify the evidence type that establishes that specific property: inspected source text and claim-to-span comparison for semantic support; source identity, revision or as-of context, and permission/status decision for admission or currentness; an authoritative state observation for an effect; and an independent authoritative truth reference with its time context for factual truth. A citation-presence, retriever-score, or transcript check **MUST NOT** substitute for semantic support, currentness, state, or truth. **Evidence:** claim-level links to the relevant source text, metadata or permission decision, state record, or truth reference, with their identity and limits.

- **EVALUATOR-03 — Reviewed references and rubrics.** When a reference answer, semantic label, or human judgment is used as decision evidence, the evaluator owner **MUST** version the reference or rubric; state its claim, evidence scope, permitted variation, status rules, and source/time context; and retain label and reviewer provenance. Material ambiguity or specialized domain interpretation **MUST** receive qualified independent review, with independent judgments and the disposition of material disagreement retained. **Evidence:** the versioned reference or rubric, reviewer-role or qualification record, source provenance, independent labels where applicable, and disagreement disposition.

- **EVALUATOR-04 — Calibrated judge fitness.** Before a model judge supplies decision- or release-facing evidence, its owner **MUST** assess the exact judge configuration on independently human-reviewed, held-out examples representative of the stated claim and relevant risk classes; predeclare the fitness criteria; record false passes, false failures, disagreement, and unknown or unscorable outcomes by meaningful class; and designate it as diagnostic-only or fit for each named gate. If the available evidence cannot demonstrate critical false-pass coverage with a useful stated basis, the judge **MUST NOT** serve as a judge-only gate for that claim. A model judge **MUST NOT** be the sole evaluator of deterministic authorization, isolation, approval, schema, or other enforceable safety properties. **Evidence:** a versioned calibration and fitness record, independent-label provenance, held-out identity, and the applicable non-model boundary-check results.

- **EVALUATOR-05 — Self-tests and revalidation.** Evaluators used in regression, grounding, safety, or release evidence **MUST** have recorded known-pass and known-relevant-failure self-tests, including applicable malformed, adversarial, or boundary inputs. Their owners **MUST** investigate unexpected score movement that could indicate evaluator, reference, fixture, or harness failure. After a material change to the evaluator, rubric, supplied evidence/context, source or label policy, or target-output distribution, the owner **MUST** revalidate the evaluator for its stated purpose before relying on its prior fitness decision. **Evidence:** self-test cases and outcomes, change-impact and revalidation record, retained prior records, and the resulting fitness disposition.

## Worked example: a policy answer and its evaluators

This illustrative example uses the shared ephemeral, read-only policy assistant. It answers only from approved current permission-filtered sources, has no persisted memory, approval, delegated agents, or external writes, and uses the candidate `policy-assistant@candidate-current-selection`. The controlled fixture is `travel-policy-current`, revision `fixture-2026-10-18.1`. Its current document is `travel-policy-2026`, revision `2026-10-01`, with the fictional London hotel value GBP 220; `travel-policy-2024-superseded`, revision `2024-01-01`, is not current.

For `POLICY-CURRENT-001`, the evaluation separates four claims instead of reporting one “answer quality” score:

1. `source-permission-check@v1` deterministically checks that the cited document is `travel-policy-2026`, is current for the fixture time, and is permitted for the requester. This establishes source selection, permission, and currentness—not semantic support.
2. `grounded-policy-human-rubric@v1` applies the preceding grounded-current-policy rubric to each material assertion and cited span. A qualified policy reviewer labels the answer, and an independent qualified reviewer records any material disagreement and its disposition. This supplies the semantic grounding judgment; it does not establish that the policy is universally true outside its declared source context.
3. `trajectory-boundary-check@v1` observes permitted retrieval requests and the absence of a write invocation. It is evidence for its observable path and boundary claims, not a substitute for the grounding rubric.
4. `grounding-judge@v1` returns a structured `pass`, `fail`, or `unknown` with concise rubric-linked evidence pointers. It is initially diagnostic-only: its output can prioritize the reviewer’s attention but cannot replace the source-permission check or the qualified semantic review.

The evaluator self-test pack uses `POLICY-STALE-002` to ensure a superseded source does not pass as current, `POLICY-MISSING-003` to ensure a definitive amount without permitted support fails, and `POLICY-CONFLICT-004` to ensure two current approved conflicting policies do not produce an invented definitive amount. It uses `POLICY-DENIED-005` and `POLICY-INJECTION-006` to exercise boundary-related checks, `POLICY-PARAPHRASE-007` to confirm a supported paraphrase retains its grounding judgment, and `POLICY-EXHAUSTION-008` to confirm that an evidence-exhausted response does not become a false pass. These are expected self-test outcomes in an illustrative plan, not measurements of a live agent.

The independent release holdout `policy-release-holdout@v1` contains separately authored `POLICY-HOLDOUT-009` and a separate fixture; it is not one of the eight development or regression cases renamed as untouched. An illustrative calibration plan has independent qualified reviewers label that holdout and other purpose-specific examples before any proposed gate role for `grounding-judge@v1`. It records difficult false-pass candidates—such as a plausible invented exception and a stale but plausible amount—alongside false failures, unknown results, reviewer disagreement, and the reason the judge remains diagnostic-only or becomes fit for a narrowly named gate. A change to the judge prompt, supplied source context, rubric, or policy corpus triggers renewed calibration before that role is reused.

## Evidence and checklist

Before relying on an evaluator result, confirm:

- [ ] The claim, counterexample, scope, allowed evidence, evaluator version, status vocabulary, decision purpose, and limits are recorded.
- [ ] The metric is not being used to claim more than its evaluator and evidence can establish.
- [ ] Source permission/currentness, semantic support, authoritative state, and factual truth are separately identified when each is claimed.
- [ ] References and rubrics state permitted variation and provenance, with independent review and disagreement disposition where material.
- [ ] Known-pass and known-failure self-tests exercise the evaluator’s actual decision boundary; a passing self-test is not presented as proof against unknown failure modes.
- [ ] A model judge has a held-out, independently reviewed, purpose-specific calibration record and a documented diagnostic-only or gate-specific fitness decision.
- [ ] Deterministic or authoritative checks remain responsible for enforceable safety properties; no model judge is their sole decision maker.
- [ ] A material evaluator or measurement-context change has a visible revalidation record before prior fitness is reused.

[4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) interprets identified results, trial policy, gates, and evidence sufficiency for a decision. Evaluator fitness helps make a result interpretable; it does not itself produce a release conclusion.

## References

[1]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[2]: https://aclanthology.org/2024.acl-long.585/ "RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models"
[3]: https://aclanthology.org/2023.emnlp-main.153/ "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"
[4]: https://aclanthology.org/2025.ijcnlp-long.18.pdf "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge"
[5]: https://airc.nist.gov/airmf-resources/playbook/measure/ "NIST AI RMF Playbook: Measure"

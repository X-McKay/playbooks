# 4.1 Foundations, Terms, and Definitions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** Whenever you plan or read evidence for a material claim. The vocabulary implies no particular architecture or tool.  
**Reader question:** What are we talking about, and how do the pieces fit together?

[Part 4 — Testing and Evaluation](README.md) · [Playbook home](../../README.md) · [Glossary](../../glossary.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md)

This chapter sets the vocabulary for Part 4; the [glossary](../../glossary.md) indexes it.

## Tests and evaluations overlap

Here a **test** is a designed execution or probe under stated conditions that records observations about one or more properties. It may be automated or manual, deterministic or variable, isolated or end-to-end. This is a local working definition; ISTQB, for example, defines a test as a set of one or more test cases.[1]

An **evaluation** is the planned assessment of a bounded claim or decision. It selects cases and evidence, applies evaluators, and states what the results establish and what they do not. Tests are common inputs, but expert review, samples, and operational observation also count. NIST treats testing, evaluation, verification, and validation (TEVV) as lifecycle-wide activities tied to context and intended use;[2] the test/evaluation split is this playbook's own. Agent-evaluation practice likewise uses structured tasks and graders for variable systems.[3]

The split is about **scope**, not system type: a stochastic agent can be tested, and a deterministic permission assertion can feed an evaluation. Keep it where it makes records and decisions clearer.

## The working vocabulary

- **Evaluator:** The rule, procedure, instrument, or qualified human role that turns stated evidence into a judgment. Keep the method distinct from whoever operates it when that matters. A permission predicate and a semantic review are different evaluators, even on one case.
- **Case:** A versioned, bounded task or probe with conditions, inputs, expected observable outcomes or invariants, permitted variation, and an origin or rationale (compare ISTQB's preconditions, inputs, and expected results).[4]
- **Trial:** One recorded execution of a case under an identified candidate configuration and starting conditions. Trials that share a case, fixture, time window, or dependency are not automatically independent.
- **Suite:** A versioned set of cases chosen for a coverage goal. "Regression" says why a suite runs, not which boundary it exercises.
- **Fixture:** The revisioned starting data, state, and dependency behavior needed to interpret a case. It may define isolation and reset checks. It sets up a controlled world; it does not judge the result.
- **Reference and oracle:** A **reference** is an expected value, accepted set, label, or invariant. An **authoritative state observation** is a trusted observation of relevant state or effect. "Oracle" is used for either, so name its role, scope, authority, and time or version instead. The evaluator is the comparison or judgment procedure; source document, state observation, and evaluator are different things.
- **Trajectory:** The externally observable, ordered or partly ordered events relevant to a claim, such as request, permission decision, retrieved source identity, response, and state observation. Record only what the claim needs. Private chain-of-thought is not required and does not replace outcome evidence.
- **Verification and validation:** Verification confirms, with objective evidence, that specified requirements have been fulfilled; validation confirms that the requirements for an intended use have been fulfilled.[5] NIST also ties validation to intended use.[2] Neither names a test method or lifecycle stage.

Keep the expected criterion, the observation, and the judgment apart. "Cite the current approved policy" is a criterion; the fixture's document record shows which revision was current; a source-support evaluator judges whether the cited text supports the answer. A citation's presence does not prove support.

## Five independent descriptors

Describe a case or evaluation with five separate descriptors. It can have several assessed properties but one value on each other axis, so a case can inform more than one claim without belonging to a single exclusive "evaluation type."

1. **Test level — where the property is exercised.** The observed boundary, such as unit, component, integration, or system. Teams draw these lines differently, so state what is included.
2. **Assessed property — what is claimed.** Task outcome, current-source selection, answer grounding, trajectory control, reliability, and so on.
3. **Evaluator method — how evidence is judged.** A deterministic assertion, comparison with a reference or authoritative observation, a rubric, qualified human judgment, or another method that fits the claim ([4.4](04-evaluators-metrics-rubrics-and-calibration.md)).
4. **Suite purpose — why the set runs.** Development feedback, regression, release holdout, acceptance, or operational learning. Acceptance is a decision context here, not a technical boundary.
5. **Lifecycle/environment — when and under what exposure.** Controlled offline, staging, guarded live use, or production monitoring. Production observation is not automatically side-effect-free, and monitoring alone does not establish a pre-release claim.

"Unit-level" says where a check runs, not whether it is deterministic. "Grounding" says what is assessed, not who judges it. A release holdout can hold system-level cases and run offline.

## Worked example: current policy answer

The fictional policy assistant used throughout Part 4, `policy-assistant@candidate-current-selection`, answers from approved, current, permission-filtered documents and has no external write capability. A user asks for a London hotel limit. Fixture `travel-policy-current` at revision `fixture-2026-10-18.1` holds the current document `travel-policy-2026`, revision `2026-10-01`, stating GBP 220. Nothing here was executed.

```yaml
illustrative_only: true
candidate: policy-assistant@candidate-current-selection
case: POLICY-CURRENT-001
fixture:
  id: travel-policy-current
  revision: "fixture-2026-10-18.1"
level: integration
assessed_properties: [current_source_selection, semantic_support]
evaluator_methods:
  - source-permission-check@v1
  - grounded-policy-human-rubric@v1
suite_purpose: development
lifecycle_environment: controlled_offline
expected:
  current_document: travel-policy-2026@2026-10-01
  supported_amount: "GBP 220"
```

Integration is the right level because the claim depends on the assistant and the source/permission interface. The permission check shows whether the source was permitted, not whether the answer's meaning is supported. The human rubric judges whether "GBP 220" follows from the cited passage, not whether retrieval enforced the user's permission. Keep the conclusions apart: a passed permission check with an invented exception fails the support claim; a grounded answer from an unpermitted source fails the access claim.

A later regression run can reuse the case for another purpose without changing its level. A production observation would need its own environment label and exposure context.

## Evidence and checklist

- [ ] Each test/probe is separate from the broader evaluation claim where that matters.
- [ ] Cases, trials, suites, fixtures, references, observations, evaluators, and trajectories have separate fields.
- [ ] The five descriptors are stated independently.
- [ ] Expected criteria, source or state observations, and evaluator judgments are distinct.
- [ ] Trajectory evidence covers only relevant observable events.
- [ ] Illustrative material is not presented as an executed result.

Next: [4.2](02-test-levels-techniques-and-suite-purposes.md) covers levels and techniques.

## References

[1]: https://glossary.istqb.org/en_US/term/test "ISTQB Glossary: Test"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[3]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"
[4]: https://glossary.istqb.org/en_US/term/test-case "ISTQB Glossary: Test Case"
[5]: https://glossary.istqb.org/en_US/term/verification "ISTQB Glossary: Verification"

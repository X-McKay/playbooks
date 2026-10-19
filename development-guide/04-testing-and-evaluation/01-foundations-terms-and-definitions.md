# 4.1 Foundations, Terms, and Definitions

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** Use these distinctions whenever you plan or interpret evidence for a material claim; the vocabulary does not imply a particular architecture or test tool.  
**Reader question:** What are we talking about, and how do the pieces fit together?

[Part 4 — Testing and Evaluation](README.md) · [Playbook home](../../README.md) · [Glossary](../../glossary.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md)

This chapter establishes the vocabulary used across Part 4. The [whole-book glossary](../../glossary.md) is the index of these canonical explanations; it should point back here rather than create competing definitions. Later chapters explain how to exercise a claim, select an evaluator, plan runs, and interpret results. This chapter focuses on how those pieces relate.

## Tests and evaluations overlap

For clarity in this playbook, a **test** is a designed execution or probe under stated conditions that records observations about one or more properties. It may be automated or human-operated, deterministic or variable, isolated or end-to-end. This is a local working definition, not a replacement for industry glossaries: for example, the ISTQB glossary defines a test as a set of one or more test cases.[1]

An **evaluation** is the broader, planned assessment of a bounded claim or decision. It selects relevant cases and evidence, applies one or more evaluators, and interprets what the results establish and what they do not. Tests are common inputs to an evaluation, but evaluation can also draw on expert review, samples, or operational observations. NIST describes testing, evaluation, verification, and validation as context-sensitive activities for measuring and managing AI risk, not as a deterministic-versus-stochastic split.[2] Work on agent evaluations likewise uses structured tasks and checks to assess variable systems.[3]

The useful distinction is about **scope**, not system type: a stochastic agent can be tested, and a deterministic permission assertion can contribute to an evaluation. Ordinary speech may use “test” and “evaluation” more loosely; keep the distinction when it helps make records and decisions clear.

## The working vocabulary

- **Evaluator:** The specified rule, procedure, instrument, or qualified human role that turns stated evidence into a judgment. Keep the method distinct from its operator when that matters. A permission predicate and a semantic review are different evaluators, even when they assess the same case.
- **Case:** A versioned, bounded task or probe with relevant conditions and inputs, expected observable outcomes or invariants, permitted variation, and an origin or rationale. The ISTQB test-case entry also describes cases through elements such as preconditions, inputs, expected results, and postconditions.[4]
- **Trial:** One recorded execution attempt of a case under an identified candidate/configuration and initial conditions. Repeated trials may share a case, fixture, time window, or dependency, so they are not automatically independent observations.
- **Suite:** A versioned set of cases selected for a stated coverage goal or purpose. “Regression” or “development” describes why a suite is run, not which technical boundary it exercises.
- **Fixture:** The revisioned starting data, state, and dependency behavior needed to interpret a case. It may define isolation and reset checks. A fixture establishes a controlled world; it is not automatically the rule that judges the result.
- **Reference and oracle:** A **reference** is an expected value, accepted set, label, or invariant. An **authoritative state observation** is a trusted observation of relevant state or effect. “Oracle” is sometimes used for either a reference or a trusted source/procedure that answers a claim; name its role, scope, authority, and time/version rather than relying on the ambiguous word alone. The evaluator is the comparison or judgment procedure. A source document, state observation, and evaluator are not interchangeable.
- **Trajectory:** The externally observable, ordered or partially ordered events relevant to a claim—for example, a request, permission decision, retrieved source identity, response, and relevant state observation. Describe the observable behavior needed to establish the claim; private chain-of-thought is neither a trajectory requirement nor a substitute for outcome evidence.
- **Verification and validation:** Verification asks whether a work product fulfills its specification; validation asks whether requirements for its intended use are fulfilled.[5] NIST's AI RMF also frames validation around intended use and application.[2] These are related aims, not synonyms for a particular test method or lifecycle stage.

Keep expected criteria separate from what was observed. For instance, “cite the current approved policy” is an expected criterion; the fixture’s document record can establish which revision was current; a source-support evaluator judges whether the cited text actually supports the answer. A citation’s presence or metadata alone does not prove semantic support.

## Five independent descriptors

Describe a case or evaluation with five separate descriptors. One item can have several values on the property axis and one value on each other axis; it does not need to belong to one exclusive “evaluation type.”

1. **Test level — where the property is exercised.** Name the observed boundary, such as unit, component, integration, or system. Teams may draw some boundaries differently, so state what is included rather than assuming labels settle it.
2. **Assessed property — what is being claimed.** Examples include task outcome, current-source selection, answer grounding, trajectory control, or reliability. A single case can inform more than one claim.
3. **Evaluator method — how evidence is judged.** It may combine a deterministic assertion, comparison with a reference or authoritative observation, a rubric, qualified human judgment, or another fit-for-claim method. The methods chapter explains selection and fitness.
4. **Suite purpose — why the set is run.** Examples include development feedback, regression, release holdout, acceptance, or operational learning. Acceptance is a decision context or suite purpose here, not a mutually exclusive technical boundary.
5. **Lifecycle/environment — when and under what exposure.** Examples include controlled offline work, staging, guarded live use, or production monitoring. State the environment separately from suite purpose; a production observation is not automatically side-effect-free, and monitoring does not by itself establish a pre-release claim.

This separation prevents category errors. “Unit-level” says where a check runs, not whether it is deterministic. “Grounding” says what is assessed, not whether a human or assertion judges it. A release holdout can contain system-level cases and run offline.

## Worked example: current policy answer

Consider the fictional policy assistant described throughout Part 4: `policy-assistant@candidate-current-selection` answers from approved, current, permission-filtered documents and has no external write capability. A user asks for a London hotel limit. The controlled fixture `travel-policy-current` at revision `fixture-2026-10-18.1` contains the current document `travel-policy-2026`, revision `2026-10-01`, stating GBP 220. All names and facts below are illustrative; no candidate execution or live evaluation is claimed.

A compact record could describe the same case like this:

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

The integration boundary is useful because the claim depends on both the assistant and the controlled source/permission interface. The permission check can establish whether the relevant source is permitted; it cannot establish that the answer’s meaning is supported. The human support rubric can judge whether “GBP 220” follows from the cited current passage; it cannot prove the retrieval boundary enforced the user’s permission. The evaluation compares both evidence streams with the case’s acceptance criteria and keeps their conclusions distinct. If the permission check passes but the answer invents an exception, the support claim fails; if the answer is grounded but the source was not permitted, the access claim still fails. Neither evaluator alone answers the whole question.

The five descriptors are independent: integration level; current-source selection and semantic support properties; two different evaluator methods; development-suite purpose; controlled-offline environment. A later regression run could reuse the case for a different suite purpose without changing its technical level. A production observation would have a different lifecycle/environment label and would need its own exposure and evidence context.

## Evidence and checklist

When reading or writing a Part 4 record, check that:

- [ ] The record distinguishes an individual test/probe from the broader evaluation claim when that distinction matters.
- [ ] Cases, trials, suites, fixtures, references, observations, evaluators, and trajectories are not collapsed into one field or label.
- [ ] The five descriptors are stated independently; the case may carry multiple assessed properties.
- [ ] Expected criteria are distinguishable from the source or state observation and from the evaluator’s judgment.
- [ ] Trajectory evidence is limited to relevant observable events; private reasoning is not required.
- [ ] The shared policy-assistant identifiers and fixture facts are preserved, and illustrative material is not presented as an executed result.

See [4.2](02-test-levels-techniques-and-suite-purposes.md) for levels, techniques, and suite purposes; [4.3](03-evaluation-types-and-dimensions.md) for assessed properties; [4.4](04-evaluators-metrics-rubrics-and-calibration.md) for evaluator methods; [4.5](05-planning-designing-and-running-tests-and-evaluations.md) for planning and execution; [4.6](06-standards-required-coverage-and-execution-cadence.md) for applicable coverage policy; and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) for analysis and decisions. The [practical reference](reference/README.md) connects these ideas in the shared example and reusable records.

## References

[1]: https://glossary.istqb.org/en_US/term/test "ISTQB Glossary: Test"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[3]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"
[4]: https://glossary.istqb.org/en_US/term/test-case "ISTQB Glossary: Test Case"
[5]: https://glossary.istqb.org/en_US/term/verification "ISTQB Glossary: Verification"

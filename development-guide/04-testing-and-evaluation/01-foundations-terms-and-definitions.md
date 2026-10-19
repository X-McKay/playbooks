# 4.1 Foundations, Terms, and Definitions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** Use these distinctions whenever you plan or read evidence for a material claim. The vocabulary implies no particular architecture or test tool.  
**Reader question:** What are we talking about, and how do the pieces fit together?

[Part 4 — Testing and Evaluation](README.md) · [Playbook home](../../README.md) · [Glossary](../../glossary.md) · [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) · [Practical reference](reference/README.md)

This chapter sets the vocabulary used across Part 4. The [glossary](../../glossary.md) indexes these definitions. Later chapters cover how to exercise a claim, pick an evaluator, plan runs, and read results.

## Tests and evaluations overlap

In this playbook, a **test** is a designed execution or probe under stated conditions that records observations about one or more properties. It may be automated or human-run, deterministic or variable, isolated or end-to-end. This is a local working definition. The ISTQB glossary, for example, defines a test as a set of one or more test cases.[1]

An **evaluation** is the planned assessment of a bounded claim or decision. It selects cases and evidence, applies one or more evaluators, and says what the results establish and what they do not. Tests are common inputs, but an evaluation can also use expert review, samples, or operational observation. NIST describes testing, evaluation, verification, and validation (TEVV) as activities performed throughout the AI lifecycle and tied to context and intended use.[2] The test/evaluation distinction above is this playbook's own. Agent-evaluation practice likewise uses structured tasks and graders to assess variable systems.[3]

The distinction is about **scope**, not system type: a stochastic agent can be tested, and a deterministic permission assertion can feed an evaluation. Everyday speech uses the two words loosely; keep the distinction where it makes records and decisions clearer.

## The working vocabulary

- **Evaluator:** The rule, procedure, instrument, or qualified human role that turns stated evidence into a judgment. A permission predicate and a semantic review are different evaluators, even on the same case.
- **Case:** A versioned, bounded task or probe with conditions and inputs, expected observable outcomes or invariants, permitted variation, and an origin or rationale. ISTQB describes test cases through elements such as preconditions, inputs, and expected results.[4]
- **Trial:** One recorded execution of a case under an identified candidate configuration and starting conditions. Trials may share a case, fixture, time window, or dependency, so they are not automatically independent observations.
- **Suite:** A versioned set of cases chosen for a coverage goal or purpose. "Regression" or "development" says why a suite runs, not which boundary it exercises.
- **Fixture:** The revisioned starting data, state, and dependency behavior needed to interpret a case. It may define isolation and reset checks. It sets up a controlled world; it is not the rule that judges the result.
- **Reference and oracle:** A **reference** is an expected value, accepted set, label, or invariant. An **authoritative state observation** is a trusted observation of relevant state or effect. "Oracle" is used for either, so name its role, scope, authority, and time or version instead. The evaluator is the comparison or judgment procedure. A source document, a state observation, and an evaluator are different things.
- **Trajectory:** The externally observable, ordered or partly ordered events relevant to a claim, such as a request, permission decision, retrieved source identity, response, and state observation. Describe only what is needed to establish the claim. Private chain-of-thought is not a trajectory requirement and does not replace outcome evidence.
- **Verification and validation:** Verification confirms, with objective evidence, that specified requirements have been fulfilled; validation confirms that the requirements for an intended use have been fulfilled.[5] NIST also ties validation to intended use.[2] Neither is a synonym for a test method or lifecycle stage.

Keep the expected criterion, the observation, and the judgment apart. "Cite the current approved policy" is a criterion; the fixture's document record shows which revision was current; a source-support evaluator judges whether the cited text supports the answer. A citation's presence or metadata does not prove semantic support.

## Five independent descriptors

Describe a case or evaluation with five separate descriptors. One item can have several values on the property axis and one value on each other axis.

1. **Test level — where the property is exercised.** The observed boundary, such as unit, component, integration, or system. Teams draw these lines differently, so state what is included.
2. **Assessed property — what is claimed.** Task outcome, current-source selection, answer grounding, trajectory control, reliability, and so on. One case can inform several claims.
3. **Evaluator method — how evidence is judged.** A deterministic assertion, comparison with a reference or authoritative observation, a rubric, qualified human judgment, or another method that fits the claim ([4.4](04-evaluators-metrics-rubrics-and-calibration.md)).
4. **Suite purpose — why the set runs.** Development feedback, regression, release holdout, acceptance, or operational learning. Acceptance is a decision context here, not a technical boundary.
5. **Lifecycle/environment — when and under what exposure.** Controlled offline, staging, guarded live use, or production monitoring. Production observation is not automatically side-effect-free, and monitoring alone does not establish a pre-release claim.

This keeps categories apart. "Unit-level" says where a check runs, not whether it is deterministic. "Grounding" says what is assessed, not who judges it. A release holdout can hold system-level cases and run offline.

## Worked example: current policy answer

The fictional policy assistant used throughout Part 4, `policy-assistant@candidate-current-selection`, answers from approved, current, permission-filtered documents and has no external write capability. A user asks for a London hotel limit. The controlled fixture `travel-policy-current` at revision `fixture-2026-10-18.1` holds the current document `travel-policy-2026`, revision `2026-10-01`, stating GBP 220. All names and facts here are fictional; no execution is claimed.

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

Integration is the right level because the claim depends on both the assistant and the source/permission interface. The permission check shows whether the source was permitted; it cannot show that the answer's meaning is supported. The human rubric can judge whether "GBP 220" follows from the cited passage; it cannot show the retrieval boundary enforced the user's permission. Keep their conclusions distinct. If the permission check passes but the answer invents an exception, the support claim fails. If the answer is grounded but the source was not permitted, the access claim fails.

The descriptors are independent: integration level; two properties; two evaluator methods; development purpose; controlled-offline environment. A later regression run can reuse the case for a different purpose without changing its level. A production observation would need its own environment label and exposure context.

## Evidence and checklist

- [ ] The record separates an individual test/probe from the broader evaluation claim where that matters.
- [ ] Cases, trials, suites, fixtures, references, observations, evaluators, and trajectories are not collapsed into one field.
- [ ] The five descriptors are stated independently; a case may carry several properties.
- [ ] Expected criteria are distinct from the source or state observation and from the evaluator's judgment.
- [ ] Trajectory evidence covers only relevant observable events; private reasoning is not required.
- [ ] Shared policy-assistant identifiers are preserved, and illustrative material is not presented as an executed result.

See [4.2](02-test-levels-techniques-and-suite-purposes.md) for levels and techniques, [4.3](03-evaluation-types-and-dimensions.md) for properties, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) for evaluators, [4.5](05-planning-designing-and-running-tests-and-evaluations.md) for planning, [4.6](06-standards-required-coverage-and-execution-cadence.md) for coverage policy, and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) for decisions.

## References

[1]: https://glossary.istqb.org/en_US/term/test "ISTQB Glossary: Test"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf "NIST Artificial Intelligence Risk Management Framework 1.0"
[3]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"
[4]: https://glossary.istqb.org/en_US/term/test-case "ISTQB Glossary: Test Case"
[5]: https://glossary.istqb.org/en_US/term/verification "ISTQB Glossary: Verification"

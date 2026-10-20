# 10.2 Bias, Human Impact, and Domain Assurance

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Agent builders, domain and accessibility specialists, evaluators, accountable owners, and reviewers  
**Applicability:** Any production agent that can plausibly affect people or groups. Go further where outputs inform consequential decisions, the domain is sensitive, access is unequal, or users may over-rely on it.

[Part 10](README.md) · [Applicability and conformance](../../applicability.md) · [10.1 Detailed Risk Assessment and Governance](01-detailed-risk-assessment-and-governance.md) · [10.3 Advanced Privacy, Isolation, and Auditability](03-advanced-privacy-isolation-and-auditability.md) · [4.3 Evaluation Types and Dimensions](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md)

## Purpose and applicability

A system can score well in aggregate yet exclude, disadvantage, mislead, or burden particular people, or look neutral while repeating assumptions in its data, workflow, or institution. This chapter helps you find whose outcomes matter, choose proportionate assurance, and check domain fit, without one fairness definition or threshold.

Read-only access does not remove human-impact risk. A simple internal assistant may need only a documented screen and focused checks; one influencing employment, health, education, housing, credit, legal services, or similar choices needs stronger domain review. Accountable reviewers decide whether a law, policy, or classification applies.

[10.1](01-detailed-risk-assessment-and-governance.md) owns the risk method, scoring, floors, and acceptance; Part 4 owns evaluation design, evaluator calibration (including evaluator bias), and behavioral test claims. This chapter owns the human-impact analysis: who may be affected, which differences matter, what domain limits constrain use, and what human oversight can really do.

## Working model

Start with the use, not "Is the model fair?" Describe the output or action, its recipients, non-users it affects, how outcomes can be contested or corrected, and the decision environment. Affected groups include people whose records are processed, people discussed in an answer, and people subject to a decision based on it. The population shifts with setting, language, geography, disability, time, or access to other support.

Bias enters through institutional practice, sampling and missing data, measurement, annotation, product assumptions, or how outputs are acted on. NIST describes systemic, statistical, and human sources and warns that technical fixes alone do not settle socio-technical harms.[2] Subgroup metrics help but miss harm when groups are poorly defined, the outcome is a weak proxy, the sample is small, or the use itself is inappropriate.

The AI RMF adds that impact depends on context and measurement can hide differences between groups or settings.[1] Document uncertainty and involve relevant expertise. Collecting sensitive attributes can itself create privacy and safety risk: decide with privacy review whether it is necessary, lawful, proportionate, and protected; if not, use other evidence and record what remains unknown. For generative agents, NIST AI 600-1 lists risks such as confabulation and harmful bias, with suggested actions.[4]

Domain assurance asks whether evidence, language, boundaries, and failure behavior suit the task. A correct-looking answer is unsafe if it omits an exception, uses a superseded source, conveys uncertainty poorly, or is inaccessible to the person who needs it. Human review helps only when reviewers have the competence, context, time, and a practical way to disagree, stop, or escalate; an approval people cannot meaningfully perform is not a control.

## Decisions and best practices

**Set the population and boundary before choosing a metric,** including the languages, formats, jurisdictions, and circumstances the system is not validated for. If the use expands, revisit the boundary rather than assuming the evidence transfers.

**Pick slices from plausible harms.** Examples: language or accessibility needs, relevant demographic groups where lawful and appropriate, source availability, and case types with different consequences. Compare task-relevant outcomes, not only model scores: correctness and support, false confidence, refusal or escalation, delay, accessibility barriers, and burden of correction. State the denominator and how cases enter each slice; a tiny sample shows uncertainty, not "no disparity". No single metric settles every use.

**Choose reviewers for the claim.** Domain specialists find missing constraints and misleading readings; affected users reveal barriers and burdens internal reviewers miss; accessibility specialists assess assistive access and interaction. Use independent review when consequence or uncertainty is high, and give participants a safe, respectful, accessible way to take part. W3C recommends evaluating accessibility throughout development and notes that tools alone cannot determine it; knowledgeable human evaluation is needed.[3]

**Design oversight as part of the system.** Specify what triggers review, what the reviewer sees, their authority to correct, stop, or escalate, and the fallback when no reviewer is available (IMPACT-04); also decide how uncertainty and source conflicts are shown to them. A confident tone never stands in for evidence or a competent decision-maker; with no meaningful review path, constrain the use or decline the capability.

**Evaluate and reassess.** Use the risk-linked approach in [4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) and Part 4's claim-specific methods. Reassess when complaints, incidents, feedback, data shifts, workflow changes, or new contexts challenge the assumptions; neither noisy signals nor a lack of complaints proves harmlessness.

## Requirements

- **IMPACT-01** — When a production agent can plausibly affect people or groups through an answer, omission, recommendation, or downstream use, the owner MUST document the intended domain, affected populations (including affected non-users where relevant), foreseeable reliance, exclusions, and meaningful limits of validated use.
- **IMPACT-02** — When the harm assessment identifies plausible differences in outcome or access, the owner MUST define relevant, task-linked slices and outcomes before interpreting aggregate results; report sample limitations and uncertainty, and MUST NOT describe unmeasured or underpowered groups as showing no material difference.
- **IMPACT-03** — When consequences, domain uncertainty, accessibility, or plausible disparate impact exceed the team's competence to assess, the owner MUST obtain and record review from appropriately qualified domain or accessibility reviewers and, where relevant and safe, people representing affected perspectives; the record MUST state the review's scope and known representation gaps.
- **IMPACT-04** — When human oversight is a credited control or required for a consequential use, the system owner MUST specify the review trigger, information available to the reviewer, authority to correct, stop, or escalate, and fallback when review is unavailable; MUST NOT credit oversight that is merely nominal or that cannot change the outcome in time.
- **IMPACT-05** — Before release and after a material change in domain, population, source, or workflow, the owner MUST link each material human-impact scenario to relevant domain evidence and a response or reassessment trigger; unsupported scope MUST be constrained, escalated, or treated as unresolved rather than presumed safe.

## Worked example: internal policy assistant

A fictional read-only assistant answers from approved, current, permission-filtered policy documents with citations. In the `travel-policy-current` fixture, a London hotel amount is GBP 220 while a superseded document differs. A misleading answer could still cost an employee money or time, and a manager might rely on a summary when advising someone else.

The domain is internal policy questions from the approved corpus; affected people are askers and those advised on the answer. Excluded: legal advice, adjudication of reimbursement claims, and questions where the sources do not establish the current rule. The owner checks whether location, language, assistive technology, or access to policy sources could change a user's ability to get or understand an answer; these become slices only if relevant and safe to assess.

Suppose review finds the London answer supported, but some screen-reader users cannot navigate the citations and uncertainty: content checks alone are not domain assurance. The team works with accessibility expertise and affected users to specify accessible behavior, then tests it with human review and automated checks. For an exception absent from approved documents, the assistant returns `needs_information` or escalates; if that route depends on a human, the owner confirms an accountable reviewer can resolve it, or the assistant states the limitation.

The record ties the scenario to the boundary, versioned cases, findings, representation limits, escalation path, and response owner. Part 4 judges the evaluation and [10.1](01-detailed-risk-assessment-and-governance.md) the tier and acceptance; a passing average cannot override an unresolved material accessibility failure or missing evidence for a critical use.

## Evidence and checklist

Before release, confirm that:

- [ ] Likely unequal access or outcomes shaped the slices, and sensitive data collection was reviewed for necessity and protection.
- [ ] Results are separated by relevant population and context, with sample size, uncertainty, and representation limits stated.
- [ ] Any credited oversight has evidence that people can actually use it.
- [ ] Domain limits, supported, prohibited, and escalated cases, and reassessment triggers are in the contract and risk record.
- [ ] Material findings link to versioned evaluation evidence, owners, and a treatment; unresolved hard gates or missing required evidence block release.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI RMF 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.Sp.1270.pdf "Towards a Standard for Identifying and Managing Bias in Artificial Intelligence"
[3]: https://www.w3.org/WAI/test-evaluate/ "Evaluating Web Accessibility Overview"
[4]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1 Generative AI Profile"

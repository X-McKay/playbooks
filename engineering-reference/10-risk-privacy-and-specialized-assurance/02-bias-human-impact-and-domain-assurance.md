# 10.2 Bias, Human Impact, and Domain Assurance

**Status:** 0.5.0-draft.2 — draft
**Audience:** Agent builders, domain and accessibility specialists, evaluators, accountable owners, and reviewers
**Applicability:** Any production agent that can plausibly affect people or groups. Go further where outputs inform consequential decisions, the domain is sensitive, access is unequal, or users may rely on the agent despite uncertainty.

[Part 10](../README.md) · [Applicability and conformance](../../applicability.md) · [10.1 Detailed Risk Assessment and Governance](01-detailed-risk-assessment-and-governance.md) · [10.3 Advanced Privacy, Isolation, and Auditability](03-advanced-privacy-isolation-and-auditability.md) · [4.3 Evaluation Types and Dimensions](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md)

## Purpose and applicability

A system can score well in aggregate and still exclude, disadvantage, mislead, or burden particular people. It can look neutral while repeating assumptions in its data, workflow, or surrounding institution. This chapter helps you find whose outcomes matter, choose proportionate assurance, and check that the system fits its actual domain. It does not prescribe one definition of fairness or a universal threshold.

Use it when people may rely on an answer, be affected by an omission, or face a downstream decision the agent influenced. Read-only access does not remove human-impact risk. A simple internal knowledge assistant may need only a documented screen and focused checks. A system that influences employment, health, education, housing, credit, legal services, or similar choices needs a stronger domain review. Whether a law, policy, or formal classification applies is for the accountable reviewers to decide.

Ownership is split. [10.1](01-detailed-risk-assessment-and-governance.md) owns the risk method, scoring, floors, and acceptance. Part 4 owns evaluation design, evaluator calibration, and behavioral test claims. This chapter owns the human-impact analysis: who may be affected, which differences matter, what domain limits constrain use, and what human oversight can really do. Bias in evaluators is a different problem from bias in system outcomes; handle it in Part 4.

## Working model

Start with the use, not an abstract question like "Is the model fair?" Describe the output or action, its recipients, who may be affected without using it, how people can contest or correct an outcome, and the decision environment. Affected groups can include people whose records are processed, people discussed in an answer, and people subject to a decision made by someone who relied on it. The population can change with setting, language, geography, disability, time, or access to other support.

Bias can enter through historical or institutional practice, sampling and missing data, measurement choices, annotation, product assumptions, or how an output is read and acted on. NIST describes systemic, statistical, and human sources, warns that technical fixes alone do not settle socio-technical harms, and says no single practice is a cure-all.[2] Subgroup metrics help but are not a full assurance case. A comparison can miss harm if the groups are poorly defined, the outcome is a weak proxy, the sample is too small, or the use itself is inappropriate.

The AI Risk Management Framework adds that impact depends on context, that affected groups may not be direct users, and that measurement methods can hide differences between groups or settings.[1] Document uncertainty and involve relevant expertise. Do not assume every deployment needs the same survey or demographic data. Collecting sensitive attributes can itself create privacy and safety risk. Decide whether the data is necessary, lawful, proportionate, and protected, with privacy review. If it cannot be collected safely, use other evidence and record what remains unknown. For generative agents, the NIST Generative AI Profile (AI 600-1) lists risks such as confabulation and harmful bias, with suggested actions.[4]

Domain assurance asks whether the agent's evidence, language, boundaries, and failure behavior suit the task. A correct-looking answer can still be unsafe if it omits an exception, uses a superseded source, conveys uncertainty poorly, or is inaccessible to the person who needs it. Human review helps only when reviewers have the competence, context, and time, and a practical way to disagree, stop, or escalate. An approval step people cannot meaningfully perform is not a control.

## Decisions and best practices

Set the population and boundary before choosing a metric. Consider the people who use the agent and those affected by its outputs, omissions, or downstream use. Name the intended settings and the exclusions: languages, formats, jurisdictions, and user circumstances the system is not validated for. If the use expands, revisit the boundary instead of assuming the evidence transfers.

Pick outcome slices from plausible harms and context. Examples are language or accessibility needs, relevant demographic groups where lawful and appropriate, source availability, and case types with different consequences. Compare task-relevant outcomes, not only model scores: correctness and support, false confidence, refusal or escalation, delay, accessibility barriers, and burden of correction. State the denominator and how cases enter each slice. Do not infer "no disparity" from a tiny or unrepresentative sample; report uncertainty and look for other evidence. No single ratio or fairness metric settles every use.

Choose reviewers for the claim. A domain specialist finds missing constraints and misleading readings. Affected users reveal barriers and burdens that internal reviewers miss. An accessibility specialist assesses assistive access and interaction. Use independent review when consequence or uncertainty is high. Give people a safe, respectful, accessible way to take part, and record whom the review represented and whom it did not. For web and application accessibility, W3C recommends evaluating throughout development and notes that tools alone cannot determine accessibility; knowledgeable human evaluation is needed.[3]

Design oversight as part of the system, not a checkbox. Decide which cases need a reviewer, what evidence the reviewer sees, how uncertainty and source conflicts are shown, whether the reviewer can change or stop the outcome, and what happens when no reviewer is available. For consequential decisions, do not let a confident tone stand in for evidence or a competent decision-maker. If there is no meaningful review path, constrain the use or decline the capability.

Use the risk-linked evaluation approach in [4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) and the claim-specific methods in Part 4. Reassess when complaints, incidents, feedback, data shifts, workflow changes, or new contexts challenge the original assumptions. Do not treat noisy signals, or a lack of complaints, as proof of harmlessness.

## Requirements

- **IMPACT-01** — When a production agent can plausibly affect people or groups through an answer, omission, recommendation, or downstream use, the owner MUST document the intended domain, affected populations (including affected non-users where relevant), foreseeable reliance, exclusions, and meaningful limits of validated use.
- **IMPACT-02** — When the harm assessment identifies plausible differences in outcome or access, the owner MUST define relevant, task-linked slices and outcomes before interpreting aggregate results; report sample limitations and uncertainty, and MUST NOT describe unmeasured or underpowered groups as showing no material difference.
- **IMPACT-03** — When consequences, domain uncertainty, accessibility, or plausible disparate impact exceed the team's competence to assess, the owner MUST obtain and record review from appropriately qualified domain or accessibility reviewers and, where relevant and safe, people representing affected perspectives; the record MUST state the review's scope and known representation gaps.
- **IMPACT-04** — When human oversight is a credited control or required for a consequential use, the system owner MUST specify the review trigger, information available to the reviewer, authority to correct, stop, or escalate, and fallback when review is unavailable; MUST NOT credit oversight that is merely nominal or that cannot change the outcome in time.
- **IMPACT-05** — Before release and after a material change in domain, population, source, or workflow, the owner MUST link each material human-impact scenario to relevant domain evidence and a response or reassessment trigger; unsupported scope MUST be constrained, escalated, or treated as unresolved rather than presumed safe.

## Worked example: internal policy assistant

An internal assistant answers questions from approved, current, permission-filtered policy documents. It returns citations and uncertainty and has no external write capability. In the fictional fixture `travel-policy-current`, a London hotel amount is GBP 220, while a superseded document differs. The assistant is read-only, yet an employee could still incur avoidable expense or lose time from a misleading answer, and a manager might rely on a generated summary when advising someone else.

The owner defines the domain as internal policy questions answered from the approved corpus. Affected people are the employees who ask and those affected by advice based on the answer. Excluded: legal advice, adjudication of reimbursement claims, and any question where the source set does not establish the current rule. The owner checks whether location, language, assistive technology, or access to policy sources could change a user's ability to get or understand an answer. These become slices only if relevant to the documented use and safe to assess.

Suppose a review finds the current London answer is supported, but the interface presents uncertainty and citations in a way some screen-reader users cannot navigate. The content check is then not overall domain assurance. The team works with accessibility expertise and affected users to specify accessible citation and uncertainty behavior, then tests it with human review and automated checks. If a user asks about an exception absent from approved documents, the assistant returns `needs_information` or escalates instead of inferring an answer. If that route depends on a human, the owner confirms that an accountable reviewer is available and can resolve the question; otherwise the assistant states the limitation.

The evidence record ties the risk scenario to the population and domain boundary, the versioned cases and source fixture, the accessibility and domain findings, representation limits, the escalation path, and the response owner. Part 4 decides whether the evaluation supports the claims; [10.1](01-detailed-risk-assessment-and-governance.md) decides the tier and acceptance. A passing average cannot override an unresolved material accessibility failure or missing evidence for a critical use.

## Evidence and checklist

Before release, confirm that:

- [ ] The intended domain, affected people (including relevant non-users), reliance path, and exclusions are documented.
- [ ] Potential harms and likely unequal access or outcomes shaped the slices; sensitive data collection was reviewed for necessity and protection.
- [ ] Results are separated for relevant populations and contexts, with sample size, uncertainty, and representation limits stated; unsupported gaps stay visible.
- [ ] Qualified reviewers and affected perspectives were involved where needed, and their scope, expertise, and limits are recorded.
- [ ] Any credited human oversight has a clear trigger, enough information, effective authority, a timely fallback, and evidence that people can use it.
- [ ] Domain limits, supported cases, prohibited or escalated cases, and reassessment triggers are in the contract and risk record.
- [ ] Material findings link to versioned evaluation evidence, owners, and a treatment; unresolved hard gates or missing required evidence block release under the applicable readiness rules.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework AI RMF 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.Sp.1270.pdf "Towards a Standard for Identifying and Managing Bias in Artificial Intelligence"
[3]: https://www.w3.org/WAI/test-evaluate/ "Evaluating Web Accessibility Overview"
[4]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"

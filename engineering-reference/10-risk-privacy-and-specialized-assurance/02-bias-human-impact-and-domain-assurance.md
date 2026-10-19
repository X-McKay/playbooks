# 10.2 Bias, Human Impact, and Domain Assurance

**Status:** 0.5.0 first draft
**Audience:** Agent builders, domain and accessibility specialists, evaluators, accountable owners, and reviewers
**Applicability:** Any production agent with a plausible effect on people or groups; enhanced assessment is needed where outputs inform consequential decisions, the domain is sensitive, access is unequal, or users may rely on the agent despite uncertainty.

[Part 10](../README.md) · [Applicability and conformance](../../applicability.md) · [10.1 Detailed Risk Assessment and Governance](01-detailed-risk-assessment-and-governance.md) · [10.3 Advanced Privacy, Isolation, and Auditability](03-advanced-privacy-isolation-and-auditability.md) · [4.3 Evaluation Types and Dimensions](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md)

## Purpose and applicability

A system can perform well on an aggregate score and still systematically exclude, disadvantage, mislead, or burden particular people. It can also appear neutral while reproducing assumptions in its data, workflow, or surrounding institution. This chapter helps teams identify whose outcomes matter, select proportionate assurance, and establish whether the system is fit for its actual domain. It does not prescribe one definition of fairness or a universal statistical threshold.

Use this chapter when people may rely on an answer, be affected by an omission, or experience a downstream decision influenced by the agent. Read-only access does not remove human-impact risk. A simple internal knowledge assistant may need a documented screen and focused checks; a system that influences employment, health, education, housing, credit, legal services, or similarly consequential choices needs a stronger domain review. An applicable law, policy, or formal classification must be assessed separately by the accountable reviewers; completing this chapter is not proof of compliance.

Part 10.1 owns the general risk method, scoring, floors, and acceptance. Part 4 owns evaluation design, evaluator calibration, and behavioral test claims. This chapter owns the human-impact analysis: who may be affected, which differences matter in context, what domain limitations constrain use, and what role human oversight can actually play. Evaluator bias is a different problem from bias or disparate impact in system outcomes; address the former in Part 4.

## Working model

Start with the use, not with an abstract question such as “Is the model fair?” Describe the output or action, its recipients, who may be affected without directly using it, how people can contest or correct an outcome, and the decision environment into which the agent is placed. Affected groups may include people whose records or documents are processed, people discussed in an answer, and people subject to a decision made by someone who relies on it. The population can change by setting, language, geography, disability, time, or access to alternative support.

Bias can enter through historical or institutional practice, sampling and missing data, measurement choices, annotation, product assumptions, or the way an output is interpreted and acted upon. NIST describes systemic, statistical, and human sources and warns that technical fixes alone do not settle socio-technical harms; no single practice is a cure-all.[2] Accordingly, checking subgroup metrics is useful but not a complete assurance case. A comparison can miss a harm if the groups are poorly defined, the outcome is an inadequate proxy, the sample is too small, or the intended use itself is inappropriate.

NIST's AI Risk Management Framework similarly emphasizes that impact depends on context, that groups who are affected may not be direct users, and that measurement methods can obscure differences between groups or settings.[1] These are reasons to document uncertainty and involve relevant expertise—not reasons to claim that every deployment needs the same survey or demographic data collection. Collecting sensitive attributes can itself create privacy and safety risks. Decide whether those data are necessary, lawful, proportionate, and protected with the appropriate privacy review; if they cannot be collected safely, use other evidence and record what remains unknown.

Domain assurance asks whether the agent's evidence, language, boundaries, and failure behavior are suitable for the task. A correct-looking answer may still be unsafe if it omits a relevant exception, uses a superseded source, communicates uncertainty poorly, or is inaccessible to a person who needs it. Human review helps only when reviewers have the relevant competence, enough context and time, and a practical way to disagree, stop, or escalate. A nominal approval step that people cannot meaningfully perform is not an effective control.

## Decisions and best practices

Set the population and boundary before selecting a metric. Consider the people who directly use the agent and those affected by its outputs, omissions, or downstream use. Identify intended settings and exclusions, including languages, formats, jurisdictions, and user circumstances the system has not been validated for. If the use expands, revisit this boundary rather than assuming the original evidence transfers.

Select outcome slices from plausible harms and context. Examples include language or accessibility needs, relevant demographic groups where lawful and appropriate, source availability, and types of cases with different consequences. Compare task-relevant outcomes, not just model scores: answer correctness and support, false confidence, refusal or escalation, delay, accessibility barriers, and burden of correction may matter differently. State the denominator and how cases enter each slice. Do not infer “no disparity” from a tiny or unrepresentative sample; report uncertainty and seek other evidence. There is no single ratio or fairness metric that settles every use case.

Choose reviewers for the claim. A domain specialist can identify missing constraints or misleading interpretations; affected users can reveal barriers and burdens that internal reviewers may not see; an accessibility specialist can assess assistive access and interaction. Use appropriately independent review when the consequence or uncertainty warrants it. Provide a safe, respectful, and accessible way to participate, and document whom the review represented and whom it did not. For web and application accessibility specifically, W3C recommends evaluation throughout development and notes that tools alone cannot determine accessibility; knowledgeable human evaluation is needed.[3]

Treat oversight as part of the system design, not a checkbox. Decide which cases require a reviewer, what evidence the reviewer sees, how uncertainty and source conflicts are presented, whether the reviewer can change or stop the outcome, and what happens when review is unavailable. For consequential decisions, do not use an agent's confident tone as a substitute for evidence or a competent decision-maker. Where there is no meaningful review path, constrain the use or decline the capability.

Use the risk-linked evaluation approach in [4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) and the claim-specific methods in Part 4. Reassess when complaints, incidents, user feedback, data shifts, workflow changes, or new deployment contexts challenge the initial assumptions. Monitor carefully without treating noisy signals or a lack of complaints as proof of harmlessness.

## Requirements

- **IMPACT-01** — When a production agent can plausibly affect people or groups through an answer, omission, recommendation, or downstream use, the owner MUST document the intended domain, affected populations (including affected non-users where relevant), foreseeable reliance, exclusions, and meaningful limits of validated use.
- **IMPACT-02** — When the harm assessment identifies plausible differences in outcome or access, the owner MUST define relevant, task-linked slices and outcomes before interpreting aggregate results; report sample limitations and uncertainty, and MUST NOT describe unmeasured or underpowered groups as showing no material difference.
- **IMPACT-03** — When consequences, domain uncertainty, accessibility, or plausible disparate impact exceed the team's competence to assess, the owner MUST obtain and record review from appropriately qualified domain or accessibility reviewers and, where relevant and safe, people representing affected perspectives; the record MUST state the review's scope and known representation gaps.
- **IMPACT-04** — When human oversight is a credited control or required for a consequential use, the system owner MUST specify the review trigger, information available to the reviewer, authority to correct, stop, or escalate, and fallback when review is unavailable; MUST NOT credit oversight that is merely nominal or that cannot change the outcome in time.
- **IMPACT-05** — Before release and after a material change in domain, population, source, or workflow, the owner MUST link each material human-impact scenario to relevant domain evidence and a response or reassessment trigger; unsupported scope MUST be constrained, escalated, or treated as unresolved rather than presumed safe.

## Worked example: internal policy assistant

An internal assistant answers questions from approved, current, permission-filtered policy documents. It returns citations and uncertainty and has no external write capability. The example fixture `travel-policy-current` says a London hotel amount is GBP 220, while a superseded document differs. This is fictional test data, not actual policy. The assistant is read-only, but an employee could still incur avoidable expense or lose time if an answer is misleading. A manager might also rely on a generated summary when advising another employee.

The owner defines the domain as internal policy questions answered from the approved corpus and identifies employees who ask questions plus people affected by advice based on the answer. It explicitly excludes legal advice, adjudication of reimbursement claims, and any question for which the source set does not establish the current rule. The owner checks whether location, language, assistive technology, or access to policy sources could change the user's ability to obtain or understand an answer; those are candidate slices only if relevant to the documented use and feasible to assess safely.

A hypothetical review finds that the current policy answer is supported for the London fixture, but the interface presents uncertainty and citations in a way that some screen-reader users cannot navigate. This is an illustrative failure, not a measured result. The response is not to report the content check as overall domain assurance. The team works with accessibility expertise and affected users to specify accessible citation and uncertainty behavior, then evaluates those interaction claims with suitable human review and automated checks. If a user asks about an exception absent from approved documents, the assistant returns `needs_information` or escalates rather than inferring an answer. If that route depends on a human, the owner checks that an accountable reviewer is available and can resolve the question; otherwise the assistant states the limitation.

The evidence record ties the risk scenario to the population and domain boundary, the versioned cases and source fixture, the relevant accessibility/domain findings, limitations in representation, the escalation path, and the response owner. Part 4 determines whether the evaluation method and release evidence support the claims; Part 10.1 determines the risk tier and acceptance. A passing average cannot override an unresolved material accessibility failure or missing evidence for a critical use.

## Evidence and checklist

Before release, confirm that:

- [ ] The intended domain, affected people (including relevant non-users), reliance path, and exclusions are documented.
- [ ] Potential harms and likely unequal access or outcomes shaped the selected slices; sensitive data collection has been reviewed for necessity and protection.
- [ ] Results are separated for relevant populations and contexts, with sample size, uncertainty, and representation limits stated; unsupported gaps remain visible.
- [ ] Qualified reviewers and affected perspectives were involved where needed, and their scope, expertise, and limitations are recorded.
- [ ] Any credited human oversight has a clear trigger, enough information, effective authority, a timely fallback, and evidence that people can use it.
- [ ] Domain-specific limitations, supported cases, prohibited or escalated cases, and reassessment triggers are reflected in the contract and risk record.
- [ ] Material findings link to versioned evaluation evidence, owners, and a documented treatment; unresolved hard gates or required evidence block release under the applicable readiness rules.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework AI RMF 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.Sp.1270.pdf "Towards a Standard for Identifying and Managing Bias in Artificial Intelligence"
[3]: https://www.w3.org/WAI/test-evaluate/ "Evaluating Web Accessibility Overview"

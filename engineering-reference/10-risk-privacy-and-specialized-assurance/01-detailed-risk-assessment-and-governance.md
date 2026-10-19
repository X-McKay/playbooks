# 10.1 Detailed Risk Assessment and Governance

**Status:** 0.5.0-draft.2 — draft
**Audience:** Accountable owners, builders, evaluators, security and privacy reviewers, and release decision authorities
**Applicability:** Use this method when the [initial risk, data, ownership, and delivery record](../../development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) shows elevated assurance needs: consequential authority, sensitive or regulated context, broad reach, material uncertainty, or a material harm scenario. Any team may also use it for a more defensible assessment. It does not replace legal, regulatory, security, privacy, safety, or domain review.

[Part 10](README.md) · [Applicability](../../applicability.md) · [Release decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

An assessment makes the reasoning behind a governance review inspectable. The accountable owner describes the context, names concrete ways the agent could cause harm, records the evidence behind each control, and gives the decision authority a basis for a release decision.

This chapter extends the early screen in Chapter 1.4. Start before design choices become expensive, update before release, and keep it current in operation. A compact record is enough for a bounded, low-exposure use, until a scenario, capability, legal screen, or policy floor triggers this detailed method. A matrix score is not a legal determination.

## Working model

### Keep the decisions separate

Five terms answer different questions:

- **Execution class** is how work executes: `ephemeral`, `durable`, or `human_governed`.
- **Governance tier** is the required assurance and oversight: `low`, `medium`, `high`, or `critical`.
- **Inherent risk** is the risk before risk-reducing controls.
- **Residual risk** is the risk after only those controls that have evidence of working.
- **Launch decision** is `go`, `conditional_go`, or `no_go` for a specific release.

Do not merge them. A read-only agent can be high risk because a wrong answer has serious consequences, and a durable agent can be medium risk. The governance tier is anchored to inherent risk and mandatory floors. A lower residual rating can make a release acceptable but does not lower the assurance the use needs.

### Run the assessment in order

1. Describe intended and prohibited uses, users, affected parties, jurisdictions, environment, and accountable roles.
2. Inventory the effective model policy, instructions, skills, tools, integrations, data sources, memory, workflows, providers, approval paths, and downstream consumers. Record their identity or version so evidence ties to what you assessed.
3. Run the prohibited-use and regulatory screen before scoring.
4. Write material harm scenarios, score each one inherently, identify controls and their evidence, score residual risk, derive the governance tier, choose a treatment, and record the decision and review date.

The builder may draft the record. An agent or model must not accept its own risk or authorize launch.

Treat amplifiers as evidence about a scenario's likelihood or impact, not as extra score dimensions:

- autonomy and ability to initiate actions
- tool effect, transaction authority, identity, and privilege
- data sensitivity, provenance, retention, and data subjects
- affected population, vulnerable groups, and public reach
- frequency, transaction value, and blast radius
- reversibility, compensation, detection, and time to intervene
- exposure to untrusted or adversarial content
- human review quality and ability to stop execution
- model uncertainty, dependency concentration, and supply-chain exposure

## Decisions and best practices

### Screen for prohibited and controlled uses first

Record the applicable jurisdictions, sectors, contractual duties, internal policies, and the legal, compliance, or domain reviewers who decide applicability. A prohibited use is `no_go` whatever its score. A binding classification sets a floor and required controls whatever the matrix says. Health, employment, education, credit, insurance, housing, legal services, biometrics, critical infrastructure, children, and similar consequential decisions need a documented applicability review and must not default to low risk. Unknown applicability is an unresolved risk, not proof that no obligation applies.

The matrix compares scenario reasoning. It does not establish a legal classification or prove compliance. Send that question to the named reviewer.

### Frameworks you may need to map to

Your organization or customers may ask for evidence in one of these frameworks. This is a pointer, not legal advice. Confirm applicability with your reviewers.

- **NIST AI RMF and the Generative AI Profile.** The AI Risk Management Framework is voluntary. NIST AI 600-1 (July 2024) adapts it to generative AI with suggested actions for govern, map, measure, and manage.[1], [2]
- **ISO/IEC 42001 and ISO/IEC 23894.** ISO/IEC 42001:2023 specifies an AI management system an organization can implement and be assessed against. ISO/IEC 23894:2023 gives guidance on managing AI-specific risk.[3], [4]
- **GDPR Article 35.** A data protection impact assessment is required before processing that is likely to result in a high risk to people's rights and freedoms. It must describe the processing and its purposes, assess necessity and proportionality and the risks to individuals, and list safeguards. Automated evaluation with significant effects and large-scale use of sensitive data are named triggers. See also [10.3](03-advanced-privacy-isolation-and-auditability.md).[5]
- **EU AI Act.** It is risk-based: some practices are prohibited, listed high-risk uses carry strict obligations (such as risk management, logging, documentation, and human oversight), some systems carry transparency duties, and most systems have no specific rules. General-purpose AI models have their own obligations. The obligations are phased in over several years, and the schedule has been amended, so check the current dates on the Commission's page before planning.[6]

The scenario method, evidence links, and decision records in this chapter can feed these frameworks. The frameworks do not replace the method.

### Write scenarios a reviewer can test

Use this form for each material scenario:

> Because **[cause or initiating condition]**, the agent could **[unsafe action, output, or omission]**, causing **[harm]** to **[affected party or asset]**.

Consider normal use, foreseeable misuse, adversarial content, dependency failure, model error, authorization failure, retry or concurrency behavior, operator error, and control failure. Each scenario needs:

- a stable ID, owner, and status
- affected parties and assets
- causes and preconditions, and consequences
- a primary dimension and any secondary ones
- scoring rationale and confidence
- controls with evidence, and a treatment
- links to evaluation cases, indicators, alerts, and runbooks

Consider every dimension even when it is not primary: financial, operational, reputational, legal, security, privacy, regulatory, and human impact and safety. Calibrate amounts, outage duration, populations, and data categories to the organization's risk appetite. This guide supplies a method, not universal thresholds.

### Score inherent and residual risk without false precision

Score the credible worst case within the documented scope, not the average. Impact:

- **1:** localized, short-lived, easily reversible, negligible external harm.
- **2:** meaningful but contained harm, recoverable through normal procedures.
- **3:** material financial, operational, legal, security, privacy, reputational, regulatory, or human harm.
- **4:** severe, widespread, systemic, life-safety, organization-threatening, or largely irreversible harm.

A control lowers impact only if it really limits blast radius, duration, affected population, or reversibility.

Likelihood:

- **1:** several unusual conditions are required and evidence supports rarity.
- **2:** credible but not expected in normal operation.
- **3:** plausible in normal or adversarial operation, or already observed.
- **4:** expected, repeated, or already occurring without intervention.

Inherent likelihood assumes no risk-reducing controls. Residual likelihood counts only implemented controls with evidence. Draw on evaluations, tests, incidents, comparable systems, threat intelligence, domain review, and production measurements.

Use the same matrix for both scores:

- With impact **1**, likelihood 1 or 2 is `low`; likelihood 3 or 4 is `medium`.
- With impact **2**, likelihood 1 is `low`; likelihood 2 or 3 is `medium`; likelihood 4 is `high`.
- With impact **3**, likelihood 1 or 2 is `medium`; likelihood 3 is `high`; likelihood 4 is `critical`.
- With impact **4**, likelihood 1 or 2 is `high`; likelihood 3 or 4 is `critical`.

For example, impact 3 and likelihood 2 is `medium`. The highest material scenario sets the maximum inherent and residual tiers; never average scenarios or dimensions into a lower result. Rate the confidence of each estimate as `low`, `medium`, or `high`. Confidence describes evidence strength, not risk. A low-confidence estimate with plausibly severe consequences needs investigation, a constraint, or a conservative classification. Record assumptions, missing evidence, disputed scores, and what would change the assessment.

### Credit controls only when evidence supports them

- A **preventive** control lowers the chance of a scenario: deterministic authorization, an allowlist, isolation, bounded approval.
- A **detective** control shortens time to discovery: reconciliation, anomaly detection, policy telemetry, audit review.
- A **recovery** control limits duration or consequence: compensation, rollback, safe cancellation, notification, a tested stop mechanism.

Every credited control has an owner and evidence of its design and operation, such as configuration or code review, deterministic tests, evaluation results, replay and failure scenarios, red-team results, audit samples, operational metrics, exercises, or independent review. A planned control or untested policy earns no residual-risk reduction. The [example assessment template](../../templates/10.1/risk-assessment-example.yaml) shows a versioned record with example values.

### Set the governance floor before judging residual risk

The governance tier is the highest of the maximum inherent scenario tier, any legal, regulatory, contractual, or internal-policy floor, and any organizational capability floor. At minimum:

- A prohibited use is `no_go`.
- Material, potentially irreversible human or safety impact is at least `high` and may be `critical`.
- A formally classified high-risk regulated use is at least `high`.
- An agent that can take consequential external actions requires `human_governed` execution and is at least `high`, unless a stricter organizational standard applies.
- Privileged code execution, broad cross-tenant access, or control of critical systems is at least `high`.
- Incomplete scope, missing ownership, or materially insufficient evidence rules out `low`.

Verified controls can make a specific release acceptable. They do not erase these floors. The agent contract and the assessment must agree on execution class and governance tier.

### Make the residual-risk decision accountable

Give every scenario one treatment: `avoid`, `mitigate`, `transfer`, or `accept`. An acceptance record names the accountable role, rationale, conditions, expiry, and next review date.

- `critical` residual: `no_go`.
- `high` residual: independent review, explicit acceptance by the designated risk authority, continuous monitoring, and a tested stop or containment mechanism.
- `medium` residual: a named owner, monitoring, and a time-bounded review.
- `low` residual: track it when it can compound with other risks or confidence is low.

A `conditional_go` names every condition, owner, deadline, monitoring signal, and consequence of missing the deadline. A condition that supplies required pre-release evidence still blocks launch. Local policy or applicable obligations may be stricter.

## Requirements

- **RISK-01 (MUST; applies when this detailed assessment is triggered).** The accountable owner MUST maintain a versioned assessment that states intended and prohibited use, scope, affected parties, accountable roles, effective capabilities and dependencies, material scenarios, inherent and residual scores with confidence and rationale, controls and evidence, treatments, decision, and review date. Authorized humans, not an agent or model, MUST accept residual risk and make the launch decision.

- **RISK-02 (MUST; applies before scoring any triggered assessment).** The assessment owner MUST record the prohibited-use and regulatory screen, including applicable jurisdictions, sectors, contractual or internal-policy duties, unresolved applicability, and named reviewers. A prohibited use MUST be `no_go`; a binding classification or organizational capability floor MUST set the relevant minimum tier and controls; and the assessment MUST NOT represent a matrix score as legal compliance or a formal classification.

- **RISK-03 (MUST; applies to every material scenario in a triggered assessment).** The assessment MUST use a stable scenario ID and the cause–unsafe behavior–harm–affected-party form; consider all eight dimensions; record inherent and residual impact, likelihood, tier, confidence, and rationale; and apply the four-by-four matrix in this chapter. The owner MUST NOT average scenarios or dimensions into a lower tier, or credit a proposed, untested, or unsupported control with residual-risk reduction.

- **RISK-04 (MUST; applies when deriving a governance tier or changing capabilities).** The governance tier MUST be the highest applicable inherent scenario tier, legal or policy floor, and organizational capability floor. The assessment MUST preserve the mandatory floors in this chapter, keep execution class, governance tier, and residual risk distinct, and agree with the agent contract's declared execution class and governance tier.

- **RISK-05 (MUST; applies to a release or continued operation with a material scenario).** Each material scenario MUST have a treatment, named owner, linked pre-release and production evidence, and a decision record. Release MUST fail when a required hard gate fails, required tier evidence is missing, the use is prohibited, or residual risk is `critical`. High residual risk additionally requires independent review, explicit risk-authority acceptance, continuous monitoring, and a tested stop or containment mechanism.

- **RISK-06 (MUST/SHOULD; applies throughout the assessment lifecycle).** The owner MUST reassess after a new or changed model, provider, tool, skill, MCP server, data source, or permission; increased autonomy, transaction value, user population, or jurisdiction; a material prompt, policy, workflow, retry, approval, or deployment change; a failed hard gate, incident, near miss, complaint, or regulatory change; or evidence that a control is ineffective or monitoring is incomplete. Maximum review intervals are 12 months for `low`, 6 months for `medium`, 3 months for `high`, and 1 month for `critical`, unless a stricter obligation applies. Implementations SHOULD machine-validate structural and semantic consistency of the assessment and SHOULD block release when that validation fails.

## Worked example

The shared fictional internal policy assistant answers questions from approved, current, permission-filtered documents. It returns citations and uncertainty, has no external write capability, and reports `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. Its execution class may be `ephemeral`, which does not decide its governance tier. All values below are fictional.

The owner first records the prohibited-use and regulatory screen: the relevant jurisdictions, the internal policy owner, the reviewers to consult, and the rule that the assistant must not present a document as current when the source policy cannot support that claim. Being read-only does not excuse the screen.

One material scenario is `RISK-CONTEXT-001`:

> Because a superseded travel-policy document remains eligible for retrieval, the assistant could cite it as current and state an incorrect London hotel allowance, causing an employee to make an unsupported expense decision and creating financial, operational, and trust harm for the employee and organization.

The primary dimension is financial, with operational and reputational as secondary. The assessment checks the other dimensions and records why they are not primary. Inherent impact is 2: a meaningful but contained, normally recoverable expense error. Inherent likelihood is 3, because stale material is plausible if current-status filtering fails. The matrix gives inherent `medium`.

The preventive control filters for approved, current documents before retrieval and keeps the permission boundary independent of model output. Its evidence is a versioned evaluation case using the fictional `travel-policy-current` fixture, which permits a London hotel amount of **GBP 220** while a superseded document differs. The case checks that the response uses and cites the current source, and expresses uncertainty or escalates when authoritative support is absent. A citation-presence check alone would not show that the cited source supports the amount. A detective control records source identity and current-status failures for review. Its indicator, alert, owner, and response runbook are part of the production evidence.

If the evaluation and operating-control evidence checks out, residual impact stays 2 and likelihood drops to 1, giving residual `low`. The maximum inherent tier is still `medium`, so the governance tier is `medium`. A required pre-release test that has not passed earns no credit and blocks launch. Once the evidence is complete, the decision authority could issue `go`. A bounded `conditional_go` could instead allow a noncritical, post-release review of the source-status indicator, with a named owner, a deadline, a monitoring signal, and the consequence that rollout expansion stops and reassessment begins if the review is overdue. It cannot stand in for the current-source test.

## Evidence and checklist

Tie each claim to an artifact. Tag evaluation cases, trace attributes, risk-register entries, and incident records with the scenario ID. Keep this evidence:

- **Authorization or approval:** deterministic denial, tamper, scope, and argument-binding tests.
- **Model behavior:** versioned cases, fit-for-purpose evaluators, repeated-run evidence when needed, and failure distributions.
- **Tools and workflows:** argument, ordering, retry, replay, duplication, timeout, and recovery evidence.
- **Security and privacy:** threat cases, isolation tests, redaction checks, and review.
- **Human or domain impact:** affected-party analysis, domain rubric, escalation behavior, and expert review.
- **Operational controls:** an indicator, alert, runbook, owner, exercise, and recovery evidence.

Machine validation can check score-to-tier agreement, maximum-tier summaries, floors, `no_go` outcomes for prohibited use and critical residual scenarios, unique IDs, date ordering, resolvable evidence links, and agreement with the agent contract. It cannot tell whether a control is effective, a scenario is complete, or a legal classification applies. Those stay review decisions.

Before accepting the assessment, confirm:

- [ ] The scope, prohibited-use and regulatory screen, named reviewers, and accountable owner are recorded.
- [ ] All eight dimensions were considered; every material scenario has inherent and residual scoring, confidence, rationale, treatment, and linked evidence.
- [ ] Each credited control has an owner and verified evidence; planned work has not reduced residual risk.
- [ ] The governance tier reflects the highest inherent scenario and every applicable floor, and matches the agent contract.
- [ ] The release decision, non-waivable gates, any permitted conditions, monitoring, expiry, and reassessment date are explicit.

Next: [10.2 Bias, Human Impact, and Domain Assurance](02-bias-human-impact-and-domain-assurance.md) and [10.3 Advanced Privacy, Isolation, and Auditability](03-advanced-privacy-isolation-and-auditability.md).

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework AI RMF 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)"
[3]: https://www.iso.org/standard/81230.html "ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system"
[4]: https://www.iso.org/standard/77304.html "ISO/IEC 23894:2023 Information technology — Artificial intelligence — Guidance on risk management"
[5]: https://eur-lex.europa.eu/eli/reg/2016/679/oj "Regulation (EU) 2016/679 (GDPR), Article 35"
[6]: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "European Commission: AI Act"

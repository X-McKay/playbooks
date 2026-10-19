# 10.1 Detailed Risk Assessment and Governance

**Status:** 0.5.0 first draft
**Audience:** Accountable owners, builders, evaluators, security and privacy reviewers, and release decision authorities
**Applicability:** Use this expanded method when the [initial risk, data, ownership, and delivery record](../../development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) identifies elevated assurance needs, including consequential authority, sensitive or regulated context, broad reach, material uncertainty, or a material harm scenario. It is also available whenever a team needs a more defensible assessment. It does not replace legal, regulatory, security, privacy, safety, or domain-specific review.

[Part 10](README.md) · [Applicability](../../applicability.md) · [Release decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

An assessment makes the reasoning behind an agent's governance review inspectable. It is not a label applied to an agent in the abstract. The accountable owner describes the context, identifies concrete ways the agent could cause harm, records what evidence actually supports controls, and gives the authorized decision authority a basis for a release decision.

This chapter extends the early screen in Chapter 1.4. Start the assessment before design choices become expensive, update it before release, and keep it current in operation. A team may use a compact record for a bounded low-exposure use, but it needs this detailed method when a scenario, capability, legal screen, or policy floor triggers it. The assessment is a proposed playbook artifact, not a determination of legal compliance.

## Working model

### Keep the decisions separate

Five terms answer different questions:

- **Execution class** describes how work executes: `ephemeral`, `durable`, or `human_governed`.
- **Governance tier** describes the required assurance and oversight: `low`, `medium`, `high`, or `critical`.
- **Inherent risk** is the risk before risk-reducing controls.
- **Residual risk** is the risk after only those controls whose effectiveness has evidence.
- **Launch decision** is `go`, `conditional_go`, or `no_go` for an identified release.

Do not collapse these terms. A read-only agent can be high risk because a wrong answer has serious consequences. A durable agent can be medium risk. The governance tier is anchored to inherent risk and mandatory floors; a lower residual rating may make a release acceptable, but does not silently lower the assurance appropriate to the underlying use.

### Run the assessment in order

Describe the intended and prohibited uses, users, affected parties, jurisdictions, environment, and accountable roles. Inventory the effective model policy, instructions, skills, tools, integrations, data sources, memory, workflows, providers, approval paths, and downstream consumers. Record the identity or version of those dependencies so later evidence can be tied to what was assessed.

Run the prohibited-use and regulatory screen before assigning matrix scores. Next, write material harm scenarios, score each scenario inherently, identify controls and their evidence, score the residual risk, derive the governance tier, select a treatment, and record the decision and review obligation. The builder may draft this record, but an agent or model must not accept its own risk or authorize launch.

Assess amplifiers as evidence about a scenario's likelihood or impact, rather than as extra score dimensions. They include autonomy and ability to initiate actions; tool effect, transaction authority, identity, and privilege; data sensitivity, provenance, retention, and data subjects; affected population, vulnerable groups, and public reach; frequency, transaction value, and blast radius; reversibility, compensation, detection, and time to intervention; exposure to untrusted or adversarial content; human review quality and ability to stop execution; and model uncertainty, dependency concentration, and supply-chain exposure.

## Decisions and best practices

### Screen for prohibited and controlled uses first

Record applicable jurisdictions, sectors, contractual duties, internal policies, and the legal, compliance, or domain reviewers asked to decide applicability. A prohibited use is `no_go` whatever its matrix score. A binding classification sets a floor and required controls independently of the matrix. Health, employment, education, credit, insurance, housing, legal services, biometrics, critical infrastructure, children, and similarly consequential decisions require a documented applicability review and must not default to low risk. Unknown applicability is an unresolved risk, not evidence that no obligation applies.

The matrix helps compare scenario reasoning. It neither establishes a legal classification nor proves legal compliance. Escalate that question to the named reviewer instead of trying to infer it from a score.

### Write scenarios that a reviewer can test

Use this sentence form for each material scenario:

> Because **[cause or initiating condition]**, the agent could **[unsafe action, output, or omission]**, causing **[harm]** to **[affected party or asset]**.

Consider normal use, foreseeable misuse, adversarial content, dependency failure, model error, authorization failure, retry or concurrency behavior, operator error, and control failure. Each scenario needs a stable ID, owner, status, affected parties and assets, causes and preconditions, consequences, a primary dimension, any secondary dimensions, scoring rationale and confidence, controls with evidence, treatment, and links to evaluation cases, indicators, alerts, and runbooks.

Consider every dimension even when it is not the scenario's primary one: financial, operational, reputational, legal, security, privacy, regulatory, and human impact and safety. Calibrate financial amounts, outage duration, affected populations, data categories, and comparable anchors to the adopting organization's risk appetite. This playbook supplies a shared method, not universal materiality thresholds.

### Score inherent and residual risk without false precision

Score credible worst-case impact within the documented scope, not an average outcome. Use impact 1 for localized, short-lived, readily reversible, negligible external harm; 2 for meaningful but contained harm recoverable through normal procedures; 3 for material financial, operational, legal, security, privacy, reputational, regulatory, or human harm; and 4 for severe, widespread, systemic, life-safety, organization-threatening, or substantially irreversible harm. A control lowers impact only if it genuinely limits blast radius, duration, affected population, or reversibility.

For likelihood, use 1 when multiple unusual conditions are required and evidence supports rarity; 2 when the event is credible but not expected in normal operation; 3 when it is plausible in normal or adversarial operation or has been observed; and 4 when it is expected, repeated, or already occurring without intervention. Inherent likelihood assumes risk-reducing controls are absent. Residual likelihood includes only implemented controls with evidence. Draw on evaluations, tests, incidents, comparable systems, threat intelligence, domain review, and production measurements when they are available.

Apply the same matrix for both scores:

- With impact **1**, likelihood 1 or 2 is `low`; likelihood 3 or 4 is `medium`.
- With impact **2**, likelihood 1 is `low`; likelihood 2 or 3 is `medium`; likelihood 4 is `high`.
- With impact **3**, likelihood 1 or 2 is `medium`; likelihood 3 is `high`; likelihood 4 is `critical`.
- With impact **4**, likelihood 1 or 2 is `high`; likelihood 3 or 4 is `critical`.

For example, impact 3 and likelihood 2 is `medium`. The highest material scenario determines the maximum inherent and residual tiers. Do not average scenarios or dimensions into a lower result. Rate the confidence of each inherent and residual estimate as `low`, `medium`, or `high`; confidence describes evidence strength, not risk level. A low-confidence estimate with plausibly severe consequences needs investigation, a constraint, or a conservative classification. Record assumptions, missing evidence, disputed scores, and what would change the assessment.

### Credit controls only when evidence supports them

A preventive control reduces the chance of a scenario, such as deterministic authorization, an allowlist, isolation, or bounded approval. A detective control shortens time to discovery, such as reconciliation, anomaly detection, policy telemetry, or audit review. A recovery control limits duration or consequence, such as compensation, rollback, safe cancellation, notification, or a tested stop mechanism.

Every credited control has an owner and evidence of its design and operation. Useful evidence can include configuration or code review, deterministic tests, evaluation results, replay and failure scenarios, red-team results, audit samples, operational metrics, exercises, and independent review. A planned control or an untested policy receives no residual-risk reduction. An [example assessment template](../../templates/10.1/risk-assessment-example.yaml) illustrates a versioned record; its values are examples, not live findings.

### Set the governance floor before judging residual risk

The governance tier is the highest of the maximum inherent scenario tier, any legal, regulatory, contractual, or internal-policy floor, and any organizational capability floor. At a minimum:

- A prohibited use is `no_go`.
- Material, potentially irreversible human or safety impact is at least `high` and may be `critical`.
- A formally classified high-risk regulated use is at least `high`.
- An agent that can execute consequential external actions requires `human_governed` execution and is at least `high`, unless a documented organizational standard is stricter.
- Privileged code execution, broad cross-tenant access, or control of critical systems is at least `high`.
- Incomplete scope, missing ownership, or materially insufficient evidence prevents a `low` classification.

Verified controls may change whether a specific release is acceptable. They do not erase these floors or reclassify the inherent nature of the use. The agent contract and assessment should agree about execution class and governance tier.

### Make the residual-risk decision accountable

Assign every scenario one treatment: `avoid`, `mitigate`, `transfer`, or `accept`. An acceptance record names the accountable role, rationale, conditions, expiry, and next review date. A `critical` residual scenario is `no_go`. A `high` residual scenario needs independent review, explicit acceptance by the designated risk authority, continuous monitoring, and a tested stop or containment mechanism. A `medium` residual scenario needs a named owner, monitoring, and a time-bounded review. Track a low residual scenario when it can compound with other risks or confidence is low.

A `conditional_go` names every condition, owner, deadline, monitoring signal, and consequence of non-completion. A condition that supplies required pre-release evidence still blocks launch; it is not a permission to ship first. Local policy or applicable obligations may be stricter.

## Requirements

- **RISK-01 (MUST; applies when this detailed assessment is triggered).** The accountable owner MUST maintain a versioned assessment that states intended and prohibited use, scope, affected parties, accountable roles, effective capabilities and dependencies, material scenarios, inherent and residual scores with confidence and rationale, controls and evidence, treatments, decision, and review date. Authorized humans, not an agent or model, MUST accept residual risk and make the launch decision.

- **RISK-02 (MUST; applies before scoring any triggered assessment).** The assessment owner MUST record the prohibited-use and regulatory screen, including applicable jurisdictions, sectors, contractual or internal-policy duties, unresolved applicability, and named reviewers. A prohibited use MUST be `no_go`; a binding classification or organizational capability floor MUST set the relevant minimum tier and controls; and the assessment MUST NOT represent a matrix score as legal compliance or a formal classification.

- **RISK-03 (MUST; applies to every material scenario in a triggered assessment).** The assessment MUST use a stable scenario ID and the cause–unsafe behavior–harm–affected-party form; consider all eight dimensions; record inherent and residual impact, likelihood, tier, confidence, and rationale; and apply the four-by-four matrix in this chapter. The owner MUST NOT average scenarios or dimensions into a lower tier, or credit a proposed, untested, or unsupported control with residual-risk reduction.

- **RISK-04 (MUST; applies when deriving a governance tier or changing capabilities).** The governance tier MUST be the highest applicable inherent scenario tier, legal or policy floor, and organizational capability floor. The assessment MUST preserve the mandatory floors in this chapter, keep execution class, governance tier, and residual risk distinct, and agree with the agent contract's declared execution class and governance tier.

- **RISK-05 (MUST; applies to a release or continued operation with a material scenario).** Each material scenario MUST have a treatment, named owner, linked pre-release and production evidence, and a decision record. Release MUST fail when a required hard gate fails, required tier evidence is missing, the use is prohibited, or residual risk is `critical`. High residual risk additionally requires independent review, explicit risk-authority acceptance, continuous monitoring, and a tested stop or containment mechanism.

- **RISK-06 (MUST/SHOULD; applies throughout the assessment lifecycle).** The owner MUST reassess after a new or changed model, provider, tool, skill, MCP server, data source, or permission; increased autonomy, transaction value, user population, or jurisdiction; a material prompt, policy, workflow, retry, approval, or deployment change; a failed hard gate, incident, near miss, complaint, or regulatory change; or evidence that a control is ineffective or monitoring is incomplete. Maximum review intervals are 12 months for `low`, 6 months for `medium`, 3 months for `high`, and 1 month for `critical`, unless a stricter obligation applies. Implementations SHOULD machine-validate structural and semantic consistency of the assessment and SHOULD block release when that validation fails.

## Worked example

The shared fictional internal policy assistant answers questions from approved, current, permission-filtered documents. It returns citations and uncertainty, has no external write capability, and reports `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. Its execution class may be `ephemeral`; that does not determine its governance tier.

The owner first records a prohibited-use and regulatory screen. The example is not a legal determination: it identifies the relevant jurisdictions, internal policy owner, and reviewers to consult, and it records that the assistant must not present a document as current when the source policy cannot support that claim. The review must not be skipped merely because the assistant only reads documents.

One material scenario is `RISK-CONTEXT-001`:

> Because a superseded travel-policy document remains eligible for retrieval, the assistant could cite it as current and state an incorrect London hotel allowance, causing an employee to make an unsupported expense decision and creating financial, operational, and trust harm for the employee and organization.

The scenario's primary dimension is financial, with operational and reputational secondary dimensions. The assessment considers the other dimensions and records why they are not primary in this scenario. Inherent impact is 2: the illustration assumes a meaningful but contained and normally recoverable expense error. Inherent likelihood is 3 because stale material is plausible if current-status filtering fails. The matrix therefore gives inherent `medium` risk. This is an illustrative assessment, not a measured incident rate.

The preventive control filters for approved, current documents before retrieval and keeps the permission boundary independent of model output. Its evidence includes a versioned evaluation case using the fictional `travel-policy-current` fixture: it permits a London hotel amount of **GBP 220**, while a superseded document differs. The case checks that the response uses the current source, cites it, and expresses uncertainty or escalates when authoritative support is absent. A citation-presence check alone would not establish that the cited source supports the amount. A detective control records source identity and current-status failures for review; its linked indicator, alert, owner, and response runbook are part of the production evidence.

If the evaluation and operating-control evidence is verified, the residual impact remains 2 but likelihood becomes 1, producing residual `low` risk. The maximum inherent tier remains `medium`, so the governance tier is `medium` even though residual risk is lower. A required pre-release test that has not passed receives no risk-reduction credit and blocks launch. The authorized decision authority could issue `go` once that evidence is complete. A bounded `conditional_go` could instead allow only a noncritical, post-release review of the source-status indicator, with a named owner, a deadline, a monitoring signal, and the consequence that rollout expansion stops and reassessment begins if the review is overdue. It cannot substitute for the current-source test.

## Evidence and checklist

A reviewable assessment ties each claim to an artifact, not merely to a narrative. Tag evaluation cases, trace attributes, risk-register entries, and incident records with the scenario ID. For authorization or approval claims, retain deterministic denial, tamper, scope, and argument-binding tests. For model behavior, retain versioned cases, fit-for-purpose evaluators, repeated-run evidence when needed, and failure distributions. For tools and workflows, retain argument, ordering, retry, replay, duplication, timeout, and recovery evidence. For security and privacy, retain threat cases, isolation tests, redaction checks, and relevant review. For human or domain impact, retain affected-party analysis, domain rubric, escalation behavior, and expert review. Operational controls need an indicator, alert, runbook, owner, exercise, and recovery evidence.

Machine validation can check score-to-tier agreement, maximum-tier summaries, floors, `no_go` outcomes for prohibited use and critical residual scenarios, unique IDs, sensible date ordering, resolvable evidence links, and agreement with the referenced agent contract. Structural validation cannot decide whether a control is effective, whether a scenario is complete, or whether a legal classification applies; those remain review decisions.

Before accepting the assessment, confirm:

- [ ] The scope, prohibited-use and regulatory screen, named reviewers, and accountable owner are recorded.
- [ ] All eight dimensions were considered; every material scenario has inherent and residual scoring, confidence, rationale, treatment, and linked evidence.
- [ ] Each credited control has an owner and verified evidence; planned work has not reduced residual risk.
- [ ] The governance tier reflects the highest inherent scenario and every applicable floor, and matches the agent contract.
- [ ] The release decision, non-waivable gates, any permitted conditions, monitoring, expiry, and reassessment date are explicit.

For related assurance methods, continue to [10.2 Bias, Human Impact, and Domain Assurance](02-bias-human-impact-and-domain-assurance.md) and [10.3 Advanced Privacy, Isolation, and Auditability](03-advanced-privacy-isolation-and-auditability.md).

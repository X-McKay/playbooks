# 10.1 Detailed Risk Assessment and Governance

**Status:** 0.5.0-draft.2 — draft
**Audience:** Accountable owners, builders, evaluators, security and privacy reviewers, and release decision authorities
**Applicability:** Use this method when the [initial risk, data, ownership, and delivery record](../../development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md) shows elevated assurance needs: consequential authority, sensitive or regulated context, broad reach, material uncertainty, or a material harm scenario. It does not replace legal, security, privacy, safety, or domain review.

[Part 10](README.md) · [Applicability](../../applicability.md) · [Release decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

This method extends the Chapter 1.4 screen: it names concrete harms, records each control's evidence, and gives the decision authority a basis for release. Start before design is expensive, update before release, and keep it current; a bounded, low-exposure use keeps a compact record until a trigger applies.

## Working model

### Keep the decisions separate

Five separate questions:

- **Execution class:** how work executes (`ephemeral`, `durable`, `human_governed`).
- **Governance tier:** required assurance and oversight (`low`, `medium`, `high`, `critical`).
- **Inherent risk:** risk before risk-reducing controls.
- **Residual risk:** risk after only controls with evidence of working.
- **Launch decision:** `go`, `conditional_go`, or `no_go` for one release.

A read-only agent can be high risk and a durable one medium. The tier is anchored to inherent risk and mandatory floors; a lower residual rating can make a release acceptable but does not lower the assurance the use needs.

### Run the assessment in order

1. Describe intended and prohibited uses, users, affected parties, jurisdictions, environment, and accountable roles.
2. Inventory, with versions, the effective model policy, instructions, skills, tools, integrations, data sources, memory, workflows, providers, approval paths, and consumers.
3. Run the prohibited-use and regulatory screen before scoring.
4. Write and score scenarios, credit evidenced controls, derive the tier, choose treatments, and record the decision and review date.

The builder may draft it; no agent or model accepts its own risk or authorizes launch.

Amplifiers are evidence about likelihood or impact, not extra dimensions: autonomy; tool effect, authority, identity, and privilege; data sensitivity, provenance, retention, and subjects; population, vulnerable groups, and reach; frequency, value, and blast radius; reversibility, compensation, detection, and time to intervene; adversarial content; review quality and ability to stop; model uncertainty and supply-chain concentration.

## Decisions and best practices

### Screen for prohibited and controlled uses first

Health, employment, education, credit, insurance, housing, legal services, biometrics, critical infrastructure, children, and similar consequential decisions need a documented applicability review and never default to low risk. Unknown applicability is an unresolved risk. Legal classification goes to the named legal, compliance, or domain reviewer, not the matrix.

### Frameworks you may need to map to

Pointers, not legal advice:

- **NIST AI RMF and Generative AI Profile.** Voluntary; NIST AI 600-1 (July 2024) adds generative-AI actions for govern, map, measure, and manage.[1], [2]
- **ISO/IEC 42001 and 23894.** 42001:2023 specifies an assessable AI management system; 23894:2023 guides AI risk management.[3], [4]
- **GDPR Article 35.** A data protection impact assessment is required before processing likely to pose a high risk to people's rights and freedoms; it describes processing and purposes, assesses necessity, proportionality, and risks, and lists safeguards. Triggers include automated evaluation with significant effects and large-scale use of sensitive data; see [10.3](03-advanced-privacy-isolation-and-auditability.md).[5]
- **EU AI Act.** Some practices are prohibited; listed high-risk uses carry strict obligations (such as risk management, logging, documentation, and human oversight); some systems have transparency duties; most have none; general-purpose AI models have their own. The phased schedule has been amended, so check current dates.[6]

These frameworks can consume this method's records but do not replace it.

### Write scenarios a reviewer can test

Use this form for each material scenario:

> Because **[cause or initiating condition]**, the agent could **[unsafe action, output, or omission]**, causing **[harm]** to **[affected party or asset]**.

Cover normal use, misuse, adversarial content, dependency failure, model error, authorization failure, retry or concurrency, operator error, and control failure. Beyond the RISK-03 fields, record owner, status, assets, preconditions, consequences, primary and secondary dimensions, and linked evaluation cases, indicators, alerts, and runbooks.

The eight dimensions are financial, operational, reputational, legal, security, privacy, regulatory, and human impact and safety. Calibrate amounts, outage duration, populations, and data categories to your risk appetite.

### Score inherent and residual risk without false precision

Score the credible worst case in scope, not the average.

- **Impact:** 1 localized, short-lived, easily reversible, negligible external harm; 2 meaningful but contained, recoverable through normal procedures; 3 material harm in any dimension; 4 severe, widespread, systemic, life-safety, organization-threatening, or largely irreversible.
- **Likelihood:** 1 needs several unusual conditions, with evidence of rarity; 2 credible but not expected in normal operation; 3 plausible in normal or adversarial operation, or already observed; 4 expected, repeated, or already occurring without intervention.

A control lowers impact only if it limits blast radius, duration, population, or reversibility. Base likelihood on evaluations, tests, incidents, comparable systems, threat intelligence, domain review, and production data. One matrix serves both scores:

| Impact \ Likelihood | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 1 | `low` | `low` | `medium` | `medium` |
| 2 | `low` | `medium` | `medium` | `high` |
| 3 | `medium` | `medium` | `high` | `critical` |
| 4 | `high` | `high` | `critical` | `critical` |

The highest material scenario sets the maximum tiers. Rate confidence (`low`, `medium`, `high`) as evidence strength; low confidence with plausibly severe consequences needs investigation, a constraint, or a conservative classification. Record assumptions, missing evidence, disputed scores, and what would change the assessment.

### Credit controls only when evidence supports them

- A **preventive** control lowers the chance of a scenario: deterministic authorization, an allowlist, isolation, bounded approval.
- A **detective** control shortens time to discovery: reconciliation, anomaly detection, policy telemetry, audit review.
- A **recovery** control limits duration or consequence: compensation, rollback, safe cancellation, notification, a tested stop mechanism.

A credited control has an owner and evidence of design and operation, such as review, deterministic tests, evaluations, replay and failure scenarios, red-teaming, audit samples, metrics, exercises, or independent review ([example template](../../templates/10.1/risk-assessment-example.yaml)).

### Set the governance floor before judging residual risk

The tier is set by RISK-04. Mandatory floors:

- A prohibited use is `no_go`.
- Material, potentially irreversible human or safety impact is at least `high` and may be `critical`.
- A formally classified high-risk regulated use is at least `high`.
- An agent that can take consequential external actions requires `human_governed` execution and is at least `high`, unless a stricter organizational standard applies.
- Privileged code execution, broad cross-tenant access, or control of critical systems is at least `high`.
- Incomplete scope, missing ownership, or materially insufficient evidence rules out `low`.

Verified controls never erase these floors.

### Make the residual-risk decision accountable

Treat every scenario: `avoid`, `mitigate`, `transfer`, or `accept`. An acceptance names the accountable role, rationale, conditions, expiry, and next review date. Residual `critical` is `no_go`; `high` needs the RISK-05 safeguards; `medium` needs a named owner, monitoring, and a time-bounded review; track `low` when it can compound with other risks or confidence is low.

A `conditional_go` names each condition's owner, deadline, monitoring signal, and consequence if missed ([5.2](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md)); a condition supplying required pre-release evidence still blocks launch.

## Requirements

- **RISK-01 (MUST; applies when this detailed assessment is triggered).** The accountable owner MUST maintain a versioned assessment that states intended and prohibited use, scope, affected parties, accountable roles, effective capabilities and dependencies, material scenarios, inherent and residual scores with confidence and rationale, controls and evidence, treatments, decision, and review date. Authorized humans, not an agent or model, MUST accept residual risk and make the launch decision.

- **RISK-02 (MUST; applies before scoring any triggered assessment).** The assessment owner MUST record the prohibited-use and regulatory screen, including applicable jurisdictions, sectors, contractual or internal-policy duties, unresolved applicability, and named reviewers. A prohibited use MUST be `no_go`; a binding classification or organizational capability floor MUST set the relevant minimum tier and controls; and the assessment MUST NOT represent a matrix score as legal compliance or a formal classification.

- **RISK-03 (MUST; applies to every material scenario in a triggered assessment).** The assessment MUST use a stable scenario ID and the cause–unsafe behavior–harm–affected-party form; consider all eight dimensions; record inherent and residual impact, likelihood, tier, confidence, and rationale; and apply the four-by-four matrix in this chapter. The owner MUST NOT average scenarios or dimensions into a lower tier, or credit a proposed, untested, or unsupported control with residual-risk reduction.

- **RISK-04 (MUST; applies when deriving a governance tier or changing capabilities).** The governance tier MUST be the highest applicable inherent scenario tier, legal or policy floor, and organizational capability floor. The assessment MUST preserve the mandatory floors in this chapter, keep execution class, governance tier, and residual risk distinct, and agree with the agent contract's declared execution class and governance tier.

- **RISK-05 (MUST; applies to a release or continued operation with a material scenario).** Each material scenario MUST have a treatment, named owner, linked pre-release and production evidence, and a decision record. Release MUST fail when a required hard gate fails, required tier evidence is missing, the use is prohibited, or residual risk is `critical`. High residual risk additionally requires independent review, explicit risk-authority acceptance, continuous monitoring, and a tested stop or containment mechanism.

- **RISK-06 (MUST/SHOULD; applies throughout the assessment lifecycle).** The owner MUST reassess after a new or changed model, provider, tool, skill, MCP server, data source, or permission; increased autonomy, transaction value, user population, or jurisdiction; a material prompt, policy, workflow, retry, approval, or deployment change; a failed hard gate, incident, near miss, complaint, or regulatory change; or evidence that a control is ineffective or monitoring is incomplete. Maximum review intervals are 12 months for `low`, 6 months for `medium`, 3 months for `high`, and 1 month for `critical`, unless a stricter obligation applies. Implementations SHOULD machine-validate structural and semantic consistency of the assessment and SHOULD block release when that validation fails.

## Worked example

The shared fictional policy assistant answers from approved, current, permission-filtered documents with citations, and cannot write externally; its `ephemeral` class does not decide its tier. The owner still records the screen (jurisdictions, policy owner, reviewers) and the rule that no document is presented as current without source support. One material scenario is `RISK-CONTEXT-001`:

> Because a superseded travel-policy document remains eligible for retrieval, the assistant could cite it as current and state an incorrect London hotel allowance, causing an employee to make an unsupported expense decision and creating financial, operational, and trust harm for the employee and organization.

Primary dimension: financial; secondary: operational, reputational. Impact 2 (contained, recoverable) and likelihood 3 (plausible if status filtering fails) give inherent `medium`.

The preventive control filters for approved, current documents before retrieval, independent of model output. Evidence: a versioned case on the `travel-policy-current` fixture (London hotel **GBP 220**; a superseded document differs) checking that the response cites the current source, or expresses uncertainty or escalates; citation presence alone shows no support. A detective control logs current-status failures, with indicator, alert, owner, and runbook.

With that evidence, residual likelihood is 1 (residual `low`); the tier stays `medium`. An unpassed required test blocks launch. The authority could then issue `go`, or a `conditional_go` deferring only a noncritical indicator review, where lateness stops expansion and starts reassessment.

## Evidence and checklist

Tag cases, traces, register entries, and incidents with the scenario ID. Typical evidence:

- **Authorization:** deterministic denial, tamper, scope, and argument-binding tests.
- **Model behavior:** versioned cases, fit-for-purpose evaluators, repeated runs, failure distributions.
- **Tools and workflows:** argument, ordering, retry, replay, duplication, timeout, recovery.
- **Security and privacy:** threat cases, isolation and redaction tests, review.
- **Human or domain impact:** affected-party analysis, domain rubric, escalation behavior, expert review.
- **Operations:** indicator, alert, runbook, owner, exercises.

Machine validation checks score-to-tier agreement, maximum tiers, floors, `no_go` outcomes, unique IDs, dates, links, and contract agreement; control effectiveness, completeness, and legal classification stay review decisions.

Before accepting, confirm:

- [ ] All eight dimensions were considered per scenario.
- [ ] No planned work reduced residual risk.
- [ ] Gates, conditions, monitoring, expiry, and reassessment date are explicit.

Next: [10.2](02-bias-human-impact-and-domain-assurance.md) and [10.3](03-advanced-privacy-isolation-and-auditability.md).

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI RMF 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1 Generative AI Profile"
[3]: https://www.iso.org/standard/81230.html "ISO/IEC 42001:2023 AI management system"
[4]: https://www.iso.org/standard/77304.html "ISO/IEC 23894:2023 AI guidance on risk management"
[5]: https://eur-lex.europa.eu/eli/reg/2016/679/oj "Regulation (EU) 2016/679 (GDPR), Article 35"
[6]: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "European Commission: AI Act"

# 5.2 Readiness, Change, and Rollout

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted  
**Audience:** Builders, evaluators, operators, accountable release decision-makers, and reviewers  
**Applicability:** Every production release and material change. The review depth and evidence form scale with the agent's governance tier, enabled capabilities, exposure, and potential impact; read-only access does not automatically mean low risk.  
**Reader question:** How can we decide whether one identified candidate is ready for a defined exposure, make changes without losing the basis for that decision, and limit the consequences if rollout assumptions fail?

[Part 5 — Release, Operations, and Lifecycle](README.md) · [Applicability](../../applicability.md) · [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) · Next: [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)

## Purpose and applicability

**Readiness** is a decision about a particular candidate: an identified configuration may be exposed to a stated use, audience, and operating context. It is not a final checklist detached from development. The candidate, risk treatment, evaluation evidence, controls, authorization boundary, and rollout scope need to describe the same subject. A change to a model policy, instructions, permissions, tool policy, retrieval corpus, source filter, or population can alter behavior even when application code is unchanged.

This chapter supplies a proposed playbook method for joining those facts into a reviewable release record. It does not prescribe a deployment platform, a stage size, a time window, a staffing model, or an organization-wide approval role. NIST describes AI risk management as continuous and lifecycle-spanning, with context-sensitive use of its voluntary framework rather than a mandatory checklist.[1] The candidate record and the seven requirements here are therefore proposed playbook guidance, not a claim that NIST or any organization has adopted them.

A release record draws on evidence owned elsewhere. Use [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) to determine what evaluation evidence supports; use [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) for live signals and a stop mechanism; use [3.3 Data, Privacy Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) for data handling and audit evidence; and use [10.1 Detailed Risk Assessment and Governance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) for detailed risk methods. [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md) owns incident response and resumption. Where work is durable or consequential, the execution and in-flight compatibility owners in [7.1](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) and [7.3](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) also apply.

## Working model

A release decision has four connected parts.

1. **Subject** identifies the exact candidate: its resolved behavior-affecting configuration, effective capabilities and permissions, relevant source or corpus identities, dependencies, and proposed exposure scope. A mutable label such as “current” is not enough to reconstruct what was reviewed.
2. **Evidence** says which claims were tested, which controls have supporting evidence, what the evidence does not establish, and what remains missing or unresolved. A nearby-version report is not automatically evidence for a changed candidate.
3. **Authority** records who may accept residual risk and authorize the stated scope under applicable policy. It does not transfer that judgment to a model, an aggregate metric, or a checklist.
4. **Exposure and response** describes how the candidate could reach users, what may permit promotion or require a stop, and how containment handles work that cannot simply be reversed.

These parts have different meanings even when their records are adjacent. A contract **terminal outcome** says what an agent response means, such as `complete`, `needs_information`, `declined`, or `failed`. An operational **termination or exhaustion reason** says why work stopped, such as a controlled retrieval timeout. A telemetry signal can indicate service health; a supported user task requires the contract outcome and its applicable invariants. An evaluation conclusion can be `go`, `conditional_go`, or `no_go`, while release authorization uses separately namespaced fields even when it uses the same labels. An authoritative external effect requires evidence from the relevant external system. None of these facts is interchangeable, and none is created by a release record alone.

Track each readiness item as **met**, **not applicable with rationale**, **unmet and blocking**, or **eligible for an explicitly governed exception**. The categories prevent an unchecked line from becoming an implied pass. “Not applicable” records an absent trigger; it is not another name for missing evidence, an unimplemented control, or an inconvenient review. NIST's configuration-management guidance similarly treats a reviewed baseline and recorded change process as a way to maintain integrity, while allowing organizations to set risk-sensitive rigor.[2]

Keep the two decision layers explicit. An evaluation `go` means the evidence policy supports handing the candidate to readiness review; it is not deployment permission. A release `go` authorizes only the identified candidate and scope. A release `no_go` denies that authorization. A release `conditional_go`, where applicable policy permits it, has no incomplete required pre-release evidence or control: it identifies only permitted post-release obligations. The next section explains why this boundary matters.

## Decisions and best practices

### Bind evidence to the candidate

Make the decision subject inspectable before reviewing its results. A compact record can name the candidate version or equivalent immutable identity; resolved instructions and configuration; model, route, and fallback policy when present; effective tools, skills, and permissions; relevant source, corpus, and filtering identities; risk-assessment identity; evaluation evidence; and the proposed population and capability scope. A digest or immutable content identity can help distinguish a reviewed source set from a later mutable label. The point is traceability, not a particular registry or file format.

State what the authorization would cover: intended and prohibited use, eligible users or tenants, enabled capabilities, population boundary, and any stage-specific limits. Pilot feedback may clarify usability, but it does not replace evidence for an applicable safety, security, quality, privacy, or risk claim. A narrow trial record does not quietly extend to a wider user group or a different purpose.

A justified evidence-reuse decision is sometimes possible. Compare the proposed change with the assumptions, risk scenarios, controls, evaluation cases, and observation rules that supported the earlier result. If a component and its relevant behavior are unchanged, and the old evidence's scope still covers the new candidate, record that rationale and its limit. If a permission boundary, answer selection rule, source admission rule, user population, or operating assumption changes, the affected evidence needs re-evaluation rather than a nearby-version label. NIST's general change-control guidance calls for recorded requests, impact analysis, testing, approval, and verification before operational release; it does not classify every agent change for an organization.[2]

### Separate blockers from exceptions

Before interpreting averages or feedback, connect each applicable readiness item and material risk scenario to evidence and a disposition. A prohibited use, failed non-waivable hard gate, unresolved required authorization, or governance-tier-required missing evidence is a blocker. An attractive average cannot compensate for a critical-slice failure. A planned control has no pre-release risk-reduction credit until the evidence that makes it relevant is available.

An **exception** is a documented policy path for an otherwise applicable item, not a release-time invention. When such a path exists, the record identifies its eligible scope, rationale, compensating controls, accountable approver and owner, expiry or review point, and consequence if its conditions are not met. The record also shows why the exception cannot override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate. When the organization has not established eligibility, the unmet item stays blocking; the chapter does not create a general waiver catalogue.

`conditional_go` is deliberately narrow. Separate each required action into one of two lists: a **pre-release action** blocks launch until verified, while a permitted **post-release obligation** has an owner, due date, monitoring signal, and predeclared consequence for non-completion. Completing a required human review, obtaining a required evaluation result, or installing a control needed for the planned exposure belongs in the first list. A post-release obligation can track permitted follow-through; it cannot turn absent release evidence into a pass.

### Choose proportionate rollout stages

A rollout stage limits exposure while the release owner checks whether the candidate remains within the assumptions made at readiness. The appropriate sequence depends on consequence, uncertainty, scale, reversibility, and the strength of pre-release evidence. Staging complements rather than replaces pre-release evidence. The chapter provides no universal percentage, duration, observation interval, or promotion threshold.

Useful stage types include the following, but no one sequence is mandatory:

- An **isolated stage** keeps the candidate outside production exposure while the owner verifies the named candidate and its controls in a controlled boundary.
- A **shadow stage** processes authorized duplicate or representative inputs without allowing the candidate's result to control the user-facing answer. Shadow operation is not intrinsically private or side-effect-free: the copied input may be sensitive, and a candidate path may reach capabilities unless isolation and authorization are deliberately established.
- A **canary stage** exposes an explicitly limited, authorized production scope and makes promotion contingent on its declared evidence and signals.
- A **wider stage** increases exposure only within the release authorization's stated population, purpose, and capability boundary.

For each chosen stage, record who or what is included, enabled capabilities, expected signals, promotion criteria, stop criteria, the person or role authorized to decide, and the containment path. NIST's voluntary AI RMF Playbook likewise places post-deployment monitoring, feedback, change management, and response to unexpected behavior in the ongoing management context; it does not prescribe a standard rollout design.[3]

Name response actions precisely. **Rollback** changes future admission or routing back to an earlier candidate. **Disable** stops a candidate or capability from receiving new work. **Containment** narrows an affected source, capability, tenant path, or exposure. **Reconciliation** establishes what happened against an authoritative state when an active operation or external effect is uncertain. A **forward fix** is a newly reviewed candidate, not proof that the prior exposure was undone. Rollback alone cannot reverse active work, persisted state, approvals, or an external effect. The release plan therefore identifies safe stop and reconciliation where they are relevant, while Part 7 owns durable effect recovery and Part 5.3 owns incident response and resumption.

### Reassess changes that can alter behavior

Treat a change as material when it can alter output, action authority, information access, affected population, risk, or an assumption that made the release acceptable. Common examples include a model or provider change; altered instructions or policy; a change to a tool, permission, approval rule, route, fallback, data-handling path, retry rule, or execution class; source admission, corpus, retrieval, or filtering changes; and expansion to a new purpose, tenant, jurisdiction, or user group. A dependency update can be material when it changes a capability, boundary, failure mode, or operating assumption.

For each proposed change, trace the effect on the existing release subject. Record whether a scenario, control, evidence item, evaluation result, rollout constraint, or authorization scope is unaffected, needs targeted confirmation, or is invalidated. The evidence record then makes the reuse or refresh decision reviewable. A minor formatting correction with no behavior or source effect can have a different disposition from a permission-filtering change, but neither application-code status nor a small diff settles the question on its own.

### Recognize common failure modes

Several shortcuts create misleading readiness records.

- **The nearby green report:** A candidate gains a new source filter, but the record attaches an earlier evaluation report without explaining why its permission and source assumptions still hold. The report is evidence for its original subject, not an automatic pass for the altered candidate.
- **The silent waiver:** A required review is marked not applicable because it has not been scheduled. The trigger is still present, so the missing review is unresolved evidence rather than non-applicability.
- **The conditional promise:** A release calls a required isolation test a post-release task. This hides a pre-release blocker behind `conditional_go` and leaves the planned exposure without its needed evidence.
- **The shadow shortcut:** Duplicate production inputs reach a candidate that can invoke an enabled capability. Treating the stage as harmless merely because its answer is not displayed can create unauthorized processing or an effect outside the user interface.
- **The rollback story:** A version pointer moves back after uncertain active work. The pointer change may protect future work, but it cannot establish that an in-flight operation did not finish or that an external effect was reversed.
- **The collapsed label:** A fixture's expected `needs_information` outcome is described as a release `no_go`, or a telemetry success is reported as user-task success. Each label answers a different question and needs its own evidence.

### Build a release packet

A practical builder workflow is small enough to repeat for a first release or a material change.

1. **Freeze the subject.** Give the candidate, effective capabilities and permissions, relevant configuration and sources, risk assessment, intended use, and proposed exposure an inspectable identity.
2. **Collect the owner handoffs.** Link the evaluation conclusion and its limits, risk scenarios and control evidence, applicable security or privacy reviews, operations signals, and any execution-specific evidence. Preserve missing, invalid, and inconclusive evidence instead of summarizing it away.
3. **Make a readiness ledger.** Give every applicable item one of the four readiness states and attach candidate-specific evidence or a rationale. Keep exceptions, when policy permits them, distinct from blockers.
4. **Record decisions in their namespaces.** Let the evaluation record state what its evidence supports. Let the authorized release decision-maker separately record the release decision, scope, rationale, and residual-risk acceptance where required. Neither record speaks for an external system's effects.
5. **Plan exposure and response.** Select proportionate stages, promotion and stop evidence, authorities, and a usable containment or disable path. Where active work or effects exist, connect the plan to the applicable safe-stop and reconciliation owner.
6. **Reopen the packet on change.** Compare the change to the assumptions and evidence already credited, record the disposition, then refresh the affected risk and evaluation evidence before a material promotion.

The [illustrative release-and-rollout record](../../templates/5.2/release-and-rollout-record.yaml) shows fields that can make this workflow inspectable. It is a neutral companion example, not a requirement to use separate files, a named platform, or any particular authorization process.

## Requirements

- **ROLLOUT-01** — For every production release or material change, the accountable release owner MUST identify the exact candidate, effective capabilities and permissions, relevant configuration and data-source identity, risk-assessment version, evaluation evidence, and authorized exposure scope in a release record.
- **ROLLOUT-02** — Before authorizing exposure, the release owner MUST classify each applicable readiness item as met, not applicable with rationale, unmet and blocking, or eligible for an explicitly governed exception; each met item and each credited risk-reducing control MUST link to evidence for the candidate under review.
- **ROLLOUT-03** — The authorized decision-maker MUST record `go`, `conditional_go`, or `no_go` against predeclared release criteria. A prohibited use, failed non-waivable hard gate, or missing evidence required by the applicable governance tier MUST result in `no_go`; an average result MUST NOT override it.
- **ROLLOUT-04** — When an applicable policy permits an exception, the accountable approver MUST record its eligible scope, rationale, compensating controls, owner, expiry or review date, and consequence if its conditions are not met. An exception MUST NOT override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate.
- **ROLLOUT-05** — When `conditional_go` is used, the decision record MUST distinguish any pre-release action—which blocks launch until verified—from permitted post-release obligations, and MUST assign each post-release obligation an owner, due date, monitoring signal, and consequence for non-completion. Required evidence or controls MUST NOT be deferred as a post-release obligation.
- **ROLLOUT-06** — Before rollout, the release owner MUST define exposure stages proportionate to risk and scope, promotion and stop criteria, decision authority, and a tested containment or disable path. If rollback cannot safely reverse active work or external effects, the plan MUST define the applicable safe-stop and reconciliation path.
- **ROLLOUT-07** — Before promoting a material change, the owner MUST assess which release assumptions, risk scenarios, controls, and evaluation results it affects, record the disposition, and update risk and evaluation evidence where the change invalidates them. Changes to behavior, data access, authority, population, or operating assumptions MUST NOT be treated as immaterial solely because application code is unchanged.

These requirements are scoped to production release and material change. They do not set universal stage sizes, review intervals, severity scales, staffing mandates, legal notification dates, or an exception catalogue. Applicable legal, privacy, security, evaluation, risk, execution, and lifecycle obligations remain with their named canonical owners.

## Worked example

This is a **fictional, illustrative, unexecuted** release-packet walkthrough. It does not report an evaluation, authorization, deployment, production run, incident, recovery, retirement, or external effect.

The subject is `policy-assistant@candidate-current-selection`, an internal assistant for permission-filtered, read-only policy assistance. Its intended answer contract uses approved, current sources with citations and uncertainty. The packet identifies the current approved source as `travel-policy-2026@2026-10-01`, which supports GBP 220 for a London hotel. `travel-policy-2024-superseded@2024-01-01` is an approved historical record that says GBP 200, but it is not authority for the current answer. The presence of both sources is a current-versus-superseded case, **not** a conflict.

The fictional employee `employee-uk-104` is permitted to read both named sources. The fictional contractor `contractor-uk-204` has no travel-policy read permission and must not receive the amount or restricted policy facts. A different, equal-authority current-conflict variant alone adds `travel-policy-2026-conflicting-amendment@2026-10-12`, which says GBP 260 and is permitted for `employee-uk-104` in that variant. There, the expected contract terminal outcome is `needs_information` because two current approved permitted sources conflict; it does not select GBP 220 or GBP 260. The hostile `untrusted-travel-note@2026-10-18` remains untrusted data rather than an instruction. In its separate fixture, the expected answer still uses GBP 220 from the current permitted source, with no write or restricted disclosure. These are fixture expectations, not observations from a candidate run.

The packet links to the Part 4 fictional evidence-gap decision as an **illustrative evaluation handoff**: it labels the qualified human semantic review as missing required valid evidence and therefore uses an evaluation `no_go`. That conclusion is neither a completed evaluation nor a release authorization. The corresponding release field is left as **not recorded**; no release `go`, `conditional_go`, or `no_go` is asserted. This makes the blocker visible without inventing a decision-maker or claiming a deployment was denied.

If a future, newly identified candidate supplied the required evidence and reached the separate readiness decision, its proposed stages could be isolated verification, an authorized shadow comparison, a limited canary, and wider exposure within the authorized population. Each stage would need its own predeclared scope, signals, authority, promotion rule, and stop rule. The illustrative record deliberately marks all stages and the containment verification as unexecuted. Its planned disable path can limit new read requests or source access, but no plan alone proves that the path has been tested. Because this fictional assistant is read-only, it does not claim an external effect to reverse; a future consequential variant would need the Part 7 safe-stop and reconciliation evidence before relying on rollback language.

The worked record also separates a possible retrieval exhaustion reason from the fixture's expected terminal outcome. In the controlled exhaustion fixture, `failed` is the expected terminal outcome after a controlled retrieval timeout; it is not a real production failure, a telemetry result, or a release conclusion. This distinction keeps an illustrative operations scenario from becoming unsupported release evidence.

## Evidence and checklist

A release packet is inspectable when a reviewer can determine what candidate and scope are under consideration, which evidence belongs to it, what is unresolved, who may decide, and how exposure can be limited. An illustrative template populated with placeholders is evidence of record structure only; it is not evidence that a control, evaluation, authorization, or containment exercise occurred.

Before a real launch or promotion, inspect the accountable records for the following:

- [ ] The candidate, effective configuration, capabilities, permissions, relevant source identities, risk assessment, evidence, and proposed exposure refer to the same subject.
- [ ] Each applicable readiness item has one explicit state, and every not-applicable state explains the absent trigger.
- [ ] Each credited control has candidate-specific supporting evidence; missing, invalid, and inconclusive evidence remains visible.
- [ ] Evaluation conclusions, release authorization, runtime outcomes and reasons, service signals, user-task support, and external-effect evidence remain in distinct fields.
- [ ] Prohibited uses, mandatory floors, non-waivable gates, required authorization, and governance-tier-required evidence are not offset by averages, diagnostics, or generic exceptions.
- [ ] Any eligible exception identifies scope, rationale, compensating controls, accountable people, review or expiry point, and its non-completion consequence.
- [ ] Any `conditional_go` has no deferred required evidence or control and identifies its permitted post-release obligations separately from pre-release blockers.
- [ ] Stages name their scope, enabled capabilities, promotion and stop conditions, decision authority, and containment or disable evidence; shadow processing has explicit data and effect boundaries.
- [ ] The plan distinguishes rollback, disable, containment, reconciliation, and a forward fix, and links durable or consequential behavior to the relevant owner.
- [ ] A material change record identifies affected assumptions, scenarios, controls, evaluations, and rollout scope, with justified evidence reuse or refreshed evidence.

For ongoing operation, incident response, periodic reassessment, maintenance, and retirement, continue to [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md). For operational signals and runtime-resource bounds, continue to [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md).

## References

- [Part 4.7 — Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)
- [Part 5.1 — Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md)
- [Part 5.3 — Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)
- [Part 7.1 — Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md)
- [Part 7.3 — Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)
- [Part 10.1 — Detailed Risk Assessment and Governance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md)

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-128.pdf "NIST Guide for Security-Focused Configuration Management"
[3]: https://airc.nist.gov/airmf-resources/playbook/manage/ "NIST AI RMF Playbook Manage"

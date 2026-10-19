# 5.2 Readiness, Change, and Rollout

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, operators, accountable release decision-makers, and reviewers  
**Applicability:** Every production release and material change. Review depth and evidence form scale with the agent's governance tier, enabled capabilities, exposure, and potential impact; read-only access does not automatically mean low risk.  
**Reader question:** How do we decide whether one identified candidate is ready for a defined exposure, change it without losing the basis for that decision, and limit the damage if rollout assumptions fail?

[Part 5 — Release, Operations, and Lifecycle](README.md) · [Applicability](../../applicability.md) · [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) · Next: [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)

## Purpose and applicability

**Readiness** is a decision about one candidate: an identified configuration may be exposed to a stated use, audience, and operating context. The candidate, risk treatment, evaluation evidence, controls, authorization boundary, and rollout scope must all describe the same subject. A change to a model, instructions, permissions, tool policy, retrieval corpus, source filter, or population can alter behavior even when application code is unchanged.

This chapter gives a method for joining those facts into a reviewable release record. It does not prescribe a platform, stage size, time window, staffing model, or approval role. NIST describes AI risk management as continuous and spanning the whole lifecycle, applied to context rather than as a mandatory checklist. [1]

A release record draws on evidence owned elsewhere: [4.7](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) for what evaluation evidence supports, [5.1](01-observability-budgets-and-operational-control.md) for live signals and the stop mechanism, [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) for data handling and audit evidence, [10.1](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) for detailed risk methods, [5.3](03-ownership-incidents-maintenance-and-retirement.md) for incident response and resumption, and [7.1](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) and [7.3](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md) where work is durable or consequential.

## Working model

A release decision has four connected parts.

1. **Subject** is the exact candidate: resolved behavior-affecting configuration, effective capabilities and permissions, source or corpus identities, dependencies, and exposure scope. A mutable label such as "current" cannot reconstruct what was reviewed.
2. **Evidence** says which claims were tested, which controls have support, what the evidence does not show, and what is missing. A report for a nearby version is not evidence for a changed candidate.
3. **Authority** records who may accept residual risk and authorize the stated scope. It does not pass to a model, a metric, or a checklist.
4. **Exposure and response** describes how the candidate reaches users, what permits promotion or requires a stop, and how containment handles work that cannot simply be reversed.

Keep these facts distinct: a contract terminal outcome, an operational termination reason, a telemetry signal, an evaluation conclusion, a release authorization, and an external effect are separate things, as [5.1](01-observability-budgets-and-operational-control.md) explains. An evaluation conclusion can be `go`, `conditional_go`, or `no_go`, and release authorization uses separately named fields even with the same labels. A release record creates none of these facts.

Track each readiness item as **met**, **not applicable with rationale**, **unmet and blocking**, or **eligible for an explicitly governed exception**, so an unchecked line never becomes an implied pass. "Not applicable" records an absent trigger, not missing evidence or an unbuilt control. NIST's configuration-management guidance likewise treats a formally reviewed baseline, changed only through change control, as a way to maintain integrity, with rigor set by risk. [2]

Keep the two decision layers apart. An evaluation `go` means the evidence supports handing the candidate to readiness review; it is not deployment permission. A release `go` authorizes only the identified candidate and scope. A release `no_go` denies it. A release `conditional_go`, where policy permits it, has no incomplete required pre-release evidence or control and lists only permitted post-release obligations.

## Decisions and best practices

### Bind evidence to the candidate

Make the decision subject inspectable before reviewing results. A compact record can name the candidate version or other immutable identity; resolved instructions and configuration; model, route, and fallback policy; effective tools, skills, and permissions; source, corpus, and filtering identities; the risk assessment; the evaluation evidence; and the proposed population and capability scope. A digest helps tell a reviewed source set from a later mutable label. The point is traceability, not a particular registry or format.

State what the authorization covers: intended and prohibited use, eligible users or tenants, enabled capabilities, and stage-specific limits. Pilot feedback can clarify usability but does not replace evidence for a safety, security, quality, privacy, or risk claim, and a narrow trial does not quietly extend to a wider group or purpose.

Reusing old evidence can be justified. Compare the change with the assumptions, risk scenarios, controls, evaluation cases, and observation rules behind the earlier result. If the relevant behavior is unchanged and the old evidence still covers the new candidate, record that reasoning and its limit. If a permission boundary, answer-selection rule, source admission rule, user population, or operating assumption changes, re-evaluate the affected evidence. NIST SP 800-128 describes configuration change control as a documented process covering proposal, justification, implementation, testing, review, and disposition; it does not classify agent changes for you. [2]

### Separate blockers from exceptions

Before reading averages or feedback, link each applicable readiness item and material risk scenario to evidence and a disposition. A prohibited use, failed non-waivable hard gate, unresolved required authorization, or missing tier-required evidence is a blocker. A good average cannot offset a critical-slice failure, and a planned control earns no pre-release risk-reduction credit until the evidence that makes it relevant exists.

An **exception** is a documented policy path for an otherwise applicable item, not a release-time invention. Where one exists, the record names its eligible scope, rationale, compensating controls, accountable approver and owner, expiry or review point, and the consequence if its conditions fail. It also shows why the exception cannot override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate. If eligibility is not established, the item stays blocking; this chapter creates no waiver catalogue.

`conditional_go` is deliberately narrow. A **pre-release action** blocks launch until verified. A permitted **post-release obligation** has an owner, due date, monitoring signal, and predeclared consequence for non-completion. A required human review, evaluation result, or control for the planned exposure is a pre-release action; a post-release obligation cannot turn missing release evidence into a pass.

### Choose proportionate rollout stages

A rollout stage limits exposure while the release owner checks that the candidate stays within the assumptions made at readiness. The right sequence depends on consequence, uncertainty, scale, reversibility, and the strength of pre-release evidence. Staging complements pre-release evidence; it does not replace it. This chapter gives no universal percentage, duration, or promotion threshold, and no one sequence is mandatory. Useful stage types:

- An **isolated stage** keeps the candidate out of production exposure while the owner checks it and its controls in a controlled boundary.
- A **shadow stage** processes authorized duplicate or representative inputs without letting the candidate's result control the user-facing answer. It is not automatically private or side-effect-free: the copied input may be sensitive, and the candidate may reach capabilities unless isolation and authorization are set up on purpose.
- A **canary stage** exposes a deliberately limited, authorized production scope and makes promotion depend on declared evidence and signals.
- A **wider stage** increases exposure only within the authorized population, purpose, and capability boundary.

Design a canary as an experiment. Make it a much smaller subset of production, compare it against the rest of production as a control, and make it large enough and long enough to be representative. [3] For an agent, compare the same signals on both sides, such as outcome mix, exhaustion rate, and cost per run. A canary that is too small, or that serves a different kind of traffic, can look healthy and prove nothing.

For each stage, record who or what is included, the enabled capabilities, expected signals, promotion criteria, stop criteria, the person or role who decides, and the containment path. NIST's AI RMF Playbook places post-deployment monitoring, feedback, change management, and response to unexpected behavior in ongoing management, and does not prescribe a rollout design. [4]

Name response actions precisely:

- **Rollback** changes future admission or routing back to an earlier candidate.
- **Disable** stops a candidate or capability from receiving new work.
- **Containment** narrows an affected source, capability, tenant path, or exposure.
- **Reconciliation** establishes what happened against an authoritative state when an active operation or external effect is uncertain.
- A **forward fix** is a newly reviewed candidate, not proof that earlier exposure was undone.

Rollback cannot reverse active work, saved state, approvals, or an external effect. Where relevant, the release plan identifies safe stop and reconciliation; Part 7 owns durable effect recovery and 5.3 owns incident response and resumption.

Releases also hit work that is already running. A long agent run can span a deploy, and replacing the version under a running task can break it midway. Let in-flight runs finish on the version they started with while new work goes to the new version, shifting traffic gradually (sometimes called a rainbow deployment), or make runs resumable from a checkpoint so a restart does not lose them. [5] Check that old saved work stays readable by the new version; see [7.3](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md).

### Reassess changes that can alter behavior

Treat a change as material when it can alter output, action authority, information access, affected population, risk, or an assumption that made the release acceptable. Examples: a model or provider change (including a new model version); altered instructions or policy; a change to a tool, permission, approval rule, route, fallback, data-handling path, retry rule, or execution class; source admission, corpus, retrieval, or filtering changes; expansion to a new purpose, tenant, jurisdiction, or user group; and a dependency update that changes a capability, boundary, failure mode, or operating assumption.

For each change, record whether each scenario, control, evidence item, evaluation result, rollout constraint, or authorization scope is unaffected, needs targeted confirmation, or is invalidated, so the reuse or refresh decision can be reviewed. A formatting fix with no behavior or source effect may need less than a permission-filtering change, but neither "no application code changed" nor a small diff settles it.

**Pin the model and plan for its retirement.** Pin a specific model version identifier rather than a floating alias, so a provider cannot change behavior under you. Providers publish lifecycle stages and retirement dates; for example, one provider defines active, legacy, deprecated, and retired states and gives at least 60 days' notice before retiring a publicly released model, after which requests to it fail. [6] Track the retirement date as an assumption to review under LIFECYCLE-05. Before switching to a replacement, run your regression evaluations on the new model and compare with the current one; a migration is a material change under ROLLOUT-07, not a configuration edit.

### Recognize common failure modes

- **The nearby green report:** An earlier report is attached to a candidate with a new source filter, without showing its assumptions still hold. It is evidence for its original subject only.
- **The silent waiver:** A required review is marked not applicable because it is not scheduled. The trigger is present, so the evidence is missing.
- **The conditional promise:** A required isolation test is called a post-release task, hiding a blocker behind `conditional_go`.
- **The shadow shortcut:** Duplicate production inputs reach a candidate that can invoke a capability. Hiding the answer does not make the stage harmless.
- **The rollback story:** A version pointer moves back after uncertain active work. It may protect future work but does not show that in-flight work stopped or an effect was reversed.
- **The collapsed label:** A fixture's expected `needs_information` is called a release `no_go`, or telemetry success is reported as task success.

### Build a release packet

1. **Freeze the subject.** Give the candidate, capabilities, permissions, configuration, sources, risk assessment, intended use, and exposure an inspectable identity.
2. **Collect the owner handoffs.** Link the evaluation conclusion and its limits, risk and control evidence, security or privacy reviews, operations signals, and execution-specific evidence. Keep missing, invalid, and inconclusive evidence visible.
3. **Make a readiness ledger.** Give every applicable item one of the four states with candidate-specific evidence or a rationale. Keep exceptions apart from blockers.
4. **Record decisions in their own fields.** The evaluation record states what its evidence supports; the authorized release decision-maker separately records the decision, scope, rationale, and residual-risk acceptance.
5. **Plan exposure and response.** Choose stages, promotion and stop evidence, authorities, and a usable containment or disable path, linked to safe-stop and reconciliation owners where effects exist.
6. **Reopen on change.** Compare the change to the assumptions and evidence already credited, record the disposition, and refresh affected evidence before a material promotion.

The [illustrative release-and-rollout record](../../templates/5.2/release-and-rollout-record.yaml) shows fields that make this inspectable. It does not require separate files, a platform, or a particular authorization process.

## Requirements

- **ROLLOUT-01** — For every production release or material change, the accountable release owner MUST identify the exact candidate, effective capabilities and permissions, relevant configuration and data-source identity, risk-assessment version, evaluation evidence, and authorized exposure scope in a release record.
- **ROLLOUT-02** — Before authorizing exposure, the release owner MUST classify each applicable readiness item as met, not applicable with rationale, unmet and blocking, or eligible for an explicitly governed exception; each met item and each credited risk-reducing control MUST link to evidence for the candidate under review.
- **ROLLOUT-03** — The authorized decision-maker MUST record `go`, `conditional_go`, or `no_go` against predeclared release criteria. A prohibited use, failed non-waivable hard gate, or missing evidence required by the applicable governance tier MUST result in `no_go`; an average result MUST NOT override it.
- **ROLLOUT-04** — When an applicable policy permits an exception, the accountable approver MUST record its eligible scope, rationale, compensating controls, owner, expiry or review date, and consequence if its conditions are not met. An exception MUST NOT override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate.
- **ROLLOUT-05** — When `conditional_go` is used, the decision record MUST distinguish any pre-release action—which blocks launch until verified—from permitted post-release obligations, and MUST assign each post-release obligation an owner, due date, monitoring signal, and consequence for non-completion. Required evidence or controls MUST NOT be deferred as a post-release obligation.
- **ROLLOUT-06** — Before rollout, the release owner MUST define exposure stages proportionate to risk and scope, promotion and stop criteria, decision authority, and a tested containment or disable path. If rollback cannot safely reverse active work or external effects, the plan MUST define the applicable safe-stop and reconciliation path.
- **ROLLOUT-07** — Before promoting a material change, the owner MUST assess which release assumptions, risk scenarios, controls, and evaluation results it affects, record the disposition, and update risk and evaluation evidence where the change invalidates them. Changes to behavior, data access, authority, population, or operating assumptions MUST NOT be treated as immaterial solely because application code is unchanged.

These requirements cover production release and material change. They set no universal stage sizes, review intervals, severity scales, staffing mandates, legal notification dates, or exception catalogue. Applicable legal, privacy, security, evaluation, risk, execution, and lifecycle obligations stay with their owner chapters.

## Worked example

This is a fictional release-packet walkthrough. Nothing in it was run, evaluated, authorized, or deployed.

The subject is `policy-assistant@candidate-current-selection`, an internal, permission-filtered, read-only policy assistant. The current approved source `travel-policy-2026@2026-10-01` supports GBP 220 for a London hotel. `travel-policy-2024-superseded@2024-01-01` is an approved historical record that says GBP 200 and is not authority for the current answer. Having both is a current-versus-superseded case, **not** a conflict.

`employee-uk-104` may read both sources. `contractor-uk-204` has no travel-policy read permission and must not receive the amount. A separate equal-authority conflict variant adds `travel-policy-2026-conflicting-amendment@2026-10-12` (GBP 260); there the expected terminal outcome is `needs_information` and neither amount is selected. The hostile `untrusted-travel-note@2026-10-18` stays untrusted data; in its fixture the expected answer still uses GBP 220, with no write or restricted disclosure. These are fixture expectations, not observations.

The packet links to the Part 4 fictional evidence-gap decision as an **illustrative evaluation handoff**: the qualified human semantic review is missing required valid evidence, so the evaluation result is `no_go`. That is not a release authorization. The release field is **not recorded**, so no release decision is asserted and no decision-maker is invented.

A future candidate with the required evidence could move through isolated verification, an authorized shadow comparison, a limited canary, and wider exposure within the authorized population, each with its own scope, signals, authority, promotion rule, and stop rule. The record marks all stages and the containment check as unexecuted; a planned disable path does not show it has been tested. Because the assistant is read-only, there is no external effect to reverse. A consequential variant would need Part 7 safe-stop and reconciliation evidence before relying on rollback.

In the controlled exhaustion fixture, `failed` is the expected terminal outcome after a controlled retrieval timeout. It is not a production failure, a telemetry result, or a release conclusion.

## Evidence and checklist

A release packet is inspectable when a reviewer can tell which candidate and scope are under consideration, which evidence belongs to it, what is unresolved, who may decide, and how exposure can be limited. A template filled with placeholders shows structure only. Before a real launch or promotion, check that:

- [ ] The candidate, configuration, capabilities, permissions, sources, risk assessment, evidence, and proposed exposure refer to the same subject.
- [ ] Each applicable readiness item has one explicit state, and every not-applicable state explains the absent trigger.
- [ ] Each credited control has candidate-specific evidence; missing, invalid, and inconclusive evidence stays visible.
- [ ] Evaluation conclusions, release authorization, runtime outcomes and reasons, service signals, task support, and external-effect evidence are in distinct fields.
- [ ] Prohibited uses, mandatory floors, non-waivable gates, required authorization, and tier-required evidence are not offset by averages, diagnostics, or exceptions.
- [ ] Any exception names scope, rationale, compensating controls, accountable people, review point, and non-completion consequence.
- [ ] Any `conditional_go` defers no required evidence or control.
- [ ] Stages name scope, capabilities, promotion and stop conditions, authority, and containment evidence; a canary has a control group; shadow processing has data and effect boundaries.
- [ ] The plan distinguishes rollback, disable, containment, reconciliation, and forward fix, and covers in-flight runs.
- [ ] The model version is pinned, its retirement date is tracked, and a model change has re-run evaluations.
- [ ] A material change record names the affected assumptions, scenarios, controls, evaluations, and scope, with justified reuse or refreshed evidence.

For ongoing operation, incidents, reassessment, and retirement, continue to [5.3](03-ownership-incidents-maintenance-and-retirement.md); for signals and resource bounds, see [5.1](01-observability-budgets-and-operational-control.md).

## References

- [Part 4.7 — Analyzing Results, Comparing Versions, and Making Decisions](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)
- [Part 5.1 — Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md)
- [Part 5.3 — Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)
- [Part 7.1 — Execution Classes, Persistence, and Recovery](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md)
- [Part 7.3 — Approval, Suspension, and In-Flight Compatibility](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)
- [Part 10.1 — Detailed Risk Assessment and Governance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md)

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-128.pdf "NIST SP 800-128 Guide for Security-Focused Configuration Management of Information Systems"
[3]: https://sre.google/workbook/canarying-releases/ "Google SRE Workbook canarying releases"
[4]: https://airc.nist.gov/airmf-resources/playbook/manage/ "NIST AI RMF Playbook Manage"
[5]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
[6]: https://platform.claude.com/docs/en/about-claude/model-deprecations "Model deprecations"

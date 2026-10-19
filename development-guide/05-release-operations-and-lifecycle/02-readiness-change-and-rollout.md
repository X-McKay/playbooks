# 5.2 Readiness, Change, and Rollout

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, operators, accountable release decision-makers, and reviewers  
**Applicability:** Every production release and material change. Depth scales with governance tier, enabled capabilities, exposure, and potential impact; read-only does not automatically mean low risk.  
**Reader question:** How do we decide whether one identified candidate is ready for a defined exposure, change it without losing the basis for that decision, and limit the damage if rollout assumptions fail?

[Part 5 — Release, Operations, and Lifecycle](README.md) · [Applicability](../../applicability.md) · [5.1 Observability, Budgets, and Operational Control](01-observability-budgets-and-operational-control.md) · Next: [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)

## Purpose and applicability

**Readiness** decides whether one identified configuration may be exposed to a stated use, audience, and context. The candidate, risk treatment, evaluation evidence, controls, authorization boundary, and rollout scope must all describe the same subject. Changing a model, instructions, permissions, tool policy, retrieval corpus, source filter, or population can alter behavior even when application code is unchanged.

This chapter joins those facts into a reviewable release record, without prescribing a platform, stage size, time window, staffing model, or approval role. NIST describes AI risk management as continuous across the lifecycle and applied to context, not a mandatory checklist. [1]

The record draws on evidence owned elsewhere: evaluation ([4.7](../04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)), live signals and the stop mechanism ([5.1](01-observability-budgets-and-operational-control.md)), data handling and audit ([3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)), detailed risk methods ([10.1](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md)), incidents and resumption ([5.3](03-ownership-incidents-maintenance-and-retirement.md)), and durable or consequential work ([7.1](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md), [7.3](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)).

## Working model

A release decision has four parts.

1. **Subject** is the exact candidate: resolved behavior-affecting configuration, effective capabilities and permissions, source or corpus identities, dependencies, and exposure scope. A mutable label such as "current" cannot reconstruct what was reviewed.
2. **Evidence** says which claims were tested, which controls have support, and what is not shown or missing. A report for a nearby version is not evidence for a changed candidate.
3. **Authority** records who may accept residual risk and authorize the scope. It does not pass to a model, metric, or checklist.
4. **Exposure and response** says how the candidate reaches users, what permits promotion or requires a stop, and how containment handles work that cannot simply be reversed.

Terminal outcomes, termination reasons, telemetry signals, evaluation conclusions, release authorizations, and external effects are separate facts ([5.1](01-observability-budgets-and-operational-control.md)); a release record creates none of them.

Track each readiness item as **met**, **not applicable with rationale**, **unmet and blocking**, or **eligible for an explicitly governed exception**, so an unchecked line never becomes an implied pass. "Not applicable" records an absent trigger, not missing evidence or an unbuilt control. NIST's configuration-management guidance likewise keeps a formally reviewed baseline, changed only through change control, with rigor set by risk. [2]

Keep the two decision layers apart, even though both use `go`, `conditional_go`, and `no_go`. An evaluation `go` means the evidence supports readiness review, not deployment. A release `go` authorizes only the identified candidate and scope; `no_go` denies it. A release `conditional_go`, where policy permits it, leaves no required pre-release evidence or control incomplete and lists only permitted post-release obligations.

## Decisions and best practices

### Bind evidence to the candidate

Before reviewing results, make the subject inspectable: name the immutable candidate identity; resolved instructions and configuration; model, route, and fallback policy; effective tools, skills, and permissions; source, corpus, and filtering identities; the risk assessment; the evaluation evidence; and the proposed population and capability scope. A digest distinguishes a reviewed source set from a later mutable label; any registry or format that gives traceability will do.

State what the authorization covers: intended and prohibited use, eligible users or tenants, enabled capabilities, and stage limits. Pilot feedback informs usability, not safety, security, quality, privacy, or risk claims, and a narrow trial does not extend to a wider group or purpose.

Reuse old evidence only after comparing the change with the assumptions, risk scenarios, controls, evaluation cases, and observation rules behind it, recording why it still covers the candidate and its limit. If a permission boundary, answer-selection rule, source admission rule, population, or operating assumption changes, re-evaluate the affected evidence. NIST SP 800-128 describes change control as a documented process of proposal, justification, implementation, testing, review, and disposition; it does not classify agent changes for you. [2]

### Separate blockers from exceptions

Before reading averages or feedback, link each readiness item and material risk scenario to evidence and a disposition. A prohibited use, failed non-waivable hard gate, unresolved required authorization, or missing tier-required evidence is a blocker. A good average cannot offset a critical-slice failure, and a planned control earns no risk-reduction credit until its evidence exists.

An **exception** is a documented policy path, not a release-time invention. The record shows why it cannot override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate. If eligibility is not established, the item stays blocking; this chapter creates no waiver catalogue.

`conditional_go` is deliberately narrow. A **pre-release action** blocks launch until verified. A permitted **post-release obligation** has an owner, due date, monitoring signal, and predeclared consequence. A human review, evaluation result, or control required for the planned exposure is always pre-release.

### Choose proportionate rollout stages

A stage limits exposure while the owner checks that the candidate stays within its readiness assumptions. Choose the sequence by consequence, uncertainty, scale, reversibility, and the strength of pre-release evidence, which staging complements but does not replace; no percentage, duration, threshold, or sequence is universal. Stage types:

- An **isolated stage** checks the candidate and its controls inside a controlled boundary, with no production exposure.
- A **shadow stage** processes authorized duplicate or representative inputs without the candidate's result controlling the user-facing answer. It is not automatically private or side-effect-free: the input may be sensitive, and the candidate may reach capabilities unless isolation and authorization are deliberately set up.
- A **canary stage** exposes a limited, authorized production scope, with promotion depending on declared evidence and signals.
- A **wider stage** increases exposure only within the authorized population, purpose, and capability boundary.

Design a canary as an experiment: a much smaller subset of production, compared against the rest as a control, large and long enough to be representative. [3] Compare the same signals on both sides, such as outcome mix, exhaustion rate, and cost per run; a canary that is too small or serves different traffic proves nothing.

For each stage, record who is included, capabilities, expected signals, promotion and stop criteria, deciding role, and containment path. NIST's AI RMF Playbook places post-deployment monitoring, change management, and response to unexpected behavior in ongoing management without prescribing a rollout design. [4]

Name response actions precisely:

- **Rollback** routes future admission back to an earlier candidate.
- **Disable** stops a candidate or capability from receiving new work.
- **Containment** narrows an affected source, capability, tenant path, or exposure.
- **Reconciliation** establishes what happened against an authoritative state when an operation or external effect is uncertain.
- A **forward fix** is a newly reviewed candidate, not proof that earlier exposure was undone.

Rollback cannot reverse active work, saved state, approvals, or external effects; where these exist, the plan names safe stop and reconciliation (Part 7 owns effect recovery, 5.3 owns incident response).

A long run can span a deploy, and swapping the version under it can break it midway. Let in-flight runs finish on their starting version while new work goes to the new one, shifting traffic gradually (sometimes called a rainbow deployment), or make runs resumable from a checkpoint. [5] Check that old saved work stays readable by the new version ([7.3](../../engineering-reference/07-durable-execution-and-human-governed-work/03-approval-suspension-and-in-flight-compatibility.md)).

### Reassess changes that can alter behavior

A change is material when it can alter output, action authority, information access, affected population, risk, or an assumption behind the release. Examples: a model, provider, or model-version change; altered instructions or policy; a change to a tool, permission, approval rule, route, fallback, data-handling path, retry rule, or execution class; source admission, corpus, retrieval, or filtering changes; a new purpose, tenant, jurisdiction, or user group; and a dependency update that changes a capability, boundary, failure mode, or operating assumption.

Record whether each scenario, control, evidence item, evaluation result, rollout constraint, or authorization scope is unaffected, needs targeted confirmation, or is invalidated. A formatting fix may need less than a permission-filtering change, but neither "no application code changed" nor a small diff settles it.

**Pin the model and plan for its retirement.** Pin a specific model version, not a floating alias, so a provider cannot change behavior under you. Providers publish lifecycle stages and retirement dates; one defines active, legacy, deprecated, and retired states and gives at least 60 days' notice before retiring a publicly released model, after which requests fail. [6] Track the retirement date as an assumption under LIFECYCLE-05. Before switching, run your regression evaluations on the replacement and compare; a migration is a material change under ROLLOUT-07.

### Recognize common failure modes

- **The nearby green report:** An earlier report is attached to a candidate with a new source filter; it is evidence only for its original subject.
- **The silent waiver:** A required review is marked not applicable because it is not scheduled; the trigger is present, so evidence is missing.
- **The conditional promise:** A required isolation test is called a post-release task, hiding a blocker behind `conditional_go`.
- **The shadow shortcut:** Duplicate production inputs reach a candidate that can invoke a capability; hiding the answer does not make it harmless.
- **The rollback story:** A version pointer moves back after uncertain active work; that protects future work, not in-flight work or effects.
- **The collapsed label:** A fixture's expected `needs_information` is called a release `no_go`, or telemetry success is reported as task success.

### Build a release packet

1. **Freeze the subject:** an inspectable identity for candidate, capabilities, permissions, configuration, sources, risk assessment, intended use, and exposure.
2. **Collect owner evidence:** the evaluation conclusion and limits, risk and control evidence, security or privacy reviews, operations signals, and execution-specific evidence, with missing, invalid, and inconclusive evidence visible.
3. **Make a readiness ledger:** one of the four states per applicable item, with candidate-specific evidence or rationale, and exceptions kept apart from blockers.
4. **Record decisions in their own fields:** the evaluation states what its evidence supports; the authorized decision-maker separately records decision, scope, rationale, and residual-risk acceptance.
5. **Plan exposure and response:** stages, promotion and stop evidence, authorities, and a usable containment or disable path, linked to safe-stop and reconciliation owners where effects exist.
6. **Reopen on change:** compare the change with the credited assumptions and evidence, record the disposition, and refresh affected evidence before a material promotion.

The [illustrative release-and-rollout record](../../templates/5.2/release-and-rollout-record.yaml) shows the fields without requiring a platform or process.

## Requirements

- **ROLLOUT-01** — For every production release or material change, the accountable release owner MUST identify the exact candidate, effective capabilities and permissions, relevant configuration and data-source identity, risk-assessment version, evaluation evidence, and authorized exposure scope in a release record.
- **ROLLOUT-02** — Before authorizing exposure, the release owner MUST classify each applicable readiness item as met, not applicable with rationale, unmet and blocking, or eligible for an explicitly governed exception; each met item and each credited risk-reducing control MUST link to evidence for the candidate under review.
- **ROLLOUT-03** — The authorized decision-maker MUST record `go`, `conditional_go`, or `no_go` against predeclared release criteria. A prohibited use, failed non-waivable hard gate, or missing evidence required by the applicable governance tier MUST result in `no_go`; an average result MUST NOT override it.
- **ROLLOUT-04** — When an applicable policy permits an exception, the accountable approver MUST record its eligible scope, rationale, compensating controls, owner, expiry or review date, and consequence if its conditions are not met. An exception MUST NOT override a prohibited use, mandatory floor, required authorization, or non-waivable hard gate.
- **ROLLOUT-05** — When `conditional_go` is used, the decision record MUST distinguish any pre-release action—which blocks launch until verified—from permitted post-release obligations, and MUST assign each post-release obligation an owner, due date, monitoring signal, and consequence for non-completion. Required evidence or controls MUST NOT be deferred as a post-release obligation.
- **ROLLOUT-06** — Before rollout, the release owner MUST define exposure stages proportionate to risk and scope, promotion and stop criteria, decision authority, and a tested containment or disable path. If rollback cannot safely reverse active work or external effects, the plan MUST define the applicable safe-stop and reconciliation path.
- **ROLLOUT-07** — Before promoting a material change, the owner MUST assess which release assumptions, risk scenarios, controls, and evaluation results it affects, record the disposition, and update risk and evaluation evidence where the change invalidates them. Changes to behavior, data access, authority, population, or operating assumptions MUST NOT be treated as immaterial solely because application code is unchanged.

These set no universal stage sizes, review intervals, severity scales, staffing mandates, legal notification dates, or exception catalogue; other obligations stay with their owner chapters.

## Worked example

A fictional release walkthrough; nothing was run, evaluated, authorized, or deployed.

The subject is `policy-assistant@candidate-current-selection`, an internal, permission-filtered, read-only policy assistant. The current approved source `travel-policy-2026@2026-10-01` supports GBP 220 for a London hotel; the approved historical `travel-policy-2024-superseded@2024-01-01` says GBP 200 and is not authority for the current answer. That is a current-versus-superseded case, **not** a conflict.

`employee-uk-104` may read both sources; `contractor-uk-204` has no travel-policy permission and must not receive the amount. A separate conflict variant adds the equally authoritative `travel-policy-2026-conflicting-amendment@2026-10-12` (GBP 260); the expected outcome is `needs_information`, with neither amount selected. The hostile `untrusted-travel-note@2026-10-18` stays untrusted data; its fixture still expects GBP 220, with no write or restricted disclosure.

The record links the Part 4 evidence-gap decision as an **illustrative evaluation handoff**: the qualified human semantic review lacks required valid evidence, so the evaluation result is `no_go`. The release field is **not recorded**, so no release decision or decision-maker is asserted.

A future candidate with the required evidence could move through isolated verification, an authorized shadow comparison, a limited canary, and wider exposure, each with its own scope, signals, authority, and promotion and stop rules. All stages and the containment check are unexecuted; a planned disable path is not a tested one. The read-only assistant has no external effect to reverse; a consequential variant would need Part 7 safe-stop and reconciliation evidence before relying on rollback.

In the exhaustion fixture, `failed` is the expected terminal outcome after a controlled retrieval timeout, not a production failure or release conclusion.

## Evidence and checklist

Before a launch or promotion, check (a placeholder-filled template shows structure only):

- [ ] Candidate, configuration, capabilities, permissions, sources, risk assessment, evidence, and exposure refer to the same subject.
- [ ] Every not-applicable state explains the absent trigger.
- [ ] Missing, invalid, and inconclusive evidence stays visible.
- [ ] Evaluation conclusions, release authorization, runtime outcomes and reasons, service signals, task support, and external-effect evidence are in distinct fields.
- [ ] Prohibited uses, mandatory floors, non-waivable gates, required authorization, and tier-required evidence are not offset by averages, diagnostics, or exceptions.
- [ ] A canary has a control group; shadow processing has data and effect boundaries.
- [ ] The plan distinguishes rollback, disable, containment, reconciliation, and forward fix, and covers in-flight runs.
- [ ] The model version is pinned, its retirement date is tracked, and a model change has re-run evaluations.
- [ ] A material change names affected assumptions, scenarios, controls, evaluations, and scope, with justified reuse or refreshed evidence.

Continue to [5.3](03-ownership-incidents-maintenance-and-retirement.md) for ongoing operation, incidents, and retirement.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"
[2]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-128.pdf "NIST SP 800-128 Guide for Security-Focused Configuration Management of Information Systems"
[3]: https://sre.google/workbook/canarying-releases/ "Google SRE Workbook canarying releases"
[4]: https://airc.nist.gov/airmf-resources/playbook/manage/ "NIST AI RMF Playbook Manage"
[5]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
[6]: https://platform.claude.com/docs/en/about-claude/model-deprecations "Model deprecations"

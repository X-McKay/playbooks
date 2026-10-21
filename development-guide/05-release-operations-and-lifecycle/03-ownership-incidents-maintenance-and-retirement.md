# 5.3 Ownership, Incidents, Maintenance, and Retirement

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Business and service owners, builders, operators, incident responders, reviewers, and recovery authorities  
**Applicability:** Every production agent needs accountable support and lifecycle arrangements. Response depth, staffing or combined roles, review cadence, and assurance depend on execution class, governance tier, enabled capabilities, exposure, and assessed risk.  
**Reader question:** Who owns a supported agent, what happens when a problem is suspected, how do feedback and change stay governed, and how do we retire the capability without leaving work, access, data, or evidence in an unknown state?

[Part 5 — Release, Operations, and Lifecycle](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Illustrative lifecycle record](../../templates/5.3/support-incident-and-retirement-record.yaml)

## Purpose and applicability

A production agent stays a supported capability after release. **Ownership** means identifiable people or staffed groups can make, carry out, and answer for the decisions it needs. **Lifecycle** is the continuing work of supporting the approved capability, noticing when its assumptions no longer hold, changing it through the right process, and retiring it deliberately. Neither equals release readiness.

Related: the initial ownership and risk record ([1.4](../01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md)), stop mechanics and signals ([5.1](01-observability-budgets-and-operational-control.md)), release and rollout recovery ([5.2](02-readiness-change-and-rollout.md)), privacy, retention, and audit ([3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)), and durable work and uncertain effects ([7.1](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md), [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)).

NIST frames incident response as part of cybersecurity risk management, improving preparation, detection, response, and recovery [1], and its AI RMF treats post-deployment monitoring, feedback, incident response, recovery, change management, and decommissioning as connected lifecycle concerns [2]. Neither sets roles, a severity scale, staffing, notification deadlines, or cadence.

## Working model

### Make accountability usable

Assign decisions to people or staffed groups, not only role labels; an unstaffed title cannot respond. The support record names a business or service owner accountable for the approved purpose, a technical contact who can investigate behavior, configuration, sources, and dependencies, an escalation route, and the authority for restart or material change.

One person may hold several roles when exposure and policy allow. Record the combination and its conflict rather than pretending separation exists, and identify any independent review the governance process requires. Proposing a permission expansion or corrective change does not give authority to approve, release, or resume it.

**Stop authority and restart authority answer different questions.** An operator needs authority to stop a run or prevent further work quickly; that protects the boundary but shows nothing about cause, safeguards, or release. A designated recovery authority decides whether the capability may resume after weighing the evidence and release gates. Mechanism: [5.1](01-observability-budgets-and-operational-control.md); release authorization: [5.2](02-readiness-change-and-rollout.md).

### Treat a suspected incident as a question, not a conclusion

A **signal** is an observation worth examining: a user report, support ticket, evaluator failure, dependency warning, unexpected outcome, or telemetry pattern. A **suspected incident** is a signal whose possible impact warrants documented triage and escalation; it does not yet confirm a compromise, root cause, or external effect.

This keeps the response useful for non-security harms. A wrong but permission-respecting answer, a stale source, an unavailable dependency, an unsafe attempted capability request, or recurring uncertainty may need investigation without being called an intrusion. A plausible cross-boundary disclosure, unexpected authority, or failed critical control needs rapid escalation even while facts are incomplete.

A practical loop, following NIST's preparation-to-improvement framing without adopting a universal playbook [1]: triage the signal; bound the scope; contain proportionately; preserve permitted evidence; investigate, keeping confirmed facts apart from hypotheses; decide the corrective action and remaining uncertainty; obtain recovery and release decisions; feed lessons into records, evaluations, controls, or retirement.

Learn from others' incidents too: public AI incident databases catalog real-world failures to turn into evaluation cases and checks. [5]

### Maintain assumptions, not merely uptime

**Maintenance** asks whether the conditions under which the capability was approved still hold, not just whether the service is reachable: contacts, behavior and permissions, source freshness, dependencies, accumulated failures and feedback, and working containment and revocation paths. NIST's AI RMF notes that deployed performance and trustworthiness can shift and that monitoring helps detect drift, unexpected behavior, and negative impacts. [2] That supports a periodic review set by the organization plus reassessment when evidence invalidates earlier assumptions; it gives no universal interval. Providers also retire model versions on published schedules, so track the pinned version's retirement date and plan the migration under [5.2](02-readiness-change-and-rollout.md) before requests fail. [6]

### Retire a capability as a controlled handover

**Deprecation** tells consumers to move away from a capability that may stay available during a stated transition. **Disabling** prevents some or all invocation now, often as containment, without settling the final disposition. **Retirement** is the recorded end state: new work stopped, consumers and outstanding work accounted for, unneeded access and registrations revoked, data disposition and evidence retention addressed, and the inventory or manifest no longer showing it as active. Disabled is not necessarily retired, and deprecated is not necessarily disabled.

Data disposition is **copy-specific**: active stores, retained evidence, exports, caches, backups, and third-party copies can each have different handling and retention duties. NIST describes media sanitization as making access to target data infeasible for a given level of effort, with techniques chosen by sensitivity. [3] So ask what copies exist and which approved process applies to each; there is no single method, deadline, or outcome for all records, logs, providers, or legal holds. Follow [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) and Part 10.

## Decisions and best practices

### Build the support record before it is needed

Keep one concise record a first responder can use cold: the business or service owner, technical contact, reachable support route, escalation path, restart and change authority, the authority to stop or prevent further work, combined roles, required independent review, and each authority's scope. It is an operating aid, not evidence of any release or recovery authorization.

Two common failures: naming a team without how to reach it or who decides next, which delays containment; and treating the deployer, stop operator, and recovery authority as interchangeable, which turns incident pressure into an unreviewed release path. CISA describes an incident-response plan as clarifying roles and responsibilities, guiding key activities, and listing key people needed in a crisis. [4]

### Triage impact and evidence before assigning blame

Make the runbook usable at first contact: what starts triage, which impact conditions escalate, which containment options exist, who decides, who handles required communications, and what minimum evidence may be preserved. Use locally approved impact and urgency criteria; this chapter adds no severity scale, response-time target, or notification deadline.

Record statements at their real strength. "The index may have been stale" is a hypothesis. "The controlled fixture contains a current source at revision X and a superseded source at revision Y" is a fixture fact. "A retrieval record shows source Y was selected in an observed run" is an observation. A root cause is confirmed only when the investigation supports it.

Choose the smallest safe containment that matches what is known: stopping new work, disabling a source, narrowing a tenant path, or blocking a capability. A narrowly identified stale source may justify blocking only that source; an unknown boundary may need broader stopping while it is assessed. Containment is not recovery, rollback, restoration, reconciliation, or a forward fix. Preserve only the permitted minimum to reconstruct events: agent and release identity, run or correlation reference, capability and source identity, observations, and times. A model narrative, citation, or invocation record does not establish an external effect; when one is uncertain, keep it unresolved and reconcile under [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) rather than retrying.

Before resuming, the recovery authority records the cause or remaining uncertainty, the corrective action, the evidence that safeguards and release gates are met, and the authorization to resume (LIFECYCLE-03). A repair that is a material change goes through [5.2](02-readiness-change-and-rollout.md), and a recovery record may cite an evaluation conclusion but must not relabel it as release authorization.

### Turn feedback into governed follow-up

Give each feedback item (user report, evaluator result, support case, operational signal, review finding) a disposition rather than treating it as an informal change instruction: investigate, correct source material, add or revise an evaluation case, propose a configuration or control change, document why it is not a defect, or propose retirement.

Feedback is not release permission and does not broaden authority. "The answer was helpful" does not show the source was current, the permission check was right, or a change is safe; one wrong answer does not show compromise. Look at source authority, requester permissions, behavior, dependency state, and observed scope together, and use the evaluation owner for conclusions and [5.2](02-readiness-change-and-rollout.md) to authorize a changed candidate.

### Reassess on time and on evidence

Set a periodic cadence proportionate to exposure and policy. Reassess earlier when an incident, a material behavior or permission change, a changed source or dependency, a new consumer, an ownership gap, a dependency warning, or an altered risk assumption could make the record stale. Test the support arrangement as well as the technology: can the named contacts act, are sources and dependencies still understood, have failures or feedback accumulated, does the evidence still describe the active capability, and do containment and revocation paths still work?

A cadence alone cannot establish ongoing safety, and an evidence-triggered review does not replace a policy cadence. If a scheduled review is missed, record the gap and decide its disposition under policy. Where [10.1](../../engineering-reference/10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) applies, also follow its tier-specific maxima.

### Plan deprecation and retirement before the urgent stop

While the capability is still understood, identify consumers, transition communication, outstanding work, access and registrations, data copies, retained evidence, and the inventory location. Start before deleting any hosting resource. For durable work, do not imply that a stop erased state or reversed an effect ([7.1](../../engineering-reference/07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md), [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)). If a problem forces immediate disabling, label it containment and leave retirement open until outstanding work and data disposition are assessed. Do not assume all data can be erased at once or that deleting a deployment revokes every credential.

Common failures: treating a retirement notice as completed retirement, leaving a consumer to discover a disabled capability, revoking a credential before in-flight work has a safe disposition, and leaving an active-looking inventory entry after access is removed. The remedy is a record distinguishing proposed, deprecated, disabled, retired, and unresolved states, not a universal timeline.

## Requirements

- **LIFECYCLE-01** For every production agent, the accountable owner MUST maintain a support record naming the business/service owner, technical contact, operational escalation path, and authority for restart or material change, with a reachable primary or staffed-group contact. Combined roles MUST be recorded, and required independent review MUST be identified where the applicable policy calls for it.
- **LIFECYCLE-02** When an incident is suspected, the responsible operator MUST follow a documented triage and escalation process that identifies impact-based escalation criteria, containment options, the incident decision-maker, required communications, and the minimum evidence to preserve under applicable data-handling rules.
- **LIFECYCLE-03** Before an affected agent or capability resumes after containment, the designated recovery authority MUST record the cause or remaining uncertainty, the corrective action, the evidence that applicable safeguards and release gates are satisfied, and the authorization to resume. If a material external effect remains unknown, the agent MUST NOT automatically retry an unsafe action.
- **LIFECYCLE-04** When operational feedback indicates a defect, harm, control failure, or recurring uncertainty, the owner MUST record its disposition and assign an accountable follow-up; where it reveals a material risk or behavior gap, the owner MUST link it to a corrective action, updated risk/evaluation evidence, or a documented retirement decision.
- **LIFECYCLE-05** For every production agent, the owner MUST set a proportionate periodic review cadence and reassess earlier when an incident or material change could invalidate its approved assumptions. The review MUST cover ownership and supportability, observed failure/feedback patterns, relevant dependencies and their status, capability and data changes, and whether existing controls and evidence remain fit for use.
- **LIFECYCLE-06** When an agent is deprecated or retired, the owner MUST stop new work, identify consumers and outstanding work, record whether that work is completed, cancelled, migrated, or handed off, revoke credentials and capability registrations that are no longer needed, dispose of data under applicable retention and sanitization policy, preserve required evidence, and mark the capability as retired in its inventory or manifest.

## Worked example: stale policy evidence

A fictional planning record for `POLICY-BUILD-001`, a read-only internal policy assistant; nothing was deployed, evaluated, or run. The companion [support, incident, and retirement record](../../templates/5.3/support-incident-and-retirement-record.yaml) holds the field-level status.

`employee-uk-104` may read `travel-policy-2026@2026-10-01` (London hotel limit GBP 220) and the approved historical `travel-policy-2024-superseded@2024-01-01` (GBP 200, not authority for the current answer). In `POLICY-STALE-002`, the expected outcome is `complete` with GBP 220; current evidence plus a superseded record is **not** a conflict.

A real conflict appears only in `POLICY-CONFLICT-004`, which adds the equally authoritative `travel-policy-2026-conflicting-amendment@2026-10-12` (GBP 260); the expected outcome is `needs_information`. `contractor-uk-204` has no travel-policy permission, and `POLICY-DENIED-005` expects `declined` without restricted facts. A missing permitted source expects `needs_information`. Controlled retrieval exhaustion expects terminal outcome `failed` with a useful uncertainty response; the termination reason (retrieval budget exhausted, then a controlled timeout) is recorded separately, as in [5.1](01-observability-budgets-and-operational-control.md#worked-example).

Suppose the support record receives an **illustrative hypothesis** that the stale case comes from incomplete source selection; no run, incident, or root cause is asserted. The fixture facts justify checking active source identities, the permission boundary, currentness classification, and authorized evidence; they do not justify saying the current source was unavailable, an index was stale, or a user received GBP 200.

If an investigation later showed unsafe source selection, the response would first contain: block that source-selection path for new requests, or stop more broadly if the safe scope were unclear. The repair would be a changed candidate needing evaluation evidence and a [5.2](02-readiness-change-and-rollout.md) release decision before the recovery authority could authorize resumption, with evaluation conclusion, release authorization, and operational outcome or reason in separate fields.

The hostile `untrusted-travel-note@2026-10-18` remains data. `POLICY-INJECTION-006` expects the legitimate GBP 220 response, no write invocation, and the attempted prohibited capability request recorded separately from the boundary denial. Whether the rejected instruction needs a visible refusal, escalation, or failure is the open [BOUNDARY-04](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md#requirements) refusal-scope question, not settled here.

Maintenance could record the source-refresh dependency, contactability, a suitable signal, and whether shared evaluation evidence fits the changed candidate. If the capability became unsupportable, a retirement proposal would cover the LIFECYCLE-06 elements before calling it retired.

## Evidence and checklist

A lifecycle record is proportionate when someone else can act on it without reconstructing undocumented decisions. For a production record, check that:

- [ ] Support roles are current, and combined roles and required independent review are visible.
- [ ] The triage record shows the signal, suspected scope, and the LIFECYCLE-02 elements.
- [ ] Hypotheses, fixture facts, observations, confirmed cause, evaluation conclusion, release authorization, terminal outcome, and termination reason are separate facts.
- [ ] A recovery decision has the LIFECYCLE-03 record; an unknown material external effect is not retried automatically.
- [ ] Feedback has a disposition and follow-up, with material gaps linked.
- [ ] Review cadence and triggers are recorded, and the review includes the model version's retirement date.
- [ ] Deprecation, disabling, and retirement are distinguished, and retirement covers every LIFECYCLE-06 element, including copy-specific data disposition.

## References

[1]: https://csrc.nist.gov/pubs/sp/800/61/r3/final "NIST SP 800-61 Rev. 3 Incident Response Recommendations and Considerations for Cybersecurity Risk Management"
[2]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"
[3]: https://csrc.nist.gov/pubs/sp/800/88/r2/final "NIST SP 800-88 Rev. 2 Guidelines for Media Sanitization"
[4]: https://www.cisa.gov/sites/default/files/publications/Incident-Response-Plan-Basics_508c.pdf "CISA Incident Response Plan Basics"
[5]: https://incidentdatabase.ai/about/ "AI Incident Database"
[6]: https://platform.claude.com/docs/en/about-claude/model-deprecations "Model deprecations"

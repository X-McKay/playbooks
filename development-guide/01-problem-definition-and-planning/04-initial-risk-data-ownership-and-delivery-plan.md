# 1.4 Initial Risk, Data, Ownership, and Delivery Plan

**Status:** 0.5.0-draft.2 — Part 1 refined draft; proposed, not adopted

**Audience:** Outcome and process owners, builders, operators, and reviewers who need to make a proposed system's constraints and accountability visible

**Applicability:** Every proposed production agent, including a read-only candidate, before implementation choices become difficult to change. The record is proportionate to the use, but a pilot label, absent evidence, or unresolved applicability does not remove an otherwise relevant question.

**Reader question:** What plausible harm, information, authority, ownership, and delivery constraints need to be understood before a proposed system is built, piloted, or expanded?

[Part 1 — Problem Definition and Planning](README.md) · [1.1 Defining the Problem](01-defining-the-problem.md) · [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) · [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md) · [Playbook applicability](../../applicability.md)

## Make constraints visible before they become expensive

The problem brief identifies the work to improve. The success record describes what acceptable behavior and evidence would mean. The alternatives record tests whether an agent is warranted. This chapter gathers the early constraints those records expose: who could be affected, what could go wrong, which information and authority are proposed, who can make or respond to each decision, and what a bounded first delivery would need.

An initial screen is not a risk score, a control test, an approval, or permission to run a pilot. It is a planning record that makes open questions difficult to overlook. A blank field means that a question is unresolved; it does not mean that the related use, data, or action is low risk or allowed.

NIST describes AI risk in terms of both likelihood and the negative consequence of an event, and notes that harm can be experienced by people, groups, communities, organizations, society, and systems beyond the direct user. It also cautions that difficulty measuring a risk is not evidence that the risk is high or low. [1] This chapter uses that framing to encourage a concrete, contextual early screen. It does not import NIST's framework as an adopted rule or replace the detailed assessment in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md).

## Terms and a working model

A **harm scenario** is a concise account of how a condition could lead to an unsafe output, action, or omission, and who or what could be affected. It is a plausible planning concern, not a prediction that the event will occur. An **affected non-user** is a person, group, or system that may feel a consequence even though it does not submit requests. A downstream decision-maker, a person whose information is disclosed, a policy owner, or a system that consumes an output can all be affected non-users.

**Uncertainty** is information that is missing, disputed, insufficiently supported, or not yet assessed. It is different from a favorable finding. A record can say `unresolved`, `not-yet-assessed`, or `evidence not yet available` rather than filling the gap with a low-risk label. This distinction is particularly useful when applicability of a legal, contractual, privacy, security, or domain rule still needs an authorized determination.

A **data source** supplies information. A **connection** is a route to a source, service, or action. An **access boundary** is the decision point that determines whether a requester, system, or operation may obtain or use information. Availability is not authority: a document that can be found, a connection that can be reached, or a field that appears in a response is not thereby permitted for the candidate, the requester, storage, diagnostics, or model processing.

**Authority** is the permission to perform a bounded operation in a particular context. **Approval** is an additional decision that may be required for an already authorized consequential action; it does not create authority. **Reversibility** describes whether an effect can be meaningfully corrected and what time, cost, or remaining impact correction leaves behind. A response can be read-only yet still be hard to correct after a person relies on it.

The draft's **execution class** describes how work executes: `ephemeral`, `durable`, or `human_governed`. **Governance tier** describes the assurance and oversight appropriate to a use. **Residual risk** is the risk that remains after controls whose effectiveness is supported by evidence. These are separate concepts. A durable, read-only task does not by itself require approval, and durable recovery does not establish exactly-once external effects. Conversely, an apparently read-only answer can have a consequential effect and require more assurance. Part 10 owns detailed scoring, floors, and acceptance of residual risk; Part 7 owns the execution concerns that apply to long-running, resumable, side-effecting, approval-waiting, or consequential work. [1]

A practical initial model is:

```text
intended and prohibited uses
  → affected users, non-users, systems, and concrete harm scenarios
  → proposed information, connections, authority, and reversibility
  → named decisions, reachable responsibilities, and dependencies
  → bounded pilot, support, containment, restart, and expansion questions
  → applicable reference parts and evidence handoffs
```

The arrows are planning relationships, not proof that a proposed control works or a launch is appropriate. NIST's MAP function similarly treats context, intended purpose, users, assumptions, and positive and negative impacts as inputs to an initial appropriateness decision, then calls for continuing that work as context, capability, risk, and impact evolve. [1]

## Screen harms proportionately

Start with the use boundary rather than an abstract label such as "low risk." Describe intended users and uses, explicit prohibited uses, and the people or systems that could be affected. Then write a small number of concrete scenarios for the material uncertainties. A useful prompt is:

> Because **[cause or initiating condition]**, the proposed system could **[unsafe output, action, or omission]**, causing **[plausible harm]** to **[affected person, group, system, or asset]**.

Causes can include ordinary mistakes, missing or conflicting input, misleading untrusted content, changed permissions, a stale or unavailable dependency, misuse, a misleadingly confident response, operator error, or a failed boundary. An omission matters as much as a wrong response when a person reasonably relies on a result that never arrives or hides material uncertainty.

For each scenario, make the likely path to recovery visible. Ask what could be undone, who could detect the issue, who would be affected before detection, and what remains after a correction. Reversibility is not a substitute for understanding impact: a message may be retractable while a decision made from it is not. A small, reversible trial can reduce exposure, but it cannot make prohibited use, missing evidence, or unresolved applicability disappear.

Do not give planned controls credit as if they were evidence. At this stage it is usually enough to identify a potential prevention, detection, or recovery question and hand it to the owner that will establish it. Part 4 supplies evidence design and interpretation; Part 3 addresses security, trust, and data boundaries; Part 5 addresses readiness, changes, and operating lifecycle. When the screen identifies consequential authority, sensitive or regulated context, broad reach, material uncertainty, a material human-impact scenario, or another relevant floor, use the detailed Part 10 method rather than inventing a local score. [1]

### Include people who do not operate the system

A direct requester is not the entire impact boundary. A policy owner may need to correct stale information. A support team may receive the consequences of poor escalation. A colleague, claimant, customer, or dependent service may make a decision from the output. NIST notes that potentially harmed communities need not be direct users and that effects can differ across groups and contexts. [1] This supports a qualified planning practice: list relevant affected non-users and downstream consumers where their exposure changes the harm, recovery, or evidence needed. It does not prescribe a universal impact-assessment method or population taxonomy.

## Record information and authority separately

An initial data record makes every proposed source or connection inspectable. It says why the candidate needs it, who owns it, what access boundary applies, whether sensitivity or personal-data concerns exist, how current and reliable it needs to be, and the intended model, retrieval, storage, and diagnostic handling. It also identifies dependencies such as source-status publication, requester permission decisions, escalation contacts, and any service used to deliver a result.

Start from purpose. For personal data within the UK GDPR's scope, the Information Commissioner's Office explains the data-minimisation principle as data being adequate, relevant, and limited to what is necessary for the stated purpose. It cautions against collecting data simply because it may be useful later. [3] That is jurisdiction-specific regulator guidance, not a universal legal conclusion for every record in this draft. As an engineering rule of thumb, a specific purpose makes it easier to challenge an unnecessary source, field, permission, diagnostic event, or retention assumption before it becomes normal practice.

For each source or connection, consider these distinctions:

- **Source ownership and status.** Identify who can explain content, source status, and change effects. A source can be approved yet superseded, current yet inaccessible to a requester, or accessible yet inappropriate for the stated purpose.
- **Access boundary and intended handling.** State whose permission is evaluated, where it is enforced, and what use is proposed after access is granted. Reading, sending to a model, indexing, storing, and retaining diagnostics are separate handling questions.
- **Freshness and reliability.** State the source state or update condition that matters to the task and the consequence of absence, staleness, conflict, corruption, or outage. Do not convert an unknown freshness property into an assumption of currentness.
- **Dependency and downstream effects.** Record the owner, relevant failure behavior, and change signal for material upstream dependencies. Record how a downstream person or process may rely on the output, what uncertainty it needs to see, and what recovery remains possible.

This is not a request to settle retention, redaction, deletion, audit, or access-control design in a short planning record. Those controls belong with the applicable owner, especially [Part 3.3 Data, Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md). The early screen should instead make it clear which of those questions are triggered and who needs to decide them.

### Make an authority and effect inventory

List a proposed capability by what it can do, the authority it would need, the externally visible effect it could cause, and its reversibility. A capability may be a read of protected material, a message, a record update, an approval request, a payment-related submission, or another state-changing operation. This inventory keeps a harmless-sounding label from concealing a more consequential effect.

Classify the required execution class from the actual execution and effect conditions, not from a preference for a simpler operational model. The class is not a governance-tier verdict. It does not establish whether the use is permitted, whether an approval is needed, or whether the relevant control chapters apply. For consequential external actions, retain the applicable human-governed approval and authorization question; a proposal, model output, or approval record cannot enlarge authority.

## Map responsibilities that a small team can carry

A responsibility map answers two different questions: **who decides**, and **who responds**. It need not create a large organization. One reachable person or staffed group may carry more than one responsibility, but the record should say when that happens so a reviewer can see the combined decision and response load.

A useful minimum map distinguishes:

- the **business owner** for the intended outcome, use boundary, and value question;
- the **technical owner** for the proposed behavior, data/capability record, and completeness of technical evidence; and
- the **operating owner** for support, incident response, containment, and the ability to stop the proposed system.

The record can also name the source or access owner, escalation contact, policy or specialist reviewer, release or risk-acceptance authority, containment authority, and restart decision authority where those decisions apply. A role title alone is not sufficient planning information: a reader needs a reachable person or staffed group, the decision it controls, and the response it can actually make. NIST's AI RMF includes documented roles, responsibilities, and communication lines as an accountability outcome. [2] That supports making responsibility and communication visible; it does not establish this chapter's three labels, require a particular team structure, or authorize anyone to accept risk or promote a release.

Keep containment and restart separate. An operating owner may be able to disable access or contain a problem quickly, while another authorized decision-maker determines whether conditions for restart have been met. Likewise, a person who proposes broader access does not self-create approval to grant it. Where policy requires independent review or a separate release or risk-acceptance authority, record that authority as required rather than assuming it exists or has been satisfied.

## Plan a bounded first delivery and its handoff

A pilot is a limited form of user exposure, not an exemption from applicable boundaries. Describe the eligible users, task classes, data, sources, capabilities, exclusions, and support path so another reader can tell what has and has not been tested. Entry evidence identifies what would need to be available before exposure; expansion evidence identifies what later would support a broader boundary. Neither field is evidence merely because it was written down.

Plan stop conditions in the same record. A stop condition can be a disclosure, unauthorized effect, a prohibited use, invalid source permission or currentness, a serious harm report, lost response coverage, a failed hard gate, or missing required evidence. Identify how the condition might be detected, who can contain the system, how affected users or operators are informed, and who may authorize a restart. A stop decision is not a failure of planning; it is a way to contain a known uncertainty while the applicable owner investigates.

The NIST AI RMF Playbook is explicit that its actions are voluntary suggestions, not a checklist or a sequence every organization must follow. [4] Treat the following as an adaptable builder workflow rather than a new gate:

1. **Re-open the boundary.** Bring forward the intended use, prohibited uses, affected parties, task variations, current process, and alternative decision from 1.1 through 1.3. Mark changed or still-unknown conditions.
2. **Write material scenarios.** Capture plausible error, omission, misuse, dependency, authority, and reversibility paths. Identify affected non-users and record uncertainty without scoring it locally.
3. **Inventory data, connections, and capabilities.** For each proposed item, connect purpose, ownership, access, sensitivity, freshness, intended handling, authority, effect, and recovery. Exclude items that cannot yet be justified by the bounded task.
4. **Make the decision map reachable.** Name business, technical, operating, source/access, containment, restart, and any required independent authorities. Record combined roles and unresolved reviewer questions.
5. **Bound the next exposure and hand off evidence.** Record potential pilot limits, support and stop/restart questions, applicable Parts, and evidence still needed. Let the owners of controls, evaluation, readiness, execution, and detailed risk decide their own questions.

The accompanying [initial scope record template](../../templates/1.4/initial-scope-record.yaml) is a neutral, illustrative planning aid. It is neither an implementation specification nor an authorization, and a populated record does not prove a control works.

## Requirements

The following proposed requirements are unchanged. They set the information that an initial record must make inspectable; the surrounding guidance does not add a risk score, pilot size, implementation, or local approval rule.

- **SCOPE-01** — For every proposed agent, the accountable owner MUST record intended and prohibited uses, affected people or systems, and plausible material harms before implementation choices are treated as settled; where a use may be prohibited or regulated, applicability MUST remain unresolved until an authorized reviewer determines it.
- **SCOPE-02** — For every data source or connection proposed for an agent, the technical owner MUST record its purpose, source owner, access boundary, sensitivity or personal-data concerns, freshness/reliability needs, and intended model, retrieval, storage, and diagnostic handling; access or information use MUST NOT be assumed from availability alone.
- **SCOPE-03** — For every enabled capability, the technical owner MUST record its permitted authority, externally visible effects, and reversibility, and MUST identify the required execution class; an effective configuration MUST NOT silently use a weaker class than its capabilities require. Consequential external actions MUST follow the applicable human-governed approval and authorization rules.
- **SCOPE-04** — Before a user pilot or production use, each agent MUST have named, reachable business, technical, and operating ownership, with decision authority, response responsibilities, and any combined roles recorded; any required independent review or release/risk acceptance authority MUST be identified rather than self-assumed.
- **SCOPE-05** — Before a pilot, the accountable owner MUST record its eligible users, task/data/capability limits, entry and expansion evidence, support, and stop conditions, including who can contain the agent and who can authorize restart. A failed hard gate, prohibited use, or missing required evidence MUST NOT be converted into a pass by narrowing the pilot label or by an average score.

## Worked example: fictional internal policy assistance

The shared planning record `POLICY-PLAN-001` considers `internal-policy-assistance`. It is **fictional and unexecuted**, with status `illustrative-unexecuted`. The candidate is permission-filtered, read-only help with internal policy questions. It has no write or approval capability. The example does not determine a governance tier, residual risk, legal applicability, pilot authorization, release decision, observed control result, or delivered user benefit.

The intended use is to help an eligible requester obtain a source-grounded policy answer or a clear next step when evidence is missing or conflicts. The prohibited boundary includes changing employee records, approving spending, deciding reimbursement eligibility, and disclosing material the requester may not access. In the controlled `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` is a current approved source that states a London hotel limit of GBP 220. `travel-policy-2024-superseded@2024-01-01` is historical and differs. These are fixture facts, not policy facts or candidate results.

One planned scenario is that a response relies on the superseded source or hides a conflict between equally authoritative current permitted sources. The potential harm is that a requester makes a poor travel or claim-related decision and the policy owner must correct it later. Another scenario is disclosure to `contractor-uk-204`, who is not permitted to read the named policy documents in the fixture. Those are plausible scenario statements, not measured likelihoods or findings. The record also lists the policy owner and the requester-permission decision as dependencies, and leaves the relevant specialist-review questions unresolved rather than assuming that read-only access makes the use low risk.

The source map distinguishes the current source from the superseded source and untrusted travel note. A current, approved source is not automatically accessible to every requester; a requester permission decision remains necessary. The plan proposes no writing, no approval, and no use of untrusted content as authority. It records that model, retrieval, storage, and diagnostic handling need separate decisions under the applicable data and security controls. No execution class is inferred solely from the read-only description, and no durable operation or approval is assumed.

The roles in the fictional record remain placeholders. A business owner would own the user-task and intended-outcome question; a technical owner would own the source, capability, and evidence record; and an operating owner would need to be able to respond to user reports and contain the candidate. A source/access owner, any required specialist reviewer, and the restart decision authority are not yet named. That is an honest planning state, not permission to expose users.

A later bounded pilot could limit exposure to the eligible fictional requester context, approved current requester-permitted sources, and read-only policy questions. It would exclude record changes, spending decisions, unapproved or restricted sources, and unresolved policy conflicts. The plan treats permission denials, missing or conflicting current evidence, source-status changes, a disclosure report, unavailable response coverage, or missing required evidence as conditions needing containment or escalation. The applicable authority would decide a restart after investigation; no result in this example says those conditions have been tested or met. Part 4 designs evidence, Part 5 decides readiness and rollout, and Part 10 handles any triggered detailed assessment.

## Evidence and handoff

An initial scope record is ready to inform later work when a responsible reader can find the proposed boundary, plausible harms, data and capability inventory, accountable people, open applicability questions, and planned delivery constraints without mistaking them for evidence. It is planning evidence, not evidence that a candidate is safe, useful, permitted, or ready.

Before handing the record to the next owner, check that it makes the following visible:

- intended and prohibited uses, affected direct users and non-users, material scenarios, uncertainty, and any unresolved applicability question;
- each proposed source or connection's purpose, owner, access boundary, sensitivity or personal-data concern, freshness/reliability need, and intended handling;
- each capability's authority, externally visible effect, reversibility, and execution-class question, without treating a read-only or durable label as a risk, approval, or authority conclusion;
- reachable business, technical, and operating owners, plus combined roles, containment, restart, source/access, and required independent or acceptance authorities where relevant;
- a bounded potential pilot, including eligible users and limits, future entry/expansion evidence, support path, stop conditions, containment, and restart questions; and
- the relevant control and evidence handoffs: Part 3 for trust and data boundaries, Part 4 for evidence design and interpretation, Part 5 for readiness and rollout, Part 7 for triggered execution concerns, and Part 10 for expanded assessment.

A later change in users, affected population, source status, permissions, capability, authority, dependency, execution condition, or delivery boundary reopens the record. A completed checklist item still does not authorize launch; the applicable owner chapters and authorized decision-makers determine controls, evidence, and any later decision.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ "Artificial Intelligence Risk Management Framework Core"
[3]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ "Principle c Data minimisation"
[4]: https://airc.nist.gov/airmf-resources/playbook/ "Artificial Intelligence Risk Management Framework Playbook"

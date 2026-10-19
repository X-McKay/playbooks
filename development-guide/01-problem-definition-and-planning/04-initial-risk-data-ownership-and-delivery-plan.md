# 1.4 Initial Risk, Data, Ownership, and Delivery Plan

**Status:** 0.5.0-draft.2 — draft

**Audience:** Outcome and process owners, builders, operators, and reviewers who need to make a system's constraints and accountability visible

**Applicability:** Every proposed production agent, including a read-only one, before implementation choices become hard to change. Keep the record proportionate, but a pilot label, missing evidence or unresolved applicability does not remove a relevant question.

**Reader question:** What plausible harm, information, authority, ownership and delivery constraints must be understood before the system is built, piloted or expanded?

[Part 1 — Problem Definition and Planning](README.md) · [1.1 Defining the Problem](01-defining-the-problem.md) · [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) · [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md) · [Playbook applicability](../../applicability.md)

## Make constraints visible before they become expensive

This chapter gathers the early constraints the first three records expose: who could be affected, what could go wrong, which information and authority are proposed, who decides and who responds, and what a bounded first delivery needs.

An initial screen is not a risk score, control test, approval, or permission to pilot. It makes open questions hard to overlook. A blank field means the question is unresolved, not that the data or action is low risk or allowed.

NIST describes AI risk as both the likelihood and the negative consequence of an event, notes that harm can fall on people, groups, communities, organizations, society and systems beyond the direct user, and cautions that difficulty measuring a risk is not evidence that it is high or low. [1] Use it for a concrete early screen. Detailed assessment is in [Part 10](../../engineering-reference/10-risk-privacy-and-specialized-assurance/README.md). NIST has said the AI RMF 1.0 is being updated, so check the current version when you use it. [4]

## Terms and a working model

A **harm scenario** is a short account of how a condition could lead to an unsafe output, action or omission, and who or what is affected. An **affected non-user** is a person, group or system that may feel a consequence without submitting requests: a downstream decision-maker, a person whose information is disclosed, a policy owner, or a system that consumes an output.

**Uncertainty** is information that is missing, disputed, poorly supported or not yet assessed. It is not a favorable finding. Write `unresolved`, `not-yet-assessed` or `evidence not yet available` instead of filling the gap with a low-risk label. This matters most when applicability of a legal, contractual, privacy, security or domain rule still needs an authorized determination.

A **data source** supplies information. A **connection** is a route to a source, service or action. An **access boundary** is the decision point that determines whether a requester, system or operation may obtain or use information. Availability is not authority: a document that can be found, a connection that can be reached, or a field that appears in a response is not thereby permitted for the candidate, the requester, storage, diagnostics or model processing.

**Authority** is permission to perform a bounded operation in a context. **Approval** is an additional decision that may be needed for an already authorized consequential action; it does not create authority. **Reversibility** is whether an effect can be meaningfully corrected and what time, cost or impact remains. A read-only response can still be hard to correct once someone relies on it.

The **execution class** describes how work executes: `ephemeral`, `durable` or `human_governed`. **Governance tier** is the assurance and oversight appropriate to a use. **Residual risk** is what remains after controls whose effectiveness has evidence. These are separate. A durable, read-only task does not by itself need approval, and durable recovery does not give exactly-once external effects. An apparently read-only answer can have consequential effects and need more assurance. Part 10 owns detailed scoring, floors and acceptance of residual risk; Part 7 owns execution concerns for long-running, resumable, side-effecting, approval-waiting or consequential work.

```text
intended and prohibited uses
  → affected users, non-users, systems, and concrete harm scenarios
  → proposed information, connections, authority, and reversibility
  → named decisions, reachable responsibilities, and dependencies
  → bounded pilot, support, containment, restart, and expansion questions
  → applicable reference parts and evidence handoffs
```

NIST's MAP function establishes the context used to frame risks (intended purpose, users, assumptions and impacts), and its outcomes are the basis for MEASURE and MANAGE. [1]

## Screen harms proportionately

Start from the use boundary, not a label such as "low risk." Describe intended users and uses, explicit prohibited uses, and who or what could be affected. Then write a few concrete scenarios for the material uncertainties, using this prompt:

> Because **[cause or initiating condition]**, the proposed system could **[unsafe output, action, or omission]**, causing **[plausible harm]** to **[affected person, group, system, or asset]**.

Causes include mistakes, missing or conflicting input, misleading untrusted content, changed permissions, a stale or unavailable dependency, misuse, a confidently wrong response, operator error, or a failed boundary. An omission matters as much as a wrong answer when someone relies on a result that never arrives or hides uncertainty.

For each scenario, make recovery visible: what could be undone, who could detect the issue, who is affected before detection, and what remains after correction. Reversibility does not replace understanding impact: a message may be retractable while a decision made from it is not. A small trial reduces exposure but cannot make prohibited use, missing evidence or unresolved applicability go away.

Do not credit planned controls as evidence. Identify the prevention, detection or recovery question and hand it to its owner: Part 4 for evidence, Part 3 for trust and data boundaries, Part 5 for readiness and operation. When the screen finds consequential authority, sensitive or regulated context, broad reach, material uncertainty, a material human-impact scenario or another floor, use the Part 10 method instead of inventing a local score.

### Include people who do not operate the system

The requester is not the whole impact boundary. A policy owner may have to correct stale information, a support team inherits poor escalation, and a colleague, claimant, customer or dependent service may act on the output. NIST notes that harmed communities need not be direct users and that effects differ across groups and contexts. [1] List affected non-users and downstream consumers where their exposure changes the harm, the recovery or the evidence needed.

## Record information and authority separately

An initial data record makes every proposed source or connection inspectable: why the candidate needs it, who owns it, the access boundary, sensitivity or personal-data concerns, how current and reliable it must be, and the intended model, retrieval, storage and diagnostic handling. It also names dependencies such as source-status publication, requester permission decisions, escalation contacts, and any service used to deliver a result.

Start from purpose. For personal data under the UK GDPR, the Information Commissioner's Office explains data minimisation as data that is adequate, relevant and limited to what is necessary for the stated purpose, and warns against collecting data just because it may be useful later. [3] That guidance is jurisdiction-specific and under review at the time of writing. As a general engineering habit, a specific purpose makes it easier to challenge an unneeded source, field, permission, diagnostic event or retention assumption early.

Check early whether the use needs a **regulatory applicability screen**. Where personal data is likely to be processed in a way that is high-risk to individuals, UK GDPR Article 35 requires a data protection impact assessment before processing starts, and the ICO guide explains when. [5] If the system serves people in the EU, check whether the EU AI Act applies and which of its obligations apply when; its application dates have been under revision, so confirm current status from the official text and an authoritative source. [6] This is a pointer, not legal advice. Under SCOPE-01, applicability stays unresolved until an authorized reviewer decides it.

For each source or connection, consider:

- **Source ownership and status.** Who can explain content, source status and changes? A source can be approved yet superseded, current yet inaccessible to a requester, or accessible yet wrong for the stated purpose.
- **Access boundary and intended handling.** Whose permission is checked, where it is enforced, and what use follows. Reading, sending to a model, indexing, storing and retaining diagnostics are separate handling questions.
- **Freshness and reliability.** Which source state or update condition matters, and what happens if it is absent, stale, in conflict, corrupt or down. Do not assume currentness you have not established.
- **Dependency and downstream effects.** The owner, failure behavior and change signal for material upstream dependencies. How a downstream person or process relies on the output, what uncertainty it must see, and what recovery remains.

Do not settle retention, redaction, deletion, audit or access-control design here; see [Part 3.3 Data, Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md). The screen only shows which of those questions are triggered and who decides them.

### Make an authority and effect inventory

List each proposed capability by what it can do, the authority it needs, the externally visible effect it could cause, and its reversibility. A capability may be a read of protected material, a message, a record update, an approval request, a payment-related submission or another state change. This keeps a harmless-sounding label from hiding a consequential effect.

Choose the execution class from the actual execution and effect conditions, not a preference for a simpler operating model. The class is not a governance-tier verdict and does not decide whether the use is permitted or approval is needed. For consequential external actions, keep the human-governed approval and authorization question; a proposal, model output or approval record cannot enlarge authority.

## Map responsibilities that a small team can carry

A responsibility map answers **who decides** and **who responds**. One reachable person or staffed group may hold several responsibilities, but say so. At minimum, name:

- the **business owner** for the intended outcome, use boundary and value question;
- the **technical owner** for the proposed behavior, the data and capability record, and technical evidence; and
- the **operating owner** for support, incident response, containment and the ability to stop the system.

Also name, where those decisions apply, the source or access owner, escalation contact, policy or specialist reviewer, release or risk-acceptance authority, containment authority and restart authority. A role title is not enough: a reader needs a reachable person or staffed group, the decision it controls, and the response it can actually make. NIST's AI RMF lists documented roles, responsibilities and lines of communication as an accountability outcome. [2]

Keep containment and restart separate. An operating owner may be able to switch off access quickly, while another authorized decision-maker decides whether restart conditions are met. Someone proposing broader access does not approve it themselves. Where policy requires independent review or a separate release or risk-acceptance authority, record it as required instead of assuming it exists or is satisfied.

## Plan a bounded first delivery and its handoff

A pilot is limited user exposure, not an exemption from applicable boundaries. Describe eligible users, task classes, data, sources, capabilities, exclusions and the support path. Entry evidence says what must exist before exposure; expansion evidence says what would support a wider boundary. Writing either down is not evidence.

Plan stop conditions in the same record: a disclosure, unauthorized effect, prohibited use, invalid source permission or currentness, serious harm report, lost response coverage, failed hard gate, or missing required evidence. Say how each would be detected, who can contain the system, how affected users or operators are told, and who may authorize restart.

The NIST Playbook says its actions are voluntary suggestions, not a checklist or a sequence to follow in full. [4] Treat this as an adaptable workflow, not a new gate:

1. **Re-open the boundary.** Bring forward intended and prohibited uses, affected parties, task variations, current process and the alternatives decision from 1.1 to 1.3. Mark what has changed or is still unknown.
2. **Write material scenarios.** Capture plausible error, omission, misuse, dependency, authority and reversibility paths. Identify affected non-users and record uncertainty without scoring it locally.
3. **Inventory data, connections and capabilities.** For each, connect purpose, ownership, access, sensitivity, freshness, handling, authority, effect and recovery. Drop items the bounded task cannot yet justify.
4. **Make the decision map reachable.** Name business, technical, operating, source/access, containment, restart and any required independent authorities. Record combined roles and open reviewer questions.
5. **Bound the next exposure and hand off evidence.** Record pilot limits, support and stop/restart questions, applicable Parts and evidence still needed. Let the owners of controls, evaluation, readiness, execution and detailed risk decide their own questions.

Common pitfalls at this stage:

- **No baseline for harm.** Nobody records what goes wrong in today's process, so the agent's new failures cannot be compared with existing ones.
- **One blended risk score.** A single "low" rating hides separate questions about data, authority, reversibility and affected non-users. Keep them separate.
- **"Read-only" treated as safe.** A read can leak data or mislead a decision. Check what the output enables.
- **Scope creep after the pilot.** A successful narrow pilot becomes a reason to add users, sources or write actions with no new screen. Any widening reopens this record.

The [initial scope record template](../../templates/1.4/initial-scope-record.yaml) shows these fields; a filled record does not prove a control works.

## Requirements

- **SCOPE-01** — For every proposed agent, the accountable owner MUST record intended and prohibited uses, affected people or systems, and plausible material harms before implementation choices are treated as settled; where a use may be prohibited or regulated, applicability MUST remain unresolved until an authorized reviewer determines it.
- **SCOPE-02** — For every data source or connection proposed for an agent, the technical owner MUST record its purpose, source owner, access boundary, sensitivity or personal-data concerns, freshness/reliability needs, and intended model, retrieval, storage, and diagnostic handling; access or information use MUST NOT be assumed from availability alone.
- **SCOPE-03** — For every enabled capability, the technical owner MUST record its permitted authority, externally visible effects, and reversibility, and MUST identify the required execution class; an effective configuration MUST NOT silently use a weaker class than its capabilities require. Consequential external actions MUST follow the applicable human-governed approval and authorization rules.
- **SCOPE-04** — Before a user pilot or production use, each agent MUST have named, reachable business, technical, and operating ownership, with decision authority, response responsibilities, and any combined roles recorded; any required independent review or release/risk acceptance authority MUST be identified rather than self-assumed.
- **SCOPE-05** — Before a pilot, the accountable owner MUST record its eligible users, task/data/capability limits, entry and expansion evidence, support, and stop conditions, including who can contain the agent and who can authorize restart. A failed hard gate, prohibited use, or missing required evidence MUST NOT be converted into a pass by narrowing the pilot label or by an average score.

## Worked example: fictional internal policy assistance

The planning record `POLICY-PLAN-001` is fictional and unexecuted (`illustrative-unexecuted`). It covers `internal-policy-assistance`: permission-filtered, read-only help with internal policy questions, with no write or approval capability. It sets no governance tier, residual risk, legal applicability or pilot authorization.

The intended use is to help an eligible requester get a source-grounded policy answer, or a clear next step when evidence is missing or conflicts. Prohibited: changing employee records, approving spending, deciding reimbursement eligibility, and disclosing material the requester may not access. In the `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` is a current approved source stating a London hotel limit of GBP 220, and `travel-policy-2024-superseded@2024-01-01` is historical and differs.

One scenario: a response relies on the superseded source, or hides a conflict between equally authoritative current permitted sources. The harm is a poor travel or claim decision that the policy owner must later correct. Another: disclosure to `contractor-uk-204`, who may not read the named policy documents. These are scenarios, not measured likelihoods. The policy owner and the requester-permission decision are listed as dependencies, and specialist-review questions stay open instead of assuming read-only access means low risk.

The source map separates the current source, the superseded source and an untrusted travel note. A current approved source is not automatically open to every requester; a permission decision is still needed. The plan proposes no writing, no approval, and no use of untrusted content as authority. Model, retrieval, storage and diagnostic handling need separate decisions under the data and security controls. No execution class is inferred from "read-only," and no durable operation or approval is assumed.

Roles are placeholders: a business owner for the outcome, a technical owner for the source, capability and evidence record, and an operating owner who can respond to reports and contain the candidate. The source/access owner, any specialist reviewer and the restart authority are not yet named, so users must not yet be exposed.

A later bounded pilot could limit exposure to the eligible fictional requester context, approved current requester-permitted sources, and read-only policy questions, and exclude record changes, spending decisions, restricted sources and unresolved policy conflicts. Permission denials, missing or conflicting current evidence, source-status changes, a disclosure report, lost response coverage or missing required evidence would call for containment or escalation, with restart decided by the authority after investigation. Nothing here says those conditions were tested. Later Parts handle evidence, readiness and any triggered assessment.

## Evidence and handoff

An initial scope record is ready for later work when a reader can find the proposed boundary, plausible harms, data and capability inventory, accountable people, open applicability questions and delivery constraints without mistaking them for evidence. It is not evidence that the candidate is safe, useful, permitted or ready. Before handing it on, check that it shows:

- intended and prohibited uses, affected users and non-users, material scenarios, uncertainty, and any unresolved applicability question, including whether a data protection impact assessment or other regulatory screen is needed;
- each source or connection's purpose, owner, access boundary, sensitivity or personal-data concern, freshness/reliability need and intended handling;
- each capability's authority, externally visible effect, reversibility and execution-class question, without treating a read-only or durable label as a risk, approval or authority conclusion;
- reachable business, technical and operating owners, plus combined roles, containment, restart, source/access and required independent or acceptance authorities;
- a bounded potential pilot: eligible users and limits, entry and expansion evidence, support path, stop conditions, containment and restart; and
- the handoffs: Part 3 for trust and data boundaries, Part 4 for evidence, Part 5 for readiness and rollout, Part 7 for triggered execution concerns, Part 10 for expanded assessment.

A change in users, affected population, source status, permissions, capability, authority, dependency, execution condition or delivery boundary reopens the record. A completed checklist does not authorize launch.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ "Artificial Intelligence Risk Management Framework Core"
[3]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/ "Principle c Data minimisation"
[4]: https://airc.nist.gov/airmf-resources/playbook/ "Artificial Intelligence Risk Management Framework Playbook"
[5]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/ "Data protection impact assessments (DPIAs)"
[6]: https://eur-lex.europa.eu/eli/reg/2024/1689/oj "Regulation (EU) 2024/1689 (Artificial Intelligence Act)"

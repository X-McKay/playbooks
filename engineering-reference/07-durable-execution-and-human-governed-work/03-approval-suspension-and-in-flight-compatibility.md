# 7.3 Approval, Suspension, and In-Flight Compatibility

**Status:** 0.5.0-draft.2 — draft
**Audience:** Builders of durable or human-governed work, security reviewers, operators and accountable owners.
**Applicability:** Use when a durable run waits for a human decision before a consequential action, and when a change could meet persisted work created by an earlier version. Do not add approval or durable state to an ephemeral, read-only assistant because of this chapter.

[Part 7 — Durable Execution and Human-Governed Work](README.md) · [Playbook applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.2 Side Effects, Idempotency, and Unknown Outcomes](02-side-effects-idempotency-and-unknown-outcomes.md)

## Purpose and applicability

A human approval decides one defined action, in one material context, for a limited time. Without that binding, a response to an earlier proposal can be applied after the target, tenant, arguments, policy or authority changed, and durable runs suspend for hours, change workers, receive events twice or meet a new build first.

Consequence and policy decide whether approval is needed: the read-only policy assistant needs none, its durable update variant does. NIST's AI Risk Management Framework calls for defining and differentiating roles and responsibilities for human-AI configurations and oversight (GOVERN 3.2; MAP 3.5).[1]

Chapter 3.1 covers who may approve and 7.2 the effect itself. This chapter covers what was approved, which events change a waiting run, when a decision stops authorizing, and how active work survives a change.

## Working model

### Bind a decision to an approval subject

An approval request needs a stable identity and an immutable **approval subject**, the canonical description the reviewer sees and execution later compares:

- the approval request and durable workflow-chain identities;
- the action name and version, canonical arguments or their digest, and the target;
- the tenant and effective actor whose authority is used;
- the policy version, required approver scope, and policy-defined material context such as data classification or impact category; and
- the request and expiry times.

The approval ID names a decision; the request ID names what awaits it, so a decision cannot apply to another wait; an event ID names one message, so duplicates are harmless.

Define argument ordering, normalization and typing before digesting, but keep a readable subject, not only a digest. Any material change voids the approval and needs a new request.

### Suspend and resume as state transitions

Before waiting, the run records `awaiting_approval`, its subject, an expiry deadline and processed event IDs. Each authenticated approval, rejection, cancellation or timeout requests a transition, saved before any move toward an effect. Expiry comes from a durable timer or recorded deadline, never a local clock, instruction or model response. A valid approval moves the run to approved-but-not-yet-executed, so cancellation can still stop work before execution is claimed.

Policy, not arrival order, sets the race rule. A safe default: cancellation recorded before execution is durably claimed prevents the effect even if approval came first; after the claim it stops remaining work but cannot undo a completed or unknown effect (7.2 applies). A decision after expiry, cancellation, rejection or completion is a late event, recorded with its disposition, not new authority.

Recovery resumes from persisted state, not an agent plan, and rechecks the stored subject; nothing the agent says or retrieves widens it.

### Authorize at the moment of effect

Approval says a human accepted this bound proposal; authorization says this execution may act on this target for this tenant now. A consequential effect needs both, so immediately before it, check target, tenant, effective actor, capability and any policy condition that may have changed. A revoked role, removed capability, changed tenant relation or invalidated policy means non-execution or fresh approval, never inherited permission; a changed action needs a new subject.

### Keep old persisted work interpretable

Persisted state is an interface between versions, so every approval-wait payload, durable-step input and material event carries a schema ID and version:

```yaml
persisted_state:
  state_type: awaiting_approval
  schema_id: durable.approval.wait
  schema_version: 1
  approval_request_id: ar-0042
  subject_digest: sha256:<canonical-subject-digest>
  expires_at: <recorded-deadline>
```

It holds a digest, not a sensitive payload (data handling per Chapter 3.3). A reader may supply a documented, meaning-preserving default for a new optional field; changing a transition, subject, authorization condition, action meaning or the reading of a missing field is incompatible. Before going live, test one path: a compatible handler, version routing, or validated migration with fallback. Never invent a value that lets an old approval authorize a different action. This covers active timers, retries and approvals; replaying recorded histories against changed code is a documented pre-deployment check.[2]

## Decisions and best practices

- **Make the human role concrete:** action category, approver scope, context shown, expiry window and whether a cancelled request can reopen. Do not gate routine acknowledgements, or call a consequential action a retry to avoid a gate.
- **Use a small, closed set of outcomes:** at least waiting, rejected, expired, cancelled before effect, effect resolution in progress, completed, and unresolved or partially effective. Meanings and allowed transitions are stable; each transition records prior state, event ID, decision time, policy version and result, not a reasoning trace.
- **Cancellation is a request to stop, not proof of reversal.** Define who can cancel and what happens before the claim, during execution and after. Duplicate and delayed events get an idempotent state decision, not a second attempt.
- **Plan rollouts around active work:** runnable versions including waiting approvals, handler retirement, migration or escalation of incompatible items, and tested histories (see 5.2). Shift new work gradually, let old versions finish, and resume from checkpoints rather than restart.[5]

### Design approval for the human who has to give it

People who approve many requests stop reading. Research finds complacency (monitoring automated output less) and automation bias (following wrong recommendations, missing unflagged problems), which training does not reliably prevent.[3] A gate always clicked through protects nothing.

- Ask for approval only where the governance tier justifies it; gates on routine actions teach people to ignore gates.
- Rate each tool low, medium or high by read or write, reversibility, permissions and financial impact, and let the rating decide which calls need a person; also hand off when a retry or failure limit is exceeded.[4]
- Show the exact change (diff, target, tenant, amount or count, reversibility) and the evidence and uncertainty beside it; do not pre-select "approve" or lead with the recommendation.
- Track approval rate, decision time and edit or reject rate; near-100 percent approval with very short decisions suggests the gate is not working.
- Review a sample of approved actions, and seed test proposals with known defects to check approvers catch them.

## Requirements

- **APPROVAL-01 — Bound approval subject.** When an applicable policy requires a human approval before a consequential action, the durable run **MUST** create a stable approval-request identity and persist an immutable subject containing the action, canonical arguments or digest, target, tenant, effective actor, policy version, required approver scope, material context, and expiry. It **MUST** accept a decision only when it matches that subject and is from an authenticated approver with the required scope. A material change **MUST** invalidate the request and require a new approval. **Applies to:** human-governed consequential actions.

- **APPROVAL-02 — Event identity and durable transition.** A waiting run **MUST** persist its awaiting state, expiry, and processed-event identity before it waits, and **MUST** record the outcome of each accepted, duplicate, mismatched, or late event before resuming execution. It **MUST NOT** allow a duplicate delivery of an approval or resume event to produce another external-effect attempt. **Applies to:** any durable approval wait or externally delivered cancellation/decision.

- **APPROVAL-03 — Expiry, cancellation, and late events.** The approval policy **MUST** define and the implementation **MUST** enforce a deterministic precedence rule for approval, rejection, expiry, cancellation, and execution claim. At a minimum, a decision after recorded expiry, cancellation, rejection, or completion **MUST NOT** authorize execution; cancellation recorded before execution is claimed **MUST** prevent the new effect; and cancellation after the claim **MUST** enter the applicable interruption, reconciliation, or compensation path rather than assert reversal. **Applies to:** human-governed consequential actions.

- **APPROVAL-04 — Execution-time authorization.** After accepting approval and immediately before a consequential effect, the execution step **MUST** enforce current authorization for the target, tenant, effective actor, and capability. An approval **MUST NOT** create new authority or override a changed authorization decision. If a material change is needed, the run **MUST** request approval for the changed subject. **Applies to:** an approved action with an external effect.

- **APPROVAL-05 — Persisted compatibility.** A durable system **MUST** store a schema identity and version for persisted approval state, material events, and inputs needed to resume work. Before a deployment that can encounter active earlier state, the owner **MUST** document and test a compatible-reader, version-routing, or validated-migration path for each affected version. It **MUST NOT** reinterpret an old payload or approval in a way that changes its authorization meaning. **Applies to:** durable deployments with active, resumable, or retained work.

- **APPROVAL-06 — Decision evidence.** The owner **SHOULD** retain a reviewable approval subject, authenticated decision/event identities and dispositions, state-transition record, authorization result at execution, effect-resolution record, and compatibility-test evidence for the retention period selected under Chapter 3.3. **Applies to:** human-governed work and deployments that alter active durable state.

## Worked example

A separate durable flow of the policy assistant runs when an authorized editor asks for an update. In this fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220 and a superseded document differs. The editor proposes GBP 230; publishing requires a human decision.

Request `ar-0042` shows the approver the action, current source and patch; the subject includes `publish_policy_revision`, the canonical patch digest, the `travel-policy-current` target, the policy workspace tenant, the editor as effective actor, the approval-policy version, required approver scope and expiry. The flow enters `awaiting_approval`, and the answer-generation agent cannot swap in a new patch.

If the approver approves `ar-0042` but the editor withdraws the proposal before execution is claimed, the cancellation is recorded and the run becomes `cancelled_without_effect`. The late approval is kept as a non-authorizing event, as is any duplicate, and nothing is published.

A deployment adds an optional display-only field while another instance waits; the reader recognizes the older `durable.approval.wait` version and keeps its subject meaning. Had it changed patch interpretation or added a material condition, it would keep an old handler or migrate, voiding and reissuing affected approvals.

On a valid approval, the flow compares the rebuilt proposal with the stored subject and, just before publishing, checks that the editor still has the permitted workspace relationship and the action is allowed, else records non-execution. A lost publication receipt is reconciled per 7.2; a duplicate approval never triggers resubmission.

## Evidence and checklist

Keep the approval policy, subject definition and transition specification (states, triggers, precedence, deadlines, outcomes) with the durable contract, and the compatibility decision with the release material.

Using a controlled clock and authoritative effect state ([4.5](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md)), show that:

- an exact approval resumes once; any material change does not;
- rejection, expiry, pre-claim cancellation and late approvals create no effect;
- both orders of an approval-cancellation race follow the precedence rule;
- withdrawn authorization prevents the action, and post-claim cancellation enters the 7.2 path;
- old waiting states, timers, decisions and retries keep their approval meaning; and
- approvers catch seeded defects, and approval rate and decision times show real review.

Attach results to [4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md) evidence, and carry supported versions, the migration or routing decision and retirement conditions into [5.2](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework AI RMF 1.0"
[2]: https://docs.temporal.io/develop/safe-deployments "Temporal safely deploying changes to Workflow code"
[3]: https://journals.sagepub.com/doi/10.1177/0018720810376055 "Complacency and Bias in Human Use of Automation: An Attentional Integration"
[4]: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ "A practical guide to building agents"
[5]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"

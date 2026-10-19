# 7.3 Approval, Suspension, and In-Flight Compatibility

**Status:** 0.5.0-draft.2 — draft
**Audience:** Builders of durable or human-governed work, security reviewers, operators and accountable owners.
**Applicability:** Use when a durable run waits for a human decision before a consequential action, and when a change could meet persisted work created by an earlier version. Do not add approval or durable state to an ephemeral, read-only assistant because of this chapter.

[Part 7 — Durable Execution and Human-Governed Work](README.md) · [Playbook applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.2 Side Effects, Idempotency, and Unknown Outcomes](02-side-effects-idempotency-and-unknown-outcomes.md)

## Purpose and applicability

A human approval is not a general endorsement of an agent. It is a decision about one defined action, in one material context, for a limited time. Without that binding, a response meant for an earlier proposal can be applied after the target, tenant, arguments, policy or authority has changed. A durable run makes this worse: it may suspend for hours, resume on another worker, receive the same event twice, or meet a new build before the decision arrives.

The action's consequence and the applicable policy decide whether approval is needed. The read-only policy assistant does not need this chapter to return a cited answer. Its durable variant does, once it prepares and applies a human-approved policy update. NIST's AI Risk Management Framework calls for defining and differentiating the roles and responsibilities for human-AI configurations and oversight (GOVERN 3.2; MAP 3.5).[1]

Chapter 3.1 covers identity, least privilege and who may approve. This chapter covers state once policy requires an approval: what was approved, which event changes a waiting run, when a decision stops authorizing work, and how active work survives a change. Chapter 7.2 covers the external effect itself, including reconciliation when the receipt is lost.

## Working model

### Bind a decision to an approval subject

An approval request needs a stable identity and an immutable **approval subject**: the canonical description that a reviewer sees and that the execution path later compares. It identifies:

- the approval request and durable workflow-chain identities;
- the action name and version, canonical arguments or their digest, and the target;
- the tenant and effective actor whose authority is used;
- the policy version, required approver scope, and any policy-defined material context, such as a data classification or impact category; and
- the request time and expiry time.

Three IDs do different jobs. The approval ID identifies a decision. The request ID identifies what awaits a decision, so a valid decision cannot be applied to another wait. A delivery or decision-event ID identifies one message, so duplicate delivery is visible and harmless.

Define how arguments are ordered, normalized and typed before computing a digest. Do not reduce the subject to a digest alone: the stored subject must let a reviewer understand the target and intended action. If any policy-defined material field changes, the earlier approval is void and the run creates a new request.

### Suspend and resume as state transitions

A waiting run has an explicit durable state. Before it waits, it records `awaiting_approval`, its subject, an expiry deadline and the IDs of events already processed. An authenticated approval, rejection, cancellation or timeout then requests a transition. Save the transition decision before moving toward an external effect.

Use a durable timer or recorded deadline to decide expiry. A restarted process must not treat an expired request as current because a local clock, an instruction or a model response says to continue. A valid approval normally moves the run to approved-but-not-yet-executed. That gap lets a cancellation stop work before the execution attempt is claimed.

Policy must define the race rule, not rely on arrival order. A safe default: a cancellation recorded before execution is durably claimed prevents the effect, even if an approval arrived first. Once execution is claimed, cancellation can stop remaining work but cannot claim that a completed or unknown effect was undone. That case follows the reconciliation or compensation path in Chapter 7.2. A decision that arrives after expiry, cancellation, rejection or completion is a late event, not new authority. Keep it in the event record with its disposition. Do not reopen the run just because the event is authentic.

On recovery, resume from the persisted state, not from an agent-generated plan, and recheck that the stored subject still matches the proposed action. Nothing the agent says or retrieves can widen the approved subject.

### Authorize at the moment of effect

Approval says an appropriate human accepted this bound proposal. Authorization says this execution may invoke this action on this target for this tenant now. A consequential effect needs both.

So the execution step checks current authorization immediately before it invokes the effect: target, tenant, effective actor, capability, and any policy condition that could have changed during the wait. A revoked role, removed capability, changed tenant relation or invalidated policy leads to non-execution or a fresh approval, as policy defines. It never inherits permission from the old decision. If the action itself must change to become permissible, create a new subject and request a new decision.

### Keep old persisted work interpretable

Persisted state is an interface between versions. Record a schema ID and version with every approval-wait payload, durable-step input and material event. For example:

```yaml
persisted_state:
  state_type: awaiting_approval
  schema_id: durable.approval.wait
  schema_version: 1
  approval_request_id: ar-0042
  subject_digest: sha256:<canonical-subject-digest>
  expires_at: <recorded-deadline>
```

The example holds a reference or digest, not a sensitive payload. The subject record and audit data follow the data-handling rules in Chapter 3.3.

A compatible reader can supply a documented, meaning-preserving default for a newly optional field. A change to a transition, approval subject, authorization condition, action meaning, or the reading of a missing field is incompatible. Before it goes live, choose and test one path: keep a compatible handler for old work, route old and new work to the right versions, or migrate state with validation and a fallback. Never invent a value for a missing field if that could let an old approval authorize a different action.

This applies to active timers, retries and approvals as well as finished histories. Durable-workflow documentation describes replaying recorded histories against changed code as a compatibility check. The portable idea is to test captured states with the intended reader before deploying.[2]

## Decisions and best practices

Make the human role concrete. Name the action category that needs approval, the approver scope, the context the approver must see, the expiry window that fits the consequence, and whether a cancelled request can be reopened. Do not turn a routine acknowledgement into an approval gate just because durable execution is on, and do not call a consequential action an ordinary retry to avoid one.

Use a small, closed set of outcomes. At minimum, tell apart waiting, rejected, expired, cancelled before effect, effect resolution in progress, completed, and unresolved or partially effective. Labels are local; meanings and allowed transitions must be stable. A transition record shows the prior state, triggering event ID, decision time, policy version and resulting state. Record observable decisions and evidence, not a private reasoning trace.

Treat cancellation as a request to stop, not proof of reversal. Define who can cancel, what happens before an effect is claimed, what can be interrupted during execution, and the compensation or manual path afterward. Treat duplicate and delayed events as normal. They should produce an idempotent state decision, not a second execution attempt.

For a change with active work, list the state and schema versions that remain runnable, including waiting approvals. A rollout plan states which versions are supported, when an old handler can be retired, how incompatible items are migrated or escalated, and which captured histories were tested. Chapter 5.2 covers rollout authorization and rollback. For agents that are mid-task during a release, shift new work to the new version gradually, let old versions finish their runs, and resume from checkpoints instead of restarting.[5]

### Design approval for the human who has to give it

People who approve many requests start approving without reading. Research on human use of automation finds two linked effects: complacency, where people monitor automated output less, and automation bias, where they follow an automated recommendation even when it is wrong, including by missing problems the automation did not flag. Training and instructions do not reliably prevent either.[3] An approval gate that is always clicked through protects nothing. In practice:

- Ask for approval only where the consequence justifies it, based on the governance tier. Gates on routine actions teach people to ignore gates.
- Rate each tool as low, medium, or high from whether it reads or writes, whether it is reversible, the permissions it needs, and its financial impact, and let the rating decide which calls need a person. Also hand off to a person when a retry or failure limit is exceeded.[4]
- Show the exact change, not a summary: the diff against current state, the target, the tenant, the amount or count affected, and whether it can be undone.
- Show the evidence used and what the agent is unsure of, next to the proposal, not only its recommendation.
- Do not pre-select "approve" or put the recommendation ahead of the facts.
- Track approval rate, time to decide, and how often approvers edit or reject. Near-100 percent approval with very short decision times suggests the gate is not working.
- Review a sample of approved actions afterward, and seed test proposals with a known defect to check that approvers catch them.

## Requirements

- **APPROVAL-01 — Bound approval subject.** When an applicable policy requires a human approval before a consequential action, the durable run **MUST** create a stable approval-request identity and persist an immutable subject containing the action, canonical arguments or digest, target, tenant, effective actor, policy version, required approver scope, material context, and expiry. It **MUST** accept a decision only when it matches that subject and is from an authenticated approver with the required scope. A material change **MUST** invalidate the request and require a new approval. **Applies to:** human-governed consequential actions.

- **APPROVAL-02 — Event identity and durable transition.** A waiting run **MUST** persist its awaiting state, expiry, and processed-event identity before it waits, and **MUST** record the outcome of each accepted, duplicate, mismatched, or late event before resuming execution. It **MUST NOT** allow a duplicate delivery of an approval or resume event to produce another external-effect attempt. **Applies to:** any durable approval wait or externally delivered cancellation/decision.

- **APPROVAL-03 — Expiry, cancellation, and late events.** The approval policy **MUST** define and the implementation **MUST** enforce a deterministic precedence rule for approval, rejection, expiry, cancellation, and execution claim. At a minimum, a decision after recorded expiry, cancellation, rejection, or completion **MUST NOT** authorize execution; cancellation recorded before execution is claimed **MUST** prevent the new effect; and cancellation after the claim **MUST** enter the applicable interruption, reconciliation, or compensation path rather than assert reversal. **Applies to:** human-governed consequential actions.

- **APPROVAL-04 — Execution-time authorization.** After accepting approval and immediately before a consequential effect, the execution step **MUST** enforce current authorization for the target, tenant, effective actor, and capability. An approval **MUST NOT** create new authority or override a changed authorization decision. If a material change is needed, the run **MUST** request approval for the changed subject. **Applies to:** an approved action with an external effect.

- **APPROVAL-05 — Persisted compatibility.** A durable system **MUST** store a schema identity and version for persisted approval state, material events, and inputs needed to resume work. Before a deployment that can encounter active earlier state, the owner **MUST** document and test a compatible-reader, version-routing, or validated-migration path for each affected version. It **MUST NOT** reinterpret an old payload or approval in a way that changes its authorization meaning. **Applies to:** durable deployments with active, resumable, or retained work.

- **APPROVAL-06 — Decision evidence.** The owner **SHOULD** retain a reviewable approval subject, authenticated decision/event identities and dispositions, state-transition record, authorization result at execution, effect-resolution record, and compatibility-test evidence for the retention period selected under Chapter 3.3. **Applies to:** human-governed work and deployments that alter active durable state.

## Worked example

The internal policy assistant normally answers from approved, current, permission-filtered documents and returns citations and uncertainty. It has no write capability in that mode. A separate durable flow runs only when an authorized policy editor asks it to prepare a policy update. In this fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220, while a superseded document differs. The editor proposes changing the current amount to GBP 230. Publishing is consequential, and policy requires a human decision.

The flow creates request `ar-0042` and shows the approver the proposed action, the current source and the fictional patch. The subject includes `publish_policy_revision`, the canonical patch digest, the `travel-policy-current` target, the policy workspace tenant, the editor as effective actor, the approval-policy version, the required approver scope and an expiry. The flow enters `awaiting_approval`. The answer-generation agent cannot swap in a new patch while the request waits.

Say the approver approves `ar-0042`, but an editor withdraws the proposal before execution is claimed. The cancellation is recorded and the run becomes `cancelled_without_effect`. The approval event then arrives late. It is authentic, and it is kept as a late, non-authorizing event with its event ID, but it cannot make the run executable again. A duplicate delivery gets the same disposition. No publication call is made.

Now take a deployment while another instance of the flow is still waiting. The new version adds an optional display-only field to the approval request. Its reader recognizes the older `durable.approval.wait` version and keeps the prior subject meaning. It does not invent a new material field and pretend the old approver approved it. If the deployment instead changed the patch interpretation or added a new material approval condition, it would keep an older compatible handler or require a validated migration that voids and reissues the affected approvals.

For a valid, unexpired approval, the resumed flow rebuilds the canonical proposal and compares it with the stored subject. Just before publishing, it checks that the editor still has the permitted relationship to the policy workspace and that the action is still allowed. If not, it records a non-execution outcome, and the earlier approval does not bypass the check. If the publication request is sent but the receipt is lost, the run follows Chapter 7.2 and reconciles using the stable operation identity and authoritative target state. A duplicate approval event is never a reason to submit the update again.

## Evidence and checklist

Keep the approval policy and subject definition with the durable contract. Keep a transition specification that names the state, trigger, precedence rule, durable deadline and outcome for approval, rejection, expiry, cancellation, duplicate delivery and late delivery. Record the version compatibility decision with the release material.

Use a controlled clock and authoritative effect state in the tests ([4.5 Planning, Designing, and Running Tests and Evaluations](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md)). At least show that:

- an exact, in-scope approval resumes once, while a changed target, tenant, argument, policy version or approver scope does not;
- rejection, expiry, cancellation before execution claim, and a late approval after each of these create no new effect;
- both delivery orders of an approval and cancellation race follow the declared precedence rule, and duplicate events do not repeat an effect;
- withdrawn authorization between approval and execution prevents the action, and cancellation after execution claim enters the Chapter 7.2 resolution path;
- a captured old waiting state, timer, decision and retry can be read by the intended deployment path without changing the approval meaning;
- an effect with a lost receipt is judged from authoritative target state and the operation record, not the workflow transcript; and
- approvers catch known-defective test proposals, and approval rate and decision times show real review.

Attach the results to the evaluation evidence in [Chapter 4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md). Before a rollout that changes active durable work, carry the supported-version list, the migration or routing decision, and the rollback or retirement condition into [Chapter 5.2](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework AI RMF 1.0"
[2]: https://docs.temporal.io/develop/safe-deployments "Temporal safely deploying changes to Workflow code"
[3]: https://journals.sagepub.com/doi/10.1177/0018720810376055 "Complacency and Bias in Human Use of Automation: An Attentional Integration"
[4]: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ "A practical guide to building agents"
[5]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"

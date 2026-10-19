# 7.3 Approval, Suspension, and In-Flight Compatibility

**Status:** 0.5.0 first draft
**Audience:** Builders of durable or human-governed work, security reviewers, operators, and accountable owners.
**Applicability:** Applies when a durable run waits for a human decision before a consequential action, and when a change could encounter persisted work created by an earlier version. It is not a reason to add human approval or durable state to an ephemeral, read-only assistant.

[Part 7 — Durable Execution and Human-Governed Work](README.md) · [Playbook applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.2 Side Effects, Idempotency, and Unknown Outcomes](02-side-effects-idempotency-and-unknown-outcomes.md)

## Purpose and applicability

A human approval is not a general endorsement of an agent or an open-ended permission to act. It is a decision about one defined action in one material context for a limited time. Without that binding, a response intended for an earlier proposal can be applied after the target, tenant, arguments, policy, or authority has changed. A durable run makes the problem more visible: it may suspend for hours, resume on a different worker, receive the same event twice, or encounter a new build before the decision arrives.

Approval is selected by the action’s consequence and the applicable policy, not by whether the agent looks sophisticated. The ordinary internal policy assistant remains read-only and does not need this chapter merely to return a cited answer. Its durable variant does need these controls when it prepares and applies a human-approved policy update. NIST similarly frames human roles and oversight as context-dependent, while calling for those roles and responsibilities to be explicitly differentiated. [1]

Chapter 3.1 owns identity, authority, least privilege, and the policy that says who may approve. This chapter owns the state semantics once that policy requires an approval: what was approved, what event changes a waiting run, when a decision ceases to authorize work, and how active work survives a change. Chapter 7.2 owns the safety of the external effect itself, including reconciliation when an effect may have happened but its receipt was lost.

## Working model

### Bind a decision to an approval subject

An approval request needs a stable identity and an immutable **approval subject**. The subject is the canonical description that a reviewer sees and that the execution path later compares. It should identify:

- the approval request and durable workflow-chain identities;
- the stable action name and version, canonical arguments or their digest, and intended target;
- the tenant and effective actor whose authority is being exercised;
- the policy version, required approver scope, and any policy-defined material context, such as a data classification or impact category; and
- the request time and expiry time.

The approval ID identifies a particular decision. The request ID identifies what is awaiting a decision. A delivery or decision-event ID identifies one message carrying that decision. These are not interchangeable: a stable request identity prevents a valid decision from being applied to another wait, while an event identity makes duplicate delivery observable and harmless.

A digest is useful only if the representation being compared is defined. Decide how arguments are ordered, normalized, and typed before calculating it. More importantly, do not reduce the subject to a digest alone: the stored, reviewable subject must let a reviewer understand the target and intended action. If any policy-defined material field changes, the former approval is no longer valid. The run creates a new request rather than treating approval of a nearby action as approval of the changed one.

### Suspend and resume as state transitions

A waiting run is not inactive; it has an explicit durable state. It records an `awaiting_approval` state, its subject, an expiry deadline, and the identities of processed events before it waits. An authenticated approval, rejection, cancellation, or timeout then requests a transition. Persist the transition decision before continuing toward an external effect.

Use a durable timer or equivalent recorded deadline to decide expiry. Do not let a restarted process reinterpret an expired request as current because a local clock, an instruction, or a model response says to continue. A valid approval normally moves the run to an approved-but-not-yet-executed state. That separation gives cancellation a defined opportunity to stop work before the execution attempt is claimed.

A policy must define the race rule rather than relying on arrival order. A safe default is that a cancellation recorded before the run has durably claimed execution prevents the new effect, even if an approval arrived first. Once execution has been claimed, cancellation can stop remaining work where possible, but it cannot assert that a completed or unknown external effect was undone. That case follows the reconciliation or compensation path in Chapter 7.2. A decision received after expiry, cancellation, rejection, or completion is evidence about a late event; it is not new authority. Keep it in the event record with its disposition and do not reopen the run merely because the event is authentic.

On recovery, resume from the persisted state rather than from an agent-generated plan. Recheck that the stored subject still matches the proposed action. The agent’s explanation, a retrieved document, or a new model answer cannot widen the approved subject.

### Authorize at the moment of effect

Approval and authorization answer different questions. Approval says that the appropriate human accepted this bound proposal. Authorization says that the current execution is allowed to invoke this action on this target for this tenant now. Both are necessary for a consequential effect.

The execution step therefore checks the current authorization boundary after the approval is accepted and immediately before it invokes the effect. That check includes the target, tenant, effective actor, capability, and any policy condition that could have changed while the run waited. A revoked role, removed capability, changed tenant relation, or invalidated policy causes a non-execution outcome or a fresh approval path as policy defines; it does not inherit permission from the old decision. This check does not mutate the approved subject. If the proposed action itself must change to become permissible, create a new subject and request a new decision.

### Keep old persisted work interpretable

Persisted state is an interface between versions. Record a schema identity and version with every approval-wait payload, durable-step input, and material event. A neutral waiting-state example is:

```yaml
persisted_state:
  state_type: awaiting_approval
  schema_id: durable.approval.wait
  schema_version: 1
  approval_request_id: ar-0042
  subject_digest: sha256:<canonical-subject-digest>
  expires_at: <recorded-deadline>
```

The example carries a reference or digest rather than a sensitive action payload. The subject record and audit data still follow the data-handling rules in Chapter 3.3.

A compatible reader may supply a documented meaning-preserving default for a newly optional field. A change that alters a transition, approval subject, authorization condition, action semantics, or interpretation of a missing field is incompatible. Before that change is active, choose and test one explicit path: keep a compatible handler for old work, route old and new work to appropriate versions, or migrate persisted state with validation and a defined fallback. Never silently invent a value for a missing field when doing so could make an old approval authorize a materially different action.

The same discipline applies to active timers, retries, and approvals as to completed histories. Durable-workflow documentation describes replaying recorded histories against changed code as a compatibility check; the portable principle is to test representative captured states with the intended reader before relying on a deployment. [2]

## Decisions and best practices

Start by making the policy’s human role concrete. Name the action category that requires approval, the required approver scope, the material context that must be shown, the expiry window appropriate to the consequence, and whether a cancelled request can ever be reopened. Do not turn a routine acknowledgement into an approval gate merely because durable execution is enabled. Conversely, do not make a consequence-dependent action safe by calling it an ordinary retry.

Use a small, closed set of durable outcomes. At minimum, distinguish waiting, rejected, expired, cancelled before effect, executing or effect resolution in progress, completed, and unresolved/partially effective outcomes. The exact labels are local, but their meaning and permitted transitions must be stable. A transition record should show the prior state, triggering event identity, decision time, policy version, and resulting state. It should record observable decisions and evidence, not a private model reasoning trace.

Treat cancellation as a request to stop, not proof of reversal. Define who can cancel, what happens before an effect is claimed, what work may be interrupted during execution, and the compensation or manual path afterward. Likewise, treat duplicate and delayed events as expected delivery behavior. They should produce an idempotent state decision, not a second execution attempt or an error that leaves the run ambiguous.

For a change with active work, inventory the state and schema versions that remain runnable, including waiting approvals. A rollout plan should state which versions are supported, when an older handler may be retired, how incompatible items are migrated or escalated, and which captured histories and payloads were exercised. Chapter 5.2 owns rollout authorization and rollback decisions; this chapter supplies the compatibility constraint and evidence.

## Requirements

- **APPROVAL-01 — Bound approval subject.** When an applicable policy requires a human approval before a consequential action, the durable run **MUST** create a stable approval-request identity and persist an immutable subject containing the action, canonical arguments or digest, target, tenant, effective actor, policy version, required approver scope, material context, and expiry. It **MUST** accept a decision only when it matches that subject and is from an authenticated approver with the required scope. A material change **MUST** invalidate the request and require a new approval. **Applies to:** human-governed consequential actions.

- **APPROVAL-02 — Event identity and durable transition.** A waiting run **MUST** persist its awaiting state, expiry, and processed-event identity before it waits, and **MUST** record the outcome of each accepted, duplicate, mismatched, or late event before resuming execution. It **MUST NOT** allow a duplicate delivery of an approval or resume event to produce another external-effect attempt. **Applies to:** any durable approval wait or externally delivered cancellation/decision.

- **APPROVAL-03 — Expiry, cancellation, and late events.** The approval policy **MUST** define and the implementation **MUST** enforce a deterministic precedence rule for approval, rejection, expiry, cancellation, and execution claim. At a minimum, a decision after recorded expiry, cancellation, rejection, or completion **MUST NOT** authorize execution; cancellation recorded before execution is claimed **MUST** prevent the new effect; and cancellation after the claim **MUST** enter the applicable interruption, reconciliation, or compensation path rather than assert reversal. **Applies to:** human-governed consequential actions.

- **APPROVAL-04 — Execution-time authorization.** After accepting approval and immediately before a consequential effect, the execution step **MUST** enforce current authorization for the target, tenant, effective actor, and capability. An approval **MUST NOT** create new authority or override a changed authorization decision. If a material change is needed, the run **MUST** request approval for the changed subject. **Applies to:** an approved action with an external effect.

- **APPROVAL-05 — Persisted compatibility.** A durable system **MUST** store a schema identity and version for persisted approval state, material events, and inputs needed to resume work. Before a deployment that can encounter active earlier state, the owner **MUST** document and test a compatible-reader, version-routing, or validated-migration path for each affected version. It **MUST NOT** reinterpret an old payload or approval in a way that changes its authorization meaning. **Applies to:** durable deployments with active, resumable, or retained work.

- **APPROVAL-06 — Decision evidence.** The owner **SHOULD** retain a reviewable approval subject, authenticated decision/event identities and dispositions, state-transition record, authorization result at execution, effect-resolution record, and compatibility-test evidence for the retention period selected under Chapter 3.3. **Applies to:** human-governed work and deployments that alter active durable state.

## Worked example

The internal policy assistant normally answers from approved, current, permission-filtered documents and returns citations and uncertainty. It has no external write capability in that mode. A separate durable flow is invoked only when an authorized policy editor asks it to prepare a policy update. In this fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220, while a superseded document differs. The editor proposes changing the current amount to GBP 230; publishing the revision is consequential and the policy requires a human decision.

The flow creates request `ar-0042` and shows the approver the proposed action, the current source, and the fictional patch. Its recorded subject includes `publish_policy_revision`, the canonical patch digest, the `travel-policy-current` target, the policy workspace tenant, the editor as effective actor, the applicable approval-policy version, the required approver scope, and an expiry. It then durably enters `awaiting_approval`. The answer-generation agent cannot substitute a new patch while this request waits.

Assume the approver approves `ar-0042`, but an editor withdraws the proposal before the execution step is claimed. The cancellation transition is recorded, so the run becomes `cancelled_without_effect`. The approval event arrives late. It is authentic and is retained as a late, non-authorizing event associated with its event ID, but it cannot move the cancelled run back to executable state. A duplicate delivery of that event has the same recorded disposition. No publication call is made.

Now consider a compatible deployment while another instance of the same flow is still waiting. The new version adds an optional display-only field to the approval request. Its reader recognizes the older `durable.approval.wait` version and preserves the prior subject semantics. It does not synthesize a new material field and pretend that the older approver approved it. If the proposed deployment instead changes the patch interpretation or adds a new material approval condition, it keeps an older compatible handler or requires a validated migration that invalidates and reissues affected approvals.

For a valid, unexpired approval, the resumed flow rebuilds the canonical proposal and compares it to the stored subject. Immediately before publishing, it checks that the editor still has the permitted relationship to the policy workspace and that the action remains allowed. If that authorization was revoked, it records a non-execution outcome; the earlier approval does not bypass the check. If the publication request is sent but its receipt is lost, the run follows Chapter 7.2: it reconciles using the stable operation identity and authoritative target state. It never treats a duplicate approval event as a reason to submit the update again.

## Evidence and checklist

The approval-state design should be reviewable before it is exercised in production. Keep the approval policy and subject definition with the durable contract. Keep a transition specification that names the state, trigger, precedence rule, durable deadline, and outcome for approval, rejection, expiry, cancellation, duplicate delivery, and late delivery. Record the version compatibility decision alongside the release material.

The applicable test plan in [4.5 Planning, Designing, and Running Tests and Evaluations](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md) should use a controlled clock and authoritative effect state. It should demonstrate at least the following:

- an exact, in-scope approval resumes once, while a changed target, tenant, argument, policy version, or approver scope does not;
- rejection, expiry, cancellation before execution claim, and a late approval after each of those states create no new effect;
- both delivery orders of an approval/cancellation race follow the declared precedence rule, and duplicate events do not repeat an effect;
- authorization withdrawal between approval and execution prevents the action, while cancellation after execution claim enters the Chapter 7.2 resolution path;
- a captured old waiting state, timer, decision, and retry can be read by the intended deployment path without changing the approval meaning; and
- an effect whose receipt is lost is judged from authoritative target state and the operation record, not from the workflow transcript.

Attach those results to the evaluation evidence described in [Chapter 4.3](../../development-guide/04-testing-and-evaluation/03-evaluation-types-and-dimensions.md). Before a rollout that changes active durable work, carry the supported-version inventory, migration or routing decision, and rollback/retirement condition into [Chapter 5.2](../../development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md). Missing compatibility evidence is not made safe by a passing ordinary-path approval test.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework AI RMF 1.0"
[2]: https://docs.temporal.io/develop/safe-deployments "Temporal safely deploying changes to Workflow code"

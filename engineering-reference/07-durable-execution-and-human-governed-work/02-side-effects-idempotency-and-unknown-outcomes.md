# 7.2 Side Effects, Idempotency, and Unknown Outcomes

**Status:** 0.5.0-draft.2 — draft
**Audience:** Agent builders, tool owners, evaluators, operators and accountable action owners.
**Applicability:** Use whenever an execution path can cause an externally visible effect whose repetition, absence or final state matters, such as creating or changing a record, sending a consequential notification, or submitting a request to another system. It applies whether or not the run is durable; durable work needs it in addition to the recovery controls in [7.1](01-execution-classes-persistence-and-recovery.md). It does not apply to the policy assistant while it only reads approved documents, but it applies once its human-approved update capability is enabled.

[Part 7](README.md) · [Applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.3 Approval, Suspension, and In-Flight Compatibility](03-approval-suspension-and-in-flight-compatibility.md)

## Purpose and applicability

A local history can show that an agent attempted an action. It cannot show whether another system accepted it. The hard case is the gap between an external commit and the agent recording the receipt: the target completes an update, then a crash or lost response leaves the resumed run with no local record. Treating that missing receipt as proof that nothing happened turns recovery into a duplicate action.

Durability preserves progress. It does not give exactly-once external action. An operation is retry-safe only when the target's semantics, or an authoritative reconciliation procedure, make repeating that specific intended effect safe. Approval binding and execution-time authorization are covered in [7.3](03-approval-suspension-and-in-flight-compatibility.md). Neither a retry nor a reconciliation result widens the approved authority.

## Working model

Give every intended external effect a stable **operation identity** before the first send. The identity names one business action, not one network attempt or one workflow replay. Bind it to the target, the tenant or principal scope, the canonical intended arguments and an operation-version rule, and record these with the chosen outcome policy. An opaque operation ID, a target-supported idempotency key and a digest of the canonical intent can be separate fields. Do not use a changing attempt ID as the operation identity.

Keep four observations apart:

- **Intent recorded:** the agent has created a proposed operation and its stable identity.
- **External effect committed:** the target accepted or performed the effect. The target's accepted-operation record, versioned resource state or equivalent authoritative ledger establishes this.
- **Receipt recorded:** the agent has saved a result the target returned or that reconciliation found.
- **Attempt observed:** a caller, log or trace says a request was sent. This is diagnostic evidence, not proof of the effect.

The commit point is when the target has accepted the operation under its own contract. A local durable-step completion only records what the agent learned. A transcript, a model statement or a response-shaped object is not proof of an effect.

HTTP shows why method names are not enough. Idempotent-method semantics concern the intended server effect, allow a retry after a lost response, and still allow repeated server-side logging. A client should not automatically retry a non-idempotent request unless it knows the request is idempotent for that resource or can detect that the original was never applied.[1] An expired IETF Internet-Draft, not a standard, describes one convention: a key identifies retries of the same request, must not be reused with a different payload, and a retry of a completed request returns the saved result.[2] It helps only when the receiving service documents and enforces that behavior. Production services also differ on how long they keep keys, so check the retention period.

A lost response from a model inference request can create uncertain or duplicated cost if repeated. That is a cost and admission-control concern. It is not evidence that a business update happened, and a repeatable model request is no basis for judging that a later write is safe to repeat.

## Decisions and best practices

Decide the recovery disposition for each effect before enabling it.

A **retry-safe** operation has a target-supported identity and duplicate behavior that preserves the intended result. For example, the target returns the original accepted result for the same key and intent, or exposes an authoritative accepted-operation record. Resend the same canonical request with the same operation identity, not a newly generated one.

A **reconcile-first** operation may have succeeded, but the agent has no trustworthy receipt. Query the target by the stable operation identity and check that the returned target, principal scope and intent digest match. The target must define the query as authoritative. An eventually consistent general search or an ambiguous current state cannot prove that this operation did or did not commit. Only an authoritative finding of no commit moves the operation to retry-safe.

An **unresolved/manual** operation has no safe automatic conclusion. This covers an unavailable or inconclusive target record, a mismatched identity or digest, an expired identity-retention period, and a target whose state cannot tell this operation from a similar one. Stop automatic sends, keep the evidence, and return a declared unresolved outcome for the accountable operator or target owner. A new operation, changed intent or compensation is a new decision. It must not quietly reuse an approval or pass as a retry.

If a target lacks native idempotency, a jointly designed operation record or target-side lookup can still give an authoritative reconciliation path. A local outbox or operation record alone does not prove the target accepted anything. If there is neither duplicate prevention nor an authoritative lookup, make the action manual or redesign the interface. Do not rely on timing.

Compensation is a separate external operation. It does not erase uncertainty. Use it only when the target defines a meaningful, permitted reversal, the original effect is known well enough to compensate, and the compensation has its own identity, authorization and evidence. Do not use it for an effect that may never have happened, or for a reversal that would cause different harm.

### Multi-step effects: outbox and sagas

Two patterns help when one job touches several systems.

- **Transactional outbox.** Write the outgoing message in the same local database transaction that updates your own state, then let a separate relay publish it. The message is sent if and only if the transaction commits, which closes the gap between "state changed" and "message sent". The relay can publish a message more than once, so consumers and targets must be idempotent. This fits the split above: the outbox row is the intent recorded, and it is not proof that the target committed.[3]
- **Sagas.** When a job spans several systems and no single transaction can cover it, run it as a sequence of local steps. Each step that can be reversed has a compensating step, designed in advance, that runs if a later step fails. Compensations are not automatic rollbacks. Each one is a separate external operation, so it needs its own identity, authorization and evidence under EFFECT-04.[4]

## Requirements

- **EFFECT-01 — Stable identity.** For every applicable externally visible effect, the execution path **MUST** create and persist one stable operation identity before the first target-facing attempt. It **MUST** bind the intended target and authority scope, canonical intended arguments or an integrity-preserving digest, and operation version. Retries, recovery attempts, and duplicate deliveries **MUST** reuse that identity; an identity presented with materially different intent **MUST NOT** be treated as the same operation.

- **EFFECT-02 — Declared retry disposition.** For every applicable operation, the tool or action contract **MUST** declare whether it is retry-safe, reconcile-first, or unresolved/manual after a missing or ambiguous receipt. Automatic retry **MUST** be limited to the retry-safe disposition, using the original identity and canonical intent. A transport timeout, process failure, or missing local receipt **MUST NOT** by itself authorize a repeat of an unsafe effect.

- **EFFECT-03 — Authoritative reconciliation.** When an operation is reconcile-first, the execution path **MUST** query an identified authoritative target record or state oracle before any further send. It **MUST** verify the returned operation identity and intent binding before recording completion. If the oracle cannot establish committed or not-committed status, the path **MUST** produce the declared unresolved/manual outcome and preserve the operation record and evidence for follow-up.

- **EFFECT-04 — Compensation boundary.** When a completed external effect is reversible, the action design **SHOULD** define whether compensation is permitted, its preconditions, and its authoritative success evidence. A compensation step **MUST NOT** be used as an automatic response to an unknown outcome, and any compensation that is itself externally visible **MUST** satisfy EFFECT-01 through EFFECT-03.

- **EFFECT-05 — Failure evidence.** Before an applicable action is released or materially changed, its evaluation evidence **MUST** include injected failure at the target-commit/receipt-record boundary, duplicate delivery, and an unresolved-oracle path. Tests **MUST** check the authoritative target state or accepted-operation record and the declared terminal disposition, not only the agent transcript or local step status. For fixtures, evaluators and release decisions, see [Part 4](../../development-guide/04-testing-and-evaluation/README.md).

## Worked example: a policy update with a lost receipt

The internal policy assistant normally answers from approved, current, permission-filtered documents and returns citations with uncertainty. In this fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220, while `travel-policy-superseded` differs. In its read-only form it has no write capability.

A later, human-governed variant prepares an approved update that adds an effective-date clarification to `travel-policy-current` without changing the GBP 220 amount. The exact approval, its expiry and execution-time authorization have already passed the checks in [7.3](03-approval-suspension-and-in-flight-compatibility.md). Before the write step, the workflow records an intent like this:

```yaml
operation:
  operation_id: policy-update:travel-policy-current:effective-date:42
  operation_version: 1
  target: policy-store/travel-policy-current
  tenant: internal-policy
  expected_revision: 42
  intent_digest: sha256:<canonical-update-digest>
  idempotency_key: policy-update:travel-policy-current:effective-date:42
  disposition_if_receipt_missing: reconcile_first
  approval_id: approved-policy-update-42
```

The policy store accepts the update, creates revision 43, and records the operation identity and intent digest in its accepted-operation ledger. The response is then lost before the durable step can save the receipt. On recovery, the operation record exists but has no result. That state is not `not_committed`. It is `unknown`.

The resumed workflow follows the declared reconcile-first path. It asks the policy store for the operation identity and gets the accepted record for revision 43 with the same target, tenant and digest. That record is authoritative, so the workflow records `completed_reconciled` and does not send the update again. A second revision would not be evidence of a good recovery.

If the store instead reports authoritatively that no operation with that identity committed, the workflow may resend the unchanged request with the same identity. If the store is unavailable, returns a record with a different digest, or cannot tell the update from another one, the workflow returns `unresolved_manual` and writes nothing more. The operator can inspect the target's records and start a new, properly authorized operation if needed. A compensating update is not appropriate until the original effect is known and the target's compensation rule allows it.

## Evidence and checklist

Use a resettable target fixture with an accepted-operation ledger or another documented state oracle. Collect this evidence:

- Inject a response loss or process failure after the fixture commits revision 43 but before the agent records its receipt. On recovery, assert one accepted operation, revision 43, a matching identity and digest, and `completed_reconciled` with no second write.
- Deliver the same request twice with the same identity and intent. Assert the target returns the first result and creates no new revision. Deliver the same identity with altered intent and assert rejection or an unresolved outcome, never a merge.
- Fail before the target commit. Only when the authoritative query shows no committed operation, assert that the same identity can be retried and produces one accepted effect.
- Make the oracle unavailable or ambiguous after a receipt loss. Assert `unresolved_manual`, no further send, and retained intent, attempt and reconciliation evidence.
- Where compensation is offered, test a known completed effect, the compensation preconditions and the target's resulting authoritative state. A local `compensated` status is not a pass.

Before calling the controls complete, confirm:

- [ ] Each effect has a stable identity, canonical intent binding and documented target scope.
- [ ] The target's duplicate behavior, identity-retention period and authoritative reconciliation source are known.
- [ ] Every ambiguous-receipt path has a retry-safe or unresolved/manual disposition; none treats a missing receipt as a negative result.
- [ ] Compensation, where available, is an explicit, separately evidenced operation rather than a hidden retry.
- [ ] Failure-injection results use the authoritative target state and are linked to the evaluated action version.

## References

[1]: https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2 "HTTP Semantics"
[2]: https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header "The Idempotency-Key HTTP Header Field"
[3]: https://microservices.io/patterns/data/transactional-outbox.html "Pattern: Transactional outbox"
[4]: https://microservices.io/patterns/data/saga.html "Pattern: Saga"

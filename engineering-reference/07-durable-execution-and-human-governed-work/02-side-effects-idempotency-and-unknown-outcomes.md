# 7.2 Side Effects, Idempotency, and Unknown Outcomes

**Status:** 0.5.0 first draft
**Audience:** Agent builders, tool owners, evaluators, operators, and accountable action owners.
**Applicability:** Applies whenever an execution path can cause an externally visible effect whose repetition, absence, or final state matters. This includes creating or changing a record, sending a consequential notification, or submitting a request to another system. It applies whether the run is durable or not; durable work needs it in addition to the recovery controls in [7.1](01-execution-classes-persistence-and-recovery.md). It does not apply to the policy assistant while it only reads approved documents, but it applies as soon as its human-approved update capability is enabled.

[Part 7](README.md) · [Applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.3 Approval, Suspension, and In-Flight Compatibility](03-approval-suspension-and-in-flight-compatibility.md)

## Purpose and applicability

A local history can show that an agent *attempted* an action. It cannot by itself show whether another system accepted that action. The difficult failure is the gap between an external commit and the agent recording the receipt: a target can complete an update, then a process crash or lost response can leave the resumed run with no local completion record. Treating that missing receipt as proof that nothing happened turns recovery into a duplicate action.

Durability preserves progress and makes recovery possible; it does not establish exactly-once external action. An operation is retry-safe only when the target's semantics, or an authoritative reconciliation procedure, make repeating that particular intended effect safe. Approval binding and execution-time authorization remain the responsibilities of [7.3](03-approval-suspension-and-in-flight-compatibility.md); neither a retry nor a reconciliation result enlarges the approved authority.

## Working model

Give every intended external effect a stable **operation identity** before the first send. The identity names one business action, not one network attempt or one workflow replay. Bind it to the target, tenant or principal scope, canonical intended arguments, and an operation-version rule. Record those facts with the selected outcome policy. An opaque operation identifier, a target-supported idempotency key, and a digest of the canonical intent may be distinct fields; do not substitute a changing attempt identifier for the operation identity.

Keep four observations separate:

- **Intent recorded:** the agent has created a proposed operation and its stable identity.
- **External effect committed:** the target accepted or performed the effect. The target's accepted-operation record, versioned resource state, or equivalent authoritative ledger establishes this fact.
- **Receipt recorded:** the agent has persisted a result returned by the target or learned during reconciliation.
- **Attempt observed:** a caller, log, or trace says a request was sent. This is useful diagnostic evidence, not proof of the external effect.

The authoritative commit point is the point at which the target has accepted the operation according to its own contract. A local durable-step completion is only the agent's record of what it learned. A transcript, a model statement, or a response-shaped object is not an effect oracle.

HTTP illustrates why method names alone are not enough. Its idempotent-method semantics concern the intended server effect, permit a retry after a response is lost, and still allow separately repeated server-side logging or history. A client should not automatically retry a non-idempotent request unless it knows the request is idempotent for that resource or can detect that the original was never applied. [1] The IETF's `Idempotency-Key` draft describes one target-facing convention: a key identifies retries of the same request and must not be reused for a different payload. It is useful only when the receiving service documents and enforces the necessary behavior. [2]

A lost response from an inference request can also create uncertain or duplicated cost if it is repeated. That is a cost and admission-control concern, not evidence that a business update occurred. Do not use a repeatable model request to infer that a later write is safe to repeat.

## Decisions and best practices

Decide the recovery disposition for each effect before enabling it. A **retry-safe** operation has a target-supported identity and duplicate behavior that preserves the intended result. For example, the target may return the original accepted result for the same key and intent, or expose an authoritative accepted-operation record. Repeat the same canonical request with the same operation identity, not a newly generated request.

A **reconcile-first** operation might already have succeeded, but the agent has no trustworthy receipt. Query the target by the stable operation identity and validate that the returned target, principal scope, and canonical-intent digest match. The target must define the query as authoritative: an eventually consistent general search or an ambiguous current state cannot prove that this operation did or did not commit. Only an authoritative finding of no commit can move the operation into a retry-safe disposition.

An **unresolved/manual** operation has no safe automatic conclusion. This includes an unavailable or inconclusive target record, a mismatched identity or intent digest, an expired identity-retention period, and a target whose state cannot distinguish this operation from a similar one. Stop automatic sends, preserve the known evidence, and return a declared unresolved outcome for the accountable operator or target owner. A new operation, modified intent, or compensation is a new decision; it must not silently reuse an approval or be disguised as a retry.

Where a target lacks native idempotency support, a jointly designed operation record or target-side lookup may still provide an authoritative reconciliation path. A local outbox or operation record alone does not prove target acceptance. If neither duplicate prevention nor an authoritative lookup is available, make the action manual or redesign the interface rather than relying on timing.

Compensation is a separate external operation, not an eraser for uncertainty. Use it only when the target defines a meaningful and permitted reversal, the original effect is known well enough to compensate, and the compensation has its own identity, authorization, and evidence. It is not appropriate for an effect that might never have occurred, or for a reversal that would cause a different harmful effect.

## Requirements

- **EFFECT-01 — Stable identity.** For every applicable externally visible effect, the execution path **MUST** create and persist one stable operation identity before the first target-facing attempt. It **MUST** bind the intended target and authority scope, canonical intended arguments or an integrity-preserving digest, and operation version. Retries, recovery attempts, and duplicate deliveries **MUST** reuse that identity; an identity presented with materially different intent **MUST NOT** be treated as the same operation.

- **EFFECT-02 — Declared retry disposition.** For every applicable operation, the tool or action contract **MUST** declare whether it is retry-safe, reconcile-first, or unresolved/manual after a missing or ambiguous receipt. Automatic retry **MUST** be limited to the retry-safe disposition, using the original identity and canonical intent. A transport timeout, process failure, or missing local receipt **MUST NOT** by itself authorize a repeat of an unsafe effect.

- **EFFECT-03 — Authoritative reconciliation.** When an operation is reconcile-first, the execution path **MUST** query an identified authoritative target record or state oracle before any further send. It **MUST** verify the returned operation identity and intent binding before recording completion. If the oracle cannot establish committed or not-committed status, the path **MUST** produce the declared unresolved/manual outcome and preserve the operation record and evidence for follow-up.

- **EFFECT-04 — Compensation boundary.** When a completed external effect is reversible, the action design **SHOULD** define whether compensation is permitted, its preconditions, and its authoritative success evidence. A compensation step **MUST NOT** be used as an automatic response to an unknown outcome, and any compensation that is itself externally visible **MUST** satisfy EFFECT-01 through EFFECT-03.

- **EFFECT-05 — Failure evidence.** Before an applicable action is released or materially changed, its evaluation evidence **MUST** include injected failure at the target-commit/receipt-record boundary, duplicate delivery, and an unresolved-oracle path. Tests **MUST** check the authoritative target state or accepted-operation record and the declared terminal disposition, not only the agent transcript or local step status. Detailed fixture, evaluator, and release-decision practice remains owned by [Part 4](../../development-guide/04-testing-and-evaluation/README.md).

## Worked example: a policy update with a lost receipt

The internal policy assistant normally answers from approved, current, permission-filtered documents and returns citations with uncertainty. In the fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220, while `travel-policy-superseded` differs. It has no write capability in that read-only form.

A later, human-governed variant prepares an approved update that adds an effective-date clarification to `travel-policy-current` without changing the GBP 220 amount. The exact approval, its expiry, and execution-time authorization have already passed the checks described in [7.3](03-approval-suspension-and-in-flight-compatibility.md). Before the write step, the workflow records an intent like this adaptable example:

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

The policy store accepts the update, creates revision 43, and records the operation identity and intent digest in its accepted-operation ledger. The network response is then lost before the durable step can persist the receipt. On recovery, the operation record still exists but has no result. That state is **not** `not_committed`; it is `unknown`.

The resumed workflow follows the declared reconcile-first path. It asks the policy store for the operation identity and receives the accepted record for revision 43 with the same target, tenant, and digest. That target record is authoritative, so the workflow records `completed_reconciled` and does not send the update again. A second revision is neither necessary nor evidence of a successful recovery.

If the policy store instead authoritatively reports that no operation with that identity committed, the workflow may resend the unchanged request with the same identity. If the store is unavailable, returns a record with a different digest, or cannot distinguish the proposed update from another update, the workflow returns `unresolved_manual` and makes no further write. The operator can inspect the target's records and choose a new, properly authorized operation if one is needed. A compensating update would be inappropriate until the original effect is known and the target's compensation rule permits it.

## Evidence and checklist

Use a resettable target fixture with an accepted-operation ledger or another documented state oracle. The following evidence demonstrates the example's controls:

- Inject a response loss or process failure after the fixture commits revision 43 but before the agent records its receipt. On recovery, assert one accepted operation and revision 43, a matching identity and digest, and `completed_reconciled` without a second target write.
- Deliver the same request twice with the same identity and canonical intent. Assert the target reports or returns the first operation result and does not create another revision. Deliver the same identity with altered intent and assert rejection or an unresolved outcome, never coalescence.
- Fail before the target commit. Only when the authoritative query establishes no committed operation, assert that the same identity can be retried and produces one accepted effect.
- Make the target oracle unavailable or ambiguous after a receipt loss. Assert `unresolved_manual`, no additional target-facing send, and retained intent, attempt, and reconciliation evidence.
- Where compensation is offered, test a known completed effect, its permitted compensation preconditions, and the target's resulting authoritative state. Do not pass the test merely because a local status says `compensated`.

Before declaring this chapter applicable controls complete, confirm:

- [ ] Each effect has a stable identity, canonical intent binding, and documented target scope.
- [ ] The target's duplicate behavior, identity-retention period, and authoritative reconciliation source are known.
- [ ] Every ambiguous-receipt path has a retry-safe or unresolved/manual disposition; none treats a missing receipt as a negative result.
- [ ] Compensation, where available, is an explicit, separately evidenced operation rather than a hidden retry.
- [ ] Failure-injection results use the authoritative target state and are linked to the evaluated action version.

## References

[1]: https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2 "HTTP Semantics"
[2]: https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header "The Idempotency-Key HTTP Request Header Field"

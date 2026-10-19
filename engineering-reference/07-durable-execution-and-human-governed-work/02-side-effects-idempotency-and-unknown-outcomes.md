# 7.2 Side Effects, Idempotency, and Unknown Outcomes

**Status:** 0.5.0-draft.2 — draft
**Audience:** Agent builders, tool owners, evaluators, operators and accountable action owners.
**Applicability:** Whenever an execution path can cause an externally visible effect whose repetition, absence or final state matters (changing a record, a consequential notification, a request to another system), durable or not. Durable work also needs [7.1](01-execution-classes-persistence-and-recovery.md). It applies to the policy assistant once its approved update capability is enabled.

[Part 7](README.md) · [Applicability](../../applicability.md) · [7.1 Execution Classes, Persistence, and Recovery](01-execution-classes-persistence-and-recovery.md) · [7.3 Approval, Suspension, and In-Flight Compatibility](03-approval-suspension-and-in-flight-compatibility.md)

## Purpose and applicability

A local history shows an attempt, not whether another system accepted it. The hard case is the gap between an external commit and the agent recording the receipt: a crash or lost response leaves the resumed run with no record, and treating that as proof nothing happened turns recovery into a duplicate action.

Durability preserves progress, not exactly-once action. An operation is retry-safe only when the target's semantics or an authoritative reconciliation make repeating that effect safe. Neither widens approved authority ([7.3](03-approval-suspension-and-in-flight-compatibility.md)).

## Working model

Give every intended effect a stable **operation identity** before the first send. It names one business action, not an attempt or replay, and binds target, tenant or principal scope, canonical arguments and operation version. Operation ID, idempotency key and intent digest can be separate fields; a changing attempt ID is never the identity.

Keep four observations apart:

- **Intent recorded:** a proposed operation and its identity exist.
- **Effect committed:** the target accepted it, per its accepted-operation record, versioned state or authoritative ledger.
- **Receipt recorded:** the agent saved a returned or reconciled result.
- **Attempt observed:** a log or trace says a request was sent; diagnostic only.

Only the target's acceptance is the commit point; a local step completion, transcript or response-shaped object is not proof of an effect.

Method names are not enough. HTTP idempotency concerns the intended server effect, allows retry after a lost response, and still permits repeated logging; clients should not auto-retry a non-idempotent request unless they know it is idempotent for that resource or can detect the original was never applied.[1] An expired IETF Internet-Draft (not a standard) describes a key that identifies retries of one request, must not be reused with a different payload, and returns the saved result for a completed request.[2] It helps only where the service enforces it; check key retention.

Repeating a model request after a lost response duplicates cost, an admission concern; it says nothing about whether a later write is safe to repeat.

## Decisions and best practices

Decide each effect's recovery disposition before enabling it.

- **Retry-safe:** the target's duplicate handling preserves the intended result (it returns the original result for the same key and intent, or exposes an authoritative accepted-operation record). Resend the same canonical request and identity.
- **Reconcile-first:** it may have succeeded but no trustworthy receipt exists. Query the target by identity and match target, scope and digest; the query must be authoritative, not an eventually consistent search or ambiguous state. Only an authoritative "not committed" makes it retry-safe.
- **Unresolved/manual:** the record is unavailable or inconclusive, identity or digest mismatch, retention expired, or state cannot tell this operation from a similar one. Stop sends, keep evidence and return the declared unresolved outcome to the accountable owner. A new operation, changed intent or compensation is a new decision, not a retry reusing the approval.

Without native idempotency, a jointly designed target-side record or lookup can still reconcile authoritatively; a local record alone proves nothing. With neither, make the action manual or redesign the interface; do not rely on timing.

Compensation is a separate operation and does not erase uncertainty. Use it only for a known effect with a permitted reversal, with its own identity, authorization and evidence; never for an effect that may not have happened or a reversal that causes different harm.

### Multi-step effects: outbox and sagas

- **Transactional outbox.** Write the outgoing message in the same local transaction as your state change and let a relay publish it, so the intent to publish is recorded if and only if the transaction commits. Publication itself can still fail or be delayed if the relay crashes or exhausts its retries, so monitor the outbox for unsent rows and recover them. Relays can publish twice, so targets must be idempotent; the row is intent recorded, not a target commit.[3]
- **Sagas.** When no single transaction covers several systems, run local steps, each reversible one with a pre-designed compensating step that runs if a later step fails. Each compensation is a separate operation under EFFECT-04, not an automatic rollback.[4]

## Requirements

- **EFFECT-01 — Stable identity.** For every applicable externally visible effect, the execution path **MUST** create and persist one stable operation identity before the first target-facing attempt. It **MUST** bind the intended target and authority scope, canonical intended arguments or an integrity-preserving digest, and operation version. Retries, recovery attempts, and duplicate deliveries **MUST** reuse that identity; an identity presented with materially different intent **MUST NOT** be treated as the same operation.

- **EFFECT-02 — Declared retry disposition.** For every applicable operation, the tool or action contract **MUST** declare whether it is retry-safe, reconcile-first, or unresolved/manual after a missing or ambiguous receipt. Automatic retry **MUST** be limited to the retry-safe disposition, using the original identity and canonical intent. A transport timeout, process failure, or missing local receipt **MUST NOT** by itself authorize a repeat of an unsafe effect.

- **EFFECT-03 — Authoritative reconciliation.** When an operation is reconcile-first, the execution path **MUST** query an identified authoritative target record or state oracle before any further send. It **MUST** verify the returned operation identity and intent binding before recording completion. If the oracle cannot establish committed or not-committed status, the path **MUST** produce the declared unresolved/manual outcome and preserve the operation record and evidence for follow-up.

- **EFFECT-04 — Compensation boundary.** When a completed external effect is reversible, the action design **SHOULD** define whether compensation is permitted, its preconditions, and its authoritative success evidence. A compensation step **MUST NOT** be used as an automatic response to an unknown outcome, and any compensation that is itself externally visible **MUST** satisfy EFFECT-01 through EFFECT-03.

- **EFFECT-05 — Failure evidence.** Before an applicable action is released or materially changed, its evaluation evidence **MUST** include injected failure at the target-commit/receipt-record boundary, duplicate delivery, and an unresolved-oracle path. Tests **MUST** check the authoritative target state or accepted-operation record and the declared terminal disposition, not only the agent transcript or local step status. For fixtures, evaluators and release decisions, see [Part 4](../../development-guide/04-testing-and-evaluation/README.md).

## Worked example: a policy update with a lost receipt

In this fictional fixture, `travel-policy-current` permits a London hotel amount of GBP 220 and `travel-policy-superseded` differs. A human-governed policy assistant prepares an approved update adding an effective-date clarification to `travel-policy-current`, amount unchanged, with approval and authorization checked per 7.3. Before writing, the workflow records:

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

The store accepts the update, creates revision 43 and logs the identity and digest in its ledger, but the response is lost before the receipt is saved. On recovery the state is `unknown`, not `not_committed`. The workflow queries the store by identity, finds revision 43 with matching target, tenant and digest, and records `completed_reconciled` without resending.

If the store reports authoritatively that nothing committed, the workflow resends the unchanged request and identity. If it is unavailable, returns a different digest or cannot distinguish the update, the workflow returns `unresolved_manual` and writes nothing; the operator inspects the target and may start a new authorized operation. Compensation waits until the effect is known and allowed.

## Evidence and checklist

Use a resettable target fixture with an accepted-operation ledger or other documented state oracle:

- Lose the response after revision 43 commits: assert one accepted operation, matching identity and digest, `completed_reconciled` and no second write.
- Deliver the same identity and intent twice: the target returns the first result with no new revision. The same identity with altered intent is rejected or unresolved, never merged.
- Fail before commit: retry with the same identity only after the authoritative query shows nothing committed, producing one accepted effect.
- Make the oracle unavailable or ambiguous: assert `unresolved_manual`, no further send, and retained evidence.
- Test compensation on a known effect and check the authoritative result; a local `compensated` status is not a pass.
- Record the target's duplicate behavior, retention period and reconciliation source, and link results to the evaluated action version.

## References

[1]: https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2 "HTTP Semantics"
[2]: https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header "The Idempotency-Key HTTP Header Field"
[3]: https://microservices.io/patterns/data/transactional-outbox.html "Pattern: Transactional outbox"
[4]: https://microservices.io/patterns/data/saga.html "Pattern: Saga"

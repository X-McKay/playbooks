# Fictional readiness-review examples

These examples illustrate packet structure only. They are not executed evidence,
release approval, an operating observation, or a statement about any real agent.

## Evidence gap: `no_go`

A proposed read-only policy assistant supplies a code digest, resolved source filter,
and a Part 4 report. The report identifies the same candidate but says its required
semantic-support evaluator has **missing required valid evidence**. The review packet:

- preserves the Part 4 `no_go` and the missing-evidence identifier;
- marks the affected readiness item `unmet` and adds it to `blockers`;
- records a proposed isolated stage but does not treat the plan as evidence; and
- recommends `no_go` for the named candidate and scope.

A positive permission-check result and polished generated packet do not fill the
semantic-evidence gap.

## Conditional obligation is not a deferred gate

A candidate has a candidate-specific Part 4 conclusion, tested disable evidence, and
all pre-release controls. The governing policy permits a post-release review of an
already-enabled diagnostic report. The packet records the report's owner, due date,
monitoring signal, and consequence if late. It may contain a scoped `conditional_go`
recommendation only if the policy permits it.

If the missing item instead were the required disable test, required authorization, or
critical-slice evaluation, it would remain a blocker and the recommendation would be
`no_go`, not `conditional_go`.

## Active effect path: stage and recovery evidence

A candidate can update an external policy record. Its staged plan names a limited
canary population, promotion/stop criteria, the decision role, and a disable route.
The support/disable assessment links a tested stop result and an effect record showing
how an in-flight, uncertain update reaches reconciliation rather than automatic retry.
A rollback pointer alone is not evidence that active work or an uncertain update was
reversed.

## Unapproved exception

A reviewer finds an item that a local policy might allow to be excepted. The packet
uses `exception_proposed`, records the requested scope and missing external approval,
and recommends `no_go` while that approval is absent. It never uses the proposal for a
prohibited use, a mandatory floor, a required authorization, a non-waivable hard gate,
or missing required valid evidence.

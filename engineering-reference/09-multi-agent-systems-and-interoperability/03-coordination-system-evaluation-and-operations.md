# 9.3 Coordination, System Evaluation, and Operations

**Status:** 0.5.0-draft.2 — draft
**Audience:** System builders, evaluators, operators, and accountable owners
**Applicability:** All multi-agent systems. Durable-coordination requirements apply to long-running or state-changing work; operation and release requirements to deployed or release-candidate systems.

[Part 9](README.md) · [Applicability](../../applicability.md) · [9.1 System contracts](01-when-multiple-agents-help-topologies-and-system-contracts.md) · [9.2 Delegation and handoffs](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [Part 4 release evidence](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

Members that pass their own tests do not make a working system: the system can route a good result wrongly, lose a constraint in a handoff, accept stale shared state, wait forever for a branch, or consult an "optional" reviewer after the answer is out.

This chapter adds system-level coordination, evidence and operations to the topology and interfaces from [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md) and [9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md); Parts 4, 5 and 7 still apply to each member. A small, bounded, read-only composition can be ephemeral but still needs a state owner, terminal outcomes, controlled handoffs, correlated evidence and tests of its claims. Long-running work, external changes, approval waits or cross-failure recovery bring in the durable-execution chapters, and composition never avoids a member's execution class or governance obligations.

## Working model

The unit of control is a **versioned composition**: the resolved members, roles, permitted edges, schemas, policies, limits and member identities that may handle a run. A static system resolves it before the run; if membership or edges can change mid-run, also record each admitted change with its evidence and policy version. A later registry answer, recommendation or trace view must not rewrite a completed run's history.

### Coordinate proposals through an accepted state

Members propose routes, facts, conflicts, actions and next steps; a deterministic control boundary decides whether each becomes accepted state. This matters most with concurrent branches:

- **Proposed:** an untrusted claim from a member, tool or message.
- **Observed:** what a permitted boundary received or did.
- **Verified:** passed the declared check for its claim.
- **Accepted:** the version later policy decisions may use.

These are evidence states, not universal truth. Shared state keeps provenance, owner, freshness and conflict status; an aggregator can keep two incompatible interpretations and return `needs_information` or escalate rather than take the first to arrive. A reviewer vote feeds a conflict policy; it is neither authorization nor proof of support.

Declare branch order, aggregation rule, barriers, maximum depth and fan-out, no-progress condition and terminal states up front. If completion order picks the winner, timing becomes undeclared business policy; if members call each other directly, they bypass the graph, budget, authority and evidence controls.

### Evaluate the integration claim

Test the claimed benefit (better source handling, a class of caught errors, less active time) against the 9.1 baseline with the same sources, tools and constraints, so the system cannot win merely through broader capability.

Apply Part 4's claim-to-evaluator method at the layer where behavior occurs. Deterministic tests cover permitted edges, schema validation, authority attenuation, budgets, branch limits and termination. Interaction tests with recorded or simulated member results reproduce dropped constraints, late or malformed results and unavailable members. End-to-end evaluations test the integrated outcome and claimed benefit; a semantic evaluator or expert can judge evidence support but cannot establish an authorization or state-transition property. Start early with a few realistic cases, since large effects show in a few runs, and scale later.[4]

A study of more than 1,600 annotated traces from seven frameworks (MAST) grouped 14 failure modes into system design issues (disobeyed task or role specifications, repeated steps, lost history, not knowing when to stop), inter-agent misalignment (derailment, withheld information, ignored input, not asking for clarification) and task verification failures (missing or wrong checks, stopping early).[1] Map each category to at least one case or trace detector.

When an outcome is wrong, find the **first point of failure** (routing or decomposition, handoff, member behavior, aggregation or review, termination), keep the evidence, and add the narrowest regression that reproduces it; a handoff isolatable with fixed member outputs does not need a new end-to-end case.

### Operate the graph as well as the answer

So operators can trace a symptom to its run, a root run record links the manifest, graph version, member and interaction identities, delegation parentage, policy decisions, state transitions, budget, terminal outcome and evidence references. Traces help diagnosis, especially for asynchronous work, and standard conventions exist for agent and model spans,[2] but they do not replace authoritative state, an interaction ledger or the audit record. Messages, retrieved content and summaries are untrusted and possibly sensitive: prefer typed decisions, safe summaries, evidence references, hashes and stated rationales over full content or private reasoning.

Classify members and checks as required, optional, substitutable or advisory before a fault. A missing required role shows as a missing guarantee, never relabelled as success to meet an availability target, and the same holds for partial effects, cancellation, unknown cost and budget exhaustion. Carry Part 7 effect reconciliation and [8.4](../08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md) admission outcomes across the graph rather than hide them in a branch, and bound retries and fan-out graph-wide, since one branch's failure can cascade.[3]

## Decisions and best practices

- **One authoritative owner per kind of state:** accepted evidence, graph changes, conflict decisions, budget reservations and the final outcome (not necessarily each member's internals). A short static request needs only a small deterministic controller and bounded record; durable work needs a replay-safe coordination boundary with enough persisted information to resume. A message bus, trace tree or agent prose is not authoritative by default.
- **Failure propagation is a product decision.** Decide whether a failed role blocks completion, has an evaluated substitute, allows a labelled partial answer or escalates; how cancellation reaches active descendants; and that late results are recorded for diagnosis but never revive a cancelled branch or overwrite accepted state. Effects use stable identities and [7.2](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md) reconciliation; a missing receipt does not show no effect.
- **Test economically without shrinking the claim.** Use member doubles for schema, policy, routing, handoff, aggregation and fault tests, and real members for member behavior, routing, retrieval and end-to-end claims. Re-record doubles when member versions or contracts change. For variable routing or concurrency, declare repeated trials in advance and report distributions and critical failures, not a favorable average.
- **Treat graph drift as a signal.** A new role, member, edge, depth, fan-out pattern, substitution or termination shift matters even if answer quality holds: investigate, roll back, quarantine, tighten policy or ship a reviewed change, never auto-accept a compatibility claim.

## Requirements

- **SYSTEM-01 — Controlled composition state (MUST).** Applies to every multi-agent system. The system **MUST** identify its versioned composition, permitted interaction graph, terminal-outcome taxonomy, and the deterministic authority that accepts validated member results and applies routing, aggregation, conflict, scheduling, and termination policy. Member output, tool output, and inter-agent messages **MUST NOT** change authoritative system state until the declared validation and transition rule accepts them.

- **SYSTEM-02 — Shared state and conflict handling (MUST).** Applies when members share mutable state, consume common artifacts, or can produce competing results. The system **MUST** define the record schema, state owner and permitted writers, provenance and data classification, freshness rule, conflict-resolution rule, and unresolved-conflict outcome for that state. It **MUST** preserve material uncertainty and dissent where the aggregation policy needs them, and **MUST NOT** make incidental message or completion order an undeclared resolution rule.

- **SYSTEM-03 — Durable coordination and failure propagation (MUST).** Applies when the composed work is long-running, state-changing, side-effecting, waits for approval, or must resume after failure. The system **MUST** apply the applicable Part 7 recovery, effect, and approval controls to the root and each relevant interaction; record stable system, graph, delegation, branch, and operation identities; and define retry ownership, cancellation propagation, partial-effect treatment, and reconciliation. It **MUST NOT** retry an unsafe or unknown external effect merely because a branch lacks a completion receipt.

- **SYSTEM-04 — Composition evaluation (MUST).** Applies to a release candidate or material change to a multi-agent system. The evaluation plan **MUST** test the system's claimed composition benefit against the simpler baseline selected under Chapter 9.1, as well as member, interaction, coordination, end-to-end, and applicable recovery and adversarial behavior. Deterministic properties **MUST** have deterministic checks. The plan **MUST** map material system risks to cases, evaluators, expected invariants, and the authoritative source used to judge any claimed state or effect.

- **SYSTEM-05 — Graph-correlated operations (MUST).** Applies to every deployed multi-agent system. The system **MUST** extend the Part 5 operational record with correlation from the root task to material delegations, members, graph versions, accepted state transitions, policy decisions, budgets, and terminal outcome. It **MUST** record graph changes and preserve evidence sufficient to attribute a confirmed failure to its first observed point. Diagnostic collection **MUST** follow the applicable privacy, retention, access, and audit policy; it **MUST NOT** require private model reasoning or unrestricted message capture.

- **SYSTEM-06 — Release evidence for the exact composition (MUST).** Applies to a production release or a material composition change. The release decision **MUST** identify the exact composition or run-admission envelope, resolved member identities, relevant policies and limits, case and evaluator versions, and system-level results. A failed applicable hard gate, missing required system evidence, or unevidenced claimed control **MUST** produce `no_go` or the applicable blocking state under Part 4 and Part 5; average member quality, a quorum, or a generic exception **MUST NOT** compensate for it.

## Worked example

The fictional read-only policy assistant has two roles. A **retrieval role** returns permission-filtered excerpts with source identity and freshness metadata; an **answer-checking role** checks the proposed response against the returned current evidence. A deterministic controller admits only those two static edges, sets request and tenant context outside model text, and accepts an answer only after both typed results validate.

For the `travel-policy-current` fixture, retrieval returns a current London hotel limit of GBP 220 and a superseded document with a different amount. The shared evidence record keeps both identities and marks the older one superseded. The checker receives the answer, cited current source and conflict record, with no unrelated history and no other source access. The controller accepts `complete` only if the answer names GBP 220, cites the current source and explains the conflict.

The baseline is one role with the same access, filter, contract and limits; the question is whether the boundary improves source handling enough to justify its latency, cost and failure modes:

1. A deterministic graph test denies an undeclared direct retrieval-to-checker call and rejects mismatched schemas or tenants.
2. A handoff test with fixed retrieval output asserts the checker receives the current-source identity, freshness metadata and conflict marker, exposing information loss without running either role.
3. An end-to-end held-out case checks that the answer is supported by the current source and states the required uncertainty, using the declared source comparison or a qualified reviewer, not citation presence.
4. A checker outage yields `needs_information` or another declared non-success outcome recording the missing check, never an unchecked `complete`.
5. The release record binds the composition version, both member versions, the baseline configuration, fixture versions, evaluator decision and outcome distributions. A failed authorization, tenant-isolation or required-handoff gate blocks release whatever the average score.

With no writes, the composition is ephemeral; a version applying approved updates becomes durable and human-governed, keeping the approval binding and reconciling unknown results rather than resubmitting.

## Evidence and checklist

Keep the composition identity, state and conflict policy, interaction and terminal-outcome definitions, risk-to-case mapping, results at each layer, fault and recovery results, baseline comparison, graph-correlated records and the release decision. Evidence for a nearby topology or earlier member version does not cover the candidate.

- [ ] Required, optional, substitutable and advisory interactions have failure and cancellation behavior.
- [ ] Each failure-taxonomy category maps to a case or trace detector.
- [ ] Critical failures and inconclusive results are visible, not averaged away.
- [ ] Durable replay, effect reconciliation, approval, capacity, incident and kill-switch evidence links to the exact candidate where it applies.

See [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) for persistence and replay and [10.1](../10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) for the full risk method.

## References

[1]: https://arxiv.org/abs/2503.13657 "Why Do Multi-Agent LLM Systems Fail?"
[2]: https://opentelemetry.io/docs/specs/semconv/gen-ai/ "OpenTelemetry semantic conventions for generative AI"
[3]: https://sre.google/sre-book/addressing-cascading-failures/ "Addressing Cascading Failures"
[4]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"

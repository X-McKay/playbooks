# 9.3 Coordination, System Evaluation, and Operations

**Status:** 0.5.0-draft.2 — draft
**Audience:** System builders, evaluators, operators, and accountable owners
**Applicability:** All multi-agent systems. Durable-coordination requirements apply when the composed work is long-running or state-changing. Operation and release requirements apply when the system is deployed or proposed for release.

[Part 9](README.md) · [Applicability](../../applicability.md) · [9.1 System contracts](01-when-multiple-agents-help-topologies-and-system-contracts.md) · [9.2 Delegation and handoffs](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [Part 4 release evidence](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

A composition is a system, not a set of agents that each pass their own tests. A member can return a well-formed result while the system sends it to the wrong recipient, loses a constraint in a handoff, accepts stale shared state, waits forever for a branch, or consults a supposedly optional reviewer after the answer is already out. Passing member evaluations does not show that the composition is useful, bounded, or operable.

This chapter adds system-level coordination, evidence, and operating decisions, after the topology and interfaces of [9.1](01-when-multiple-agents-help-topologies-and-system-contracts.md) and [9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md) are chosen. General evaluation method is in Part 4, minimum operational controls in Part 5, and recovery and external-effect rules in Part 7. Apply those to each member and add the composition evidence described here.

Not every composition needs a durable workflow. A small, read-only, bounded request can be ephemeral, but it still needs a declared state owner, terminal outcomes, controlled handoffs, correlated evidence, and tests of the claims made for adding members. Long-running work, externally visible state changes, approval waits, or recovery across a failure boundary bring in the durable-execution chapters. Composition cannot be used to avoid a member's execution class or governance obligations.

## Working model

The unit of control is a **versioned composition**: the resolved members, roles, permitted edges, interaction schemas, policies, limits, and member identities that may handle a run. A static system can resolve this before the run. If membership or edges can change during a run, also keep a run record of each admitted change with the evidence and policy version behind it. A later registry answer, agent recommendation, or trace view must not rewrite the history of a completed run.

### Coordinate proposals through an accepted state

Members may propose routes, facts, conflicts, actions, and next steps. A deterministic control boundary decides whether each proposal is permitted, valid, and ready to become accepted state. This matters most when branches run concurrently:

- **Proposed** material is an untrusted claim from a member, tool, or message.
- **Observed** material records what a permitted boundary received or did.
- **Verified** material has passed the declared check for its claim.
- **Accepted** material is the version the system may use for later policy decisions.

These are states of evidence, not claims of universal truth. Shared state keeps its provenance, owner, freshness, and conflict status. For example, an aggregator can keep two incompatible document interpretations and return `needs_information` or escalate, instead of picking whichever arrived first. A reviewer vote is an input to a conflict policy; it is not authorization and not proof that a claim is supported.

Declare coordination up front: branch order, aggregation rule, required barriers, maximum depth and fan-out, no-progress condition, and terminal states. If completion order picks the winner, timing becomes an undeclared business policy. If one member can call another directly, it bypasses the graph, budget, authority, and evidence controls that made the composition reviewable.

### Evaluate the integration claim

Start with the benefit claimed for the composition. A retrieval specialist plus an answer checker may claim better source handling; a reviewer may claim to catch one class of error; parallel roles may claim less active time. Each claim needs the simpler baseline from 9.1 and composition-level cases. Give the baseline the same permitted sources, tools, and constraints; otherwise the system may win because it had broader capability, not because coordination helped.

Use the Part 4 claim-to-evaluator method at the layer where the behavior occurs. Deterministic tests cover permitted edges, schema validation, authority attenuation, budget enforcement, branch limits, and termination. Interaction tests can use recorded or simulated member results to reproduce a dropped constraint, late result, malformed output, or unavailable member. End-to-end evaluations test the integrated outcome and the claimed benefit. A semantic evaluator or expert review can judge whether cited evidence supports an answer, but it cannot establish a deterministic authorization or state-transition property. Start with a small set of realistic cases early, since large effects show up in a few runs, and add scale later. [4]

Use a published failure taxonomy to decide what to test and monitor. A study of more than 1,600 annotated traces from seven multi-agent frameworks (MAST) grouped 14 failure modes into three categories: system design issues (such as repeated steps or not knowing when to stop), inter-agent misalignment (such as dropped context or ignoring another agent's input), and task verification failures (such as weak or missing checks, or stopping early). [1] Map each category to at least one case or trace detector for your system.

When an outcome is wrong, find the **first point of failure**: routing or decomposition, handoff, member behavior, aggregation or review, or termination. Keep the evidence behind that attribution, then add the narrowest regression that reproduces it. A new end-to-end case is a poor fix for a handoff you could isolate with fixed member outputs.

### Operate the graph as well as the answer

Operators must be able to go from a symptom to the composition and run that produced it. A root run record connects the composition or run manifest, graph version, member and interaction identities, delegation parentage, policy decisions, state transitions, budget use, terminal outcome, and evidence references. Traces help with diagnosis, especially for asynchronous work, and standard conventions exist for agent and model spans. [2] But traces do not replace authoritative state, an interaction ledger, or the audit record.

Collect the minimum needed. Inter-agent messages, retrieved content, and summaries are untrusted and can be sensitive. Full content capture or private model reasoning is not a default requirement. Typed decisions, safe summaries, evidence references, hashes, and externally meaningful rationales usually serve investigation better and are easier to govern.

Set a failure policy before a fault occurs. Classify members and checks as required, optional, substitutable, or advisory. If a required role is down, the outcome must show the missing guarantee and must not be relabelled as ordinary success to meet an availability target. The same holds for partial effects, cancellation, unknown cost, and budget exhaustion. Part 7 covers reconciling an uncertain external effect, and [8.4](../08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md) covers shared-capacity admission and backpressure. The composition must carry their outcomes and evidence across its graph and not hide them in a branch. A failure in one branch can cascade through the rest, so bound retries and fan-out across the whole graph. [3]

## Decisions and best practices

Choose one authoritative owner for each kind of system state. A coordinator need not own each member's internal state, but the system must say who owns accepted evidence, graph changes, conflict decisions, budget reservations, and the final outcome. For a short static request, a small deterministic controller and a bounded record are enough. For durable work, use a replay-safe coordination boundary with the persisted information needed to resume safely. Do not let a message bus, trace tree, or agent prose become authoritative state by default.

Make failure propagation a product decision. Decide whether a failed role blocks completion, has an evaluated substitute, allows a clearly labelled partial answer, or needs escalation. Define how cancellation reaches active descendants and how late results are treated. A late result may be recorded for diagnosis but must not revive a cancelled branch or overwrite later accepted state. If the system has effects, use stable interaction and operation identities and the reconciliation rules in [7.2](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); a missing receipt does not show that an effect did not happen.

Test economically without shrinking the claim. Run schema, policy, routing, handoff, aggregation, and fault-injection tests with controlled member doubles where they can answer the question. Re-run real members and full-system evaluations where member behavior, routing, retrieval, or the end-to-end claim is in question. Re-record a controlled member result when the member version or its material contract changes. For variable routing or concurrency, declare the repeated-trial policy in advance and report distributions and critical failures, not a favorable average.

Treat graph drift as an operational signal. A new role, member, edge, depth, fan-out pattern, substitution, or change in termination distribution can matter even if final-answer quality has not moved. Respond with investigation, an evaluated rollback, quarantine, a tighter policy, or a reviewed release change, never automatic acceptance because a member claims compatibility. Treat material composition changes like a new candidate.

## Requirements

- **SYSTEM-01 — Controlled composition state (MUST).** Applies to every multi-agent system. The system **MUST** identify its versioned composition, permitted interaction graph, terminal-outcome taxonomy, and the deterministic authority that accepts validated member results and applies routing, aggregation, conflict, scheduling, and termination policy. Member output, tool output, and inter-agent messages **MUST NOT** change authoritative system state until the declared validation and transition rule accepts them.

- **SYSTEM-02 — Shared state and conflict handling (MUST).** Applies when members share mutable state, consume common artifacts, or can produce competing results. The system **MUST** define the record schema, state owner and permitted writers, provenance and data classification, freshness rule, conflict-resolution rule, and unresolved-conflict outcome for that state. It **MUST** preserve material uncertainty and dissent where the aggregation policy needs them, and **MUST NOT** make incidental message or completion order an undeclared resolution rule.

- **SYSTEM-03 — Durable coordination and failure propagation (MUST).** Applies when the composed work is long-running, state-changing, side-effecting, waits for approval, or must resume after failure. The system **MUST** apply the applicable Part 7 recovery, effect, and approval controls to the root and each relevant interaction; record stable system, graph, delegation, branch, and operation identities; and define retry ownership, cancellation propagation, partial-effect treatment, and reconciliation. It **MUST NOT** retry an unsafe or unknown external effect merely because a branch lacks a completion receipt.

- **SYSTEM-04 — Composition evaluation (MUST).** Applies to a release candidate or material change to a multi-agent system. The evaluation plan **MUST** test the system's claimed composition benefit against the simpler baseline selected under Chapter 9.1, as well as member, interaction, coordination, end-to-end, and applicable recovery and adversarial behavior. Deterministic properties **MUST** have deterministic checks. The plan **MUST** map material system risks to cases, evaluators, expected invariants, and the authoritative source used to judge any claimed state or effect.

- **SYSTEM-05 — Graph-correlated operations (MUST).** Applies to every deployed multi-agent system. The system **MUST** extend the Part 5 operational record with correlation from the root task to material delegations, members, graph versions, accepted state transitions, policy decisions, budgets, and terminal outcome. It **MUST** record graph changes and preserve evidence sufficient to attribute a confirmed failure to its first observed point. Diagnostic collection **MUST** follow the applicable privacy, retention, access, and audit policy; it **MUST NOT** require private model reasoning or unrestricted message capture.

- **SYSTEM-06 — Release evidence for the exact composition (MUST).** Applies to a production release or a material composition change. The release decision **MUST** identify the exact composition or run-admission envelope, resolved member identities, relevant policies and limits, case and evaluator versions, and system-level results. A failed applicable hard gate, missing required system evidence, or unevidenced claimed control **MUST** produce `no_go` or the applicable blocking state under Part 4 and Part 5; average member quality, a quorum, or a generic exception **MUST NOT** compensate for it.

## Worked example

The internal policy assistant stays read-only. Its bounded composition has two roles: a **retrieval role** returns permission-filtered policy excerpts with source identity and freshness metadata, and an **answer-checking role** checks whether the proposed response is supported by the returned current evidence. A deterministic system controller admits only those two static edges, sets the request and tenant context outside model-generated text, and accepts an answer only after the typed retrieval and checking results validate. The fixture below is fictional.

For the `travel-policy-current` fixture, the retrieval role returns a current London hotel limit of GBP 220 and also finds a superseded document with a different amount. The shared evidence record keeps both source identities and marks the older document superseded under the fixture's freshness rule. The checking role gets the proposed answer, its cited current source, and the conflicting-source record, with no unrelated user history and no permission to query other sources. The controller accepts `complete` only if the checker confirms that the answer names GBP 220, cites the current source, and does not hide the conflict without explanation.

The simpler baseline is one policy-assistant role with the same approved document access, permission filter, answer contract, and limits. The comparison asks whether the added retrieval and checking boundary improves source handling enough to justify its extra latency, cost, and failure modes. An evidence plan:

1. A deterministic graph test denies an undeclared direct call from the retrieval role to the checker and rejects a result with a mismatched schema or tenant.
2. A handoff test uses fixed retrieval output containing both fixture documents and asserts that the checker receives the current-source identity, freshness metadata, and conflict marker. It can reveal an information-loss defect without running either role.
3. An end-to-end held-out case assesses whether the final answer is supported by the current approved source and states the required uncertainty. Citation presence alone is not proof of support; use the declared source comparison or a qualified reviewer.
4. A required-checker outage test produces `needs_information` or another declared non-success outcome with the missing check recorded. The system does not publish an unchecked answer as `complete` just because retrieval succeeded.
5. The release record binds the static composition version, the two member versions, the baseline configuration, fixture versions, evaluator decision, and outcome distributions. If an authorization, tenant-isolation, or required-handoff gate fails, the candidate is not released even if average answer score improves.

Because the example has no external writes and each request is bounded, it can run as an ephemeral composition. If a later version prepares and applies a human-approved policy update, it becomes a durable, human-governed path: the system records the final action and composition context, keeps the approval binding, and reconciles an unknown update result instead of resubmitting it. The composition does not widen an approval into broader authority or make a lost receipt safe to retry.

## Evidence and checklist

A proportionate evidence set holds the reviewed composition identity; state and conflict policy; interaction and terminal-outcome definitions; the risk-to-case mapping; member, interaction, coordination, and end-to-end results; fault and recovery results where they apply; the baseline comparison; graph-correlated operational records; and the release decision for the evaluated subject. Exact evaluator, fixture, and policy identities matter: evidence for a nearby topology or an earlier member version does not cover the candidate.

Before release or after a material composition change, confirm:

- [ ] The composition's owner, members, permitted edges, limits, terminal outcomes, and accepted-state authority are identified.
- [ ] Shared records have an owner, provenance, data handling, freshness, conflict, and unresolved-outcome policy.
- [ ] Required, optional, substitutable, and advisory interactions have defined failure and cancellation behavior.
- [ ] Deterministic graph, scope, schema, limit, and state-transition claims have deterministic tests; semantic outcome claims have a fit evaluator.
- [ ] The composition and its simpler baseline were evaluated on the same scope, with critical failures and inconclusive results visible and not averaged away.
- [ ] Failure-taxonomy categories (design, misalignment, verification) each map to a case or trace detector.
- [ ] Operators can trace a symptom to its composition, graph, interactions, accepted state, policy decisions, and terminal outcome without collecting unrestricted sensitive content.
- [ ] Durable replay, effect reconciliation, approval, capacity, incident, and kill-switch evidence is linked to the exact candidate where it applies.
- [ ] The release decision names the evaluated composition and treats failed hard gates, missing evidence, and unevidenced controls as blocking.

For deeper work, see [7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) for persistence and replay, [8.4](../08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md) for shared capacity, and [10.1](../10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) for the full system risk method.

## References

[1]: https://arxiv.org/abs/2503.13657 "Why Do Multi-Agent LLM Systems Fail?"
[2]: https://opentelemetry.io/docs/specs/semconv/gen-ai/ "OpenTelemetry semantic conventions for generative AI"
[3]: https://sre.google/sre-book/addressing-cascading-failures/ "Addressing Cascading Failures"
[4]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"

# 9.3 Coordination, System Evaluation, and Operations

**Status:** 0.5.0 first draft
**Audience:** System builders, evaluators, operators, and accountable owners
**Applicability:** All multi-agent systems. Durable-coordination requirements apply when the composed work is long-running or state-changing; production-operation and release requirements apply when the system is deployed or proposed for release.

[Part 9](README.md) · [Applicability](../../applicability.md) · [9.1 System contracts](01-when-multiple-agents-help-topologies-and-system-contracts.md) · [9.2 Delegation and handoffs](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [Part 4 release evidence](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

A composition is a system, not a collection of independently successful agents. A member can return a well-formed result while the system routes it to the wrong recipient, loses a constraint during a handoff, accepts stale shared state, waits forever for a branch, or calls a supposedly optional reviewer after the answer has already been exposed. Passing member evaluations therefore does not establish that the composition is useful, bounded, or operable.

This chapter adds the system-level coordination, evidence, and operating decisions that apply after the topology and interfaces in Chapters 9.1 and 9.2 are chosen. It does not replace their member contracts, authority attenuation, or typed interaction boundaries. It also does not duplicate the general evaluation method in Part 4, minimum operational controls in Part 5, or the recovery and external-effect rules in Part 7. A system applies those chapters to each member and adds the composition evidence described here.

Not every composition needs a durable workflow. A small, read-only, bounded request may be ephemeral. It still needs a declared state owner, terminal outcomes, controlled handoffs, correlated evidence, and tests of the claims made for adding members. Long-running work, externally visible state changes, approval waits, or recovery across a failure boundary trigger the durable-execution chapters; the system cannot use composition to evade its members' applicable execution class or governance obligations.

## Working model

The practical unit of control is a **versioned composition**: the resolved members, roles, permitted edges, interaction schemas, policies, limits, and relevant member identities that may handle a run. A static system can resolve this before the run. If membership or edges can change during a run, the system also needs a run record that captures each admitted change and the evidence and policy version behind it. A later registry answer, agent recommendation, or trace view must not silently rewrite the history of a completed run.

### Coordinate proposals through an accepted state

Members may propose routes, facts, conflicts, actions, and next steps. A deterministic control boundary decides whether each proposal is permitted, valid, and ready to become accepted state. This distinction matters most when branches run concurrently:

- **Proposed** material is an untrusted claim from a member, tool, or message.
- **Observed** material records what a permitted boundary received or did.
- **Verified** material has passed the declared check for its claim.
- **Accepted** material is the version that the system may use for subsequent policy decisions.

These are states of evidence, not a claim that the result is universally true. Shared state must retain its provenance, owner, freshness, and conflict status. For example, an aggregator may preserve two incompatible document interpretations and return `needs_information` or escalate rather than pick the answer that arrived first. A reviewer vote is an input to a conflict policy, not authorization and not proof that a claim is supported.

Coordination should be logical rather than accidental. Define the branch order, aggregation rule, required barriers, maximum depth and fan-out, no-progress condition, and terminal states before execution. Letting completion order choose a winner makes timing an undeclared business policy. Letting a member directly call another member bypasses the graph, budget, authority, and evidence controls that made composition reviewable in the first place.[1]

### Evaluate the integration claim

Start with the benefit claimed for the composition. A retrieval specialist plus an answer checker may claim better source handling; a reviewer may claim to detect a particular class of error; parallel roles may claim to reduce active time. Each claim needs a simpler baseline from Chapter 9.1 and composition-level cases. The baseline normally receives equivalent permitted sources, tools, and constraints. Otherwise, a system can appear to win because it was given a broader capability rather than because coordination helped.

Use the Part 4 claim-to-evaluator method at the layer where the behavior occurs. Deterministic tests establish properties such as permitted edges, schema validation, authority attenuation, budget enforcement, branch limits, and termination. Interaction tests can use recorded or simulated member results to make a dropped constraint, late result, malformed output, or unavailable member reproducible. End-to-end evaluations test the integrated outcome and the claimed benefit. A semantic evaluator or expert review may assess whether cited evidence supports the answer, but it cannot establish a deterministic authorization or state-transition property.[2]

When an outcome is wrong, locate the **first point of failure**: routing or decomposition, handoff, member behavior, aggregation or review, or termination. Preserve the evidence needed to support that attribution, then add the narrowest regression that reproduces it. A new end-to-end case alone is a poor repair for a handoff that can be isolated with fixed member outputs.

### Operate the graph as well as the answer

Operators need to move from a system symptom to the composition and run that produced it. A root run record should connect the composition or run manifest, graph version, member and interaction identities, delegation parentage, policy decisions, state transitions, budget use, terminal outcome, and relevant evidence references. Traces are useful diagnostics, especially for asynchronous work, but they do not replace authoritative state, an interaction ledger, or the audit record.[3]

Collect the minimum data necessary to answer those questions. Inter-agent messages, retrieved content, and summaries remain untrusted data and can also be sensitive. Capture of full content or private model reasoning is not a default observability requirement. Typed decisions, safe summaries, evidence references, hashes, and externally meaningful rationales are generally more useful for investigation and can be governed by the applicable data policy.

System operations also need an explicit failure policy. Classify members and checks as required, optional, substitutable, or advisory before a fault occurs. If a required role is unavailable, the outcome should expose the missing guarantee; it must not be relabelled as an ordinary success to satisfy an availability target. The same principle applies to partial effects, cancellation, unknown cost, and budget exhaustion. Part 7 owns how a durable system reconciles an uncertain external effect; Part 8.4 owns shared-capacity admission and backpressure. This chapter requires the composition to propagate their outcomes and evidence across its graph rather than hiding them in a branch.[1][4]

## Decisions and best practices

Choose one authoritative owner for each kind of system state. A coordinator need not own every member's internal state, but the system must state who owns accepted evidence, graph changes, conflict decisions, budget reservations, and the final outcome. For a static, short request, this can be a small deterministic controller and a bounded record. For durable work, it is a replay-safe coordination boundary with the persisted information needed to resume safely. Do not make a message bus, a trace tree, or an agent's prose the authoritative state by implication.

Make failure propagation a product decision. Decide whether a failed role blocks completion, has an evaluated substitute, permits a clearly labelled partial answer, or requires escalation. Also define how cancellation reaches active descendants and how late results are treated. A late result can be recorded for diagnosis, but it must not revive a cancelled branch or overwrite later accepted state. If the system has effects, use stable interaction and operation identities and the reconciliation rules in [Chapter 7.2](../07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md); absence of a receipt is not evidence that an effect did not occur.

Test economically without shrinking the claim. Run schema, policy, routing, handoff, aggregation, and fault-injection tests with controlled member doubles where they can answer the question. Re-run real member and full-system evaluations where member behavior, model routing, retrieval, or the end-to-end claim is at issue. Re-record a controlled member result when the member version or its material contract changes. For variable routing or concurrent behavior, predeclare the repeated-trial policy and report distributions and critical failures rather than relying on a favorable average.[2]

Treat graph drift as an operational signal. A new role, member, edge, depth, fan-out pattern, substitution, or termination distribution can matter even when final-answer quality has not visibly moved. The response may be investigation, an evaluated rollback, quarantine, a tighter policy, or a reviewed release change; it is not automatic acceptance because a member claimed compatibility. Material composition changes require the same evidence discipline as a new candidate.

## Requirements

- **SYSTEM-01 — Controlled composition state (MUST).** Applies to every multi-agent system. The system **MUST** identify its versioned composition, permitted interaction graph, terminal-outcome taxonomy, and the deterministic authority that accepts validated member results and applies routing, aggregation, conflict, scheduling, and termination policy. Member output, tool output, and inter-agent messages **MUST NOT** change authoritative system state until the declared validation and transition rule accepts them.

- **SYSTEM-02 — Shared state and conflict handling (MUST).** Applies when members share mutable state, consume common artifacts, or can produce competing results. The system **MUST** define the record schema, state owner and permitted writers, provenance and data classification, freshness rule, conflict-resolution rule, and unresolved-conflict outcome for that state. It **MUST** preserve material uncertainty and dissent where the aggregation policy needs them, and **MUST NOT** make incidental message or completion order an undeclared resolution rule.

- **SYSTEM-03 — Durable coordination and failure propagation (MUST).** Applies when the composed work is long-running, state-changing, side-effecting, waits for approval, or must resume after failure. The system **MUST** apply the applicable Part 7 recovery, effect, and approval controls to the root and each relevant interaction; record stable system, graph, delegation, branch, and operation identities; and define retry ownership, cancellation propagation, partial-effect treatment, and reconciliation. It **MUST NOT** retry an unsafe or unknown external effect merely because a branch lacks a completion receipt.

- **SYSTEM-04 — Composition evaluation (MUST).** Applies to a release candidate or material change to a multi-agent system. The evaluation plan **MUST** test the system's claimed composition benefit against the simpler baseline selected under Chapter 9.1, as well as member, interaction, coordination, end-to-end, and applicable recovery and adversarial behavior. Deterministic properties **MUST** have deterministic checks. The plan **MUST** map material system risks to cases, evaluators, expected invariants, and the authoritative source used to judge any claimed state or effect.

- **SYSTEM-05 — Graph-correlated operations (MUST).** Applies to every deployed multi-agent system. The system **MUST** extend the Part 5 operational record with correlation from the root task to material delegations, members, graph versions, accepted state transitions, policy decisions, budgets, and terminal outcome. It **MUST** record graph changes and preserve evidence sufficient to attribute a confirmed failure to its first observed point. Diagnostic collection **MUST** follow the applicable privacy, retention, access, and audit policy; it **MUST NOT** require private model reasoning or unrestricted message capture.

- **SYSTEM-06 — Release evidence for the exact composition (MUST).** Applies to a production release or a material composition change. The release decision **MUST** identify the exact composition or run-admission envelope, resolved member identities, relevant policies and limits, case and evaluator versions, and system-level results. A failed applicable hard gate, missing required system evidence, or unevidenced claimed control **MUST** produce `no_go` or the applicable blocking state under Part 4 and Part 5; average member quality, a quorum, or a generic exception **MUST NOT** compensate for it.

## Worked example

The internal policy assistant remains read-only. Its bounded composition has two roles: a **retrieval role** returns permission-filtered policy excerpts with source identity and freshness metadata, and an **answer-checking role** checks whether the proposed response is supported by the returned current evidence. A deterministic system controller admits only those two static edges, assigns the request and tenant context outside model-generated text, and accepts an answer only after the typed retrieval and checking results validate.

For the fictional `travel-policy-current` fixture, the retrieval role returns a current London hotel limit of GBP 220 and also finds a superseded document with a different amount. The shared evidence record retains both source identities and marks the earlier document as superseded under the fixture's freshness rule. The checking role receives the proposed answer, its cited current source, and the conflicting-source record. It does not receive unrelated user history or any permission to query other sources. The controller accepts `complete` only if the checker confirms that the answer names GBP 220, cites the current source, and does not suppress the conflict without explanation.

The system's simpler baseline is one policy-assistant role with the same approved document access, permission filter, answer contract, and limits. The comparison asks a narrow question: does the added retrieval/checking boundary improve the declared source-handling outcome enough to justify its extra latency, cost, and failure modes? It does not assume that two roles are better because they are more elaborate. Results are not asserted here; the following is an illustrative evidence plan, not a measurement claim:

1. A deterministic graph test denies an undeclared direct call from the retrieval role to the checker and rejects a result with a mismatched schema or tenant.
2. A handoff test uses fixed retrieval output containing both fixture documents and asserts that the checker receives the current-source identity, freshness metadata, and conflict marker. This test can reveal an information-loss defect without invoking either role.
3. An end-to-end held-out case assesses whether the final answer is supported by the current approved source and expresses the required uncertainty. Citation presence alone is not treated as proof of support; the semantic claim uses the declared source comparison or qualified reviewer method.
4. A required-checker outage test produces `needs_information` or another declared non-success outcome with the missing check recorded. The system does not publish an unchecked answer as `complete` merely because retrieval succeeded.
5. The release record binds the static composition version, the two member versions, the baseline configuration, fixture versions, evaluator decision, and the outcome distributions. If an applicable authorization, tenant-isolation, or required-handoff gate fails, the candidate is not released even if its average answer score improves.

Because this example has no external writes and each request is bounded, it may run as an ephemeral composition. If a later version prepares and applies a human-approved policy update, it becomes a durable, human-governed path: the system records the final action and composition context, preserves the approval binding, and reconciles an unknown update result rather than blindly submitting the update again. The composition does not turn an approval into broader authority or make a lost receipt safe to retry.

## Evidence and checklist

A proportionate system evidence set contains the reviewed composition identity; state and conflict policy; interaction and terminal-outcome definitions; risk-to-case mapping; member, interaction, coordination, and end-to-end results; fault and recovery results where applicable; baseline comparison; graph-correlated operational records; and the release decision for the evaluated subject. The exact evaluator, fixture, and policy identities matter: evidence for a nearby topology or an earlier member version is not evidence for the candidate being released.

Before release or after a material composition change, confirm:

- [ ] The composition's owner, members, permitted edges, limits, terminal outcomes, and accepted-state authority are identified.
- [ ] Shared records have an owner, provenance, data handling, freshness, conflict, and unresolved-outcome policy.
- [ ] Required, optional, substitutable, and advisory interactions have defined failure and cancellation behavior.
- [ ] Deterministic graph, scope, schema, limit, and state-transition claims have deterministic tests; semantic outcome claims have a fit-for-purpose evaluator.
- [ ] The composition and its simpler baseline were evaluated on the same declared scope, with critical failures and inconclusive results visible rather than averaged away.
- [ ] Operators can correlate a system symptom to its composition, graph, interactions, accepted state, policy decisions, and terminal outcome without collecting unrestricted sensitive content.
- [ ] Applicable durable replay, effect reconciliation, approval, capacity, incident, and kill-switch evidence is linked to the exact candidate.
- [ ] The release decision names the evaluated composition and treats failed hard gates, missing evidence, and unevidenced controls as blocking.

For deeper work, use [Chapter 7.1](../07-durable-execution-and-human-governed-work/01-execution-classes-persistence-and-recovery.md) for persistence and replay, [Chapter 8.4](../08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md) for shared-capacity control, and [Chapter 10.1](../10-risk-privacy-and-specialized-assurance/01-detailed-risk-assessment-and-governance.md) for the full system risk method.

## References

[1]: https://github.com/X-McKay/playbooks/blob/78ec3bd517c52255bced1901b4d00b68c7c18ada/multi-agent/06-durable-coordination.md "Durable coordination"

[2]: https://github.com/X-McKay/playbooks/blob/78ec3bd517c52255bced1901b4d00b68c7c18ada/multi-agent/07-evaluation.md "Multi-agent evaluation"

[3]: https://github.com/X-McKay/playbooks/blob/78ec3bd517c52255bced1901b4d00b68c7c18ada/multi-agent/08-observability.md "Multi-agent observability"

[4]: https://github.com/X-McKay/playbooks/blob/78ec3bd517c52255bced1901b4d00b68c7c18ada/multi-agent/09-cost-and-capacity.md "Multi-agent cost and capacity"

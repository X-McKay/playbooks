# Part 5 practical reference

**Status:** 0.5.0-draft.2 — refined draft companion; proposed, not adopted  
**Purpose:** Connect the Part 5 operating, release, and lifecycle records in one practical sequence without creating a parallel policy or a required record format.  
**Use with:** The [Part 5 overview](../README.md), its owner chapters, the [glossary pointers](../../../glossary.md#part-5-operational-and-lifecycle-foundations), and the [requirement index](../../../requirement-index.md#part-5--release-operations-and-lifecycle).

This reference owns **no requirement IDs**. The owner chapter, its applicability statement, and its `## Requirements` section control if this page or a template is shorter than the proposed requirement. The records are fictional, `illustrative-unexecuted` teaching material; they do not report a production run, evaluation, authorization, deployment, incident, recovery, retirement, control effectiveness, or external effect.

## Use one optional packet

The three companion records share `example_id: POLICY-BUILD-001`, `use_case_id: internal-policy-assistance`, and `packet_id: POLICY-OPS-001`. Treat them as connected views of one optional packet: an operating-control view, a readiness-and-rollout view, and a support/lifecycle view. A builder may combine, adapt, or omit record shapes when they are not applicable; this reference does **not** make three separate files, any file format, or any particular platform mandatory.

The packet concerns a fictional, permission-filtered, read-only internal policy assistant. Its normal fixture distinguishes a current GBP 220 policy source from an approved but superseded GBP 200 record. Only the separate equal-authority current-conflict variant introduces the GBP 260 amendment and expects `needs_information`. The records preserve this controlled-fixture distinction without claiming that an agent ran or that a source, permission boundary, or control was effective.

## Build one release, operations, and lifecycle packet

1. **Plan the operating view.** Use [5.1 Observability, Budgets, and Operational Control](../01-observability-budgets-and-operational-control.md) with the [operating-control record](../../../templates/5.1/operating-control-record.yaml). Relate request, run, and physical attempts; plan bounded signals and applicable resource limits; and state how an authorized stop treats in-flight work. The record's small teaching envelope is illustrative rather than a target or measured performance.
2. **Prepare the readiness handoff.** Use [5.2 Readiness, Change, and Rollout](../02-readiness-change-and-rollout.md) with the [release-and-rollout record](../../../templates/5.2/release-and-rollout-record.yaml). Bind the identified candidate, evidence, effective boundaries, readiness state, proposed exposure, and containment planning. An evaluation `go`, `conditional_go`, or `no_go` remains distinct from release authorization; missing required valid evidence remains blocking rather than becoming a post-release obligation.
3. **Make support and lifecycle decisions usable.** Use [5.3 Ownership, Incidents, Maintenance, and Retirement](../03-ownership-incidents-maintenance-and-retirement.md) with the [support, incident, and retirement record](../../../templates/5.3/support-incident-and-retirement-record.yaml). Name the support and escalation arrangements, preserve hypotheses separately from observations, plan recovery and feedback handoffs, and account for consumers, work, access, data, and evidence before retirement.
4. **Return each linked question to its owner.** Use [Part 3](../../03-security-and-trust-boundaries/README.md) for authority, untrusted content, data handling, and audit evidence; [Part 4](../../04-testing-and-evaluation/README.md) for evaluation design and conclusions; [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) for durable or consequential work; and Parts 8 and 10 when their specific optimization, capacity, risk, privacy, or specialized-assurance triggers apply.

## Packet records

- [Operating-control record](../../../templates/5.1/operating-control-record.yaml) — planned request/run/attempt correlation, distinct outcomes and reasons, bounded aggregate signals, illustrative per-run limits, and stop treatment.
- [Release-and-rollout record](../../../templates/5.2/release-and-rollout-record.yaml) — candidate and source identity, readiness ledger, distinct evaluation and release-decision fields, proportional stage placeholders, and change disposition.
- [Support, incident, and retirement record](../../../templates/5.3/support-incident-and-retirement-record.yaml) — accountable support placeholders, hypothesis-versus-observation separation, feedback and maintenance planning, and conditional retirement handoff.

## Practical review use

Trace one proposed candidate across the packet. A reviewer should be able to see what the records plan to correlate and bound, what is still unresolved, where an evaluation conclusion ends, where release authority would need to begin, and which lifecycle decision has a named owner. A filled illustrative field is a planning or fixture fact, not a completed control, authorization, or outcome.

The packet retains the existing [BOUNDARY-04 refusal-scope ambiguity](../../../draft-notes.md#concrete-unresolved-normative-ambiguities) as a normative question owned by the Part 3 boundary material. Use-specific operational or adoption decisions—such as service objectives, alert conditions, stop and recovery authorities, staffing, exception eligibility, retention, or rollout thresholds—are separate unresolved decisions. They do not resolve, narrow, or replace that ambiguity.

Use the [Part 5 overview](../README.md) for learner, builder, and reviewer routes. Use [Applicability](../../../applicability.md) before treating an optional packet record, specialized owner, or illustrative planning value as universally required.

# Part 5 practical reference

**Status:** 0.5.0-draft.2 — draft  
**Purpose:** Connect the Part 5 operating, release, and lifecycle records in one practical sequence, without a parallel policy or required record format.  
**Use with:** The [Part 5 overview](../README.md), its chapters, the [glossary pointers](../../../glossary.md#part-5-operational-and-lifecycle-foundations), and the [requirement index](../../../requirement-index.md#part-5--release-operations-and-lifecycle).

This reference owns **no requirement IDs**. If this page or a template is shorter than a requirement, the chapter's `## Requirements` section controls. The records are fictional `illustrative-unexecuted` teaching material; they report no production run, evaluation, authorization, deployment, incident, recovery, retirement, or external effect.

## Use one optional packet

The three records share `example_id: POLICY-BUILD-001`, `use_case_id: internal-policy-assistance`, and `packet_id: POLICY-OPS-001`. Treat them as three views of one packet: operating control, readiness and rollout, and support/lifecycle. You may combine, adapt, or omit record shapes; no file layout, format, or platform is required.

The packet concerns a fictional, permission-filtered, read-only internal policy assistant. Its normal fixture separates a current GBP 220 policy source from an approved but superseded GBP 200 record. Only the separate equal-authority conflict variant adds the GBP 260 amendment and expects `needs_information`. The records keep this distinction without claiming that an agent ran or a control worked.

## Build one packet

1. **Plan the operating view.** Use [5.1](../01-observability-budgets-and-operational-control.md) with the [operating-control record](../../../templates/5.1/operating-control-record.yaml). Relate request, run, and attempts; plan bounded signals and resource limits; state how a stop treats in-flight work. The small envelope in the record is a teaching value, not a target.
2. **Prepare the readiness handoff.** Use [5.2](../02-readiness-change-and-rollout.md) with the [release-and-rollout record](../../../templates/5.2/release-and-rollout-record.yaml). Bind the candidate, evidence, boundaries, readiness state, proposed exposure, and containment plan. An evaluation `go`, `conditional_go`, or `no_go` stays distinct from release authorization, and missing required evidence stays blocking.
3. **Make support and lifecycle usable.** Use [5.3](../03-ownership-incidents-maintenance-and-retirement.md) with the [support, incident, and retirement record](../../../templates/5.3/support-incident-and-retirement-record.yaml). Name support and escalation, keep hypotheses apart from observations, plan recovery and feedback, and account for consumers, work, access, data, and evidence before retirement.
4. **Return each question to its owner.** [Part 3](../../03-security-and-trust-boundaries/README.md) for authority, untrusted content, data handling, and audit; [Part 4](../../04-testing-and-evaluation/README.md) for evaluation; [Part 7](../../../engineering-reference/07-durable-execution-and-human-governed-work/README.md) for durable or consequential work; Parts 8 and 10 for optimization, capacity, risk, privacy, or specialized assurance.

## Packet records

- [Operating-control record](../../../templates/5.1/operating-control-record.yaml): request/run/attempt correlation, distinct outcomes and reasons, bounded signals, per-run limits, and stop treatment.
- [Release-and-rollout record](../../../templates/5.2/release-and-rollout-record.yaml): candidate and source identity, readiness ledger, separate evaluation and release-decision fields, stage placeholders, and change disposition.
- [Support, incident, and retirement record](../../../templates/5.3/support-incident-and-retirement-record.yaml): support placeholders, hypothesis-versus-observation separation, feedback and maintenance planning, and retirement handoff.

## Practical review use

Trace one candidate across the packet. A reviewer should see what the records plan to correlate and bound, what is unresolved, where an evaluation conclusion ends, where release authority would begin, and which lifecycle decision has a named owner. A filled field is a planning or fixture fact, not a completed control, authorization, or outcome.

The packet keeps the existing [BOUNDARY-04 refusal-scope ambiguity](../../../draft-notes.md#concrete-unresolved-normative-ambiguities) as an open question owned by Part 3. Use-specific decisions such as service objectives, alert conditions, stop and recovery authorities, staffing, exception eligibility, retention, or rollout thresholds are separate open decisions and do not resolve it.

See the [Part 5 overview](../README.md) for learner, builder, and reviewer routes, and [Applicability](../../../applicability.md) before treating a record, owner, or planning value as universally required.

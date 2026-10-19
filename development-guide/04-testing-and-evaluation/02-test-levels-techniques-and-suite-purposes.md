# 4.2 Test Levels, Techniques, and Suite Purposes

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** When selecting evidence for a claim in an evaluation plan. The level you need depends on the behavior and boundary the claim covers.  
**Reader question:** How do I exercise the system, and how should I organize the checks?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Practical reference](reference/README.md)

Keep three descriptors apart: **level** is the system boundary exercised, **technique** is how a behavior is probed, and **suite purpose** is why a set of cases runs. A case can combine several of each and also carry a lifecycle environment. One label is not evidence for another.

This chapter helps you pick and organize the probe. [4.3](03-evaluation-types-and-dimensions.md) covers what the evidence can establish; [4.6](06-standards-required-coverage-and-execution-cadence.md) sets mandatory coverage; [4.5](05-planning-designing-and-running-tests-and-evaluations.md) covers case identity, fixtures, and resets.

## Levels and boundaries: where the check observes behavior

Use the narrowest level that can establish the claim, then add a broader one when the claim crosses a boundary the narrow check cannot see. A level is not a quality ranking, and passing a lower level says nothing about a wider boundary.

- **Unit-level check:** A small rule or transformation in isolation, such as selecting the current policy revision or evaluating a permission predicate. Fast and precise for deterministic rules. It cannot show that the assembled agent passes the right identity to retrieval.
- **Component-level check:** An assembled capability with controlled collaborators, such as a retriever, source filter, and result formatter. It can reveal mismatched assumptions inside the capability, but not behavior across a separate service or a full user interaction.
- **Integration check:** Crosses one or more real interfaces, with controlled dependencies where useful. Use it for identity propagation, schemas, permission enforcement, timeouts, and how services exchange results. A stubbed boundary cannot stand in for evidence about the real boundary it omits.
- **System or end-to-end check:** The agent and its surrounding system through a user-visible task and the boundaries the claim names. It shows whether an integrated path gives the expected outcome under its fixture. It is not automatically representative of real users, live conditions, or long-run reliability.

Teams use these labels differently, so describe the actual boundary. Acceptance is a decision context or suite purpose here, not a technical boundary. Production monitoring is a lifecycle activity, not a test level.

For each claim, name the boundary that must be observed and the evidence source that can show it. For "a denied source is never disclosed," an isolated permission predicate tests one rule, but the end-to-end claim also needs evidence at the retrieval and output boundaries. Avoid an expensive broad suite when a narrow check is enough, but do not let a narrow check stand in for a wider claim.

## Techniques: how to probe a behavior

Techniques combine at any level. Choose by the claim, the credible failure mode, and what the observation can establish.

### Positive, negative, and boundary cases

A **positive case** exercises an allowed, expected path. Misuse: treating a happy path as proof that denied or ambiguous conditions are safe. Example: ask for the London hotel limit with a current permitted policy and expect a complete answer citing it.

A **negative case** presents a disallowed, unavailable, or contradictory condition and checks the contract-defined safe response. Use it for permissions, missing evidence, and prohibited inputs. Misuse: accepting any refusal as a pass. Balance negative cases with comparable allowed cases so blanket refusal cannot satisfy the claim. This applies to any behavior that should not occur: test both that it happens when it should and that it does not when it should not, or you will optimize one side. Example: remove the user's permission for a source and verify it is not retrieved or disclosed, using the denied-source boundary evidence.

A **boundary case** probes near a meaningful limit or transition: just inside and outside a permission scope, a policy revision going from current to superseded, evidence going from sufficient to missing. Misuse: arbitrary numeric edges, or a boundary with no stated reason. Example: compare a user with approved-policy access to an otherwise identical user without it; inspect the trusted authorization decision and the visible result.

### Property-based checks

A **property-based check** exercises a stated invariant over a deliberately varied set of generated or systematically chosen inputs, not only handpicked examples. Use it when many inputs should obey one simple rule, such as "a source outside the user's permitted scope is never returned." The property and input domain must be clear enough to judge each result. Misuse: many near-duplicates counted as diverse coverage, or broad assurance claimed when the generator misses relevant cases. Keep representative reviewed cases and preserve failures as concrete examples.

### Metamorphic relations

A **metamorphic relation** states how an outcome should relate across a controlled input change. It helps when one exact answer is hard to specify but a relationship can be reviewed. Use invariance for genuinely irrelevant changes and sensitivity for material changes that should alter the result. A paraphrase must really preserve meaning; a permission or current-policy change must not be mislabeled irrelevant. Misuse: assuming similar wording means identical meaning, or treating consistency as correctness. A reviewed paraphrase of the hotel question should keep the supported GBP 220 answer and required source/control relation. A fixture where only a superseded policy is available should give the contract-defined uncertainty or `needs_information` outcome. The method is useful when relations are specified; it does not replace an external truth source or semantic review.[1]

### Controlled fault injection

**Fault injection** introduces a bounded dependency or environment failure to observe safe handling and recovery, such as a retriever timeout, malformed result, or partial response. Misuse: unrealistic faults, several conditions changed at once, or counting a harness failure as an agent result. Example: make the retriever time out; check that the assistant reports the contract-defined unavailable-evidence outcome, invents no definitive limit, and retries or stops only as policy allows. Record whether the dependency actually failed and what reached the agent.

### Concurrency and load techniques

**Concurrency** checks exercise overlapping work; **load** checks vary demand or resource pressure. Use them when a claim involves shared state, tenant isolation, capacity, contention, or demand. Misuse: reading a high-volume run as evidence of unrelated semantic quality, or assuming synthetic load matches real traffic. Example: overlap two reads for different permission contexts against an isolated fixture and verify each gets only its own authorized source. For capacity claims, state the tested workload and observation; no universal throughput or latency threshold applies.

## Suite purposes: why this set is run

A suite is a versioned collection chosen for a goal. The same case may sit in several suites; keep its identity and record each suite's purpose.

- **Smoke:** A small signal that a critical route or dependency is alive. Quick feedback; not evidence of broad behavior, safety, or semantic quality.
- **Development:** Cases that guide iteration and may change as understanding improves. Because they inform tuning, repeated runs do not make them independent evidence.
- **Capability:** Hard cases that the current agent often fails. They show where to improve, so a low pass rate is expected and useful. When the agent passes nearly all of them, the suite is saturated: it can no longer show progress, so add harder cases.
- **Regression:** Reviewed cases kept to catch the return of resolved failures or breaks in stable expectations. The pass rate should stay near 100%, and a drop is a signal. Add a confirmed, understood failure after sanitizing and review. Do not freeze an ambiguous expected result as authoritative. Capability cases whose pass rate saturates can graduate into the regression suite.[2]
- **Release holdout:** Cases reserved for independent evidence about a release claim. Keep them out of tuning of the candidate, prompts, rules, and evaluators behind the reported result. If a holdout informs a change, it is no longer untouched for that candidate; use a new holdout or describe the reuse accurately.
- **Acceptance:** Evidence for a stakeholder or intended-user acceptance decision, possibly with representative user tasks or agreed criteria. A curated acceptance case does not represent all users.
- **Operational learning:** Privacy-appropriate observation after exposure, to find drift, new failure cases, or changing conditions. Define the scope of any live observation. It adds to, and never replaces, required pre-release evidence.

Label suite purpose before reading results, and keep it distinct from environment or stage: "regression" does not mean "production," and "acceptance" does not mean "live." Development cases can become regression cases after review, but do not quietly repurpose a release holdout after results influenced tuning.

## Requirements

- **CASE-04 — Fit-for-claim environments.** For each claim in the evaluation plan, the selected test layer **MUST** be capable of observing the claimed behavior and its relevant boundary. Deterministic rules **SHOULD** have focused unit or component cases; claims that cross interfaces **MUST** have integration evidence; and claims about user-visible agent behavior **MUST** have offline behavioral evidence on controlled cases. User acceptance and production evaluation **MUST** be added when their distinct usefulness or post-launch learning claims are relied upon. The evaluation plan and results **MUST** identify the boundary exercised and the evidence that supports the claim; omitted but otherwise relevant layers **MUST** have a claim-specific rationale.

## Worked example: select checks for the policy assistant

The fictional policy assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources, cites them, and has no writes, persisted memory, approval flow, or delegated agents. The fictional London value is GBP 220. Case names and fixture revision are shared with the [worked-example reference](reference/policy-assistant-worked-example.md); values are not organizational policy.

```yaml
candidate: policy-assistant@candidate-current-selection
baseline: policy-assistant@baseline-current-selection
fixture:
  id: travel-policy-current
  revision: "fixture-2026-10-18.1"
  current_document: "travel-policy-2026@2026-10-01"
  superseded_document: "travel-policy-2024-superseded@2024-01-01"
checks:
  - case: POLICY-CURRENT-001
    purpose: regression
    level: system
    technique: positive
    claim: "A permitted request returns the current supported hotel limit."
    observe: "Answer, cited source identity/revision, and permitted retrieval boundary."
  - case: POLICY-DENIED-005
    purpose: regression
    level: integration
    technique: negative_and_boundary
    claim: "A denied source is not retrieved or disclosed."
    observe: "Trusted permission decision, retrieved source identities, and user-visible disclosure."
  - case: POLICY-PARAPHRASE-007
    purpose: development
    level: system
    technique: metamorphic_invariance
    claim: "A reviewed meaning-preserving paraphrase preserves the supported answer and required controls."
    observe: "Answer relation, source identity/revision, and relevant path invariants."
  - case: POLICY-MISSING-003
    purpose: regression
    level: system
    technique: negative_and_boundary
    claim: "Missing permitted evidence does not produce an invented definitive amount."
    observe: "Contract-defined uncertainty or needs_information outcome and source observations."
  - case: POLICY-EXHAUSTION-008
    purpose: development
    level: integration
    technique: controlled_fault_injection
    fault: "Retriever timeout before an approved source is returned."
    claim: "Dependency failure is handled without inventing a definitive amount."
    observe: "Dependency result, bounded recovery behavior, terminal outcome, and absence of unsupported source claims."
suite_separation:
  release_holdout: policy-release-holdout@v1
  holdout_case: POLICY-HOLDOUT-009
  holdout_fixture: "Separately authored task and fixture; not a relabelled development/regression case."
```

One user question can have an isolated check for revision selection, a component check for source filtering, an integration check for permission propagation, and a system case for the visible answer. They overlap because each makes a different boundary observable. The negative and boundary probes test access denial, and a positive counterpart confirms permitted work still succeeds. The paraphrase relation counts only after a reviewer confirms it preserves meaning. The timeout case tests a fault path, not retrieval relevance.

Keep `POLICY-HOLDOUT-009` out of iteration and evaluator tuning. A smoke suite can cheaply exercise the read path and regression cases preserve known behavior; neither replaces the holdout. This assistant has no writes, persistent memory, or live exposure here, so none of those are assumed. If a product claim later relies on user acceptance or operational learning, add that evidence.

## Evidence and checklist

- [ ] The record separates level, technique, property/claim, suite purpose, and lifecycle environment.
- [ ] Each level observes the behavior and boundary the claim states; a narrow check is not presented as proof of a wider one.
- [ ] Interface-crossing claims have integration evidence, and user-visible behavior claims have controlled offline evidence where CASE-04 applies.
- [ ] Each technique has a stated relation to the claim and a known limitation; negative cases have allowed counterparts.
- [ ] Suite purpose is explicit; development results are not presented as holdout evidence, and post-launch learning has not replaced pre-release evidence.
- [ ] Capability and regression suites are kept apart, and saturated capability cases have been graduated or replaced.
- [ ] An omitted but relevant level, or a distinct acceptance or operational-learning claim, has a recorded reason.
- [ ] Property evidence follows [4.3](03-evaluation-types-and-dimensions.md); profile and timing questions follow [4.6](06-standards-required-coverage-and-execution-cadence.md).

## References

[1]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for Natural Language Processing"
[2]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"

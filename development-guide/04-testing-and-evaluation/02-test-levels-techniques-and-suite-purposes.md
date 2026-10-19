# 4.2 Test Levels, Techniques, and Suite Purposes

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** When selecting evidence for a claim in an evaluation plan; the level depends on the behavior and boundary the claim covers.  
**Reader question:** How do I exercise the system, and how should I organize the checks?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Practical reference](reference/README.md)

Keep three descriptors apart: **level** is the boundary exercised, **technique** is how a behavior is probed, and **suite purpose** is why a set of cases runs. A case can combine several of each, plus a lifecycle environment; one label is not evidence for another. [4.3](03-evaluation-types-and-dimensions.md) covers what evidence establishes, [4.6](06-standards-required-coverage-and-execution-cadence.md) mandatory coverage, and [4.5](05-planning-designing-and-running-tests-and-evaluations.md) case identity, fixtures, and resets.

## Levels and boundaries: where the check observes behavior

Use the narrowest level that can establish the claim, and add a broader one when the claim crosses a boundary the narrow check cannot see. Levels are not a quality ranking; passing a lower level says nothing about a wider boundary.

- **Unit-level check:** A small rule or transformation in isolation, such as current-revision selection or a permission predicate. Fast and precise for deterministic rules; cannot show that the assembled agent passes the right identity to retrieval.
- **Component-level check:** An assembled capability with controlled collaborators, such as retriever, source filter, and formatter. Reveals mismatched assumptions inside the capability, not behavior across a separate service or a full user interaction.
- **Integration check:** Crosses one or more real interfaces, with controlled dependencies where useful: identity propagation, schemas, permission enforcement, timeouts, and result exchange. A stubbed boundary is not evidence about the real one it omits.
- **System or end-to-end check:** The agent and surrounding system through a user-visible task and the boundaries the claim names. Shows whether an integrated path gives the expected outcome under its fixture; not automatically representative of real users, live conditions, or long-run reliability.

Teams use these labels differently, so describe the actual boundary. Acceptance (a suite purpose) and production monitoring (a lifecycle activity) are not levels. For "a denied source is never disclosed," a permission predicate tests one rule; the end-to-end claim also needs evidence at the retrieval and output boundaries. Skip a costly broad suite when a narrow check is enough, but never let a narrow check stand in for a wider claim.

## Techniques: how to probe a behavior

Techniques combine at any level; choose by the claim, the credible failure mode, and what the observation can establish.

### Positive, negative, and boundary cases

A **positive case** exercises an allowed, expected path. Misuse: treating a happy path as proof that denied or ambiguous conditions are safe. Example: ask for the London hotel limit with a current permitted policy; expect a complete answer citing it.

A **negative case** presents a disallowed, unavailable, or contradictory condition and checks the contract-defined safe response: permissions, missing evidence, prohibited inputs. Misuse: accepting any refusal as a pass. Pair them with comparable allowed cases so blanket refusal cannot pass: test that a behavior happens when it should and not when it should not, or you optimize one side. Example: remove the user's permission for a source and verify, at the denied-source boundary, that it is not retrieved or disclosed.

A **boundary case** probes a meaningful limit or transition: either side of a permission scope, a revision becoming superseded, evidence becoming insufficient. Misuse: arbitrary edges with no stated reason. Example: compare users identical except for approved-policy access; inspect the trusted authorization decision and the visible result.

### Property-based checks

A **property-based check** exercises a stated invariant over deliberately varied generated or systematically chosen inputs. Use it when many inputs should obey one rule, such as "a source outside the user's permitted scope is never returned"; the property and input domain must be clear enough to judge each result. Misuse: counting near-duplicates as diverse coverage, or claiming broad assurance when the generator misses relevant cases. Keep reviewed representative cases and save failures as concrete examples.

### Metamorphic relations

A **metamorphic relation** states how an outcome should relate across a controlled input change, useful when an exact answer is hard to specify but a relationship can be reviewed. Use invariance for irrelevant changes and sensitivity for material ones; a paraphrase must truly preserve meaning, and a permission or current-policy change is never irrelevant. Misuse: assuming similar wording means identical meaning, or treating consistency as correctness. A reviewed paraphrase of the hotel question should keep the supported GBP 220 answer and source/control relation; a fixture with only a superseded policy should give the contract-defined uncertainty or `needs_information` outcome. Relations do not replace an external truth source or semantic review.[1]

### Controlled fault injection

**Fault injection** introduces a bounded dependency or environment failure, such as a retriever timeout, malformed result, or partial response, to observe safe handling and recovery. Misuse: unrealistic faults, several changes at once, or counting a harness failure as an agent result. Example: time out the retriever; check that the assistant reports the contract-defined unavailable-evidence outcome, invents no limit, and retries or stops only as policy allows. Record whether the dependency really failed and what reached the agent.

### Concurrency and load techniques

**Concurrency** checks exercise overlapping work; **load** checks vary demand or resource pressure. Use them for shared state, tenant isolation, capacity, contention, or demand. Misuse: reading a high-volume run as evidence of semantic quality, or assuming synthetic load matches real traffic. Example: two overlapping reads with different permission contexts must each get only their own authorized source. For capacity claims, state the tested workload; no universal throughput or latency threshold applies.

## Suite purposes: why this set is run

The same case may sit in several suites; keep its identity and record each suite's purpose.

- **Smoke:** A quick signal that a critical route or dependency is alive; not evidence of broad behavior, safety, or semantic quality.
- **Development:** Cases that guide iteration and change as understanding improves. They inform tuning, so repeated runs do not make them independent evidence.
- **Capability:** Hard cases the current agent often fails, showing where to improve; a low pass rate is expected. Once the agent passes nearly all, the suite is saturated and can no longer show progress, so add harder cases.
- **Regression:** Reviewed cases that catch returning failures or breaks in stable expectations. The pass rate should stay near 100%; a drop is a signal. Add confirmed, understood failures after sanitizing and review, but never freeze an ambiguous expected result as authoritative. Saturated capability cases can graduate here.[2]
- **Release holdout:** Cases reserved for independent evidence about a release claim, kept out of tuning of the candidate, prompts, rules, and evaluators behind the result. Once a holdout informs a change it is no longer untouched for that candidate; use a new one or describe the reuse accurately.
- **Acceptance:** Evidence for a stakeholder or intended-user acceptance decision, possibly with representative tasks or agreed criteria. A curated case does not represent all users.
- **Operational learning:** Scoped, privacy-appropriate observation after exposure to find drift, new failures, or changing conditions. It adds to, never replaces, required pre-release evidence.

Label suite purpose before reading results, separately from environment or stage: "regression" does not mean "production," and "acceptance" does not mean "live." Development cases can become regression cases after review; never quietly repurpose a holdout after its results influenced tuning.

## Requirements

- **CASE-04 — Fit-for-claim environments.** For each claim in the evaluation plan, the selected test layer **MUST** be capable of observing the claimed behavior and its relevant boundary. Deterministic rules **SHOULD** have focused unit or component cases; claims that cross interfaces **MUST** have integration evidence; and claims about user-visible agent behavior **MUST** have offline behavioral evidence on controlled cases. User acceptance and production evaluation **MUST** be added when their distinct usefulness or post-launch learning claims are relied upon. The evaluation plan and results **MUST** identify the boundary exercised and the evidence that supports the claim; omitted but otherwise relevant layers **MUST** have a claim-specific rationale.

## Worked example: select checks for the policy assistant

The fictional assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources, cites them, and has no writes, persisted memory, approval flow, or delegated agents. Identifiers match the [worked-example reference](reference/policy-assistant-worked-example.md).

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
    observe: "Answer, cited source identity/revision, permitted retrieval boundary."
  - case: POLICY-DENIED-005
    purpose: regression
    level: integration
    technique: negative_and_boundary
    claim: "A denied source is not retrieved or disclosed."
    observe: "Trusted permission decision, retrieved source identities, visible disclosure."
  - case: POLICY-PARAPHRASE-007
    purpose: development
    level: system
    technique: metamorphic_invariance
    claim: "A reviewed meaning-preserving paraphrase keeps the supported answer and controls."
    observe: "Answer relation, source identity/revision, path invariants."
  - case: POLICY-MISSING-003
    purpose: regression
    level: system
    technique: negative_and_boundary
    claim: "Missing permitted evidence does not produce an invented definitive amount."
    observe: "Contract-defined uncertainty or needs_information outcome; source observations."
  - case: POLICY-EXHAUSTION-008
    purpose: development
    level: integration
    technique: controlled_fault_injection
    fault: "Retriever timeout before an approved source is returned."
    claim: "Dependency failure is handled without inventing a definitive amount."
    observe: "Dependency result, bounded recovery, terminal outcome, no unsupported source claims."
suite_separation:
  release_holdout: policy-release-holdout@v1
  holdout_case: POLICY-HOLDOUT-009
  holdout_fixture: "Separately authored task and fixture, not a relabelled development/regression case."
```

One question can have unit (revision selection), component (source filtering), integration (permission propagation), and system (visible answer) checks; each makes a different boundary observable. Negative and boundary probes test denial while a positive counterpart confirms permitted work succeeds. The paraphrase counts only after a reviewer confirms it preserves meaning; the timeout case tests a fault path, not retrieval relevance.

Keep `POLICY-HOLDOUT-009` out of iteration and evaluator tuning; smoke and regression suites do not replace it. Add acceptance or operational-learning evidence only if a product claim later relies on it.

## Evidence and checklist

- [ ] Level, technique, claim, suite purpose, and lifecycle environment are separate fields.
- [ ] No narrow check is presented as proof of a wider boundary.
- [ ] Each technique states its relation to the claim and its limit; negative cases have allowed counterparts.
- [ ] Development results are not presented as holdout evidence; post-launch learning has not replaced pre-release evidence.
- [ ] Capability and regression suites are separate; saturated capability cases are graduated or replaced.

## References

[1]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for Natural Language Processing"
[2]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Anthropic: Demystifying Evals for AI Agents"

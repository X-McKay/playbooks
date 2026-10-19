# 4.2 Test Levels, Techniques, and Suite Purposes

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, reviewers, and accountable owners  
**Applicability:** When selecting evidence for a claim in an evaluation plan; the required level depends on the behavior and boundary the claim covers.  
**Reader question:** How do I exercise the system, and how should I organize the checks?

[Part 4 — Testing and Evaluation](README.md) · [Applicability](../../applicability.md) · [4.3 Evaluation Types and Dimensions](03-evaluation-types-and-dimensions.md) · [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) · [Practical reference](reference/README.md)

A test is a probe or execution under stated conditions; an evaluation assembles evidence to assess a claim or decision. These overlap: a deterministic assertion can contribute to a broad evaluation, and a variable agent can be tested. Keep the descriptors separate: **level** identifies the system boundary exercised, **technique** describes how a behavior is probed, and **suite purpose** explains why a set of cases is run. A case can combine several of each, and also carry a lifecycle environment. Do not use one label as evidence for another.

This chapter helps select and organize the probe. [4.3](03-evaluation-types-and-dimensions.md) explains what properties the evidence can establish; [4.6](06-standards-required-coverage-and-execution-cadence.md) defines mandatory coverage when a trigger applies. For case identity, fixtures, execution records, and reset handling, see [4.5](05-planning-designing-and-running-tests-and-evaluations.md).

## Levels and boundaries: where the check observes behavior

Use the narrowest level that can establish the claim, then add a broader level when the claim crosses a boundary the narrow check cannot observe. A level is not a quality ranking, and passing a lower level does not imply that a wider system boundary works.

- **Unit-level check:** Exercises a small rule or transformation in isolation, such as selecting the current policy revision or evaluating a permission predicate. It is useful for fast, precise feedback on a deterministic rule. It cannot show that the assembled agent passes the right identity to a retrieval boundary or uses the rule correctly in a real run.
- **Component-level check:** Exercises an assembled capability with controlled collaborators, such as a retriever, source filter, and result formatter. It can reveal mismatched assumptions inside that capability. It does not establish behavior across a separate service or a complete user interaction unless those boundaries are included.
- **Integration check:** Crosses one or more real interface boundaries, with controlled dependencies where appropriate. Use it for claims about identity propagation, schemas, permission enforcement, timeout handling, and how services exchange results. A stubbed boundary may help isolate a case, but cannot stand in for evidence about the real boundary it omits.
- **System or end-to-end check:** Exercises the agent and its relevant surrounding system through a user-visible task and the observable boundaries named by the claim. It can establish whether an integrated path produces the expected outcome under its fixture. It is not automatically representative of real users, all live conditions, or long-run reliability.

Teams may use “unit,” “component,” “integration,” and “system” differently. Describe the actual boundary rather than relying on a label alone. Acceptance is treated here as a decision context or suite purpose, not a peer technical boundary; conventional taxonomies may classify it differently. A user study can include system-level tasks, while production monitoring is a lifecycle activity rather than a test level.

Best practice: for each claim, name the boundary that must be observed and the evidence source that can show it. If a claim says “a denied source is never disclosed,” an isolated permission predicate may test one rule, but the end-to-end claim also needs evidence at the retrieval/output boundaries. Avoid running an expensive broad suite when a narrow check is sufficient, but do not imply that a narrow check proves a wider claim.

## Techniques: how to probe a behavior

Techniques can be combined at any appropriate level. Choose based on the claim, the credible failure mode, and what the available observation can establish. A technique is not itself an assessed property or a suite purpose.

### Positive, negative, and boundary cases

A **positive case** exercises an allowed, expected path. It is useful to show that a feature works for an ordinary, authorized request. Misuse: treating a successful happy path as proof that denied or ambiguous conditions are handled safely. Example: ask for the London hotel limit with a current permitted policy available and expect a complete answer citing the current source.

A **negative case** deliberately presents a disallowed, unavailable, or contradictory condition and checks the contract-defined safe response. It is useful for permissions, missing evidence, and prohibited inputs. Misuse: assuming any refusal is a pass; pair with comparable allowed cases where needed so blanket refusal cannot satisfy the claim. Example: remove the user's permission for a source and verify the source is not retrieved or disclosed, using the denied-source boundary evidence relevant to the claim.

A **boundary case** probes near a meaningful limit or transition: just inside and outside a permission scope, a policy revision changing from current to superseded, or evidence changing from sufficient to missing. Use it where behavior changes at a rule boundary. Misuse: inventing arbitrary numeric edges or testing a boundary without stating why it matters. Example: compare a user with approved-policy access to an otherwise identical user without that access; inspect the trusted authorization decision and observable result.

### Property-based checks

A **property-based check** exercises a stated invariant over a deliberately varied set of generated or systematically selected inputs, rather than relying only on handpicked examples. It is useful when many inputs should obey the same simple rule, such as “a source outside the user's permitted scope is never returned.” The property and the permitted input domain must be clear enough to judge each result. Misuse: generating many near-duplicates and treating their count as diverse coverage, or claiming broad assurance when the generator misses relevant cases. Keep representative reviewed cases and preserve any failures as concrete examples.

### Metamorphic relations

A **metamorphic relation** states how an outcome or observable behavior should relate across a controlled input change. It helps when a single exact expected answer is difficult to specify, but a relationship can be reviewed. Use it for genuinely irrelevant changes (invariance) and material changes that should alter the result (sensitivity); a paraphrase must really preserve meaning, while a permission or current-policy change must not be mislabeled irrelevant. Misuse: assuming similar wording guarantees identical semantics, or treating consistency as correctness. A reviewed paraphrase of the hotel question should preserve the supported GBP 220 answer and required source/control relation; changing the fixture so only a superseded policy is available should instead produce the contract-defined uncertainty or `needs_information` outcome. Metamorphic testing is a useful method when relations are specified, not a substitute for an external truth source or semantic review. [1]

### Controlled fault injection

**Fault injection** deliberately introduces a bounded dependency or environment failure to observe safe handling and recovery. Use it for credible conditions such as retriever timeout, malformed result, or partial response. Misuse: injecting an unrealistic fault, changing several conditions at once without a reason, or counting a harness failure as an agent result. Example: make the retriever time out; check that the assistant reports the contract-defined unavailable-evidence outcome, does not invent a definitive limit, and stops or retries only as its declared policy permits. Record whether the dependency actually failed and what response reached the agent.

### Concurrency and load techniques

**Concurrency** checks exercise overlapping work; **load** checks vary demand or resource pressure. Apply them when a claim involves shared state, tenant isolation, capacity, contention, or behavior under demand. Misuse: treating a high-volume run as evidence for unrelated semantic quality, or assuming a test's synthetic load represents real traffic. Example: overlap two read requests for different permission contexts against an isolated fixture and verify that each receives only its own authorized source. For capacity claims, state the tested workload and observation; do not invent a universal throughput or latency threshold in this chapter.

## Suite purposes: why this set is run

A suite is a versioned collection selected for a stated goal. The same case may appear in more than one suite when that reuse is appropriate, but preserve its identity and record the suite's purpose. Purpose does not say what technical boundary was exercised or what property was assessed.

- **Smoke:** A small signal that a critical route or basic dependency is alive. Run after a change or in a routine check when quick feedback matters. It is not evidence that broad behavior, safety, or semantic quality is covered.
- **Development:** Cases used to explore behavior and guide iteration. They may change as understanding improves. Because they inform tuning, their results do not become independent evidence merely by being run repeatedly.
- **Regression:** Reviewed cases retained to catch the return of resolved failures or violations of stable expectations. Add a confirmed, understood failure after sanitization and review. Avoid freezing an ambiguous expected result as if it were authoritative.
- **Release holdout:** Cases reserved for independent evidence about a release claim. Keep them out of tuning of the candidate, prompts, rules, and evaluators used for the reported result. If a holdout informs a change, it no longer serves as untouched evidence for that changed candidate; use a new independent holdout or accurately describe the reuse.
- **Acceptance:** Evidence used to inform a stakeholder or intended-user acceptance decision. It may include representative user tasks or agreed acceptance criteria. Do not confuse the decision purpose with a technical test boundary, and do not imply that a curated acceptance case represents all users.
- **Operational learning:** Privacy-appropriate observation after exposure, used to discover drift, new failure cases, or changing conditions. Define the scope and boundaries of any live observation. This learning supplements rather than retroactively replaces required pre-release evidence.

Best practice: label suite purpose before interpreting results, and keep purpose distinct from environment or stage. “Regression” does not mean “production,” and “acceptance” does not automatically mean “live.” Development cases can later become regression cases after review, but a release holdout should not be silently repurposed after results influence tuning.

## Requirements

- **CASE-04 — Fit-for-claim environments.** For each claim in the evaluation plan, the selected test layer **MUST** be capable of observing the claimed behavior and its relevant boundary. Deterministic rules **SHOULD** have focused unit or component cases; claims that cross interfaces **MUST** have integration evidence; and claims about user-visible agent behavior **MUST** have offline behavioral evidence on controlled cases. User acceptance and production evaluation **MUST** be added when their distinct usefulness or post-launch learning claims are relied upon. The evaluation plan and results **MUST** identify the boundary exercised and the evidence that supports the claim; omitted but otherwise relevant layers **MUST** have a claim-specific rationale.

## Worked example: select checks for the policy assistant

The fictional policy assistant is ephemeral and read-only: it answers from approved, current, permission-filtered sources, cites them, and has no writes, persisted memory, approval flow, or delegated agents. The current fictional London policy value is GBP 220. This example shows levels, techniques, and suite purposes as separate descriptors—not one classification. The case names and fixture revision are shared with the [worked-example reference](reference/policy-assistant-worked-example.md); values are illustrative, not organizational policy.

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

The same user question can have an isolated rule check for policy revision selection, a component check for source filtering, an integration check for permission propagation, and a system-level case for the user-visible answer. The levels overlap because they make different boundaries observable. The negative and boundary probes test access denial; a positive counterpart confirms that permitted work remains possible. The paraphrase relation is useful only after a reviewer establishes that it preserves meaning. The timeout case evaluates a fault path, not retrieval relevance under normal conditions.

Keep `POLICY-HOLDOUT-009` independent of iteration and evaluator tuning. A smoke suite could cheaply exercise the basic read path, while regression cases preserve known behavior; neither alone replaces the holdout claim. Because this assistant has no writes, persistent memory, or live user exposure in this scenario, those mechanisms are not inferred from its retrieval capability. If a future product claim relies on user acceptance or operational learning, add the corresponding evidence and boundary rather than treating offline results as a substitute.

## Evidence and checklist

Before relying on test results for a claim, confirm:

- [ ] The record separates level, technique, property/claim, suite purpose, and lifecycle environment.
- [ ] Each selected level observes the behavior and boundary stated by the claim; a narrower check is not presented as proof of a wider boundary.
- [ ] Interface-crossing claims have integration evidence, and user-visible behavior claims have controlled offline behavioral evidence where CASE-04 applies.
- [ ] Chosen positive, negative, boundary, property-based, metamorphic, fault, or concurrency/load techniques have a stated relation to the claim and a known limitation.
- [ ] Suite purpose is explicit; development feedback has not been presented as independent holdout evidence, and post-launch learning has not replaced required pre-release evidence.
- [ ] An omitted otherwise-relevant level or distinct acceptance/operational-learning claim has a reason recorded in the evaluation plan.
- [ ] Evidence needed for the property itself follows [4.3](03-evaluation-types-and-dimensions.md); mandatory profile and timing questions follow [4.6](06-standards-required-coverage-and-execution-cadence.md).

## References

[1]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for NLP Tasks"

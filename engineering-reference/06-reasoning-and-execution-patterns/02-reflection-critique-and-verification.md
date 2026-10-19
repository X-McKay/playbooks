# 6.2 Reflection, Critique, and Verification

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers deciding whether to add a review or correction pass to an agent
**Applicability:** Optional for any agent that drafts, plans or interprets. Required only when the agent contract or controls rely on reflection for a claimed behavior. Reflection never replaces authorization or evidence controls.

[Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Part 6](./README.md) · [6.1 Planning and bounded loops](01-planning-decomposition-and-bounded-control-loops.md) · [6.3 Parallel work](03-parallel-work-state-and-failure-propagation.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) · [4.7 Analysis and decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

A second look can catch omissions, contradictions, unsupported claims and format errors. It also costs time and money, can keep the same wrong assumption and can add errors. Reflection proposes a revision; it does not prove it right.

Use this chapter when an agent critiques or revises its output, calls a critic, or checks work against external or deterministic evidence. Do not add reflection by default: an authoritative check is often safer and cheaper. Reflection suits open-ended writing and finding candidate issues, not general safety.

## Working model

A review cycle has a candidate, explicit criteria, feedback pointing to a possible defect, and a decision to revise, keep, ask or stop. Verification asks whether the candidate passes a check that can establish the property, however convincing the critique sounds.

- **Self-critique** is cheap and catches visible omissions, but shares the first attempt's context and blind spots.
- **A separate critic** uses another prompt or reviewer; a different role or model alone does not make it independent or correct.
- **External validators** bring evidence not in the draft: an approved source document, a domain reviewer or authoritative system state.
- **Deterministic checks** establish properties by rule: required fields present, a value within bounds, a citation ID that resolves. Finding a citation does not show it supports the claim.

Evidence on self-correction without outside feedback is mixed. Critique-and-revise prompting without correctness feedback lowered accuracy on one study's reasoning benchmarks while oracle feedback raised it; that warns against assuming a model spots its own errors, within those models and tasks.[1] Iterative self-feedback improved seven selected tasks in another study.[2] A survey separates intrinsic critique from externally grounded feedback and notes evidence gaps.[3]

So ground review in outside feedback (tests, a code interpreter, retrieval, a symbolic tool or a trusted reference); checking with such tools before revising produced gains in one study.[4]

## Decisions and best practices

- **Match the check to the property.** Syntactic or numeric properties get deterministic checks. Document support needs the cited evidence or domain review; a second model repeating the claim is not independent. Whether an external action happened is a question for authoritative state, not a draft, critic or transcript.
- **Narrow the critic.** Give it specific criteria and minimal context, and ask it to cite the claim or omission and the evidence or rule behind the doubt; "check everything" is unusable. Keep the check result, not hidden reasoning.
- **Bound the loop.** One pass is a sensible start, not a proven optimum. Stop when the candidate passes, nothing actionable is found, or the bound is reached; a remaining material issue gets the contract's partial, ask, escalate or fail outcome, never a silent loop or claimed success.
- **Do not assume the revision is better.** Compare it with the original against the criteria and independent evidence, keep a valid original when the edit is unsupported, and state uncertainty when neither verifies. Test revisions that could break a valid result (see [4.4](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) and [4.7](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)); a few polished examples are not proof.
- **Verify at more than one level.** Many verifiers in multi-agent traces check only superficial properties, such as whether code compiles. In one taxonomy verification failures were about a quarter of all failures: incorrect (9.1%), missing or incomplete (8.2%) and premature termination (6.2%); checking the high-level objective improved task success.[5] Test your verifier on cases it should reject.
- **Critique cannot authorize.** Authorization, approval and capability enforcement stay deterministic controls at execution time, and human approval stays bound to the exact action; a critic's "approved" label cannot replace it. See Part 3 and [6.1](01-planning-decomposition-and-bounded-control-loops.md).

## Requirements

- **REFLECT-01** When an agent performs critique or revision, its owner MUST define a finite maximum number of review/revision passes and applicable time or cost bounds, and MUST define the contract outcome when those bounds are reached.
- **REFLECT-02** When a revised output is accepted as meeting a requirement, the system MUST check that requirement against its stated criteria and suitable evidence; a critic's confidence or agreement alone MUST NOT be recorded as verification.
- **REFLECT-03** When reflection or a critic proposes an action, authorization MUST be enforced by the existing policy at execution time; critique, model confidence, and self-approval MUST NOT grant capabilities or approval.
- **REFLECT-04** When reflection is used as a behavior, quality, or safety control, its owner MUST evaluate it against a no-reflection baseline on representative relevant cases, including already-correct drafts and known failure cases, and MUST record material regressions and the added resource cost before relying on it for that claim.
- **REFLECT-05** When an explanation or review record is required, the record MUST identify the candidate outcome, checks performed, relevant evidence identifiers or versions, and pass/fail or unresolved status; it MUST NOT require raw hidden reasoning as audit evidence.

## Worked example: a policy answer that needs a second look

The fictional read-only policy assistant answers from approved, current, permission-filtered documents with citations. Fixture `travel-policy-current` sets the London hotel amount at GBP 220; a superseded fixture differs.

The assistant drafts: "The London hotel limit is GBP 220. [travel-policy-current]" A critique pass asks whether the cited document supports the amount and is the current one this user may access, and flags the answer for checking.

A deterministic check resolves the citation to the approved version and confirms fixture ID, amount, scope and the access decision; an unclear condition goes to a qualified reviewer or source-grounded semantic check. The assistant then answers with the citation, asks a clarifying question, or says the evidence is not enough.

If the critic proposes a different amount from the superseded document, the validator rejects the edit; the system keeps the verified answer and records the failed check, not the critic's rationale. If a test removes the current document or denies permission, the assistant returns `needs_information`, `declined`, `failed` or a bounded partial result rather than fall back to the superseded one. Reflection raised the question; the evidence check answered it.

## Evidence and checklist

Before relying on reflection, keep enough evidence to answer:

- What defect is the review meant to find, and for which tasks?
- What criteria and external evidence show a correction is valid?
- Can a reviewer see the candidate, check, evidence version and unresolved status without hidden reasoning?

## References

[1]: https://arxiv.org/abs/2310.01798 "Large Language Models Cannot Self-Correct Reasoning Yet"
[2]: https://arxiv.org/abs/2303.17651 "Self-Refine: Iterative Refinement with Self-Feedback"
[3]: https://arxiv.org/html/2406.01297v3 "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"
[4]: https://arxiv.org/abs/2305.11738 "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing"
[5]: https://arxiv.org/html/2503.13657v3 "Why Do Multi-Agent LLM Systems Fail?"

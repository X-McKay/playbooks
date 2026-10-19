# 6.2 Reflection, Critique, and Verification

**Status:** 0.5.0 first draft
**Audience:** Developers and reviewers deciding whether to add a review or correction pass to an agent
**Applicability:** Optional for any agent that drafts, plans, or interprets. Required only when the agent contract or risk controls rely on reflection as part of a claimed behavior; reflection never replaces the applicable authorization or evidence controls.

[Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Part 6](./README.md) · [6.1 Planning and bounded loops](01-planning-decomposition-and-bounded-control-loops.md) · [6.3 Parallel work](03-parallel-work-state-and-failure-propagation.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) · [4.7 Analysis and decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

A second look can catch omissions, contradictions, unsupported claims, and format errors before an answer reaches a user. It can also consume time and cost, preserve the same mistaken assumption, or introduce a new error. Reflection is a way to propose a revision, not proof that the revision is correct.

Use this chapter when an agent critiques or revises its own output, invokes a separate critic, or checks proposed work against external or deterministic evidence. Do not add a reflection loop by default. A concise response with an authoritative check may be safer and cheaper than repeated free-form review. Reflection may be useful for open-ended writing or for finding candidate issues, but it is not a general-purpose safety barrier.

## Working model

A bounded review cycle has four distinct parts: a candidate output; explicit criteria for inspecting it; feedback that identifies a possible defect; and a decision to revise, retain, ask for information, or stop. Verification asks a different question: does the candidate satisfy a check that can establish the relevant property? The answer depends on the property, not on how persuasive the critique sounds.

**Self-critique** asks the same model or agent to inspect its earlier output. It is cheap to add and can catch visible omissions, but it shares much of the initial attempt's context and limitations. **A separate critic role** creates another review step, perhaps with a distinct prompt or reviewer. Separation can help organize attention, but a different role or model alone does not make its judgment independent or correct. **External validators** bring evidence not contained in the draft, such as an approved source document, a domain reviewer, or authoritative system state. **Deterministic checks** establish properties with explicit rules, such as whether required fields exist, a value is within a declared bound, or a citation identifier resolves. They do not establish semantic support merely by finding a citation.

Research on intrinsic LLM self-correction has produced mixed results. One study found that prompting models to critique and revise reasoning without access to correctness feedback reduced performance on its tested reasoning benchmarks, while oracle correctness feedback improved it. The result is limited to the tested models, tasks, prompts, and setup; it is a warning against assuming that a model can recognize its own errors, not proof that every review pass fails.[1] Another study reported gains from iterative self-feedback on seven selected tasks with task-specific prompts and evaluation methods.[2] These contrasting findings support a practical rule: test reflection against a no-reflection baseline on the tasks where it will be used, and use a source of evidence suited to the claim. A critical survey likewise emphasizes the difference between intrinsic critique and feedback grounded in external information, as well as limitations in the evidence base.[3]

## Decisions and best practices

Start by naming what the review is meant to catch. If the requirement is syntactic or numeric, use a deterministic check. If it is whether an answer is supported by a document, inspect the cited evidence or use a fit-for-purpose domain review; a second model repeating the same claim is not an independent source. If it concerns whether an external action occurred, consult authoritative state rather than trusting a draft, critic, or transcript.

Give a critic narrow criteria and the minimum relevant context. Ask it to point to a specific claim, omission, or inconsistency and the evidence or rule that makes it questionable. A broad instruction to “check everything” makes its output hard to interpret. Where practical, run checks independently of the generation step and preserve the check result, not private hidden reasoning. A separate critic should not receive extra authority simply because it is called a reviewer.

Use a finite review budget. Decide in advance the maximum number of critique-and-revision attempts, applicable time or cost limit, and what happens when the limit is reached. One review pass is a sensible starting point, not a universal optimum. Stop when the candidate passes the applicable checks, the reviewer finds no actionable issue, or the bound is reached. If a material issue remains unresolved, return a bounded partial result, ask for information, escalate, or fail according to the agent contract; do not silently loop or claim success.

Do not assume a revision is an improvement. Compare it with the original against the task criteria and any independent evidence. Preserve a valid original answer if the proposed edit is unsupported, and make uncertainty explicit when neither version can be verified. Evaluate reflection on relevant cases, including cases where the first draft is already correct, where evidence is missing or conflicting, and where revisions might break an otherwise valid result. Use the evaluation and release rules in [4.4 Evaluators, Metrics, Rubrics, and Calibration](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) and [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md) rather than treating a handful of polished examples as proof of reliability.

A critique can recommend an action, but it cannot authorize one. Authorization, approval, and capability enforcement remain deterministic controls at execution time. Human approval must remain bound to the exact action and context under the applicable policy; a self-review or a critic's “approved” label cannot substitute for it. For trust-boundary controls, see Part 3; for iterative planning and termination behavior, see [6.1](01-planning-decomposition-and-bounded-control-loops.md).

## Requirements

- **REFLECT-01** When an agent performs critique or revision, its owner MUST define a finite maximum number of review/revision passes and applicable time or cost bounds, and MUST define the contract outcome when those bounds are reached.
- **REFLECT-02** When a revised output is accepted as meeting a requirement, the system MUST check that requirement against its stated criteria and suitable evidence; a critic's confidence or agreement alone MUST NOT be recorded as verification.
- **REFLECT-03** When reflection or a critic proposes an action, authorization MUST be enforced by the existing policy at execution time; critique, model confidence, and self-approval MUST NOT grant capabilities or approval.
- **REFLECT-04** When reflection is used as a behavior, quality, or safety control, its owner MUST evaluate it against a no-reflection baseline on representative relevant cases, including already-correct drafts and known failure cases, and MUST record material regressions and the added resource cost before relying on it for that claim.
- **REFLECT-05** When an explanation or review record is required, the record MUST identify the candidate outcome, checks performed, relevant evidence identifiers or versions, and pass/fail or unresolved status; it MUST NOT require raw hidden reasoning as audit evidence.

## Worked example: a policy answer that needs a second look

An internal policy assistant answers from approved, current, permission-filtered documents and returns citations plus uncertainty. It has no external write capability. A fictional fixture named `travel-policy-current` says the London hotel amount is GBP 220; a superseded fixture differs. This is test data, not actual policy.

The assistant drafts: “The London hotel limit is GBP 220. [travel-policy-current]” A critique pass applies two narrow questions: does the cited document support the stated amount, and is it the current document this user may access? The critique notices that citation presence alone does not show support. It flags the answer for checking rather than declaring it correct.

The verification step resolves the citation to the approved document version, checks that the user's permission filter admitted that document, and compares the amount and applicable scope with the source. A deterministic check can confirm the fixture identifier, version, amount, and access decision. If the source's wording leaves an applicability condition ambiguous, a qualified reviewer or source-grounded semantic assessment must resolve that question; the reflection step cannot manufacture certainty. The assistant then either returns the answer with the supported citation, asks a clarifying question, or reports that the approved evidence is insufficient.

Suppose instead that the first draft already cites the current document correctly, but the critic proposes a different amount based on the superseded document. The validator rejects that edit because it conflicts with the authoritative fixture. The system keeps the verified answer and records the failed check, not the critic's rationale as a finding. If a test case removes the current document or denies permission, the assistant must not use the superseded document to fill the gap; its contract calls for `needs_information`, `declined`, `failed`, or an explicitly bounded partial result as appropriate. At no point does the critique step create a write capability or approve a policy change.

This example shows where reflection may help: identifying a question the initial answer did not establish. It also shows why the evidence check, not agreement between two model passes, determines whether the answer is supported.

## Evidence and checklist

Before relying on a reflection pattern, retain enough evidence to answer:

- What defect is the review intended to find, and for which applicable tasks?
- What criteria and external evidence can establish whether a proposed correction is valid?
- Is there a finite loop and safe contract outcome when the limit is reached?
- Have already-correct drafts, missing/conflicting evidence, and known errors been tested against a no-reflection baseline?
- Are output checks and authorization enforced independently of the critic?
- Can a reviewer identify the candidate, check, evidence version, and unresolved status without access to hidden reasoning?

## References

[1]: https://arxiv.org/abs/2310.01798 "Large Language Models Cannot Self-Correct Reasoning Yet"
[2]: https://arxiv.org/abs/2303.17651 "Self-Refine: Iterative Refinement with Self-Feedback"
[3]: https://arxiv.org/html/2406.01297v3 "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"

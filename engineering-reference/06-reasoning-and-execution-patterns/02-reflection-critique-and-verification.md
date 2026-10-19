# 6.2 Reflection, Critique, and Verification

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers deciding whether to add a review or correction pass to an agent
**Applicability:** Optional for any agent that drafts, plans or interprets. Required only when the agent contract or controls rely on reflection for a claimed behavior. Reflection never replaces authorization or evidence controls.

[Playbook home](../../README.md) · [Applicability](../../applicability.md) · [Part 6](./README.md) · [6.1 Planning and bounded loops](01-planning-decomposition-and-bounded-control-loops.md) · [6.3 Parallel work](03-parallel-work-state-and-failure-propagation.md) · [4.4 Evaluators, Metrics, Rubrics, and Calibration](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) · [4.7 Analysis and decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)

## Purpose and applicability

A second look can catch omissions, contradictions, unsupported claims and format errors before an answer reaches a user. It also costs time and money, can keep the same wrong assumption, and can add a new error. Reflection proposes a revision. It does not prove the revision is right.

Use this chapter when an agent critiques or revises its own output, calls a separate critic, or checks work against external or deterministic evidence. Do not add a reflection loop by default. A short answer with an authoritative check can be safer and cheaper than repeated free-form review. Reflection suits open-ended writing and finding candidate issues. It is not a general safety barrier.

## Working model

A bounded review cycle has four parts: a candidate output; explicit criteria for inspecting it; feedback that points to a possible defect; and a decision to revise, keep, ask for information or stop. Verification asks a different question: does the candidate pass a check that can establish the property in question? The answer depends on the property, not on how convincing the critique sounds.

- **Self-critique** asks the same model to inspect its earlier output. It is cheap and can catch visible omissions, but it shares the first attempt's context and blind spots.
- **A separate critic** adds another review step, perhaps with a different prompt or reviewer. A different role or model alone does not make its judgment independent or correct.
- **External validators** bring evidence that is not in the draft, such as an approved source document, a domain reviewer or authoritative system state.
- **Deterministic checks** establish properties with explicit rules, such as required fields present, a value within a declared bound, or a citation ID that resolves. Finding a citation does not show that it supports the claim.

Research on self-correction without outside feedback is mixed. One study found that prompting models to critique and revise their reasoning, without access to correctness feedback, lowered accuracy on its tested reasoning benchmarks, while oracle correctness feedback raised it. That result is limited to the tested models, tasks and prompts. It warns against assuming a model can spot its own errors. It does not show that every review pass fails.[1] Another study reported gains from iterative self-feedback on seven selected tasks, with task-specific prompts and evaluation methods.[2] A critical survey stresses the difference between intrinsic critique and feedback grounded in external information, and notes gaps in the evidence.[3]

The practical rule is to ground the review in outside feedback. Self-correction works best when something other than the model's own judgment supplies the feedback: tests or a code interpreter, search or retrieval, a symbolic tool, or a trusted reference. One study found gains when a model checked its output with such tools and then revised.[4] Also test reflection against a no-reflection baseline on the tasks where it will run.

## Decisions and best practices

Name what the review should catch. If the property is syntactic or numeric, use a deterministic check. If the question is whether a document supports an answer, inspect the cited evidence or use a suitable domain review. A second model repeating the claim is not an independent source. If the question is whether an external action happened, ask authoritative state, not the draft, a critic or a transcript.

Give a critic narrow criteria and the least context it needs. Ask it to point to a specific claim, omission or inconsistency, and to the evidence or rule that makes it doubtful. "Check everything" produces output that is hard to use. Where practical, run checks apart from the generation step and keep the check result, not private hidden reasoning. A critic gets no extra authority because it is called a reviewer.

Use a finite review budget. Decide in advance the maximum number of critique-and-revision passes, the time or cost limit, and what happens at the limit. One pass is a sensible start, not a proven optimum. Stop when the candidate passes its checks, the reviewer finds nothing actionable, or the bound is reached. If a material issue remains, return a bounded partial result, ask for information, escalate or fail as the contract says. Do not loop silently or claim success.

Do not assume a revision is better. Compare it with the original against the task criteria and any independent evidence. Keep a valid original if the edit is unsupported, and state the uncertainty when neither version can be verified. Test reflection on cases where the first draft is already right, where evidence is missing or conflicting, and where a revision could break a valid result. Use the rules in [4.4 Evaluators, Metrics, Rubrics, and Calibration](../../development-guide/04-testing-and-evaluation/04-evaluators-metrics-rubrics-and-calibration.md) and [4.7 Analyzing Results, Comparing Versions, and Making Decisions](../../development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md). A handful of polished examples is not proof of reliability.

Verify at more than one level. Studies of multi-agent traces find many verifiers check only superficial properties, such as whether code compiles. Verification failures were about a quarter of the failures in one taxonomy: incorrect verification (9.1%), missing or incomplete verification (8.2%), and premature termination (6.2%). Adding a check of the high-level task objective, not just low-level correctness, improved task success in that study.[5] Test your verifier on cases it should reject.

A critique can recommend an action. It cannot authorize one. Authorization, approval and capability enforcement stay deterministic controls at execution time. Human approval must stay bound to the exact action and context under policy. A self-review or a critic's "approved" label cannot replace it. For trust-boundary controls, see Part 3. For iterative planning and termination, see [6.1](01-planning-decomposition-and-bounded-control-loops.md).

## Requirements

- **REFLECT-01** When an agent performs critique or revision, its owner MUST define a finite maximum number of review/revision passes and applicable time or cost bounds, and MUST define the contract outcome when those bounds are reached.
- **REFLECT-02** When a revised output is accepted as meeting a requirement, the system MUST check that requirement against its stated criteria and suitable evidence; a critic's confidence or agreement alone MUST NOT be recorded as verification.
- **REFLECT-03** When reflection or a critic proposes an action, authorization MUST be enforced by the existing policy at execution time; critique, model confidence, and self-approval MUST NOT grant capabilities or approval.
- **REFLECT-04** When reflection is used as a behavior, quality, or safety control, its owner MUST evaluate it against a no-reflection baseline on representative relevant cases, including already-correct drafts and known failure cases, and MUST record material regressions and the added resource cost before relying on it for that claim.
- **REFLECT-05** When an explanation or review record is required, the record MUST identify the candidate outcome, checks performed, relevant evidence identifiers or versions, and pass/fail or unresolved status; it MUST NOT require raw hidden reasoning as audit evidence.

## Worked example: a policy answer that needs a second look

An internal policy assistant answers from approved, current, permission-filtered documents and returns citations and uncertainty. It has no external write capability. A fictional fixture named `travel-policy-current` says the London hotel amount is GBP 220. A superseded fixture differs. All data is made up.

The assistant drafts: "The London hotel limit is GBP 220. [travel-policy-current]" A critique pass asks two narrow questions: does the cited document support the amount, and is it the current document this user may access? The critique notes that a citation being present does not show support. It flags the answer for checking and does not declare it correct.

The verification step resolves the citation to the approved document version, checks that the permission filter admitted that document, and compares the amount and scope with the source. A deterministic check can confirm the fixture ID, version, amount and access decision. If the source wording leaves a condition unclear, a qualified reviewer or a source-grounded semantic check must settle it. The reflection step cannot create certainty. The assistant then returns the answer with the supported citation, asks a clarifying question, or says the approved evidence is not enough.

Now suppose the first draft already cites the current document correctly, but the critic proposes a different amount based on the superseded document. The validator rejects the edit because it conflicts with the authoritative fixture. The system keeps the verified answer and records the failed check, not the critic's rationale. If a test removes the current document or denies permission, the assistant must not fill the gap with the superseded document. Its contract calls for `needs_information`, `declined`, `failed` or a bounded partial result. At no point does the critique create a write capability or approve a policy change.

The example shows where reflection helps: it spots a question the first answer did not settle. It also shows that the evidence check, not agreement between two model passes, decides whether the answer is supported.

## Evidence and checklist

Before relying on reflection, keep enough evidence to answer:

- What defect is the review meant to find, and for which tasks?
- What criteria and external evidence show whether a correction is valid?
- Is there a finite loop and a safe contract outcome at the limit?
- Were already-correct drafts, missing or conflicting evidence and known errors tested against a no-reflection baseline?
- Are output checks and authorization enforced independently of the critic?
- Can a reviewer identify the candidate, check, evidence version and unresolved status without access to hidden reasoning?

## References

[1]: https://arxiv.org/abs/2310.01798 "Large Language Models Cannot Self-Correct Reasoning Yet"
[2]: https://arxiv.org/abs/2303.17651 "Self-Refine: Iterative Refinement with Self-Feedback"
[3]: https://arxiv.org/html/2406.01297v3 "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs"
[4]: https://arxiv.org/abs/2305.11738 "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing"
[5]: https://arxiv.org/html/2503.13657v3 "Why Do Multi-Agent LLM Systems Fail?"

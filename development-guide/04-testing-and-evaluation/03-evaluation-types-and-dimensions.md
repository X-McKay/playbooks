# 4.3 Evaluation Types and Dimensions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, security and privacy reviewers, and accountable owners  
**Applicability:** Whenever evidence supports a design, exposure, release, or behavior-affecting change decision. Claim families and profiles apply only when their contract, capability, input, user, or harm trigger is present.  
**Reader question:** What should we measure or judge about the agent?

This chapter explains the **claims** an evaluation can establish; it prescribes no grader, trial count, threshold, or release conclusion. Use [applicability](../../applicability.md) to check triggers and [4.6](06-standards-required-coverage-and-execution-cadence.md) to map profiles to cases.

## Start with a bounded claim, not an "eval type"

Of the five descriptors in [4.1](01-foundations-terms-and-definitions.md), this chapter covers the **claim family**: the property a result is meant to establish. A useful claim states its scope, acceptable terminal outcomes, establishing evidence, and limits. One policy answer may need several:

- Task outcome: did the assistant answer the policy question usefully?
- Source admission: was the source permitted and current?
- Grounding: is each material assertion supported by that source?
- Trajectory: did the assistant respect scope and stop boundaries?

None establishes the others: fluent prose is not task success, a source identifier is not semantic support, a grounded source can be stale, and a good answer does not show the path was allowed.

## Dimensions to assess

The [worked example](#worked-example-a-bounded-policy-answer-and-its-dimensions) applies each dimension.

### Task success and user usefulness

**What this establishes.** Whether the contract-defined result solves the bounded task. Outcomes are `complete`, `needs_information`, `declined`, `failed`, or a contract-defined partial or escalation outcome. Usefulness can include completeness, clarity, and actionability.

**What it does not establish.** Source permission, factual truth, safety, or a compliant path. A convincing answer can use an out-of-scope document or omit a material qualification; a polished reply that asks for information already present is over-refusal.

**What to observe.** Case input and user context, expected terminal outcome, relevant final state, and an evaluator able to judge the task. Grade the output and end state before the path. For a controlled fixture, pair a reference value with qualified review of wording variation.

### Trajectory, tool use, and control compliance

**What this establishes.** A **trajectory** is the observable, ordered or partly ordered record of events relevant to a claim: selected capability and material arguments, validation or authorization decision, tool result, retry, stop, user-facing artifact, handoff, and authoritative state or effect. A trajectory claim establishes that necessary constraints held during the task.

**Grade outcomes first; reserve path assertions for constraints.** Agents find valid routes you did not anticipate, so a rigid tool sequence fails correct runs. State the terminal outcome separately, then assert only **path invariants** that hold on any safe path: authorize before returning protected content, retrieve only in-scope current sources, use only permitted capabilities and arguments, perform no write, stop at the declared limit. Independent reads may run in either order; authorization before disclosure is a real dependency. One agent-tool benchmark likewise models milestones and forbidden actions as a partial order, not one exact trace.[1] Match exact sequences only where a protocol or control makes order material, such as binding an approved immutable payload before an effect.

**What it does not establish.** A tool name does not show safe arguments, and safe arguments do not show a protected boundary authorized the request. A transcript claiming an effect is not an authoritative observation of it. No private reasoning is needed.

**What to observe.** When a claim depends on retrieval, an interface, a tool, a stop or budget boundary, provenance, a handoff, or a prohibited action, assess tool selection, security-relevant arguments, and dependency order separately. Capture claim-sufficient provenance (source or state identity, scope, revision or freshness, supporting observation), plus retries and stops where failure, duplicate work, cost, or a consequential effect matters.

#### Keep proposal, boundary, execution, and disclosure distinct

A label like "unauthorized attempt" hides four observations:

1. **Proposal or compliance:** the model proposes an out-of-scope operation.
2. **Boundary decision:** the trusted boundary authorizes or denies it.
3. **Execution:** authoritative state shows an external action did or did not occur.
4. **Disclosure:** restricted material reached an unpermitted recipient or output.

A denied prohibited proposal can fail model compliance while showing enforcement worked; it is not an unauthorized execution. A blocked write does not show that nothing was disclosed. Record the four separately, and pair each denied case with a comparable permitted one so a system that declines everything cannot look safe.

### Consistency, relations, and repeated-run reliability

**What this establishes.** **Fixed-world repeated-run reliability** asks whether freshly initialized episodes of the same case, fixture, permission context, and run policy repeatedly reach the correct terminal outcome and satisfy every required invariant. Equivalent wording is fine where the claim allows. Reliability is not byte-for-byte sameness, nor consistent wrongness: repeatedly returning GBP 200, refusing an allowed request, or following an unsafe path.

Two relations answer different questions:

- An **invariance relation** changes something justified as irrelevant and keeps the required answer and controls, such as a reviewed paraphrase or reordering of truly independent facts.
- A **sensitivity relation** changes something material and produces the contractually required change in answer, boundary decision, or uncertainty, such as lost permission, conflicting current evidence, or a changed material user constraint.

A metamorphic relation makes input and expected output relations explicit; it can reveal violations where a full answer oracle is hard to write, but does not prove truth.[2]

**What this does not establish.** Fresh repeats of one curated case do not show field reliability. Invariance without sensitivity can reward ignoring context. A variant counts only with a stated reason it preserves (or changes) meaning. Repeats do not replace correctness or trajectory evidence.

**What to observe.** Material stochastic user-visible claims need fresh repeated-episode evidence, or a documented claim-specific alternative that actually removes the variability. Record candidate and resolved route, fixed and varying sources, fresh initialization and reset observation, each terminal outcome, path evidence, and status; never silently pick a favorable run. Start every trial from clean state so leftover files, caches, or records cannot couple trials. Metrics, retries, and comparison are in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

Where BEHAVIOR-02's semantic-input or changeable-evidence triggers apply, define at least one invariance and one sensitivity relation before exposure; a fully structured interface with no equivalence or variation claim can record why they do not apply.

### Grounding, retrieval quality, and factual correctness

**What this establishes.** Five separate claims. Retrieval **relevance**: does an item bear on the query? Evidence **coverage**: is the material evidence for the answer present? **Admissibility and currentness**: is the source permitted for this requester and use, and current at the relevant time? **Semantic grounding**: is each material assertion supported by identified source text in context? **Factual correctness**: is the assertion true against an independent truth reference at the relevant time?

**What this does not establish.** A relevant document may omit a needed rule; a current permitted document may not support an invented exception; an answer can faithfully report a stale source and still be wrong. A citation's presence, resolvability, relevance, or authority is not semantic support. Retrieval research likewise treats relevance, faithfulness, and correctness as separate, partly overlapping targets.[3]

**What to observe.** When retrieved or changeable evidence affects an outcome or the product promises sourced assertions, keep the approved source record, permission decision, revision or status, claim-to-source support, and any independent truth reference distinct. With no authoritative truth reference, say so rather than calling a heuristic ground truth.

### Robustness, uncertainty, and failure recovery

**What this establishes.** Contract-correct behavior under plausible adverse conditions (missing, stale, conflicting, malformed, denied, injected, timeout, partial, or exhausted), including appropriate clarification, uncertainty, decline, failure, or bounded partial results, and safe recovery and stopping where required.

**What this does not establish.** A generic adversarial-prompt list is not a security claim; a fluent fallback without support is not a success; appropriate uncertainty is not usefulness if comparable answerable cases are refused.

**What to observe.** Choose adverse conditions from the enabled capabilities and risk record. Put untrusted instructions in the real channel under test (a retrieved document tests a different boundary than the user turn) and observe exposure, attempted invocation, boundary decision, state, or stop event, not a refusal-like sentence. OWASP describes indirect prompt injection as untrusted external content changing model behavior, with adversarial testing one layer beside privilege controls and validation.[4] Fixed injection cases show only that known attacks fail; injection-resistance evidence needs adaptive or red-team attacks that iterate against the system. In a public red-teaming competition of more than 250,000 attempts against 13 frontier models, every model had at least one successful hijack.[6]

### Safety, privacy, and human-impact outcomes

**What this establishes.** That the agent avoided a specified prohibited exposure, action, scope violation, or control bypass. A short **harm screen** asks whether the intended use gives a material reason to examine outcomes by population, domain, language, role, entitlement, geography, accessibility, or other context; if so, slice evidence shows task and control outcomes per justified group.

**What this does not establish.** A favorable aggregate cannot show a critical slice is acceptable. Equal outputs are not automatically fair, because legitimate entitlements and policy rules can require different treatment. A small curated slice can expose a defect but not give a population rate. The screen requires neither collecting sensitive attributes nor one fairness metric; NIST presents its AI Risk Management Framework as voluntary guidance with no fairness threshold.[5]

**What to observe.** Record the screen before release and after material changes (BEHAVIOR-04). If differentiated harm is plausible, define slices with appropriate expertise, hold task and entitlement constant where equal treatment is the claim, keep legitimate policy differences, and report task outcomes and control failures separately. See [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

### Cost, latency, and resource performance

**What this establishes.** Whether the candidate stays inside the declared latency, call, cost, capacity, admission, backoff, or degradation behavior for the stated environment and workload.

**What this does not establish.** A good answer does not excuse crossing a stop or admission boundary; one quiet run says nothing about shared capacity; missing telemetry does not mean zero cost or no effect.

**What to observe.** When the contract or risk record has a resource, availability, capacity, or truthful-degradation claim: resource use, limit decision, user-facing degradation, and final result. Shared queues, caches, concurrency limits, or downstream capacity add their own profile.

## Apply dimensions to the actual execution context

These add claim-specific evidence only where they exist.

- **Conversation or transformed context:** assess the whole bounded episode: milestones, forbidden events, terminal result, and where material constraints came from. Test ordering sensitivity only where order should be irrelevant; a later correction, priority rule, or consent statement may be material.
- **Stored memory or cache:** assess identity or tenant scope, expiry or deletion claims, poisoning resistance, provenance through transformations, and absent, corrupt, or over-limit behavior. Conversation alone is not persistent memory.
- **Long-running, resumable, approval-waiting, or consequential work:** assess stop, recovery, approval, reconciliation, and authoritative-state claims through the controls in Part 7. Durable read-only work implies no write or approval test.
- **Multi-agent composition or remote interaction:** assess critical handoff, delegated scope, identity, source, and denial propagation, malicious-peer handling, loop limits, and end-to-end outcome. Routing does not imply a model judge, and composition does not create authority.

## Requirements

- **BEHAVIOR-01 — Outcome and constrained trajectory.** **Applicability:** all production candidates and every behavior-affecting change; trajectory clauses apply where a claim depends on an observable path, tool, boundary, provenance, retry, or stop condition. The evaluation **MUST** specify each behavior claim’s acceptable terminal outcome and relevant observable invariants. Where trajectory matters, it **MUST** separately state required or forbidden events, material partial-order constraints, permitted safe alternatives, permitted tools or capabilities and material argument constraints, provenance, and retry or stopping conditions as applicable, together with the observation that establishes each. Outcome and path results **MUST** be reported separately. Exact trace or sequence matching **MUST NOT** be the default where invariant-compliant alternatives are safe; an exact sequence gate **MUST** have a documented contract or protocol rationale. The evidence **MUST NOT** require hidden reasoning. **Observable evidence:** identified case and fixture; expected outcome and allowed variation; claim-sufficient event, source, boundary, or state observations; and separate outcome and invariant judgments.

- **BEHAVIOR-02 — Adverse behavior, relation pairs, and uncertainty.** **Applicability:** when the applicable coverage profile identifies an adverse condition; and, before exposure, when the agent accepts semantic natural-language or conversational input, uses retrieved or otherwise changeable evidence, or makes a policy, permission, currentness, or user-constraint decision. The suite **MUST** exercise the applicable missing, stale, conflicting, malformed, denied, untrusted or injected, dependency-failure, exhaustion, and uncertainty conditions and **MUST** assert both the contract-defined user-visible outcome and applicable exposure, action, provenance, or stop invariant. It **MUST** pair appropriate uncertainty or refusal cases with comparable answerable or permitted cases and **MUST** assess over-refusal separately. For the stated semantic or changeable-evidence triggers, it **MUST** include a justified applicable invariance relation and a relevant-change sensitivity relation before exposure; each relation **MUST** identify the input change, why it is irrelevant or relevant, the allowed output relation, and the expected trajectory or control relation. A fully structured no-equivalence or no-variation interface **MAY** record non-applicability with its trigger rationale. For materially stochastic user-visible claims, the suite **MUST** provide documented fresh repeated-episode evidence or a documented claim-specific alternative that actually removes variability for that claim; it **MUST NOT** treat a selected favorable transcript as repeat evidence. **Observable evidence:** versioned base and derived cases; transformation rationale and provenance; terminal and path observations for both relation members; reset and run-context observations where repeated episodes apply; and the disposition of every condition.

- **BEHAVIOR-03 — Critical controls and four-way boundary evidence.** **Applicability:** when an agent can propose or invoke restricted operations, access protected data, disclose restricted material, cross a tenant or authorization boundary, use a consequential capability, or rely on an enforced stop or limit. The suite **MUST** exercise each applicable critical control at its enforcement boundary and **MUST** retain authoritative evidence of the applicable access decision, invocation, state, recipient, or stop event. It **MUST** separately record, as applicable, model proposal or compliance, trusted-boundary authorization or denial, actual external execution, and disclosure. A blocked proposal **MUST NOT** be represented as completed external execution, and a blocked effect **MUST NOT** be represented as proof that no disclosure occurred. A model explanation, citation-presence check, or unverified transcript **MUST NOT** be the sole evidence for a critical control. The suite **MUST** include a comparable allowed counterpart when needed to demonstrate that a control did not succeed through blanket refusal. **Observable evidence:** protected-boundary decision record; permitted selection and security-relevant argument observation; authoritative state or invocation record when applicable; output and recipient-scope observation for disclosure; and paired allowed-case result.

- **BEHAVIOR-04 — Harm screen and affected slices.** **Applicability:** all production candidates before release and after a material change to intended users, data, capability, domain, or use; slice evaluation applies when the harm screen or an applicable domain policy identifies material differentiated harm. The accountable owner **MUST** record whether the harm model creates a reason for population or domain slice testing. When it does, the suite **MUST** define risk-relevant slices, evaluate affected task and control claims separately, and preserve legitimate entitlement or policy distinctions in the case design. It **MUST NOT** treat a favorable aggregate as evidence that a critical slice is acceptable. **Observable evidence:** dated harm-screen record; slice and comparator rationale; relevant task, uncertainty, refusal, and control observations by slice; qualified domain-review evidence where the applicable assurance owner requires it; and stated limitations of any curated slice.

- **BEHAVIOR-05 — Claim-sufficient provenance and evidence status.** **Applicability:** any behavioral, safety, robustness, consistency, or slice result offered as evidence. Each result **MUST** identify the claim, case, fixture, expected terminal outcome or invariant, observed outcome, claim-sufficient trajectory or boundary evidence, source or state provenance where material, evaluator, and evidence status. It **MUST** preserve `pass`, `fail`, `invalid`, or `inconclusive` status as applicable, and an invalid or inconclusive run **MUST NOT** be reported as a passing agent case. An independently observable candidate failure **MUST NOT** be relabelled invalid merely because a fixture, harness, or evaluator condition also needs repair. Records **MUST** contain only the events and material needed to establish the claim; they **MUST NOT** require raw hidden reasoning. **Observable evidence:** identified candidate and configuration; case and fixture revisions; evaluator identity; retained status and reason; linked event, source, permission, state, or recipient observations; and documented evidence limits.

## Worked example: a bounded policy answer and its dimensions

The fictional, unexecuted candidate `policy-assistant@candidate-current-selection` is ephemeral and read-only, citing approved current permission-filtered sources, with no memory, approvals, delegation, or writes. Fixture `travel-policy-current`, revision `fixture-2026-10-18.1`, holds current document `travel-policy-2026`, revision `"2026-10-01"`, with the London hotel value **GBP 220**; `travel-policy-2024-superseded`, revision `"2024-01-01"`, is superseded, not equal authority.

For `POLICY-CURRENT-001`, an authorized requester asks the London hotel value. Task outcome accepts `complete` only with GBP 220, a citation to the current permitted document, and clear wording. Source admission checks requester scope and current status; grounding checks the cited text supports the amount. No separate truth claim is needed in this controlled world unless the contract makes an external-world promise.

The trajectory claim allows safe alternatives with no reference tool count: check scope then read `travel-policy-2026`, or resolve an already admitted current record after the same check. Both pass only if no protected content returns before the scope decision, every source is permitted and current (a superseded one is never equal authority), no write is invoked, and the episode stops within its boundary. The evaluator records selection, arguments, scope decision, source revision, citation, terminal outcome, and any stop event.

`POLICY-PARAPHRASE-007` is a reviewed meaning-preserving rewrite; its invariance relation keeps GBP 220, the permitted current-source class, and the trajectory constraints. Its sensitivity pairs are `POLICY-DENIED-005` (permission to the answer-bearing source removed; expects the contract-defined bounded result and a denied access decision) and `POLICY-CONFLICT-004` (two conflicting current approved policies; expects `needs_information`). `POLICY-STALE-002` checks that a superseded conflict is recognized as superseded. Together these catch wording fragility and context-insensitive disclosure.

If the model proposes an out-of-scope retrieval in `POLICY-DENIED-005`, that is a compliance failure if the contract says so; the denial is enforcement success; no authorized retrieval record shows the document was not returned through that boundary; and a separate output and recipient-scope check shows whether disclosure occurred. Neither a completed action nor non-disclosure is inferred from the denial.

`POLICY-MISSING-003` withholds permitted supporting evidence, and `POLICY-EXHAUSTION-008` makes retrieval unavailable after the declared stop condition. Each expects a defined uncertainty, failure, or bounded partial outcome, never a fabricated amount, citation, or zero-cost claim, and a comparable allowed case rules out blanket refusal. On exhaustion the record shows no new spend-producing work was admitted after the stop; this assesses honest degradation, not that all later billing is known. `POLICY-INJECTION-006` puts a harmless instruction in an untrusted retrieved channel; evidence checks it is not treated as policy, no out-of-scope content reaches the requester, and no prohibited invocation occurs.

Fresh `POLICY-CURRENT-001` episodes test fixed-world reliability only if each starts from the named fixture and permission context and meets both the GBP 220 predicate and the trajectory invariants. Comparison with `policy-assistant@baseline-current-selection` is in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

The owner also records a harm screen. If country rules (which may legitimately change results) or supported-language access could create differentiated harm, the suite adds country-rule cases and matched same-entitlement wording cases, with disclosure or denial evidence per slice, reporting completion, `needs_information`, decline, failure, and scope-control failure separately.

## Evidence and checklist

- [ ] Each material claim names the user-visible outcome, evidence scope, and limit, not a generic quality label.
- [ ] Task success, source admission/currentness, grounding, factual correctness, and uncertainty are separate claims where each matters.
- [ ] Outcome and end state are graded first; trajectory cases use invariants and allowed alternatives, not a brittle reference trace.
- [ ] Critical-control evidence separates proposal, boundary decision, execution, and disclosure.
- [ ] Adverse cases cover plausible conditions; injection-resistance claims rest on adaptive or red-team attacks, not only fixed cases.
- [ ] Triggered relation pairs have paired outcome and control evidence.
- [ ] Repeated episodes start from clean state and keep each run's outcome, controls, reset context, and status.
- [ ] The harm screen is recorded; triggered slices separate task outcomes from control failures.
- [ ] Resource claims observe the limit, degradation, and final result.

## References

[1]: https://arxiv.org/html/2408.04682v1 "ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities"
[2]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for Natural Language Processing"
[3]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[4]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[5]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
[6]: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition "NIST CAISI: Insights into AI Agent Security from a Large-Scale Red-Teaming Competition"

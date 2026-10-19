# 4.3 Evaluation Types and Dimensions

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Builders, evaluators, security and privacy reviewers, and accountable owners  
**Applicability:** Use this chapter whenever evidence supports a design, exposure, release, or behavior-affecting change decision. Claim families and profiles apply only when their contract, capability, input, user, or harm trigger is present.  
**Reader question:** What should we measure or judge about the agent?

This chapter explains the **claims** an evaluation can establish. It prescribes no single grader, trial count, threshold, or release conclusion. Start with the [Part 4 overview](README.md); use [applicability](../../applicability.md) to see whether a trigger is present and [4.6](06-standards-required-coverage-and-execution-cadence.md) to map profiles to cases. [4.2](02-test-levels-techniques-and-suite-purposes.md) covers how to exercise a claim, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) how an observation becomes a trustworthy judgment, [4.5](05-planning-designing-and-running-tests-and-evaluations.md) the process, and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) aggregation and decisions. The [practical reference](reference/README.md) has integrated records and templates.

## Start with a bounded claim, not an "eval type"

Describe each case by its technical boundary, claim family, evaluator method, suite purpose, and environment. This chapter covers the **claim family**: the property a result is meant to establish.

A useful claim says what is in scope, which terminal outcomes are acceptable, what evidence can establish it, and its limits. One policy answer may need several claims:

- Task outcome: did the assistant answer the policy question usefully?
- Source admission: was the source permitted and current?
- Grounding: is each material assertion supported by that source?
- Trajectory: did the assistant respect scope and stop boundaries?

None of these establishes the others. Fluent prose is not task success; a source identifier is not semantic support; a source can be grounded yet stale; and a good final answer does not show the path was allowed.

## Dimensions to assess

### Task success and user usefulness

**What this establishes.** Whether the contract-defined result solves the bounded user task. The result can be `complete`, `needs_information`, `declined`, `failed`, or a contract-defined partial or escalation outcome. Usefulness can include completeness, clarity, and actionability when the task needs them.

**What it does not establish.** Source permission, factual truth, safety, or a compliant path. A convincing answer can still use an out-of-scope document or omit a material qualification.

**What to observe.** Record the case input and user context, the expected terminal outcome, any relevant final state, and an evaluator that can judge the task. Grade what the agent produced, and the end state it left behind, before grading how it got there. For a controlled policy fixture, a reference value plus qualified review of wording variation work well together.

**Example.** A permitted employee asks for the London hotel limit. `complete` is useful only if the answer gives the right amount, clearly, with the required policy citation. A polished reply that asks for information already present is over-refusal.

### Trajectory, tool use, and control compliance

**What this establishes.** A **trajectory** is the observable ordered or partly ordered record of events relevant to a claim: selected capability and material arguments, validation or authorization decision, tool result, retry, stop, user-facing artifact, handoff, and authoritative state or effect. A trajectory claim establishes that the necessary constraints held while the task progressed.

**Grade outcomes first; reserve path assertions for constraints.** Agents often find valid routes you did not anticipate, so a rigid expected tool sequence fails correct runs. State the terminal outcome separately, then assert only **path invariants**: conditions that must hold on any safe path. Examples are authorizing before returning protected content, retrieving only an in-scope current source, using only permitted capabilities and arguments, performing no write, and stopping at the declared limit. Independent reads may happen in either order; authorization before disclosure is a real dependency. One agent-tool benchmark likewise models required milestones and forbidden actions as partial ordering instead of one exact trace.[1] Use exact-sequence matching only where a protocol or control makes order material, such as binding an approved immutable payload before an effect.

**What it does not establish.** A tool name does not show its arguments were safe, and safe arguments do not show a protected boundary authorized the request. A transcript saying an effect occurred is not an authoritative observation of it. Trajectory evaluation does not need private reasoning.

**What to observe.** This matters when a claim depends on retrieval, an interface, an admitted tool, a stop or budget boundary, provenance, a handoff, or a prohibited action. Assess permitted tool selection, security-relevant arguments, and dependency order as separate properties. Capture provenance sufficient for the claim: source or state identity, scope, revision or freshness, and the boundary or state observation that supports it. Add retry and stop observations where failure, duplicate work, cost, or a consequential effect can matter.

**Example.** Two paths can safely answer a policy question: locate a permitted current source after a scope decision, or read an already admitted current record after the same decision. Neither must match a reference tool count. Both fail if they retrieve a restricted document before authorization, treat a superseded source as equal authority, or continue after a declared stop.

#### Keep proposal, boundary, execution, and disclosure distinct

A label like "unauthorized attempt" hides four observations:

1. **Proposal or compliance:** the model proposes an out-of-scope operation.
2. **Boundary decision:** the trusted boundary authorizes or denies it.
3. **Execution:** authoritative state shows an external action did or did not occur.
4. **Disclosure:** restricted material reached an unpermitted recipient or output.

A prohibited proposal that the boundary denies can fail a model-compliance claim while showing that enforcement worked. It is not an unauthorized execution. A blocked write does not show that no disclosure occurred. Record these fields separately. Pair each denied case with a comparable permitted case so a system that declines all work cannot look safe.

### Consistency, relations, and repeated-run reliability

**What this establishes.** **Fixed-world repeated-run reliability** asks whether freshly initialized episodes of the same case, fixture, permission context, and run policy repeatedly give the correct terminal outcome and satisfy every required invariant. Equivalent wording is allowed when the claim allows it. It is not byte-for-byte sameness, and it is not consistent wrongness: repeatedly returning GBP 200, refusing an allowed request, or following an unsafe path is not reliability.

Two relation checks answer different questions:

- An **invariance relation** changes something justified as irrelevant to the claim and keeps the required answer and controls. Candidates are a reviewed paraphrase or reordering of truly independent facts.
- A **sensitivity relation** changes something material and produces the contractually required change in answer, boundary decision, or uncertainty. Examples are losing permission, replacing a current policy with conflicting current evidence, or changing a material user constraint.

A metamorphic relation makes the input relation and expected output relation explicit. It can reveal a violation where a full answer oracle is hard to write, but it does not prove factual truth.[2]

**What this does not establish.** Fresh repeats of one curated case do not establish field reliability. Invariance without sensitivity can reward an agent for ignoring context. A variant that looks like a paraphrase is valid only with a stated reason that it preserves or changes meaning. Repeat evidence does not replace correctness or trajectory evidence, or the analysis in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**What to observe.** Material stochastic user-visible claims need fresh repeated-episode evidence, or a documented claim-specific alternative that actually removes the variability. Record the candidate and resolved route, fixed and varying sources, fresh initialization and reset observation, each terminal outcome, path evidence, and evidence status. Do not silently pick a favorable run. Start every trial from a clean state so leftover files, caches, or records cannot make trials depend on each other. Metrics, denominators, retry aggregation, dependence assumptions, and comparison belong in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

For semantic natural-language or conversational input, changeable evidence, or decisions based on policy, permission, currentness, or user constraints, identify at least one invariance relation and one sensitivity relation before exposure. A fully structured interface with no semantic-equivalence or variation claim can record why they do not apply.

**Example.** A reviewed paraphrase of an authorized London-policy question keeps the GBP 220 answer, the permitted current-source class, and the no-prohibited-invocation invariant. The related permission-loss case instead gives the contract-defined bounded outcome and a denied boundary observation. Together they catch both wording fragility and context-insensitive disclosure.

### Grounding, retrieval quality, and factual correctness

**What this establishes.** Retrieval **relevance**: does an item bear on the query? Evidence **coverage**: is the material evidence needed for the answer present? **Admissibility and currentness**: is the source permitted for this requester and use, and current at the relevant time? **Semantic grounding**: is each material assertion supported by identified source text in context? **Factual correctness**: is the assertion true against an independent truth reference at the relevant time?

**What this does not establish.** These are separate claims. A relevant document may omit a needed rule. A current permitted document may not support an invented exception. An answer may faithfully report a stale source yet fail factual correctness. A citation's presence, resolvability, relevance, or authority is not semantic support. Retrieval research likewise treats relevance, faithfulness, and correctness as separate targets, with some overlap.[3]

**What to observe.** This matters whenever retrieved or changeable evidence affects an outcome or the product promises sourced assertions. Keep the approved source record, permission decision, revision or status, claim-to-source support evidence, and any independent truth reference distinct. If no authoritative truth reference exists, state that limit instead of calling a heuristic ground truth.

**Example.** The current travel policy supports "the London hotel value is GBP 220" for an authorized requester. It does not support an invented exception. A superseded document with a conflicting amount needs currentness handling; it is not equal authority just because it is relevant.

### Robustness, uncertainty, and failure recovery

**What this establishes.** Contract-correct behavior under plausible adverse conditions: missing, stale, conflicting, malformed, denied, injected, timeout, partial, or exhausted. That includes appropriate clarification, uncertainty, decline, failure, or bounded partial results, and safe recovery and stopping where the contract requires them.

**What this does not establish.** A generic adversarial-prompt list is not a security claim, and a fluent fallback is not a successful fallback when its support is absent. Appropriate uncertainty is not usefulness if comparable answerable cases are refused.

**What to observe.** Choose adverse conditions from the enabled capabilities and the risk record. Put untrusted instructions in the real channel under test: an instruction inside a retrieved document tests a different boundary than a user instruction. Observe the exposure, attempted invocation, boundary decision, state, or stop event rather than a refusal-like sentence. OWASP describes indirect prompt injection as untrusted external content that changes model behavior, and presents adversarial testing as one layer beside privilege controls and validation.[4] Fixed injection cases show only that known attacks fail. Evidence of injection resistance needs adaptive or red-team attacks that iterate against the system. In a public red-teaming competition of more than 250,000 attempts against 13 frontier models, every model had at least one successful hijack.[6]

**Example.** With two conflicting current approved policies, the assistant returns `needs_information` and not an invented amount. With missing permitted evidence or an exhausted retrieval budget, it returns the contract-defined uncertainty or failure outcome, cites no fabricated source, and starts no new work after the stop. A comparable allowed case confirms this is not blanket refusal.

### Safety, privacy, and human-impact outcomes

**What this establishes.** That the agent avoided a specified prohibited exposure, action, scope violation, or control bypass. A short **harm screen** establishes whether the intended use gives a material reason to examine outcomes by population, domain, language, role, entitlement, geography, accessibility, or other context. If it does, slice evidence shows task and control outcomes for the justified groups.

**What this does not establish.** A favorable aggregate cannot show a critical slice is acceptable. Equal outputs are not automatically fair, because legitimate entitlements and policy rules can require different treatment. A small curated slice can expose a defect but not give a population rate. The screen does not require collecting sensitive attributes or one universal fairness metric. NIST presents its AI Risk Management Framework as voluntary guidance and sets no fairness threshold.[5]

**What to observe.** Record the harm-screen question and conclusion before release and revisit it after a material change to users, data, capability, domain, or use. If differentiated harm is plausible, define slices with appropriate expertise, hold task and entitlement constant where equal treatment is the claim, keep legitimate policy differences, and report task outcomes and control failures separately. Detailed assurance is in [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

**Example.** Country rules may legitimately change a travel-policy result, while equivalent authorized wording in supported languages should not cause an unexplained refusal or scope failure. Separate country-policy outcomes from matched wording cases and keep disclosure or denial evidence visible for each slice.

### Cost, latency, and resource performance

**What this establishes.** Whether the candidate stays inside the declared latency, call, cost, capacity, admission, backoff, or degradation behavior for the stated environment and workload.

**What this does not establish.** A good answer does not make up for crossing a safe stop or admission boundary. One quiet run does not show behavior under shared capacity, and missing telemetry does not mean zero cost or no effect.

**What to observe.** Assess this when the contract or risk record has a resource, availability, capacity, or truthful-degradation claim. Observe resource use, the limit decision, user-facing degradation, and the final result. Shared queues, caches, concurrency limits, or downstream capacity add their own profile.

**Example.** On `POLICY-EXHAUSTION-008`, the assistant reaches its declared retrieval boundary, gives the contract-defined failure or bounded response, and records that no new spend-producing work was admitted after the stop. The case assesses honest degradation and stopping, not that all later billing is known.

## Apply dimensions to the actual execution context

Conversation, memory, durable work, and composition add claim-specific evidence; they are not dimensions every agent needs.

- **Conversation or transformed context:** assess the whole bounded episode, including milestones, forbidden events, terminal result, and where material constraints came from. Test ordering sensitivity only where order is meant to be irrelevant; a later correction, priority rule, or consent statement may be material.
- **Stored memory or cache:** when it exists and affects behavior, assess identity or tenant scope, expiry or deletion claims, poisoning resistance, provenance through transformations, and absent, corrupt, or over-limit behavior. A conversation alone does not show persistent memory.
- **Long-running, resumable, approval-waiting, or consequential work:** assess stop, recovery, approval, reconciliation, and authoritative-state claims through the controls in Part 7. Durable read-only work implies no write or approval test.
- **Multi-agent composition or remote interaction:** assess critical handoff, delegated scope, identity and source propagation, denial propagation, malicious-peer handling, loop limits, and end-to-end outcome when those exist. Routing does not imply a model judge, and composition does not create authority.

## Requirements

- **BEHAVIOR-01 — Outcome and constrained trajectory.** **Applicability:** all production candidates and every behavior-affecting change; trajectory clauses apply where a claim depends on an observable path, tool, boundary, provenance, retry, or stop condition. The evaluation **MUST** specify each behavior claim’s acceptable terminal outcome and relevant observable invariants. Where trajectory matters, it **MUST** separately state required or forbidden events, material partial-order constraints, permitted safe alternatives, permitted tools or capabilities and material argument constraints, provenance, and retry or stopping conditions as applicable, together with the observation that establishes each. Outcome and path results **MUST** be reported separately. Exact trace or sequence matching **MUST NOT** be the default where invariant-compliant alternatives are safe; an exact sequence gate **MUST** have a documented contract or protocol rationale. The evidence **MUST NOT** require hidden reasoning. **Observable evidence:** identified case and fixture; expected outcome and allowed variation; claim-sufficient event, source, boundary, or state observations; and separate outcome and invariant judgments.

- **BEHAVIOR-02 — Adverse behavior, relation pairs, and uncertainty.** **Applicability:** when the applicable coverage profile identifies an adverse condition; and, before exposure, when the agent accepts semantic natural-language or conversational input, uses retrieved or otherwise changeable evidence, or makes a policy, permission, currentness, or user-constraint decision. The suite **MUST** exercise the applicable missing, stale, conflicting, malformed, denied, untrusted or injected, dependency-failure, exhaustion, and uncertainty conditions and **MUST** assert both the contract-defined user-visible outcome and applicable exposure, action, provenance, or stop invariant. It **MUST** pair appropriate uncertainty or refusal cases with comparable answerable or permitted cases and **MUST** assess over-refusal separately. For the stated semantic or changeable-evidence triggers, it **MUST** include a justified applicable invariance relation and a relevant-change sensitivity relation before exposure; each relation **MUST** identify the input change, why it is irrelevant or relevant, the allowed output relation, and the expected trajectory or control relation. A fully structured no-equivalence or no-variation interface **MAY** record non-applicability with its trigger rationale. For materially stochastic user-visible claims, the suite **MUST** provide documented fresh repeated-episode evidence or a documented claim-specific alternative that actually removes variability for that claim; it **MUST NOT** treat a selected favorable transcript as repeat evidence. **Observable evidence:** versioned base and derived cases; transformation rationale and provenance; terminal and path observations for both relation members; reset and run-context observations where repeated episodes apply; and the disposition of every condition.

- **BEHAVIOR-03 — Critical controls and four-way boundary evidence.** **Applicability:** when an agent can propose or invoke restricted operations, access protected data, disclose restricted material, cross a tenant or authorization boundary, use a consequential capability, or rely on an enforced stop or limit. The suite **MUST** exercise each applicable critical control at its enforcement boundary and **MUST** retain authoritative evidence of the applicable access decision, invocation, state, recipient, or stop event. It **MUST** separately record, as applicable, model proposal or compliance, trusted-boundary authorization or denial, actual external execution, and disclosure. A blocked proposal **MUST NOT** be represented as completed external execution, and a blocked effect **MUST NOT** be represented as proof that no disclosure occurred. A model explanation, citation-presence check, or unverified transcript **MUST NOT** be the sole evidence for a critical control. The suite **MUST** include a comparable allowed counterpart when needed to demonstrate that a control did not succeed through blanket refusal. **Observable evidence:** protected-boundary decision record; permitted selection and security-relevant argument observation; authoritative state or invocation record when applicable; output and recipient-scope observation for disclosure; and paired allowed-case result.

- **BEHAVIOR-04 — Harm screen and affected slices.** **Applicability:** all production candidates before release and after a material change to intended users, data, capability, domain, or use; slice evaluation applies when the harm screen or an applicable domain policy identifies material differentiated harm. The accountable owner **MUST** record whether the harm model creates a reason for population or domain slice testing. When it does, the suite **MUST** define risk-relevant slices, evaluate affected task and control claims separately, and preserve legitimate entitlement or policy distinctions in the case design. It **MUST NOT** treat a favorable aggregate as evidence that a critical slice is acceptable. **Observable evidence:** dated harm-screen record; slice and comparator rationale; relevant task, uncertainty, refusal, and control observations by slice; qualified domain-review evidence where the applicable assurance owner requires it; and stated limitations of any curated slice.

- **BEHAVIOR-05 — Claim-sufficient provenance and evidence status.** **Applicability:** any behavioral, safety, robustness, consistency, or slice result offered as evidence. Each result **MUST** identify the claim, case, fixture, expected terminal outcome or invariant, observed outcome, claim-sufficient trajectory or boundary evidence, source or state provenance where material, evaluator, and evidence status. It **MUST** preserve `pass`, `fail`, `invalid`, or `inconclusive` status as applicable, and an invalid or inconclusive run **MUST NOT** be reported as a passing agent case. An independently observable candidate failure **MUST NOT** be relabelled invalid merely because a fixture, harness, or evaluator condition also needs repair. Records **MUST** contain only the events and material needed to establish the claim; they **MUST NOT** require raw hidden reasoning. **Observable evidence:** identified candidate and configuration; case and fixture revisions; evaluator identity; retained status and reason; linked event, source, permission, state, or recipient observations; and documented evidence limits.

## Worked example: a bounded policy answer and its dimensions

The fictional candidate is `policy-assistant@candidate-current-selection`. It is ephemeral and read-only: it answers from approved current permission-filtered sources with citations, and has no persisted memory, approval step, delegated agents, or write capability. The controlled fixture is `travel-policy-current`, revision `fixture-2026-10-18.1`. Its current document is `travel-policy-2026`, revision `"2026-10-01"`; the fictional London hotel value is **GBP 220**. `travel-policy-2024-superseded`, revision `"2024-01-01"`, is superseded, not equal authority. Everything here is fictional and unexecuted.

For `POLICY-CURRENT-001`, an authorized requester asks for the London hotel value. The task-outcome claim accepts `complete` with GBP 220, a citation to the current permitted document, and understandable wording. The source-admission claim checks requester scope and current-document status. The grounding claim checks that the amount is supported by the cited text. A separate truth claim is unnecessary in this controlled world unless the contract adds an external-world promise.

The trajectory claim allows safe alternatives. One episode checks requester scope and then reads `travel-policy-2026`; another resolves an already admitted current record after the same check. Both satisfy the claim if protected content is not returned before the scope decision, every used source is permitted and current, no write is invoked, and the episode ends within its declared boundary. The evaluator records selection, source and requester arguments, scope decision, source revision, final citation, terminal outcome, and any stop event. It asks for no reasoning trace and does not require the same incidental read sequence.

`POLICY-PARAPHRASE-007` is a reviewed meaning-preserving rewrite of the same question. Its invariance relation keeps the GBP 220 result, permitted current-source class, and trajectory constraints even when prose differs. Its paired sensitivity checks are meaningful changes: `POLICY-DENIED-005` removes the requester’s permission to the answer-bearing source, and `POLICY-CONFLICT-004` presents two current approved policies with conflicting values. The first expects the contract-defined bounded result and a denied access decision; the second expects `needs_information`. `POLICY-STALE-002` checks that a superseded conflict is recognized as superseded.

These cases also show the four-way boundary distinction. Suppose the model proposes an out-of-scope retrieval in `POLICY-DENIED-005`. That can be recorded as a compliance failure if the contract treats it so. The trusted boundary’s denial is enforcement success. The absence of an authorized retrieval record shows the restricted document was not returned through that boundary. A separately inspected output and recipient scope shows whether disclosure occurred. The evaluator never calls the blocked proposal a completed action or infers non-disclosure from the denial alone.

`POLICY-MISSING-003` withholds permitted supporting evidence, while `POLICY-EXHAUSTION-008` makes the retrieval dependency unavailable after the declared stop condition. Each expects a defined uncertainty, failure, or bounded partial outcome, not a fabricated amount, citation, or zero-cost claim. `POLICY-INJECTION-006` places a harmless embedded instruction in an untrusted retrieved channel. The evidence checks that the content is not treated as policy, no out-of-scope content reaches the requester, and the read-only configuration shows no prohibited invocation.

Fresh episodes of `POLICY-CURRENT-001` test fixed-world reliability only when each starts from the named fixture and permission context and meets both the GBP 220 predicate and the trajectory invariants. The record keeps each outcome and status and sets no universal repeat count or field rate. Numerical summary, retry policy, and comparison with `policy-assistant@baseline-current-selection` are in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

Finally, the owner records a harm screen. If country-specific rules or supported-language access could create differentiated harm, the suite adds country-rule cases and matched same-entitlement wording cases, and reports useful completion, `needs_information`, decline, failure, and scope-control failure separately.

## Evidence and checklist

Use [4.6](06-standards-required-coverage-and-execution-cadence.md) to select profiles and [4.5](05-planning-designing-and-running-tests-and-evaluations.md) to keep case, fixture, and execution records.

- [ ] Each material claim names the user-visible outcome, evidence scope, and limit, not a generic quality label.
- [ ] Task success, source admission/currentness, grounding, factual correctness, and uncertainty are distinct claims where each matters.
- [ ] Outcome and end state are graded first; trajectory cases use invariants, partial ordering, allowed alternatives, capability and argument constraints, provenance, and stop conditions instead of a brittle reference trace.
- [ ] Critical-control evidence separates proposal, boundary decision, execution, and disclosure, with an allowed counterpart where blanket refusal could hide failure.
- [ ] Adverse cases cover conditions the enabled capabilities and risks make plausible, including safe uncertainty and recovery. Injection-resistance claims rest on adaptive or red-team attacks, not only fixed cases.
- [ ] Where semantic or changeable-evidence triggers apply, there is an invariance relation and a sensitivity relation with paired outcome and control evidence.
- [ ] Where material stochastic behavior remains, fresh clean-state episodes keep each run’s outcome, control observations, reset context, and status, with no universal count or field-rate claim.
- [ ] The harm screen is recorded, and triggered slices separate task outcomes from control failures while keeping legitimate policy differences.
- [ ] Resource claims observe the limit, degradation, and final result.
- [ ] Every evidence item links to the candidate, case, fixture, evaluator, material event or provenance, and an honest pass, fail, invalid, or inconclusive status.

## References

[1]: https://arxiv.org/html/2408.04682v1 "ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities"
[2]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for Natural Language Processing"
[3]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[4]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[5]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
[6]: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition "NIST CAISI: Insights into AI Agent Security from a Large-Scale Red-Teaming Competition"

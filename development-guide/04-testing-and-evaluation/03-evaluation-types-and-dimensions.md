# 4.3 Evaluation Types and Dimensions

**Status:** 0.5.0-draft.2 assembled draft — proposed, not adopted
**Audience:** Builders, evaluators, security and privacy reviewers, and accountable owners  
**Applicability:** Use this chapter whenever evidence supports a material design, exposure, release, or behavior-affecting change decision. The claim families and profiles apply only when their stated contract, capability, input, user, or harm trigger is present.  
**Reader question:** What should we measure or judge about the agent?

This chapter explains the **claims** an evaluation can establish. It does not prescribe one tool tree, grader, trial count, threshold, or release conclusion. Start with the [Part 4 overview](README.md), use [applicability](../../applicability.md) to determine whether a trigger is present, and use [4.6 Standards, Required Coverage, and Execution Cadence](06-standards-required-coverage-and-execution-cadence.md) to map applicable profiles to cases. [4.2 Test Levels, Techniques, and Suite Purposes](02-test-levels-techniques-and-suite-purposes.md) explains how to exercise a claim; [4.4 Evaluators, Metrics, Rubrics, and Calibration](04-evaluators-metrics-rubrics-and-calibration.md) explains how an observation becomes a trustworthy judgment; [4.5 Planning, Designing, and Running Tests and Evaluations](05-planning-designing-and-running-tests-and-evaluations.md) records the process; and [4.7 Analyzing Results, Comparing Versions, and Making Decisions](07-analyzing-results-comparing-versions-and-making-decisions.md) handles trial aggregation and decision interpretation. See the [practical reference](reference/README.md) for integrated records and templates.

## Start with a bounded claim, not an “eval type”

Tests and evaluations overlap. A deterministic check can contribute to an evaluation, and a variable agent can be tested. Rather than sorting work into two separate universes, describe each case by its technical boundary, claim family, evaluator method, suite purpose, and lifecycle or environment. This chapter concerns the **claim family**: the property that a result is intended to establish.

A useful claim says what is in scope, which terminal outcomes are acceptable, the evidence that can establish it, and its limits. The policy assistant used here illustrates why one answer may need several claims:

- A task-outcome claim asks whether the assistant answered the policy question usefully.
- A source-admission claim asks whether the source was permitted and current.
- A grounding claim asks whether the answer’s material assertion is supported by that source.
- A trajectory claim asks whether the assistant observed the applicable scope and stop boundaries while answering.

None of these establishes the others automatically. In particular, fluent prose is not task success; a source identifier is not semantic support; a source can be grounded yet stale for a separate truth claim; and a successful terminal answer is not proof that the path was allowed.

## Dimensions to assess

### Task success and user usefulness

**What this establishes.** A task-outcome claim establishes whether the contract-defined result solves the bounded user task. The appropriate result can be `complete`, `needs_information`, `declined`, `failed`, or a contract-defined partial or escalation outcome. Usefulness can include completeness, clarity, and actionability when those matter to the stated user task.

**What it does not establish.** It does not establish source permission, factual truth, safety, or a compliant action path. A convincing answer can still use an out-of-scope document or omit a material qualification.

**When it matters and what to observe.** It matters for every material user-facing contract. Record the case input and user context, expected terminal outcome, any relevant final state, and an evaluator that can judge the bounded task. For a controlled policy fixture, a reference value and qualified review of any permitted wording variation can complement each other.

**Small example.** A permitted employee asks for the London hotel limit. `complete` is useful only if the answer gives the applicable amount, communicates it clearly, and cites the required policy evidence. A polished response that asks for information already present is an over-refusal rather than a useful completion.

### Trajectory, tool use, and control compliance

**What this establishes.** A **trajectory** is the observable ordered or partially ordered event record relevant to a claim: selected capability and material arguments, validation or authorization decision, tool result, retry, stop, user-facing artifact, handoff, and authoritative state or effect where relevant. A trajectory claim establishes whether the necessary constraints held while the task progressed.

A useful default is a **path invariant** rather than a literal transcript. State the terminal outcome separately from the conditions that must hold across any safe path. For example: authorize access before returning protected content; retrieve only an in-scope current source; use only permitted capabilities and arguments; perform no write; and stop after the declared limit. Independent reads may happen in either order, while authorization before protected disclosure is a real dependency. One agent-tool benchmark likewise represents required milestones and forbidden actions through partial ordering instead of one exact trace; that is a useful design example, not a required trace format.[1]

**What it does not establish.** A tool name does not show that its arguments were safe, and safe arguments do not show that a protected boundary authorized or executed the request. A transcript saying that an effect occurred is not an authoritative observation of that effect. Trajectory evaluation also does not require private reasoning or infer it from calls; it uses only the observable events needed for the claim.

**When it matters and what to observe.** This dimension matters when a claim depends on retrieval, an interface, an admitted tool, a stop or budget boundary, source provenance, a handoff, or a prohibited action. Assess permitted tool selection, security-relevant arguments, and dependency order as separate properties. Capture provenance sufficient for the claim: source or state identity, applicable scope, revision or freshness, and the boundary or state observation that supports it. Add retry and stopping observations when failure, duplicate work, cost, or a consequential effect can matter.

**Small example.** Two paths can safely answer a policy question: a permitted current source can be located after a scope decision, or an already admitted current record can be read after that same decision. Neither path needs to match a reference tool count. Both fail if they retrieve a restricted document before authorization, use a superseded source as equal authority, or continue after a declared stop. Exact-sequence matching is useful only where a protocol or control makes the exact order material, such as binding an approved immutable payload before an effect.

#### Keep proposal, boundary, execution, and disclosure distinct

A single label such as “unauthorized attempt” hides four different observations:

1. **Proposal or compliance:** the model proposes an out-of-scope operation.
2. **Boundary decision:** the trusted boundary authorizes or denies the request.
3. **Execution:** authoritative state shows that an external action occurred or did not occur.
4. **Disclosure:** restricted material reached an unpermitted recipient or output.

A prohibited proposal that the boundary denies can fail a separately declared model-compliance claim while showing successful enforcement. It is not an unauthorized execution. Conversely, a blocked write does not establish that no disclosure occurred. Record the applicable fields separately so that a reviewer can identify a proposal, enforcement decision, state change, and recipient observation without guessing from a narrative. Pair a denied case with a comparable permitted case when otherwise a system that declines all work could appear safe.

### Consistency, relations, and repeated-run reliability

**What this establishes.** **Fixed-world repeated-run reliability** asks whether newly initialized episodes of the same identified case, fixture, permission context, and run policy repeatedly produce the correct terminal outcome and satisfy every required observable invariant. It permits semantically equivalent wording when the claim allows it. It is not byte-for-byte sameness and it is not consistent wrongness: repeatedly returning GBP 200, refusing an allowed request, or following an unsafe path does not become reliable behavior.

Two relation-based checks answer different questions:

- An **invariance relation** changes something that is justified as irrelevant to the claim and preserves the required answer and controls. A reviewed paraphrase or an ordering change of truly independent facts can be candidates.
- A **sensitivity relation** changes something that is material and produces the contractually required change in answer, boundary decision, or uncertainty. Losing permission, replacing a current policy with conflicting current evidence, or changing a material user constraint are examples.

A metamorphic relation makes the input relation and expected output relation explicit; it can reveal a violation where a complete answer oracle is difficult, but it does not prove factual truth.[2]

**What this does not establish.** Fresh repeats of one curated case do not establish field reliability across a population. Invariance without sensitivity can reward an agent for ignoring context. Relation variants are not valid merely because they look like paraphrases: the team needs a stated reason that a transformation preserves or changes meaning. Repeated-run evidence does not replace task correctness, trajectory evidence, or the release analysis in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

**When it matters and what to observe.** Material stochastic user-visible claims need fresh repeated-episode evidence, or a documented, claim-specific alternative that actually removes variability from the claim. The record identifies the candidate and resolved route, fixed and varying sources, fresh initialization and reset observation, each terminal outcome, applicable path evidence, and each evidence status. It does not silently select only a favorable run. Numerical metrics, denominators, retry/selection-policy aggregation, dependence assumptions, and candidate comparison belong in [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md), not here.

For semantic natural-language or conversational input, changeable evidence, or decisions based on policy, permission, currentness, or user constraints, identify at least one applicable invariance relation and one applicable sensitivity relation before exposure. A fully structured interface that makes no semantic-equivalence or relevant-variation claim can record why those relations do not apply. Additional relation pairs are useful where they illuminate a material robustness claim.

**Small example.** A reviewed paraphrase of an authorized London-policy question preserves the required GBP 220 answer, permitted current-source class, and no-prohibited-invocation invariant. The related permission-loss case instead produces the contract-defined bounded outcome and a denied boundary observation. The two checks prevent both wording fragility and context-insensitive disclosure.

### Grounding, retrieval quality, and factual correctness

**What this establishes.** Retrieval **relevance** asks whether an item bears on the query. Evidence **coverage** asks whether the material evidence needed for an answer is present. **Admissibility and currentness** ask whether the source is permitted for this requester and use and current at the relevant time. **Semantic grounding** asks whether each material assertion is supported by identified source text in context. **Factual correctness** asks whether the assertion is true against the appropriate independent truth reference at the relevant time.

**What this does not establish.** These are separate claims. A relevant document may omit a necessary rule. A current permitted document may not support an invented exception. An answer may accurately report a stale source yet fail a separate factual-correctness claim. A citation’s presence, resolvability, topical relevance, or authority alone is not semantic support. Retrieval research similarly treats relevance, faithfulness, correctness, and answer quality as distinct targets.[3]

**When it matters and what to observe.** This family matters whenever retrieved or changeable evidence affects an outcome, or when the product promises sourced factual assertions. Keep the approved source record, permission decision, revision or status, claim-to-source support evidence, and any independent truth reference distinct. If an authoritative truth reference is unavailable, qualify that limit rather than calling a heuristic ground truth.

**Small example.** The current travel policy can support “the London hotel value is GBP 220” for an authorized requester. It does not support a made-up exception. A superseded document with a conflicting amount is evidence that requires currentness handling, not equal authority merely because it is relevant.

### Robustness, uncertainty, and failure recovery

**What this establishes.** Robustness establishes contract-correct behavior under plausible adverse conditions: missing, stale, conflicting, malformed, denied, injected, timeout, partial, or exhausted conditions. It includes appropriate clarification, uncertainty, decline, failure, or bounded partial results, as well as safe recovery and stopping behavior where those are part of the contract.

**What this does not establish.** A generic adversarial-prompt collection is not a security claim, and a fluent fallback is not a successful fallback when its support is absent. Appropriate uncertainty is also not proof of usefulness if comparable answerable cases are unnecessarily refused.

**When it matters and what to observe.** Choose adverse conditions from the agent’s enabled capabilities and risk record. Place untrusted instructions in the real channel being assessed: an instruction embedded in a retrieved document tests a different boundary from a user instruction. Observe the claimed exposure, attempted invocation, boundary decision, state, or stop event rather than relying on a refusal-like sentence. OWASP describes indirect prompt injection as untrusted external content that changes model behavior and presents adversarial testing as one layer alongside privilege controls and validation.[4]

**Small example.** With two current approved policies that conflict, the assistant returns `needs_information` rather than inventing an amount. With missing permitted evidence or an exhausted retrieval budget, it returns the contract-defined uncertainty or failure outcome, cites no fabricated source, and stops new work after the recorded stop decision. A comparable allowed case confirms that this is not blanket refusal.

### Safety, privacy, and human-impact outcomes

**What this establishes.** Safety and privacy claims establish that the agent avoided a specified prohibited exposure, action, scope violation, or control bypass. A concise **harm screen** establishes whether the intended use creates a material reason to examine outcomes by population, domain, language, role, entitlement, geography, accessibility, or another context. When the screen identifies a concern, slice evidence establishes the affected task and control outcomes for the justified groups.

**What this does not establish.** A favorable aggregate cannot show that a critical slice is acceptable. Equal numeric outputs are not automatically fair: legitimate entitlements and policy rules can require different treatment. A small curated slice can expose a defect but does not itself establish a population-wide rate. The screen does not require collecting sensitive attributes or using one universal fairness metric. NIST presents its AI Risk Management Framework as voluntary guidance for incorporating trustworthiness considerations into AI design, development, use, and evaluation; it does not supply a universal fairness threshold.[5]

**When it matters and what to observe.** Record the harm-screen question and conclusion before release and revisit it after a material change to users, data, capability, domain, or intended use. If a differentiated harm is plausible, define relevant slices with appropriate expertise, hold task and entitlement constant where equal treatment is the claim, preserve meaningful policy differences, and report task outcomes and control failures separately. Detailed human-impact and domain assurance remain with [10.2 Bias, Human Impact, and Domain Assurance](../../engineering-reference/10-risk-privacy-and-specialized-assurance/02-bias-human-impact-and-domain-assurance.md).

**Small example.** Country rules may legitimately change a travel-policy result, while equivalent authorized wording in supported languages should not create an unexplained refusal or scope failure. The record therefore separates country-policy outcomes from matched wording cases and keeps any disclosure or denial evidence visible for each slice.

### Cost, latency, and resource performance

**What this establishes.** Resource claims establish whether the candidate operates inside the declared latency, call, cost, capacity, admission, backoff, or degradation behavior for the stated environment and workload.

**What this does not establish.** A good answer score does not compensate for exceeding a safe stop or admission boundary. A single quiet run does not establish behavior under shared capacity, and missing telemetry does not establish zero cost or no effect.

**When it matters and what to observe.** Assess this family when the contract or risk record includes a resource, availability, capacity, or truthful-degradation claim. Observe the applicable resource use, limit decision, user-facing degradation, and final result. Shared queues, caches, concurrency limits, or downstream capacity add their own applicable profile; their presence does not turn an ordinary task-quality evaluator into a resource evaluator.

**Small example.** On `POLICY-EXHAUSTION-008`, the assistant reaches its declared retrieval boundary, produces the contract-defined failure or bounded response, and records that no new spend-producing work was admitted after the stop. The case assesses honest degradation and stopping, not a claim that all later billing is known.

## Apply dimensions to the actual execution context

Conversation, memory, durable work, and composition are contexts that add claim-specific evidence; they are not peer dimensions that every agent needs.

- **Conversation or transformed context:** assess the whole bounded episode, including relevant milestones, forbidden events, terminal result, and material-constraint provenance. Test ordering sensitivity only where order is meant to be irrelevant; a later correction, priority rule, or consent statement may be material.
- **Stored memory or cache:** when such state exists and affects behavior, assess applicable identity or tenant scope, expiry or deletion claims, poisoning resistance, provenance through transformations, and absent, corrupt, or over-limit behavior. A conversation alone does not establish persistent memory.
- **Long-running, resumable, approval-waiting, or consequential work:** assess the applicable stop, recovery, approval, reconciliation, and authoritative-state claims through the detailed controls in Part 7. Durable read-only work does not thereby imply a write or approval test.
- **Multi-agent composition or remote interaction:** assess critical handoff, delegated scope, identity and source propagation, denial propagation, malicious-peer handling, loop limits, and end-to-end outcome when those capabilities exist. Routing does not imply a model judge, and composition does not create authority.

## Requirements

- **BEHAVIOR-01 — Outcome and constrained trajectory.** **Applicability:** all production candidates and every behavior-affecting change; trajectory clauses apply where a claim depends on an observable path, tool, boundary, provenance, retry, or stop condition. The evaluation **MUST** specify each behavior claim’s acceptable terminal outcome and relevant observable invariants. Where trajectory matters, it **MUST** separately state required or forbidden events, material partial-order constraints, permitted safe alternatives, permitted tools or capabilities and material argument constraints, provenance, and retry or stopping conditions as applicable, together with the observation that establishes each. Outcome and path results **MUST** be reported separately. Exact trace or sequence matching **MUST NOT** be the default where invariant-compliant alternatives are safe; an exact sequence gate **MUST** have a documented contract or protocol rationale. The evidence **MUST NOT** require hidden reasoning. **Observable evidence:** identified case and fixture; expected outcome and allowed variation; claim-sufficient event, source, boundary, or state observations; and separate outcome and invariant judgments.

- **BEHAVIOR-02 — Adverse behavior, relation pairs, and uncertainty.** **Applicability:** when the applicable coverage profile identifies an adverse condition; and, before exposure, when the agent accepts semantic natural-language or conversational input, uses retrieved or otherwise changeable evidence, or makes a policy, permission, currentness, or user-constraint decision. The suite **MUST** exercise the applicable missing, stale, conflicting, malformed, denied, untrusted or injected, dependency-failure, exhaustion, and uncertainty conditions and **MUST** assert both the contract-defined user-visible outcome and applicable exposure, action, provenance, or stop invariant. It **MUST** pair appropriate uncertainty or refusal cases with comparable answerable or permitted cases and **MUST** assess over-refusal separately. For the stated semantic or changeable-evidence triggers, it **MUST** include a justified applicable invariance relation and a relevant-change sensitivity relation before exposure; each relation **MUST** identify the input change, why it is irrelevant or relevant, the allowed output relation, and the expected trajectory or control relation. A fully structured no-equivalence or no-variation interface **MAY** record non-applicability with its trigger rationale. For materially stochastic user-visible claims, the suite **MUST** provide documented fresh repeated-episode evidence or a documented claim-specific alternative that actually removes variability for that claim; it **MUST NOT** treat a selected favorable transcript as repeat evidence. **Observable evidence:** versioned base and derived cases; transformation rationale and provenance; terminal and path observations for both relation members; reset and run-context observations where repeated episodes apply; and the disposition of every condition.

- **BEHAVIOR-03 — Critical controls and four-way boundary evidence.** **Applicability:** when an agent can propose or invoke restricted operations, access protected data, disclose restricted material, cross a tenant or authorization boundary, use a consequential capability, or rely on an enforced stop or limit. The suite **MUST** exercise each applicable critical control at its enforcement boundary and **MUST** retain authoritative evidence of the applicable access decision, invocation, state, recipient, or stop event. It **MUST** separately record, as applicable, model proposal or compliance, trusted-boundary authorization or denial, actual external execution, and disclosure. A blocked proposal **MUST NOT** be represented as completed external execution, and a blocked effect **MUST NOT** be represented as proof that no disclosure occurred. A model explanation, citation-presence check, or unverified transcript **MUST NOT** be the sole evidence for a critical control. The suite **MUST** include a comparable allowed counterpart when needed to demonstrate that a control did not succeed through blanket refusal. **Observable evidence:** protected-boundary decision record; permitted selection and security-relevant argument observation; authoritative state or invocation record when applicable; output and recipient-scope observation for disclosure; and paired allowed-case result.

- **BEHAVIOR-04 — Harm screen and affected slices.** **Applicability:** all production candidates before release and after a material change to intended users, data, capability, domain, or use; slice evaluation applies when the harm screen or an applicable domain policy identifies material differentiated harm. The accountable owner **MUST** record whether the harm model creates a reason for population or domain slice testing. When it does, the suite **MUST** define risk-relevant slices, evaluate affected task and control claims separately, and preserve legitimate entitlement or policy distinctions in the case design. It **MUST NOT** treat a favorable aggregate as evidence that a critical slice is acceptable. **Observable evidence:** dated harm-screen record; slice and comparator rationale; relevant task, uncertainty, refusal, and control observations by slice; qualified domain-review evidence where the applicable assurance owner requires it; and stated limitations of any curated slice.

- **BEHAVIOR-05 — Claim-sufficient provenance and evidence status.** **Applicability:** any behavioral, safety, robustness, consistency, or slice result offered as evidence. Each result **MUST** identify the claim, case, fixture, expected terminal outcome or invariant, observed outcome, claim-sufficient trajectory or boundary evidence, source or state provenance where material, evaluator, and evidence status. It **MUST** preserve `pass`, `fail`, `invalid`, or `inconclusive` status as applicable, and an invalid or inconclusive run **MUST NOT** be reported as a passing agent case. An independently observable candidate failure **MUST NOT** be relabelled invalid merely because a fixture, harness, or evaluator condition also needs repair. Records **MUST** contain only the events and material needed to establish the claim; they **MUST NOT** require raw hidden reasoning. **Observable evidence:** identified candidate and configuration; case and fixture revisions; evaluator identity; retained status and reason; linked event, source, permission, state, or recipient observations; and documented evidence limits.

## Worked example: a bounded policy answer and its dimensions

The fictional candidate is `policy-assistant@candidate-current-selection`. It is ephemeral and read-only: it answers from approved current permission-filtered sources with citations, has no persisted memory, no approval step, no delegated agents, and no write capability. The controlled world is fixture `travel-policy-current`, revision `fixture-2026-10-18.1`. Its current policy document is `travel-policy-2026`, revision string `"2026-10-01"`; the fictional London hotel value is **GBP 220**. `travel-policy-2024-superseded`, revision string `"2024-01-01"`, is a superseded document, not equal authority.

For `POLICY-CURRENT-001`, an authorized requester asks for the London hotel value. The task-outcome claim accepts `complete` with GBP 220, a citation to the current permitted document, and wording that is understandable to the requester. The source-admission claim checks the requester scope and current-document status. The grounding claim checks that the material amount assertion is supported by the cited policy text. A separate truth claim is unnecessary in this fictional controlled world unless the contract adds an external-world truth promise.

The trajectory claim permits safe alternatives. One episode may check requester scope and then read `travel-policy-2026`; another may resolve an already admitted current record after the same scope check. Both paths satisfy the claim if protected content is not returned before the scope decision, every used source is permitted and current, no write capability is invoked, and the episode terminates within its declared boundary. The evaluator records selection, relevant source and requester arguments, scope decision, source revision, final citation, terminal outcome, and any stop event. It does not ask for a private reasoning trace or require the same incidental read sequence.

`POLICY-PARAPHRASE-007` is a reviewed meaning-preserving rewrite of the same authorized question. Its invariance relation preserves the GBP 220 result, permitted current-source class, and trajectory constraints even when the prose differs. Its paired sensitivity checks are meaningful changes, not random variants: `POLICY-DENIED-005` removes the requester’s permission to the answer-bearing source, and `POLICY-CONFLICT-004` presents two current approved policies with conflicting values. The first expects the contract-defined bounded result and a denied access decision; the second expects `needs_information` rather than an invented definitive amount. `POLICY-STALE-002` checks that a superseded conflict is recognized as superseded rather than treated as equal authority.

These cases also illustrate the four-way boundary distinction. Suppose the model proposes a retrieval that is outside the requester’s scope in `POLICY-DENIED-005`. The proposal can be recorded as a compliance failure if the product contract treats it that way. The trusted source boundary’s denial is enforcement success. No authorized retrieval record establishes that the restricted document was not returned through that boundary. A separately inspected terminal output and recipient scope establishes whether disclosure occurred. The evaluator therefore never calls the blocked proposal a completed external action or infers non-disclosure solely from the denial.

`POLICY-MISSING-003` withholds permitted supporting evidence, while `POLICY-EXHAUSTION-008` makes the retrieval dependency unavailable after the declared stop condition. Each expects a defined uncertainty, failure, or bounded partial outcome rather than a fabricated amount, citation, or zero-cost claim. `POLICY-INJECTION-006` places a harmless embedded instruction in an untrusted retrieved channel. The evidence checks that the content is not treated as policy, that no out-of-scope content reaches the requester, and that the read-only configuration shows no prohibited invocation. These are expected fictional outcomes, not results of a live benchmark.

Fresh episodes of `POLICY-CURRENT-001` test fixed-world reliability only when each starts from the named fixture and permission context and meets both the GBP 220 task predicate and applicable trajectory invariants. The record preserves each outcome and status instead of displaying a chosen success. It contains no universal repeat count or claimed field rate. Any eventual numerical summary, retry policy, or comparison with `policy-assistant@baseline-current-selection` is handled under [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md).

Finally, the owner records a harm screen. If country-specific policy rules or supported-language access could create differentiated harm, the suite adds justified country-rule and matched same-entitlement wording cases. It reports useful completion, `needs_information`, decline, failure, and any scope-control failure separately. The screen does not imply a universal fairness metric, nor does this small fixture establish a population statistic.

## Evidence and checklist

Use [4.6](06-standards-required-coverage-and-execution-cadence.md) to select applicable profiles and [4.5](05-planning-designing-and-running-tests-and-evaluations.md) to preserve case, fixture, and execution records. The following review questions keep the dimensions distinct:

- [ ] Does each material claim name the user-visible outcome, evidence scope, and limit instead of using a generic quality label?
- [ ] Are task success, source admission/currentness, grounding, factual correctness, and uncertainty recorded as distinct claims where each matters?
- [ ] Do trajectory cases use material invariants, partial ordering, allowed alternatives, permitted capability and argument constraints, provenance, and stopping conditions rather than a brittle reference trace?
- [ ] Does critical-control evidence distinguish proposal, boundary decision, execution, and disclosure, with an allowed counterpart where blanket refusal could mask failure?
- [ ] Do adverse cases cover the conditions plausibly introduced by enabled capabilities and risk, including safe uncertainty and recovery behavior?
- [ ] Where semantic or changeable-evidence triggers apply, is there a justified invariance relation and a relevant-change sensitivity relation with paired outcome and control evidence?
- [ ] Where material stochastic behavior remains, do fresh episodes retain each run’s outcome, control observations, reset context, and status without claiming a universal count or field-rate inference?
- [ ] Is the harm screen recorded, and do any triggered slices separate task outcomes from control failures while preserving legitimate policy differences?
- [ ] Do resource claims observe the relevant limit, degradation, and final result rather than treating a good answer as compensation for unsafe exhaustion?
- [ ] Does every evidence item link to the candidate, case, fixture, evaluator, material event or provenance, and an honest pass, fail, invalid, or inconclusive status?

## References

[1]: https://arxiv.org/html/2408.04682v1 "ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities"
[2]: https://valerio-terragni.github.io/assets/pdf/cho-icsme-2025.pdf "Metamorphic Testing of Large Language Models for NLP Tasks"
[3]: https://arxiv.org/html/2405.07437v2 "Evaluation of Retrieval-Augmented Generation: A Survey"
[4]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[5]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"

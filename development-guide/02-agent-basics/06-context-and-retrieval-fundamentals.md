# 2.6 Context and Retrieval Fundamentals

**Status:** 0.5.0-draft.2 — refined draft; proposed, not adopted

**Audience:** Builders and reviewers who design what an agent receives as evidence for a bounded task

**Applicability:** Every agent needs an intelligible account of the information presented to its model. Apply the retrieval guidance when external documents, records, or indexes supply run-time context. Apply the memory guidance only when information is intentionally persisted across tasks. Retrieval, memory, caching, and context optimization are not universal components.

**Reader question:** How can a builder assemble just enough permitted, traceable evidence for a task, recognize when it is insufficient, and leave a reviewer able to inspect what the proposed design would rely on?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) · [Part 8 — Model Context and Resource Engineering](../../engineering-reference/08-model-context-and-resource-engineering/README.md)

## Purpose and applicability

**Context** is the bounded material supplied to a model for one decision or response. It can include task instructions, the current request, trusted run-time facts, selected conversation turns, and evidence returned from an approved source. **Context engineering** is the deliberate work of choosing, ordering, limiting, and labelling that material so the model receives the information that is useful for this task and not information it does not need.

**Retrieval** is one conditional context-building path. It obtains candidate material from a larger external or indexed collection, then selects a bounded set of passages or records for the task. Retrieval-augmented generation, often shortened to **RAG**, combines retrieval with a generated answer. It is not a claim that retrieved material is true, current, permitted, or correctly used. A source can be authoritative yet superseded, current yet unavailable to this requester, or accessible yet outside the task’s purpose.

**Memory** is different. It intentionally preserves information from one task for possible use in a later task. Retrieval may read a memory store, and a retrieved document may be temporarily retained for a run, but neither fact makes retrieval durable memory. A proposed policy assistant can work without persistent memory when its bounded question can be answered from the current request, trusted run-time context, and approved sources.

This chapter explains the decisions that make context and retrieval reviewable. It does not select an embedding method, chunk size, ranking algorithm, model window, cache implementation, or memory architecture. Those performance and optimization choices belong in [Part 8](../../engineering-reference/08-model-context-and-resource-engineering/README.md). Identity and permission checks remain owned by [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md); treatment of untrusted retrieved content remains owned by [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md); data lifecycle and audit handling remain owned by [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

## Working model

A useful context record separates why material is present from what the material says. Instructions describe the task behavior. The request states what the requester wants. Trusted run-time context supplies facts such as the authenticated requester, tenant, and permission decision. Retrieved text is domain evidence. A tool result, summary, cache entry, or conversation turn is still data to assess. None of these roles upgrades the others: a retrieved instruction is not operating policy, a source label is not authorization, and a source schema is not proof that a claim is true.

A proposed retrieval path can be understood as the following bounded sequence:

```text
declared task and admitted source purpose
  → trusted requester and permitted source scope
  → candidate retrieval with source metadata
  → relevance, authority, currentness, and conflict assessment
  → selected excerpts or labelled transformations within a context budget
  → supported answer, bounded uncertainty, or declared terminal outcome
  → source/selection record for review
```

The arrows show dependencies, not a promise that a source will be found or that the answer will be correct. A fixed workflow can make each transition explicit, including a branch for a missing source or unresolved conflict. A bounded adaptive alternative may choose among a finite set of admitted next steps, such as requesting clarification, locating permitted evidence, returning a bounded response, or escalating. In either design, the model does not decide what it is authorized to read or whether a source becomes authoritative.

### Five properties that must not be collapsed

A source’s **provenance** identifies where a piece of supplied material came from and how it reached its current form. A document identity, revision, passage locator, retrieval time, and the identity of a transformation can make a later review possible. NIST’s Generative AI Profile suggests establishing practices to determine data origin and content lineage for documentation and evaluation; it presents this as context-dependent guidance, not as a universal index schema. [1]

**Domain authority** answers whether a source is entitled to establish the kind of fact at issue. **Currentness** answers whether its version, effective status, or other defined freshness signal applies now. **Requester accessibility** answers whether this requester may receive it through the protected boundary. **Semantic support** answers whether the material actually supports the statement in the response. These are separate questions. A current source does not automatically support every interpretation, and an approved historical document can remain useful as evidence of a superseded rule without being authoritative for a current answer.

**Lineage** is especially important when context is transformed. The W3C PROV data model describes derivation as a transformation, update, or construction of one entity from another and allows an activity to make that path explicit. [2] In a context design, a chunk, excerpt, summary, translation, normalized record, or cache entry can therefore carry the source identity and revision it derives from, plus a plain description or identity of the transformation. This does not make the transformation lossless or correct. It gives the reviewer a route to inspect the original and ask whether the transformed form preserved the qualification that matters.

**Relevance** is task-specific usefulness, not a keyword match. A passage can mention London yet fail to say which worker group, date, spending category, or condition applies. The search stage may retrieve broad candidates; ranking orders them; reranking is an optional later comparison intended to prioritize the better candidates; and excerpt selection places a bounded passage in model context. These are different decisions and can fail differently. A concise excerpt can remove a condition from its surrounding text, while a full document can conceal the answer among irrelevant detail.

**Permission** is evaluated before protected content is exposed to the model, not after a polished answer is formed. Trusted identity and the protected retrieval boundary decide which source records are eligible. A model-generated source name, tenant, or query may be a request parameter, but it is not the permission decision. This is important for read-only candidates: filtering the final answer cannot undo a disclosure that already occurred in model context. See [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) for the canonical authorization controls.

### A bounded context is a design choice

A **context budget** is the amount of model-visible material the proposed task is prepared to supply at a decision point. It is not a universal token number. The budget has to leave room for instructions, the request, the selected evidence, a response, and the task’s uncertainty path. It also establishes a reason to prefer a smaller, traceable excerpt over an indiscriminate dump of search results.

More input is not automatically better. In experiments on multi-document question answering and key-value retrieval, Liu and colleagues found that performance for the models they evaluated varied with the position of relevant information and often fell when it appeared in the middle of long context. [4] That result is a reason to test a proposed context selection under its own task conditions, not a universal rule about source order or context length. It does not establish that a particular chunking, ranking, or reranking method is best.

A practical budget decision asks which evidence is necessary to establish the answer, which qualifiers need to travel with it, and what can safely remain outside model context. A record can preserve why an item was selected, excluded, truncated, or transformed. It should not hide an excluded conflict or a removed condition merely because the retained answer sounds convenient. Detailed measurement and tuning are Part 8 work.

## Decisions and best practices

### Decide whether retrieval is needed and what it may establish

Start with the bounded user task. If a response can be produced from the request, fixed instructions, and trusted run-time facts, retrieval adds a dependency without automatically adding value. If the task needs external facts, name the admitted source collection and the claim each source type may establish. This turns an undefined search over “what is available” into a reviewable evidence boundary.

For each source, distinguish admission from authority. Admission says that the collection is eligible for the task. Authority says what fact it can establish. Currentness says how the design recognizes the applicable revision or effective state. Accessibility says which requester and tenant may see it. The context-source record linked below expresses these as separate fields so an approved source is not casually represented as current or accessible.

A source may need a domain-specific precedence rule. For example, a policy source might declare a status, effective date, revision, owner publication decision, or an explicit supersession relationship. A date alone is not a safe universal tie-breaker. When equally authoritative current sources conflict and the declared rule does not resolve the relevant scope, the useful response is to surface that uncertainty rather than select the most recent-looking document.

### Design retrieval as evidence selection, not as a document dump

Choose a source unit that can retain its connection to the original. A large document can be divided into smaller **chunks** to make selection and review practical, but a chunk boundary can separate a rule from an exception, a definition, or an applicability condition. A source record can therefore retain a stable source identity, revision or effective state, a passage locator, and enough nearby context to explain why the excerpt applies. It can also say whether the selection is a direct excerpt or a derived form.

Search, ranking, and reranking are optional ways to narrow candidates; none is a truth test. A search miss can result from terminology, indexing, permissions, an unavailable dependency, or a query that did not express the user’s actual condition. An apparent high-ranking match can be stale, off-scope, or semantically weak. Builders can make the failure policy visible by distinguishing no permitted match, denied access, unavailable retrieval, and conflicting eligible evidence rather than collapsing them into “no answer.”

A **summary** is a new derived artifact, not a shortcut to source authority. It may improve comprehension or fit a bounded context, but it can omit an exception or blur which revision supplied a claim. Before a transformed artifact is offered as answer evidence, the record can identify its inputs, source revisions, transformation purpose, and the way a reviewer can reach the underlying passages. The source identities alone do not establish that the summary preserved meaning. When the material is untrusted, labels and delimiters may help interpretation but do not turn it into instructions or enforcement; apply [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

### Carry provenance without confusing it for support

A citation is a pointer for review. It is useful when it identifies the particular source and passage supplied to the model or used in a deterministic answer path. It is not evidence merely because it is present. A citation can refer to a correct document while the answer overstates it, cite a superseded revision, or omit the condition that changes the outcome.

The RAGAS paper separates context relevance, answer relevance, and faithfulness to supplied context. [3] This is a helpful diagnostic distinction: a review can ask whether the design found relevant, permitted evidence; whether the answer used supplied evidence faithfully; and whether the response addresses the request. The paper’s proposed automated methods are not required here, and a score or citation does not settle authority, currentness, permission, or factual truth. [Part 4 — Testing and Evaluation](../04-testing-and-evaluation/README.md) owns case design, evaluators, and interpretation of evidence.

A proportionate provenance record commonly includes source identity, revision or status, a locator, the source role, the access decision context, retrieval or transformation identity, and the time or release context that makes the selection intelligible. The exact fields and retained content depend on the task and the data-handling policy. It is usually more useful to retain safe identifiers and a bounded selection rationale than to copy unrestricted document bodies into diagnostic records.

### Plan for absence, stale evidence, conflict, and cache drift

A retrieval result should not silently stand in for the whole source universe. “No match” can mean the corpus is silent, the request needs clarification, the right source is inaccessible, the index is unavailable, or the retrieval method missed it. These cases can map to different terminal outcomes. A bounded `needs_information` response may request a condition needed to find applicable evidence or state that the current evidence is insufficient. A protected source denial may require `declined`, while a dependency failure can require `failed` under the declared agent contract. The correct outcome is case-dependent, not a way to make every uncertainty look successful.

A **cache** is another derived copy of source material or a prior selection. It can reduce repeated work, but it can also outlive a source revision, a policy change, or a requester’s permission. The cache design therefore needs to state the source and scope assumptions under which an entry is eligible for reuse, the change signal or invalidation decision that matters, and the handling of its derived data. A cache cannot turn a formerly permitted excerpt into material that may still be shown after the requester’s scope changes. The organization-specific invalidation mechanism, retention treatment, and ownership remain unresolved in this proposed local record; do not fill those gaps with an implicit universal default.

A common failure is to give a cache key a document name but omit the revision, requester scope, or permission decision that made the earlier selection valid. Another is to treat a recently refreshed index as proof that every source it contains is currently applicable. An observable review record can distinguish cache candidate, source revision, access decision, and currentness signal, then show why reuse was eligible or why a fresh selection was required. The data lifecycle for caches and derived artifacts belongs with [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

### Keep memory purpose-limited and separately reviewable

If cross-task continuity is proposed, define the **memory write scope**: what type of information may be retained, for what purpose, from which task context, and who or what process can correct or delete it. Define the **memory read scope** separately: which requester, task, tenant, and purpose may retrieve it later. A durable fact recorded in memory does not acquire authority for a new task, and a prior conversation does not make its content current.

Memory can be useful for a defined continuity need, such as preserving a requester preference that the task is permitted to retain. It can also create stale, private, or cross-scope context. A proposed candidate with no such continuity need can record memory as disabled rather than leaving an accidental persistence path. Retention, deletion, correction, access, and derived-copy questions are governed by [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), not by this chapter.

### Builder workflow for a proposed local review unit

1. **State the evidence need.** Describe the bounded question that needs external evidence and the task outcome when evidence is unavailable. Record retrieval as not applicable when the task genuinely does not need it; do not infer persistent memory from that decision.
2. **Create a source map.** For each proposed source, record its admitted purpose, domain authority, currentness/precedence signal, access boundary, data-handling concern, and source identity. Keep unresolved owner, refresh, or invalidation details visibly unresolved rather than inventing them.
3. **Describe the selection path.** Identify the candidate source unit, permissible search scope, selection or ranking decision, contextual excerpt, and exclusion rationale. Ensure the protected access decision occurs before the selected material is exposed to the model.
4. **Record transformations and context bounds.** Mark a selected item as a direct excerpt or a derived artifact. For a derived artifact, link its source revisions and transformation purpose. State the task-specific context budget rationale and what must remain visible when an item is shortened.
5. **Define bounded evidence outcomes.** Make missing, stale, denied, unavailable, and conflicting evidence distinguishable. Link each to the existing terminal outcome contract rather than creating a new result taxonomy.
6. **Prepare review evidence.** Connect the source record to the candidate’s capability manifest, fixture or case design, and data-handling record. A proposed record is a planning/build artifact, not evidence that a retrieval, cache, or memory control has operated.

## Requirements

- **CONTEXT-01** — **MUST**, when external documents, records, or indexes are retrieved for a run: use only sources approved for the task, and apply the caller's permitted scope using trusted identity and controls outside model-generated decisions. Discovery or retrieval does not itself authorize access. See 3.1 for the canonical authorization requirements.
- **CONTEXT-02** — **MUST**, when retrieved evidence can affect an answer: preserve enough source and version or freshness metadata to identify the material used and trace relevant claims back to it, consistent with data-minimization rules. If the source's current status cannot be established, do not represent it as verified current information.
- **CONTEXT-03** — **MUST**, when sources may be missing, stale, out of scope, or conflicting: define the precedence and freshness signals that apply, and provide a bounded response for unresolved evidence. The agent MUST NOT present retrieval failure as proof that no applicable information exists or resolve unresolved conflict by unsupported guesswork.
- **CONTEXT-04** — **MUST**, when retrieval is part of the task: evaluate whether relevant, permitted evidence was retrieved separately from whether the final answer is correct and supported. Citation-presence checks MUST NOT be treated as proof that cited material supports the claims.
- **CONTEXT-05** — **SHOULD**, when information persists across tasks as memory: define its purpose, scope, ownership, access boundaries, and correction and deletion handling before enabling it; apply the applicable privacy and retention requirements. Persistent memory is not required for agents whose tasks do not need continuity.

## Worked example

The shared fictional example is an **illustrative, unexecuted** policy-assistance candidate, `POLICY-BUILD-001`, for `internal-policy-assistance`. It is a proposed fixed retrieval-and-answer workflow, not an approved or deployed system. It has no external write capability. Its existing terminal outcomes are `complete`, `needs_information`, `declined`, and `failed`; the scenarios below are expected behavior for review, not observations from a run.

The source map admits `travel-policy-2026@2026-10-01` as the current policy source and retains `travel-policy-2024-superseded@2024-01-01` as an approved historical record. The permitted requester is `employee-uk-104`; `contractor-uk-204` is not permitted to read the policy. The context-source record identifies the sources, revisions, status, access scope, and intended source role. It does not claim that the record itself made either source authoritative or accessible.

For the London question, trusted requester context is used to filter the source set before content is assembled for the model. The proposed selection contains a direct, bounded excerpt from the current permitted source: “London hotel limit: GBP 220.” It preserves the source revision and a passage locator. The superseded GBP 200 passage may be present for a stale-evidence test, but it is not represented as the current authority. The expected `complete` answer states GBP 220 and points to the current policy evidence. The citation is a review pointer, not proof that the answer is semantically supported.

Now consider the missing-evidence variant. If the current permitted source is absent, the candidate does not infer that there is no London policy. The expected outcome is `needs_information` with a bounded statement that it cannot verify the current limit. If the retrieval dependency reaches the declared bounded failure condition, the expected outcome is `failed`; it does not invent an amount or citation. The distinction helps a reviewer separate source silence or ambiguity from a dependency problem.

In the conflict variant, `travel-policy-2026-conflicting-amendment@2026-10-12` is also current, approved for that variant, permitted to the employee, and equally authoritative. Its GBP 260 statement conflicts with the GBP 220 source. A later revision date is not an automatic precedence rule. Because the declared map does not resolve the conflict, the expected outcome is `needs_information`, identifies the conflict, and avoids a definitive amount.

For `contractor-uk-204`, the protected retrieval boundary denies source access before policy content enters context. The expected terminal outcome is `declined`, with no restricted amount or policy text. In the indirect-injection variant, an untrusted travel note attempts to redirect behavior. The note remains untrusted data and cannot add a capability or authority. The expected result still preserves the permitted utility of the question—GBP 220 from the current permitted policy—without a write attempt or a blanket refusal caused solely by hostile text.

The example’s source record marks memory as disabled because cross-task continuity is not part of the described policy question. It also marks persistent caching as not enabled in this illustrative candidate. If either is proposed later, the record requires a fresh design decision about source revision, requester scope, permission changes, correction, deletion, and derived-data handling; it does not treat the earlier selection as a reusable answer for a different requester or a later policy state.

## Evidence and checklist

### The local review artifact

The accompanying [context-source record](../../templates/2.6/context-source-record.yaml) is a neutral planning/build template for this chapter’s shared example. It makes the admitted sources, source status, expected permission boundary, selection lineage, bounded outcomes, cache questions, and memory decision inspectable. Its `illustrative-unexecuted` status means that its fields are intended design and expected behavior, not a record of a live source lookup, an authorization decision, a model response, or a control result.

The source record complements rather than replaces the [agent contract](02-agent-contracts-and-configuration.md). The contract declares the candidate’s trusted dependencies, capability bounds, terminal outcomes, and effective configuration identity. The context record describes how a proposed permitted evidence path would be assembled. The data-handling record in [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) decides whether and how source bodies, excerpts, cache entries, prompts, and diagnostic material may be retained. No artifact by itself proves the other controls operate.

### What a reviewer can inspect

For a retrieval-capable proposed candidate, useful completion evidence links the following observable design artifacts without retaining more content than the data policy allows:

- a source map showing source identity, revision or currentness signal, authority role, allowed task purpose, and unresolved precedence questions;
- the trusted identity and permission path that filters protected material before model exposure;
- a selection record for a representative case showing selected and excluded source identities, passage locators, direct-excerpt or transformation status, and the bounded context rationale;
- an explicit expected response for missing, stale, inaccessible, conflicting, and unavailable evidence, connected to existing terminal outcomes;
- a cache and memory decision that identifies whether either component is absent or, if proposed, the source/scope/change assumptions it needs; and
- Part 4 case and evaluator records that assess evidence retrieval, semantic support, and answer behavior as related but distinct claims.

These artifacts make the proposal reviewable. They do not demonstrate that the retrieval boundary is active, that a source is factually correct, that a summary preserved every qualification, or that an answer is safe in every context. A later evaluation can compare expected and observed behavior using a fit-for-purpose case, fixture, and evaluator; follow [Part 4](../04-testing-and-evaluation/README.md) for that work.

### Handoff and open decision

The source map needs a source-status and permission-change signal before a cache or transformed artifact can be treated as reusable. The responsible owner, invalidation mechanism, cache retention treatment, and adoption decision are `null` or unresolved in the illustrative record. This is an integration handoff, not a new default policy. A reviewer should resolve it with the accountable source, authorization, and data-handling owners before treating a persistent retrieval optimization as part of a production candidate.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1 Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"
[2]: https://www.w3.org/TR/prov-dm/ "W3C PROV-DM The PROV Data Model"
[3]: https://arxiv.org/html/2309.15217v1 "RAGAS Automated Evaluation of Retrieval Augmented Generation"
[4]: https://aclanthology.org/2024.tacl-1.9/ "Lost in the Middle How Language Models Use Long Contexts"

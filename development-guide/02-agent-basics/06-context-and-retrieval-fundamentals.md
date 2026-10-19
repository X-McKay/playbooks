# 2.6 Context and Retrieval Fundamentals

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders and reviewers who design what an agent receives as evidence for a bounded task

**Applicability:** Every agent needs a clear account of the information presented to its model. Apply the retrieval guidance when external documents, records, or indexes supply run-time context. Apply the memory guidance only when information is deliberately kept across tasks. Retrieval, memory, caching, and context optimization are not universal components.

**Reader question:** How do you assemble just enough permitted, traceable evidence for a task, recognize when it is insufficient, and leave a reviewer able to inspect what the design relies on?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) · [Part 8 — Model Context and Resource Engineering](../../engineering-reference/08-model-context-and-resource-engineering/README.md)

## Purpose and applicability

**Context** is the bounded material supplied to a model for one decision or response: task instructions, the current request, trusted run-time facts, selected conversation turns, and evidence from an approved source. **Context engineering** is the work of choosing, ordering, limiting, and labelling that material so the model gets what is useful for this task and nothing it does not need.

**Retrieval** is one conditional way to build context. It obtains candidates from a larger external or indexed collection, then selects a bounded set of passages or records. Retrieval-augmented generation (**RAG**) combines retrieval with a generated answer. [5] Retrieved material is not thereby true, current, permitted, or correctly used. A source can be authoritative yet superseded, current yet unavailable to this requester, or accessible yet outside the task's purpose.

**Memory** deliberately keeps information from one task for a later one. Retrieval may read a memory store, and a retrieved document may be held for one run, but neither makes retrieval durable memory. A policy assistant can work without memory when the request, trusted run-time context, and approved sources answer the question.

This chapter does not pick an embedding method, chunk size, ranking algorithm, model window, cache implementation, or memory architecture; those belong to [Part 8](../../engineering-reference/08-model-context-and-resource-engineering/README.md). Identity and permission checks stay with [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), untrusted retrieved content with [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md), and data lifecycle and audit with [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

## Working model

Separate why material is present from what it says. Instructions describe task behavior. The request states what the requester wants. Trusted run-time context supplies facts such as the authenticated requester, tenant, and permission decision. Retrieved text is domain evidence. Tool results, summaries, cache entries, and conversation turns are data to assess. No role upgrades another: a retrieved instruction is not policy, a source label is not authorization, and a schema does not prove a claim.

A retrieval path can be read as this bounded sequence:

```text
declared task and admitted source purpose
  → trusted requester and permitted source scope
  → candidate retrieval with source metadata
  → relevance, authority, currentness, and conflict assessment
  → selected excerpts or labelled transformations within a context budget
  → supported answer, bounded uncertainty, or declared terminal outcome
  → source/selection record for review
```

A fixed workflow can make each step explicit, including a branch for a missing source or unresolved conflict. A bounded adaptive alternative may choose among a finite set of admitted steps (clarify, locate permitted evidence, respond, escalate). In both, the model does not decide what it may read or whether a source becomes authoritative.

### Five properties that must not be collapsed

**Provenance** identifies where supplied material came from and how it reached its current form: document identity, revision, passage locator, retrieval time, and transformation identity. NIST's Generative AI Profile suggests practices to determine data origin and content lineage for documentation and evaluation, as context-dependent guidance. [1]

**Domain authority** asks whether a source may establish this kind of fact. **Currentness** asks whether its version or effective status applies now. **Requester accessibility** asks whether this requester may receive it through the protected boundary. **Semantic support** asks whether the material supports the statement in the response. A current source does not support every interpretation, and an approved historical document can show a superseded rule without being authoritative now.

**Lineage** matters most when context is transformed. The W3C PROV data model describes derivation as transforming, updating, or constructing one entity from another, with an activity that makes the path explicit. [2] A chunk, excerpt, summary, translation, normalized record, or cache entry can carry the source identity and revision it derives from, plus the transformation. That does not make it lossless; it gives the reviewer a route back to the original.

**Relevance** is task-specific usefulness, not a keyword match: a passage can mention London yet not say which worker group, date, or condition applies. Search retrieves candidates, ranking orders them, optional reranking compares the better ones, and excerpt selection puts a bounded passage in context. These fail differently: a short excerpt can drop a condition, and a full document can bury the answer.

**Permission** is checked before protected content reaches the model, not after an answer is formed. Trusted identity and the protected retrieval boundary decide which records are eligible; a model-generated source name, tenant, or query is a request parameter, not the decision. Filtering the final answer cannot undo a disclosure already made in model context. See [3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md). Where records live in a vector index, keep the index permission-aware or partitioned by tenant, since similarity search across mixed data can leak between tenants. [8]

### A bounded context is a design choice

A **context budget** is the amount of model-visible material the task will supply at a decision point. It is not a universal token count. It must leave room for instructions, the request, the evidence, a response, and the uncertainty path, and it favors a small, traceable excerpt over a dump of search results.

Treat context as a finite resource. More input is not better: as context grows, the model's ability to recall any one item tends to fall, sometimes called context rot. Liu and colleagues found, on multi-document question answering and key-value retrieval, that the models they tested did best when relevant information was at the start or end of the input and often worse in the middle. [4] That is a reason to test your context selection under your own task conditions, not a rule about source order, and it does not show that any chunking, ranking, or reranking method is best. The aim, as one engineering guide puts it, is the smallest set of high-signal material that gets the outcome. [6]

Ask which evidence the answer needs, which qualifiers must travel with it, and what can stay outside context. Record why an item was selected, excluded, truncated, or transformed, and do not hide an excluded conflict or removed condition. Measurement and tuning are Part 8 work.

For long-running tasks, three practices help keep the budget under control. [6]

- **Just-in-time loading.** Keep lightweight references (identifiers, locators, saved queries) in context and load the full content only when a step needs it.
- **Compaction.** When history outgrows the budget, summarize it and continue with the summary. Tune for recall first so that constraints, open decisions, and unresolved conflicts survive, and clear stale raw tool results that are no longer needed.
- **Notes outside the window.** Persist working notes to storage the agent can read back, and treat them as memory (below) if they cross tasks.

A summary is a derived artifact, covered below.

## Decisions and best practices

### Decide whether retrieval is needed and what it may establish

If the request, fixed instructions, and trusted run-time facts suffice, retrieval adds a dependency without adding value. If the task needs external facts, name the admitted source collection and the claim each source type may establish, so an open-ended search becomes a reviewable evidence boundary.

For each source, separate admission (the collection is eligible), authority (what fact it can establish), currentness (how the applicable revision is recognized), and accessibility (who may see it). The [context-source record](../../templates/2.6/context-source-record.yaml) keeps these as separate fields.

A source may need a precedence rule, such as status, effective date, revision, owner decision, or an explicit supersession link. A date alone is not a safe tie-breaker. When equally authoritative current sources conflict and the rule does not resolve the scope, surface the uncertainty rather than pick the most recent-looking document.

### Design retrieval as evidence selection, not a document dump

Choose a source unit that keeps its link to the original. A large document can be split into **chunks** to make selection practical, but a boundary can separate a rule from its exception, definition, or condition. Retain a stable source identity, revision or effective state, a passage locator, and enough surrounding context to show why the excerpt applies, and say whether the selection is a direct excerpt or a derived form. One well-established fix for lost chunk context is to prepend a short, chunk-specific explanation of where the chunk sits in its document before indexing, and to combine meaning-based (embedding) search with keyword search (such as BM25) and then rerank; the published results show fewer failed retrievals than embeddings alone. [7] Test it on your own data.

Search, ranking, and reranking narrow candidates; none is a truth test. A miss can come from terminology, indexing, permissions, an unavailable dependency, or a query that missed the user's condition, and a top match can be stale, off-scope, or weak. Keep no permitted match, denied access, unavailable retrieval, and conflicting eligible evidence distinct rather than folding them into "no answer."

A **summary** is a new derived artifact, not a shortcut to source authority. It can drop an exception or blur which revision supplied a claim. Before offering one as evidence, identify its inputs, source revisions, purpose, and how a reviewer reaches the underlying passages. For untrusted material, labels and delimiters may help interpretation but are not enforcement; apply [3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md).

### Carry provenance without confusing it for support

A citation is a pointer for review, not evidence by being present: it can name the right document while the answer overstates it, cite a superseded revision, or omit the condition that changes the outcome.

The RAGAS paper (peer-reviewed at EACL 2024) separates context relevance, answer relevance, and faithfulness to the supplied context. [3] The distinction is a good diagnostic: did the design find relevant, permitted evidence, did the answer use it faithfully, and does the response address the request? You do not need the paper's automated methods, and no score settles authority, currentness, permission, or truth. [Part 4 — Testing and Evaluation](../04-testing-and-evaluation/README.md) owns case design, evaluators, and interpretation.

A proportionate provenance record usually has source identity, revision or status, a locator, the source role, the access decision context, the retrieval or transformation identity, and the time or release context. Prefer safe identifiers and a short rationale to copies of unrestricted document bodies.

### Plan for absence, stale evidence, conflict, and cache drift

"No match" can mean the corpus is silent, the request needs clarification, the right source is inaccessible, the index is down, or retrieval missed it. These map to different terminal outcomes: `needs_information` (ask for a missing condition, or say current evidence is insufficient), `declined` (protected-source denial), or `failed` (dependency failure), under the agent contract. Do not make every uncertainty look like success.

A **cache** is a derived copy of source material or a prior selection. It can outlive a source revision, a policy change, or a requester's permission. State the source and scope assumptions under which an entry may be reused, the invalidation rule, and how derived data is handled. A cache cannot make a formerly permitted excerpt displayable after the requester's scope changes. Leave invalidation, retention, and ownership as explicit open decisions rather than silent defaults.

Common failures: a cache key that names a document but omits the revision, requester scope, or permission decision that made the selection valid, and treating a recently refreshed index as proof that everything in it is current. A review record should separate cache candidate, source revision, access decision, and currentness signal, and show why reuse was allowed. Data lifecycle for caches and derived artifacts belongs to [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

### Keep memory purpose-limited and separately reviewable

If cross-task continuity is proposed, define the **memory write scope** (what may be kept, for what purpose, from which task context, and who or what can correct or delete it) and, separately, the **memory read scope** (which requester, task, tenant, and purpose may retrieve it later). A fact in memory gains no authority in a new task, and a prior conversation does not make its content current.

Memory suits a defined continuity need, such as a requester preference the task may keep. It can also hold stale, private, or cross-scope context, or content poisoned by an earlier untrusted input. A candidate with no such need should record memory as disabled. Retention, deletion, correction, access, and derived copies are governed by [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

### Builder workflow

1. **State the evidence need.** Describe the question that needs external evidence and the outcome when it is unavailable. Record retrieval as not applicable if the task does not need it.
2. **Create a source map.** For each source: purpose, authority, currentness or precedence signal, access boundary, data-handling concern, identity. Leave unresolved owner, refresh, or invalidation details visibly unresolved.
3. **Describe the selection path.** Source unit, search scope, selection or ranking step, excerpt context, exclusion rationale. The protected access decision comes before material reaches the model.
4. **Record transformations and bounds.** Mark each item a direct excerpt or derived artifact (linking source revisions and purpose). State the budget rationale and what must stay visible if an item is shortened.
5. **Define evidence outcomes.** Keep missing, stale, denied, unavailable, and conflicting evidence distinct, each tied to the existing terminal outcomes.
6. **Prepare review evidence.** Connect the source record to the capability manifest, case design, and data-handling record.

## Requirements

- **CONTEXT-01** — **MUST**, when external documents, records, or indexes are retrieved for a run: use only sources approved for the task, and apply the caller's permitted scope using trusted identity and controls outside model-generated decisions. Discovery or retrieval does not itself authorize access. See 3.1 for the canonical authorization requirements.
- **CONTEXT-02** — **MUST**, when retrieved evidence can affect an answer: preserve enough source and version or freshness metadata to identify the material used and trace relevant claims back to it, consistent with data-minimization rules. If the source's current status cannot be established, do not represent it as verified current information.
- **CONTEXT-03** — **MUST**, when sources may be missing, stale, out of scope, or conflicting: define the precedence and freshness signals that apply, and provide a bounded response for unresolved evidence. The agent MUST NOT present retrieval failure as proof that no applicable information exists or resolve unresolved conflict by unsupported guesswork.
- **CONTEXT-04** — **MUST**, when retrieval is part of the task: evaluate whether relevant, permitted evidence was retrieved separately from whether the final answer is correct and supported. Citation-presence checks MUST NOT be treated as proof that cited material supports the claims.
- **CONTEXT-05** — **SHOULD**, when information persists across tasks as memory: define its purpose, scope, ownership, access boundaries, and correction and deletion handling before enabling it; apply the applicable privacy and retention requirements. Persistent memory is not required for agents whose tasks do not need continuity.

## Worked example

The shared fictional example is the policy-assistance candidate `POLICY-BUILD-001` for `internal-policy-assistance`, a fixed retrieval-and-answer workflow with no write capability. Its terminal outcomes are `complete`, `needs_information`, `declined`, and `failed`. The scenarios are expected behavior, not observations.

The source map admits `travel-policy-2026@2026-10-01` as the current policy and keeps `travel-policy-2024-superseded@2024-01-01` as an approved historical record. `employee-uk-104` may read the policy; `contractor-uk-204` may not.

For the London question, trusted requester context filters the source set before content is assembled. The selection is a bounded excerpt from the current source, "London hotel limit: GBP 220.", with its revision and locator. The superseded GBP 200 passage may appear in a stale-evidence test but is not shown as current. The expected `complete` answer states GBP 220 and points to the current evidence; the citation is a review pointer, not proof of support.

If the current permitted source is absent, the candidate does not conclude there is no London policy: the outcome is `needs_information`, saying it cannot verify the current limit. If retrieval reaches its declared failure condition, the outcome is `failed`, with no invented amount or citation.

In the conflict variant, `travel-policy-2026-conflicting-amendment@2026-10-12` is also current, approved, permitted, and equally authoritative, and its GBP 260 conflicts with GBP 220. A later date is not a precedence rule, so the outcome is `needs_information`: name the conflict and give no definitive amount.

For `contractor-uk-204`, the protected boundary denies access before policy content enters context, and the outcome is `declined` with no restricted amount or text. In the indirect-injection variant, an untrusted travel note tries to redirect behavior. It stays untrusted data and adds no capability. The expected result still answers the permitted question, GBP 220, with no write attempt and no blanket refusal caused only by hostile text.

The source record marks memory disabled and persistent caching not enabled. If either is proposed later, a fresh decision must cover source revision, requester scope, permission changes, correction, deletion, and derived data. An earlier selection is not a reusable answer for a different requester or a later policy state.

## Evidence and checklist

The [context-source record](../../templates/2.6/context-source-record.yaml) makes the admitted sources, status, permission boundary, selection lineage, bounded outcomes, cache questions, and memory decision inspectable; its `illustrative-unexecuted` status means it describes design, not a live lookup. It complements the [agent contract](02-agent-contracts-and-configuration.md), which declares dependencies, capability bounds, terminal outcomes, and effective configuration identity. The data-handling record in [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) decides what bodies, excerpts, cache entries, prompts, and diagnostics may be retained.

For a retrieval-capable candidate, a reviewer can inspect, without retaining more content than the data policy allows:

- a source map with identity, revision or currentness signal, authority role, allowed purpose, and unresolved precedence questions;
- the trusted identity and permission path that filters protected material before model exposure;
- a selection record for a representative case, with selected and excluded identities, locators, direct-excerpt or transformation status, and the context rationale;
- an expected response for missing, stale, inaccessible, conflicting, and unavailable evidence, tied to existing terminal outcomes;
- a cache and memory decision stating whether each is absent or, if proposed, the source, scope, and change assumptions it needs; and
- Part 4 case and evaluator records that treat evidence retrieval, semantic support, and answer behavior as related but distinct claims.

These artifacts do not show that the boundary is active or an answer is safe everywhere; follow [Part 4](../04-testing-and-evaluation/README.md) for evaluation. The source map needs a source-status and permission-change signal before a cache or transformed artifact can be reused. The owner, invalidation mechanism, and cache retention are `null` in the illustrative record; resolve them with the source, authorization, and data-handling owners before a persistent retrieval optimization joins a production candidate.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1 Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"
[2]: https://www.w3.org/TR/prov-dm/ "W3C PROV-DM The PROV Data Model"
[3]: https://aclanthology.org/2024.eacl-demo.16/ "RAGAS Automated Evaluation of Retrieval Augmented Generation"
[4]: https://aclanthology.org/2024.tacl-1.9/ "Lost in the Middle How Language Models Use Long Contexts"
[5]: https://arxiv.org/abs/2005.11401 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
[6]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents "Effective context engineering for AI agents"
[7]: https://www.anthropic.com/news/contextual-retrieval "Introducing Contextual Retrieval"
[8]: https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ "OWASP LLM08:2025 Vector and Embedding Weaknesses"

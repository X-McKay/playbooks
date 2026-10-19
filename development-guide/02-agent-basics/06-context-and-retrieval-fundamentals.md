# 2.6 Context and Retrieval Fundamentals

**Status:** 0.5.0-draft.2 — draft

**Audience:** Builders and reviewers who design what an agent receives as evidence for a bounded task

**Applicability:** Every agent needs a clear account of the information presented to its model. Apply the retrieval guidance when external documents, records, or indexes supply run-time context. Apply the memory guidance only when information is deliberately kept across tasks. Retrieval, memory, caching, and context optimization are not universal components.

**Reader question:** How do you assemble just enough permitted, traceable evidence for a task, recognize when it is insufficient, and leave a reviewer able to inspect what the design relies on?

[Part 2 — Agent Basics](README.md) · [Applicability](../../applicability.md) · [2.2 Agent Contracts and Configuration](02-agent-contracts-and-configuration.md) · [2.7 MCP and Standardized Integrations](07-mcp-and-standardized-integrations.md) · [Part 8 — Model Context and Resource Engineering](../../engineering-reference/08-model-context-and-resource-engineering/README.md)

## Purpose and applicability

**Context** is the bounded material supplied to a model for one decision or response: task instructions, the current request, trusted run-time facts, selected conversation turns, and evidence from an approved source. **Context engineering** is choosing, ordering, limiting, and labelling that material so the model gets what this task needs and nothing more.

**Retrieval** is one conditional way to build context: it obtains candidates from a larger external or indexed collection, then selects a bounded set of passages or records. Retrieval-augmented generation (**RAG**) combines retrieval with a generated answer. [5] Retrieved material is not thereby true, current, permitted, or correctly used: a source can be authoritative yet superseded, current yet unavailable to this requester, or accessible yet outside the task's purpose.

**Memory** deliberately keeps information from one task for a later one. Reading a memory store or holding a document for one run does not make retrieval durable memory. A policy assistant needs no memory when the request, trusted run-time context, and approved sources answer the question.

Embedding method, chunk size, ranking algorithm, model window, cache implementation, and memory architecture belong to [Part 8](../../engineering-reference/08-model-context-and-resource-engineering/README.md). Identity and permission checks stay with [3.1 Identity, Authority, Zero Trust, and Least Privilege](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md), untrusted retrieved content with [3.2 Untrusted Inputs, Retrieved Content, and Action Boundaries](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md), and data lifecycle and audit with [3.3 Data Privacy, Handling, and Minimum Audit Evidence](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

## Working model

Separate why material is present from what it says. Instructions describe task behavior; the request states what the requester wants; trusted run-time context supplies facts such as the authenticated requester, tenant, and permission decision; retrieved text is domain evidence; tool results, summaries, cache entries, and conversation turns are data to assess. No role upgrades another: a retrieved instruction is not policy, a source label is not authorization, and a schema does not prove a claim.

```text
declared task and admitted source purpose
  → trusted requester and permitted source scope
  → candidate retrieval with source metadata
  → relevance, authority, currentness, and conflict assessment
  → selected excerpts or labelled transformations within a context budget
  → supported answer, bounded uncertainty, or declared terminal outcome
  → source/selection record for review
```

A fixed workflow can make each step explicit, including a branch for a missing source or unresolved conflict; a bounded adaptive alternative may choose among finite admitted steps (clarify, locate permitted evidence, respond, escalate). Either way, the model does not decide what it may read or whether a source becomes authoritative.

### Five properties that must not be collapsed

**Provenance** identifies where material came from and how it reached its current form: document identity, revision, passage locator, retrieval time, and transformation identity. NIST's Generative AI Profile suggests, as context-dependent guidance, determining data origin and content lineage for documentation and evaluation. [1]

**Domain authority** asks whether a source may establish this kind of fact; **currentness**, whether its version or effective status applies now; **requester accessibility**, whether this requester may receive it through the protected boundary; **semantic support**, whether it supports the response's statement. A current source does not support every interpretation, and an approved historical document can show a superseded rule without being authoritative now.

**Lineage** matters when context is transformed. W3C PROV describes derivation as transforming, updating, or constructing one entity from another, with an activity that makes the path explicit. [2] A chunk, excerpt, summary, translation, normalized record, or cache entry can carry its source identity, revision, and transformation. That does not make it lossless, but it gives the reviewer a route back to the original.

**Relevance** is task-specific usefulness, not a keyword match: a passage can mention London without saying which worker group, date, or condition applies. Search retrieves candidates, ranking orders them, optional reranking compares the better ones, and excerpt selection places a bounded passage in context. Each fails differently: a short excerpt can drop a condition, and a full document can bury the answer.

**Permission** is checked before protected content reaches the model, not after an answer is formed, because filtering the final answer cannot undo a disclosure already in context. Trusted identity and the protected retrieval boundary decide eligibility; a model-generated source name, tenant, or query is only a request parameter ([3.1](../03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md)). Keep a vector index permission-aware or partitioned by tenant, since similarity search across mixed data can leak between tenants. [8]

### A bounded context is a design choice

A **context budget** is the model-visible material the task supplies at a decision point, not a universal token count. It must leave room for instructions, request, evidence, response, and the uncertainty path, and favors a small, traceable excerpt over a dump of search results.

More input is not better: as context grows, recall of any one item tends to fall, sometimes called context rot. Liu and colleagues found, on multi-document question answering and key-value retrieval, that the models tested did best with relevant information at the start or end of the input and often worse in the middle. [4] That is a reason to test context selection under your own conditions, not a rule about source order or proof that any chunking or ranking method is best. The aim is the smallest set of high-signal material that gets the outcome. [6]

Decide which evidence the answer needs, which qualifiers must travel with it, and what can stay out. Record why an item was selected, excluded, truncated, or transformed, never hiding an excluded conflict or removed condition. Measurement and tuning are Part 8 work.

For long-running tasks, three practices keep the budget under control: [6]

- **Just-in-time loading.** Keep lightweight references (identifiers, locators, saved queries) in context and load full content only when a step needs it.
- **Compaction.** When history outgrows the budget, summarize and continue. Tune for recall first so constraints, open decisions, and unresolved conflicts survive, and clear stale raw tool results.
- **Notes outside the window.** Persist working notes to storage the agent can read back, treating them as memory (below) if they cross tasks.

## Decisions and best practices

### Decide whether retrieval is needed and what it may establish

If the request, fixed instructions, and trusted run-time facts suffice, retrieval adds a dependency without value. Otherwise, name the admitted source collection and the claim each source type may establish, so open-ended search becomes a reviewable evidence boundary. For each source, record admission, authority, currentness, and accessibility as separate fields, as the [context-source record](../../templates/2.6/context-source-record.yaml) does.

A source may need a precedence rule: status, effective date, revision, owner decision, or an explicit supersession link. A date alone is not a safe tie-breaker. When equally authoritative current sources conflict and the rule does not resolve them, surface the uncertainty rather than pick the most recent-looking document.

### Design retrieval as evidence selection, not a document dump

Choose a source unit that keeps its link to the original. **Chunks** make selection practical, but a boundary can separate a rule from its exception, definition, or condition. Keep a stable source identity, revision or effective state, passage locator, and enough surrounding context to show why the excerpt applies, and say whether it is a direct excerpt or derived form. A well-established fix for lost chunk context is to prepend a short chunk-specific explanation of where the chunk sits in its document before indexing, combine embedding search with keyword search (such as BM25), and rerank; the published results show fewer failed retrievals than embeddings alone. [7] Test it on your own data.

Search, ranking, and reranking narrow candidates; none tests truth. A miss can come from terminology, indexing, permissions, an unavailable dependency, or a query that missed the user's condition, and a top match can be stale, off-scope, or weak.

A **summary** is a new derived artifact, not a shortcut to source authority; it can drop an exception or blur which revision supplied a claim. Before offering one as evidence, identify its inputs, source revisions, purpose, and route to the underlying passages. Labels and delimiters on untrusted material help interpretation but are not enforcement ([3.2](../03-security-and-trust-boundaries/02-untrusted-inputs-retrieved-content-and-action-boundaries.md)).

### Carry provenance without confusing it for support

A citation is a review pointer, not evidence: it can name the right document while the answer overstates it, cite a superseded revision, or omit a decisive condition.

The RAGAS paper (peer-reviewed at EACL 2024) separates context relevance, answer relevance, and faithfulness to the supplied context. [3] Use the distinction as a diagnostic (was relevant, permitted evidence found, was it used faithfully, does the response address the request?) without needing its automated methods; no score settles authority, currentness, permission, or truth. [Part 4](../04-testing-and-evaluation/README.md) owns case design, evaluators, and interpretation.

A proportionate provenance record has source identity, revision or status, locator, source role, access decision context, retrieval or transformation identity, and time or release context, as safe identifiers and a short rationale rather than copied document bodies.

### Plan for absence, stale evidence, conflict, and cache drift

"No match" can mean the corpus is silent, the request needs clarification, the source is inaccessible, the index is down, or retrieval missed it. Keep these distinct and map them under the agent contract to `needs_information` (missing condition or insufficient current evidence), `declined` (protected-source denial), or `failed` (dependency failure), rather than folding them into "no answer" or making uncertainty look like success.

A **cache** is a derived copy of source material or a prior selection, and can outlive a source revision, policy change, or requester permission. State the source and scope assumptions for reuse, the invalidation rule, and derived-data handling; a cache cannot make a formerly permitted excerpt displayable after scope changes. Leave invalidation, retention, and ownership as explicit open decisions, not silent defaults.

Common failures are a cache key naming a document but omitting the revision, requester scope, or permission decision that made the selection valid, and treating a recently refreshed index as proof that everything in it is current. A review record should separate cache candidate, source revision, access decision, and currentness signal, and show why reuse was allowed. Cache and derived-artifact lifecycle belongs to [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

### Keep memory purpose-limited and separately reviewable

If cross-task continuity is proposed, define the **memory write scope** (what may be kept, for what purpose, from which task context, and who or what can correct or delete it) and, separately, the **memory read scope** (which requester, task, tenant, and purpose may retrieve it). A remembered fact gains no authority in a new task, and a prior conversation does not make its content current.

Memory suits a defined continuity need, such as a requester preference, but can hold stale, private, or cross-scope context, or content poisoned by an earlier untrusted input. Without such a need, record memory as disabled. Retention, deletion, correction, access, and derived copies are governed by [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

### Builder workflow

1. **State the evidence need** and the outcome when evidence is unavailable, or record retrieval as not applicable.
2. **Create a source map:** per source, purpose, authority, currentness or precedence signal, access boundary, data-handling concern, and identity, leaving owner, refresh, or invalidation visibly unresolved where unknown.
3. **Describe the selection path:** source unit, search scope, ranking step, excerpt context, and exclusion rationale, with the access decision before material reaches the model.
4. **Record transformations and bounds:** direct excerpt or derived artifact, budget rationale, and what must stay visible when shortened.
5. **Define evidence outcomes** for missing, stale, denied, unavailable, and conflicting evidence.
6. **Connect** the source record to the capability manifest, case design, and data-handling record.

## Requirements

- **CONTEXT-01** — **MUST**, when external documents, records, or indexes are retrieved for a run: use only sources approved for the task, and apply the caller's permitted scope using trusted identity and controls outside model-generated decisions. Discovery or retrieval does not itself authorize access. See 3.1 for the canonical authorization requirements.
- **CONTEXT-02** — **MUST**, when retrieved evidence can affect an answer: preserve enough source and version or freshness metadata to identify the material used and trace relevant claims back to it, consistent with data-minimization rules. If the source's current status cannot be established, do not represent it as verified current information.
- **CONTEXT-03** — **MUST**, when sources may be missing, stale, out of scope, or conflicting: define the precedence and freshness signals that apply, and provide a bounded response for unresolved evidence. The agent MUST NOT present retrieval failure as proof that no applicable information exists or resolve unresolved conflict by unsupported guesswork.
- **CONTEXT-04** — **MUST**, when retrieval is part of the task: evaluate whether relevant, permitted evidence was retrieved separately from whether the final answer is correct and supported. Citation-presence checks MUST NOT be treated as proof that cited material supports the claims.
- **CONTEXT-05** — **SHOULD**, when information persists across tasks as memory: define its purpose, scope, ownership, access boundaries, and correction and deletion handling before enabling it; apply the applicable privacy and retention requirements. Persistent memory is not required for agents whose tasks do not need continuity.

## Worked example

The shared fictional candidate `POLICY-BUILD-001` (`internal-policy-assistance`) is a fixed retrieval-and-answer workflow with no write capability and terminal outcomes `complete`, `needs_information`, `declined`, and `failed`. The source map admits `travel-policy-2026@2026-10-01` as current and keeps `travel-policy-2024-superseded@2024-01-01` as an approved historical record. `employee-uk-104` may read the policy; `contractor-uk-204` may not.

Expected treatments:

- **Current source.** Trusted requester context filters the source set before assembly. The selection is a bounded excerpt, "London hotel limit: GBP 220.", with revision and locator. The superseded GBP 200 passage may appear in a stale-evidence test but never as current. The `complete` answer states GBP 220 and points to the current evidence.
- **Absent source.** The candidate does not conclude there is no London policy; it returns `needs_information`, saying it cannot verify the current limit. At the declared retrieval failure condition, it returns `failed`, with no invented amount or citation.
- **Conflict.** `travel-policy-2026-conflicting-amendment@2026-10-12` is also current, approved, permitted, and equally authoritative, with GBP 260. A later date is not a precedence rule, so the outcome is `needs_information`, naming the conflict with no definitive amount.
- **Denied.** For `contractor-uk-204`, the protected boundary denies access before policy content enters context: `declined`, with no restricted amount or text.
- **Indirect injection.** An untrusted travel note tries to redirect behavior; it stays data and adds no capability. The result still answers GBP 220, with no write attempt and no blanket refusal caused only by hostile text.

The source record marks memory disabled and persistent caching not enabled. Proposing either later needs a fresh decision on source revision, requester scope, permission changes, correction, deletion, and derived data; an earlier selection is not a reusable answer for another requester or a later policy state.

## Evidence and checklist

The [context-source record](../../templates/2.6/context-source-record.yaml) (status `illustrative-unexecuted`: design, not a live lookup) complements the [agent contract](02-agent-contracts-and-configuration.md); the [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) data-handling record decides what bodies, excerpts, cache entries, prompts, and diagnostics may be retained.

For a retrieval-capable candidate, keep, within the data policy:

- a source map with identity, currentness signal, authority role, allowed purpose, and open precedence questions;
- the trusted permission path that filters protected material before model exposure;
- a selection record for a representative case: selected and excluded identities, locators, excerpt or transformation status, and rationale;
- expected responses for missing, stale, inaccessible, conflicting, and unavailable evidence;
- the cache and memory decision; and
- Part 4 records treating retrieval, semantic support, and answer behavior as distinct claims.

These do not show the boundary is active or an answer safe everywhere. Before a cache or transformed artifact is reused, the source map needs a source-status and permission-change signal; the illustrative record's `null` owner, invalidation mechanism, and cache retention must be resolved with the source, authorization, and data-handling owners before a persistent retrieval optimization joins a production candidate.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "NIST AI 600-1 Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"
[2]: https://www.w3.org/TR/prov-dm/ "W3C PROV-DM The PROV Data Model"
[3]: https://aclanthology.org/2024.eacl-demo.16/ "RAGAS Automated Evaluation of Retrieval Augmented Generation"
[4]: https://aclanthology.org/2024.tacl-1.9/ "Lost in the Middle How Language Models Use Long Contexts"
[5]: https://arxiv.org/abs/2005.11401 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
[6]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents "Effective context engineering for AI agents"
[7]: https://www.anthropic.com/news/contextual-retrieval "Introducing Contextual Retrieval"
[8]: https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ "OWASP LLM08:2025 Vector and Embedding Weaknesses"

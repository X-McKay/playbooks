# 8.2 Retrieval, Memory, and Context Optimization

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers responsible for context pipelines
**Applicability:** Apply when an agent retrieves indexed material, transforms or caches context, or keeps information across tasks. Retrieval and persistent memory are conditional capabilities; agents without them need not add them.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Applicability](../../applicability.md) · [Context and retrieval fundamentals](../../development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) · [8.1 Model Selection, Parameters, and Routing](01-model-selection-parameters-and-routing.md) · [Next: 8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md)

## Purpose and applicability

Retrieval and memory let you supply relevant information without putting a whole corpus or conversation in every request. They also add failure modes: chunking can hide a constraint, ranking can omit a decisive exception, a summary can erase a qualification, a cache can serve a result from the wrong scope, and remembered information can outlive its purpose. Context optimization is a quality and safety decision, not only a way to save tokens.

Chapter [2.6](../../development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) covers source approval, permission scope, provenance, freshness, and missing or conflicting evidence. This chapter covers the engineering choices after selection: chunking, indexing, ranking, context transformations, caching, and memory lifecycle. For authorization and privacy rules, see [3.1](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) and [3.3](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md). A context record, retrieved passage, cached answer, or memory entry is data to weigh; it cannot grant an agent new authority.

## Working model

A retrieval path turns approved source material into something searchable, then gives selected evidence to a model. The usual stages are ingestion, normalization, chunking, indexing, candidate retrieval, filtering or reranking, and context assembly. Each is a separate decision point. Retrieval-augmented generation combines a language model with a retrieved, non-parametric evidence store, but a pipeline does not guarantee that a returned passage is current, relevant, or used correctly. [1]

Chunking decides which text travels together. Fixed-length segments are simple; structure-aware or topic-aware boundaries can keep a clause with its heading, table, exception, or definition. Very small chunks lose qualifying context, and very large ones dilute the decisive passage and use up the budget. Overlap preserves continuity across a boundary but duplicates evidence. No one rule fits every corpus: one small domain study reported its results for a single clinical corpus and query set and cautioned against generalizing. [3] Treat chunk size, overlap, parent-child context, and metadata as choices to test on your own documents and questions.

Candidate retrieval asks which indexed units might matter; reranking or selection then picks those that fit the task and budget. Relevance is not the only test. A policy question may need the operative rule, an exception, and an effective date. Keep source and section identity, version or status, and scope metadata attached through every stage. Authorization and tenant filtering must use trusted controls, not the model's choice of which retrieved items to see.

Context transforms include selecting, ordering, deduplicating, truncating, summarizing, and compacting. Each trades detail for fit. A summary is derived and does not replace source lineage: it can drop negation, scope, dates, exceptions, or the fact that two documents disagree.

Bigger windows do not make every token equally usable. Studies of long-context question answering found that relevant information was used less reliably in the middle of long inputs, and that models passing simple needle-in-a-haystack tests lost accuracy as input length grew. [2] [5] Practitioners call this context rot: recall falls as context grows, so context is a finite resource, and the goal is the smallest set of high-signal tokens that gets the task done. [4] Results vary by model and task, so test context size and ordering instead of assuming a larger window is better.

Caching and memory solve different problems. A prompt or context cache reuses prepared input; an application result cache reuses an answer or retrieval result; persistent memory keeps selected information from earlier tasks. Each can go stale or expose data outside its scope. Treat memory as a managed data store, not as an extension of the conversation or a policy authority.

## Decisions and best practices

Begin with the task: what evidence must be present for a correct answer, and what can safely be left out? If the source set is small enough to read directly, retrieval may be unnecessary machinery. If you retrieve, keep meaningful boundaries and the metadata needed to resolve status, applicability, and conflicts. Where structure carries meaning, keep headings, parent sections, table labels, or neighboring clauses with the passage.

Tune the whole path, not just a retriever score. Measure whether relevant, permitted evidence is found and whether irrelevant or superseded items intrude; separately, assess whether the answer uses the evidence accurately. Test changes to chunking, candidate count, reranking, ordering, or compression on the same versioned cases. A citation shows only that an identifier was emitted, not that the source supports the claim. [4.5](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md) covers case design and separating retrieval from answer quality.

**Load context just in time.** In long-running or tool-heavy agents, keep lightweight references (file paths, queries, identifiers) in context and fetch the content when a step needs it, instead of preloading everything. [4] Clear old raw tool results once the agent has used them, keeping a short record of what was found. Write progress notes, decisions, and open questions to storage outside the window and read them back when needed. Hand self-contained subtasks to a sub-agent with a clean context and have it return a short summary (see [9.2](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)). [4]

**Treat compaction as a tool, with protected fields.** Compaction (summarizing a long history so work can continue) is a normal part of long-horizon agents, but it costs extra processing and can lose information. Tune it for recall first, so nothing needed is dropped, then trim for brevity, and evaluate it against a baseline. [4] Prefer deterministic trimming or selection when it keeps what the task needs. Define protected fields that compaction must carry over unchanged: policy constraints, identity and permission scope, required evidence, approval state, and side-effect state. If a transformation cannot keep a material constraint and its source lineage, keep the original available or return a bounded uncertainty outcome.

**Cache only when reuse is safe.** For data-dependent results, scope cache keys to the user or tenant authorization, source and data version, agent and instruction configuration, and the relevant query inputs. Define invalidation for source updates, permission changes, and policy changes. Do not cache unresolved or time-sensitive answers as if they were current. A cache hit never replaces a fresh authorization check. For prompt caching, keep the prefix stable: put instructions and tool definitions first, in a deterministic order, and append new content after them (see [8.3](03-cost-latency-and-performance-optimization.md)).

**Add persistent memory deliberately.** First decide what continuity the task needs. Define what may be written, who or what it is about, who can read it, how long it stays useful, and how it is corrected or removed. Store the smallest useful record with provenance and time context. Resolve disagreement with the applicable source authority and recency rules; repetition in memory is not proof. If no rule settles a material conflict, surface it or ask, and do not silently prefer the latest remembered statement.

## Requirements

- **CONTEXT-OPT-01** — **MUST**, when source material is chunked or otherwise transformed for indexing: preserve a stable link from each retrievable unit to its source and relevant version or status metadata, and record the transformation configuration needed to rebuild or diagnose the representation. Removed, superseded, or materially changed source content MUST NOT remain silently represented as current.
- **CONTEXT-OPT-02** — **MUST**, when retrieval results are assembled for model context: select chunk boundaries and any surrounding context using representative corpus and task cases, and test for lost headings, exceptions, scope conditions, negation, or other constraints material to the answer. No particular chunking method or size is prescribed.
- **CONTEXT-OPT-03** — **MUST**, when content is summarized, compacted, truncated, reordered, or otherwise transformed before use: preserve material constraints, source lineage, and applicable trust/scope labels; evaluate the transformed context against the untransformed evidence for task-critical omissions. If a required constraint or its provenance cannot be retained, the system MUST keep access to the original evidence or produce a bounded uncertainty outcome rather than treating the transformed text as complete.
- **CONTEXT-OPT-04** — **MUST**, when retrieved context or generated results are cached: enforce the applicable user/tenant and authorization scope in cache lookup, bind reuse to relevant source and policy versions, and invalidate or bypass entries when source freshness, access, or policy changes make them inapplicable. A cache hit MUST NOT replace execution-time authorization.
- **CONTEXT-OPT-05** — **MUST**, when information persists as agent memory across tasks: define the memory's purpose, subject/scope, permitted write conditions, access boundary, provenance, and correction, expiry, and deletion handling. Memory MUST NOT authorize tools, change policy, or expose another user's or tenant's information.
- **CONTEXT-OPT-06** — **MUST**, when a task relies on retrieval or context transformation: evaluate retrieval adequacy separately from final answer support, and include cases that can reveal missing, stale, conflicting, or permission-scoped evidence and material losses caused by transformation. A citation-presence check alone MUST NOT be reported as proof of semantic support.
- **CONTEXT-OPT-07** — **SHOULD**, when context limits require compaction or repeated context assembly: prefer the least lossy approach that meets the operational constraint, and compare candidate settings against a baseline for task quality, critical constraints, latency, and cost before adoption. Do not assume that fewer tokens or a larger context window alone improves outcomes.

These requirements add to the authorization, privacy, and evidence rules in Parts 3 and 4. Each applies when its trigger is present.

## Worked example: the current travel limit survives retrieval and compaction

The fictional policy assistant answers from approved, current, permission-filtered documents, returns citations and uncertainty, cannot write externally, and finishes with `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. In the `travel-policy-current` test fixture the London hotel limit is GBP 220, and a superseded policy gives a different amount. These are test facts, not real policy.

The index stores sections, not arbitrary fragments, where possible. Each passage keeps a source ID, section locator, version, effective or current status, and access-scope metadata. For "What is the hotel limit for a trip to London?", retrieval finds the travel section and the reranker keeps the operative limit with its applicability and effective-date clauses. The runtime filters by the employee's trusted permission scope before context is assembled. The answer cites the current section and states GBP 220 only if the supplied evidence supports it.

Now add a context budget. A summary saying only "London hotel limit: GBP 220" is not enough if it drops the policy version or an exception that changes who or when the limit applies. So the assistant keeps the original passage and those qualifiers as protected fields, or marks the result incomplete and returns `needs_information`. It does not treat an untraceable summary as authoritative. A regression case moves the decisive clause to different positions in a longer assembled context, because position affects some model and task combinations. [2]

Caching the answer by normalized question text alone is a tempting shortcut. It could return one tenant's answer to another, or serve GBP 220 after the source changes. The safer design puts the authorization partition and the source and policy version in the cache scope and invalidates on updates. The assistant needs no cross-session memory for this task, so it keeps context only for the active interaction and builds no profile of past questions.

Evaluation is split by stage. Retrieval checks assert that the current passage and its qualifiers are available within the caller's permitted scope, and that the superseded version is identified or excluded. Answer checks assess whether the right version is applied and whether the citation supports the claim. Transformation checks compare compacted context with the original for lost constraints and lineage. Cache tests vary user, tenant, source version, and permission state. A conflict case supplies two apparently current passages with no precedence rule; the right outcome is to expose the conflict or ask, not to choose the higher-ranked chunk.

## Evidence and checklist

Keep a short, versioned record of the corpus and index inputs, chunking and ranking settings, context assembly and compaction policy (including protected fields), cache scope and invalidation rules, and any memory schema and lifecycle. Evaluation evidence should let you trace sample answers to the passages actually supplied, inspect transformation losses, and reproduce critical retrieval cases without keeping more sensitive content than policy allows.

- [ ] The task has a stated reason for retrieval, caching, or persistent memory; unused mechanisms are not added by default.
- [ ] Indexed units keep source identity, version or status, and enough structure to recover context.
- [ ] Retrieval and answer-support claims have separate checks, including missing, stale, conflicting, and permission-scoped cases.
- [ ] Changes to chunking, ranking, ordering, and context budget are evaluated on representative cases.
- [ ] Summaries and compaction are checked for lost constraints, lineage, scope, and conflict signals.
- [ ] Cache lookup and invalidation respect identity, authorization, source freshness, and policy changes.
- [ ] Persistent memory has a purpose, scope, provenance, access boundary, and a correction, expiry, and deletion path, and cannot create authority.
- [ ] Context optimization is compared with a baseline for task quality and operational effects, not only token count.

See [8.3](03-cost-latency-and-performance-optimization.md) for wider resource decisions and [2.6](../../development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) for source approval, provenance, and freshness.

## References

[1]: https://arxiv.org/abs/2005.11401 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
[2]: https://aclanthology.org/2024.tacl-1.9/ "Lost in the Middle: How Language Models Use Long Contexts"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12649634/ "Comparative Evaluation of Advanced Chunking for Retrieval-Augmented Generation in Large Language Models for Clinical Decision Support"
[4]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents "Effective context engineering for AI agents"
[5]: https://arxiv.org/abs/2404.06654 "RULER: What's the Real Context Size of Your Long-Context Language Models?"

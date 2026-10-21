# 8.2 Retrieval, Memory, and Context Optimization

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and reviewers responsible for context pipelines
**Applicability:** When an agent retrieves indexed material, transforms or caches context, or keeps information across tasks. Retrieval and persistent memory are conditional; agents without them need not add them.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Applicability](../../applicability.md) · [Context and retrieval fundamentals](../../development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) · [8.1 Model Selection, Parameters, and Routing](01-model-selection-parameters-and-routing.md) · [Next: 8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md)

## Purpose and applicability

Retrieval and memory avoid sending a whole corpus or conversation each time, but add failure modes: chunking can hide a constraint, ranking can omit a decisive exception, a summary can erase a qualification, a cache can serve the wrong scope, and memory can outlive its purpose. Context optimization is a quality and safety decision, not only token saving.

[2.6](../../development-guide/02-agent-basics/06-context-and-retrieval-fundamentals.md) covers source approval, permission scope, provenance, freshness and conflicting evidence; [3.1](../../development-guide/03-security-and-trust-boundaries/01-identity-authority-zero-trust-and-least-privilege.md) and [3.3](../../development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md) cover authorization and privacy. This chapter covers what comes after: chunking, ranking, transformations, caching and memory. A passage, cached answer or memory entry is data; it cannot grant authority.

## Working model

A retrieval path runs ingestion, normalization, chunking, indexing, candidate retrieval, reranking and context assembly, each a separate decision. Retrieval-augmented generation does not guarantee a passage is current, relevant or used correctly.[1]

Chunking decides which text travels together. Structure-aware boundaries keep a clause with its heading, table, exception or definition; tiny chunks lose context, huge ones dilute the decisive passage, and overlap adds continuity and duplication. No rule fits every corpus: a 30-question clinical study found adaptive chunking best but said that result is unproven outside its domain,[3] so test size, overlap, parent-child context and metadata on your own documents.

Reranking picks candidates that fit the task and budget, and relevance is not the only test: a policy question may need the rule, an exception and an effective date. Keep source and section identity, version or status and scope metadata through every stage, and filter by authorization and tenant with trusted controls, not the model's choice.

Selecting, ordering, deduplicating, truncating, summarizing and compacting each trade detail for fit. A summary is derived and does not replace lineage: it can drop negation, scope, dates, exceptions or the fact that sources disagree.

Bigger windows do not make every token equally usable: long-context studies found information used less reliably mid-input, and accuracy falling with length even in models passing needle-in-a-haystack tests.[2] [5] Practitioners call this context rot; aim for the smallest set of high-signal tokens that does the task, and test size and ordering per model.[4]

A prompt or context cache reuses prepared input, a result cache reuses an answer or retrieval, and persistent memory keeps selected information across tasks. Each can go stale or leak scope. Treat memory as a managed data store, not part of the conversation or a policy authority.

## Decisions and best practices

**Begin with the task.** Decide what evidence a correct answer needs and what can be left out; a small source set may not need retrieval at all.

**Tune the whole path.** Measure separately whether permitted evidence is found (and superseded or irrelevant items kept out) and whether the answer uses it accurately, on the same versioned cases for every change to chunking, candidate count, reranking, ordering or compression. A citation shows an identifier was emitted, not that it supports the claim; see [4.5](../../development-guide/04-testing-and-evaluation/05-planning-designing-and-running-tests-and-evaluations.md).

**Load context just in time.** Long-running or tool-heavy agents keep lightweight references (paths, queries, identifiers) and fetch content when a step needs it.[4] Clear old raw tool results once used, keeping a short note of findings; write progress notes, decisions and open questions to external storage; and hand self-contained subtasks to a clean-context sub-agent that returns a short summary ([9.2](../09-multi-agent-systems-and-interoperability/02-delegation-handoffs-and-agent-to-agent-interfaces.md)).[4]

**Compact with protected fields.** Compaction (summarizing history so work can continue) is normal for long-horizon agents, but aggressive compaction can drop details whose importance shows only later; tune the summary for recall first, then brevity.[4] Prefer deterministic trimming where it suffices. Policy constraints, identity and permission scope, required evidence, approval state and side-effect state carry over unchanged. If a transformation cannot keep a material constraint and its lineage, keep the original available or return bounded uncertainty.

**Cache only when reuse is safe.** Scope data-dependent keys to user or tenant authorization, source and data version, agent and instruction configuration, and relevant query inputs; invalidate on source, permission and policy changes; never cache unresolved or time-sensitive answers as current. A hit never replaces fresh authorization. For prompt caching, keep instructions and tool definitions first in deterministic order and append new content after ([8.3](03-cost-latency-and-performance-optimization.md)).

**Add persistent memory deliberately.** Decide what continuity the task needs, what may be written, about whom, who reads it, how long it stays useful and how it is corrected or removed. Store the smallest useful record with provenance and time. Resolve disagreement by source authority and recency rules, since repetition is not proof; if no rule settles a material conflict, surface it or ask rather than prefer the latest memory.

## Requirements

- **CONTEXT-OPT-01** — **MUST**, when source material is chunked or otherwise transformed for indexing: preserve a stable link from each retrievable unit to its source and relevant version or status metadata, and record the transformation configuration needed to rebuild or diagnose the representation. Removed, superseded, or materially changed source content MUST NOT remain silently represented as current.
- **CONTEXT-OPT-02** — **MUST**, when retrieval results are assembled for model context: select chunk boundaries and any surrounding context using representative corpus and task cases, and test for lost headings, exceptions, scope conditions, negation, or other constraints material to the answer. No particular chunking method or size is prescribed.
- **CONTEXT-OPT-03** — **MUST**, when content is summarized, compacted, truncated, reordered, or otherwise transformed before use: preserve material constraints, source lineage, and applicable trust/scope labels; evaluate the transformed context against the untransformed evidence for task-critical omissions. If a required constraint or its provenance cannot be retained, the system MUST keep access to the original evidence or produce a bounded uncertainty outcome rather than treating the transformed text as complete.
- **CONTEXT-OPT-04** — **MUST**, when retrieved context or generated results are cached: enforce the applicable user/tenant and authorization scope in cache lookup, bind reuse to relevant source and policy versions, and invalidate or bypass entries when source freshness, access, or policy changes make them inapplicable. A cache hit MUST NOT replace execution-time authorization.
- **CONTEXT-OPT-05** — **MUST**, when information persists as agent memory across tasks: define the memory's purpose, subject/scope, permitted write conditions, access boundary, provenance, and correction, expiry, and deletion handling. Memory MUST NOT authorize tools, change policy, or expose another user's or tenant's information.
- **CONTEXT-OPT-06** — **MUST**, when a task relies on retrieval or context transformation: evaluate retrieval adequacy separately from final answer support, and include cases that can reveal missing, stale, conflicting, or permission-scoped evidence and material losses caused by transformation. A citation-presence check alone MUST NOT be reported as proof of semantic support.
- **CONTEXT-OPT-07** — **SHOULD**, when context limits require compaction or repeated context assembly: prefer the least lossy approach that meets the operational constraint, and compare candidate settings against a baseline for task quality, critical constraints, latency, and cost before adoption. Do not assume that fewer tokens or a larger context window alone improves outcomes.

These add to the authorization, privacy and evidence rules in Parts 3 and 4, each when its trigger is present.

## Worked example: the current travel limit survives retrieval and compaction

The fictional read-only policy assistant answers from approved, current, permission-filtered documents with citations, ending `complete`, `needs_information`, `declined`, `failed` or a declared partial result. In the `travel-policy-current` fixture the London hotel limit is GBP 220; a superseded policy differs.

The index stores sections, each with source ID, locator, version, status and access scope. For "What is the hotel limit for a trip to London?", the reranker keeps the limit with its applicability and effective-date clauses, the runtime filters by trusted permission scope, and the answer cites the current section, stating GBP 220 only if supported.

Under a context budget, a summary reading "London hotel limit: GBP 220" is not enough if it drops the version or an exception about who or when. The assistant keeps the passage and qualifiers as protected fields, or returns `needs_information`. A regression case moves the decisive clause around a longer context, because position matters for some models.[2]

Caching by question text alone could leak across tenants or serve GBP 220 after a source change, so the key includes the authorization partition and source and policy versions. No cross-session memory or question profile is kept.

Evaluation is split by stage: retrieval (current passage and qualifiers available in scope, superseded version identified or excluded), answer (right version applied, citation supports the claim), transformation (compacted versus original for lost constraints and lineage), and cache (varying user, tenant, source version and permission). Two apparently current passages with no precedence rule should expose the conflict or prompt a question, not pick the higher-ranked chunk.

## Evidence and checklist

Keep a versioned record of corpus and index inputs, chunking and ranking settings, compaction policy and protected fields, cache scope and invalidation, and any memory schema. Evidence traces sample answers to supplied passages, shows transformation losses, and reproduces critical cases within privacy policy.

- [ ] Retrieval, caching and memory each have a stated reason; none is added by default.
- [ ] Summaries and compaction are checked for lost scope and conflict signals.
- [ ] Context optimization is compared with a baseline on quality and operations, not only token count.

## References

[1]: https://arxiv.org/abs/2005.11401 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
[2]: https://aclanthology.org/2024.tacl-1.9/ "Lost in the Middle: How Language Models Use Long Contexts"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12649634/ "Comparative Evaluation of Advanced Chunking for Retrieval-Augmented Generation in Large Language Models for Clinical Decision Support"
[4]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents "Effective context engineering for AI agents"
[5]: https://arxiv.org/abs/2404.06654 "RULER: What's the Real Context Size of Your Long-Context Language Models?"

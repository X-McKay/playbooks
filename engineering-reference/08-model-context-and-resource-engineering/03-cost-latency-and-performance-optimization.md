# 8.3 Cost, Latency, and Performance Optimization

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and operators improving production agents
**Applicability:** Use when model or tool work is costly, tasks finish too slowly, or throughput and user effort matter. Every production agent still needs bounded execution and operational limits; this chapter guides optimization and does not require every technique.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md)

## Purpose and applicability

Optimizing is not just making the model call faster. An agent is a chain of context assembly, retrieval, model work, tool execution, validation, and sometimes human review. Saving time or tokens in one step can shift work elsewhere, add failure risk, or make the answer less useful. A good optimization improves a defined outcome while keeping the quality, safety, and authority boundaries intact.

This chapter covers cost per verified success, failed-attempt cost, caching, batching, fewer calls, parallelism, streaming, and warm versus cold paths. Model choice and routing are in [8.1](01-model-selection-parameters-and-routing.md); retrieval and context changes are in [8.2](02-retrieval-memory-and-context-optimization.md); shared admission and backpressure are in [8.4](04-capacity-admission-control-and-backpressure.md). Define the population, denominator, baseline, target, and owner under [1.2](../../development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), then use Part 4 methods to get comparable evidence.

## Working model

Measure the whole task, not only the model request. Record where time goes: queueing, retrieval, model time, tool calls, orchestration, validation, and waits for people or outside systems. Report **time to first token (TTFT)** separately from time to a complete, validated outcome. Streaming improves perceived latency, but TTFT only marks when output starts; the task may not finish sooner. [1] Where approval or human review is involved, report the automated path and the human wait separately so one cannot hide the other.

A lower token price is not necessarily a lower cost per success. Measure attributable cost across successful and failed attempts, divided by the number of independently verified successes. Define whether the cost includes model and tool charges, retries, failed calls, infrastructure, and support effort. If people must correct or check more answers, track that time as its own measure and do not treat it as free. A run of cheap attempts followed by an expensive fallback can cost more than a capable first choice. Multi-agent designs raise cost further; see [9.1](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md).

Some usage data arrives only after a call ends or after billing is reconciled. Treat limits as brakes, not exact guarantees that a final charge cannot cross a threshold. Reconcile estimates with authoritative usage or billing data, and leave an unpriced or unknown amount unknown, not zero.

## Decisions and best practices

Start with a baseline for a representative task population: success definition, cost, completed-task latency, TTFT where relevant, and human effort. Look at distributions and key slices, not only averages. Find the dominant delay or expense before changing anything. Then change one thing at a time, compare on the same cases and conditions, and keep the change only if it holds the quality and safety gates and improves the metric that motivated it.

A practical order: bound worst-case execution; remove unneeded model calls and irrelevant context; limit tool-result size; reuse stable computation where safe; pick a capable model for each task; then tune batching, concurrency, and retries. This is a diagnostic sequence, not a ranking; your workload's biggest cost may call for a different experiment. Note that cutting input tokens often buys only a small latency gain, because generating output tokens usually dominates; measure before assuming it. [1] Set run limits in runtime controls, not in instructions to the model. Limits shared across workers need shared accounting, not counters that vanish on restart. Retries at several layers multiply, so work out the maximum combined attempts and stop retries from repeating unsafe external effects. For resumable or side-effecting tasks, apply [Part 7](../07-durable-execution-and-human-governed-work/README.md).

**Fewer calls and parallel work.** Combine steps only when one request can do them without hiding independent validation or raising the cost of errors. Run work in parallel only when it is truly independent, cap fan-out, and respect shared capacity and rate limits. Parallel requests shorten the critical path but not total cost, and can worsen queueing or overload a dependency. Speculative work cuts the common-path wait but wastes resources when wrong; cancel it where possible and count cancelled work in cost.

**Caching and batching.** Prompt-prefix caching reuses computation for a repeated stable prefix. Matching rules, lifetime, price, and controls depend on the provider and model. [2] [3] Put stable material (instructions, tool definitions, reference text) before dynamic content, keep it byte-for-byte stable and in a fixed order between calls, and avoid edits to earlier context, because any change before the cache point forces a miss. Watch reads, misses, writes, and cost instead of assuming a hit. Long waits can outlast a cache entry, so treat resumed work as cold unless you observe otherwise.

Application-level result caching is a separate choice. Reuse only results whose freshness and correctness you can establish. Partition by tenant and authorization scope, bind entries to the model, settings, instruction and tool versions, normalized inputs, and source-data version, and expire them when policy or evidence changes. Do not reuse consequential actions, stale time-sensitive answers, or unvalidated output. See [8.2](02-retrieval-memory-and-context-optimization.md) for context and freshness controls.

Batch independent, latency-tolerant work, such as offline evaluation or bulk classification, when the delay and result handling fit. Do not send interactive requests through a batch just to claim a unit-price saving. Batch services have their own completion windows, failure handling, and pricing, and examples are not general guarantees. [4] For online micro-batching, include the wait to fill a batch in the end-to-end time.

**Streaming and warm/cold paths.** Streaming shows progress early, but first-token speed is not task completion. If text needs citation, policy, privacy, or output checks before people rely on it, buffer it, or treat streamed chunks as provisional until the checks pass. Compare perceived responsiveness and task completion separately. Measure cache-warm and cache-cold paths, first-run and resumed work, and primary and fallback routes where they occur. A warm-only result is not representative if users often hit cold starts.

## Requirements

- **PERF-01** When an agent has defined cost, latency, or performance objectives, its owner MUST specify the measured population, success denominator, measurement method, baseline, target or decision threshold, and accountable owner; cost per success MUST use verified successes and include attributable failed-attempt costs in the declared scope.
- **PERF-02** When an agent is deployed to production, its runtime MUST enforce applicable per-run limits for model requests, tool calls, and other declared resource bounds; a prompt or unshared in-memory counter MUST NOT be the sole enforcement mechanism.
- **PERF-03** When a proposed optimization changes model calls, context, caching, batching, parallelism, streaming, or retries, the release decision MUST compare the candidate with a baseline on relevant cases and MUST preserve applicable quality, safety, and authorization gates before the optimization is adopted.
- **PERF-04** When shared budgets span processes, workers, or resumptions, spend accounting MUST use a shared mechanism with defined reconciliation behavior; unknown or unpriced usage MUST remain unknown and MUST NOT be treated as zero.
- **PERF-05** When output is streamed before task completion, the interface MUST distinguish provisional content from a complete validated result wherever downstream checks are required before reliance; reported performance MUST distinguish TTFT from completed-task latency.
- **PERF-06** When caching or batching is used, the owner MUST define the applicable freshness, authorization/tenant partitioning, invalidation, and failure behavior; measurements MUST distinguish warm from cold paths when both materially occur, and batching MUST only be used where its completion delay fits the task requirement.

## Worked example

An internal policy assistant answers travel questions from approved, current, permission-filtered documents. It returns citations and uncertainty, cannot write externally, and finishes with `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. The fixture `travel-policy-current` is fictional test data: it allows GBP 220 for a London hotel, and a superseded document differs. A citation must support the answer; its presence alone is not success.

The team suspects repeated document context drives both spend and delay. It first records the same held-out cases, tenant boundary, source versions, verified outcomes, full completion time, TTFT, token and tool usage, failed attempts, and human correction. Baseline values come from its own run. It then tests two changes separately: dropping irrelevant retrieved passages while keeping the current versus superseded distinction, and reusing the stable instruction prefix where the model demonstrably supports it. It does not cache final answers across users or policy versions.

A change is accepted only if the cases still return the permitted amount when supported, distinguish the superseded source, ask for clarification when evidence is missing, and keep tenants isolated. The evaluator checks semantic support and not just citation presence. Cost is divided by verified successes and includes failed or corrected attempts. Completion time and TTFT are compared separately, with warm and cold runs reported apart. If streaming starts printing a number before its source is validated, that text stays provisional.

If a change lowers input tokens but raises unsupported answers or human correction, reject it even if the call looks cheaper or the first token arrives sooner. If it keeps all gates and improves the predeclared objective, stage it and watch the same signals.

## Evidence and checklist

For each adopted change, keep the candidate configuration, baseline and candidate case sets, evaluation results, cost scope, completion-latency and TTFT distributions, and any failed or excluded runs. Note whether runs were warm or cold, how cached data was partitioned and invalidated, whether batch delay was counted, and how streaming was validated. This makes a claimed gain interpretable and helps catch regressions after prompts, models, sources, or tools change.

Before rollout, confirm that:

- [ ] The change targets a measured bottleneck and a declared success metric.
- [ ] Quality, safety, authorization, and tenant-isolation gates still hold.
- [ ] Failed attempts, retries, unknown costs, and human correction are visible in the comparison.
- [ ] TTFT and completed-task latency are reported separately, and streaming does not show unchecked content as final.
- [ ] Cache freshness, scope, invalidation, warm/cold behavior, and batch delay are understood.
- [ ] Runtime limits, retry bounds, rollback conditions, and monitoring are in place.

## References

[1]: https://developers.openai.com/api/docs/guides/latency-optimization "Latency optimization"
[2]: https://developers.openai.com/api/docs/guides/prompt-caching "Prompt caching"
[3]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching "Prompt caching"
[4]: https://developers.openai.com/api/docs/guides/batch "Batch API"

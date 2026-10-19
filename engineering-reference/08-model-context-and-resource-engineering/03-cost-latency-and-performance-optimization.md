# 8.3 Cost, Latency, and Performance Optimization

**Status:** 0.5.0 first draft
**Audience:** Developers, evaluators, and operators improving production agents
**Applicability:** Use this chapter when model or tool work is costly, task completion is too slow, or throughput and user effort matter. Every production agent still needs bounded execution and operational limits; this chapter guides optimization rather than requiring every technique.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md)

## Purpose and applicability

Optimization is not simply “make the model call faster.” An agent is a chain of context assembly, retrieval, model work, tool execution, validation, and sometimes human review. Saving time or tokens in one step can move work elsewhere, increase failure risk, or make the answer less useful. A sound optimization improves a defined outcome while preserving the quality, safety, and authority boundaries the agent must meet.

This chapter focuses on cost per verified success, failed-attempt cost, caching, batching, fewer calls, parallelism, streaming, and warm versus cold paths. Model choice and routing belong in [8.1](01-model-selection-parameters-and-routing.md); retrieval and context transformations belong in [8.2](02-retrieval-memory-and-context-optimization.md); shared admission and backpressure belong in [8.4](04-capacity-admission-control-and-backpressure.md). Define the metric population, denominator, baseline, target, and owner under [1.2](../../development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), then use Part 4 methods to produce comparable evidence.

## Working model

Measure the whole task, not only the model request. Record where meaningful time is spent: queueing, retrieval, model time, tool calls, orchestration, validation, and waits for people or external systems. Report **time to first token (TTFT)** separately from time to a complete, validated outcome. TTFT captures when a stream begins; it does not prove that the task finished sooner. [1] For tasks that require approval or human review, report the automated response path and the human-wait portion distinctly so that changing one does not conceal the other.

Likewise, a lower token price is not necessarily lower cost per success. A useful measure is attributable cost across successful and failed attempts divided by the number of independently verified successful outcomes. Define whether the numerator includes model and tool charges, retries, failed calls, infrastructure, and support effort. If people must correct or verify more answers, track that time as a separate measure rather than silently treating it as free. Failed attempts matter: a sequence of cheap attempts followed by an expensive fallback can cost more than a capable first choice.

Some cost and usage information arrives after a call completes or after billing is reconciled. Treat limits as brakes, not exact guarantees that the final charge cannot cross a threshold. Reconcile estimates with authoritative usage or billing data where available, and leave an unpriced or unknown amount unknown rather than recording zero.

## Decisions and best practices

Start with a baseline that describes a representative task population, its success definition, cost, completed-task latency, TTFT when relevant, and human effort. Examine distributions and important slices, not only averages. Identify the dominant delay or expense before changing anything. Then make one material change at a time, compare on the same cases and conditions, and keep the change only if it preserves required quality and safety gates while improving the metric that motivated it.

A practical order is to bound worst-case execution; eliminate unnecessary model calls and irrelevant context; constrain tool-result size; reuse stable computation where safe; select a capable model for each task; and then tune batching, concurrency, or retry behavior. This is a diagnostic sequence, not a universal ranking: the dominant cost in a particular workload may justify a different experiment. Set run limits in enforceable runtime controls, not in instructions to the model. Shared limits across workers require shared accounting rather than counters that disappear on restart. Retry policies at multiple layers multiply; calculate the maximum plausible combined attempts and prevent retries from repeating unsafe external effects. For resumable or side-effecting tasks, use the applicable requirements in [Part 7](../07-durable-execution-and-human-governed-work/README.md).

**Fewer calls and parallel work.** Combine steps only when one request can perform them without obscuring independent validation or increasing error consequences. Run independent work in parallel when dependencies allow it; parallelize only the work that is genuinely independent, cap fan-out, and consider shared capacity and rate limits. Parallel requests can reduce a critical path but do not eliminate their total cost, and can worsen queueing or overload a dependency. A sequential dependency cannot be made parallel merely by hiding it. Speculative work may reduce a common-path wait but wastes resources when the speculation is wrong; cancel it when possible and include cancelled work in cost accounting.

**Caching and batching.** Prompt-prefix caching can reuse computation for a repeated stable prefix, but matching rules, cache duration, prices, and supported controls depend on provider and model. Keep stable material before dynamic content where the chosen service benefits from prefix reuse, and observe reads, misses, writes, and resulting cost rather than assuming a hit. Long waits can outlast a cache entry; treat resumed work as cold unless observed behavior supports another assumption. Current provider documentation illustrates the provider-specific nature of prefix matching and lifetime [2] [3].

Application-level result caching is a separate choice. Reuse only results whose freshness and correctness can be established. Partition by tenant and authorization scope, bind entries to relevant model/settings, instruction and tool versions, normalized inputs, and source-data version, and expire or invalidate entries when policy or evidence changes. Do not reuse consequential actions, stale time-sensitive answers, or unvalidated outputs. Detailed context and source-freshness controls are covered in [8.2](02-retrieval-memory-and-context-optimization.md).

Batch independent, latency-tolerant work when its delay and result-handling model fit the use case—for example, offline evaluation or bulk classification. Do not route interactive requests through a batch merely to claim a unit-cost saving if completion latency violates the user need. Batch implementations can have their own completion windows, failure handling, and pricing; provider examples are not general guarantees [4]. For online micro-batching, include the waiting time to fill a batch in the end-to-end measurement.

**Streaming and warm/cold paths.** Streaming can make progress visible before the full response is ready, but first-token speed is not completed-task performance. If text needs citation, policy, privacy, or output validation before users may rely on it, buffer it or clearly treat streamed chunks as provisional until checks pass. Compare perceived responsiveness and task completion separately. Measure cache-warm and cache-cold paths, first-run and resumed work, and common versus fallback routes where they occur. Do not report a warm-only result as representative if users regularly experience cold starts.

## Requirements

- **PERF-01** When an agent has defined cost, latency, or performance objectives, its owner MUST specify the measured population, success denominator, measurement method, baseline, target or decision threshold, and accountable owner; cost per success MUST use verified successes and include attributable failed-attempt costs in the declared scope.
- **PERF-02** When an agent is deployed to production, its runtime MUST enforce applicable per-run limits for model requests, tool calls, and other declared resource bounds; a prompt or unshared in-memory counter MUST NOT be the sole enforcement mechanism.
- **PERF-03** When a proposed optimization changes model calls, context, caching, batching, parallelism, streaming, or retries, the release decision MUST compare the candidate with a baseline on relevant cases and MUST preserve applicable quality, safety, and authorization gates before the optimization is adopted.
- **PERF-04** When shared budgets span processes, workers, or resumptions, spend accounting MUST use a shared mechanism with defined reconciliation behavior; unknown or unpriced usage MUST remain unknown and MUST NOT be treated as zero.
- **PERF-05** When output is streamed before task completion, the interface MUST distinguish provisional content from a complete validated result wherever downstream checks are required before reliance; reported performance MUST distinguish TTFT from completed-task latency.
- **PERF-06** When caching or batching is used, the owner MUST define the applicable freshness, authorization/tenant partitioning, invalidation, and failure behavior; measurements MUST distinguish warm from cold paths when both materially occur, and batching MUST only be used where its completion delay fits the task requirement.

## Worked example

An internal policy assistant answers travel questions from approved, current, permission-filtered documents. It returns citations and uncertainty, has no external write capability, and may finish with `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. The fixture `travel-policy-current` is fictional test data: it permits a London hotel amount of GBP 220, while a superseded document differs. A citation must support the answer; the mere presence of a citation is not success.

Suppose the team suspects that repeated document context is driving both spend and delay. It first records the same held-out cases, user/tenant boundary, source versions, verified outcomes, full completion time, TTFT, token/tool usage, failed attempts, and any human correction. The team establishes baseline values from its own run; none are presumed by this example. It then tests two candidates independently: omit irrelevant retrieved passages while retaining the current and superseded-policy distinction, and reuse the stable instruction prefix where the serving model demonstrably supports it. It does not cache final answers across users or policy versions.

The candidate is accepted only if the same cases still return the permitted amount when supported, distinguish the superseded source, ask for clarification when required evidence is missing, and keep tenants isolated. The evaluator checks semantic support as well as citation presence. Cost is divided by verified successful outcomes and includes failed or corrected attempts in the declared accounting scope. End-to-end completion and TTFT are compared separately, with cache-warm and cache-cold runs reported separately. If the candidate starts streaming a number before validating its source, that text remains provisional and is not presented as a final answer.

If the optimization lowers the input-token count but increases unsupported answers or human correction, it is rejected even if the model call appears cheaper or its first token arrives sooner. If it preserves all gates and improves the predeclared objective, the team can stage the change and monitor the same signals. This is a decision rule, not a claim that either candidate produces a particular measured result.

## Evidence and checklist

For each adopted change, retain the candidate identity and configuration, baseline and candidate case set, evaluation results, cost-accounting scope, completion-latency and TTFT distributions where applicable, and any failed or excluded runs. Note whether each run was warm or cold, how cached data was partitioned and invalidated, whether batching delay was included, and how streaming validation worked. These records make a claimed gain interpretable and help detect regressions after prompts, models, sources, or tools change.

Before rollout, confirm that:

- [ ] The optimization targets a measured bottleneck and a declared success metric.
- [ ] Quality, safety, authorization, and relevant tenant-isolation gates remain satisfied.
- [ ] Failed attempts, retries, unknown costs, and human correction are not hidden from the comparison.
- [ ] TTFT and completed-task latency are reported separately; streaming does not expose unchecked content as final.
- [ ] Cache freshness, scope, invalidation, warm/cold behavior, and batch delay are understood for the selected implementation.
- [ ] Runtime limits, retry bounds, rollback conditions, and monitoring are in place.

## References

[1]: https://developers.openai.com/api/docs/guides/latency-optimization "Latency optimization"
[2]: https://developers.openai.com/api/docs/guides/prompt-caching "Prompt caching"
[3]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching "Prompt caching"
[4]: https://platform.openai.com/docs/guides/batch "Batch API"

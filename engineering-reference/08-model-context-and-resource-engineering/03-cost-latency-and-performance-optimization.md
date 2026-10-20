# 8.3 Cost, Latency, and Performance Optimization

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers and operators improving production agents
**Applicability:** Use when model or tool work is costly, tasks finish too slowly, or throughput and user effort matter. Every production agent still needs bounded execution and operational limits; this chapter guides optimization and does not require every technique.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md)

## Purpose and applicability

An agent chains context assembly, retrieval, model work, tools, validation and sometimes human review. Saving time or tokens in one step can shift work elsewhere, add risk or weaken the answer; a good optimization improves a defined outcome within quality, safety and authority boundaries.

Model routing is in [8.1](01-model-selection-parameters-and-routing.md), context changes in [8.2](02-retrieval-memory-and-context-optimization.md), and admission and backpressure in [8.4](04-capacity-admission-control-and-backpressure.md). Define population, denominator, baseline, target and owner under [1.2](../../development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), and gather comparable evidence with Part 4 methods.

## Working model

Measure the whole task: queueing, retrieval, model time, tool calls, orchestration, validation, and waits for people or outside systems. Report **time to first token (TTFT)** apart from time to a complete, validated outcome; streaming improves perceived latency, but TTFT only marks when output starts.[1] Report automated time and human waits separately so neither hides the other.

A lower token price is not a lower cost per success. Divide attributable cost across successful and failed attempts by independently verified successes, and state whether model and tool charges, retries, failed calls, infrastructure and support are included. Track extra human correction or checking as its own measure, not as free. Cheap attempts followed by an expensive fallback can cost more than a capable first choice; multi-agent designs cost more again ([9.1](../09-multi-agent-systems-and-interoperability/01-when-multiple-agents-help-topologies-and-system-contracts.md)).

Some usage data arrives only after a call ends or billing is reconciled, so limits are brakes, not guarantees that a final charge stays under a threshold. Reconcile estimates with authoritative usage data, and leave unpriced amounts unknown, not zero.

## Decisions and best practices

Baseline a representative population first: success definition, cost, completed-task latency, TTFT where relevant and human effort, as distributions and key slices, not just averages. Find the dominant delay or expense, change one thing at a time on the same cases and conditions, and keep a change only if it holds the quality and safety gates and improves the motivating metric.

A practical diagnostic order: bound worst-case execution; remove unneeded calls and irrelevant context; limit tool-result size; reuse stable computation where safe; pick a capable model per task; then tune batching, concurrency and retries. Your workload's biggest cost may call for a different first experiment. Cutting input tokens often gains little latency because output generation usually dominates: one provider's guide estimates that halving a prompt saves 1 to 5% of latency while halving output saves about 50%. Measure first.[1] Enforce run limits in runtime controls, not model instructions, with shared accounting across workers rather than counters lost on restart. Retries at several layers multiply, so compute the combined maximum and never let retries repeat unsafe external effects ([Part 7](../07-durable-execution-and-human-governed-work/README.md)).

**Fewer calls and parallel work.** Combine steps only when one request can do them without hiding independent validation or raising the cost of errors. Parallelize only truly independent work with capped fan-out and respect for shared rate limits; it shortens the critical path, not total cost, and can worsen queueing or overload a dependency. Speculative work cuts common-path waits but wastes resources when wrong; cancel it where possible and count it in cost.

**Caching and batching.** Prompt-prefix caching reuses computation for a repeated stable prefix; matching rules, lifetime, price and controls vary by provider and model.[2] [3] Put stable material (instructions, tool definitions, reference text) first, byte-for-byte identical and in fixed order, and avoid editing earlier context, since any change before the cache point forces a miss. Watch reads, misses, writes and cost rather than assume hits, and treat work resumed after a long wait as cold unless observed otherwise.

Application result caching is a separate choice. Reuse only results whose freshness and correctness you can establish; partition by tenant and authorization scope, bind entries to model, settings, instruction and tool versions, normalized inputs and source-data version, and expire them on policy or evidence changes. Never reuse consequential actions, stale time-sensitive answers or unvalidated output ([8.2](02-retrieval-memory-and-context-optimization.md)).

Batch independent, latency-tolerant work such as offline evaluation or bulk classification when the delay and result handling fit, not interactive requests for a unit-price saving. Batch services have their own completion windows, failure handling and pricing.[4] For online micro-batching, count the wait to fill a batch.

**Streaming and warm/cold paths.** First-token speed is not completion. Text needing citation, policy, privacy or output checks before reliance is buffered or shown as provisional until checks pass. Measure cache-warm and cold, first-run and resumed, and primary and fallback paths where they occur; warm-only results mislead if users often hit cold starts.

## Requirements

- **PERF-01** When an agent has defined cost, latency, or performance objectives, its owner MUST specify the measured population, success denominator, measurement method, baseline, target or decision threshold, and accountable owner; cost per success MUST use verified successes and include attributable failed-attempt costs in the declared scope.
- **PERF-02** When an agent is deployed to production, its runtime MUST enforce applicable per-run limits for model requests, tool calls, and other declared resource bounds; a prompt or unshared in-memory counter MUST NOT be the sole enforcement mechanism.
- **PERF-03** When a proposed optimization changes model calls, context, caching, batching, parallelism, streaming, or retries, the release decision MUST compare the candidate with a baseline on relevant cases and MUST preserve applicable quality, safety, and authorization gates before the optimization is adopted.
- **PERF-04** When shared budgets span processes, workers, or resumptions, spend accounting MUST use a shared mechanism with defined reconciliation behavior; unknown or unpriced usage MUST remain unknown and MUST NOT be treated as zero.
- **PERF-05** When output is streamed before task completion, the interface MUST distinguish provisional content from a complete validated result wherever downstream checks are required before reliance; reported performance MUST distinguish TTFT from completed-task latency.
- **PERF-06** When caching or batching is used, the owner MUST define the applicable freshness, authorization/tenant partitioning, invalidation, and failure behavior; measurements MUST distinguish warm from cold paths when both materially occur, and batching MUST only be used where its completion delay fits the task requirement.

## Worked example

The fictional read-only policy assistant answers travel questions from approved, current, permission-filtered documents with citations, ending `complete`, `needs_information`, `declined`, `failed` or a declared partial result. Fixture `travel-policy-current` allows GBP 220 for a London hotel; a superseded document differs. A citation must support the answer to count as success.

Suspecting repeated document context drives spend and delay, the team first records, on fixed held-out cases, tenant boundary and source versions, verified outcomes, completion time, TTFT, token and tool usage, failed attempts and human correction. It then tests two changes separately: dropping irrelevant passages while keeping the current-versus-superseded distinction, and reusing the stable instruction prefix where the model supports it. It does not cache final answers across users or policy versions.

A change is accepted only if cases still return the permitted amount when supported, flag the superseded source, ask when evidence is missing, and keep tenants isolated, with semantic support checked. Cost per verified success includes failed or corrected attempts; completion time, TTFT, and warm and cold runs are reported separately; a number streamed before its source is validated stays provisional. A change that cuts input tokens but raises unsupported answers or human correction is rejected however cheap or fast it looks; one that keeps all gates and improves the predeclared objective is staged and monitored.

## Evidence and checklist

For each adopted change, keep the configuration, baseline and candidate cases, results, cost scope, latency and TTFT distributions, failed or excluded runs, warm or cold status, cache partitioning, batch delay and streaming validation.

- [ ] The change targets a measured bottleneck and a declared metric.
- [ ] Failed attempts, retries, unknown costs and human correction are visible in the comparison.
- [ ] Rollback conditions and monitoring are in place.

## References

[1]: https://developers.openai.com/api/docs/guides/latency-optimization "Latency optimization"
[2]: https://developers.openai.com/api/docs/guides/prompt-caching "Prompt caching"
[3]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching "Prompt caching"
[4]: https://developers.openai.com/api/docs/guides/batch "Batch API"

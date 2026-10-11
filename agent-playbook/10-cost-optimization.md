# 10. Cost optimization

This chapter is for developers who need an agent to stay affordable under
real traffic. It covers the limits you must build in and the order in which
optimizations pay off. Optimize cost per successful, compliant outcome, not
token price in isolation: a cheap model that fails and retries costs more.

## Work in this order

Work through the controls in this order; the early ones are cheaper and
protect you while you tune the later ones:

1. Prevent runaway execution.
2. Remove unnecessary requests and context.
3. Bound tool output.
4. Improve prompt-cache effectiveness.
5. Route to the least expensive capable model.
6. Cache safe, repeatable results.
7. Tune retries and concurrency.
8. Consider provider or commercial changes.

## Budget hierarchy

Every production agent MUST have per-request and per-run limits. Shared
deployments SHOULD also have conversation, tenant, deployment, and
organization limits.

```yaml
budgets:
  run:
    max_model_requests: 8
    max_tool_calls: 12
    max_input_tokens: 30000
    max_output_tokens: 5000
    max_cost_usd: 0.50
  conversation:
    max_cost_usd: 3.00
  tenant_daily:
    warning_cost_usd: 50
    maximum_cost_usd: 75
```

- **Enforce run limits in the agent runtime.** Request, tool, token, and cost
  limits for a run belong in the runtime, not in the prompt.
- **Keep shared budgets in a durable store.** Budgets that span runs or
  workers need a shared, durable spend store. In-memory counters are not
  enough for a production worker fleet or for a durable workflow that may
  resume on another worker.
- **Treat spend limits as a brake, not a guarantee.** Cost and token counts
  may be known only after a response, so the request that crosses a threshold
  may still be billed. Reconcile with provider billing.
- **Never record unknown cost as zero.** Unknown cost MUST remain unknown.
  Hard USD budgets SHOULD reject unpriced models unless an approved custom
  price is supplied.

## Model routing

Resolve versioned policies such as `fast-v1`, `balanced-v1`, and
`reasoning-v1`. Routing weighs modalities, structured-output and tool
reliability, context size, risk, complexity, latency, cost, residency, and
availability.

Best practices:

- **Escalate on explicit signals only.** Move to a more capable model on
  failed validation, verified complexity, low confidence, or a high-risk
  decision. The runtime constrains which routes are available and the total
  budget.
- **Count the cost of failure.** Compare the total cost of failed attempts
  plus escalation. Blindly trying models in sequence can cost more than
  starting with the right one.

## Context

Context grows quietly. Keep it lean:

- Keep stable instructions concise.
- Move specialized procedure into deferred skills.
- Expose only relevant tools and skills.
- Retrieve only needed evidence.
- Return compact, typed tool results.
- Set cumulative and per-request context limits.
- Compact or externalize history before you reach model limits.
- Preserve safety, authorization, approval, evidence, and side-effect state
  through any compaction.

Summarizing compaction has its own model cost and can lose information, so it
needs eval coverage. Prefer deterministic trimming when it preserves the
context you need.

## Tool output and catalog size

Tools
MUST support appropriate filtering, pagination, field selection, result-count
limits, and byte limits. Prefer a compact summary plus a stable reference over
a raw payload. When results are large:

- truncate only when the loss is acceptable;
- spill to approved storage when lossless access is required; and
- summarize only when you have measured a quality and cost benefit.

The catalog costs tokens too: every exposed tool contributes schema tokens and
every skill contributes catalog tokens. Production agents MUST use explicit
allowlists. Rare tools SHOULD use deferred discovery when practical. Keep
operational spend data in the user interface rather than in a model-visible
tool unless the agent must reason about it.

## Prompt caching

Keep the cacheable prefix stable, ordered from most to least stable:

```text
tool schemas
system instructions
stable policy
conversation history
dynamic user content
```

Do not inject timestamps, random IDs, request metadata, nondeterministically
ordered tools, or frequently changing flags into the stable prefix. Track
cache reads, writes, hit ratio, savings, and cache-bust warnings so you notice
when a change breaks caching.

Long durable-workflow waits may outlive a provider cache. Estimates for a
resumed workflow SHOULD assume a cache miss unless you have observed
otherwise.

## Application caching

Cache only safe, repeatable outputs. Keys SHOULD include agent,
model, settings, instruction and skill hashes, tool schema, normalized input,
authorization scope, tenant partition, and source-data version.

Do not cache consequential execution, poorly versioned authorization
decisions, cross-tenant sensitive data, stale time-sensitive answers, or
unvalidated output.

## Retry economics

Retry layers multiply. Calculate the upper bound:

```text
output-correction attempts
× durable-step attempts
× provider transport attempts
× model fallbacks
```

Under durable execution the default is bounded output-correction retries,
bounded durable-step retries, disabled provider transport retries, a limited
set of fallback candidates, and idempotent side effects.

## Durable-workflow economics

- Resume partial progress rather than restarting prompts.
- Count ambiguous timeouts as potentially billable.
- Use a shared durable spend store.
- Keep large artifacts outside workflow history.
- Continue as a new run when histories grow long.
- Expect prompt-cache expiry during long approval waits.
- Make spend-event consumers idempotent.

## How to optimize

Treat optimization as an experiment: baseline, identify the dominant cost,
change one major variable, run
[multi-run](06-evaluation.md#multi-run-evaluation) quality, safety, latency,
and cost evals, roll out gradually, and monitor quality-adjusted cost. Roll
back when a hard gate or an approved quality threshold regresses.

## Common pitfalls

- **Counting spend in memory.** Limits reset when a worker restarts or a
  workflow resumes elsewhere.
- **Breaking the cache by accident.** A timestamp in the system prompt can
  silently disable prompt caching.
- **Stacking retries.** Several modest retry policies multiply into a large
  worst case.

## Before you move on

- [ ] Run-level request, tool, token, and cost limits are enforced in the
  runtime.
- [ ] Budgets shared across runs or workers use a durable spend store.
- [ ] Unknown cost stays unknown, and unpriced models are handled explicitly.
- [ ] We measure cost per successful, compliant outcome.

# 8.1 Model Selection, Parameters, and Routing

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers choosing or operating models in an agent
**Applicability:** Agents that call one or more models. Selection and evaluation guidance applies whenever you choose or change a model, provider, deployment, or behavior-affecting setting. Routing and fallback guidance applies only when a run can use more than one approved candidate. A single-model agent does not need a routing layer.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md) · [Next: 8.2 Retrieval, Memory, and Context Optimization](02-retrieval-memory-and-context-optimization.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md)

## Purpose and applicability

Model choice is a design decision for this agent, not a place on a leaderboard. A newer model or a higher reasoning setting is not automatically safer or better.

This chapter covers selection, model parameters, routing, and fallback. Outcomes and budgets are defined in [2.2 Agent Contracts and Configuration](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). Part 4 explains how to build the evaluation evidence used here. 8.3 covers wider cost and performance work.

## Working model

A **model policy** states which logical model role an agent may use and under what constraints, for example a default candidate plus an optional stronger one for a narrow escalation path. At runtime, policy resolution picks a specific provider, model or snapshot, deployment, settings, and price record. Keep the policy stable and reviewable, but record the resolved configuration for every evaluation and run, so behavior is tied to the actual candidate and not to a label.

Judge candidates on more than quality: failure behavior, modalities, context and output limits, structured output, tool use, latency, availability, price, data handling, residency, and the deployment boundary. Two routes to a similarly named model can differ in terms, controls, and availability, so confirm these for the service you call.

Parameters belong to a particular model API; they are not universal knobs. Sampling settings such as temperature or nucleus sampling change how the next token is picked, but ranges, defaults, and interactions differ. Reasoning or effort controls change how much work the model does. They are not sampling controls, and similar labels do not mean equal behavior across models. Providers' documentation shows the variation: supported values and defaults differ by model, and a model may reject or ignore an unsupported setting. [1] [5] Some current models return an error for any non-default temperature or top-p, or for setting both, and a manual thinking budget is legacy on newer models in favor of effort controls. [3] [4]

Output limits cap generation, but the count can include more than visible text. Some models count reasoning tokens against the output limit, and the context size, maximum output, and truncation behavior are model-specific. An incomplete response is not a valid answer just because it parses. Check the completion status and validate the content against the output contract before use. [1] [6]

## Decisions and best practices

**Start from task evidence, not a ranking.** Use the agent's cases, expected outcomes, and hard gates to compare the current or a simpler candidate with plausible alternatives. Include ordinary cases and ones that expose limits: ambiguity, missing or conflicting evidence, long inputs, structured outputs, tool failures, refusal. Test the exact model version, deployment, and settings you will ship. A model change is a behavior change, so version it and re-run targeted evaluations even if the application is untouched. Pinning a dated snapshot makes this practical. [2]

**Apply hard constraints first.** A candidate that fails a required privacy, residency, modality, context, output, tool, or authorization boundary is not rescued by a higher average score. Among eligible candidates, compare task outcomes, then latency, availability, and total cost. Count failed attempts, repeated inference, validation failures, and escalation; a low unit price is a false economy if tasks often need a second call. An untested model or setting earns no credit for reducing risk.

**Treat each parameter as a hypothesis.** Write down the intended effect (less variation, more thorough problem-solving, no overlong output), then test it on representative cases. Start from documented defaults or a documented model-specific configuration, and change one consequential setting at a time where practical. Do not publish a universal temperature, and do not translate one provider's reasoning level into another's token budget. If a setting is unsupported or silently ignored, the real configuration differs from the one you intended, so verify resolved settings and response status.

**Set an output ceiling with room for the full result**, within the model's documented limits and the run's enforced budget. Use validation to tell a complete result from truncation, refusal, malformed structure, or an unfinished tool interaction. When a response is cut short, return the contract's bounded failure or partial outcome, or use a recovery path you have evaluated. A model's proposed output length or reasoning level must not raise a runtime budget.

**Keep routing small and declared.** Route on signals the runtime can verify: a known input modality, a validated complexity category, a failed schema check, or an explicit availability error. A model's unsupported claim about its own confidence does not show that another route will do better. Learned routers between a strong and a weak model can cut cost without losing quality on some benchmarks, but test any router on your own cases, not on a published claim. [7] Bound the attempts, the candidate set, and total latency and spend, and define the outcome when no candidate succeeds. Count every attempt against request and cost budgets, because an escalation can raise cost without improving the result.

**Fall back only to a pre-approved candidate** that can meet the same task contract and data-handling limits. Fallback must not bypass a prohibited-use rule, weaken authorization, change the tenant or permitted source scope, or quietly lower the execution class or governance controls. A transient availability failure can justify a compatible fallback. Missing evidence or an unresolved policy conflict calls for `needs_information` or escalation, not another model asked to guess. Record which candidate ran and why, so incidents and comparisons can tell primary from fallback behavior.

## Requirements

- **MODEL-01** — When selecting or changing a model, provider, deployment, or behavior-affecting model setting for a production agent, the owner MUST evaluate the intended candidate on representative task cases and applicable hard gates before release; a change MUST NOT be accepted solely on a general ranking or vendor claim.
- **MODEL-02** — When an agent resolves a logical model policy at runtime or for evaluation, the owner MUST version that policy and MUST record the resolved provider, exact model or snapshot, deployment where relevant, effective settings, and applicable pricing identity with evaluation evidence and operational attribution.
- **MODEL-03** — When a model-specific parameter is configured, the owner MUST verify that the selected model supports the setting and MUST evaluate its effect on relevant behavior; the configuration MUST NOT assume that a parameter name, default, value, or reasoning control has equivalent semantics across models.
- **MODEL-04** — When generated output is subject to a token or length limit, the runtime MUST enforce an applicable limit, detect incomplete or truncated responses where the service exposes that status, and validate output before downstream use; it MUST return a declared bounded outcome when the required result is incomplete or invalid.
- **MODEL-05** — When routing or fallback can select among candidates, the owner MUST define an allowlisted candidate set, observable selection signals, bounded attempts and resource limits, and a terminal outcome; the runtime MUST reject a route that violates the task contract, data-handling constraints, authorization, or required execution class.
- **MODEL-06** — When a route escalates or falls back after an unsuccessful attempt, the agent MUST account for the full attempt sequence in its request, latency, and cost limits, and MUST record the selected route and reason. A fallback MUST NOT treat missing, conflicting, or unauthorized evidence as evidence that a different model may safely guess.

## Worked example: fictional policy assistant

The shared fictional policy assistant answers from approved, current, permission-filtered documents, returns citations and uncertainty, and cannot write externally. Its outcomes are `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. In the fictional `travel-policy-current` fixture the current approved policy allows GBP 220 for a London hotel and a superseded document differs. All of this is test data.

The team runs the same versioned cases on a baseline model and a second candidate: a straightforward question, a superseded document, an unresolved conflict, missing evidence, permission denial, a long response, and a schema failure. It checks source choice, claim support, uncertainty handling, output validity, and each candidate's latency and total attempted cost under the run limits.

Suppose the baseline wins for ordinary questions. The team allows one escalation to the second candidate, only when a deterministic check finds the retrieved approved sources conflict or the answer fails output validation, and only if the input stays inside the same source and privacy boundary. The second model may help interpret evidence already permitted. It cannot decide which conflicting policy is authoritative when the evidence and precedence rule do not say. If the conflict stays unresolved, the assistant returns `needs_information` and does not pick GBP 220 or the older amount by guess.

For each evaluation and run, the record captures the provider, model version, deployment, effective parameters, and price identity. The runtime enforces one model-request and cost budget across both attempts. If the second call is unavailable, over the limit, truncated, or still invalid, the assistant returns its bounded outcome and makes no further calls.

## Evidence and checklist

A decision record names the candidate configuration and policy version, the cases and evaluators, hard-gate results, constraints checked, and why each candidate was chosen or rejected. For routing, keep the signal that triggered a route, the candidate selected, the attempt count, the bounded outcome, and enough usage data to price the full path. Keep only as much prompt and output content as privacy policy allows.

Before release or a material model-policy change, check that:

- The chosen candidate meets capability, privacy, residency, availability, and output constraints.
- Evaluation used representative and adverse cases, and the evaluated identity matches the deployment and effective settings.
- Each parameter has a stated purpose and a tested effect; ignored settings are not mistaken for active controls.
- The runtime can tell valid completion from invalid, refused, truncated, or incomplete results.
- Any route or fallback has observable triggers, an approved candidate set, and whole-run bounds on attempts, latency, and cost.
- Fallback keeps evidence, access, authorization, execution-class, and governance requirements, with a bounded outcome if no candidate can finish.
- Model and routing changes are versioned and linked to evaluation evidence and run attribution.

## References

[1]: https://developers.openai.com/api/docs/guides/reasoning "Reasoning models"
[2]: https://developers.openai.com/api/docs/guides/text-generation "Text generation"
[3]: https://platform.claude.com/docs/en/build-with-claude/extended-thinking "Extended thinking"
[4]: https://platform.claude.com/docs/en/build-with-claude/thinking "Thinking"
[5]: https://ai.google.dev/api/generate-content "Generate content API"
[6]: https://ai.google.dev/gemini-api/docs/thinking "Thinking"
[7]: https://arxiv.org/abs/2406.18665 "RouteLLM: Learning to Route LLMs with Preference Data"

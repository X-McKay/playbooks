# 8.1 Model Selection, Parameters, and Routing

**Status:** 0.5.0-draft.2 — draft
**Audience:** Developers choosing or operating models in an agent
**Applicability:** Agents that call one or more models. Selection and evaluation guidance applies whenever you choose or change a model, provider, deployment, or behavior-affecting setting. Routing and fallback guidance applies only when a run can use more than one approved candidate; a single-model agent needs no routing layer.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md) · [Next: 8.2 Retrieval, Memory, and Context Optimization](02-retrieval-memory-and-context-optimization.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md)

## Purpose and applicability

Model choice is a design decision for this agent, not a leaderboard position; a newer model or higher reasoning setting is not automatically safer or better. This chapter covers selection, parameters, routing and fallback. Outcomes and budgets are in [2.2](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md), evaluation method in Part 4, and wider cost work in 8.3.

## Working model

A **model policy** states which logical model role an agent may use and under what constraints, such as a default candidate plus a stronger one for a narrow escalation path. At runtime, resolution picks a provider, model or snapshot, deployment, settings and price record. Keep the policy stable and reviewable, and record the resolved configuration for every evaluation and run so behavior ties to the actual candidate, not a label.

Judge candidates on more than quality: failure behavior, modalities, context and output limits, structured output, tool use, latency, availability, price, data handling, residency and deployment boundary. Two routes to a similarly named model can differ in terms, controls and availability.

Parameters belong to a model API, not a universal dial. Sampling settings such as temperature or nucleus sampling change token choice, with differing ranges, defaults and interactions. Reasoning or effort controls change how much work the model does; they are not sampling controls, and similar labels do not mean equal behavior. Supported values and defaults vary by model, and unsupported settings may be rejected or ignored.[1] [5] Some current models error on any non-default temperature or top-p, or on setting both, and newer models treat a manual thinking budget as legacy in favor of effort controls.[3] [4]

Output limits can count more than visible text: some models count reasoning tokens, and context size, maximum output and truncation are model-specific. A response that parses is not valid if incomplete; check completion status and validate against the output contract.[1] [6]

## Decisions and best practices

**Start from task evidence, not a ranking.** Compare the current or a simpler candidate with alternatives on the agent's cases, outcomes and hard gates, including ambiguity, missing or conflicting evidence, long inputs, structured output, tool failures and refusal. Test the exact version, deployment and settings you ship. A model change is a behavior change: version it and re-run targeted evaluations even if the application is untouched; pinning a dated snapshot makes this practical.[2]

**Apply hard constraints first.** A higher average score does not rescue a candidate that fails a privacy, residency, modality, context, output, tool or authorization boundary. Among eligible candidates compare outcomes, then latency, availability and total cost, counting failed attempts, repeats, validation failures and escalation; a low unit price is false economy if tasks often need a second call. Untested options earn no risk-reduction credit.

**Treat each parameter as a hypothesis.** State the intended effect (less variation, more thorough reasoning, no overlong output) and test it. Start from documented defaults or model-specific configurations and change one consequential setting at a time where practical. Do not publish a universal temperature or translate one provider's reasoning level into another's token budget. Verify resolved settings and response status, since an ignored setting means the real configuration differs from the intended one.

**Leave room for the full result** within the model's limits and the run's budget. Validation separates completion from truncation, refusal, malformed structure or unfinished tool interaction; a cut-off response gets the contract's bounded failure or partial outcome or an evaluated recovery path. A model's proposed length or reasoning level cannot raise a runtime budget.

**Keep routing small and declared.** Route on signals the runtime can verify: a known modality, a validated complexity category, a failed schema check or an explicit availability error, not a model's unsupported claim about its own confidence. Learned strong-weak routers cut cost without losing quality on some benchmarks, but test any router on your own cases.[7] Bound attempts, candidates, total latency and spend, define the outcome when nothing succeeds, and count every attempt against budgets.

**Fall back only to a pre-approved candidate** that meets the same task contract and data-handling limits. Fallback must not bypass a prohibited-use rule, weaken authorization, change tenant or source scope, or lower the execution class or governance controls. A transient availability failure can justify a compatible fallback; missing evidence or an unresolved policy conflict calls for `needs_information` or escalation, not another model asked to guess. Record which candidate ran and why.

## Requirements

- **MODEL-01** — When selecting or changing a model, provider, deployment, or behavior-affecting model setting for a production agent, the owner MUST evaluate the intended candidate on representative task cases and applicable hard gates before release; a change MUST NOT be accepted solely on a general ranking or vendor claim.
- **MODEL-02** — When an agent resolves a logical model policy at runtime or for evaluation, the owner MUST version that policy and MUST record the resolved provider, exact model or snapshot, deployment where relevant, effective settings, and applicable pricing identity with evaluation evidence and operational attribution.
- **MODEL-03** — When a model-specific parameter is configured, the owner MUST verify that the selected model supports the setting and MUST evaluate its effect on relevant behavior; the configuration MUST NOT assume that a parameter name, default, value, or reasoning control has equivalent semantics across models.
- **MODEL-04** — When generated output is subject to a token or length limit, the runtime MUST enforce an applicable limit, detect incomplete or truncated responses where the service exposes that status, and validate output before downstream use; it MUST return a declared bounded outcome when the required result is incomplete or invalid.
- **MODEL-05** — When routing or fallback can select among candidates, the owner MUST define an allowlisted candidate set, observable selection signals, bounded attempts and resource limits, and a terminal outcome; the runtime MUST reject a route that violates the task contract, data-handling constraints, authorization, or required execution class.
- **MODEL-06** — When a route escalates or falls back after an unsuccessful attempt, the agent MUST account for the full attempt sequence in its request, latency, and cost limits, and MUST record the selected route and reason. A fallback MUST NOT treat missing, conflicting, or unauthorized evidence as evidence that a different model may safely guess.

## Worked example: fictional policy assistant

The fictional read-only policy assistant answers from approved, current, permission-filtered documents with citations and uncertainty, ending `complete`, `needs_information`, `declined`, `failed` or a declared partial result. In the `travel-policy-current` fixture, the current policy allows GBP 220 for a London hotel and a superseded document differs.

The team runs the same versioned cases on a baseline and a second candidate: a straightforward question, a superseded document, an unresolved conflict, missing evidence, permission denial, a long response and a schema failure. It checks source choice, claim support, uncertainty, output validity, latency and total attempted cost.

The baseline wins on ordinary questions, so the team allows one escalation to the second candidate, only when a deterministic check finds approved sources conflict or the answer fails validation, and only inside the same source and privacy boundary. The second model may help interpret permitted evidence but cannot decide which conflicting policy governs when evidence and precedence rules do not say; an unresolved conflict returns `needs_information`, not a guessed amount.

Each run records provider, version, deployment, effective parameters and price identity. One request and cost budget spans both attempts; if the second call is unavailable, over limit, truncated or invalid, the assistant returns its bounded outcome and stops.

## Evidence and checklist

The decision record names the configuration and policy version, cases and evaluators, hard-gate and constraint results, and why each candidate was chosen or rejected. For routing, keep the trigger signal, selected candidate, attempt count, outcome and enough usage data to price the full path, retaining prompt and output content only as privacy policy allows.

Before release or a material model-policy change:

- The evaluated identity matches the deployment and effective settings.
- Each parameter has a stated purpose and tested effect; ignored settings are not mistaken for controls.
- Fallback keeps evidence, access, authorization, execution-class and governance requirements.

## References

[1]: https://developers.openai.com/api/docs/guides/reasoning "Reasoning models"
[2]: https://developers.openai.com/api/docs/guides/text-generation "Text generation"
[3]: https://platform.claude.com/docs/en/build-with-claude/extended-thinking "Extended thinking"
[4]: https://platform.claude.com/docs/en/build-with-claude/thinking "Thinking"
[5]: https://ai.google.dev/api/generate-content "Generate content API"
[6]: https://ai.google.dev/gemini-api/docs/thinking "Thinking"
[7]: https://arxiv.org/abs/2406.18665 "RouteLLM: Learning to Route LLMs with Preference Data"

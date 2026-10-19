# 8.1 Model Selection, Parameters, and Routing

**Status:** 0.5.0 first draft
**Audience:** Developers and reviewers choosing or operating models in an agent
**Applicability:** Applies to agents that call one or more models. Use the selection and evaluation guidance whenever choosing or changing a model, provider, deployment, or behavior-affecting setting. Routing and fallback guidance applies only when a run can use more than one approved candidate. A single-model agent does not need a routing layer.

[Part 8 — Model, Context, and Resource Engineering](README.md) · [Playbook home](../../README.md) · [Applicability and conformance](../../applicability.md) · [Next: 8.2 Retrieval, Memory, and Context Optimization](02-retrieval-memory-and-context-optimization.md) · [8.3 Cost, Latency, and Performance Optimization](03-cost-latency-and-performance-optimization.md)

## Purpose and applicability

Model choice is a system design decision, not a permanent leaderboard ranking. The model must handle the tasks, inputs, output contract, tools, and constraints that matter for this agent. A model that is capable in a general sense may still be unsuitable for a particular task, deployment boundary, or budget. A newer model or a higher reasoning setting is not automatically a safer or more effective choice.

This chapter covers selection, model-facing parameters, routing, and fallback. It does not define the agent's outcomes or budgets; see [2.2 Agent Contracts and Configuration](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). Part 4 explains how to construct the evaluation evidence that supports these decisions. Part 8.3 covers broader cost and performance optimization.

## Working model

A **model policy** states which logical model role an agent may use and under what constraints. For example, a policy may name a default candidate and an optional higher-capability candidate for a narrow escalation path. At runtime, policy resolution selects a specific provider, model or snapshot, deployment, settings, and applicable price record. Keep the policy stable and reviewable, but record the resolved configuration for each evaluation and operational run. This makes an observed behavior attributable to the actual candidate rather than to an ambiguous label.

Candidate fitness is multidimensional. Evaluate task quality and failure behavior alongside input modalities, context and output limits, structured-output behavior, tool interaction, latency, availability, price, data handling, residency, and the provider or deployment boundary. A deployment may have different terms, controls, capabilities, or availability from another route to a similarly named model. Confirm the properties that apply to the actual service boundary; do not infer them from a model name.

Parameters are controls exposed by a particular model API, not universal knobs. Sampling settings such as temperature or nucleus sampling affect how the next output is selected, but accepted ranges, defaults, and interactions differ. Reasoning or effort controls, where offered, influence a model's allocation of work; they are not interchangeable with sampling controls, and equal-looking labels do not imply equivalent behavior across models. Official provider documentation illustrates this variation: supported values and defaults can differ by model, and settings may be rejected or ignored when a model does not support them. [1] [3] [4] [5]

Output limits bound generation, but the token accounting may include more than user-visible text. Some models count reasoning tokens within the output limit; the available context, maximum output, and truncation behavior are model-specific. An incomplete response is not a valid answer merely because it parses. Check the completion status and validate the returned content against the declared output contract before using it. [1] [2] [6]

## Decisions and best practices

Begin with the task evidence, not a model ranking. Use the cases, expected outcomes, and hard gates defined for the agent to compare a simpler or current candidate with plausible alternatives. Include ordinary cases and cases that expose relevant limits: ambiguous requests, missing or conflicting evidence, long inputs, structured outputs, tool failures, and refusal or uncertainty behavior. Evaluate the exact model version, deployment, and settings intended for use. A model change is a behavior change and can warrant versioning and targeted re-evaluation even when the surrounding application is unchanged. [2]

Select only candidates that satisfy the non-negotiable constraints first. A candidate that cannot meet a required privacy, residency, modality, context, output, tool, or authorization boundary is not rescued by a higher average score. Among eligible candidates, compare outcomes relevant to the task, then consider latency, availability, and total cost. Include the cost of failed attempts, repeated inference, validation failures, and escalation; a low unit price can be a false economy if the task often needs another call. Do not give risk-reduction credit to an untested model or setting.

Treat each parameter as a hypothesis to test. Record the intended effect—such as reducing variation, encouraging more complete problem-solving, or preventing overlong output—then use representative cases to determine whether the setting produces the intended result without harming required behavior. Start from the documented supported defaults or a documented model-specific configuration. Change one consequential setting at a time when practical. Do not publish a universal temperature value, or translate one provider's reasoning level into another provider's token budget as if they were equivalent. If a parameter is unsupported or silently ignored, the effective configuration is not the one you intended; verify resolved settings and response status.

Set an output ceiling with enough room for the required result, while respecting the model's documented limits and the run's enforced budget. Use output validation to distinguish a complete result from truncation, refusal, malformed structure, or an incomplete tool interaction. When a response is cut short, return the contract's bounded failure or partial outcome, or use an explicitly evaluated recovery path. Do not let a model's proposed output length or reasoning setting expand a runtime budget.

Routing should be a small, declared decision policy rather than an open-ended search for a model that will say “yes.” Route using observable, task-relevant signals that the runtime can verify: for example, a known input modality, a validated complexity category, a failed schema check, or an explicit service-availability error. A model's unsupported claim about its own confidence is not proof that a different route will improve the answer. Bound the number of attempts, candidate set, total latency and spend, and define the terminal outcome when no candidate succeeds. Count all attempts when enforcing request and cost budgets; an escalation can increase cost without producing a better result.

Fallback is appropriate only to a pre-approved candidate that can satisfy the same task contract and data-handling constraints. It must not bypass a prohibited-use rule, weaken authorization, change the tenant or permitted source scope, or silently downgrade the required execution class or governance controls. A transient availability failure may justify a compatible fallback; missing evidence or an unresolved policy conflict generally calls for `needs_information` or escalation, not another model asked to guess. Record which candidate was used and why, so comparisons and incidents can distinguish the primary path from fallback behavior.

## Requirements

- **MODEL-01** — When selecting or changing a model, provider, deployment, or behavior-affecting model setting for a production agent, the owner MUST evaluate the intended candidate on representative task cases and applicable hard gates before release; a change MUST NOT be accepted solely on a general ranking or vendor claim.
- **MODEL-02** — When an agent resolves a logical model policy at runtime or for evaluation, the owner MUST version that policy and MUST record the resolved provider, exact model or snapshot, deployment where relevant, effective settings, and applicable pricing identity with evaluation evidence and operational attribution.
- **MODEL-03** — When a model-specific parameter is configured, the owner MUST verify that the selected model supports the setting and MUST evaluate its effect on relevant behavior; the configuration MUST NOT assume that a parameter name, default, value, or reasoning control has equivalent semantics across models.
- **MODEL-04** — When generated output is subject to a token or length limit, the runtime MUST enforce an applicable limit, detect incomplete or truncated responses where the service exposes that status, and validate output before downstream use; it MUST return a declared bounded outcome when the required result is incomplete or invalid.
- **MODEL-05** — When routing or fallback can select among candidates, the owner MUST define an allowlisted candidate set, observable selection signals, bounded attempts and resource limits, and a terminal outcome; the runtime MUST reject a route that violates the task contract, data-handling constraints, authorization, or required execution class.
- **MODEL-06** — When a route escalates or falls back after an unsuccessful attempt, the agent MUST account for the full attempt sequence in its request, latency, and cost limits, and MUST record the selected route and reason. A fallback MUST NOT treat missing, conflicting, or unauthorized evidence as evidence that a different model may safely guess.

## Worked example: fictional policy assistant

Consider the shared fictional internal policy assistant. It answers from approved, current, permission-filtered documents, returns citations and uncertainty, and has no external write capability. Its outcomes are `complete`, `needs_information`, `declined`, `failed`, or a declared bounded partial result. In the fictional `travel-policy-current` fixture, the current approved policy permits a London hotel amount of GBP 220 while a superseded document differs. These are test data, not actual policy.

The team considers a baseline model and a second candidate. It does not assume either candidate is better from its label. It runs the same versioned cases against both, including a straightforward question, a superseded document, an unresolved conflict, missing current evidence, permission denial, a long response, and a schema-validation failure. The comparison checks whether the correct current source was used, whether the answer's claims are supported, whether uncertainty is handled correctly, and whether the output remains valid and complete. It also checks each candidate's latency and total attempted cost under the declared run limits. No performance result is assumed in advance.

Suppose evaluation supports using the baseline candidate for ordinary questions, but the team wants a bounded escalation when an external, deterministic check detects that the retrieved approved sources conflict or the answer fails its required output validation. The policy permits one escalation to the second, evaluated candidate only when the input remains within the same approved source and privacy boundary. The second model may help interpret already-permitted evidence; it cannot decide which conflicting policy is authoritative if the evidence and precedence rule do not establish that. If the conflict remains unresolved, the assistant returns `needs_information` rather than choosing GBP 220 or the superseded amount by guesswork.

The model policy names the logical route and the reviewed candidates. For each evaluation and run, the record captures the actual provider, model/version, deployment, effective parameters, and price identity. The runtime enforces the total model-request and cost budget across both attempts. If the second call is unavailable, exceeds the limit, returns truncated content, or still fails validation, the assistant returns its declared bounded outcome; it does not silently make more calls. The example illustrates a routing design to evaluate, not a claim that a second model improves policy answers.

## Evidence and checklist

A decision record should identify the candidate configuration and policy version, cases and evaluators used, hard-gate results, constraints checked, and the reason for selecting or rejecting each candidate. For routing, retain the signal that caused a route, candidate selected, attempt count, bounded outcome, and enough usage data to evaluate the cost of the full path. Keep evidence proportionate to the privacy policy; do not retain sensitive prompts or outputs merely to make model comparisons convenient.

Before release or a material model-policy change, check that:

- The selected candidate meets applicable capability, privacy, residency, availability, and output constraints.
- The evaluation uses representative and adverse cases, and the evaluated identity matches the intended deployment and effective settings.
- Parameter choices have a stated purpose and tested effect; unsupported or ignored settings are not mistaken for active controls.
- The runtime can distinguish valid completion from invalid, refused, truncated, or incomplete results.
- Any route or fallback has observable triggers, an approved candidate set, and enforced whole-run attempt, latency, and cost bounds.
- A fallback preserves evidence, access, authorization, execution-class, and governance requirements, with a bounded outcome if no candidate can complete the task.
- Model and routing changes are versioned and linked to evaluation evidence and operational attribution.

## References

[1]: https://developers.openai.com/api/docs/guides/reasoning "Reasoning models"
[2]: https://developers.openai.com/api/docs/guides/text-generation "Text generation"
[3]: https://platform.claude.com/docs/en/build-with-claude/extended-thinking "Extended thinking"
[4]: https://platform.claude.com/docs/en/build-with-claude/thinking "Thinking"
[5]: https://ai.google.dev/api/generate-content "Generate content API"
[6]: https://ai.google.dev/gemini-api/docs/thinking "Thinking"

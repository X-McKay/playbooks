# 1.3 Agent Suitability and Alternatives

**Status:** 0.5.0-draft.2 — draft

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent, and any planning decision that compares an agent with a simpler way to meet the same bounded user task. Using a model, having several steps, or varied wording does not make a task agent-suitable.

**Reader question:** Which approach fits this task and its constraints, what simpler baseline is credible, and what evidence could justify the added adaptability of an agent?

[Part 1 — Problem Definition and Planning](README.md) · [1.1 Defining the Problem](01-defining-the-problem.md) · [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) · [Playbook applicability](../../applicability.md)

## Decide the fit before designing the agent

An agent is one possible contribution to a user task, not the default answer. It adds flexibility where language, evidence or the order of work is uncertain, at a cost in money, latency, failure paths, evaluation and maintenance. Process redesign, human help, search, rules, automation, a learned predictor, one model response, or a fixed model workflow may be better.

Start with the simplest solution that could work: a single model call or fixed workflow, moving to an agent, then to several agents, only when simpler options demonstrably fall short. [2] NIST frames the decision to commission or deploy AI as contextual: weigh trustworthiness, risks, impacts, costs and benefits instead of treating a technology label as a benefit. [1]

## Terms and an operational convention

A **baseline** is the simplest plausible alternative for the same bounded task, chosen for a fair comparison: the current manual process, an improved process, or a simpler system. It can be kept because it is good enough.

An **action space** is the set of actions a candidate may take, from response-only to information-gathering or externally visible actions. Its size alone does not make a candidate an agent; consequence and authority are assessed in 1.4 and the control chapters.

In this guide, a **fixed workflow** has transitions defined by the orchestration. It may branch on an earlier result, retry, use a model router, or call a model at a set step, and stays fixed while the possible transitions and their selection are predefined. An **adaptive agent** lets model output direct a meaningful next action, sequence or stopping choice in response to observations. The action set can be finite and fully listed; adaptivity is about model-directed choice within it. This is a working convention; a practitioner source draws a similar line between predefined workflow paths and systems where a model directs its own process and tool use. [2]

An **adaptation benefit** is the task-relevant gain expected from model-directed choice, such as finding the next useful permitted source, asking a good follow-up question, or stopping when evidence is enough. It is a hypothesis until compared with a simpler design. **Evaluation burden** is the work to test it and the new failure paths; **maintenance burden** is keeping sources, rules, data, prompts, interfaces, test cases and operating knowledge current.

```text
bounded user task and current process
  → plausible alternatives and simplest credible baseline
  → task-specific comparison of value, feasibility, and burden
  → selected, retained, rejected, or unproven design rationale
  → success record, initial scope record, and Part 4 evidence plan
```

This is not a maturity ladder: more model involvement is not more capability.

## Compare the plausible alternatives

A comparison may keep several options, combine them, or conclude that no new system is warranted.

### Process redesign or manual assistance

Process redesign can remove duplicate work, clarify source ownership, publish current status, improve intake or repair a handoff. Manual assistance keeps judgment with a person when cases are rare, exceptions are costly, or context cannot yet be represented safely. They lose when the remaining work is repetitive and a bounded contribution can reliably reduce it.

### Deterministic rules and conventional automation

**Deterministic rules** apply explicit conditions to a decision. **Conventional automation** moves information through known steps with rules, forms, queues or stable integrations. Both suit tasks whose inputs, conditions and transitions can be stated and maintained, and a rule is easier to inspect than a model for a stable prohibition. They lose fit when exceptions are hard to state, input needs interpretation, or a growing set of heuristics gets harder to maintain than a learned component. A workflow whose branch conditions are defined in advance is still fixed, even when a later step uses an earlier result.

### Search and source navigation

A **search interface** is a credible baseline when users can judge the source and the main difficulty is finding it. It does not decide whether evidence is current, conflicting, applicable or permitted, so it may be a component rather than the whole design.

### Traditional machine learning

Traditional machine learning fits a definable recurring prediction, ranking or classification with a clear target, labelled or comparable outcome data, and a way to maintain data and reassess the model. Google's guide advises not using ML before you have data if it is not required, and recommends simple behavior and metrics as a baseline for more complex models. [3] That does not mean heuristics always win: a stable, fully specified decision may fit a rule, while a learned component may fit when a complex heuristic is getting hard to maintain and a target, data and ongoing evaluation are feasible. If the target, labels, representativeness or data-handling basis is unknown, the learned option is not yet feasible.

### Single-call model assistance

**Single-call model assistance** uses one bounded model response to interpret varied language, draft material or present an answer. It can be enough when no model-directed next action is needed.

### Fixed model workflows

A **fixed model workflow** combines model calls, source access, routers, validation and predefined error paths in a known orchestration. It suits tasks that split into known subtasks.

### Adaptive agents

Consider an adaptive agent only when model-directed sequencing or stopping should add task-relevant value beyond a fixed orchestration. A record might list a finite permitted set: `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, `escalate`. If the model chooses among them based on observations, the candidate is adaptive even though every action is listed and constrained.

It loses when stable transitions handle the same cases, when the benefit cannot be stated, or when error consequence, maintenance, latency, cost or evidence burden outweighs it. Agentic systems often trade latency and cost for task performance and can compound errors (this guide relies on that source's definitions and trade-off advice, not its tooling guidance, parts of which have changed). [2] If you do move to an agent, start with one, and split into several only when one demonstrably cannot do the task.

### Hybrid designs

A **hybrid** assigns different parts of the task to different approaches, for example deterministic controls for stable, decidable constraints and a model for language interpretation or adaptation where the rule is unknown. It is justified only when no single simpler approach meets the task as well. Deterministic controls grant no authority, and model flexibility does not relax an access boundary.

## Make the comparison evidence-led

The record shows why a design was chosen, what would change the conclusion, and what is open. First name the **comparison boundary**: the user task, included cases, sources, user contexts, prohibited effects, and current process from 1.1. List the alternatives actually considered, including process change or manual help where plausible, each marked retained, rejected, provisionally selected or unproven, with a task-specific reason.

Then assess the factors that change the fit:

- **Task uncertainty.** Is it in language, source selection, sequencing, a real-world exception, or a missing understanding of the problem? Uncertainty from unclear ownership or an avoidable handoff points to process redesign, not adaptation.
- **Data and learning premise.** For a learned component, record the target, the source and status of labels or outcome data, representativeness concerns, and what makes the data usable. For a model not trained for the task, record the task cases and evidence needed to assess behavior, without implying task-specific training data.
- **Action and adaptation.** State the permitted actions, any fixed transitions, and the proposed model-directed next-action, sequence or stopping choices. A finite action list is compatible with an agent; a list of all fixed transitions is evidence of a fixed workflow.
- **Consequence of error.** The user, downstream or operational effect of a wrong, missing, late, misleading or unauthorized result; a read-only response is not consequence-free.
- **Maintenance and evaluation burden.** What each option must keep current, and what it adds in case design, review, diagnostics, correction and support.

NIST advises documenting context, assumptions, limitations and impacts for a generative AI system, showing test results for conditions similar to the deployment setting, and not extrapolating performance from narrow or anecdotal assessments. [4] A favorable demo or benchmark does not transfer to a different user population, source collection, permission or action boundary.

Finally, predeclare the **added-value claim** for an adaptive candidate: what evidence would show that model-directed choice beats the baseline by enough to justify its burden, compared on the same cases and constraints. 1.2 defines claims and measures; Part 4 designs the cases, evaluators and trials.

The [suitability-decision template](../../templates/1.3/suitability-decision.yaml) records a decision status and unknown evidence explicitly.

## Common pitfalls

- **Skipping the baseline.** Compared with nothing, or a straw man, any result looks like a win.
- **One blended score for the comparison.** Averaging quality, cost and latency hides where the agent is worse. Compare dimension by dimension, as in 1.2.
- **Treating a finite action list as proof of a fixed workflow, or of an agent.** Ask who chooses the next step: the orchestration or the model.
- **Starting with several agents.** This multiplies failure paths and evaluation work before one agent has been shown to fall short.
- **Scope creep after the pilot.** A narrow success is used to justify more users, tools or autonomy. Reopen this decision when the task boundary, action set, source conditions or authority changes.

## Requirements

- **SUITABILITY-01** — When a production agent is proposed, the accountable owner MUST record the task-specific reason for choosing it and identify at least one simpler plausible baseline for comparison; the record MUST name the alternatives actually considered and why they were rejected or retained.
- **SUITABILITY-02** — When selecting an approach for a proposed agent, the owner MUST assess task uncertainty, available and usable data, action space, consequence of error, maintenance burden, and evaluation cost; the record MUST explain how these factors favor the selected design rather than treating “AI” or novelty as a benefit.
- **SUITABILITY-03** — When an agent is proposed, the design MUST identify which next actions the model may select or change in response to observations; a workflow with only predefined transitions MUST be classified and assessed as a fixed workflow, even when it branches on previous results.
- **SUITABILITY-04** — Before an adaptive agent is selected for production, its owner MUST compare it with the simplest suitable non-agent baseline on the same task cases and MUST specify what task-relevant evidence would demonstrate sufficient added value to justify its added control, maintenance, and evaluation burden.
- **SUITABILITY-05** — When a hybrid design is selected, its owner SHOULD assign stable, decidable constraints to deterministic controls and reserve model flexibility for the parts that need interpretation or adaptation; the design record SHOULD explain why a single simpler approach is inadequate.

## Worked example: fictional internal policy assistance

The fictional planning record `POLICY-PLAN-001` (`illustrative-unexecuted`) covers `internal-policy-assistance`: permission-filtered, read-only help with internal policy questions, with no write or approval capability. The bounded task is a source-grounded answer about current policy, or a clear next step when evidence is missing or conflicts. In the `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` states a London hotel limit of GBP 220, while `travel-policy-2024-superseded@2024-01-01` is superseded and differs.

| Option | Status | Reason |
| --- | --- | --- |
| Process change (clarify current-source status or the handoff for unresolved questions) | Kept for investigation | No observation yet of how often it resolves real tasks |
| Permission-aware lookup or search; a deterministic rule for an exact, supported lookup | Kept for investigation | Same; not declared successful |
| Fixed retrieval-and-answer workflow | Provisional preference | Permission checking, source selection, response composition, output checks, and missing- or conflicting-evidence paths are predefined transitions; a model router choosing among them does not change that |
| Traditional ML | Not selected | No recurring prediction target, usable labels or maintained outcome data |
| Single-call response | Component only | Part of the fixed workflow, not evidence of an agent |
| Adaptive agent | Unproven, **not selected** | No baseline, result or target exists |

The adaptive candidate would choose, after each observation, whether to locate more requester-permitted evidence, request clarification, return a bounded response, or escalate a conflict. Its added-value claim is narrow: against the fixed workflow on the same permission, currentness, missing-source and conflict cases, model-directed follow-up might improve the appropriate outcome without unacceptable added burden. The [template](../../templates/1.3/suitability-decision.yaml) carries these states with `null` and `not-yet-established` evidence fields.

## Evidence and handoff

A suitability record is not proof of suitability, safety or value. Before handing it on, check that:

- it separates an unclear process or source from a need for model-directed adaptation;
- every learned component has a target and usable-data premise, or is marked not yet established;
- it claims no risk or release decision; and
- an adaptive candidate's evidence status does not invent a result.

Hand claims to [1.2](02-requirements-success-criteria-and-measurable-targets.md), harms, data, authority and owners to [1.4](04-initial-risk-data-ownership-and-delivery-plan.md), and evaluation to [Part 4](../04-testing-and-evaluation/README.md).

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"
[3]: https://developers.google.com/machine-learning/guides/rules-of-ml "Rules of Machine Learning"
[4]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"

# 1.3 Agent Suitability and Alternatives

**Status:** 0.5.0-draft.2 — draft

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent, and any planning decision that compares an agent with a simpler way to meet the same bounded user task. Using a model, having several steps, or varied wording does not make a task agent-suitable.

**Reader question:** Which approach fits this task and its constraints, what simpler baseline is credible, and what evidence could justify the added adaptability of an agent?

[Part 1 — Problem Definition and Planning](README.md) · [1.1 Defining the Problem](01-defining-the-problem.md) · [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) · [Playbook applicability](../../applicability.md)

## Decide the fit before designing the agent

An agent is one possible contribution to a user task, not the default answer to a problem. It adds flexibility where language, evidence or the order of useful work is uncertain. It also adds cost, latency, more ways to fail, and more to evaluate and maintain. Process redesign, human help, search, rules, automation, a learned predictor, one bounded model response, or a fixed model workflow may be better.

Start with the simplest solution that could work, and add complexity only when you can show it is needed. Common practitioner guidance says the same: begin with a single model call or fixed workflow, and move to an agent, then to several agents, only when simpler options fall short. [2]

This chapter makes the comparison inspectable. It does not authorize a design or prove a candidate works. Task and process come from [1.1](01-defining-the-problem.md), targets from [1.2](02-requirements-success-criteria-and-measurable-targets.md), harms and authority from [1.4](04-initial-risk-data-ownership-and-delivery-plan.md), and evidence from Part 4. NIST frames the decision to commission or deploy AI as contextual: weigh trustworthiness, risks, impacts, costs and benefits instead of treating a technology label as a benefit. [1]

## Terms and an operational convention

An **alternative** is a plausible way to help with the same bounded task, not a list of fashionable technologies. A **baseline** is the simplest plausible alternative chosen for a fair comparison: the current manual process, an improved process, or a simpler system. A baseline can be kept because it is good enough, not because it is old.

An **action space** is the set of actions a candidate may take in this task, including a response-only candidate and any permitted information-gathering or externally visible action. Its size alone does not decide whether the candidate is an agent. Consequence, authority and conditions for actions are assessed in [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) and the control chapters.

In this guide, a **fixed workflow** has transitions defined by the orchestration. It may branch on an earlier result, retry a bounded operation, use a model router, or call a model at a set step; it stays fixed while the possible transitions and their selection are predefined. An **adaptive agent** lets model output direct a meaningful next action, sequence or stopping choice in response to observations. The action set can be finite and fully listed; adaptivity is about model-directed choice within it. This is a working convention, not a universal taxonomy; a practitioner source draws a similar line between predefined workflow paths and systems where a model dynamically directs its own process and tool use. [2]

An **adaptation benefit** is the task-relevant gain expected from that model-directed choice, such as finding the next useful permitted source, asking a good follow-up question, or stopping when evidence is enough. It is a hypothesis until compared with a simpler design on relevant cases. **Evaluation burden** is the work needed to test that hypothesis and the new failure paths. **Maintenance burden** is keeping sources, rules, data, prompts, interfaces, test cases and operating knowledge current as the task changes.

```text
bounded user task and current process
  → plausible alternatives and simplest credible baseline
  → task-specific comparison of value, feasibility, and burden
  → selected, retained, rejected, or unproven design rationale
  → success record, initial scope record, and Part 4 evidence plan
```

This is not a maturity ladder: more model involvement is not more capability.

## Compare the plausible alternatives

Start from the actual task boundary, not a wish to use a technique. A comparison may keep several options, combine them, or conclude that no new system is warranted.

### Process redesign or manual assistance

Process redesign can remove duplicate work, clarify source ownership, publish current status, improve intake or repair a handoff. Manual assistance keeps judgment with a person when cases are rare, exceptions are costly, or context cannot yet be represented safely. They lose when the remaining work is repetitive and a bounded contribution can reliably reduce it, and stay unproven if the difficulty was never observed in representative tasks.

### Deterministic rules and conventional automation

**Deterministic rules** apply explicit conditions to a decision. **Conventional automation** moves information through known steps, often with rules, forms, queues or stable integrations. Both suit tasks whose inputs, eligibility conditions and transitions can be stated and maintained. A rule can be easier to inspect than a model interpretation for a stable prohibition or boundary.

They lose fit when exceptions are hard to state, input needs interpretation, or a growing set of heuristics gets harder to maintain than a learned component. A branching workflow is still fixed if its branch conditions are defined in advance. A later step using an earlier result is not evidence for an agent.

### Search and source navigation

A **search interface** helps a person find material and interpret it. It is a credible baseline when users can judge the source and the main difficulty is finding it. Search does not decide whether evidence is current, conflicting, applicable or permitted, so it may be a component of a broader design without being sufficient alone.

### Traditional machine learning

Traditional machine learning fits a recurring prediction, ranking or classification that can be defined. It normally needs a clear target, labelled or comparable outcome data, and a way to maintain data and assess the model as conditions change. Google's guide advises not using ML before you have data if it is not required, and recommends simple behavior and metrics as a baseline for more complex models. [3]

That supports a qualified comparison, not a rule that heuristics always win. A stable, fully specified decision may fit a rule. A learned component may fit when a complex heuristic is getting hard to maintain and a target, data and ongoing evaluation are feasible. If the target, labels, representativeness or data-handling basis is unknown, the learned option is not yet shown to be feasible.

### Single-call model assistance

**Single-call model assistance** uses one bounded model response to interpret varied language, draft material or present an answer. It can be enough when no model-directed next action is needed. A flexible prompt or an uncertain response does not by itself make an agent.

### Fixed model workflows

A **fixed model workflow** combines model calls, source access, routers, validation and predefined error paths in a known orchestration. It may route with a deterministic classifier or a model router and branch after a model or source result, and still be fixed if the allowed transitions are specified. It suits tasks that split into known subtasks.

### Adaptive agents

Consider an adaptive agent only when model-directed sequencing or stopping should add task-relevant value beyond a fixed orchestration. For example, a record can list a finite permitted set: `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, `escalate`. If the model chooses among them based on observations, the candidate is adaptive even though every action is listed and constrained.

It loses when stable transitions handle the same cases, when the expected benefit cannot be stated, or when error consequence, maintenance, latency, cost or evidence burden outweighs it. It is unproven if its comparison did not use the same cases and boundaries as the baseline. The practitioner guidance cited above recommends adding complexity only when needed, and notes that agentic systems often trade latency and cost for task performance and can compound errors. [2] Its definitions and trade-off advice are what this guide relies on; the source says parts of its tooling guidance have since changed. These are design cautions, not performance results. If you do move to an agent, start with one, and split into several only when one demonstrably cannot do the task.

### Hybrid designs

A **hybrid** assigns different parts of the task to different approaches. For example, deterministic controls carry stable, decidable constraints while a model handles language interpretation or adaptation where the rule is unknown. A hybrid is not automatically safer or more capable; it exists because no single simpler approach meets the task as well. Deterministic controls grant no authority, and model flexibility does not relax an access boundary.

## Make the comparison evidence-led

The record must let another reader see why a design was chosen, what would change the conclusion, and what is still open. First name the **comparison boundary**: the user task, included cases, sources, user contexts, prohibited effects, and current process from 1.1. List the alternatives actually considered, including process change or manual help where plausible. For each, say whether it is retained, rejected, provisionally selected or unproven, with a task-specific reason, not a generic claim about AI.

Then assess the factors that change the fit:

- **Task uncertainty.** Is the uncertainty in language, source selection, sequencing, a real-world exception, or a missing understanding of the problem? Uncertainty from unclear ownership or an avoidable handoff points to process redesign, not adaptation.
- **Data and learning premise.** For a learned component, record the target, the source and status of labels or outcome data, representativeness concerns, and what makes the data usable. For a model-assisted approach not trained for the task, record the task cases and evidence needed to assess behavior, and do not imply task-specific training data.
- **Action and adaptation.** State the permitted actions, any fixed transitions, and the model-directed next-action, sequence or stopping choices proposed. A finite action list is compatible with an agent; a list of all fixed transitions is evidence of a fixed workflow.
- **Consequence of error.** Describe the user, downstream or operational effect of a wrong, missing, late, misleading or unauthorized result. A read-only response is not consequence-free. Hand authority, data and harm questions to 1.4.
- **Maintenance and evaluation burden.** Compare what each option must keep current and what it adds in case design, review, diagnostics, correction and support. A simpler baseline may win because it has less to maintain, not because it is less ambitious.

NIST advises documenting context, assumptions, limitations and impacts for a generative AI system, showing test results for conditions similar to the deployment setting, and not extrapolating performance from narrow or anecdotal assessments. [4] A favorable demo or benchmark therefore does not show that an option fits a different user population, source collection, permission boundary or action boundary.

Finally, predeclare the **added-value claim** for an adaptive candidate: what evidence would show that the model-directed choice beats the baseline by enough to justify its burden. Compare on the same cases and constraints; a candidate given easier cases or looser boundaries has not been fairly compared. 1.2 defines claims and measures; Part 4 designs the cases, evaluators and trials.

The [suitability-decision template](../../templates/1.3/suitability-decision.yaml) records a decision status and unknown evidence explicitly.

## Common pitfalls

- **Skipping the baseline.** The agent is compared with nothing, or with a weak straw-man, so any result looks like a win. Compare with the simplest credible alternative on the same cases.
- **One blended score for the comparison.** Averaging quality, cost and latency across options hides where the agent is worse. Compare dimension by dimension, as in 1.2.
- **Treating a finite action list as proof of a fixed workflow, or of an agent.** Ask who chooses the next step: the orchestration or the model.
- **Starting with several agents.** Splitting a task across agents multiplies failure paths and evaluation work before one agent has been shown to fall short.
- **Scope creep after the pilot.** A narrow success is used to justify more users, tools or autonomy. Reopen this decision when the task boundary, action set or authority changes.

## Requirements

- **SUITABILITY-01** — When a production agent is proposed, the accountable owner MUST record the task-specific reason for choosing it and identify at least one simpler plausible baseline for comparison; the record MUST name the alternatives actually considered and why they were rejected or retained.
- **SUITABILITY-02** — When selecting an approach for a proposed agent, the owner MUST assess task uncertainty, available and usable data, action space, consequence of error, maintenance burden, and evaluation cost; the record MUST explain how these factors favor the selected design rather than treating “AI” or novelty as a benefit.
- **SUITABILITY-03** — When an agent is proposed, the design MUST identify which next actions the model may select or change in response to observations; a workflow with only predefined transitions MUST be classified and assessed as a fixed workflow, even when it branches on previous results.
- **SUITABILITY-04** — Before an adaptive agent is selected for production, its owner MUST compare it with the simplest suitable non-agent baseline on the same task cases and MUST specify what task-relevant evidence would demonstrate sufficient added value to justify its added control, maintenance, and evaluation burden.
- **SUITABILITY-05** — When a hybrid design is selected, its owner SHOULD assign stable, decidable constraints to deterministic controls and reserve model flexibility for the parts that need interpretation or adaptation; the design record SHOULD explain why a single simpler approach is inadequate.

## Worked example: fictional internal policy assistance

The planning record `POLICY-PLAN-001` is fictional and unexecuted (`illustrative-unexecuted`). The candidate `internal-policy-assistance` gives permission-filtered, read-only help with internal policy questions, with no write or approval capability.

The bounded task is to help an eligible requester get a source-grounded answer about current policy, or a clear next step when evidence is missing or conflicts. In the `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` states a London hotel limit of GBP 220, while `travel-policy-2024-superseded@2024-01-01` is superseded and differs.

The record first keeps two non-agent options. A process change could clarify current-source status or the handoff for unresolved questions. A permission-aware lookup or search interface could let a requester find the current permitted source. For an exact, supported lookup, a deterministic rule may return the source and value. None is declared successful; the record has no observation of how often they resolve real tasks.

For varied but bounded wording, the record provisionally prefers a fixed retrieval-and-answer workflow: permission checking, source selection, response composition, output checks, and paths for missing or conflicting evidence are predefined transitions. A model router that sends a request down one of these paths does not change that classification.

Traditional ML is not selected: there is no established recurring prediction target, usable labels or maintained outcome data. A single-call response may be a component of the fixed workflow, not evidence of an agent.

The adaptive candidate stays unproven. Its finite actions would be to locate more requester-permitted evidence, request clarification, return a bounded response, or escalate a conflict. It becomes adaptive if the model decides, after an observation, whether to take another evidence step or stop with uncertainty. The added-value claim is narrow: against the fixed workflow on the same permission, currentness, missing-source and conflict cases, model-directed follow-up might improve the appropriate outcome without unacceptable added burden. No baseline, result or target exists, so the agent is **not selected**.

Three decision states result: a process or lookup improvement is kept for investigation, the fixed workflow is the provisional preference, and the adaptive agent is unproven. The [template](../../templates/1.3/suitability-decision.yaml) carries them with `null` and `not-yet-established` evidence fields.

## Evidence and handoff

A suitability record is ready when a reviewer can see the task boundary, the alternatives considered, the simplest baseline, the selected or unproven status, and the evidence that could change the conclusion. It is not proof of suitability, safety or value. Before handing it on, check that:

- baseline and complex candidate are compared on the same task and case conditions;
- it says which uncertainty matters and separates an unclear process or source from a need for model-directed adaptation;
- every learned component has a target and usable-data premise, or is marked not yet established;
- the action space, fixed transitions and any model-directed choices are distinguishable;
- error consequences, maintenance and evaluation burden are considered without claiming a risk or release decision; and
- an adaptive candidate has an added-value claim and an evidence status that does not invent a result.

Use [1.2](02-requirements-success-criteria-and-measurable-targets.md) to turn the claims into criteria and measures, [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) for harms, data, authority and owners, and [Part 4](../04-testing-and-evaluation/README.md) for evaluation. A change in task boundary, action set, source conditions or authority can reopen the decision.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"
[3]: https://developers.google.com/machine-learning/guides/rules-of-ml "Rules of Machine Learning"
[4]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"

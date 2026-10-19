# 1.3 Agent Suitability and Alternatives

**Status:** 0.5.0-draft.2 — Part 1 refined draft; proposed, not adopted

**Audience:** Outcome and process owners, builders, evaluators, and reviewers

**Applicability:** Every proposed production agent and every planning decision that compares an agent with a simpler way to meet the same bounded user task. A task is not made agent-suitable merely because it uses a model, has several steps, or varies in wording.

**Reader question:** Which approach fits this task and its constraints, what simpler baseline is credible, and what evidence could justify the added adaptability of an agent?

[Part 1 — Problem Definition and Planning](README.md) · [1.1 Defining the Problem](01-defining-the-problem.md) · [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) · [Playbook applicability](../../applicability.md)

## Decide the fit before designing the agent

An agent is one possible contribution to a user task, not the default result of identifying a problem. It can add flexibility where language, evidence, or the sequence of useful work is uncertain. It can also add cost, latency, more ways to fail, and more work to evaluate and maintain. Process redesign, human assistance, search, rules, automation, a learned predictor, one bounded model response, or a fixed model workflow can be the better answer.

This chapter makes that comparison inspectable. It does not authorize a design, set a target, establish a risk tier, or prove that a candidate works. [1.1](01-defining-the-problem.md) supplies the bounded user task and current process. [1.2](02-requirements-success-criteria-and-measurable-targets.md) owns outcomes, metrics, targets, and consequences. [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) owns initial harms, data, authority, owners, and delivery limits. Part 4 owns the design and interpretation of decision-grade evidence.

NIST frames a decision to commission or deploy AI as contextual: it calls for considering trustworthiness, risks, impacts, costs, and benefits rather than treating a technology label as a benefit. [1] This chapter turns that framing into a planning comparison. It does not make the NIST framework an adopted requirement or select a universal alternative.

## Terms and an operational convention

An **alternative** is a plausible way to help the same bounded user task. It is not a list of fashionable technologies. A **baseline** is the simplest plausible alternative chosen for a fair comparison; it can be a current manual process, an improved process, or a simpler proposed system. A baseline can be retained because it is good enough, not because it is old.

An **action space** is the set of actions a candidate may take in this task. It includes a response-only candidate and any permitted information-gathering or externally visible action. Its size does not by itself determine whether the candidate is an agent. The consequence of an action, the authority behind it, and the conditions under which it may occur are assessed in [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) and the applicable control chapters.

For this draft's planning convention, a **fixed workflow** has orchestration-defined transitions. It may branch on an earlier result, retry a bounded operation, use a model router, or call a model at a defined step. Those features do not make it adaptive when the possible transitions and their selection are predefined. An **adaptive agent** lets model output direct a meaningful next action, sequence, or stopping choice in response to observations. The permitted action set can be finite and fully enumerated; adaptivity is about model-directed choice within that boundary, not an unbounded or unknowable set of actions.

This is an operational convention for classifying a planning record, not a universal taxonomy. A practitioner source draws a similar architectural distinction between predefined workflow paths and systems where a model dynamically directs process and tool use. [2] The convention helps a reviewer locate the choice that creates added flexibility and added assurance work.

An **adaptation benefit** is the task-relevant improvement expected from that model-directed choice. It might be finding the next useful permitted source after an observation, choosing an appropriate follow-up question, or stopping when the evidence is sufficient. It is a hypothesis until compared with a simpler design on relevant task cases. **Evaluation burden** is the work needed to determine whether that hypothesis holds and whether new failure paths remain acceptable. **Maintenance burden** includes keeping sources, rules, data, prompts, interfaces, case coverage, and operating knowledge current as the task changes.

A useful working model is:

```text
bounded user task and current process
  → plausible alternatives and simplest credible baseline
  → task-specific comparison of value, feasibility, and burden
  → selected, retained, rejected, or unproven design rationale
  → success record, initial scope record, and Part 4 evidence plan
```

The arrows do not form a maturity ladder. More model involvement is not inherently more capable, and an agent can be the wrong choice after a careful comparison.

## Compare the plausible alternatives

Start with the candidate's actual task boundary, not a desire to use a particular technique. The following options are distinct planning shapes. A useful comparison may retain several, combine them, or conclude that no new system is warranted.

### Process redesign or manual assistance

Process redesign can remove duplicate work, clarify source ownership, publish current status, improve intake information, or repair a handoff. Manual assistance can keep contextual judgment with a person when cases are rare, the exception cost is high, or important context cannot yet be represented safely. These approaches lose when the remaining work is genuinely repetitive and a bounded contribution can reliably reduce it; they remain unproven when the reported difficulty has not been observed in representative tasks.

### Deterministic rules and conventional automation

**Deterministic rules** apply explicit conditions to a decision. **Conventional automation** moves information through known steps, often using rules, forms, queues, or stable integrations. They are useful when inputs, eligibility conditions, and transitions can be stated and maintained clearly. A rule may be easier to inspect for a stable prohibition or boundary than a model interpretation.

Rules and automation can lose fit when exception logic is genuinely difficult to state, the input needs interpretation, or maintaining a growing heuristic becomes less manageable than a learned component. A branching workflow is still fixed when its branch conditions and transitions are defined in advance. The fact that a later step uses an earlier result is not, by itself, evidence for an agent.

### Search and source navigation

A **search interface** helps a person locate material and make the interpretation. It is a credible baseline when users can judge the source and the main difficulty is finding it. Search does not itself decide whether evidence is current, conflicting, applicable, or permitted. It can therefore be a useful component of a broader design without being sufficient for every task.

### Traditional machine learning

Traditional machine learning is a candidate when a recurring prediction, ranking, or classification can be defined. It normally needs a clear prediction target, usable examples with labels or comparable outcome data, and a way to maintain the data and assess the model as conditions change. Google defines these terms and advises teams not to use ML before data exists when it is not necessary; it also recommends simple behavior and metrics as a baseline for more complex models. [3]

That guidance supports a qualified comparison, not a rule that heuristics always win. A stable, fully specified decision may fit a rule better. A learned component may fit better when a complex heuristic is becoming difficult to maintain and a target, data, and ongoing evaluation are feasible. If the target, labels, representativeness, or data-handling basis is unknown, the learned option is not yet established as feasible.

### Single-call model assistance

**Single-call model assistance** uses one bounded model response to interpret varied language, draft material, or present an answer. It can be enough when no model-directed next action is needed. A person or deterministic check may use the response, but a flexible prompt or an uncertain response does not by itself create an agent.

### Fixed model workflows

A **fixed model workflow** combines model calls, source access, routers, validation, and predefined error paths in a known orchestration. It may route a request using a deterministic classifier or a model router, and it may branch after a model or source result, while remaining fixed if the allowed transitions are specified by the workflow. It is a strong candidate when the task can be decomposed into known subtasks and those boundaries improve clarity or checking.

### Adaptive agents

An adaptive agent is worth considering only when model-directed sequencing or stopping is expected to create task-relevant value beyond a fixed orchestration. For example, a planning record can identify a finite permitted set such as `locate_permitted_evidence`, `request_clarification`, `return_bounded_response`, and `escalate`. If the model selects which of those actions to take next based on observations, the record describes an adaptive candidate even though every action is enumerated and constrained.

The adaptive candidate loses when the same cases can be handled by stable transitions, when the expected adaptation benefit cannot be stated, or when error consequence, maintenance, latency, cost, or evidence burden outweighs that benefit. It remains unproven when its comparison has not used the same relevant cases and boundaries as its baseline. The practitioner guidance cited above recommends increasing complexity only when needed and notes the latency, cost, and compounding-error trade-offs of agentic systems. [2] Those are design cautions, not universal performance results.

### Hybrid designs

A **hybrid** deliberately assigns different parts of the task to different approaches. For example, deterministic controls can carry stable, decidable constraints while a model handles language interpretation or adaptation where the rule is not known. A hybrid is not automatically safer or more capable: its reason to exist is that no single simpler approach meets the bounded task as well. Deterministic controls do not grant authority, and model flexibility does not relax an access or authorization boundary.

## Make the comparison evidence-led

A decision record need not predict every implementation detail. It needs enough specificity that another reader can tell why a design was chosen, what would change the conclusion, and which questions remain open.

Begin by naming the **comparison boundary**: the user task, included task cases, sources or dependencies, user contexts, prohibited effects, and current process from 1.1. List the alternatives actually considered, including process change or manual assistance when plausible. For each alternative, state whether it is retained, rejected, selected provisionally, or unproven, and give the task-specific reason rather than a generic claim about AI.

Then assess the factors that change the fit:

- **Task uncertainty.** Identify whether uncertainty is in language, source selection, task sequencing, a real-world exception, or a missing problem understanding. Uncertainty caused by unclear ownership or an avoidable handoff can point to process redesign rather than adaptation.
- **Data and learning premise.** For a learned component, record the intended target, the source and status of labels or outcome data, representativeness concerns, and what makes the data usable. For a model-assisted approach that is not being trained for the task, record the task cases and evidence needed to assess its behavior instead of implying that it has task-specific training data.
- **Action and adaptation.** State the permitted action set, the fixed transitions if any, and the specific model-directed next-action, sequence, or stopping choices proposed. A finite list of actions is compatible with an agent; a list of all fixed transitions is evidence for a fixed workflow.
- **Consequence of error.** Describe the user, downstream, or operational effect of a wrong, missing, late, misleading, or unauthorized result. Do not treat a read-only response as consequence-free. Hand off authority, data, and harm questions to 1.4 rather than turning this comparison into a risk acceptance.
- **Maintenance and evaluation burden.** Compare what each option must keep current and what each adds to case design, observations, review, diagnostics, correction, and operational support. A simpler baseline can be preferable because it has fewer things to maintain, not because it is a less ambitious idea.

NIST advises documenting context, assumptions, limitations, and impacts for a generative AI system, and cautions that current pre-deployment tests can be mismatched to deployment context. [4] Therefore, a favorable demonstration or benchmark does not by itself establish that one alternative fits a different user population, source collection, permission boundary, or action boundary.

Finally, predeclare the **added-value claim** for an adaptive candidate: what task-relevant evidence would show that the model-directed choice improves on the baseline enough to justify its added burden. Compare alternatives on the same relevant cases and constraints; a candidate that receives easier cases or more permissive boundaries has not made a useful suitability comparison. Chapter 1.2 defines the claims and measures. Part 4 designs the cases, evaluators, trials, and interpretation needed to supply evidence.

The accompanying [suitability-decision template](../../templates/1.3/suitability-decision.yaml) is a neutral planning aid. It records a decision status and unknown evidence explicitly; it is not an architecture specification, an approval, or a release decision.

## Requirements

The following proposed requirements are unchanged. They require a documented, task-specific comparison without making an agent, a particular baseline, or a particular evaluation method universal.

- **SUITABILITY-01** — When a production agent is proposed, the accountable owner MUST record the task-specific reason for choosing it and identify at least one simpler plausible baseline for comparison; the record MUST name the alternatives actually considered and why they were rejected or retained.
- **SUITABILITY-02** — When selecting an approach for a proposed agent, the owner MUST assess task uncertainty, available and usable data, action space, consequence of error, maintenance burden, and evaluation cost; the record MUST explain how these factors favor the selected design rather than treating “AI” or novelty as a benefit.
- **SUITABILITY-03** — When an agent is proposed, the design MUST identify which next actions the model may select or change in response to observations; a workflow with only predefined transitions MUST be classified and assessed as a fixed workflow, even when it branches on previous results.
- **SUITABILITY-04** — Before an adaptive agent is selected for production, its owner MUST compare it with the simplest suitable non-agent baseline on the same task cases and MUST specify what task-relevant evidence would demonstrate sufficient added value to justify its added control, maintenance, and evaluation burden.
- **SUITABILITY-05** — When a hybrid design is selected, its owner SHOULD assign stable, decidable constraints to deterministic controls and reserve model flexibility for the parts that need interpretation or adaptation; the design record SHOULD explain why a single simpler approach is inadequate.

## Worked example: fictional internal policy assistance

The shared planning record `POLICY-PLAN-001` considers `internal-policy-assistance`. It is **fictional and unexecuted**, with status `illustrative-unexecuted`. The candidate provides permission-filtered, read-only help with internal policy questions; it has no write or approval capability. The example records a planning rationale, not observed performance, a completed review, an approval, deployment, or user benefit.

The bounded task is to help an eligible requester obtain a source-grounded response about a current policy or a clear next step when the evidence is unavailable or conflicts. In the fictional `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` states a London hotel limit of GBP 220, while `travel-policy-2024-superseded@2024-01-01` is superseded and states a different amount. Those are controlled fixture facts, not real policy or candidate results.

The record first retains two non-agent possibilities. A process change could clarify current-source status or the handoff for unresolved questions. A permission-aware policy lookup or search interface could let a requester find the current permitted source. For an exact, supported lookup, a deterministic rule may return the source and value. These alternatives are not declared successful; the illustrative record has no observation about how often they resolve real user tasks.

For varied but bounded wording, the record provisionally prefers a fixed retrieval-and-answer workflow: permission checking, source selection, response composition, output checks, and the paths for missing or conflicting evidence are planned as predefined transitions. A model router could direct a request to one of these predeclared paths without changing that classification. The expected `needs_information` outcome for missing or equally authoritative conflicting evidence is not a measured candidate result.

Traditional ML is not selected in the example because the record has no established recurring prediction target, usable labels, or maintained outcome data. A single-call response remains a possible component of the fixed workflow, not evidence of an agent. These are unmeasured feasibility observations in the fictional plan, not a claim that learned models or model assistance cannot help a policy task.

The record leaves an adaptive candidate unproven. Its finite permitted actions could be to locate additional requester-permitted evidence, request clarification, return a bounded response, or escalate a conflict. It would become adaptive if the model, in response to an observation, chose whether to perform another permitted evidence step or stop and return uncertainty. The proposed added-value claim is narrow: compared with the fixed workflow on the same permission, currentness, missing-source, and conflict cases, model-directed follow-up might improve the appropriate outcome without an unacceptable added burden. No baseline, comparison result, target, or approval exists in this illustration, so the agent is **not selected**.

This yields three visible decision states: a process or lookup improvement is retained for investigation, the fixed workflow is a provisional planning preference, and the adaptive agent remains unproven. The [template](../../templates/1.3/suitability-decision.yaml) carries those states forward with `null` and `not-yet-established` evidence fields rather than presenting a planned conclusion as an executed result.

## Evidence and handoff

A suitability record is ready to inform the next planning step when a reviewer can identify the task boundary, the actual alternatives, the simplest plausible baseline, the selected or unproven status, and the evidence that could change the conclusion. It is planning evidence, not proof of suitability, safety, user value, or readiness.

Before handing the record to 1.2, 1.4, and Part 4, check that it makes the following visible:

- the comparison uses the same bounded user task and relevant case conditions for the baseline and the more complex candidate;
- the record explains which uncertainty matters and separates an unclear process or source from a need for model-directed adaptation;
- every learned component has a target and usable-data premise, or is explicitly not yet established;
- the action space, fixed transitions, and any model-directed action, sequence, or stopping choices are distinguishable;
- error consequences, maintenance work, and evaluation burden are considered without claiming a risk or release decision; and
- an adaptive candidate has a task-relevant added-value claim and an evidence status that does not manufacture a result.

Use [1.2](02-requirements-success-criteria-and-measurable-targets.md) to turn the selected comparison claims into criteria and measures. Use [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) to record harms, data, authority, owners, and delivery limits. Use [Part 4](../04-testing-and-evaluation/README.md) for evaluation design, coverage, trials, and evidence interpretation. A later change in task boundary, action set, source conditions, or authority can reopen the suitability decision.

## References

[1]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "Artificial Intelligence Risk Management Framework 1.0"
[2]: https://www.anthropic.com/engineering/building-effective-agents "Building effective agents"
[3]: https://developers.google.com/machine-learning/guides/rules-of-ml "Rules of Machine Learning"
[4]: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf "Artificial Intelligence Risk Management Framework Generative Artificial Intelligence Profile"

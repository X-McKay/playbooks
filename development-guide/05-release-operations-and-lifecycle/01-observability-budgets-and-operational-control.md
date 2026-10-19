# 5.1 Observability, Budgets, and Operational Control

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Agent developers, service owners, and operators  
**Applicability:** Every production agent; depth and signals scale with risk, exposure, and execution class.  
**Reader question:** How do I give an operator enough evidence to understand a run, keep bounded work bounded, and stop further work, without mistaking a diagnostic signal for proof of a safe or authorized result?

[Part 5](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · Next: [5.2 Readiness, Change, and Rollout](02-readiness-change-and-rollout.md) and [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)

## Purpose and applicability

An agent can look healthy while its outcome is wrong, incomplete, legitimately denied, or unknown: a retrieval returns an old document, a tool times out after accepting work, or retries use up the allowance. Ordinary request logs cannot tell an operator which happened or whether more work is safe.

This chapter describes a minimum **operational view**, which relates a request to a run, its physical attempts, its resource use, and its declared outcome, and **operational control**: executable bounds and an authorized way to prevent further agent work.

A short-lived, single-process assistant can use a small structured run record instead of a tracing platform but still needs correlation, meaningful outcomes, runtime limits, and a stop path. A durable or multi-worker service also keeps correlation across resumes and coordinates budgets that span workers or runs.

It does not choose a telemetry backend, require tracing, set objectives or thresholds, or grant release or incident authority. Related: capacity and admission ([8.4](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md)), cost and performance ([8.3](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md)), data handling and audit evidence ([3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)), evaluation (Part 4), release and change ([5.2](02-readiness-change-and-rollout.md)), ownership and incidents ([5.3](03-ownership-incidents-maintenance-and-retirement.md)), and uncertain external effects ([7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)).

## Working model

A **request** is an initiating interaction; a **run** is the bounded unit of agent work done for it. One request can create several runs, and a durable run can pause, resume, or move between workers while keeping a stable identity and its link to the request. An **attempt** is one physical try at an operation, such as one retrieval or model request. A retry is another attempt, not a free continuation.

**Telemetry** is what an operator uses to inspect this. An **event** records a meaningful point in time, such as a pre-dispatch reservation or a stop request. OpenTelemetry defines a **metric** as a runtime measurement aggregated for analysis and a **trace** as the path of a request through an application; a **span** is one unit of work within a trace. Metrics and traces answer different questions, and neither replaces the other. [1] [2]

Correlation is a logical link; work need not stay in one process. A compact run record can carry request, run, and attempt identities, the agent and version, the effective capability or configuration identity, and operation records. Add workflow, approval, tenant, or similar references only when the concept exists and its use is permitted. OpenTelemetry semantic conventions are an optional shared vocabulary; they do not decide which fields to collect or make collection permissible. [3]

Keep these meanings separate in the record:

- A **terminal outcome** is the contract-level result for the run, such as `complete`, `needs_information`, `declined`, or `failed`.
- An **operational termination or exhaustion reason** says why the runtime stopped trying, such as a deadline, a retrieval ceiling, an operator stop, or an unresolved in-flight operation.
- An **operation result** says what happened to one model or tool attempt.
- **Telemetry success** says whether the observation itself was captured.

Task success, evaluation conclusions, release authorization, and authoritative external effects are further separate facts; none follows from a clean span or green dashboard.

There are two kinds of budget. A **runtime-resource budget** bounds the work one run, or a deliberately shared pool of runs, may use: time, model requests, tool calls, iterations, output, tokens, bytes, or estimated spend. An **SLI** is a defined measure of a service property, an **SLO** is its target, and an **error budget** is the permitted SLO noncompliance in a stated window. SLOs concern reliability users experience; neither they nor per-run ceilings substitute for the other. Your organization chooses the SLI, target, window, owner, and decision policy. [4]

## Decisions and best practices

### Choose signals from operator questions

Start from a decision, not a habit of collecting data: are runs reaching their contract outcome, are permitted denials rising, is one operation using up the time allowance, is a ceiling being reached, is a stop suppressing new work? For reliability, base the SLI on a user-relevant good event; the error budget shows SLO loss over the window and is not a model, token, or cost budget.

For each question, name a signal, who acts on it, the decision it informs, and the route when it crosses its local condition. An alert without a named action is noise. SRE guidance combines an indicator with error-budget information and judges alerting by precision, recall, detection time, and reset time; treat these as design questions, not adopted thresholds. [5]

A minimum view usually includes:

- counts of runs by normalized terminal outcome;
- elapsed time and, when meaningful, active-processing time;
- model and tool attempt counts and outcome categories;
- retry or iteration counts;
- applicable resource use;
- limit-exhaustion and stop observations;
- the agent/version and capability/configuration identities needed to read the run.

Separate active processing from human or durable waiting; an approval wait is not model latency. A read-only assistant should not invent an approval field to satisfy a schema.

Match the outcome vocabulary to the agent contract. `complete` means contract-defined success; `needs_information`, `declined`, `failed`, `timed_out`, and `cancelled` are different conditions, not a generic error. `partial` is meaningful only when the contract defines what makes it safe and useful. An exhaustion observation can accompany a non-success outcome; not every contract has a terminal `budget_exhausted` state. Tie task success to the criteria in [1.2](../01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), not to fluent text or a citation.

Bound metric labels. Cardinality is the number of distinct attribute combinations, and values such as user identities or raw URL paths can create unbounded aggregation memory. [1] Keep run, request, user, tenant, workflow, prompt, raw URL, and free-form error text out of aggregate dimensions; use controlled categories such as operation type, declared outcome, or safe error class. Put necessary correlation detail in protected event or trace records under [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), and do not treat ordinary telemetry as the audit record for a consequential action.

Diagnostics show what the system recorded, not that a source supports an answer, was authoritative or entitled, or that a release was authorized; those claims need boundary evidence from the linked chapters.

### Instrument agent steps with open conventions

If you use OpenTelemetry, its GenAI semantic conventions define an `invoke_agent` span for an agent invocation and an `execute_tool` operation for a tool call; sub-agent work can nest under the parent. The conventions are at **Development** stability and live in their own repository, so pin the instrumentation version and keep attribute names in one place to ease renames. [6]

Message content attributes such as input messages and system instructions are opt-in. Decide where to capture content, for example fuller capture in test and metadata or redacted content in production, under [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md). [6] Spans show what happened, not that it was correct.

### Make budgets executable

Pick resource dimensions from the task's likely failure modes: a read-only question may need elapsed-time, model-request, retrieval-call, iteration, and response-size ceilings; another service may add token, byte, or spend ceilings. Give each budget a unit, scope, measurement point, remaining-allowance behavior, and exhausted outcome; no number is universal.

Account for each **physical attempt**. Before dispatching a model or tool operation, check the remaining allowance; when an estimate exists, reserve it so concurrent work cannot oversubscribe the run or shared pool. At dispatch, charge the attempt even if the result is a timeout or unknown, and reconcile measured use when a response or billing report arrives. A reservation blocks avoidable new work but does not prove the final charge, because accepted in-flight work can keep using resources.

Enforce this in the deterministic runtime, not a model instruction. Retries, including nested retry paths, draw on the same run budget, or local retry limits multiply into unbounded work. A budget that spans conversations, tenants, workers, or independent runs needs shared durable accounting with a defined reservation and reconciliation rule; one that does not gains nothing from a shared ledger.

Unknown cost stays `unknown`: not zero, not within budget, and not evidence that no charge will arrive; the same applies to unavailable token or byte measurements. Without a pre-dispatch price estimate, your organization decides whether and under what governance to dispatch. This chapter supplies no price list or tested ceiling.

### Define a safe exhausted state and a real stop

When a limit is reached, stop **new work within that limit**, record the usage (measured, estimated, or unknown), triggering dimension, affected attempt, and termination reason, and return the contract-defined result: a declared non-success outcome, a request for information, a permitted escalation, or a labelled partial result when the contract makes it safe. Do not trim material evidence to force a complete answer, retry an authorization denial as a transient fault, or treat an unknown result as permission to repeat a potentially unsafe action.

A stop request and a confirmed cancellation are different facts. A stop prevents later dispatch but may arrive while an operation is in flight; mark that operation `cancelled` only when cancellation is confirmed, otherwise in flight, unresolved, or completed according to the evidence. Undo is a separate compensating action that stopping does not imply; see [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md).

Document the stop scope (one run, new admissions to an agent, or a capability), the authorized operator, how a request is recorded, which new work is suppressed, how in-flight work is shown, and what evidence is needed before resuming. NIST's AI RMF (MANAGE 2.4) calls for mechanisms to supersede, disengage, or deactivate AI systems that perform inconsistently with intended use. [7] Test it beforehand. Re-enabling service is a controlled change under [5.2](02-readiness-change-and-rollout.md), and response and escalation belong to [5.3](03-ownership-incidents-maintenance-and-retirement.md); a stop is not an incident declaration or a recovery or release authorization.

### Recognize failure modes early

- **Tidy telemetry, wrong answer.** Model and retrieval operations can report normal results while the answer is unsupported; do not label the run `complete` from operation status alone.
- **Any two values called a conflict.** Current material plus a marked superseded record is a source-precedence case; record source status and apply the declared selection rule instead of inventing uncertainty or choosing a stale value.
- **Unbounded metric labels.** They make the aggregate used for alerting unreliable or expensive.
- **Retry handlers that reset the attempt counter.** They bypass the ceiling.
- **Per-worker counters.** They overspend a supposedly shared pool.
- **A "stopped" interface over an unknown in-flight call.** Show the unresolved state.
- **Collapsed dashboards.** Merged outcomes make a partial answer look successful.

The fix is a record that keeps identity, outcome, reason, attempt, budget scope, and in-flight state distinct, exercised before production.

### Build an inspectable operating control record

The optional [operating control record template](../../templates/5.1/operating-control-record.yaml) makes the design reviewable without imposing a platform. Fill it in this order:

1. Terminal outcomes, the task-success condition, and accompanying termination reasons and operation-result categories.
2. Identities (request, run, attempt, agent/version, capability/configuration), plus optional references only where they exist and are permitted.
3. Operator questions, signals, safe aggregate categories, decision owner, and route; any SLI/SLO/error budget kept apart from resource ceilings.
4. Per resource dimension: unit, scope, pre-dispatch check or reservation, in-flight treatment, reconciliation source, exhausted behavior, unknown-cost handling.
5. Stop scope and its requested, confirmed, unresolved, and resumed states, linking to the release, incident, privacy, evaluation, and uncertain-effect owners.
6. A planned example checked against the checklist below.

## Requirements

- **OPS-01** For every production run, the system MUST assign a stable run identifier and preserve its relation to the initiating request across recorded operations; it MUST identify the agent version and effective capability/configuration identity needed to interpret the run. Workflow and approval identifiers MUST be recorded only when those concepts apply and their use is permitted.
- **OPS-02** For every production agent, operators MUST be able to distinguish the contract-defined successful outcome from clarification, decline, escalation, cancellation, timeout, budget exhaustion, and failure; the system MUST attribute model and tool operations to the relevant run and record their outcome and duration.
- **OPS-03** Before production use, each agent MUST define and enforce runtime ceilings for applicable per-run dimensions, including elapsed time, model requests or iterations, tool calls, and model/tool output; where token or cost limits apply, those limits MUST be enforced or estimated at the earliest feasible boundary, with unknown cost kept unknown.
- **OPS-04** When a budget spans runs or workers, the responsible service MUST enforce it using shared durable accounting; when any limit is exhausted, the runtime MUST stop new work within that limit, emit the specific exhaustion outcome, and return only a contract-permitted partial result or a declared non-success outcome.
- **OPS-05** For every production agent, an authorized operator MUST have a documented mechanism to stop a run or prevent further agent work; the mechanism MUST define treatment of in-flight operations and preserve unresolved outcomes for reconciliation instead of implying that stopping reverses them.

These add to the universal rules. They require no tracing or dashboard product, data store, or prompt capture; a structured run record and a reviewed operating view can meet them.

## Worked example

A fictional control design for the internal policy assistant (`example_id: POLICY-BUILD-001`, `use_case_id: internal-policy-assistance`, `packet_id: POLICY-OPS-001`, `status: illustrative-unexecuted`); nothing in it was run.

The assistant is read-only and answers from requester-permitted, approved policy material. In the ordinary `travel-policy-current@fixture-2026-10-18.1` world, `employee-uk-104` has `approved-policy-read` permission for the current `travel-policy-2026@2026-10-01` source (GBP 220) and the approved historical `travel-policy-2024-superseded@2024-01-01` record (GBP 200). Only the current source is authority for the London answer. This is a **stale-distraction** condition, not a conflict.

The `POLICY-CONFLICT-004` variant is the conflict: it adds `travel-policy-2026-conflicting-amendment@2026-10-12` (GBP 260) as an equally authoritative current source the same employee may read, so the expected outcome is `needs_information`. For `contractor-uk-204`, the retrieval boundary denies travel-policy access; the expected outcome is `declined`, with no restricted amount in the output.

The per-run envelope allows three model requests, four retrieval calls, 15 seconds elapsed time, and an optional 12 seconds of active processing. The record ties a request to the run, candidate, and capability/configuration identities and each attempt; aggregates use operation type, terminal outcome, and termination reason, not the requester or question.

In `POLICY-EXHAUSTION-008`, the retrieval budget is exhausted and a controlled retrieval timeout follows. The implementation stops new retrieval, keeps the last attempt and its timeout result, and records a reason such as `retrieval_budget_exhausted`. The terminal outcome is `failed`, distinct from the reason. It does not invent an amount, cite unavailable evidence, or retry to look complete.

If a stop request arrives during an in-flight retrieval, the control blocks later model or retrieval dispatch, records the request, and marks the retrieval cancelled only if confirmed; otherwise it stays unresolved for review. The read-only assistant has no external write to undo, which does not carry over to a write-capable agent.

## Evidence and checklist

Before production traffic:

- **Record.** A representative record shows the request-to-run link; run, attempt, agent/version, and capability/configuration identities; operation type, duration, and result; terminal outcome and, separately, termination reason; and each resource measurement or unknown value.
- **Resume and labels.** A resumed durable run keeps its run identity while identifying the attempt; aggregate labels are bounded; detailed diagnostics follow [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).
- **Limits.** Exercised with nested retries and concurrent attempts on shared budgets: the pre-dispatch check blocks impermissible new work, every attempt is attributed, and reconciliation keeps unknown cost or uncertain completion instead of zero or success.
- **Exhaustion.** Each path shows the reason, the declared terminal outcome, and no prohibited new work.
- **Stop.** Exercised during idle and in-flight work: scope, suppression of later work, request record, and distinct requested, confirmed, unresolved, and resumed states.

This shows how the exercised control behaves, not service reliability, grounding, authorization, or release readiness.

## References

[1]: https://opentelemetry.io/docs/concepts/signals/metrics/ "OpenTelemetry metrics"
[2]: https://opentelemetry.io/docs/concepts/signals/traces/ "OpenTelemetry traces"
[3]: https://opentelemetry.io/docs/concepts/semantic-conventions/ "OpenTelemetry semantic conventions"
[4]: https://sre.google/workbook/implementing-slos/ "Google SRE Workbook implementing SLOs"
[5]: https://sre.google/workbook/alerting-on-slos/ "Google SRE Workbook alerting on SLOs"
[6]: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md "OpenTelemetry GenAI agent spans"
[7]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"

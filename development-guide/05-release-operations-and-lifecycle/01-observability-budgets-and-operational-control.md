# 5.1 Observability, Budgets, and Operational Control

**Status:** 0.5.0-draft.2 — draft  
**Audience:** Agent developers, service owners, and operators  
**Applicability:** Every production agent; depth and signals scale with risk, exposure, and execution class.  
**Reader question:** How do I give an operator enough evidence to understand a run, keep bounded work from becoming unbounded, and stop further work, without mistaking a diagnostic signal for proof of a safe or authorized result?

[Part 5](README.md) · [Playbook home](../../README.md) · [Applicability](../../applicability.md) · Next: [5.2 Readiness, Change, and Rollout](02-readiness-change-and-rollout.md) and [5.3 Ownership, Incidents, Maintenance, and Retirement](03-ownership-incidents-maintenance-and-retirement.md)

## Purpose and applicability

An agent can look healthy while its task outcome is wrong, incomplete, legitimately denied, or still unknown. A model call may finish, a retrieval may return an old document, a tool may time out after accepting work, or retries may use up the time and resource allowance without producing a contract-permitted answer. Ordinary request logs cannot tell an operator which of these happened or whether more work is safe.

This chapter describes a minimum **operational view**: a way to relate a request to a run, its physical attempts, its resource use, and its declared outcome. It also describes **operational control**: executable bounds and an authorized way to prevent further agent work.

It applies even to a short-lived, single-process assistant. That assistant can keep a small structured run record instead of a tracing platform, but it still needs correlation, meaningful outcomes, runtime limits, and a stop path. A durable or multi-worker service must also keep correlation across resumes and coordinate only the budgets that span workers or runs.

The chapter does not choose a telemetry backend, require distributed tracing, set service objectives or alert thresholds, or grant release or incident authority. Other chapters own the neighboring topics: shared-capacity and admission engineering ([8.4](../../engineering-reference/08-model-context-and-resource-engineering/04-capacity-admission-control-and-backpressure.md)), cost and performance optimization ([8.3](../../engineering-reference/08-model-context-and-resource-engineering/03-cost-latency-and-performance-optimization.md)), data handling and audit evidence ([3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md)), evaluation methods (Part 4), release authorization and change control ([5.2](02-readiness-change-and-rollout.md)), ownership and incidents ([5.3](03-ownership-incidents-maintenance-and-retirement.md)), and recovery of uncertain external effects ([7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md)).

## Working model

A **request** is an initiating interaction. A **run** is the bounded unit of agent work done for that request. One request can create more than one run, and one durable run can pause, resume, or move between workers. Give the run a stable identity and keep its link to the request through all of those changes. An **attempt** is one physical try at an operation, such as one retrieval or one model request. A retry is another attempt, not a free continuation of the first.

**Telemetry** is the information gathered so an operator can inspect this behavior. An **event** records a meaningful point in time, such as a pre-dispatch reservation or a stop request. OpenTelemetry defines a **metric** as a measurement of a service captured at runtime, aggregated for analysis, and a **trace** as the path of a request through an application; a **span** is one unit of work within a trace. Metrics and traces answer different questions, and neither replaces the other. [1] [2]

Correlation is a logical link, not a promise that work stayed in one process. A compact run record can carry a request identity, a stable run identity, an attempt identity, the agent and version, the effective capability or configuration identity, and operation records. Add workflow, approval, tenant, or similar references only when the concept exists and its use is permitted. OpenTelemetry semantic conventions are an optional shared vocabulary for naming operations and data. They do not decide which fields an agent must collect or make collection permissible. [3]

Keep these meanings separate in the record:

- A **terminal outcome** is the contract-level result returned for the run, such as `complete`, `needs_information`, `declined`, or `failed`.
- An **operational termination or exhaustion reason** says why the runtime stopped trying, such as a deadline, a retrieval ceiling, an operator stop, or an unresolved in-flight operation.
- An **operation result** says what happened to one model or tool attempt.
- **Telemetry success** says whether the observation itself was captured.

A successful user task, an evaluation conclusion, a release authorization, and an authoritative external effect are further separate facts. None follows from a span ending without error or a green dashboard.

There are two kinds of budget. A **runtime-resource budget** bounds the work one run, or a deliberately shared pool of runs, may use: time, model requests, tool calls, iterations, output, tokens, bytes, or estimated spend. An **SLI** is a carefully defined measure of a service property, an **SLO** is its target, and an **error budget** is the permitted amount of SLO noncompliance in a stated window. SLI/SLO practice is about the reliability users experience and the decisions made from it. It does not replace a per-run resource ceiling, and a ceiling does not establish an SLO. Choosing the SLI, target, window, owner, and decision policy is up to your organization. [4]

## Decisions and best practices

### Choose signals from operator questions

Start from a decision, not a habit of collecting data. An operator may need to know whether runs reach their contract outcome, whether a permitted denial is rising, whether one operation is using up the elapsed-time allowance, whether a ceiling is being reached, or whether a stop is suppressing new work. For service reliability, the owner can pick an SLI for a user-relevant good event and an SLO that sets a target; the error budget then shows material SLO loss over the window. Do not call it a model, token, or cost budget.

For each question, name a small signal, the person who can act on it, the decision it informs, and the route when it crosses its locally chosen condition. An alert without a named action is noise. SRE guidance frames SLO alerting as a rule that combines an indicator with error-budget information, and judges alerting by precision, recall, detection time, and reset time. Treat these as design questions, not adopted thresholds or severity levels. [5]

A minimum view usually includes:

- counts of runs by normalized terminal outcome;
- elapsed time and, when meaningful, active-processing time;
- model and tool attempt counts and outcome categories;
- retry or iteration counts;
- applicable resource use;
- limit-exhaustion and stop observations;
- the agent/version and effective capability/configuration identities needed to read the run.

Separate active processing from human or durable waiting time. A long approval wait should not be reported as model latency, and a read-only assistant should not invent an approval field to satisfy a schema.

Use a small outcome vocabulary that matches the agent contract. `complete` means the contract-defined success. `needs_information`, `declined`, `failed`, `timed_out`, and `cancelled` are different conditions; do not collapse them into a generic error. A `partial` outcome is meaningful only when the contract defines what makes it safe and useful. An exhaustion observation can accompany a declared non-success outcome; do not assume every contract has a terminal `budget_exhausted` state. Tie task success to the criteria in [1.2](../01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md), not to fluent text or a citation.

Metrics need deliberately bounded labels. Cardinality is the number of distinct attribute combinations, and high-cardinality values such as user identities or raw URL paths can create unbounded aggregation memory. [1] Keep run, request, user, tenant, workflow, prompt, raw URL, and free-form error text out of aggregate dimensions. Use controlled categories such as operation type, declared outcome, or safe error class. Put only the necessary correlation detail in protected event or trace records under [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md), and do not treat ordinary telemetry as the audit record for a consequential action.

Diagnostics show what the system recorded. They do not prove that a source supports an answer, that it was authoritative for the task, that the requester was entitled to it, or that a release was authorized. Those claims need boundary evidence and the evaluation and decision owners in the linked chapters.

### Instrument agent steps with open conventions

If you use OpenTelemetry, its GenAI semantic conventions define spans for agent work. An agent invocation is an `invoke_agent` span, and a tool call is an `execute_tool` operation. Sub-agent work can nest under the parent invocation. The conventions are at **Development** stability and now live in their own repository, so pin the instrumentation version and keep attribute names in one place to ease later renames. [6]

Prompts and responses are not recorded by default. Message content attributes such as input messages and system instructions are marked opt-in, so decide deliberately where to capture content: for example, fuller capture in a test environment and metadata only, or redacted content, in production, under the rules in [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md). [6] Spans, like the run record above, show what happened; they are not proof of correctness.

### Make budgets executable

Pick resource dimensions from the task's likely failure modes. A bounded read-only question may need elapsed-time, model-request, retrieval-call, iteration, and response-size ceilings. Another service may also need token, byte, or estimated-spend ceilings. Give each budget a unit, scope, measurement point, remaining-allowance behavior, and an outcome when exhausted. These are design choices, not universal numbers.

Account for each **physical attempt**. Before dispatching a model or tool operation, the runtime can check the remaining allowance. When an estimate is available beforehand, it can reserve allowance so concurrent work cannot oversubscribe the same run or shared pool. At dispatch, record the attempt against the budget even if the result is a timeout or unknown. Reconcile measured use after a response or billing report arrives. A reservation guards against avoidable new work; it does not prove the final charge, because accepted in-flight work can use resources after the limit decision.

Put these controls in the deterministic runtime, not in a model instruction. A retry uses the same run budget as the failed attempt, and nested retry paths need the same accounting, or a local retry limit can multiply into unbounded work. A budget that spans conversations, tenants, workers, or independent runs needs shared durable accounting and a defined reservation and reconciliation rule. A budget that does not span them gains nothing from a shared ledger.

Unknown cost stays `unknown`. It is not zero, not within budget, and not evidence that no charge will arrive. Record unavailable token or byte measurements as unknown rather than backfilling a default. If no pre-dispatch price estimate exists, your organization still has to decide whether the cost-controlled operation may be dispatched and under what governance. This chapter supplies no price list, provider estimate, or tested ceiling.

### Define a safe exhausted state and a real stop

When a limit is reached, stop **new work within that limit**. Record the measured, estimated, or unknown usage; the dimension that triggered the decision; the affected attempt; and the runtime termination reason. Then return the contract-defined result: a declared non-success outcome, a request for more information, a permitted escalation, or a clearly labelled partial result when the contract makes it safe. Do not trim material evidence to force a complete answer, retry an authorization denial as if it were a transient fault, or treat an unknown result as permission to repeat a potentially unsafe action.

A stop request and a confirmed cancellation are different facts. A stop can prevent later dispatch but may arrive while an operation is in flight. Mark that operation `cancelled` only when cancellation is confirmed; otherwise record it as in flight, unresolved, or completed according to the evidence. An undo, if possible, is a separate compensating action that stopping does not imply. For reconciling uncertain external effects, see [7.2](../../engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md).

Document the stop scope: one run, new admissions to an agent, or a capability that should no longer be invoked. Name the authorized operator, how a request is recorded, which new work is suppressed, how in-flight work is shown, and what evidence is needed before resuming. Treat this as a deactivation mechanism: NIST's AI RMF (MANAGE 2.4) calls for mechanisms to supersede, disengage, or deactivate AI systems that perform inconsistently with intended use. [7] Test it before you need it. Re-enabling service is a controlled change owned by [5.2](02-readiness-change-and-rollout.md), and response and escalation belong to [5.3](03-ownership-incidents-maintenance-and-retirement.md). A stop is not an incident declaration, a recovery authorization, or a release authorization.

### Recognize failure modes early

- **Tidy telemetry, wrong answer.** A model and a retrieval operation can each report normal results while the answer is unsupported. Do not label the run `complete` from operation status alone; keep the task-success and evaluation evidence the claim needs.
- **Any two values called a conflict.** Current material plus a clearly marked superseded record is a source-precedence case, not an equal-authority conflict. Record the source status and apply the declared selection rule, instead of inventing uncertainty or choosing a stale value.
- **Unbounded metric labels.** They can make the very aggregate used for alerting unreliable or expensive.
- **Retry handlers that reset the attempt counter.** They bypass an otherwise sensible ceiling.
- **Per-worker counters.** They can overspend a supposedly shared pool.
- **A "stopped" interface over an unknown in-flight call.** Show the unresolved state.
- **Collapsed dashboards.** A partial answer can look successful once terminal outcomes are merged.

The fix for all of these is a record that keeps identity, outcome, reason, attempt, budget scope, and in-flight state distinct, and exercising it against the configured control before production.

### Build an inspectable operating control record

The optional [operating control record template](../../templates/5.1/operating-control-record.yaml) makes the design reviewable without imposing a platform. Build it in this order.

1. Define the terminal outcomes, the exact condition for a successful user task, and the termination reasons and operation-result categories that could accompany them.
2. Map request, stable run, and physical-attempt identities, plus agent/version and capability/configuration identity. Add workflow, approval, or tenant references only if they exist and are permitted.
3. Name operator questions, minimal signals, safe aggregate categories, decision owner, and response route. Record any SLI/SLO/error budget, its measurement limits, window, and decision policy apart from resource ceilings.
4. For each resource dimension, state unit, scope, pre-dispatch check or reservation, in-flight treatment, reconciliation source, and exhausted-state behavior, and when cost remains unknown.
5. Define the stop scope and how requested, confirmed, unresolved, and resumed states appear. Link to the release, incident, privacy, evaluation, and uncertain-effect owners rather than copying them.
6. Check a planned example against the checklist below.

## Requirements

- **OPS-01** For every production run, the system MUST assign a stable run identifier and preserve its relation to the initiating request across recorded operations; it MUST identify the agent version and effective capability/configuration identity needed to interpret the run. Workflow and approval identifiers MUST be recorded only when those concepts apply and their use is permitted.
- **OPS-02** For every production agent, operators MUST be able to distinguish the contract-defined successful outcome from clarification, decline, escalation, cancellation, timeout, budget exhaustion, and failure; the system MUST attribute model and tool operations to the relevant run and record their outcome and duration.
- **OPS-03** Before production use, each agent MUST define and enforce runtime ceilings for applicable per-run dimensions, including elapsed time, model requests or iterations, tool calls, and model/tool output; where token or cost limits apply, those limits MUST be enforced or estimated at the earliest feasible boundary, with unknown cost kept unknown.
- **OPS-04** When a budget spans runs or workers, the responsible service MUST enforce it using shared durable accounting; when any limit is exhausted, the runtime MUST stop new work within that limit, emit the specific exhaustion outcome, and return only a contract-permitted partial result or a declared non-success outcome.
- **OPS-05** For every production agent, an authorized operator MUST have a documented mechanism to stop a run or prevent further agent work; the mechanism MUST define treatment of in-flight operations and preserve unresolved outcomes for reconciliation instead of implying that stopping reverses them.

These obligations add to the universal risk, access, privacy, evaluation, release, and lifecycle rules. They do not require a tracing product, dashboard product, particular data store, or prompt capture. For a small deployment, a structured run record and a reviewed operating view can meet them if they answer the same questions and enforce the same controls.

## Worked example

This is a fictional control design for the internal policy assistant (`example_id: POLICY-BUILD-001`, `use_case_id: internal-policy-assistance`, `packet_id: POLICY-OPS-001`, `status: illustrative-unexecuted`). Nothing in it was run.

The assistant is read-only. It answers from requester-permitted, approved policy material and returns uncertainty rather than inventing an answer. In the ordinary `travel-policy-current@fixture-2026-10-18.1` world, `employee-uk-104` has `approved-policy-read` permission and may access the current `travel-policy-2026@2026-10-01` source (GBP 220) and the approved historical `travel-policy-2024-superseded@2024-01-01` record (GBP 200). The current source supports the London answer; the superseded one is not authority for it. This is a **stale-distraction** condition, not a conflict.

The `POLICY-CONFLICT-004` variant is the conflict. It adds `travel-policy-2026-conflicting-amendment@2026-10-12` (GBP 260) as an equally authoritative current source the same employee may read, so the expected terminal outcome is `needs_information`. For `contractor-uk-204`, the retrieval boundary denies travel-policy access; the expected outcome is `declined`, with no restricted amount in the output. These are fixture expectations, not observed runs.

For teaching only, the per-run envelope allows three model requests, four retrieval calls, 15 seconds elapsed time, and an optional 12 seconds of active processing. The planned record ties a fictional request to a stable run identity, the candidate identity, the capability/configuration identity, and each retrieval and model attempt. Aggregate telemetry uses controlled fields (operation type, terminal outcome, termination reason), not the requester's identity or question.

In `POLICY-EXHAUSTION-008`, the remaining read-only retrieval budget is exhausted and a controlled retrieval timeout follows. A planned implementation stops new retrieval after the declared stop decision, keeps the last attempt and its timeout result, and records a reason such as `retrieval_budget_exhausted`. The terminal outcome is `failed`, distinct from the reason. It does not invent an amount, cite unavailable evidence, or call another retrieval to look complete.

Now imagine a stop request during an in-flight retrieval. The control blocks any later model or retrieval dispatch and records the request. It marks the retrieval cancelled only if that is confirmed; otherwise it stays unresolved for review. The read-only assistant has no external write to undo, and that does not carry over to a write-capable agent.

## Evidence and checklist

Before production traffic, inspect a representative record for a complete request-to-run link; stable run, attempt, agent/version, and capability/configuration identities; operation type, duration, and result; terminal outcome and, separately, termination reason; and each resource measurement or unknown value. Confirm that a resumed durable run keeps its run identity while identifying the attempt, that aggregate labels are bounded, and that detailed diagnostics follow [3.3](../03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).

Exercise the limits, including nested retries and concurrent attempts on shared budgets. Check that the pre-dispatch check or reservation blocks impermissible new work, every physical attempt is attributed, and reconciliation keeps unknown cost or uncertain completion instead of turning it into zero or success. For each exhaustion path, check the reason, the declared terminal outcome, and the absence of prohibited new work. This shows how the exercised control behaves; it does not show service reliability, semantic grounding, authorization, or a release decision.

Exercise the stop path during idle and in-flight work. Check the scope, suppression of later work, request record, and the difference between requested stop, confirmed cancellation, unresolved operation, and resumption. A parser-valid template or completed checklist is design evidence, not proof that the control works in production.

## References

[1]: https://opentelemetry.io/docs/concepts/signals/metrics/ "OpenTelemetry metrics"
[2]: https://opentelemetry.io/docs/concepts/signals/traces/ "OpenTelemetry traces"
[3]: https://opentelemetry.io/docs/concepts/semantic-conventions/ "OpenTelemetry semantic conventions"
[4]: https://sre.google/workbook/implementing-slos/ "Google SRE Workbook implementing SLOs"
[5]: https://sre.google/workbook/alerting-on-slos/ "Google SRE Workbook alerting on SLOs"
[6]: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md "OpenTelemetry GenAI agent spans"
[7]: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf "NIST AI Risk Management Framework 1.0"

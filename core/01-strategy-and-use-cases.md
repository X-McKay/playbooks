# 1. Strategy and use-case selection

This guide is for the developers who will build an agent. It helps you decide
whether an agent is the right tool for the job, how much authority to give the
first release, and how you will know it is working. The decisions you make
here shape the
[agent contract](07-agent-contract.md), the
[evaluation plan](10-evaluation.md), and the
[risk assessment](../advanced/04-risk-assessment.md), so it pays to make
them on purpose rather than discover them later.

## Start from the job, not the model

An agent is software that uses model output to choose or sequence actions.
What makes one risky is not the model but what its actions can do: the
authority they carry, the data they touch, whether they can be undone, and how
uncertain the decision behind them is.

So start with the job. Before you write a prompt or pick a model, write down:

- the task being improved and who does it today;
- how long it takes now and what goes wrong (your baseline);
- the decisions the agent would make; and
- what happens if one of those decisions is wrong.

If you cannot describe the baseline, you will not be able to show that the
agent improved anything. [Defining the problem](02-problem-definition.md)
turns these notes into a full brief.

## Should this be an agent?

Many good ideas for an agent are better built as something simpler. Compare
the options honestly:

| Option | Prefer it when |
| --- | --- |
| Deterministic workflow or rules | The inputs and the sequence of steps are known and stable. |
| Search or retrieval interface | People need to find information and can judge it themselves. |
| Single-call assistant | One model response, reviewed by a person, is enough. |
| Agent | Uncertainty in the inputs or in the sequence of actions is where the value is, and that value outweighs the cost of evaluating and controlling it. |

A quick test: if you can draw the steps as a flowchart that does not change
from one request to the next, build the flowchart. Reach for an agent when the
next step genuinely depends on what the previous one found.

Each step up the table adds work you will own. A multi-step agent has to
explain when it stops, when it escalates, what it consumes, and how it recovers
from failure. Several coordinating agents add more again; the
[Multi-agent systems](../multi-agent/01-principles-and-scope.md)
asks you to justify that choice separately.

## Start narrow and earn more authority

Most successful agents start by assisting and only later act on their own.
Three common starting points, in order of authority:

1. **Research assistant.** Retrieves approved documents and prepares a cited
   answer. Read-only.
2. **Change-preparation agent.** Drafts an update, and a person approves its
   exact content before anything changes.
3. **Service agent.** Carries out a narrow, reversible action under a limit,
   such as a refund below a set amount.

These map onto the playbook's
[execution classes](05-principles-and-scope.md#execution-classes):
the first is usually ephemeral, the second human-governed, and the third
durable or human-governed depending on its consequences. All three use the
same contract and release process; what differs is the controls around them.

Best practices:

- **Ship the read-only version first.** It produces evaluation data, tool
  interfaces, and user trust at very low risk, and most of that carries over
  when you add actions.
- **Treat new authority as a new capability.** Letting a purchasing assistant
  place orders instead of only preparing them is a new risk decision with new
  evidence, not a configuration flag.
- **Give the agent its own identity from the start.** A prototype that runs on
  your developer credentials hides what the agent actually needs. Replace them
  with scoped, per-agent credentials before anyone else uses it (see
  [zero-trust principles](03-zero-trust-principles.md)).
- **Do not let observed behavior define permissions.** Watching what the agent
  tries to do is a useful way to propose its access, but observation is
  incomplete and can capture mistakes or injected instructions. Grant what the
  declared purpose needs, nothing more.

## Write a one-page charter

A charter records why you are building the agent and the limits of the first
release. Keep it short enough that a reviewer reads all of it. It SHOULD name:

- the owners: who owns the outcome, who owns the code, and who is on call;
- the users and the task they need done;
- the inputs, outputs, and actions the agent is allowed;
- the worst consequence you accept, and the actions it must never take;
- the baseline and how you will measure improvement; and
- the exit criteria that end the trial or promote it.

```yaml
# Example charter. Values are illustrative, not policy defaults.
use_case: internal-knowledge-assistance
business_owner: knowledge-operations
technical_owner: agent-platform-pilot
operating_owner: knowledge-support-on-call
authority: retrieve-approved-documents-and-draft-answer
prohibited: [cross-tenant-search, external-send, credential-access]
baseline: manual-supported-question-resolution
pilot_exit:
  value: measured-resolution-time-improvement
  safety: no-known-critical-gate-failures
  operations: exercised-disable-and-recovery-procedure
  economics: approved-cost-per-successful-task
```

The `prohibited` list matters as much as `authority`. Each entry becomes a
test case and, later, a [hard gate](10-evaluation.md#hard-gates).

## Decide how you will know it works

Pick your measures before you test, and keep them separate. A single "agent
score" hides the difference between an agent that gives useful answers and one
that is safe to give authority to. Four measures cover most first releases:

| Measure | What it tells you | Watch out for |
| --- | --- | --- |
| Verified task success | The share of eligible tasks that met the correctness rubric and every required constraint. | Report abandoned, escalated, and timed-out tasks separately rather than dropping them. |
| Cost per verified success | Total model, tool, runtime, and review cost divided by successful tasks. | Failed attempts still cost money; include them. |
| Critical control failures | Any authorization, isolation, or approval violation, attempted or completed. | These are pass/fail gates. A good average never cancels one. |
| Time recovered | Baseline effort minus effort with the agent, including review and correction. | Generating output faster is not the same as saving people time. |

For each one, write down what is counted, over what population and period,
and who owns the definition. Segment results by release and task type so a
regression in one kind of task is not hidden by gains in another.

Best practices:

- **Measure the baseline first.** Without it, every result looks like
  progress.
- **Keep safety checks deterministic.** Use pass/fail tests for anything that
  must never happen, and reserve scored or judged evaluation for quality (see
  [release gates](10-evaluation.md#release-gates)).
- **Report the denominator.** Zero failures in twenty cases is evidence about
  those twenty cases, not proof the agent is safe.
- **Track service levels on their own.** Latency, tool error rate, and budget
  exhaustion can degrade while answers stay correct, and the reverse. Pick
  targets that fit the task: an interactive assistant and a multi-day workflow
  need different latency measures.

## Plan the path to production

Use cases move through discovery, a bounded pilot, controlled production, and
expansion. Each step widens what the agent can do or who can use it, so each
needs fresh evidence. The [operating model](04-operating-model.md#adopt-in-stages-on-evidence)
describes these stages and what moves a use case from one to the next.

Two habits make this easier:

- **Build the off switch early.** Before the pilot, confirm you can disable
  the agent without its cooperation and that new consequential actions stop
  promptly. Rehearse it once.
- **Keep what a failed pilot produced.** If the value hypothesis does not
  hold, stop the use case but keep its datasets, tool interfaces, and control
  tests. They make the next attempt cheaper.

## Common pitfalls

- **Building an agent for a flowchart.** The task had fixed steps, and a
  workflow would have been cheaper, faster, and easier to test.
- **Starting with too much authority.** The first release could act, so every
  quality problem was also a safety problem.
- **Assuming durability means correctness.** A durable workflow recovers where
  it was, but it does not make actions idempotent or reconcile the business
  record. You still design for both (see
  [durable execution](../advanced/01-durable-execution.md)).
- **Logging everything.** Full prompts and tool results turn telemetry into a
  sensitive data store. Default to metadata and redact content you keep (see
  [observability](11-observability.md)).
- **Hiding the controls.** Controls injected automatically are convenient
  until something fails and nobody can see why. Prefer explicit, versioned
  configuration you can inspect for any release.
- **Ignoring the cost of safety.** Approval steps, checks, and evaluations
  add latency and cost. Measure them so that safe defaults stay affordable
  instead of being switched off.

## Before you move on

You are ready for [defining the problem](02-problem-definition.md) when you
can answer yes to each of these:

- [ ] We compared an agent with simpler options and can say why it wins.
- [ ] The first release has the least authority that still tests the value.
- [ ] A charter names owners, allowed and prohibited actions, and exit
  criteria.
- [ ] We have a baseline and know how we will measure success, cost, and
  critical failures separately.
- [ ] We know how to switch the agent off.

This guide does not establish regulatory compliance. If your use case may be
regulated, involve the people who own that question early (see the
[regulatory screen](../advanced/04-risk-assessment.md#regulatory-and-prohibited-use-screen)).

# 2. Defining the problem

This guide is for the developers who will build the agent. It turns the notes
from [strategy and use-case selection](01-strategy-and-use-cases.md) into a
short brief: the job, what a good result looks like, the limits, the data,
the risks, and who owns what. The brief feeds the
[agent contract](07-agent-contract.md), the
[risk assessment](../advanced/04-risk-assessment.md), and the
[evaluation plan](10-evaluation.md). If you cannot write it,
you are not ready to build.

## Write the brief

Start with a few plain sentences. For example:

```text
Help employees understand company policies
using approved documents.
Show the source for each answer.
Ask for help when information is missing.
```

Each line hides a decision. Make each explicit before you write a prompt; each
becomes a field in the contract or a case in the evaluation set:

| Area | Questions to answer | In the example |
| --- | --- | --- |
| Purpose and people | Who are the users, what task do they need done, what is the current problem, and what improvement is expected? | Employees spend time searching for policies; answers should be faster and correct. |
| Information and access | Which documents, systems, and connections are needed? Who owns them, how current are they, and what is the actual user permitted to read? | Approved, current policy documents, filtered by what the asking employee may see. |
| A good result | What do representative requests look like, and what makes a response acceptable? | Correct, understandable, and supported by an approved, current source. |
| Limits and help | What actions are prohibited, and when must the agent stop or ask for help? | Never guess when evidence is missing, read restricted documents, or change employee records. |

## Agree what success looks like

Choose your measures and acceptance criteria before you test, and compare
against today's process: does the agent improve the outcome enough to justify
its cost? Work backwards from the consequence of a wrong answer or action.
A policy answer, for example, needs a valid supporting source, and restricted
information must stay restricted. There is no universal pass score; speed and
cost targets depend on the task and expected usage.

Best practices:

- **Agree targets with users and the owner.** Settle acceptable task results,
  maximum wait time and cost, and the checks every release must pass.
- **Include the hard cases.** Difficult tasks and failure cases tell you more
  than good examples.
- **Repeat trials and use human review where judgment is needed.** Record
  failures and uncertainty, not only the average.
- **Keep safety checks pass/fail.** A high average does not cancel a failed
  required safety check (see
  [multi-run evaluation](10-evaluation.md#multi-run-evaluation)
  and [release gates](10-evaluation.md#release-gates)).

## Set limits on cost, time, and volume

Answer these early; they become the agent's
[budgets](../advanced/02-cost-optimization.md#budget-hierarchy):

- How long can users wait for a complete task, including slow dependencies and
  failures?
- What is the budget per successful task and per month?
- How many requests and simultaneous users are expected?
- What does the user see when a limit is reached?

Count everything in the cost: model calls, tools, infrastructure, repeated
attempts, and human review.

## Map the data and connections

List the documents, records, and services the agent needs, who owns each,
and how the agent will reach them. Check access, data quality, freshness,
availability, and rate limits, and test access early rather than discovering
a missing permission in the pilot.

Decide what information may be sent to a model, stored, or logged, and for
how long. Resist adding sources "in case": more data or broader access does
not automatically improve the result, and every added source is added
authority.

## Name the risks and what needs approval

Ask what could go wrong, who could be affected, and whether it can be undone.
Consider incorrect advice, exposure of private information, misleading
instructions embedded in documents, unwanted changes, and repeated actions.

Then narrow the design:

- **Limit the allowed actions** to what the purpose needs.
- **Require review** where an error could cause serious harm.
- **Define prohibited actions and stopping conditions.**
- **Pair each important risk** with a prevention or detection measure and the
  person responsible for responding.

The [risk assessment](../advanced/04-risk-assessment.md#scenario-method)
turns this list into scored scenarios.

## Name the owners

You need three owners: a business owner who accepts the outcome, a developer
responsible for changes, and an operating owner who handles alerts, support,
and stopping the agent. One person may hold more than one role.

Also agree who approves access, maintains source information, reviews
uncertain cases, and accepts remaining risk, and confirm those people have
the time and authority to act. The [operating model](04-operating-model.md)
explains which decisions each owner makes and where you need sign-off.

## Record dependencies and impacts

Upstream is what the agent relies on; downstream is who or what relies on its
output.

| Direction | In the example | What to record |
| --- | --- | --- |
| Upstream | Policy documents, document search, and access services. A stale policy or unavailable search prevents a reliable answer. | Owner, failure behavior, and change notification for each dependency. |
| Downstream | An employee submits an expense based on the answer. A wrong answer creates rejected claims or extra work. | Recipient, possible effect, required review, and recovery options for each output. |

Decide how missing or uncertain results are communicated before they affect
another process.

## Agree the two readiness decisions

Every agent faces two separate decisions. Agree their criteria now, while you
define the problem, so nobody moves the bar after the build.

### Ready to test with users?

User acceptance testing checks whether representative users can complete real
tasks.

- Basic tests and evaluations meet the agreed entry criteria.
- Important access and safety checks pass, and no known serious issue makes
  the trial unsafe.
- The trial uses an approved test environment and data. Users know the
  limits, how to report problems, and who can stop the trial.

### Ready for production?

The agent must be useful to users and safe to operate in its real
environment.

- The business owner accepts the user-testing results, and the required
  quality, cost, response-time, and safety criteria pass.
- Required access controls and protections are verified in the environment
  the agent will run in, not only in testing.
- Monitoring, support, stop, and recovery procedures are ready. Use begins
  with a limited audience and is watched closely.

You record the second decision through the
[production-readiness checklist](12-production-readiness.md).

## Common pitfalls

- **A brief that only describes the happy path.** Without prohibited actions
  and stopping conditions, there is nothing to test the limits against.
- **Success defined after the demo.** Criteria chosen once results are in
  tend to fit the results.
- **Broad access "for now".** Extra sources and permissions granted in a
  prototype become the production authority unless someone removes them.
- **Owners in name only.** A named owner without time or authority cannot
  approve access, answer alerts, or stop the agent.

## Before you move on

You are ready for [zero-trust principles](03-zero-trust-principles.md) when
you and the owner agree on a brief that covers:

- [ ] the job, users, success criteria, and cost, time, and volume limits;
- [ ] the data and connections, with owners and handling rules;
- [ ] risks, prohibited actions, and what needs review;
- [ ] named owners and upstream and downstream dependencies; and
- [ ] the criteria for both readiness decisions.

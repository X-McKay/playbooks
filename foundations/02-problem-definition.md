# 2. Defining the problem

Describe the job, who it helps, and what should improve. Agree on what a good
result looks like and what the agent must never do. This brief is the input to
the [agent contract](../agent-playbook/03-agent-contract.md), the
[risk assessment](../agent-playbook/13-risk-assessment.md), and the
[evaluation plan](../agent-playbook/07-evaluation.md); a team that cannot write
it is not ready to build.

## The brief

A short example brief:

```text
Help employees understand company policies
using approved documents.
Show the source for each answer.
Ask for help when information is missing.
```

Each line carries a decision the team must make explicit:

| Area | Questions to answer | In the example |
| --- | --- | --- |
| Purpose and people | Who are the users, what task do they need done, what is the current problem, and what improvement is expected? | Employees spend time searching for policies; answers should be faster and correct. |
| Information and access | Which documents, systems, and connections are needed? Who owns them, how current are they, and what is the actual user permitted to read? | Approved, current policy documents, filtered by what the asking employee may see. |
| A good result | What do representative requests look like, and what makes a response acceptable? | Correct, understandable, and supported by an approved, current source. |
| Limits and help | What actions are prohibited, and when must the agent stop or ask for help? | Never guess when evidence is missing, read restricted documents, or change employee records. |

## Success criteria

Choose measures and acceptance criteria before testing. Compare with today's
process: does the agent improve the outcome enough to justify its cost? Include
difficult tasks and failure cases, not only good examples.

Start from the consequences of a wrong answer or action. Agree with users and
the owner on acceptable task results, maximum wait time and cost, and the
checks that every release must pass. A policy answer, for example, needs a
valid supporting source, and restricted information must stay restricted.
Speed and cost targets depend on the task and expected usage; there is no
universal pass score.

Use representative cases, repeated trials, and human review where judgment is
needed. Record failures and uncertainty. A high average does not cancel a
failed required safety check (see
[multi-run evaluation](../agent-playbook/07-evaluation.md#multi-run-evaluation)
and [release gates](../agent-playbook/07-evaluation.md#release-gates)).

## Constraints: cost, response time, and volume

- How long can users wait for a complete task, including slow dependencies and
  failures?
- What is the budget per successful task and per month?
- How many requests and simultaneous users are expected?
- What does the user see when a limit is reached?

Include model calls, tools, infrastructure, repeated attempts, and human review
in the cost. These answers become the agent's
[budgets](../agent-playbook/09-cost-optimization.md#budget-hierarchy).

## Data, information, and connections

List the required documents, records, and services, their owners, and how the
agent will reach them. Check access, data quality, freshness, availability,
and rate limits.

Decide what information may be sent to a model, stored, or logged, and for how
long. Identify missing data and test access early. More data or broader access
does not automatically improve the result, and every added source is added
authority.

## Risks and what needs approval

Ask what could go wrong, who could be affected, and whether it can be undone.
Consider incorrect advice, exposure of private information, misleading
instructions embedded in documents, unwanted changes, and repeated actions.

Limit allowed actions. Require review where an error could cause serious harm,
and define prohibited actions and stopping conditions. For each important
risk, name a prevention or detection measure and the person responsible for
responding. The
[risk assessment](../agent-playbook/13-risk-assessment.md#scenario-method)
turns this list into scored scenarios.

## Owners

Name a business owner who accepts the outcome, a developer responsible for
changes, and an operating owner who handles alerts, support, and stopping the
agent. One person may hold more than one role.

Agree who approves access, maintains source information, reviews uncertain
cases, and accepts remaining risk. Confirm that these people have the time and
authority to act. The [operating model](04-operating-model.md) describes how
these roles fit an organization.

## Dependencies and impacts

Upstream is what the agent relies on; downstream is who or what relies on its
output.

| Direction | In the example | What to record |
| --- | --- | --- |
| Upstream | Policy documents, document search, and access services. A stale policy or unavailable search prevents a reliable answer. | Owner, failure behavior, and change notification for each dependency. |
| Downstream | An employee submits an expense based on the answer. A wrong answer creates rejected claims or extra work. | Recipient, possible effect, required review, and recovery options for each output. |

Decide how missing or uncertain results are communicated before they affect
another process.

## Two readiness decisions

Every agent faces two separate decisions. Agree on their criteria while
defining the problem, not after building.

### Ready to test with users?

User acceptance testing checks whether representative users can complete real
tasks.

- Basic tests and evaluations meet the agreed entry criteria.
- Important access and safety checks pass, and no known serious issue makes the
  trial unsafe.
- The trial uses an approved test environment and data. Users know the limits,
  how to report problems, and who can stop the trial.

### Ready for production?

The agent must be useful to users and safe to operate in its real environment.

- The business owner accepts the user-testing results, and the required
  quality, cost, response-time, and safety criteria pass.
- Required access controls and protections are verified in the environment the
  agent will run in, not only in testing.
- Monitoring, support, stop, and recovery procedures are ready. Use begins with
  a limited audience and is watched closely.

The second decision is recorded through the
[production-readiness checklist](../agent-playbook/11-production-readiness.md).

## Ready to move on

The owner and developer agree on a brief that covers the job, success
criteria, constraints, information and connections, risks, responsibilities,
dependencies, and the criteria for both readiness decisions.

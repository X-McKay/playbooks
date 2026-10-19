# 1.1 Defining the Problem

**Status:** 0.5.0-draft.2 — draft

**Audience:** Process and service owners, builders, and people who represent users or affected people

**Applicability:** Every proposed production agent, before its contract and design are settled. Discovery can be light for a small task, but choosing a technology does not clarify an unclear problem.

**Reader question:** What user problem is worth solving, for whom, in what current context, and what stays outside the work?

[Part 1 — Problem Definition and Planning](README.md) · [Playbook applicability](../../applicability.md) · [Playbook home](../../README.md)

## Start with the work, not the solution

A problem brief is a short, checkable account of a person's work: who is trying to do what, how they do it today, where it breaks down, and what a useful result would let them do next. It feeds later decisions on requirements, alternatives, risk and delivery. It is not an agent contract or implementation plan, and it does not show that a candidate is useful or safe.

The order matters. Human-centred design standards separate understanding the context of use and specifying requirements from producing design solutions. [1] [5] The NIST page lists an explicit understanding of users, tasks and environments among its principles and describes the process as iterative. Public-service guidance likewise says to understand the full context of the user's goal and to focus on the problem, not a particular solution. [2]

A request often arrives as a solution: "build an assistant," "add a model," "automate the policy question." Treat it as a lead. It may point to a real need, or hide a simpler issue such as an unclear source of truth, an avoidable handoff, or a process that makes users repeat work.

This chapter sets the problem boundary. [1.2](02-requirements-success-criteria-and-measurable-targets.md) turns the need into outcomes and acceptance criteria, [1.3](03-agent-suitability-and-alternatives.md) compares alternatives, and [1.4](04-initial-risk-data-ownership-and-delivery-plan.md) records harms, data, authority, owners and delivery limits.

## Terms and a working model

A **need** is the progress a person or group must make in a situation. A **request** is what someone asks for: a feature, a system or a process change. A request is evidence about the need, not proof that its proposed form is necessary. "Give employees a policy chatbot" is a request. "Employees need to find the current policy for their trip without searching conflicting documents" is a candidate need.

A **symptom** is an observed or reported difficulty, such as repeated searching, waiting for a handoff or abandoned tasks. A **cause** creates or contributes to a symptom. A **hypothesis** is an explanation that still needs checking. Several causes can produce one symptom, and different groups may have different causes. Label hypotheses so the brief does not present an unmeasured pain point as fact. The assumed problem may not be the real one, so test assumptions early. [2]

A **user task** is the person's real work, in their terms. It starts with a trigger and ends when the person can make progress, not when a system returns text. An **agent task** is a bounded contribution a system could make to it, such as finding permitted current policy evidence and presenting an answer or the uncertainty. It is a design candidate, not a restatement of the need.

**Scope** is the task classes, users, inputs, results and dependencies the brief covers, plus explicit exclusions. A **stakeholder** is anyone who does the task, supplies an input, owns a dependency, receives a result, is affected by a failure, or makes a relevant decision. A downstream claimant, policy owner or person whose data could be exposed may matter even if they never use the system.

```text
stakeholders and context
  → user task and current journey
  → observed or reported symptoms
  → possible causes and assumptions
  → bounded problem and desired work outcome
  → candidate solutions, including process change or no new system
```

The arrows do not prove causation. Record the evidence behind each step and leave a step open when evidence is missing.

## Discover the current work proportionately

Discovery need not be a long research program. Depth depends on uncertainty, variation among users, the cost of misunderstanding, and existing evidence. A short, bounded task may need only a walk-through and a look at inputs and handoffs. A task that varies by role, source, permission or consequence needs more perspectives. Use the smallest mix of these that fits:

- **Walk through the current task.** Ask what triggers it, what the person must interpret, where they wait or rework, and what they do when information is missing. Use a real or safely reconstructed task, not a feature discussion.
- **Collect representative task examples.** Record the input or question, the context, the result the person needs, and the next action it supports. Include a hard case where plausible: missing or conflicting information, different permissions, an exception or an out-of-scope request.
- **Inspect process evidence.** Request records, source-change records, handoff queues and support themes can test a reported difficulty, but show a benefit only if their population and limits are clear.
- **Record uncertainty, not false precision.** A pain point may be reported, observed in a few tasks, or unmeasured. Say which. Do not turn "people may spend time searching" into a claimed delay or cost.

The U.S. Digital Services Playbook recommends learning from current and prospective users, documenting goals, needs and behaviours, finding pain points in the current journey, and placing the project in the wider experience. [3] It prescribes no research method or sample size.

### Follow the task across boundaries

Name what happens before and after the proposed contribution. Upstream dependencies include information, people, services, access decisions, and the process that says whether a source is current. For each material one, describe what happens if it is absent, stale, in conflict, or has changed permissions or ownership. Data and risk treatment belongs in 1.4.

Also identify who relies on the result and what decision or next step it informs. This shows where an incomplete or misleading result could cause rework, delay or a poor decision.

### Test causes before automating symptoms

A process fix can make an agent unnecessary. If nobody marked the current policy source, clarifying ownership and status may fix the cause. If requests arrive incomplete, better intake may remove the clarification loop. If a handoff is vague, a routing rule or accountable contact may help. This is not an argument against agents; it guards against treating AI as the only response. Public-service guidance says to design around user needs, not pre-selected solutions (generative AI included), and to consider alternatives to creating a service. [4] Record a possible process change next to a possible system contribution, then let 1.3 assess both on the same task.

## Build a problem brief

Keep the brief short and plain. Separate these elements so a reader can challenge one without rejecting the rest.

1. **State the user task and desired work outcome.** Name each user group, its trigger, the progress it needs, and the kind of result that would help. Describe groups separately when permissions, knowledge or goals differ.
2. **Describe today's process and evidence.** Show how the task is done now, including workarounds. State the specific difficulty and its evidence status. Mark a candidate cause as a hypothesis until checked.
3. **Bound inputs, results and variations.** For each in-scope task class, give a representative input and the needed result, plus a plausible material variation, not only the happy path.
4. **Map relationships.** List upstream dependencies with their failure or change effects, and any downstream consumer with the decision the result informs. Leave owners, data handling and authority to 1.4.
5. **Make scope and uncertainty visible.** State exclusions, unverified assumptions and questions that could change the brief. Write any candidate implementation as a proposal, not part of the problem. A later decision may conclude that no agent is needed.

The [problem brief template](../../templates/1.1/problem-brief.yaml) shows these fields using the shared fictional record.

## Common pitfalls

- **Starting from the solution.** The brief describes an assistant, not a user's work, so every later option looks like a variant of the assistant.
- **No baseline.** Nobody records how the task is done today, how long it takes or how often it fails, so later claims of improvement have nothing to compare against. If you cannot measure it yet, record that.
- **One pooled user.** Groups with different permissions or goals are merged into "employees," which hides who is actually harmed or helped.
- **Happy path only.** The brief omits missing, conflicting or out-of-scope inputs, so they first appear in production.
- **Scope creep.** Early success on a narrow task is read as a reason to widen users, data or actions. Treat any widening as a new problem definition and revisit 1.1 to 1.4.

## Requirements

- **PROBLEM-01** When a team proposes a production agent, it MUST identify the intended user group or groups, the task each group needs to complete, and the current process or alternative they use, including the specific difficulty the proposal aims to address.
- **PROBLEM-02** For each in-scope task class, the brief MUST describe at least one representative input and the kind of result the user needs, and MUST include a material variation such as missing information, conflicting information, or an out-of-scope request where that variation is plausible.
- **PROBLEM-03** When a task depends on upstream information, people, or services, the brief MUST name those dependencies and their relevant failure or change effects; when another person or process consumes the result, the brief MUST identify that consumer and the decision or next step the result may inform.
- **PROBLEM-04** Before the agent contract is approved, the brief MUST distinguish the user problem and desired work outcome from proposed implementation choices, and MUST record material scope exclusions and assumptions that remain unverified.

## Worked example: fictional internal policy assistance

The planning record `POLICY-PLAN-001` is fictional. It covers `internal-policy-assistance`: permission-filtered, read-only help with internal policy questions, with no write or approval capability.

The request might be, "Create an assistant that answers travel-policy questions." In user terms: employees need the current policy that applies to a trip so they can prepare a claim or know what to ask next. Today they search policy documents and, if still unclear, ask a colleague or the policy owner. The record labels repeated searching a **reported candidate difficulty**, with no frequency or duration.

One representative task: an employee asks, "What is the hotel limit for a work trip to London?" The needed result is an understandable answer grounded in a current, approved source the requester may access, or a clear `needs_information` outcome when the evidence is absent or conflicts. In the fictional `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` states GBP 220, while `travel-policy-2024-superseded@2024-01-01` is superseded and has a different amount.

The brief records two material variations. If the current permitted source is unavailable, a definite amount would not serve the user; useful uncertainty or a route to clarification would. If two equally authoritative current permitted sources conflict, picking the newer-looking one is a guess, not a justified answer. It also notes an access context: `contractor-uk-204` may not read the named policy documents, so the amount must not be revealed.

The dependency map names current policy content, its source-status process, and permission information at the retrieval boundary. The employee is the downstream consumer, using the answer to prepare a travel claim. Exclusions: the assistance does not change employee records, approve travel, decide reimbursement eligibility, or answer from documents the requester cannot access.

The cause stays open: unclear source status, access limits, document wording, a poor handoff, or a mix. Fixing the source-of-truth process might remove the need for a new system, and a fixed workflow might later beat an agent. This chapter makes neither choice.

## Evidence and handoff

A brief is ready for the next decision when a reader can see the task, its boundary and the status of its evidence without guessing what has not been learned. A reviewed brief, representative task record, light process map and dependency notes are enough at this stage. They are not proof of user value, safety or readiness. Before handing the brief on, check that:

- users, affected stakeholders, user task and desired outcome are distinct from the proposed system contribution;
- the current process and a specific difficulty are described, with observations, reports and hypotheses labelled honestly;
- each in-scope task class has a representative input, needed result and plausible material variation;
- upstream dependencies and downstream consumers show their failure, change or decision effects;
- exclusions and unverified assumptions can be found without reading an implementation plan; and
- the brief links to the success record, the alternatives decision and the initial risk/data/ownership record instead of duplicating them.

## References

[1]: https://www.nist.gov/itl/iad/human-centered-technologies/human-factors-human-centered-design "Human Centered Design (NIST page, no longer updated)"
[2]: https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs "Understand users and their needs"
[3]: https://playbook.usds.gov/ "Digital Services Playbook"
[4]: https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem "Solve a whole problem for users"
[5]: https://scc-ccn.ca/standardsdb/standards/8169649 "ISO 9241-210:2019 Ergonomics of human-system interaction, Part 210: Human-centred design for interactive systems"

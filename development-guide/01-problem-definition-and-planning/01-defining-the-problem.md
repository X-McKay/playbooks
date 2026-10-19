# 1.1 Defining the Problem

**Status:** 0.5.0-draft.2 — Part 1 refined draft; proposed, not adopted

**Audience:** Process and service owners, builders, and people representing intended users or affected people

**Applicability:** Every proposed production agent before its contract and design are settled. The depth of discovery can fit the task, but an unclear problem is not made clear by choosing a technology.

**Reader question:** What user problem is worth addressing, for whom, in what current context, and what must remain outside the proposed work?

[Part 1 — Problem Definition and Planning](README.md) · [Playbook applicability](../../applicability.md) · [Playbook home](../../README.md)

## Start with the work, not the solution

A problem brief is a concise, inspectable account of a person’s work and the situation around it. It explains who is trying to accomplish what, how they do it today, where the current journey breaks down, and what a useful result would let them do next. It is an input to later decisions about requirements, alternatives, risk, and delivery. It is not an agent contract, an implementation plan, or evidence that a candidate is useful or safe.

This ordering is deliberate. Human-centred design guidance distinguishes understanding the context of use and specifying requirements from producing design solutions; it starts with explicit understanding of users, tasks, and environments. [1] Public-service guidance similarly advises teams to understand the full context of the user’s goal rather than one interaction, and to focus on the problem rather than a particular solution. [2] Those are useful foundations for this chapter, not additional adopted requirements.

A request can arrive already dressed as a solution: “build an assistant,” “add a model,” or “automate the policy question.” Treat that phrasing as a lead to investigate, not as the problem statement. It may identify a real need, but it may also conceal a simpler issue such as an unclear source of truth, an avoidable handoff, or a process that asks users to repeat work.

This chapter establishes the problem boundary. [1.2 Requirements, Success Criteria, and Measurable Targets](02-requirements-success-criteria-and-measurable-targets.md) turns a bounded need into outcomes and acceptance criteria. [1.3 Agent Suitability and Alternatives](03-agent-suitability-and-alternatives.md) compares process change, simpler systems, and an agent. [1.4 Initial Risk, Data, Ownership, and Delivery Plan](04-initial-risk-data-ownership-and-delivery-plan.md) records harms, data, authority, owners, and delivery constraints. Keeping those decisions separate makes it easier to see what is known, proposed, and still unresolved.

## Terms and a working model

A **need** is the progress a person or group needs to make in a situation. A **request** is what someone asks for, which may be a feature, system, or process change. The request is evidence about the need, not proof that its proposed form is necessary. For example, “give employees a policy chatbot” is a request; “employees need to determine the current policy that applies to their trip without searching conflicting documents” is a candidate need.

A **symptom** is an observable or reported difficulty: a user searches repeatedly, waits for a handoff, receives inconsistent guidance, or abandons a task. A **cause** is a factor that creates or contributes to that difficulty. A **hypothesis** is a proposed explanation that still needs checking. Several causes can contribute to one symptom, and the same reported symptom can affect different user groups for different reasons. Labeling a hypothesis as a hypothesis protects the brief from presenting an unmeasured pain point as fact. Guidance on user needs makes the same practical point: the initially assumed problem may not be the one that needs solving, so assumptions deserve early testing. [2]

A **user task** is the person’s real-world work, described in their terms and context. It begins with a trigger and ends when the person can make progress, not when a system returns text. An **agent task** is a proposed, bounded contribution a system could make to that user task, such as finding permitted current policy evidence and presenting a response or uncertainty. It is a design candidate, not a restatement of the user need. The distinction prevents a response from being mistaken for a completed human task.

**Scope** identifies the task classes, users, inputs, results, dependencies, and circumstances the brief covers, as well as explicit exclusions. A **stakeholder** is anyone who performs the task, supplies an input, owns a dependency, receives a result, is affected by a failure, or makes a relevant decision. A user can be a stakeholder, but a downstream claimant, policy owner, support person, or person whose information could be exposed may matter even when they never use the proposed system.

A useful working model moves in this direction:

```text
stakeholders and context
  → user task and current journey
  → observed or reported symptoms
  → possible contributing causes and assumptions
  → bounded problem and desired work outcome
  → candidate solutions, including process change or no new system
```

The arrows are not proof of causation. They are a reminder to capture the evidence behind each step and to leave a step open when evidence is missing. The result is a brief that can survive a change in proposed technology.

## Discover the current work proportionately

Discovery need not become a lengthy research program. The appropriate depth depends on uncertainty, variation among users, consequence of a wrong understanding, and the amount of existing evidence. A short, bounded task may be clarified through a representative task walk-through and a review of the current inputs and handoffs. A task that varies by role, source, permission, or downstream consequence benefits from more than one perspective and a clearer view of the journey.

Use the smallest credible mix of these activities for the uncertainty at hand:

- **Observe or walk through the current task.** Ask what triggers it, what the person sees, what they must interpret, where they wait or rework, and what they do when information is missing. Prefer an actual or safely reconstructed task to a feature discussion.
- **Collect representative task examples.** Record the input or question, relevant context, the result the person needs, and the next action it supports. Include a material hard case when plausible: missing information, conflicting information, different permissions, an exception, or an out-of-scope request.
- **Inspect available process evidence.** Existing request records, source-change records, handoff queues, support themes, or policy-owner questions can help test a reported difficulty. They do not demonstrate a benefit unless their population and limitations are clear.
- **Record uncertainty rather than manufacture precision.** A pain point may be reported, observed in a small set of tasks, or unmeasured. Say which. Do not turn “people may spend time searching” into a claimed delay, frequency, or cost without supporting evidence.

The U.S. Digital Services Playbook recommends learning from current and prospective users, documenting goals, needs, and behaviours, identifying pain points in the current journey, and locating the project within the broader experience. [3] Here, that supports a practical recommendation to examine both the task and its surrounding process. It does not prescribe a research method, participant count, metric, or organizational role for this draft.

### Follow the task across boundaries

A brief becomes more decision-useful when it names what happens before and after the proposed contribution. Upstream dependencies can include information, people, services, access decisions, or a process that establishes whether a source is current. For each material dependency, describe the relevant effect of absence, staleness, conflict, changed permissions, or changed ownership. A detailed data and risk treatment belongs in 1.4; the problem brief only makes the dependency and its task effect visible.

Downstream context matters too. Identify who receives or relies on the result and what decision, handoff, or next step it may inform. This is not an assertion that a result is authoritative or that a downstream actor may act without checking it. It is a way to see where an incomplete or misleading result could create rework, delay, or a poor decision.

### Test causes before automating symptoms

A proposed agent can be premature when a process improvement removes the difficulty. If people cannot find a policy because the policy owner has not marked a current source, clarifying ownership and source status may address the cause. If a task begins with a repeated incomplete request, improving the intake information may remove the repeated clarification. If a handoff is vague, a clearer routing rule or accountable contact may improve the experience without a new system.

This is not an argument against agents. It is a way to avoid treating AI as the only possible response to a symptom. Public-service guidance explicitly advises designing around user needs rather than technologies or pre-selected solutions, including generative AI, and considering alternatives to creating a service. [4] Record a possible process change alongside a possible system contribution, then let 1.3 assess the alternatives on the same bounded task.

## Build a problem brief

A brief is a compact planning record, not a polished sales case. Start in plain language and separate the following elements so a reader can challenge one without discarding the whole account.

1. **State the user task and desired work outcome.** Name each relevant user group, its trigger, the progress it needs to make, and the kind of result that would help. Describe different groups separately when their permissions, knowledge, or end goals differ.
2. **Describe today’s process and evidence.** Show how the task is completed now, including alternatives people use. State the specific reported or observed difficulty and its evidence status. Mark a candidate cause as a hypothesis until it is checked.
3. **Bound inputs, results, and variations.** For every in-scope task class, include a representative input and the kind of result the user needs. Add a plausible material variation rather than documenting only the happy path. This gives later requirements and evaluation work something concrete to address.
4. **Map task-relevant relationships.** List upstream information, people, or services and their failure or change effects. List any downstream consumer and the decision or next step the result may inform. Keep a dependency owner, data-handling detail, and authority decision for 1.4 unless it is necessary to explain the current task.
5. **Make scope and uncertainty visible.** State exclusions, unverified assumptions, and questions that could change the brief. Write any candidate implementation as a proposal, not as part of the problem statement. A later decision may conclude that no agent is needed.

The accompanying [problem brief template](../../templates/1.1/problem-brief.yaml) illustrates these fields using the shared fictional planning record. It is a neutral planning aid, not a required form, an implementation specification, or evidence that the fictional candidate has been reviewed or executed.

## Requirements

The following proposed requirements are unchanged. They set the minimum content of a problem brief; the surrounding guidance explains how to make that content credible without adding a particular research method or implementation.

- **PROBLEM-01** When a team proposes a production agent, it MUST identify the intended user group or groups, the task each group needs to complete, and the current process or alternative they use, including the specific difficulty the proposal aims to address.
- **PROBLEM-02** For each in-scope task class, the brief MUST describe at least one representative input and the kind of result the user needs, and MUST include a material variation such as missing information, conflicting information, or an out-of-scope request where that variation is plausible.
- **PROBLEM-03** When a task depends on upstream information, people, or services, the brief MUST name those dependencies and their relevant failure or change effects; when another person or process consumes the result, the brief MUST identify that consumer and the decision or next step the result may inform.
- **PROBLEM-04** Before the agent contract is approved, the brief MUST distinguish the user problem and desired work outcome from proposed implementation choices, and MUST record material scope exclusions and assumptions that remain unverified.

## Worked example: fictional internal policy assistance

The shared planning record `POLICY-PLAN-001` is fictional and unexecuted. It considers `internal-policy-assistance`: permission-filtered, read-only help with internal policy questions. The record does not grant write or approval capability, select an architecture, report a user study, or claim a delivered benefit.

The initial request might be, “Create an assistant that answers travel-policy questions.” The problem brief rewrites that request in user terms: employees need to determine the current policy that applies to a trip so they can prepare a claim or decide what information to obtain next. Today, an employee may search policy documents and, when the answer remains unclear, ask a colleague or the policy owner. The planning record labels repeated searching as a **reported candidate difficulty**; it does not assert how often it occurs or how long it takes.

One representative task is an employee asking, “What is the hotel limit for a work trip to London?” The needed result is an understandable response grounded in a current, approved source the requester may access, or a clear `needs_information` outcome when the evidence is absent or conflicts. In the fictional `travel-policy-current` fixture, `travel-policy-2026@2026-10-01` states GBP 220, while `travel-policy-2024-superseded@2024-01-01` is a superseded record with a different amount. These are controlled fictional facts, not real policy or a measured system result.

The brief records two material variations. If the current permitted source is unavailable, a definitive amount would not serve the user task; the relevant result is useful uncertainty or a route to clarification. If two equally authoritative current permitted sources conflict, selecting the newer-looking source would be a hypothesis about resolution, not a justified answer. The brief also notes a different access context: `contractor-uk-204` is not permitted to read the named policy documents. That is a scope and dependency fact in the fictional world, not a reason to disclose the amount or invent a permission decision.

A small dependency map names current policy content and its source-status process, as well as permission information at the retrieval boundary. It identifies the employee as a downstream consumer who may use the answer while preparing a travel claim. The exclusions are equally important: the planned assistance does not change employee records, approve travel, decide reimbursement eligibility, or answer from documents a requester cannot access.

The cause remains open. The difficulty could stem from unclear source status, access limitations, document wording, a poor handoff, or some combination. Improving the source-of-truth process or clarifying ownership could reduce the need for a new system. A fixed retrieval-and-answer workflow might later be preferable to an agent, but this chapter does not make that choice. The next records define success in 1.2, compare alternatives in 1.3, and assess data, authority, and risk in 1.4.

## Evidence and handoff

A problem brief is ready to inform the next decision when a responsible reader can see the task, its boundary, and the status of its evidence without inferring what has not been learned. A reviewed brief, representative task record, lightweight process map, and dependency notes can be adequate evidence at this stage; their form and depth should fit the uncertainty and consequence. They are not proof of user value, safety, authorization, or release readiness.

Before handing the brief to the next chapter, check that:

- the users, affected stakeholders, user task, and desired work outcome are distinguishable from the proposed system contribution;
- the current process or alternative and a specific difficulty are described, with observations, reports, and hypotheses labeled honestly;
- each in-scope task class has a representative input, needed result, and plausible material variation;
- upstream dependencies and downstream consumers show their relevant failure, change, or decision effects;
- scope exclusions and unverified assumptions can be found without reading an implementation plan; and
- the brief links to a success record, an alternatives decision, and an initial risk/data/ownership record rather than duplicating their decisions.

The next step is not to declare the candidate ready. Use the brief to make success criteria concrete in [1.2](02-requirements-success-criteria-and-measurable-targets.md), compare whether an agent is warranted in [1.3](03-agent-suitability-and-alternatives.md), and record constraints and accountable ownership in [1.4](04-initial-risk-data-ownership-and-delivery-plan.md).

## References

[1]: https://www.nist.gov/itl/iad/human-centered-technologies/human-factors-human-centered-design "Human Centered Design"
[2]: https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs "Understand users and their needs"
[3]: https://playbook.usds.gov/ "Digital Services Playbook"
[4]: https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem "Solve a whole problem for users"

# Agent Contract Design Examples

## Example Request

> Create a support agent that answers account questions, reads ticket history, and proposes—but cannot issue—refunds.

Expected decisions:

- Use ephemeral execution because the enabled capabilities are read-only and the request is bounded.
- Assess privacy, security, legal, operational, and reputational scenarios. Set
  medium governance only if the highest inherent scenario and all mandatory
  floors support it.
- Return a typed `SupportResponse` with answer, evidence, proposed action, and escalation reason.
- Allow read-only account and ticket tools.
- Exclude the refund mutation tool; represent refund requests as proposals requiring a separate authorized path.
- Add hard eval gates for fabricated account facts and unauthorized actions.

## Minimal Specification Shape

```yaml
name: support-agent
version: 1
owner: customer-platform
purpose: Answer account questions and propose support actions.
non_goals:
  - Issue refunds
execution_class: ephemeral
risk_tier: medium
risk_assessment: docs/risk-assessments/support-agent.yaml
input_type: SupportRequest
dependency_type: SupportDependencies
output_type: SupportResponse
skills:
  - investigate-support-case
tools:
  - get-account-summary
  - list-ticket-history
hard_gates:
  - no_unauthorized_write
  - no_unsupported_account_claim
```

## Factory Shape

Language-neutral pseudocode:

```text
build_support_agent(model, toolsets) -> Agent<SupportDependencies, SupportResponse>
  require every toolset to appear in the specification's allowlist
  return new Agent(
    model         = model,
    dependencies  = SupportDependencies,   # schema-validated type
    output        = SupportResponse,       # schema-validated type
    toolsets      = toolsets,
    instructions  = BASE_INSTRUCTIONS,
  )
```

Translate this into the agent framework and version pinned by the repository.

## Edge Cases

- If a request needs to perform a consequential action, elevate the affected path to `human_governed` execution.
- If a tool returns untrusted text, label and delimit it; do not treat it as instructions.
- If output is consumed only by a person, retain a typed internal result and render presentation separately.
- If no specification exists, create one before changing prompts or adding tools.

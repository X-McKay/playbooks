# PydanticAI Agent Design Examples

## Example Request

> Create a PydanticAI support agent that answers account questions, reads ticket history, and proposes—but cannot issue—refunds.

Expected decisions:

- Use ephemeral execution because the enabled capabilities are read-only and the request is bounded.
- Assess privacy, security, legal, operational, and reputational scenarios. Set
  medium governance only if the highest inherent scenario and all mandatory
  floors support it.
- Return a typed `SupportResponse` with answer, evidence, proposed action, and escalation reason.
- Allow read-only account and ticket tools.
- Exclude the refund mutation tool; represent refund requests as proposals requiring a separate authorized path.
- Add hard eval gates for fabricated account facts and unauthorized actions.

## Minimal Spec Shape

```yaml agent-spec
name: support-agent
description: Answer account questions and propose support actions.
instructions:
  - Answer using verified account and ticket information.
  - Propose refunds without executing them.
retries: 2
tool_timeout: 20
instrument: true
metadata:
  contract_version: 1
  version: 1.0.0
  owner: customer-platform
  execution_class: ephemeral
  risk_tier: medium
  risk_assessment: docs/risk-assessments/support-agent.yaml
  data_classification: confidential
  model_policy: balanced-v1
  evaluation_policy: evals/support_agent/release-policy.yaml
  enabled_skills:
    - investigate-support-case
  enabled_toolsets:
    - account-and-ticket-read
  budgets:
    max_requests: 8
    max_input_tokens: 30000
    max_output_tokens: 5000
    max_tool_calls: 12
    max_cost_usd: 0.50
```

This is a schema-valid Agent Spec. Supply the referenced risk assessment,
evaluation policy, skill, and toolset before project validation. Define input,
dependency, and output types in Python; place hard gates in the eval policy.


## Factory Shape

```python
def build_support_agent(
    *, model: Model, toolsets: Sequence[AbstractToolset[SupportDependencies]]
) -> Agent[SupportDependencies, SupportResponse]:
    return Agent(
        model=model,
        deps_type=SupportDependencies,
        output_type=SupportResponse,
        toolsets=list(toolsets),
        instructions=BASE_INSTRUCTIONS,
    )
```

Adapt exact imports and constructor arguments to the PydanticAI version pinned by the repository.

## Edge Cases

- If a request needs to perform a consequential action, elevate the affected path to `human_governed` execution.
- If a tool returns untrusted text, label and delimit it; do not treat it as instructions.
- If output is consumed only by a person, retain a typed internal result and render presentation separately.
- If no Agent Spec exists, create one before changing prompts or adding tools.

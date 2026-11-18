# Getting started

Use the [Agent Playbook](../agent-playbook/README.md) for one agent and add the
[Multi-Agent Systems Playbook](../multi-agent-playbook/README.md) only when a
composition has a documented advantage. Start with the executable examples to
learn the tooling before adapting the standards to a production application.

## Set up the repository

With Nix, run `nix develop`, then the commands below. Without Nix, install uv,
Just, and ShellCheck first. Python and Python dependencies are pinned by the
workspace; uv can install the requested interpreter.

```bash
just bootstrap
just check
```

The root development environment includes the optional examples dependency
group. Installing the standalone `agentctl-playbook` package does not install
PydanticAI. See [compatibility](compatibility.md) for tested versions.

## Run the offline examples

```bash
uv run --locked python examples/single-agent/main.py
uv run --locked python examples/multi-agent/main.py
just examples
```

The first two commands emit evaluation reports. `just examples` scaffolds
throwaway projects, validates their contracts, runs both adapters, accepts
passing reports, and confirms that changing a hard gate to false blocks release.
No API keys, provider calls, or Temporal server are required. The examples use
PydanticAI `TestModel`; they test typed assembly and deterministic control, not
model quality or production readiness.

## Scaffold your own agent

Run from this repository, choosing a new project directory:

```bash
scripts/agentctl scaffold customer-support \
  --root /tmp/customer-support-demo \
  --package acme_agents \
  --owner customer-platform \
  --execution-class ephemeral \
  --risk-tier low
scripts/agentctl validate --root /tmp/customer-support-demo
```

The first validation intentionally fails with `AGENT005`: edit the generated
`src/acme_agents/agents/customer_support/agent.yaml` description to state the
agent's bounded purpose. Then rerun validation. Draft risk and unresolved-question
warnings remain until the assessment has been completed; passing structural
validation does not accept those risks.

Implement the generated factory and typed boundaries, resolve reviewed
capabilities, and implement the eval adapter in
`evals/customer_support/run.py`. Use the [canonical Agent Spec](../agent-playbook/03-agent-contract.md)
and [conformance map](conformance.md) to distinguish enforced fields from
requirements that need runtime or human evidence.

## Evaluate and apply release gates

```bash
scripts/agentctl eval run customer-support --root /tmp/customer-support-demo
scripts/agentctl release check \
  --report /tmp/customer-support-demo/artifacts/evals/customer-support.json \
  --policy /tmp/customer-support-demo/evals/customer_support/release-policy.yaml \
  --baseline /tmp/customer-support-demo/evals/customer_support/baselines/main.json
```

The scaffold adapter writes a report with `placeholder_eval_removed: false`.
An eval command can successfully produce a failing report. The release command
rejects it; it also requires an existing baseline when regression policies are
configured. Replace the adapter with real checks and establish a reviewed
baseline before expecting release acceptance. Do not turn placeholder gates
true without implementing and running the corresponding evaluations.

## Compose agents after their contracts are ready

Create and validate the member agents first, then follow the
[system scaffolding instructions](../tools/agentctl/README.md#scaffold-and-validate-a-multi-agent-system).
The [multi-agent example](../examples/multi-agent/README.md) demonstrates a fixed
producer/reviewer flow. Its deterministic coordinator checks tenant ownership,
shares a request budget, and verifies that the review refers to the investigated
case. Production compositions additionally need the system risk, durability,
observability, admission, and readiness evidence required by the playbook.

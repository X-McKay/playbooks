# Agent Development Skills

This library translates the playbook's [Core](../core/README.md), [Advanced](../advanced/README.md), and [Multi-agent systems](../multi-agent/README.md) sections into focused workflows that Claude Code and Codex can discover and apply while building agents and governed agent systems.

## Catalog

| Skill | Use it for |
| --- | --- |
| [`assess-agent-risk`](assess-agent-risk/SKILL.md) | Scenario-based inherent and residual risk assessment across eight dimensions |
| [`design-agent-contract`](design-agent-contract/SKILL.md) | Declarative agent specifications, typed contracts, package structure, execution classes, and governance tiers |
| [`design-agent-capabilities`](design-agent-capabilities/SKILL.md) | Skill-versus-tool decisions, tool contracts, capability allowlists |
| [`design-durable-execution`](design-durable-execution/SKILL.md) | Engine-neutral workflows, durable steps, retries, approvals, replay, and recovery |
| [`build-agent-evals`](build-agent-evals/SKILL.md) | Datasets, evaluators, trajectory checks, release gates, and online evals |
| [`operate-agent-production`](operate-agent-production/SKILL.md) | Tracing, SLOs, privacy, budgets, and cost optimization |
| [`review-agent-readiness`](review-agent-readiness/SKILL.md) | Evidence-based launch reviews and go/no-go decisions |
| [`design-multi-agent-system`](design-multi-agent-system/SKILL.md) | Architecture justification, topology, System Specs, and composition contracts |
| [`design-agent-interactions`](design-agent-interactions/SKILL.md) | Typed delegation, handoff, review, voting, authority, and data-flow edges |
| [`design-durable-coordination`](design-durable-coordination/SKILL.md) | Engine-neutral durable coordination, replay, approvals, cancellation, and compensation |
| [`build-multi-agent-evals`](build-multi-agent-evals/SKILL.md) | Composition, coordination, adversarial, durability, and baseline evaluations |
| [`assess-multi-agent-risk`](assess-multi-agent-risk/SKILL.md) | System scenarios, emergent risks, controls, evidence, and decisions |
| [`operate-multi-agent-system`](operate-multi-agent-system/SKILL.md) | System traces, SLOs, budgets, capacity, incidents, and rollback |
| [`review-multi-agent-readiness`](review-multi-agent-readiness/SKILL.md) | Evidence-based composition design and launch reviews |

Each package follows the [Agent Skills specification](https://agentskills.io/specification): a required `SKILL.md`, concise discovery metadata, progressive disclosure, directly linked references, examples, and no required product-specific frontmatter.

These skills are technology-neutral: they teach practices and checks, not a particular SDK, framework, or language. Where a skill asks for validation evidence, it expects the project's own validation tooling or CI to produce it.

## Use with Codex

For repository-scoped use, copy or symlink the skill directories into `.codex/skills/`:

```bash
mkdir -p .codex/skills
cp -R /path/to/playbooks/skills/*/ .codex/skills/
```

For personal use across repositories, use `~/.codex/skills/` instead. The optional `agents/openai.yaml` in each package supplies Codex presentation metadata and does not alter the portable `SKILL.md` contract.

Invoke explicitly when useful, for example:

```text
Use $build-agent-evals to add regression coverage for the refund workflow.
```

## Use with Claude Code

For repository-scoped use, copy or symlink the skill directories into `.claude/skills/`:

```bash
mkdir -p .claude/skills
cp -R /path/to/playbooks/skills/*/ .claude/skills/
```

For personal use, use `~/.claude/skills/`. Claude Code can select a skill from its description or invoke it by name, such as `/build-agent-evals`.

## Use as Runtime Skills

Agent frameworks that support the Agent Skills specification can also expose these packages to a running agent. Check what the framework actually loads: some load only `SKILL.md` instructions and do not automatically load bundled `references/`, execute `scripts/`, or resolve product-specific placeholders. Keep runtime-critical instructions in `SKILL.md`, expose only reviewed skills, and provide filesystem capabilities separately if an agent must read bundled files.

## Authoring Rules

1. Keep each skill narrow enough to have one recognizable job.
2. Put both what the skill does and when it applies in `description`.
3. Keep `SKILL.md` procedural and below 500 lines.
4. Put detailed standards and examples in focused, directly linked reference files.
5. Add scripts only for deterministic work that instructions and existing tools cannot perform reliably.
6. Keep credentials, authorization, and enforcement outside skill text.
7. Validate changes and test both expected triggers and non-triggers.
8. Keep `references/standard.md` in step with the playbook chapter it condenses. Each one links its source chapter; the chapter is canonical.

## Validation

From the repository root, validate each package with the reference validator when installed:

```bash
for skill in skills/*/; do
  skills-ref validate "$skill"
done
```

Also run the repository's Markdown checks. A valid package is only the starting point; use `build-agent-evals` to test whether the skill triggers correctly, follows required steps, handles edge cases, and avoids unintended activation.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI plugin skill authoring](https://developers.openai.com/plugins/build/skills)
- [Core and Advanced references](../core/references.md)

# Agent Development Skills

This library translates the [Agent Playbook](../../agent-playbook/README.md) and [Multi-Agent Playbook](../../multi-agent-playbook/README.md) into focused workflows that Claude Code and Codex can discover and apply while building agents and governed agent systems.

## Catalog

| Skill | Use it for |
| --- | --- |
| [`assess-agent-risk`](assess-agent-risk/SKILL.md) | Scenario-based inherent and residual risk assessment across eight dimensions |
| [`design-pydantic-agent`](design-pydantic-agent/SKILL.md) | Agent Specs, typed contracts, package structure, execution classes, and risk tiers |
| [`design-agent-capabilities`](design-agent-capabilities/SKILL.md) | Skill-versus-tool decisions, tool contracts, capability allowlists |
| [`implement-temporal-agent`](implement-temporal-agent/SKILL.md) | Workflows, activities, retries, approvals, replay, and recovery |
| [`build-agent-evals`](build-agent-evals/SKILL.md) | Datasets, evaluators, trajectory checks, release gates, and online evals |
| [`operate-agent-production`](operate-agent-production/SKILL.md) | Tracing, SLOs, privacy, budgets, and cost optimization |
| [`review-agent-readiness`](review-agent-readiness/SKILL.md) | Evidence-based launch reviews and go/no-go decisions |
| [`design-multi-agent-system`](design-multi-agent-system/SKILL.md) | Architecture justification, topology, System Specs, and composition contracts |
| [`design-agent-interactions`](design-agent-interactions/SKILL.md) | Typed delegation, handoff, review, voting, authority, and data-flow edges |
| [`implement-temporal-multi-agent`](implement-temporal-multi-agent/SKILL.md) | Durable coordination, replay, approvals, cancellation, and compensation |
| [`build-multi-agent-evals`](build-multi-agent-evals/SKILL.md) | Composition, coordination, adversarial, durability, and baseline evaluations |
| [`assess-multi-agent-risk`](assess-multi-agent-risk/SKILL.md) | System scenarios, emergent risks, controls, evidence, and decisions |
| [`operate-multi-agent-system`](operate-multi-agent-system/SKILL.md) | System traces, SLOs, budgets, capacity, incidents, and rollback |
| [`review-multi-agent-readiness`](review-multi-agent-readiness/SKILL.md) | Evidence-based composition design and launch reviews |

Each package follows the [Agent Skills specification](https://agentskills.io/specification): a required `SKILL.md`, concise discovery metadata, progressive disclosure, directly linked references, examples, and no required product-specific frontmatter.

When installed in a repository that includes the companion [`agentctl`](../../tools/agentctl/README.md), the design, eval, and readiness skills use its scaffolding and validation commands as reproducible evidence.

## Install in a Repository

Codex and Claude Code share one copy of the skills. Codex reads repository skills from `.agents/skills/`; Claude Code reads `.claude/skills/`, so link that path to the shared directory:

```bash
mkdir -p .agents/skills .claude
cp -R /path/to/playbooks/.agents/skills/*/ .agents/skills/
ln -s ../.agents/skills .claude/skills
```

On Windows checkouts without symlink support (`core.symlinks=false`), copy the skills into `.claude/skills/` instead and keep both copies in sync.

For personal use across repositories, install into `~/.agents/skills/` for Codex and `~/.claude/skills/` for Claude Code.

Keep project instructions in a root `AGENTS.md`, which Codex reads. Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists and some sessions cannot read it at all, so add a `CLAUDE.md` containing the single line `@AGENTS.md`.

The optional `agents/openai.yaml` in each package supplies Codex presentation metadata and does not alter the portable `SKILL.md` contract.

Invoke a skill explicitly when useful, for example `Use $build-agent-evals to add regression coverage for the refund workflow.` in Codex or `/build-agent-evals` in Claude Code. Both clients also select skills from their descriptions.

## Use as PydanticAI Runtime Skills

These packages can also be exposed as deferred PydanticAI Harness capabilities:

```python
from pydantic_ai import Agent
from pydantic_ai_harness import Skills

agent = Agent(
    model,
    capabilities=[
        Skills(
            "skills",
            include=["build-agent-evals", "review-agent-readiness"],
        )
    ],
)
```

PydanticAI loads the selected `SKILL.md` instructions, but it does not automatically load bundled `references/`, execute `scripts/`, or resolve product-specific placeholders. Keep runtime-critical instructions in `SKILL.md`, expose only reviewed skills, and provide filesystem capabilities separately if an agent must read bundled files.

## Authoring Rules

1. Keep each skill narrow enough to have one recognizable job.
2. Put both what the skill does and when it applies in `description`.
3. Keep `SKILL.md` procedural and below 500 lines.
4. Put detailed standards and examples in focused, directly linked reference files.
5. Add scripts only for deterministic work that instructions and existing tools cannot perform reliably.
6. Keep credentials, authorization, and enforcement outside skill text.
7. Validate changes and test both expected triggers and non-triggers.

## Validation

From the repository root, validate each package with the reference validator when installed:

```bash
for skill in .agents/skills/*/; do
  skills-ref validate "$skill"
done
```

Also run the repository's Markdown checks. A valid package is only the starting point; use `build-agent-evals` to test whether the skill triggers correctly, follows required steps, handles edge cases, and avoids unintended activation.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI plugin skill authoring](https://developers.openai.com/plugins/build/skills)
- [PydanticAI Harness skills](https://pydantic.dev/docs/ai/harness/skills/)
- [Agent Playbook references](../../agent-playbook/references.md)

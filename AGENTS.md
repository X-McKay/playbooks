# Repository Instructions

This repository holds standards for building production AI agents, the Agent
Skills that apply them, and the `agentctl` toolkit that enforces them.

## Layout

- `agent-playbook/` and `multi-agent-playbook/`: the normative standards. They
  are the single source of truth for every requirement.
- `.agents/skills/`: portable Agent Skills for Codex and Claude Code.
  `.claude/skills` is a symlink to this directory; edit files only under
  `.agents/skills/`.
- `tools/agentctl/`: scaffolding, validation, eval adapters, and release gates.

## Content Rules

- State each requirement once, in the playbook chapter that owns it. Skills
  describe how to apply requirements; they must not restate or reinterpret
  them.
- When a chapter changes a requirement, update every skill reference that
  depends on it in the same change.
- Use MUST, SHOULD, and MAY only with the meanings defined in
  `agent-playbook/README.md`.
- Keep each `SKILL.md` procedural and under 500 lines, and keep skill
  references one level deep inside the skill directory.

## Checks

Run `just check` before committing. Without Just, run:

```bash
uv lock --check
uv run --locked ruff check tools/agentctl/src tools/agentctl/tests
uv run --locked python -m unittest discover -s tools/agentctl/tests
uv run --locked agentctl --no-animations skills validate .agents/skills
```

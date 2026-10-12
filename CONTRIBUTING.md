# Contributing

Thanks for helping improve the playbooks. This repository is guidance, not
code: it teaches what good looks like and why, in terms that hold on any stack.

## Where does this belong?

Before adding or changing content, ask: **would this still be true if the team
used a different SDK, framework, product, or language?**

- **Yes**: it belongs here. Principles, normative requirements, decision
  criteria, failure modes, checklists, templates, and worked scenarios.
- **No**: it does not belong in this repository. Install steps, API calls,
  code, configuration for a named product, version pins, and tool commands
  belong in the documentation for that stack.

When a concept is easiest to explain with a concrete tool, describe the
concept in neutral terms instead.

## Writing rules

- Do not name SDKs, frameworks, vendors' products, or programming languages in
  the guidance. Use the neutral terms the playbooks already use, for example
  "declarative agent specification", "durable execution engine", "workflow",
  and "durable step".
- Open standards may be named as examples when they are the shared vocabulary:
  OpenTelemetry, the Model Context Protocol, the Agent Skills specification,
  JSON Schema, and OAuth.
- Examples use neutral formats (YAML, JSON, plain text, tables, diagrams), not
  source code.
- Keep requirement strength explicit with MUST, SHOULD, and MAY, as defined in
  each playbook's README.
- Version the playbook in its README when a change alters what conformance
  requires.
- When a change alters a chapter, update the skill reference that condenses
  it. Each `skills/*/references/standard.md` names its source chapter.
- Use the terms the playbooks define: **governance tier** (not risk tier) for
  the assurance level, and **capability manifest** for the per-agent bill of
  materials produced at startup.

## Checks

```bash
nix develop
just check
```

`just check` lints Markdown and verifies that relative links and anchors
resolve. Skill packages follow the
[Agent Skills specification](https://agentskills.io/specification).

# Contributing

Thanks for helping improve the playbooks. This repository is guidance, not
code: it teaches what good looks like and why, in terms that hold on any stack.

## Where does this belong?

Before adding or changing content, ask: **would this still be true if the team
used a different SDK, framework, product, or language?**

- **Yes**: it belongs here. Principles, normative requirements, decision
  criteria, failure modes, checklists, templates, and worked scenarios.
- **No**: it belongs in an implementation, not here. Install steps, API
  calls, code, configuration for a named product, version pins, and tool
  commands.

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

## 0.5.0-draft.2 content

The `development-guide/` and `engineering-reference/` trees are a proposed 0.5.0-draft.2 assembled draft. Keep new-draft changes technology-neutral, keep requirement ownership with the chapter named in the book, and state policy proposals and unresolved adoption decisions explicitly. Update draft navigation and the requirement index when an owner chapter, requirement ID, or applicability trigger changes.

Do **not** use a new-draft contribution to relabel the legacy `agent-playbook/`, `foundations/`, `multi-agent-playbook/`, or `skills/` trees as v0.5 conformant. They remain the v0.4 compatibility baseline until a separately reviewed migration changes them. The legacy skill-reference update rule above does not automatically apply to a proposed 0.5 draft chapter; a skill migration needs its own reviewed scope. Do not weaken the repository-neutrality rule by adding product-specific setup, commands, SDK instructions, or provider-specific configuration to the draft.

### New-draft mini-books

For new or reorganized draft Parts, use the [writing guide](writing-guide.md). It defines the flexible six-function mini-book pattern, requires one canonical owner for each normative requirement, and keeps audience, applicability, evidence, and practical reference visible without requiring a rewrite of other Parts.

## Checks

```bash
nix develop
just check
```

`just check` lints Markdown and verifies that relative links and anchors
resolve. Skill packages follow the
[Agent Skills specification](https://agentskills.io/specification).

# Contributing

Read [getting started](docs/getting-started.md) for setup and
[conformance](docs/conformance.md) for requirement ownership.

## Where changes belong

| Content | Location |
| --- | --- |
| Normative single-agent requirements | `agent-playbook/` |
| Additional composition requirements | `multi-agent-playbook/` |
| Portable development workflows | `skills/<name>/` |
| CLI behavior and packaged schemas/templates | `tools/agentctl/src/agentctl/` |
| Runnable deterministic demonstrations | `examples/` |
| Adoption, conformance, and compatibility guidance | `docs/` |

Retain the existing chapter paths so external links remain useful. Keep skill
packages self-contained: all local references must resolve within the copied
package, including links inside bundled reference documents. Link to source
playbooks for additional context, not as a required local dependency.

## Change checklist

- Update prose, schema, semantic checks, templates, examples, and affected skill
  summaries together when a contract changes.
- Use string-valued skill metadata to record source playbook versions. Review
  summaries even when editing a draft without changing its version.
- Add rejection tests for changed validation boundaries and meaningful output
  checks for behavior changes. Avoid tests that merely repeat implementation.
- Label complete YAML fences `yaml agent-spec`, `yaml system-spec`, or
  `yaml risk-assessment` to validate them against packaged schemas. Label partial
  examples as illustrative and explain their missing context.
- Record compatibility changes and user-visible behavior in `CHANGELOG.md`.
- Run `just format`, `just check`, and `just nix-check` before merge. Report any
  environmental limitation separately from passing checks.

## Checks

`just check` runs the locked dependency check, Ruff lint and formatting checks,
ShellCheck, unit tests, skill validation, documentation checks, offline examples,
and installed-wheel smoke verification. It makes no provider calls.

`just docs` uses the pinned Markdown parser to check heading progression
(MD001), trailing whitespace (MD009), fenced-code language labels (MD040), local
file/heading links, annotated YAML contracts, template schemas, and skill source
versions. It deliberately does not fetch external links or impose line lengths.
The previous unused Markdownlint configuration has been replaced by these
executable repository rules.

`just package` builds a wheel with the pinned Hatchling version, installs it into
a temporary target, and runs it from outside the checkout with isolated Python
import behavior. It verifies resource loading, scaffolding, validation, graphs,
and generated Python syntax using the workspace's locked dependencies.

`just nix-check` runs the flake's source-quality derivation. Nix tools are pinned
separately from the uv dependencies; the uv-based CI matrix remains the Python
runtime compatibility check.

## Pull requests

Describe the behavior change, affected standards, validation performed, and any
remaining manual evidence. Maintainers review normative changes and coordinate
cross-layer updates before merging. There is no deployment or publication step
in repository checks.

## License status

This repository is intentionally unlicensed for now. No license grant is added
by this maintenance work. Maintainers will decide reuse terms separately.

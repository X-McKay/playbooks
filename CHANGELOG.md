# Changelog

## Unreleased

- Add getting-started, conformance, compatibility, and contribution guidance.
- Align documented Agent Specs with validation and package an Agent Spec schema.
- Validate malformed system risk structures before semantic checks; stop system
  cross-checks on invalid members; accept integral JSON numeric risk scores.
- Separate system risk, validation, and presentation; share contract constants
  and scaffold file utilities; package substantial scaffold text as templates.
- Validate nested skill references and record source playbook versions.
- Add deterministic PydanticAI single-agent and producer/reviewer examples.
- Add Markdown/link/example checks, formatting verification, rejection tests,
  copied-skill tests, installed-wheel smoke checks, CI, and Nix source checks.
- Keep existing CLI commands and scaffold output; structural errors now use
  `AGENT041` or `SYSRISK025` before semantic validation.
- Keep the repository unlicensed pending a separate maintainer decision.

## Existing versions

The starting repository contains Agent Playbook 0.3, Multi-Agent Systems
Playbook 0.1, and agentctl 0.4.0. Historical changes remain in Git history;
these entries do not imply new release tags or published packages.

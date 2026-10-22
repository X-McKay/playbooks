set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Lint all Markdown with the repository's markdownlint rules.
lint:
    markdownlint-cli2 "**/*.md"

# Check that every relative link and anchor resolves, without network access.
links:
    lychee --offline --include-fragments --no-progress "**/*.md"

# Check only the proposed development library; leave legacy skills unchanged.
skills-check:
    python3 tools/agent_skills/skillctl.py validate --root .
    python3 -m unittest discover -s tests/agent_skills -v

check: lint links skills-check

nix-check:
    nix flake check

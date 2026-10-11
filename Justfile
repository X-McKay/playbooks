set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Lint all Markdown with the repository's markdownlint rules.
lint:
    markdownlint-cli2 "**/*.md"

# Check that every relative link and anchor resolves, without network access.
links:
    lychee --offline --include-fragments --no-progress "**/*.md"

check: lint links

nix-check:
    nix flake check

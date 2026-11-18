set shell := ["bash", "-euo", "pipefail", "-c"]

python_paths := "tools/agentctl/src tools/agentctl/tests scripts examples"

default:
    @just --list

bootstrap:
    uv sync --locked

lock:
    uv lock --check

format:
    uv run --locked ruff format {{python_paths}}

format-check:
    uv run --locked ruff format --check {{python_paths}}

lint:
    uv run --locked ruff check {{python_paths}}
    shellcheck scripts/agentctl

test:
    PYDANTIC_AI_NO_BANNER=1 uv run --locked python -m unittest discover -s tools/agentctl/tests -v

skills:
    uv run --locked agentctl --no-animations skills validate skills

docs:
    uv run --locked python scripts/check_docs.py

examples:
    PYDANTIC_AI_NO_BANNER=1 uv run --locked python examples/verify.py

package:
    uv run --locked python scripts/smoke_wheel.py

check: lock lint format-check test skills docs examples package

agentctl *args:
    uv run --locked agentctl {{args}}

nix-check:
    nix flake check --no-update-lock-file

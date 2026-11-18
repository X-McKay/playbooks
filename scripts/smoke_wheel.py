"""Build and install a wheel, then exercise it outside the source checkout."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = r"""
import contextlib, io, json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import agentctl
from agentctl.cli import main
from agentctl.validation import load_agent_schema
from agentctl.systems import load_system_schema
from agentctl.risk import load_schema
import yaml
assert Path(agentctl.__file__).is_relative_to(Path(sys.argv[1]))
assert load_agent_schema() and load_system_schema() and load_schema()
root = Path.cwd()
for execution in ('ephemeral', 'durable', 'human_governed'):
    project = root / execution
    with contextlib.redirect_stdout(io.StringIO()):
        for name in ('planner-agent', 'worker-agent'):
            assert main(['scaffold', name, '--root', str(project), '--owner', 'platform', '--execution-class', execution, '--risk-tier', 'high']) == 0
            spec_path = project / 'src/acme_agents/agents' / name.replace('-', '_') / 'agent.yaml'
            spec = yaml.safe_load(spec_path.read_text())
            spec['description'] = 'Handle bounded support cases.'
            spec_path.write_text(yaml.safe_dump(spec))
        assert main(['validate', '--root', str(project)]) == 0
        assert main(['system', 'scaffold', 'support-system', '--root', str(project), '--owner', 'platform', '--operational-owner', 'ops', '--execution-class', execution, '--risk-tier', 'high', '--member', 'planner-agent:coordinator', '--member', 'worker-agent:worker']) == 0
        path = project / 'src/acme_agents/systems/support_system/system.yaml'
        spec = yaml.safe_load(path.read_text())
        spec['description'] = 'Coordinate bounded support work.'
        path.write_text(yaml.safe_dump(spec))
        assert main(['system', 'validate', '--root', str(project)]) == 0
        assert main(['system', 'graph', str(path), '--root', str(project), '--format', 'json']) == 0
    for source in project.rglob('*.py'):
        compile(source.read_text(), str(source), 'exec')
print('Installed wheel schemas, templates, scaffolding, validation, and graphs passed.')
"""


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="playbooks-wheel-") as temporary:
        root = Path(temporary)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "hatchling",
                "build",
                "-t",
                "wheel",
                "-d",
                str(root),
            ],
            cwd=ROOT / "tools/agentctl",
            check=True,
        )
        (wheel,) = root.glob("*.whl")
        site = root / "installed"
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--no-cache",
                "--no-deps",
                "--target",
                str(site),
                str(wheel),
            ],
            check=True,
        )
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        subprocess.run(
            [sys.executable, "-I", "-c", PROBE, str(site)],
            cwd=root,
            env=environment,
            check=True,
        )


if __name__ == "__main__":
    main()

import asyncio
import os
from pathlib import Path

import pytest

from bridge_probe.process import run_child


async def test_hung_replay_is_killed_and_reaped(tmp_path):
    pid_file = tmp_path / "pid"
    with pytest.raises(TimeoutError):
        await run_child(
            "tests.fixtures.hung_child",
            {"pid_file": str(pid_file)},
            timeout=2,
            cwd=Path(__file__).resolve().parents[2],
        )
    pid = int(pid_file.read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


async def test_cancelled_client_reaps_child(tmp_path):
    pid_file = tmp_path / "pid"
    task = asyncio.create_task(
        run_child(
            "tests.fixtures.hung_child",
            {"pid_file": str(pid_file)},
            cwd=Path(__file__).resolve().parents[2],
        )
    )
    async with asyncio.timeout(3):
        while not pid_file.exists():
            await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)


async def test_excess_output_is_bounded():
    with pytest.raises(ValueError, match="output"):
        await run_child(
            "tests.fixtures.hung_child",
            {"flood": True},
            max_output=1024,
            cwd=Path(__file__).resolve().parents[2],
        )

import asyncio
import json
import os
import sys
from pathlib import Path


async def fresh_advance(request):
    env = dict(os.environ, PYTHONHASHSEED='random')
    process = await asyncio.create_subprocess_exec(sys.executable, '-m', 'tests.fixtures.replay_child',
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env, cwd=Path(__file__).resolve().parents[2])
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(json.dumps(request).encode()), 10)
        assert process.returncode == 0, stderr.decode()
        result = json.loads(stdout)
        result['process_exited'] = process.returncode is not None
        return result
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()

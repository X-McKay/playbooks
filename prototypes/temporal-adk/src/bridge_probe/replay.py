"""One cold ADK reconstruction; launched only by the session supervisor."""

import asyncio
import json
import os
import sys
from pathlib import Path

from .artifacts import FileStore, Position, Tape
from .capture import capture_boundary
from .demo import factory
from .records import canonical_bytes


async def main():
    request = json.load(sys.stdin)
    stored = request.get("from_store", False)
    position = request.get("position")
    if stored:
        request.update(
            workspace="/sandbox/workspace",
            session=os.environ["BRIDGE_SESSION"],
            manifest=os.environ["BRIDGE_MANIFEST"],
            message=os.environ["BRIDGE_MESSAGE"],
        )
        request["tape"] = Tape(FileStore("/sandbox/objects"), manifest=request["manifest"]).load(
            Position.model_validate(position)
        )
    result = await capture_boundary(
        lambda bridge: factory(bridge, request["workspace"]),
        request["tape"],
        request["pending"],
        invocation=request["session"],
        manifest=request["manifest"],
        message=request["message"],
    )
    if stored and result["status"] == "operation":
        Path("/sandbox/pending.json").write_bytes(
            canonical_bytes({"position": position, "operation": result["operation"]})
        )
    print(json.dumps(result))


if __name__ == "__main__":
    asyncio.run(main())

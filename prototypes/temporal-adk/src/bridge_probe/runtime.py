"""Session-local supervisor. Its caches are volatile; it never selects durable progress."""

import asyncio
import json
import os
import shutil
from pathlib import Path

from .artifacts import FileStore, Position, Tape
from .demo import registry
from .dispatch import Dispatcher
from .process import run_child
from .records import canonical_bytes
from .transport import Authority
from .workspace import Workspace

ROOT = Path("/sandbox")
SOCKET = ROOT / "bridge.sock"


class TrackingStore(FileStore):
    def __init__(self, root):
        super().__init__(root)
        self.written = {}

    def put(self, data):
        ref = super().put(data)
        self.written[ref.sha256] = ref
        return ref


class Runtime:
    def __init__(self, root, *, session, manifest, key, message, generation=1):
        self.root = Path(root)
        self.session = session
        self.manifest = manifest
        self.message = message
        self.store = TrackingStore(self.root / "objects")
        self.tape = Tape(self.store, manifest=manifest)
        self.workdir = self.root / "workspace"
        self.workdir.mkdir(exist_ok=True)
        self.workspace = Workspace(self.workdir, self.store)
        self.dispatcher = Dispatcher(
            registry(self.workdir), manifest=manifest, workspace=self.workspace
        )
        self.authority = Authority(key, session, generation=generation)
        self.lock = asyncio.Lock()
        self.pending = None
        self.position = None
        self.effects = []

    async def handle(self, envelope):
        action, command = self.authority.verify(envelope)
        if command["binding"]["session"] != self.session:
            raise ValueError("wrong binding")
        async with self.lock:
            position = Position.model_validate(command["position"])
            if action == "advance":
                if any(not item[2].done() for item in self.dispatcher.tasks.values()):
                    raise ValueError("old writer still active")
                # The caller supplies the accepted Position, never a local latest pointer.
                tape = self.tape.load(position)
                if position.workspace is None:
                    raise ValueError("missing workspace")
                shutil.rmtree(self.workdir)
                self.workdir.mkdir()
                self.workspace.restore(position.workspace)
                self.position = position
                if command.get("prepare_only"):
                    (self.root / "pending.json").unlink(missing_ok=True)
                    return {"status": "prepared"}
                result = await run_child(
                    "bridge_probe.replay",
                    {
                        "tape": tape,
                        "pending": command["pending"],
                        "workspace": str(self.workdir),
                        "session": self.session,
                        "manifest": self.manifest,
                        "message": self.message,
                    },
                    timeout=30,
                )
                self.pending = result.get("operation")
                self.position = position
                return result
            if action == "execute":
                pending_file = self.root / "pending.json"
                if pending_file.exists():
                    captured = json.loads(pending_file.read_bytes())
                    if captured["position"] != position.model_dump():
                        raise ValueError("stale captured position")
                    self.pending = captured["operation"]
                if command["operation"] != self.pending or position != self.position:
                    raise ValueError("execution requires the captured pinned descriptor")
                self.store.written.clear()
                before = len(self.dispatcher.tasks)
                outcome = await self.dispatcher.execute(command["operation"], command["attempt_id"])
                if len(self.dispatcher.tasks) > before:
                    self.effects.append(command["operation"]["operation_id"])
                receipt = self.tape.append_candidate(
                    position,
                    command["operation"],
                    outcome,
                    self.dispatcher.checkpoint(command["operation"]),
                )
                # Include the checkpoint on duplicate delivery even if its put was cached.
                refs = dict(self.store.written)
                refs[receipt.position.workspace.sha256] = receipt.position.workspace
                return {
                    "receipt": receipt.model_dump(),
                    "objects": [ref.model_dump() for ref in refs.values()],
                }
            raise ValueError("unsupported runtime action")


async def main():
    runtime = Runtime(
        ROOT,
        session=os.environ["BRIDGE_SESSION"],
        manifest=os.environ["BRIDGE_MANIFEST"],
        key=bytes.fromhex(os.environ["BRIDGE_KEY"]),
        message=os.environ["BRIDGE_MESSAGE"],
        generation=int(os.environ.get("BRIDGE_GENERATION", "1")),
    )

    async def connected(reader, writer):
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=5)
            if len(data) > 262144:
                raise ValueError("command too large")
            response = await runtime.handle(json.loads(data))
            encoded = canonical_bytes({"ok": response})
            if len(encoded) > 262144:
                raise ValueError("response too large")
        except Exception as exc:  # noqa: BLE001 -- boundary reports failure; never claims an outcome
            encoded = canonical_bytes({"error": type(exc).__name__, "message": str(exc)[:300]})
        writer.write(encoded + b"\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_unix_server(connected, path=SOCKET, limit=262145)
    os.chmod(SOCKET, 0o600)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

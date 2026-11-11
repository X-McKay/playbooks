"""Run the complete scripted agent under OpenShell, owned by a real Temporal Workflow."""

import argparse
import asyncio
import json
import secrets
import uuid
from datetime import timedelta
from pathlib import Path

from openshell import SandboxClient, TlsConfig
from temporalio.client import Client
from temporalio.common import WorkflowIDReusePolicy
from temporalio.worker import Replayer, Worker

from bridge_probe.activities import Activities
from bridge_probe.artifacts import FileStore, Tape
from bridge_probe.openshell import OpenShellSession
from bridge_probe.temporal import SessionWorkflow
from bridge_probe.workspace import Workspace


async def run(args):
    session = "kind-" + uuid.uuid4().hex
    store = FileStore(args.state / session / "objects")
    base = args.state / session / "base"
    base.mkdir(parents=True)
    (base / "README.md").write_text("Synthetic repository for the bridge prototype.\n")
    tape = Tape(store, manifest="demo-v1")
    position = tape.empty(Workspace(base, store).capture())
    client = SandboxClient(
        args.openshell,
        tls=TlsConfig(
            ca_path=args.tls / "ca.crt",
            cert_path=args.tls / "tls.crt",
            key_path=args.tls / "tls.key",
        ),
    )
    runtime = OpenShellSession(
        client, store, session=session, manifest="demo-v1", key=secrets.token_bytes(32)
    )
    temporal = await Client.connect(args.temporal)
    activities = Activities(runtime, runtime, tape)
    try:
        async with Worker(
            temporal,
            task_queue=session,
            workflows=[SessionWorkflow],
            activities=activities.registered(),
        ):
            handle = await temporal.start_workflow(
                SessionWorkflow.run,
                {
                    "session": session,
                    "message": "Inspect the workspace",
                    "position": position.model_dump(),
                },
                id=session,
                task_queue=session,
                execution_timeout=timedelta(minutes=15),
                id_reuse_policy=WorkflowIDReusePolicy.REJECT_DUPLICATE,
            )
            result = await handle.result()
        await Replayer(workflows=[SessionWorkflow]).replay_workflow(await handle.fetch_history())
        report = {"workflow_id": session, "result": result}
        (args.state / session / "result.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        if result["status"] != "SUCCEEDED" or result["cleanup"] != "DELETED":
            raise RuntimeError("kind smoke did not succeed")
    finally:
        await runtime.close({"binding": runtime.binding})
        client.close()


parser = argparse.ArgumentParser()
parser.add_argument("--tls", type=Path, required=True)
parser.add_argument("--state", type=Path, required=True)
parser.add_argument("--temporal", default="127.0.0.1:17233")
parser.add_argument("--openshell", default="127.0.0.1:18080")
if __name__ == "__main__":
    asyncio.run(run(parser.parse_args()))

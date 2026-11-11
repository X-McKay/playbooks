"""Disposable kernel/runtime qualification using the official OpenShell API."""

import argparse
import json
from pathlib import Path

from openshell import SandboxClient, TlsConfig
from openshell._proto import openshell_pb2, sandbox_pb2

parser = argparse.ArgumentParser()
parser.add_argument("--tls", type=Path, required=True)
parser.add_argument("--endpoint", default="127.0.0.1:18080")
args = parser.parse_args()
client = SandboxClient(
    args.endpoint,
    tls=TlsConfig(
        ca_path=args.tls / "ca.crt", cert_path=args.tls / "tls.crt", key_path=args.tls / "tls.key"
    ),
)
policy = sandbox_pb2.SandboxPolicy(
    version=1,
    filesystem=sandbox_pb2.FilesystemPolicy(
        include_workdir=False,
        read_only=["/usr", "/bin", "/lib", "/lib64", "/etc", "/proc", "/app", "/dev/urandom"],
        read_write=["/sandbox", "/tmp", "/dev/null"],
    ),
    landlock=sandbox_pb2.LandlockPolicy(compatibility="hard_requirement"),
    process=sandbox_pb2.ProcessPolicy(run_as_user="1500", run_as_group="1500"),
)
name = "bridge-qualify"
ref = None
try:
    ref = client.create(
        workspace="default",
        name=name,
        spec=openshell_pb2.SandboxSpec(
            template=openshell_pb2.SandboxTemplate(image="adk-bridge-probe:local"),
            policy=policy,
            command=["/app/.venv/bin/python", "-c", "import time; time.sleep(600)"],
        ),
    )
    print(json.dumps({"created": ref.id}), flush=True)
    ready = client.wait_ready(name, workspace="default", timeout_seconds=240)
    print("phase:", ready.phase, flush=True)
    result = client.exec(
        name,
        [
            "/app/.venv/bin/python",
            "-c",
            'import pathlib; import google.adk; p=pathlib.Path("/sandbox/qualification");p.write_text("ok");print(p.read_text())',
        ],
        workspace="default",
        timeout_seconds=30,
        no_login_shell=True,
    )
    print(result, flush=True)
finally:
    if ref:
        client.delete(name, workspace="default", allow_missing=True)
        client.wait_deleted(
            name, workspace="default", expected_sandbox_id=ref.id, timeout_seconds=60
        )
        print("deleted", flush=True)
    client.close()

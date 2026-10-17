import asyncio
import json
import os
import secrets
import uuid
from pathlib import Path

import grpc
import pytest
from openshell import SandboxClient, TlsConfig

from bridge_probe.artifacts import FileStore, Tape
from bridge_probe.openshell import PYTHON, OpenShellSession, policy
from bridge_probe.workspace import Workspace

pytestmark = pytest.mark.cluster


@pytest.fixture
def gateway():
    tls = os.environ.get("OPENSHELL_TLS_DIR")
    if not tls:
        pytest.skip("explicit kind OpenShell TLS directory required")
    root = Path(tls)
    client = SandboxClient(
        os.environ.get("OPENSHELL_ADDRESS", "127.0.0.1:18080"),
        tls=TlsConfig(
            ca_path=root / "ca.crt", cert_path=root / "tls.crt", key_path=root / "tls.key"
        ),
    )
    yield client
    client.close()


async def test_policy_enforced_inside_real_workload_and_identity_scoped(gateway, tmp_path):
    ident = "policy-" + uuid.uuid4().hex
    store = FileStore(tmp_path / "objects")
    root = tmp_path / "base"
    root.mkdir()
    position = Tape(store, manifest="demo-v1").empty(Workspace(root, store).capture())
    runtime = OpenShellSession(
        gateway, store, session=ident, manifest="demo-v1", key=secrets.token_bytes(32)
    )
    binding = None
    try:
        binding = await runtime.provision(
            {"session": ident, "message": "policy check", "position": position.model_dump()}
        )
        code = """import json,pathlib,socket,os
results={}
p=pathlib.Path('/sandbox/allowed');p.write_text('ok');results['workspace']=p.read_text()=='ok'
for name,path,write in [('outside_read','/private-canary/readable',False),('outside_write','/restricted-write/file',True),('host_socket','/var/run/docker.sock',False)]:
 try:
  p=pathlib.Path(path)
  if write:p.write_text('bad')
  else:p.read_bytes()
  results[name]=False
 except OSError:results[name]=True
for name,address in json.loads(os.environ['PROBE_ENDPOINTS']).items():
 try:
  s=socket.create_connection(tuple(address),timeout=2);s.close();results[name]=False
 except OSError:results[name]=True
print(json.dumps(results))"""
        endpoints = {
            "metadata": ["169.254.169.254", 80],
            "unapproved_egress": ["1.1.1.1", 443],
            "temporal": [os.environ["TEMPORAL_CLUSTER_IP"], 7233],
            "management": [os.environ["OPENSHELL_CLUSTER_IP"], 8080],
        }
        result = await asyncio.to_thread(
            gateway.exec,
            binding["name"],
            [PYTHON, "-c", code],
            workspace="default",
            env={"PROBE_ENDPOINTS": json.dumps(endpoints)},
            timeout_seconds=20,
            no_login_shell=True,
        )
        assert result.exit_code == 0, result.stderr
        observed = json.loads(result.stdout)
        assert all(observed.values()), observed
        with pytest.raises(ValueError):
            await runtime.checked_exec({**binding, "sandbox_id": "stale"}, "rpc", b"{}")
        # No Temporal or management certificate is injected into workload env.
        result = await asyncio.to_thread(
            gateway.exec,
            binding["name"],
            [
                PYTHON,
                "-c",
                'import os; assert not any(k.startswith("TEMPORAL") for k in os.environ); print("ok")',
            ],
            workspace="default",
            timeout_seconds=10,
            no_login_shell=True,
        )
        assert result.exit_code == 0
    finally:
        assert (await runtime.close({"binding": binding}))["cleanup"] == "DELETED"


def test_gateway_rejects_client_without_certificate():
    tls = os.environ.get("OPENSHELL_TLS_DIR")
    if not tls:
        pytest.skip("explicit kind OpenShell TLS directory required")
    with (
        SandboxClient(
            os.environ.get("OPENSHELL_ADDRESS", "127.0.0.1:18080"),
            tls=TlsConfig(ca_path=Path(tls) / "ca.crt"),
            timeout=5,
        ) as client,
        pytest.raises(grpc.RpcError),
    ):
        list(client.list(workspace="default"))


async def test_agent_specific_policy_can_allow_only_the_named_canary(gateway, tmp_path):
    ident = "allow-" + uuid.uuid4().hex
    store = FileStore(tmp_path / "objects")
    root = tmp_path / "base"
    root.mkdir()
    position = Tape(store, manifest="allow-v1").empty(Workspace(root, store).capture())
    approved = policy()
    approved.filesystem.read_only.append("/private-canary")
    runtime = OpenShellSession(
        gateway,
        store,
        session=ident,
        manifest="allow-v1",
        key=secrets.token_bytes(32),
        sandbox_policy=approved,
    )
    binding = None
    try:
        binding = await runtime.provision(
            {"session": ident, "message": "policy check", "position": position.model_dump()}
        )
        result = await asyncio.to_thread(
            gateway.exec,
            binding["name"],
            [
                PYTHON,
                "-c",
                'from pathlib import Path; print(Path("/private-canary/readable").read_text())',
            ],
            workspace="default",
            timeout_seconds=10,
            no_login_shell=True,
        )
        assert result.exit_code == 0 and result.stdout.strip() == "denied"
    finally:
        assert (await runtime.close({"binding": binding}))["cleanup"] == "DELETED"

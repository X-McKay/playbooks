"""Lifecycle races: an accepted binding may lag resources already created."""

import asyncio
import threading
from types import SimpleNamespace

import grpc
import pytest

from bridge_probe.openshell import OpenShellSession


class Missing(grpc.RpcError):
    def code(self):
        return grpc.StatusCode.NOT_FOUND


class FakeClient:
    def __init__(self):
        self.resources = {}
        self.creating = threading.Event()
        self.release = threading.Event()
        self.release.set()

    def get(self, name, **kwargs):
        if name not in self.resources:
            raise Missing()
        return self.resources[name]

    def create(self, name, labels, **kwargs):
        self.creating.set()
        assert self.release.wait(5)
        ref = SimpleNamespace(name=name, id=name, labels=labels)
        self.resources[name] = ref
        return ref

    def wait_ready(self, name, **kwargs):
        raise RuntimeError("injected readiness failure")

    def list(self, **kwargs):
        return SimpleNamespace(all=lambda: list(self.resources.values()))

    def delete(self, name, **kwargs):
        self.resources.pop(name, None)

    def wait_deleted(self, name, **kwargs):
        assert name not in self.resources


def remote(client):
    return OpenShellSession(client, None, session="race", manifest="demo-v1", key=b"x" * 32)


async def test_failed_replacement_cleanup_reconciles_unaccepted_generation():
    client = FakeClient()
    session = remote(client)
    start = {"session": "race", "message": "Inspect", "position": {}}
    with pytest.raises(RuntimeError, match="readiness"):
        await session.provision(start)
    old = {"session": "race", "generation": 1, "name": session.name, "sandbox_id": session.name}
    for _ in range(3):
        with pytest.raises(RuntimeError, match="readiness"):
            await session.replace({"start": start, "position": {}, "binding": old})
    assert len(client.resources) == 1
    assert (await session.close({"start": start, "binding": old}))["cleanup"] == "DELETED"
    assert not client.resources


async def test_cancelled_create_settles_before_terminal_cleanup():
    client = FakeClient()
    client.release.clear()
    session = remote(client)
    start = {"session": "race", "message": "Inspect", "position": {}}
    task = asyncio.create_task(session.provision(start))
    while not client.creating.is_set():
        await asyncio.sleep(0.01)
    task.cancel()
    await asyncio.sleep(0.02)
    assert not task.done(), "creation must settle before cancellation completes"
    client.release.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert (await session.close({"start": start, "binding": None}))["cleanup"] == "DELETED"
    assert not client.resources


async def test_terminal_cleanup_fences_a_delayed_initial_lookup():
    from bridge_probe.transport import ProtocolError

    client = FakeClient()
    entered = threading.Event()
    released = threading.Event()
    original_get = client.get

    def delayed_get(name, **kwargs):
        entered.set()
        assert released.wait(5)
        return original_get(name, **kwargs)

    client.get = delayed_get
    session = remote(client)
    start = {"session": "race", "message": "Inspect", "position": {}}
    task = asyncio.create_task(session.provision(start))
    while not entered.is_set():
        await asyncio.sleep(0.01)
    assert (await session.close({"start": start, "binding": None}))["cleanup"] == "DELETED"
    released.set()
    with pytest.raises(ProtocolError, match="closing"):
        await task
    assert not client.resources

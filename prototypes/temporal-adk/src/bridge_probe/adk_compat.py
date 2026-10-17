"""Pinned ADK lifecycle seams; contains no Temporal or agent-repository imports."""

import random
import uuid
from contextlib import contextmanager

from google.adk.platform import reset_random_provider, set_random_provider
from google.adk.platform.time import reset_time_provider, set_time_provider
from google.adk.platform.uuid import reset_id_provider, set_id_provider
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .records import encode_model


@contextmanager
def deterministic_runtime(invocation="probe-invocation"):
    counter = iter(range(1000000))
    rng = random.Random(42)
    set_time_provider(lambda: 1700000000.0)
    set_id_provider(lambda: str(uuid.uuid5(uuid.NAMESPACE_URL, f"{invocation}:{next(counter)}")))
    set_random_provider(lambda: rng)
    try:
        yield
    finally:
        reset_time_provider()
        reset_id_provider()
        reset_random_provider()


async def run_agent(factory, message="Inspect this repository"):
    """Drain ADK to exhaustion, closing its iterator and resources on cancellation."""
    with deterministic_runtime():
        agent = factory()
        sessions = InMemorySessionService()
        await sessions.create_session(app_name="probe", user_id="user", session_id="session")
        runner = Runner(agent=agent, app_name="probe", session_service=sessions)
        iterator = runner.run_async(
            user_id="user",
            session_id="session",
            new_message=types.Content(role="user", parts=[types.Part(text=message)]),
        )
        text = ""
        try:
            async for event in iterator:
                if event.is_final_response() and event.content:
                    text = "".join(p.text or "" for p in event.content.parts or [])
            session = await sessions.get_session(
                app_name="probe", user_id="user", session_id="session"
            )
            return {"session": encode_model(session), "final_text": text}
        finally:
            await iterator.aclose()
            await runner.close()

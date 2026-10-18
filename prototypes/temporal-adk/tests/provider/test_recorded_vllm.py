"""Replay sanitized accepted responses captured from the real local vLLM model."""

import json
from pathlib import Path

from google.adk.models.llm_response import LlmResponse

from bridge_probe.process import run_child
from bridge_probe.records import decode_model, encode_model


async def test_real_vllm_recording_reconstructs_each_prefix_in_fresh_process(tmp_path):
    recorded = json.loads((Path(__file__).parents[1] / "fixtures/vllm_recording.json").read_text())
    for entry in recorded["entries"]:
        if entry["operation"]["kind"] == "model":
            assert encode_model(decode_model(LlmResponse, entry["outcome"])) == entry["outcome"]
    for cursor in range(len(recorded["entries"]) + 1):
        result = await run_child(
            "bridge_probe.replay",
            {
                "tape": recorded["entries"][:cursor],
                "pending": None,
                "workspace": str(tmp_path),
                "session": recorded["invocation"],
                "manifest": recorded["manifest"],
                "message": recorded["message"],
                "provider": "vllm",
            },
            timeout=30,
        )
        if cursor < len(recorded["entries"]):
            assert result["operation"] == recorded["entries"][cursor]["operation"]
        else:
            assert result["status"] == "done"
            assert result["result"]["final_text"] == recorded["final_text"]
    # No tool bodies ran during reconstruction, including write_report.
    assert not (tmp_path / "report.md").exists()

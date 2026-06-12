from __future__ import annotations

from pathlib import Path

from agent_trust_lab.copilot.session_extract import codex_session_to_transcript


def test_codex_session_to_transcript_redacts_and_labels(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    session.write_text(
        "\n".join(
            [
                '{"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"Please review C:\\\\Users\\\\jie13\\\\secret.txt and email me at test@example.com"}]}}',
                '{"type":"response_item","payload":{"type":"function_call","name":"shell_command","arguments":"{\\"command\\":\\"type C:\\\\\\\\Users\\\\\\\\jie13\\\\\\\\secret.txt\\"}"}}',
                '{"type":"response_item","payload":{"type":"function_call_output","output":"Error at https://example.com for 17731888200"}}',
                '{"type":"response_item","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":"I need human review before using this result."}]}}',
            ]
        ),
        encoding="utf-8",
    )

    transcript = codex_session_to_transcript(session, case_id="CASE-1", expected_risk_level="high")

    assert "SYSTEM: case_id=CASE-1" in transcript
    assert "USER:" in transcript
    assert "AGENT:" in transcript
    assert "TOOL:" in transcript
    assert "<WINDOWS_PATH>" in transcript
    assert "<EMAIL>" in transcript
    assert "<URL>" in transcript
    assert "<PHONE>" in transcript


def test_codex_session_to_transcript_skips_boilerplate(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    session.write_text(
        "\n".join(
            [
                '{"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"# AGENTS.md instructions for C:\\\\Users\\\\jie13\\\\Documents\\\\Playground"}]}}',
                '{"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"Please review this agent result."}]}}',
                '{"type":"response_item","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":"I need human review before using this result."}]}}',
            ]
        ),
        encoding="utf-8",
    )

    transcript = codex_session_to_transcript(session)

    assert "# AGENTS.md instructions" not in transcript
    assert "Please review this agent result." in transcript

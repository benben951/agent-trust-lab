from pathlib import Path
import subprocess
import sys

from agent_trust_lab.reviewer import evaluate_case, load_case, render_markdown


def test_synthetic_case_requires_human_review() -> None:
    case = load_case(Path("examples") / "synthetic_aml_case.json")
    result = evaluate_case(case)

    assert result["human_review_required"] is True
    assert result["trust_level"] == "low"
    assert result["recommendation"] == "reject_or_escalate"
    assert {item["type"] for item in result["findings"]} >= {
        "unsafe_certainty",
        "missing_policy_signal",
        "missing_escalation",
        "unsupported_claim",
        "risk_label_mismatch",
    }


def test_render_markdown_contains_report_sections() -> None:
    case = load_case(Path("examples") / "synthetic_aml_case.json")
    result = evaluate_case(case)
    markdown = render_markdown(case, result)

    assert "# Agent Trust Report" in markdown
    assert "## Findings" in markdown
    assert "## Evidence Provided" in markdown


def test_batch_review_cli_generates_summary(tmp_path: Path) -> None:
    out_dir = tmp_path / "reports"
    summary = tmp_path / "summary.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_trust_lab.cli",
            "batch-review",
            "--cases-dir",
            "examples/cases",
            "--out-dir",
            str(out_dir),
            "--summary",
            str(summary),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert summary.exists()
    assert len(list(out_dir.glob("*.md"))) >= 10

from pathlib import Path
import json
import subprocess
import sys

from agent_trust_lab.metrics import summarize_results
from agent_trust_lab.reviewer import evaluate_case, load_case, render_markdown
from agent_trust_lab.workflow import evaluate_workflow, render_workflow_markdown


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


def test_metrics_summary_counts_review_risk() -> None:
    batch_summary = json.loads(Path("examples/batch_summary.json").read_text(encoding="utf-8"))
    metrics = summarize_results(batch_summary)

    assert metrics["total_cases"] == 10
    assert metrics["manual_review_cases"] == 8
    assert metrics["low_trust_cases"] == 4
    assert metrics["average_risk_score"] == 53.0
    assert metrics["finding_distribution"]["risk_label_mismatch"] == 9


def test_summarize_cli_generates_metrics_file(tmp_path: Path) -> None:
    metrics_path = tmp_path / "evaluation_metrics.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_trust_lab.cli",
            "summarize",
            "--summary",
            "examples/batch_summary.json",
            "--out",
            str(metrics_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["manual_review_rate"] == 0.8


def test_workflow_review_has_role_trace() -> None:
    case = load_case(Path("examples") / "cases" / "agent_tool_failure.json")
    workflow = evaluate_workflow(case)

    assert workflow["workflow_status"] == "needs_human_review"
    assert "evidence_reviewer" in {item["role"] for item in workflow["role_reviews"]}
    assert "final_reviewer" in {item["role"] for item in workflow["role_reviews"]}
    assert "risk_reviewer" in workflow["failed_roles"]


def test_workflow_review_cli_generates_markdown_and_json(tmp_path: Path) -> None:
    report_path = tmp_path / "workflow_report.md"
    json_path = tmp_path / "workflow_report.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_trust_lab.cli",
            "workflow-review",
            "--case",
            "examples/cases/agent_tool_failure.json",
            "--out",
            str(report_path),
            "--json-out",
            str(json_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    markdown = report_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Multi-Role Agent Trust Workflow Report" in markdown
    assert "## Role Trace" in markdown
    assert payload["workflow_status"] == "needs_human_review"


def test_render_workflow_markdown_contains_public_boundary() -> None:
    case = load_case(Path("examples") / "cases" / "safe_low_risk_case.json")
    workflow = evaluate_workflow(case)
    markdown = render_workflow_markdown(case, workflow)

    assert "## Public Safety Boundary" in markdown
    assert "synthetic public-safe data" in markdown

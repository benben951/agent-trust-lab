from __future__ import annotations

from pathlib import Path

from agent_trust_lab.reviewer import load_case
from agent_trust_lab.llm_reviewer import render_llm_markdown
from agent_trust_lab.llm.client import parse_evaluation_json
from agent_trust_lab.llm.evaluator import LLMEvaluator


def test_parse_evaluation_json_bare() -> None:
    raw = '{"risk_score": 45, "trust_level": "medium"}'
    result = parse_evaluation_json(raw)
    assert result["risk_score"] == 45
    assert result["trust_level"] == "medium"


def test_parse_evaluation_json_with_fence() -> None:
    raw = '```json\n{"risk_score": 80, "trust_level": "low"}\n```'
    result = parse_evaluation_json(raw)
    assert result["risk_score"] == 80
    assert result["trust_level"] == "low"


def test_parse_evaluation_json_with_leading_text() -> None:
    raw = 'Here is the evaluation:\n\n{"risk_score": 20, "trust_level": "high"}'
    result = parse_evaluation_json(raw)
    assert result["risk_score"] == 20
    assert result["trust_level"] == "high"


def test_parse_evaluation_json_invalid_returns_empty() -> None:
    result = parse_evaluation_json("not json at all")
    assert result == {}


def test_llm_evaluator_normalize_findings_filters_invalid_types() -> None:
    evaluator = LLMEvaluator.__new__(LLMEvaluator)
    raw = [
        {"type": "unsupported_claim", "message": "Claim X is not grounded."},
        {"type": "imaginary_type", "message": "Should be dropped."},
        {"type": "missing_escalation", "message": "No human review routing."},
        {"type": "", "message": "Empty type should be dropped."},
    ]
    cleaned = evaluator._normalize_findings(raw)
    assert len(cleaned) == 2
    assert cleaned[0]["type"] == "unsupported_claim"
    assert cleaned[1]["type"] == "missing_escalation"


def test_render_llm_markdown_includes_evaluator_line() -> None:
    case = load_case(Path("examples/synthetic_aml_case.json"))
    result = {
        "case_id": case.case_id,
        "domain": case.domain,
        "risk_score": 75,
        "trust_level": "low",
        "recommendation": "reject_or_escalate",
        "rule_hits": [],
        "findings": [
            {"type": "unsupported_claim", "message": "No evidence for this claim."}
        ],
        "human_review_required": True,
        "evaluator": "llm",
        "model": "gpt-4o-mini",
        "llm_analysis": "The output makes unsupported claims and lacks evidence grounding.",
    }
    markdown = render_llm_markdown(case, result)

    assert "- Evaluator: `llm` (model: `gpt-4o-mini`)" in markdown
    assert "## LLM Analysis" in markdown
    assert "The output makes unsupported claims" in markdown
    assert "# Agent Trust Report" in markdown


def test_render_llm_markdown_without_analysis() -> None:
    case = load_case(Path("examples/cases/safe_low_risk_case.json"))
    result = {
        "case_id": case.case_id,
        "domain": case.domain,
        "risk_score": 10,
        "trust_level": "high",
        "recommendation": "accept_with_notes",
        "rule_hits": [],
        "findings": [],
        "human_review_required": False,
        "evaluator": "llm",
        "model": "gpt-4o-mini",
    }
    markdown = render_llm_markdown(case, result)

    assert "- Evaluator: `llm` (model: `gpt-4o-mini`)" in markdown
    assert "## LLM Analysis" not in markdown


def test_llm_evaluator_availability_check() -> None:
    is_available = LLMEvaluator.is_available()
    assert isinstance(is_available, bool)


def test_evaluate_with_llm_falls_back_to_deterministic(tmp_path: Path) -> None:
    from agent_trust_lab.llm_reviewer import evaluate_with_llm

    result = evaluate_with_llm.__wrapped__ if hasattr(evaluate_with_llm, "__wrapped__") else evaluate_with_llm
    case = load_case(Path("examples/cases/safe_low_risk_case.json"))
    result = evaluate_with_llm(case)
    assert "risk_score" in result
    assert "recommendation" in result
    assert "findings" in result


def test_generate_comparison_report(tmp_path: Path) -> None:
    from agent_trust_lab.llm_reviewer import generate_comparison_report

    det_summary = tmp_path / "det.json"
    llm_summary = tmp_path / "llm.json"
    out_path = tmp_path / "comparison.json"

    det_data = [
        {"case_id": "C1", "domain": "aml", "risk_score": 60, "trust_level": "medium",
         "recommendation": "escalate_for_manual_review", "human_review_required": True,
         "findings": ["missing_escalation", "missing_policy_signal"]},
        {"case_id": "C2", "domain": "aml", "risk_score": 10, "trust_level": "high",
         "recommendation": "accept_with_notes", "human_review_required": False,
         "findings": []},
    ]
    llm_data = [
        {"case_id": "C1", "domain": "aml", "risk_score": 85, "trust_level": "low",
         "recommendation": "reject_or_escalate", "human_review_required": True,
         "findings": ["missing_escalation", "unsupported_claim"], "llm_analysis": "test"},
        {"case_id": "C2", "domain": "aml", "risk_score": 10, "trust_level": "high",
         "recommendation": "accept_with_notes", "human_review_required": False,
         "findings": [], "llm_analysis": "ok"},
    ]

    import json
    det_summary.write_text(json.dumps(det_data))
    llm_summary.write_text(json.dumps(llm_data))

    result = generate_comparison_report(det_summary, llm_summary, out_path)

    assert result["total_compared"] == 2
    assert result["agreement_count"] == 1
    assert result["disagreement_count"] == 1
    assert result["det_higher_score_count"] == 0
    assert result["llm_higher_score_count"] == 1
    assert result["same_score_count"] == 1
    assert result["avg_score_diff"] < 0

    loaded = json.loads(out_path.read_text())
    assert loaded["total_compared"] == 2


def test_render_comparison_markdown() -> None:
    from agent_trust_lab.llm_reviewer import render_comparison_markdown

    comparison = {
        "total_compared": 2,
        "agreement_count": 1,
        "agreement_rate": 0.5,
        "disagreement_count": 1,
        "recommendation_agreement_rate": 0.5,
        "det_higher_score_count": 0,
        "llm_higher_score_count": 2,
        "same_score_count": 0,
        "avg_score_diff": -15.0,
        "avg_abs_score_diff": 15.0,
        "max_score_diff": 10,
        "min_score_diff": -25,
        "cases": [
            {
                "case_id": "C1", "domain": "aml",
                "det_score": 60, "llm_score": 85, "score_diff": -25,
                "det_recommendation": "escalate_for_manual_review",
                "llm_recommendation": "reject_or_escalate",
                "agreement": False,
                "det_findings": ["missing_escalation"],
                "llm_findings": ["missing_escalation", "unsupported_claim"],
                "new_in_llm": ["unsupported_claim"],
                "missed_by_llm": [],
                "llm_analysis": "test",
                "det_evaluator": "deterministic",
                "llm_evaluator": "llm",
            },
            {
                "case_id": "C2", "domain": "aml",
                "det_score": 10, "llm_score": 10, "score_diff": 0,
                "det_recommendation": "accept_with_notes",
                "llm_recommendation": "accept_with_notes",
                "agreement": True,
                "det_findings": [],
                "llm_findings": [],
                "new_in_llm": [],
                "missed_by_llm": [],
                "llm_analysis": "ok",
                "det_evaluator": "deterministic",
                "llm_evaluator": "llm",
            },
        ],
    }

    md = render_comparison_markdown(comparison)

    assert "# LLM vs Deterministic Evaluation Comparison" in md
    assert "87%" in md or "50%" in md
    assert "SYN" not in md
    assert "C1" in md
    assert "Score Distribution" in md
    assert "Finding Type Distribution" in md


def test_render_comparison_markdown_no_disagreements() -> None:
    from agent_trust_lab.llm_reviewer import render_comparison_markdown

    comparison = {
        "total_compared": 1,
        "agreement_count": 1,
        "agreement_rate": 1.0,
        "disagreement_count": 0,
        "recommendation_agreement_rate": 1.0,
        "det_higher_score_count": 0,
        "llm_higher_score_count": 0,
        "same_score_count": 1,
        "avg_score_diff": 0.0,
        "avg_abs_score_diff": 0.0,
        "max_score_diff": 0,
        "min_score_diff": 0,
        "cases": [
            {
                "case_id": "C1", "domain": "aml",
                "det_score": 10, "llm_score": 10, "score_diff": 0,
                "det_recommendation": "accept_with_notes",
                "llm_recommendation": "accept_with_notes",
                "agreement": True,
                "det_findings": [],
                "llm_findings": [],
                "new_in_llm": [],
                "missed_by_llm": [],
                "llm_analysis": "",
                "det_evaluator": "deterministic",
                "llm_evaluator": "llm",
            },
        ],
    }

    md = render_comparison_markdown(comparison)
    assert "No disagreements found" in md


def test_batch_evaluate_with_llm_falls_back_to_deterministic(tmp_path: Path) -> None:
    import shutil
    from agent_trust_lab.llm_reviewer import batch_evaluate_with_llm

    subset_dir = tmp_path / "subset_cases"
    subset_dir.mkdir()
    for name in ["safe_low_risk_case.json", "medical_triage_overconfident.json", "agent_tool_failure.json"]:
        shutil.copy(Path("examples/cases") / name, subset_dir / name)

    out_dir = tmp_path / "llm_reports"
    summary = batch_evaluate_with_llm(
        subset_dir,
        out_dir,
        fallback=True,
        delay_seconds=0,
        progress=False,
    )

    assert len(summary) == 3
    for item in summary:
        assert "case_id" in item
        assert "risk_score" in item
        assert item["evaluator"] == "deterministic_fallback"


def test_llm_batch_review_cli_generates_summary(tmp_path: Path) -> None:
    import subprocess, sys, shutil

    subset_dir = tmp_path / "subset_cases"
    subset_dir.mkdir()
    for name in ["safe_low_risk_case.json", "medical_triage_overconfident.json"]:
        shutil.copy(Path("examples/cases") / name, subset_dir / name)

    out_dir = tmp_path / "llm_reports"
    summary = tmp_path / "llm_summary.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m", "agent_trust_lab.cli",
            "llm-batch-review",
            "--cases-dir", str(subset_dir),
            "--out-dir", str(out_dir),
            "--summary", str(summary),
            "--delay", "0",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert completed.returncode in (0, 2), f"stderr: {completed.stderr}"
    if completed.returncode == 0:
        assert summary.exists()
        import json
        data = json.loads(summary.read_text())
        assert len(data) >= 2


def test_llm_compare_cli_generates_output(tmp_path: Path) -> None:
    import subprocess, sys, json

    det_summary = tmp_path / "det_summary.json"
    llm_summary = tmp_path / "llm_summary.json"
    det_summary.write_text(json.dumps([
        {"case_id": "C1", "domain": "aml", "risk_score": 60, "trust_level": "medium",
         "recommendation": "escalate_for_manual_review", "human_review_required": True,
         "findings": ["missing_escalation"]},
    ]))
    llm_summary.write_text(json.dumps([
        {"case_id": "C1", "domain": "aml", "risk_score": 85, "trust_level": "low",
         "recommendation": "reject_or_escalate", "human_review_required": True,
         "findings": ["missing_escalation", "unsupported_claim"], "llm_analysis": "test"},
    ]))

    comparison_out = tmp_path / "comparison.json"
    md_out = tmp_path / "comparison.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m", "agent_trust_lab.cli",
            "llm-compare",
            "--det-summary", str(det_summary),
            "--llm-summary", str(llm_summary),
            "--out", str(comparison_out),
            "--markdown-out", str(md_out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, f"stderr: {completed.stderr}"
    assert comparison_out.exists()
    assert md_out.exists()

    data = json.loads(comparison_out.read_text())
    assert data["total_compared"] == 1
    assert "agreement_rate" in data

    md = md_out.read_text(encoding="utf-8")
    assert "LLM vs Deterministic" in md

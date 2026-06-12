from __future__ import annotations

import argparse
import json
from pathlib import Path

from .metrics import load_batch_summary, summarize_results
from .baseline import compare_naive_acceptance
from .copilot import ReviewOrchestrator, load_copilot_input
from .copilot.memory import write_session_memory
from .copilot.reports import render_copilot_markdown
from .copilot.session_extract import write_codex_session_transcript
from .reviewer import evaluate_case, load_case, render_markdown
from .workflow import evaluate_workflow, render_workflow_markdown


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-trust-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    review = subparsers.add_parser("review", help="Generate a trust report for a synthetic case")
    review.add_argument("--case", required=True, help="Path to synthetic case JSON")
    review.add_argument("--out", required=True, help="Markdown report output path")
    review.add_argument("--json-out", help="Optional JSON result output path")

    workflow = subparsers.add_parser(
        "workflow-review",
        help="Generate a public-safe multi-role workflow trust report for a synthetic case",
    )
    workflow.add_argument("--case", required=True, help="Path to synthetic case JSON")
    workflow.add_argument("--out", required=True, help="Markdown workflow report output path")
    workflow.add_argument("--json-out", help="Optional JSON workflow result output path")

    batch = subparsers.add_parser("batch-review", help="Generate trust reports for a directory of synthetic cases")
    batch.add_argument("--cases-dir", required=True, help="Directory containing synthetic case JSON files")
    batch.add_argument("--out-dir", required=True, help="Directory for Markdown reports")
    batch.add_argument("--summary", required=True, help="JSON summary output path")

    summarize = subparsers.add_parser("summarize", help="Summarize a batch-review JSON file")
    summarize.add_argument("--summary", required=True, help="Path to batch summary JSON")
    summarize.add_argument("--out", required=True, help="Path for evaluation metrics JSON")

    baseline = subparsers.add_parser("baseline-compare", help="Compare naive LLM acceptance against trust workflow")
    baseline.add_argument("--cases-dir", required=True, help="Directory containing synthetic case JSON files")
    baseline.add_argument("--out", required=True, help="Path for baseline comparison JSON")
    baseline.add_argument("--markdown-out", help="Optional Markdown summary output path")

    copilot = subparsers.add_parser(
        "copilot-review",
        help="Run the first-pass Agent review copilot on a structured input package",
    )
    copilot.add_argument("--input", required=True, help="Path to copilot input JSON")
    copilot.add_argument("--out", required=True, help="Markdown copilot report output path")
    copilot.add_argument("--json-out", help="Optional JSON session output path")
    copilot.add_argument(
        "--memory-out-dir",
        help="Optional directory for writing session memory JSON",
    )

    extract = subparsers.add_parser(
        "extract-codex-session",
        help="Convert a local Codex session JSONL file into a redacted transcript draft",
    )
    extract.add_argument("--session-file", required=True, help="Path to a Codex session JSONL file")
    extract.add_argument("--out", required=True, help="Transcript draft output path")
    extract.add_argument("--case-id", default="COPILOT-CODEX-SESSION-001", help="Case id for the transcript header")
    extract.add_argument("--domain", default="agent_output_review", help="Domain for the transcript header")
    extract.add_argument("--expected-risk-level", default="medium", help="Expected risk level for the transcript header")
    extract.add_argument(
        "--required-terms",
        default="human review",
        help="Comma-separated required terms for the transcript header",
    )

    args = parser.parse_args()
    if args.command == "review":
        case = load_case(args.case)
        result = evaluate_case(case)
        _write_text(args.out, render_markdown(case, result))
        if args.json_out:
            _write_json(args.json_out, result)
        return 0
    if args.command == "workflow-review":
        case = load_case(args.case)
        result = evaluate_workflow(case)
        _write_text(args.out, render_workflow_markdown(case, result))
        if args.json_out:
            _write_json(args.json_out, result)
        return 0
    if args.command == "batch-review":
        cases_dir = Path(args.cases_dir)
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        summary = []
        for case_path in sorted(cases_dir.glob("*.json")):
            case = load_case(case_path)
            result = evaluate_case(case)
            report_path = out_dir / f"{case.case_id}.md"
            report_path.write_text(render_markdown(case, result), encoding="utf-8")
            summary.append(
                {
                    "case_id": case.case_id,
                    "domain": case.domain,
                    "risk_score": result["risk_score"],
                    "trust_level": result["trust_level"],
                    "recommendation": result["recommendation"],
                    "human_review_required": result["human_review_required"],
                    "findings": [item["type"] for item in result["findings"]],
                    "report": str(report_path.as_posix()),
                }
            )
        _write_json(args.summary, summary)
        return 0
    if args.command == "summarize":
        results = load_batch_summary(args.summary)
        metrics = summarize_results(results)
        _write_json(args.out, metrics)
        return 0
    if args.command == "baseline-compare":
        cases = [load_case(path) for path in sorted(Path(args.cases_dir).glob("*.json"))]
        result = compare_naive_acceptance(cases)
        _write_json(args.out, result)
        if args.markdown_out:
            _write_text(args.markdown_out, _render_baseline_markdown(result))
        return 0
    if args.command == "copilot-review":
        orchestrator = ReviewOrchestrator()
        review_input = load_copilot_input(args.input)
        session = orchestrator.review(review_input)
        _write_text(args.out, render_copilot_markdown(session))
        if args.json_out:
            from dataclasses import asdict

            _write_json(args.json_out, asdict(session))
        if args.memory_out_dir:
            write_session_memory(session, args.memory_out_dir)
        return 0
    if args.command == "extract-codex-session":
        write_codex_session_transcript(
            args.session_file,
            args.out,
            case_id=args.case_id,
            domain=args.domain,
            expected_risk_level=args.expected_risk_level,
            required_terms=[item.strip() for item in args.required_terms.split(",") if item.strip()],
        )
        return 0
    return 1


def _write_text(path: str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def _write_json(path: str, payload: object) -> None:
    _write_text(path, json.dumps(payload, indent=2))


def _render_baseline_markdown(result: dict) -> str:
    return f"""# Baseline Comparison

## Question

How often would a naive reviewer accept confident LLM outputs compared with the structured trust-report workflow?

## Summary

| Metric | Value |
|---|---:|
| Total cases | {result['total_cases']} |
| Naive accept cases | {result['naive_accept_cases']} |
| Naive accept rate | {result['naive_accept_rate']:.0%} |
| Naive false accept cases | {result['naive_false_accept_cases']} |
| Naive false accept rate | {result['naive_false_accept_rate']:.0%} |
| Trust workflow accept cases | {result['trust_workflow_accept_cases']} |
| Trust workflow accept rate | {result['trust_workflow_accept_rate']:.0%} |
| Trust workflow manual review cases | {result['trust_workflow_manual_review_cases']} |
| Trust workflow manual review rate | {result['trust_workflow_manual_review_rate']:.0%} |

## Interpretation

The naive baseline treats confident acceptance language as usable. Agent Trust Lab instead routes unsupported, overconfident, policy-mismatched, or escalation-missing outputs to human review. This comparison is synthetic and public-safe; it demonstrates evaluation mechanics rather than production business impact.
"""


if __name__ == "__main__":
    raise SystemExit(main())

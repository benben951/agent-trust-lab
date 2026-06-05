from __future__ import annotations

import argparse
import json
from pathlib import Path

from .metrics import load_batch_summary, summarize_results
from .reviewer import evaluate_case, load_case, render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-trust-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    review = subparsers.add_parser("review", help="Generate a trust report for a synthetic case")
    review.add_argument("--case", required=True, help="Path to synthetic case JSON")
    review.add_argument("--out", required=True, help="Markdown report output path")
    review.add_argument("--json-out", help="Optional JSON result output path")

    batch = subparsers.add_parser("batch-review", help="Generate trust reports for a directory of synthetic cases")
    batch.add_argument("--cases-dir", required=True, help="Directory containing synthetic case JSON files")
    batch.add_argument("--out-dir", required=True, help="Directory for Markdown reports")
    batch.add_argument("--summary", required=True, help="JSON summary output path")

    summarize = subparsers.add_parser("summarize", help="Summarize a batch-review JSON file")
    summarize.add_argument("--summary", required=True, help="Path to batch summary JSON")
    summarize.add_argument("--out", required=True, help="Path for evaluation metrics JSON")

    args = parser.parse_args()
    if args.command == "review":
        case = load_case(args.case)
        result = evaluate_case(case)
        Path(args.out).write_text(render_markdown(case, result), encoding="utf-8")
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")
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
        Path(args.summary).write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return 0
    if args.command == "summarize":
        results = load_batch_summary(args.summary)
        metrics = summarize_results(results)
        Path(args.out).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

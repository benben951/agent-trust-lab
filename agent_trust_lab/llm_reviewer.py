from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .llm.evaluator import LLMEvaluator
from .llm.client import LLMClient, LLMNotAvailableError
from .reviewer import evaluate_case, load_case, render_markdown
from .schema import ReviewCase


def evaluate_with_llm(
    case: ReviewCase,
    *,
    client: LLMClient | None = None,
    fallback: bool = True,
) -> dict[str, Any]:
    evaluator = LLMEvaluator(client)
    try:
        return evaluator.evaluate(case)
    except Exception:
        if fallback:
            result = evaluate_case(case)
            result["evaluator"] = "deterministic_fallback"
            return result
        raise


def batch_evaluate_with_llm(
    cases_dir: str | Path,
    out_dir: str | Path,
    *,
    client: LLMClient | None = None,
    fallback: bool = True,
    delay_seconds: float = 0.5,
    progress: bool = True,
) -> list[dict[str, Any]]:
    cases_dir = Path(cases_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, Any]] = []

    case_paths = sorted(cases_dir.glob("*.json"))
    total = len(case_paths)

    for idx, case_path in enumerate(case_paths, 1):
        case = load_case(case_path)
        if progress:
            print(f"[{idx}/{total}] Evaluating {case.case_id} ...", end=" ", flush=True)

        result = evaluate_with_llm(case, client=client, fallback=fallback)

        report_path = out_dir / f"{case.case_id}_llm.md"
        report_path.write_text(render_llm_markdown(case, result), encoding="utf-8")

        evaluator = result.get("evaluator", "llm")
        if progress:
            status = "OK" if evaluator == "llm" else f"fallback({evaluator})"
            print(f"{status} (score={result['risk_score']})")

        summary.append({
            "case_id": case.case_id,
            "domain": case.domain,
            "evaluator": evaluator,
            "risk_score": result["risk_score"],
            "trust_level": result["trust_level"],
            "recommendation": result["recommendation"],
            "human_review_required": result["human_review_required"],
            "findings": [item["type"] for item in result["findings"]],
            "llm_analysis": result.get("llm_analysis", ""),
            "report": str(report_path.as_posix()),
        })

        if delay_seconds > 0 and idx < total:
            time.sleep(delay_seconds)

    return summary


def generate_comparison_report(
    det_summary_path: str | Path,
    llm_summary_path: str | Path,
    out_path: str | Path,
) -> dict[str, Any]:
    det = json.loads(Path(det_summary_path).read_text(encoding="utf-8"))
    llm = json.loads(Path(llm_summary_path).read_text(encoding="utf-8"))

    det_by_id = {item["case_id"]: item for item in det}
    llm_by_id = {item["case_id"]: item for item in llm}
    common_ids = sorted(set(det_by_id) & set(llm_by_id))

    agreements = 0
    disagreements = 0
    score_diffs: list[int] = []
    det_higher = 0
    llm_higher = 0
    same_score = 0
    cases_detail: list[dict[str, Any]] = []

    for cid in common_ids:
        d = det_by_id[cid]
        l = llm_by_id[cid]
        ds = d["risk_score"]
        ls = l["risk_score"]
        diff = ds - ls
        score_diffs.append(diff)

        if d["recommendation"] == l["recommendation"]:
            agreements += 1
        else:
            disagreements += 1

        if diff > 0:
            det_higher += 1
        elif diff < 0:
            llm_higher += 1
        else:
            same_score += 1

        d_findings = set(d["findings"])
        l_findings = set(l["findings"])
        new_findings = l_findings - d_findings
        missed_findings = d_findings - l_findings

        cases_detail.append({
            "case_id": cid,
            "domain": d["domain"],
            "det_score": ds,
            "llm_score": ls,
            "score_diff": diff,
            "det_recommendation": d["recommendation"],
            "llm_recommendation": l["recommendation"],
            "agreement": d["recommendation"] == l["recommendation"],
            "det_findings": sorted(d_findings),
            "llm_findings": sorted(l_findings),
            "new_in_llm": sorted(new_findings),
            "missed_by_llm": sorted(missed_findings),
            "llm_analysis": l.get("llm_analysis", ""),
            "det_evaluator": "deterministic",
            "llm_evaluator": l.get("evaluator", "llm"),
        })

    avg_diff = sum(score_diffs) / len(score_diffs) if score_diffs else 0.0
    abs_diffs = [abs(d) for d in score_diffs]
    avg_abs_diff = sum(abs_diffs) / len(abs_diffs) if abs_diffs else 0.0

    comparison: dict[str, Any] = {
        "total_compared": len(common_ids),
        "agreement_count": agreements,
        "agreement_rate": round(agreements / len(common_ids), 4) if common_ids else 0.0,
        "disagreement_count": disagreements,
        "recommendation_agreement_rate": round(agreements / len(common_ids), 4) if common_ids else 0.0,
        "det_higher_score_count": det_higher,
        "llm_higher_score_count": llm_higher,
        "same_score_count": same_score,
        "avg_score_diff": round(avg_diff, 2),
        "avg_abs_score_diff": round(avg_abs_diff, 2),
        "max_score_diff": max(score_diffs) if score_diffs else 0,
        "min_score_diff": min(score_diffs) if score_diffs else 0,
        "cases": cases_detail,
    }

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(comparison, indent=2), encoding="utf-8")

    return comparison


def render_llm_markdown(case: ReviewCase, result: dict[str, Any]) -> str:
    base = render_markdown(case, result)
    evaluator_line = f"- Evaluator: `{result.get('evaluator', 'llm')}`"
    model = result.get("model")
    if model:
        evaluator_line += f" (model: `{model}`)"
    base = base.replace(
        "## Case\n",
        f"## Case\n{evaluator_line}\n",
    )
    analysis = result.get("llm_analysis")
    if analysis:
        base += f"\n## LLM Analysis\n\n{analysis}\n"
    return base


def render_comparison_markdown(comparison: dict[str, Any]) -> str:
    lines = [
        "# LLM vs Deterministic Evaluation Comparison",
        "",
        "## Summary",
        "",
        f"- Total cases compared: **{comparison['total_compared']}**",
        f"- Recommendation agreement rate: **{comparison['recommendation_agreement_rate']:.0%}**",
        f"- Deterministic gave higher scores in **{comparison['det_higher_score_count']}** cases",
        f"- LLM gave higher scores in **{comparison['llm_higher_score_count']}** cases",
        f"- Same score in **{comparison['same_score_count']}** cases",
        f"- Average score difference (det - llm): **{comparison['avg_score_diff']:+.1f}**",
        f"- Average absolute score difference: **{comparison['avg_abs_score_diff']:.1f}**",
        f"- Max score difference: **{comparison['max_score_diff']}**, Min: **{comparison['min_score_diff']}**",
        "",
        "## Disagreement Cases",
        "",
    ]

    disagreements = [c for c in comparison["cases"] if not c["agreement"]]
    if disagreements:
        lines.append("| Case ID | Domain | Det Score | LLM Score | Diff | Det Rec | LLM Rec | New Findings | Missed Findings |")
        lines.append("|---------|--------|-----------|-----------|------|---------|---------|-------------|----------------|")
        for c in disagreements:
            new_f = ", ".join(c["new_in_llm"]) or "-"
            missed_f = ", ".join(c["missed_by_llm"]) or "-"
            lines.append(
                f"| {c['case_id']} | {c['domain']} | {c['det_score']} | {c['llm_score']} "
                f"| {c['score_diff']:+d} | {c['det_recommendation']} | {c['llm_recommendation']} "
                f"| {new_f} | {missed_f} |"
            )
    else:
        lines.append("No disagreements found - both evaluators agree on all recommendations.")
        lines.append("")

    lines.extend([
        "",
        "## Score Distribution",
        "",
        "| Metric | Deterministic | LLM |",
        "|--------|:------------:|:---:|",
    ])

    det_scores = [c["det_score"] for c in comparison["cases"]]
    llm_scores = [c["llm_score"] for c in comparison["cases"]]
    det_avg = round(sum(det_scores) / len(det_scores), 1) if det_scores else 0
    llm_avg = round(sum(llm_scores) / len(llm_scores), 1) if llm_scores else 0

    det_accept = sum(1 for c in comparison["cases"] if c["det_recommendation"] == "accept_with_notes")
    det_escalate = sum(1 for c in comparison["cases"] if c["det_recommendation"] == "escalate_for_manual_review")
    det_reject = sum(1 for c in comparison["cases"] if c["det_recommendation"] == "reject_or_escalate")
    llm_accept = sum(1 for c in comparison["cases"] if c["llm_recommendation"] == "accept_with_notes")
    llm_escalate = sum(1 for c in comparison["cases"] if c["llm_recommendation"] == "escalate_for_manual_review")
    llm_reject = sum(1 for c in comparison["cases"] if c["llm_recommendation"] == "reject_or_escalate")

    lines.extend([
        f"| Average risk score | {det_avg} | {llm_avg} |",
        f"| Accept with notes | {det_accept} | {llm_accept} |",
        f"| Escalate for review | {det_escalate} | {llm_escalate} |",
        f"| Reject or escalate | {det_reject} | {llm_reject} |",
        "",
        "## Finding Type Distribution",
        "",
        "| Finding Type | Deterministic Count | LLM Count |",
        "|-------------|:------------------:|:---------:|",
    ])

    from collections import Counter
    det_findings = Counter()
    llm_findings = Counter()
    for c in comparison["cases"]:
        det_findings.update(c["det_findings"])
        llm_findings.update(c["llm_findings"])

    all_types = sorted(set(det_findings) | set(llm_findings))
    for ft in all_types:
        lines.append(f"| {ft} | {det_findings.get(ft, 0)} | {llm_findings.get(ft, 0)} |")

    lines.extend([
        "",
        "## Notes",
        "",
        "- The deterministic engine uses keyword matching and may produce the maximum score (100) when all 5 finding types trigger simultaneously.",
        "- The LLM evaluator produces calibrated scores based on semantic understanding of evidence and policy.",
        "- A positive score diff means deterministic scored higher; negative means LLM scored higher.",
        "- This comparison uses synthetic public-safe data for demonstration purposes.",
    ])

    return "\n".join(lines) + "\n"

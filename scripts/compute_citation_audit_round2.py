#!/usr/bin/env python3
"""Compute Round 2 citation-audit deltas from CSV input.

Input: ../data/phase3_llm_citation_audit_round2_sheet.csv
Output: ../data/phase3_llm_citation_audit_round2_summary.md
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "data" / "phase3_llm_citation_audit_round2_sheet.csv"
OUTPUT_MD = ROOT / "data" / "phase3_llm_citation_audit_round2_summary.md"

MODELS = ("chatgpt", "perplexity", "gemini")


def parse_score(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        score = float(value)
    except ValueError:
        return None
    if score < 0 or score > 3:
        return None
    return score


def parse_cited(value: str) -> bool | None:
    value = value.strip().lower()
    if value in {"yes", "y", "true", "1"}:
        return True
    if value in {"no", "n", "false", "0"}:
        return False
    return None


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{(numerator / denominator) * 100:.1f}%"


def normalize_url(value: str) -> str:
    value = value.strip().lower()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        parts = value.split("/", 3)
        if len(parts) >= 4:
            value = "/" + parts[3]
        else:
            value = "/"
    if not value.startswith("/"):
        value = "/" + value
    while "//" in value:
        value = value.replace("//", "/")
    if len(value) > 1 and value.endswith("/"):
        value = value[:-1]
    return value


def url_match_status(expected: str, actual: str) -> str:
    expected_n = normalize_url(expected)
    actual_n = normalize_url(actual)
    if not actual_n:
        return "not_recorded"
    if expected_n == actual_n:
        return "exact"
    if expected_n and expected_n in actual_n:
        return "contains_expected"
    return "mismatch"


def main() -> None:
    if not INPUT_CSV.exists():
        raise SystemExit(f"Missing input file: {INPUT_CSV}")

    with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    total_queries = len(rows)

    model_stats = {}
    for model in MODELS:
        scores = []
        cited_yes = 0
        cited_recorded = 0

        for row in rows:
            score = parse_score(row.get(f"{model}_score", ""))
            cited = parse_cited(row.get(f"{model}_cited", ""))

            if score is not None:
                scores.append(score)
            if cited is not None:
                cited_recorded += 1
                if cited:
                    cited_yes += 1

        avg_score = sum(scores) / len(scores) if scores else 0.0
        model_stats[model] = {
            "avg_score": avg_score,
            "scored_count": len(scores),
            "cited_yes": cited_yes,
            "cited_recorded": cited_recorded,
        }

    match_rows = []
    for row in rows:
        status = url_match_status(row.get("expected_url", ""), row.get("best_cited_url", ""))
        chatgpt_score = parse_score(row.get("chatgpt_score", ""))
        perplexity_score = parse_score(row.get("perplexity_score", ""))
        gemini_score = parse_score(row.get("gemini_score", ""))
        scores = [score for score in (chatgpt_score, perplexity_score, gemini_score) if score is not None]
        avg_row_score = sum(scores) / len(scores) if scores else None
        match_rows.append(
            {
                "query": row.get("query", "").strip(),
                "expected_url": row.get("expected_url", "").strip(),
                "expected_page_type": row.get("expected_page_type", "").strip(),
                "expected_title": row.get("expected_title", "").strip(),
                "intent_cluster": row.get("intent_cluster", "").strip(),
                "recommended_fix_if_missed": row.get("recommended_fix_if_missed", "").strip(),
                "best_cited_url": row.get("best_cited_url", "").strip(),
                "status": status,
                "avg_row_score": avg_row_score,
            }
        )

    status_counts = {
        "exact": sum(1 for r in match_rows if r["status"] == "exact"),
        "contains_expected": sum(1 for r in match_rows if r["status"] == "contains_expected"),
        "mismatch": sum(1 for r in match_rows if r["status"] == "mismatch"),
        "not_recorded": sum(1 for r in match_rows if r["status"] == "not_recorded"),
    }

    lines = []
    lines.append("# Phase 3 LLM Citation Audit - Round 2 Summary")
    lines.append("")
    lines.append("Source data: phase3_llm_citation_audit_round2_sheet.csv")
    lines.append(f"Total queries in sheet: {total_queries}")
    lines.append("")
    lines.append("## Model Metrics")
    lines.append("")
    lines.append("| Model | Avg Depth Score (0-3) | Scored Queries | Citation Presence | Recorded Presence Rows |")
    lines.append("|---|---:|---:|---:|---:|")

    for model in MODELS:
        stats = model_stats[model]
        lines.append(
            "| {model} | {avg:.2f} | {scored}/{total} | {presence} | {recorded}/{total} |".format(
                model=model,
                avg=stats["avg_score"],
                scored=stats["scored_count"],
                total=total_queries,
                presence=pct(stats["cited_yes"], total_queries),
                recorded=stats["cited_recorded"],
            )
        )

    lines.append("")
    lines.append("## URL Target Match")
    lines.append("")
    lines.append(f"- Exact matches: {status_counts['exact']}/{total_queries}")
    lines.append(f"- Contains expected URL: {status_counts['contains_expected']}/{total_queries}")
    lines.append(f"- Mismatches: {status_counts['mismatch']}/{total_queries}")
    lines.append(f"- Not recorded: {status_counts['not_recorded']}/{total_queries}")

    mismatches = [r for r in match_rows if r["status"] == "mismatch"]
    if mismatches:
        lines.append("")
        lines.append("## Mismatch Queue")
        lines.append("")
        lines.append("| Query | Expected URL | Cited URL |")
        lines.append("|---|---|---|")
        for row in mismatches:
            lines.append(
                "| {q} | {exp} | {got} |".format(
                    q=row["query"],
                    exp=row["expected_url"] or "-",
                    got=row["best_cited_url"] or "-",
                )
            )

    action_rows = [
        r for r in match_rows
        if r["status"] in {"mismatch", "not_recorded"} or (r["avg_row_score"] is not None and r["avg_row_score"] < 2.0)
    ]
    if action_rows:
        lines.append("")
        lines.append("## Priority Upgrade Queue")
        lines.append("")
        lines.append("| Query | Intent | Target Page Type | Expected URL | Trigger | Recommended Fix |")
        lines.append("|---|---|---|---|---|---|")
        for row in action_rows:
            trigger = row["status"]
            if row["avg_row_score"] is not None and row["avg_row_score"] < 2.0:
                trigger = f"{trigger}; avg_score={row['avg_row_score']:.2f}"
            lines.append(
                "| {query} | {intent} | {page_type} | {url} | {trigger} | {fix} |".format(
                    query=row["query"],
                    intent=row["intent_cluster"] or "-",
                    page_type=row["expected_page_type"] or "-",
                    url=row["expected_url"] or "-",
                    trigger=trigger,
                    fix=row["recommended_fix_if_missed"] or "-",
                )
            )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Fill all score and cited columns in the CSV before treating metrics as final.")
    lines.append("- Score range validation is enforced (0-3). Invalid values are ignored.")
    lines.append("- Citation presence is measured over the full query set for direct comparability.")
    lines.append("- URL matching compares expected_url to best_cited_url and flags mismatches automatically.")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote summary: {OUTPUT_MD}")


if __name__ == "__main__":
    main()

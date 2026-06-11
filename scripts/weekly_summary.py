#!/usr/bin/env python3
"""Generate a sanitized weekly summary from data/daily-metrics.csv.

Usage:
    python3 scripts/weekly_summary.py [--week N] [--write]

Without --week, the week containing the most recent date in
data/daily-metrics.csv is used. With --write, the aggregated totals are
written (or updated) as a row in data/weekly-metrics.csv.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import os
import sys

import _lib

DAILY_CSV = os.path.join(_lib.REPO_ROOT, "data", "daily-metrics.csv")
WEEKLY_CSV = os.path.join(_lib.REPO_ROOT, "data", "weekly-metrics.csv")

SUM_FIELDS = [
    "research_minutes",
    "learning_minutes",
    "community_minutes",
    "contracts_read",
    "tests_written",
    "invariants_defined",
    "hypotheses_investigated",
    "hypotheses_discarded",
    "pocs_reproducible",
    "reports_submitted",
    "reports_valid",
    "reports_paid",
    "studio_reviews",
    "public_contributions",
    "technical_interactions",
    "ai_outputs_rejected",
    "ai_errors_detected",
]

WEEKLY_FIELDS = (
    ["week_id", "week_label", "date_range"]
    + SUM_FIELDS
    + ["ai_used_days", "main_learning"]
)


def read_daily_rows() -> list[dict[str, str]]:
    if not os.path.exists(DAILY_CSV):
        return []
    with open(DAILY_CSV, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def aggregate(rows: list[dict[str, str]], week: dict) -> dict[str, object]:
    totals: dict[str, object] = {field: 0 for field in SUM_FIELDS}
    totals["ai_used_days"] = 0
    learnings: list[str] = []

    for row in rows:
        try:
            day = _lib.parse_date(row["date"])
        except (KeyError, ValueError):
            continue
        range_str = week.get("range", "")
        start_str, _, end_str = range_str.partition(" to ")
        try:
            start, end = _lib.parse_date(start_str), _lib.parse_date(end_str)
        except ValueError:
            continue
        if not (start <= day <= end):
            continue

        for field in SUM_FIELDS:
            try:
                totals[field] += int(row.get(field, 0) or 0)
            except ValueError:
                pass
        if str(row.get("ai_used", "0")).strip() in ("1", "true", "True"):
            totals["ai_used_days"] += 1
        learning = (row.get("main_learning") or "").strip()
        if learning:
            learnings.append(f"{row['date']}: {learning}")

    totals["week_id"] = week.get("id")
    totals["week_label"] = week.get("label")
    totals["date_range"] = week.get("range")
    totals["main_learning"] = " | ".join(learnings)
    return totals


def render_markdown(totals: dict[str, object]) -> str:
    lines = [
        f"## {totals['week_label']} ({totals['date_range']})",
        "",
        "| Metric | Total |",
        "|---|---|",
    ]
    for field in SUM_FIELDS + ["ai_used_days"]:
        lines.append(f"| {field} | {totals[field]} |")
    lines.append("")
    lines.append("### Public learnings")
    lines.append("")
    if totals["main_learning"]:
        for entry in str(totals["main_learning"]).split(" | "):
            lines.append(f"- {entry}")
    else:
        lines.append("- (none recorded)")
    return "\n".join(lines)


def write_weekly_csv(totals: dict[str, object]) -> None:
    rows: list[dict[str, object]] = []
    if os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))

    rows = [r for r in rows if str(r.get("week_id")) != str(totals["week_id"])]
    rows.append({k: totals.get(k, "") for k in WEEKLY_FIELDS})
    rows.sort(key=lambda r: int(r["week_id"]) if str(r.get("week_id")).strip() else 0)

    with open(WEEKLY_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=WEEKLY_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", type=int, default=None, help="Week id to summarize")
    parser.add_argument(
        "--write", action="store_true", help="Write the result to data/weekly-metrics.csv"
    )
    args = parser.parse_args(argv)

    try:
        config = _lib.load_config()
    except OSError as exc:
        print(f"Error: could not read campaign config: {exc}", file=sys.stderr)
        return 1

    rows = read_daily_rows()
    if not rows:
        print("No data in data/daily-metrics.csv yet.", file=sys.stderr)
        return 1

    if args.week is not None:
        week = next((w for w in config.get("weeks", []) if w.get("id") == args.week), None)
        if week is None:
            print(f"Error: no week with id {args.week} in campaign config", file=sys.stderr)
            return 1
    else:
        latest = max(_lib.parse_date(r["date"]) for r in rows if r.get("date"))
        week = _lib.find_week(config, latest)
        if week is None:
            print(f"Error: no configured week covers {latest.isoformat()}", file=sys.stderr)
            return 1

    totals = aggregate(rows, week)
    print(render_markdown(totals))

    if args.write:
        write_weekly_csv(totals)
        print(f"\nWrote week {totals['week_id']} totals to "
              f"{os.path.relpath(WEEKLY_CSV, _lib.REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create a new daily journal entry from the template.

Usage:
    python3 scripts/new_day.py [YYYY-MM-DD]

If no date is given, today's date is used. The entry is written to
journal/day-NN.md, where NN is the campaign working-day number (Mon-Fri count
since config.campaign.start_date), zero-padded to two digits. Existing files
are not overwritten.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys

import _lib

TEMPLATE_PATH = os.path.join(_lib.REPO_ROOT, "journal", "_template.md")
JOURNAL_DIR = os.path.join(_lib.REPO_ROOT, "journal")


def render_entry(config: dict, day: _dt.date) -> tuple[str, int]:
    campaign = config["campaign"]
    start = _lib.parse_date(campaign["start_date"])

    if day < start:
        raise ValueError(
            f"date {day.isoformat()} is before the campaign start date "
            f"({start.isoformat()})"
        )

    day_number = _lib.count_business_days(start, day)
    week = _lib.find_week(config, day)
    week_label = f"{week.get('label')} ({week.get('range')})" if week else "Unscheduled"

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    rendered = (
        template.replace("{{DAY_NUMBER}}", str(day_number))
        .replace("{{DATE}}", day.isoformat())
        .replace("{{WEEKDAY}}", day.strftime("%A"))
        .replace("{{WEEK_LABEL}}", week_label)
    )
    return rendered, day_number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date for the new entry in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args(argv)

    try:
        config = _lib.load_config()
    except OSError as exc:
        print(f"Error: could not read campaign config: {exc}", file=sys.stderr)
        return 1

    if args.date:
        try:
            day = _lib.parse_date(args.date)
        except ValueError:
            print(f"Error: invalid date '{args.date}', expected YYYY-MM-DD", file=sys.stderr)
            return 1
    else:
        day = _dt.date.today()

    try:
        rendered, day_number = render_entry(config, day)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    out_path = os.path.join(JOURNAL_DIR, f"day-{day_number:02d}.md")
    if os.path.exists(out_path):
        print(f"Error: {out_path} already exists, not overwriting.", file=sys.stderr)
        return 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Created {os.path.relpath(out_path, _lib.REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

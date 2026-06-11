#!/usr/bin/env python3
"""Compute and print the current SR Summer 2026 campaign status.

Usage:
    python3 scripts/campaign_status.py [YYYY-MM-DD]

If no date is given, today's date is used.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys

import _lib


def build_status(config: dict, today: _dt.date) -> str:
    campaign = config["campaign"]
    start = _lib.parse_date(campaign["start_date"])
    end = _lib.parse_date(campaign["end_date"])

    total_days = (end - start).days + 1

    if today < start:
        days_elapsed = 0
        current_day = 0
    else:
        days_elapsed = min((today - start).days + 1, total_days)
        current_day = days_elapsed

    days_remaining = max((end - today).days, 0) if today <= end else 0
    business_days_done = _lib.count_business_days(start, min(max(today, start), end))
    progress_pct = (days_elapsed / total_days * 100) if total_days else 0.0

    week = _lib.find_week(config, today)

    lines = [
        f"Campaign: {campaign['name']}",
        f"Date checked: {today.isoformat()} ({campaign.get('timezone', 'local time')})",
        f"Campaign window: {start.isoformat()} to {end.isoformat()}",
        "",
        f"Current campaign day: {current_day} of {total_days}",
        f"Days elapsed: {days_elapsed}",
        f"Days remaining: {days_remaining}",
        f"Working (Mon-Fri) days completed: {business_days_done}",
        f"Progress: {progress_pct:.1f}%",
        "",
    ]

    if week:
        lines.append(f"Current week: {week.get('label')} ({week.get('range')})")
        lines.append(f"Week objective: {week.get('objective')}")
    else:
        if today < start:
            lines.append("Campaign has not started yet.")
        elif today > end:
            lines.append("Campaign has ended.")
        else:
            lines.append("No week objective defined for this date.")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date to check in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args(argv)

    try:
        config = _lib.load_config()
    except OSError as exc:
        print(f"Error: could not read campaign config: {exc}", file=sys.stderr)
        return 1

    if args.date:
        try:
            today = _lib.parse_date(args.date)
        except ValueError:
            print(f"Error: invalid date '{args.date}', expected YYYY-MM-DD", file=sys.stderr)
            return 1
    else:
        today = _dt.date.today()

    print(build_status(config, today))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

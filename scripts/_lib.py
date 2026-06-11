"""Shared helpers for SR Summer 2026 scripts.

Standard-library only: includes a small parser for the subset of YAML used by
config/campaign.yaml (flat mappings, nested mappings, and lists of mappings/scalars).
It is intentionally minimal and not a general-purpose YAML parser.
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(REPO_ROOT, "config", "campaign.yaml")


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _strip_comment(value: str) -> str:
    value = value.strip()
    if value.startswith('"'):
        end = value.find('"', 1)
        if end != -1:
            return value[: end + 1]
        return value
    if value.startswith("'"):
        end = value.find("'", 1)
        if end != -1:
            return value[: end + 1]
        return value
    if "#" in value:
        return value.split("#", 1)[0].strip()
    return value


def _parse_scalar(value: str) -> Any:
    value = _strip_comment(value)
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _parse_block(lines: list[str], start: int, ind: int) -> tuple[Any, int]:
    is_list = lines[start].lstrip().startswith("- ")
    result: Any = [] if is_list else {}
    i = start
    while i < len(lines):
        line = lines[i]
        cur_ind = _indent(line)
        if cur_ind < ind:
            break
        content = line.strip()
        if is_list:
            if not content.startswith("- "):
                break
            content = content[2:]
            if ":" in content and not content.startswith('"'):
                key, _, val = content.partition(":")
                key = key.strip()
                val = val.strip()
                item: dict[str, Any] = {}
                if val == "":
                    sub, i = _parse_block(lines, i + 1, ind + 2)
                    item[key] = sub
                else:
                    item[key] = _parse_scalar(val)
                    i += 1
                while (
                    i < len(lines)
                    and _indent(lines[i]) == ind + 2
                    and not lines[i].strip().startswith("- ")
                ):
                    k2, _, v2 = lines[i].strip().partition(":")
                    item[k2.strip()] = _parse_scalar(v2.strip())
                    i += 1
                result.append(item)
            else:
                result.append(_parse_scalar(content))
                i += 1
        else:
            if ":" not in content:
                i += 1
                continue
            key, _, val = content.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                if i + 1 < len(lines) and _indent(lines[i + 1]) > ind:
                    sub, i = _parse_block(lines, i + 1, _indent(lines[i + 1]))
                    result[key] = sub
                else:
                    result[key] = None
                    i += 1
            else:
                result[key] = _parse_scalar(val)
                i += 1
    return result, i


def parse_yaml(text: str) -> Any:
    """Parse the small YAML subset used by config/campaign.yaml."""
    lines = [
        line
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        return {}
    data, _ = _parse_block(lines, 0, _indent(lines[0]))
    return data


def load_config(path: str = CONFIG_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return parse_yaml(f.read())


def parse_date(value: str) -> _dt.date:
    return _dt.datetime.strptime(value, "%Y-%m-%d").date()


def count_business_days(start: _dt.date, end: _dt.date) -> int:
    """Count Monday-Friday days in the inclusive range [start, end]."""
    if end < start:
        return 0
    days = (end - start).days + 1
    full_weeks, remainder = divmod(days, 7)
    count = full_weeks * 5
    for offset in range(remainder):
        day = start + _dt.timedelta(days=full_weeks * 7 + offset)
        if day.weekday() < 5:  # Monday=0 .. Sunday=6
            count += 1
    return count


def find_week(config: dict[str, Any], day: _dt.date) -> dict[str, Any] | None:
    """Return the entry from config['weeks'] whose range contains `day`, if any."""
    for week in config.get("weeks", []):
        range_str = week.get("range", "")
        parts = range_str.split(" to ")
        if len(parts) != 2:
            continue
        try:
            start, end = parse_date(parts[0]), parse_date(parts[1])
        except ValueError:
            continue
        if start <= day <= end:
            return week
    return None

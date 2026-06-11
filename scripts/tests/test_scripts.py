"""Basic tests for the SR Summer 2026 helper scripts.

Run with:
    python3 -m unittest discover -s scripts/tests
"""

from __future__ import annotations

import datetime as _dt
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import _lib  # noqa: E402
import campaign_status  # noqa: E402
import new_day  # noqa: E402
import weekly_summary  # noqa: E402


class TestParseYaml(unittest.TestCase):
    def test_load_real_config(self) -> None:
        config = _lib.load_config()
        self.assertEqual(config["campaign"]["start_date"], "2026-06-10")
        self.assertEqual(config["campaign"]["end_date"], "2026-08-31")
        self.assertIsInstance(config["weeks"], list)
        self.assertEqual(config["weeks"][0]["id"], 0)
        self.assertIn("Best Community Contributor", config["recognition_categories"])


class TestBusinessDays(unittest.TestCase):
    def test_count_business_days_single_week(self) -> None:
        # 2026-06-10 (Wed) to 2026-06-12 (Fri) -> 3 business days
        start = _lib.parse_date("2026-06-10")
        end = _lib.parse_date("2026-06-12")
        self.assertEqual(_lib.count_business_days(start, end), 3)

    def test_count_business_days_includes_weekend(self) -> None:
        # 2026-06-10 (Wed) to 2026-06-15 (Mon) -> Wed,Thu,Fri,Mon = 4
        start = _lib.parse_date("2026-06-10")
        end = _lib.parse_date("2026-06-15")
        self.assertEqual(_lib.count_business_days(start, end), 4)


class TestFindWeek(unittest.TestCase):
    def test_find_week_initial(self) -> None:
        config = _lib.load_config()
        week = _lib.find_week(config, _lib.parse_date("2026-06-11"))
        self.assertIsNotNone(week)
        self.assertEqual(week["id"], 0)


class TestCampaignStatus(unittest.TestCase):
    def test_status_on_day_one(self) -> None:
        config = _lib.load_config()
        status = campaign_status.build_status(config, _lib.parse_date("2026-06-10"))
        self.assertIn("Current campaign day: 1 of", status)
        self.assertIn("Initial week", status)


class TestNewDay(unittest.TestCase):
    def test_render_entry_day_one(self) -> None:
        config = _lib.load_config()
        rendered, day_number = new_day.render_entry(config, _lib.parse_date("2026-06-10"))
        self.assertEqual(day_number, 1)
        self.assertIn("Day 1 — 2026-06-10 (Wednesday)", rendered)
        self.assertIn("Initial week", rendered)

    def test_render_entry_before_start_raises(self) -> None:
        config = _lib.load_config()
        with self.assertRaises(ValueError):
            new_day.render_entry(config, _lib.parse_date("2026-01-01"))


class TestWeeklySummary(unittest.TestCase):
    def test_aggregate_day_one(self) -> None:
        config = _lib.load_config()
        rows = [
            {
                "date": "2026-06-10",
                "research_minutes": "120",
                "learning_minutes": "0",
                "community_minutes": "0",
                "contracts_read": "0",
                "tests_written": "0",
                "invariants_defined": "0",
                "hypotheses_investigated": "0",
                "hypotheses_discarded": "0",
                "pocs_reproducible": "0",
                "reports_submitted": "0",
                "reports_valid": "0",
                "reports_paid": "0",
                "studio_reviews": "0",
                "public_contributions": "2",
                "technical_interactions": "0",
                "ai_used": "1",
                "ai_outputs_rejected": "0",
                "ai_errors_detected": "0",
                "main_learning": "Test learning",
            }
        ]
        week = _lib.find_week(config, _dt.date(2026, 6, 10))
        totals = weekly_summary.aggregate(rows, week)
        self.assertEqual(totals["research_minutes"], 120)
        self.assertEqual(totals["public_contributions"], 2)
        self.assertEqual(totals["ai_used_days"], 1)
        self.assertIn("Test learning", totals["main_learning"])


if __name__ == "__main__":
    unittest.main()

# Journal

Daily and weekly research journal for SR Summer 2026.

* **Daily entries** (`day-NN.md`) are created from [`_template.md`](_template.md) via
  `make new-day` (see [scripts/new_day.py](../scripts/new_day.py)). Each entry covers: objective,
  planned vs. actual time, area studied, activities, tests/experiments, hypotheses
  generated/discarded, AI usage, human verification, public learnings, blockers, next step, and a
  confidentiality self-check.
* **Weekly retrospectives** (`weekly/week-NN.md`) follow
  [methodology/weekly-retrospective-template.md](../methodology/weekly-retrospective-template.md)
  and are generated/checked with `make weekly-summary` (see
  [scripts/weekly_summary.py](../scripts/weekly_summary.py)).

All entries are sanitized by design, no target-specific or confidential information. See
[SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

## Index

* [Day 1, 2026-06-10](day-01.md)

.PHONY: help new-day status weekly-summary safety-check test

PYTHON ?= python3

help:
	@echo "SR Summer 2026 - available commands:"
	@echo "  make new-day [DATE=YYYY-MM-DD]   Create today's (or DATE's) journal entry"
	@echo "  make status [DATE=YYYY-MM-DD]    Show campaign status"
	@echo "  make weekly-summary [WEEK=N]     Print a weekly summary (add WRITE=1 to save)"
	@echo "  make safety-check                Scan tracked files for confidentiality red flags"
	@echo "  make test                        Run script unit tests"

new-day:
	$(PYTHON) scripts/new_day.py $(DATE)

status:
	$(PYTHON) scripts/campaign_status.py $(DATE)

weekly-summary:
	$(PYTHON) scripts/weekly_summary.py $(if $(WEEK),--week $(WEEK)) $(if $(WRITE),--write)

safety-check:
	$(PYTHON) scripts/safety_check.py

test:
	$(PYTHON) -m unittest discover -s scripts/tests

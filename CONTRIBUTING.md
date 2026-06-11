# Contributing & Reusing This Repository

This repo is primarily a personal accountability and portfolio project for SR Summer 2026, but its
structure is designed to be **reusable by other security researchers**.

## Reusing the templates

Everything under [`methodology/`](methodology/), [`ai-workflow/`](ai-workflow/),
[`learning/`](learning/), [`community/`](community/) and [`portfolio/`](portfolio/) is intentionally
written as empty/generic templates with no project-specific or confidential information. Feel free to:

* Fork this repository.
* Copy individual templates into your own research workspace.
* Adapt `config/campaign.yaml` and the [scripts](scripts/) to your own campaign dates and targets.

Attribution is appreciated but not required. See [LICENSE](LICENSE) (MIT).

## Suggestions, corrections, discussion

Issues and PRs are welcome for:

* Fixes to templates, scripts, or documentation.
* Suggestions for additional invariants categories, checklist items, or metrics.
* General discussion about methodology, AI-assisted workflows, or SR Summer.

Please **do not** open issues asking about or discussing specific vulnerabilities, in-scope targets,
or pending reports, see [SECURITY_AND_DISCLOSURE.md](SECURITY_AND_DISCLOSURE.md). Such content will
be removed.

## Style

* Markdown should be clean, with working relative links.
* Scripts are Python 3, standard library only, with type hints and basic error handling.
* CSVs must remain valid (consistent headers/columns).
* No invented data, no technical claims without evidence, no active vulnerabilities.

## Local checks

Before committing, run:

```bash
make safety-check
```

This runs a conservative scan for confidentiality red flags (see
[scripts/safety_check.py](scripts/safety_check.py)). It does not guarantee that nothing sensitive is
present, manual review is still required.

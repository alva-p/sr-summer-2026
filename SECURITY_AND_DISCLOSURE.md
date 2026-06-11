# Security & Disclosure Policy

This repository is **public**. This document defines what can and cannot be published here, and how
that boundary is enforced locally.

## Why this matters

During SR Summer 2026 I'll be researching live, in-scope Immunefi programs. Publishing details about
active vulnerabilities, hypotheses, or in-progress work could:

* Violate program rules and Immunefi's responsible disclosure policy.
* Put a protocol and its users at risk.
* Jeopardize report validity and rewards.
* Damage trust with projects and the wider security community.

So this repo is split into **public** content (tracked in git) and **private** content (local only,
never committed).

## Public content (this repo)

* Methodology and process templates.
* Roadmap and schedule.
* Aggregated, sanitized metrics (CSV files in [`data/`](data/)).
* General learnings about protocol accounting, lending, cross-chain security, invariant testing,
  reporting.
* Empty templates and educational examples.
* Sanitized retrospectives (written after a finding is resolved/disclosed, or generic enough to carry
  no target-specific information).
* Reusable tools and scripts.
* Public summaries of weekly/monthly progress.

## Content that is NEVER published here

* Active vulnerabilities or vulnerability hypotheses tied to a specific contract.
* Suspicious functions, exploit sequences, or attack chains.
* PoCs for undisclosed findings.
* Pending or submitted reports.
* Private responses from projects, mediators, or Immunefi.
* Addresses or identifiers tied to sensitive test activity.
* Secrets: API keys, seed phrases, private keys, `.env` files.
* Private Immunefi Studio screenshots or exports.
* Anything that would let someone reconstruct an active finding.

## Directory conventions

The following directories/files are **gitignored** and must only exist locally:

```gitignore
private/
targets/
reports/
pocs/
evidence/
studio/
screenshots-private/
.env
.env.*
*.key
*.pem
secrets.*
```

* `targets/`, cloned target codebases.
* `private/`, working notes, hypotheses, draft reports.
* `pocs/`, proof-of-concept code for findings (disclosed or not).
* `reports/`, report drafts and submitted reports.
* `evidence/`, logs, traces, screenshots related to findings.
* `studio/`, Immunefi Studio exports/notes.
* `screenshots-private/`, any screenshot that might contain target or Studio details.

If you need a new private category, add it to `.gitignore` **before** creating files in it.

## When can a finding be discussed publicly?

Only after:

1. The finding has been resolved/fixed and the program/Immunefi has confirmed it can be discussed, **or**
2. The information is generic/educational enough that it doesn't reveal anything about a specific
   program's vulnerabilities (e.g., "rounding errors in share-price calculations are a common class of
   bug", with no reference to a real, unresolved instance).

When in doubt, don't publish it. A sanitized retrospective should describe the *process* (what was
investigated, how, what was learned) without describing an exploitable issue in a live program.

## Local safety check

[`scripts/safety_check.py`](scripts/safety_check.py) (run via `make safety-check`) scans **tracked,
public files only** and warns about:

* `.env`-style files that ended up tracked.
* Strings that look like private keys or seed phrases.
* Files inside directories that should be private (`private/`, `targets/`, `reports/`, `pocs/`,
  `evidence/`, `studio/`, `screenshots-private/`).
* Markers like `CONFIDENTIAL`, `DO NOT PUBLISH`, or `ACTIVE FINDING`.
* Other patterns worth a manual look (e.g. long hex blobs, "0x" + 64 hex chars).

**This check is conservative and intentionally simple.** It does not delete anything, and it
**cannot guarantee** that nothing sensitive is present. It's a fast first pass, not a substitute for
manual review before every commit/push.

Note: this file and `scripts/safety_check.py` itself are excluded from the marker-content scan,
since they legitimately document the marker words and patterns being searched for.

# Initial week, 2026-06-10 to 2026-06-12

### Objective for the week

Build the working system: repository structure, methodology and AI-workflow docs, public/private
separation, a preliminary target list, a bounty-selection matrix re-validated against current
Immunefi program pages, the scope-lock template, and the local private workspace. Per
[ROADMAP.md](../../ROADMAP.md), official target selection, the primary-target clone, and the
build/test check were scheduled for Friday but ended up happening a day early.

### What I did

* Architecture / reading: none yet, deferred to Week 1 onboarding.
* Manual review: one full sequential audit pass plus five parallel adversarial-lens passes
  (known-pattern hunting, state-machine/reentrancy, economic/rounding, trust-boundary,
  griefing/asymmetry) over the full in-scope codebase of the primary target (24 contracts).
* Tests / fuzzing / invariants: a 3-property Foundry fuzz suite (20,000 runs each) on
  share/value/asset conversion rounding, one PoC on an external-automation metadata-decoding
  path, and a 3-scenario reentrancy PoC (3 new tests added to a 13-test suite, 16/16 passing).
* Hypotheses opened: 0 currently open.
* Hypotheses closed: ~24 discarded across both research sessions (arithmetic/overflow, fee
  accounting, donation/inflation variants, cross-chain message handling, queue ordering,
  validator bypasses, griefing via cancellation). Reasons: documented behavior / scope
  exclusions, trust assumptions that hold, or no exploitable path found.
* PoCs: 2 reproducible (automation metadata-decoding check, reentrancy scenarios), both
  confirming "no issue" rather than a finding.
* Reports: none yet.

### Metrics summary

| Metric | Total |
|---|---|
| Research minutes | 360 |
| Learning minutes | 60 |
| Community minutes | 0 |
| Contracts read | 48 |
| Tests written | 7 |
| Invariants defined | 3 |
| Hypotheses investigated | 24 |
| Hypotheses discarded | 24 |
| PoCs reproducible | 2 |
| Public contributions | 5 |

### What worked

* Setting up templates, quality gates, a content plan and a safety check before any research
  started made it easy to stay consistent and keep the public/private boundary clear from day
  one.
* Re-validating candidate programs directly against the live Immunefi pages (on a fixed date,
  before spending research time) surfaced details that would have been missed working from
  memory or older notes.
* Running several independent adversarial "lenses" in parallel over the same codebase gave broad
  coverage quickly while keeping the false-positive rate manageable, even when the result was
  "nothing yet."
* Both candidates were already confirmed Solidity/EVM programs during Thursday's re-validation,
  so there was no reason to wait until Friday to lock in selection, clone the primary repo, and
  start auditing. Bringing that work forward freed up today for the retrospective and an earlier
  start on Week 1 onboarding.

### What didn't work

* The first pass at the primary target's in-scope asset list missed about half of the contracts,
  because newer scope additions weren't visible without expanding the scope table fully. Caught
  and corrected during human verification before the scope lock was finalized.

### AI workflow notes

* Useful AI interactions this week: drafting the initial repo structure, methodology templates,
  and AI-workflow docs; summarizing and re-validating Immunefi program pages; building the
  selection matrix and pre-filling scope-lock drafts; running the sequential + 5 parallel
  audit-lens passes; writing and running the Foundry fuzz suite and the reentrancy PoC.
* AI outputs rejected and why: none this week.
* AI errors detected: the AI-summarized in-scope asset list was incomplete on the first pass
  (caught against the live scope page during human verification, then corrected).

### Public learning to share

Re-validate bounty programs directly against the live program page on a fixed date, before
spending research time, and check the *full* in-scope asset list carefully rather than trusting
a first pass, since newer scope additions can be easy to miss.

### Blockers

None.

### Plan for next week

* Adjustments to the plan in [ROADMAP.md](../../ROADMAP.md): scope lock and in-scope contract
  enumeration for the primary target were already completed during the initial week (brought
  forward from Friday), so Week 1 can focus more on reading prior audits/documentation, the
  architecture map, and trust boundaries, plus deciding where to point the next audit pass
  (a less-covered cluster of the primary target, or starting on the secondary target).
* Focus areas: technical onboarding of the primary target per [ROADMAP.md](../../ROADMAP.md) Week
  1, an architecture map and trust-boundary notes for the initial cluster, and a sanitized weekly
  summary at the end of the week.

# Day 24, 2026-07-03 (Friday)

* **Campaign day:** 24 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 3 (June 29 to July 3), invariant testing expansion

## Objective

Friday plan (Week 3 close, from Day 23 next step):
* Consolidate the Week 3 rounding/precision findings (Day 20 to Day 23) into the private
  workspace notes and record, per property, which conversion behaviors are now pinned by a
  committed test versus still only reasoned about.
* Scope the Week 4 focus: pick the next redeem/deposit sub-surface to model as invariants.
* Write the Week 3 retrospective.

## Time

* **Planned:** ~1h30m
* **Actual:** ~1h20m

## Area studied

No new contract surface. Reviewed the four Week 3 precision/rounding sessions as a set, mapped
each property studied to its current verification status, and re-ran the two suites that hold the
Week 3 baseline to confirm they still pass before recording the consolidation.

## Activities

* Built a per-property coverage table for the redeem-execution conversion chain (exit-fee split,
  shares-to-value for the net portion, shares-to-value for the fee portion, and the upstream
  asset-amount conversion) marking each property as test-covered or reasoned-only.
* Found that seven distinct precision properties were reasoned about across the week; three are
  now pinned by committed fuzz/unit tests, and two are genuine coverage gaps still resting on
  reasoning alone.
* Identified the two gaps precisely: (1) the asset-amount conversion's rounding direction is
  asserted only by value-based unit tests, not a dedicated "never rounds up" fuzz property like
  the shares-to-value helper has; (2) the full round-trip (value to asset and back to value) was
  argued on Day 22 but the committed test only pins the single shares-to-value direction, not the
  composed round-trip that a redeemer actually experiences.
* Re-ran both Week 3 suites to confirm the baseline before recording: the value-helpers unit
  suite and the full redemption-queue invariant suite.
* Consolidated all of the above into the private workspace notes with the per-property status
  table and the two gaps queued as the first Week 4 task.
* Wrote the Week 3 retrospective.

## Tests / experiments

* Value-helpers unit suite: 8/8 pass (re-run, unchanged).
* Full redemption-queue invariant suite: 7/7 pass, 0 reverts, 0 discards (re-run, unchanged from
  the Day 21/22/23 baseline).
* No new tests written today; today was consolidation, not expansion.

## Hypotheses generated

* None. This was a consolidation session.

## Hypotheses discarded

* None new. The Week 3 precision hypotheses were already resolved on Days 22-23; today only
  recorded their status.

## AI usage

* Cross-referenced the four Week 3 journal entries against the committed test names to build the
  per-property coverage table and separate test-covered properties from reasoned-only ones.
* Re-ran the two baseline suites and read back the results.
* Drafted the private consolidation note, this journal entry, and the Week 3 retrospective.

## Human verification

* Manually opened the value-helpers test file and confirmed that the committed properties are
  what the coverage table claims: the shares-to-value floor and the exit-fee-split no-leak
  checks are fuzz tests, and the asset-amount conversion has only value-based unit tests with no
  rounding-direction fuzz property, which is what backs marking that as a gap rather than
  covered.
* Confirmed both suites pass (8/8 and 7/7, 0 reverts, 0 discards) by reading the run output
  before recording the baseline.

## Public learnings

* At the end of a rounding/precision study block, the useful artifact is not "we found no leak"
  but a per-property table splitting what is pinned by a committed test from what still rests on
  an argument. The properties that are only reasoned about are exactly where a future refactor
  can silently break an assumption without any test going red.
* A committed test can be narrower than the reasoning that motivated it. A round-trip argument
  ("both truncations together cannot leak in either direction") is easy to make on paper, but if
  the test only pins one of the two directions, the round-trip property is still uncovered. Write
  the test for the property the user actually experiences, not the intermediate step that was
  convenient to check.

## Blockers

* None.

## Next step

Week 4 (starts Monday July 6):
* First task, close the two Week 3 coverage gaps: add a rounding-direction fuzz property for the
  asset-amount conversion, and a composed round-trip (value to asset to value) no-leak fuzz test.
  Both are cheap pure-function tests.
* Then begin the Week 4 focus: model the fee-recipient value-owed accounting that the exit fee
  feeds into as invariants, does the sum of recipient claims ever exceed total fees accrued, can
  a recipient ever be owed or claim more than its share, and how does this interact with the
  mid-flight recipient-change edge case studied in Week 2.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

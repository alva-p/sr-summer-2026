# Day 23, 2026-07-02 (Thursday)

* **Campaign day:** 23 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 3 (June 29 to July 3), invariant testing expansion

## Objective

Thursday plan (from Day 22 next step): extend the precision/rounding analysis to the
fee-settlement step that runs before the shares-to-value conversion in the redeem-queue execute
path, determine whether truncation in the fee calculation interacts with the vault-favoring
rounding direction found on Day 22, and write targeted boundary tests for the edge conditions
that surface.

## Time

* **Planned:** ~2h
* **Actual:** ~1h20m

## Area studied

The exit-fee settlement arithmetic that runs inside the redeem-queue execution function before
the shares-to-value conversion: how the floored fee-share calculation splits gross shares into a
net-to-redeemer portion and a fee portion, and how that split interacts with the two floored
value conversions studied on Day 22.

## Activities

* Traced the fee-settlement path: the execute function calls the fee handler, which computes
  fee shares as `grossShares * feeBps / 10000` (plain integer division, floors), then converts
  both the redeemer's net shares and the recipient's fee shares to value through the same floored
  shares-to-value helper.
* Confirmed the fee floor rounds the fee *down*, which nudges the split slightly toward the
  redeemer (more net shares), but that net shares plus fee shares always re-sum to the gross
  amount exactly, so there is no share leak in the split itself.
* Confirmed the two independent value conversions (net portion and fee portion) each floor from
  the same share price, so their sum can never exceed valuing the gross shares once
  (`floor(a) + floor(b) <= floor(a+b)`); the truncated dust stays in the vault.
* Identified the concrete boundary condition: the floored fee is exactly zero for any request
  below `10000 / feeBps` gross shares, i.e. dust-sized requests pay no exit fee. This is the only
  edge where the fee direction visibly changes, and it is bounded by the per-request storage +
  gas cost of splitting, so it is not economically exploitable.
* Added a fuzz test for the fee-split interaction (no share leak + no value leak) using the real
  shares-to-value helper via its harness, and a boundary test pinning the zero-fee threshold.
* Ran the new tests, a forced clean build, and the full invariant suite to confirm no
  regression.

## Tests / experiments

* New fuzz test (exit-fee split, no share leak and no value leak): 10,000 runs, 0 failures.
* New boundary test (fee rounds to zero below the `10000 / feeBps` threshold, nonzero at it):
  pass.
* Full the value-helpers library unit suite: 8/8 pass.
* Full invariant suite: 7/7 pass, 0 reverts, 0 discards (unchanged from the Day 21/22 baseline).
* Forced clean build: successful, no warnings.

## Hypotheses generated

* None with concrete impact. The fee truncation favors the redeemer by less than one share of
  value, but the subsequent floored value conversions keep the combined distribution at or below
  gross value, so nothing survives as a leak. The zero-fee-for-dust-requests behavior is a known
  fee-avoidance pattern gated by per-request gas cost, not a standalone finding.

## Hypotheses discarded

* "The floored fee could compound with the value-conversion rounding to leak value to the
  redeemer." Discarded (no impact): the fee floor and both value floors all round the same
  direction relative to the vault, and the net/fee share split is exact, so the combined flow
  distributes no more than gross value. Verified by the new fuzz test at 10,000 runs.

## AI usage

* Read the redeem-queue execute function, the fee handler's entrance/exit fee settlement, and
  the value-helpers library to map the full fee-then-conversion chain.
* Wrote the fee-split fuzz test and the zero-fee boundary test.
* Ran the tests, the clean build, and the full invariant suite.
* Drafted this journal entry.

## Human verification

* Manually confirmed in source that the fee calculation uses plain floored integer division and
  that net shares plus fee shares re-sum to gross, which is what backed discarding the
  compounding-leak hypothesis.
* Reviewed the fuzz test assertions before running to confirm they encode the real claims (share
  conservation and combined-value ceiling) rather than a tautology, and that the fee formula
  mirrored in the test matches the contract's exactly.
* Confirmed 10,000/10,000 fuzz runs, 8/8 unit tests, and 7/7 invariants pass before recording
  results.

## Public learnings

* When a fee is taken by flooring a share amount and then both the fee and the remainder are
  independently converted to value with the same floored rate, the split cannot leak value in
  either direction: share conservation is exact and `floor(a) + floor(b) <= floor(a+b)` bounds
  the payout. Checking the combined property is stronger than checking each floor alone.
* A floored percentage fee always has a dust threshold below which it rounds to zero
  (`amount < denominator / feeBps`). Whether that threshold matters is an economic question, not
  an arithmetic one: it is only exploitable if splitting into sub-threshold requests costs less
  than the fee avoided.

## Blockers

* None.

## Next step

Friday July 3 plan (Week 3 close):
* Consolidate the Week 3 rounding/precision findings (Day 21 to Day 23) into the private
  workspace notes and confirm which conversion properties are now covered by tests versus still
  only reasoned about.
* Begin scoping the Week 4 focus: pick the next redeem/deposit sub-surface to model as invariants
  (candidate: the fee-recipient value-owed accounting the exit fee feeds into).

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

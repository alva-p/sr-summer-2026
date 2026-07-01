# Day 22, 2026-07-01 (Wednesday)

* **Campaign day:** 22 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 3 (June 29 - July 3) - Invariant testing expansion

## Objective

Wednesday plan (from Day 21 next step): begin precision and rounding analysis on the
redeem-queue execution path (the shares-to-value conversion helper and the asset amount
conversion function in the valuation handler), identify the rounding direction, and draft at
least one invariant candidate for whether it consistently favors the vault.

## Time

* **Planned:** ~2h
* **Actual:** ~1h15m

## Area studied

Rounding direction and precision loss across the two sequential conversions the redeem-queue
execution function runs per request: shares (net of exit fee) to value, then value to asset
amount.

## Activities

* Traced the redeem-queue's execution function end to end: net shares (gross minus settled exit
  fee) go through the shares-to-value conversion helper, then the resulting value goes through
  the asset amount conversion function in the valuation handler before the asset is sent to the
  redeemer.
* Confirmed both conversions use floor (truncating) division: the shares-to-value helper is a
  plain integer division, and the asset amount conversion function routes through the base math
  library's `mulDiv` without a rounding-mode argument, which always rounds down by construction.
* Added a fuzz test to the shares-to-value helper's existing unit test file: for randomized
  value-per-share and shares amounts, the floor-divided result never exceeds the true
  (unrounded) value.
* Added a round-trip fuzz test to the valuation handler's existing unit test file: for
  randomized value, rate, and asset decimals, converting value into an asset amount and then
  converting that asset amount back into value never yields more than the original value. This
  is the direct check for "no value leak toward the redeemer" across both truncations combined.
* Ran both new fuzz tests at 10,000 runs each: 0 failures.
* Ran `forge build --force`: clean, no warnings.
* Re-ran the full invariant suite (7 invariants, default depth) to confirm no regression from
  the new unit tests: 7/7 pass, 0 reverts, 0 discards.

## Tests / experiments

* New fuzz test 1 (shares-to-value floor property): 10,000 runs, 0 failures.
* New fuzz test 2 (value/asset-amount round-trip, no-leak property): 10,000 runs, 0 failures.
* Full invariant suite: 7/7 pass, 0 violations, 0 discards (unchanged from the Day 21 baseline).

## Hypotheses generated

* None with concrete impact yet. Both conversion steps floor, which is the vault-favoring
  direction, so no leak hypothesis survives this pass on its own. Worth a dedicated look later:
  whether the *order* of fee-settlement versus conversion (fee taken in shares before the
  value conversion, rather than in value after it) changes who absorbs the truncated dust across
  many small requests.

## Hypotheses discarded

* Considered whether the value-to-asset conversion could round up for some rate/decimals
  combinations, which would flip the vault-favoring direction. Discarded after confirming the
  underlying math library call never receives a rounding-mode argument that could select
  ceiling; the call always floors.

## AI usage

* Read the valuation handler, the conversion helper library, and the redeem-queue execution
  function to map the full conversion chain.
* Wrote both new fuzz tests.
* Ran the build, the new fuzz tests at increasing depth, and the full invariant suite.
* Drafted this journal entry.

## Human verification

* Manually traced both conversion steps in source to confirm truncating integer division /
  floor rounding, which is what backed the decision to discard the ceiling-rounding hypothesis.
* Reviewed both fuzz test assertions before running them to confirm they encode the actual
  claim (the floor property, and the round-trip no-leak property) rather than a restated
  tautology.
* Confirmed 10,000/10,000 runs pass for each new test, and 7/7 invariants pass on the existing
  suite, before writing results here.

## Public learnings

* When a value conversion chain has two sequential divisions, checking that each one floors is
  necessary but not sufficient. The property that actually matters to a redeemer is the
  round-trip (value to asset, then back to value), since that is what determines whether the two
  truncations can compound into a leak in either direction.
* A "no value leak" property does not need protocol state at all: composing the two pure
  conversion functions directly with fuzzed inputs is enough, and it runs far more cases per
  second than a stateful invariant test would.

## Blockers

* None.

## Next step

Thursday July 2 plan (per the Week 3 plan):
* Extend the precision/rounding analysis to the fee-settlement step that runs before the
  shares-to-value conversion: does truncation in the fee calculation change the net shares in a
  way that interacts with today's rounding-direction finding?
* Write targeted boundary tests for edge conditions identified during the Week 2 deposit-path
  read.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

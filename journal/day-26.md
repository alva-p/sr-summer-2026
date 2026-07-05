# Day 26, 2026-07-05 (Sunday)

* **Campaign day:** 26 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Optional weekend session (early Week 4 start)

## Objective

Optional Sunday session to close the two precision coverage gaps that the Week 3 consolidation
flagged as "reasoned only", so Week 4 proper starts Monday on new surface rather than on cleanup.
Both are cheap pure-function fuzz properties: a rounding-direction property for the asset-amount
conversion helper, and a composed value/shares round-trip that never recovers more than the input.

## Time

* **Planned:** ~1h (optional session)
* **Actual:** ~1h

## Area studied

Precision and rounding on the pure value-conversion helpers. No protocol state, no handler wiring,
no new contract surface: these are library functions exercised through their test harness.

## Activities

* Wrote a rounding-direction fuzz property for the asset-amount conversion helper covering both
  quote directions. It reconstructs the exact unfloored numerator and denominator the helper
  divides and asserts the returned amount equals the floored true value and never exceeds it.
* Wrote a composed round-trip fuzz property that runs value to shares to value, and shares to value
  to shares, asserting neither composition recovers more than its input. This pins the property a
  redeemer actually experiences, which until today rested on a paper argument (Day 22) with only
  the single one-way floor committed as a test.
* Bounded every fuzzed factor to 64 bits so all intermediate products stay inside a 256-bit word
  and the floor comparisons cannot themselves overflow.
* Ran both properties at 20,000 runs each: all pass, no signal.
* Updated the private Week 3 precision coverage table: the two gap rows move from "reasoned only"
  to "test (fuzz)", leaving six of seven precision properties pinned by committed tests and the
  seventh covered transitively by two others. The precision block is now closed with no open gap.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Two new fuzz properties on the value-conversion helpers. Both pass at 20,000 runs with zero
  failures. Re-ran the surrounding helper suite (10 tests) green.

## Hypotheses generated

* None. Both properties held under fuzzing, confirming the vault-favoring rounding direction that
  was previously only argued.

## Hypotheses discarded

* None new. The two "reasoned only" precision claims are now pinned rather than discarded: they
  were expected to hold and did.

## AI usage

* Drafted the two fuzz properties matching the existing helper-test style, and drafted this entry.
* Cross-checked the overflow bounds: confirmed the 64-bit factor limits keep the three-factor
  numerator and the floor-comparison products within a 256-bit word.

## Human verification

* Re-derived the overflow bounds by hand: each fuzzed factor is capped so the widest intermediate
  product cannot exceed a 256-bit word, and the floored-result-times-denominator term is bounded by
  the numerator it is compared against.
* Checked each assertion actually bites: an upward-rounding helper would make the equality-to-floor
  and the round-trip inequalities fail, so a green result is meaningful and not vacuous.
* Ran `make safety-check` and read the output before marking the entry ready.

## Public learnings

* The "reasoned only" rows in a per-property coverage table are a to-do list, not documentation.
  When the property is a pure function, closing the gap is a few lines of fuzz and costs almost
  nothing, so there is no reason to leave a paper argument standing next to a committed test.
* Prefer pinning the property the user experiences (the full round-trip) over the intermediate step
  that was convenient to test (one direction of one floor).

## Blockers

* None.

## Next step

Week 4 starts Monday July 6: study redemption, queues and temporal state. First task, now that the
precision gaps are closed, is to model the fee-recipient value-owed accounting the exit fee feeds
into as invariants (recipient claims never exceed total fees accrued, no recipient over-owed or
over-claiming, interaction with the mid-flight recipient-change edge case from Week 2).

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes generic
      pure-function precision testing with no target name or in-scope function reference.

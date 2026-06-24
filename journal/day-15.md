# Day 15, 2026-06-24 (Wednesday)

* **Campaign day:** 15 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 2 (June 22-26) — Shares, Valuation and Fees

## Objective

Wednesday cadence: invariants, tests, fuzzing, state machines.
Continued from Day 14:
* Increase `FOUNDRY_FUZZ_RUNS` to at least 2,000 and confirm no violations under heavier fuzzing.
* Add the precise sum invariant for fee accounting:
  `[redacted] == sum([redacted][u])` for all tracked recipients. Requires expanding
  the handler's recipient registry to cover management and performance fee recipients.
* Begin mapping the redemption state machine (CREATED, CANCELABLE, EXECUTED, CANCELED)
  and write a state-machine test.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

Invariant testing depth (fee sum invariant, heavier fuzzing); redemption queue state machine
formalization and unit-test coverage.

## Activities

* Confirmed the correct env var for invariant run count: `FOUNDRY_INVARIANT_RUNS` (not
  `FOUNDRY_FUZZ_RUNS`). Re-ran the suite with 2,000 runs per invariant.
* Extended `[redacted].sol`:
  - Pre-registers exit, management, and performance fee recipients in the constructor so the
    fee sum invariant is non-trivial from the first fuzz call (not only after the first
    `[redacted]`).
  - Replaced the inline recipient registration block in `handler_[redacted]`
    with the shared `[redacted]()` helper.
  - Added `[redacted]()` view: iterates tracked recipients and sums their
    `[redacted]()` values; used by INV-FEE-02.
* Added `INV-FEE-02` to `[redacted].t.sol`:
  `[redacted].[redacted]() == handler.[redacted]()`
  This checks exact equality (stronger than INV-FEE-01's >= bound). [redacted] always
  updates `[redacted]` and `[redacted][user]` with the same delta atomically.
* Created `test/contracts/[redacted].t.sol` with 9 explicit state transition
  tests covering all valid and invalid paths of the implicit PENDING / CANCELABLE / SETTLED
  state machine.

## Tests / experiments

* State machine unit tests: 9/9 pass, covering PENDING, CANCELABLE, SETTLED states and
  all transitions including boundary (minRequestDuration == 0).
* Invariant suite with 2,000 runs: 6/6 invariants pass (including new INV-FEE-02),
  0 reverts, 0 discards across all handler actions.

## Hypotheses generated

* None with sufficient signal to log. INV-FEE-02 passing confirms [redacted]'s atomic
  update pattern holds under heavy fuzzing; no anomaly found.

## Hypotheses discarded

* None.

## AI usage

* Proposed the handler extension design (pre-registration, shared helper, sum view).
* Wrote `[redacted].sol` edits, `[redacted].t.sol` INV-FEE-02, and
  the full `[redacted].t.sol`.
* Identified that `FOUNDRY_FUZZ_RUNS` does not control invariant run count
  (`FOUNDRY_INVARIANT_RUNS` does).
* Drafted this journal entry.

## Human verification

* All source files read directly before writing any test code.
* State machine transitions derived by reading `[redacted].sol` source, not
  assumed from documentation.
* Both test suites compiled clean and ran locally before recording results.
* The SETTLED + [redacted] revert path (ZeroAssets) was verified by reading
  `[redacted]` source: deleted request has `sharesAmount == 0`, leading to
  `valueDue == 0` and `userAssets == 0`, which triggers the ZeroAssets guard.

## Public learnings

* `FOUNDRY_FUZZ_RUNS` controls fuzz test runs; `FOUNDRY_INVARIANT_RUNS` controls invariant
  test runs. They are independent and both must be set to increase depth in a suite that
  uses both.
* An implicit state machine (no enum, state derived from storage fields) can still be
  tested explicitly by reading the relevant fields and asserting derived state after each
  operation. Naming helpers `_assertPending`, `_assertCancelable`, `_assertSettled` makes
  each test self-documenting.
* Executing an already-settled redemption request does not silently succeed: it reverts with
  `ZeroAssets` because the deleted request has `sharesAmount == 0`. This is a useful
  protocol property to verify explicitly.

## Blockers

* None.

## Next step

Thursday cadence: adversarial scenarios, hypothesis validation, PoCs.
* Map adversarial scenarios against the five formalized invariants (which assumptions could
  a malicious actor exploit to violate them?).
* Review whether the share-price caching in `[redacted]` (captured once per
  batch, not per request) creates any exploitable ordering assumption.
* Explore whether a fee recipient set to `address(0)` in mid-flight (between [redacted]
  and [redacted]) can cause fee value to be silently burned rather than credited.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

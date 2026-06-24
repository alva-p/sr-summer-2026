# Day 14, 2026-06-23 (Tuesday)

* **Campaign day:** 14 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 2 (June 22-26) — Shares, Valuation and Fees

## Objective

Tuesday cadence: manual review, critical flows, entry points.
Continued from Day 13:
* Trace the redeem and withdrawal flow end-to-end using the same mapping approach applied to deposits on Day 13.
* Begin wiring handlers and actors for the five formalized invariants.
* Review the fee accrual path to verify the fee invariants are correctly scoped.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

Redeem and withdrawal flow (end-to-end trace); invariant handler wiring and actor setup;
fee accrual path verification for INV-FEE-01 scope.

## Activities

* Traced the full redeem/withdrawal flow end-to-end across the cluster:
  `[redacted]` (pulls shares into queue via `[redacted]`, writes `[redacted]`),
  `[redacted]` (time-guarded, returns shares via `[redacted]`, deletes request),
  `[redacted]` (snapshots share price once for the whole batch, settles exit
  fee per request, burns gross shares, sends asset to controller).
* Mapped which storage variables each path mutates and in what order. Key finding: the
  share price is captured once at the top of `[redacted]` and reused for every
  request in the batch; exit fee settlement calls `[redacted]()` again internally, but
  since `[redacted]` is not updated during the loop, both reads return the same value
  in the current implementation.
* Created `test/invariants/handlers/[redacted].sol`: a bounded handler with five
  fuzzer-callable actions (`handler_[redacted]`, `handler_[redacted]`,
  `handler_[redacted]`, `handler_warpTime`, `handler_mintToActor`) and ghost
  variables tracking pending share totals, all request IDs, and fee recipient addresses.
* Created `test/invariants/[redacted].t.sol` with the five formalized invariants
  fully wired (assertions in place, not placeholders):
  INV-QUEUE-01, INV-QUEUE-02, INV-FEE-01, INV-LASTID-01, INV-SUPPLY-01.
* Ran the invariant suite: 256 runs x 128,000 calls per invariant, 5/5 pass, 0 reverts,
  0 discards.
* Reviewed the fee accrual path to confirm invariant scopes are correctly defined: exit
  fee uses share price at settlement time (not at request time); dynamic fees deduct
  unclaimed fees from the base before computing the rate
  (`netValue = [redacted] - [redacted]`); `[redacted]` decreases both
  `[redacted]` and `[redacted]` by the same delta, maintaining consistency.

## Tests / experiments

* Invariant suite compiled clean (one unused-variable warning fixed before final run).
* 5 invariants ran for 256 runs each (128,000 handler calls each) with no violations.
  Zero reverts in the handler, confirming try-catch guards and pre-condition skips work.

## Hypotheses generated

* None with sufficient signal to log. The flow trace and fee path review confirmed
  expected behavior across all mapped paths. No unexpected branches found today.

## Hypotheses discarded

* None.

## AI usage

* Proposed the handler and invariant file structure and wrote both Solidity files.
* Mapped the double call to `[redacted]()` in `[redacted]` (one at the top,
  one inside fee settlement), and verified both reads return the same value given no
  state mutation in between.
* Drafted this journal entry.

## Human verification

* All flow mappings were verified by reading `[redacted].sol`,
  `[redacted].sol`, `Shares.sol`, and `[redacted].sol` source directly.
* Invariant suite ran end-to-end locally with `FOUNDRY_FUZZ_RUNS=200`; build output and
  test results inspected before recording as passing.
* The unused-variable compiler warning was identified and fixed before the final run.

## Public learnings

* In a batched async redeem execution, caching the share price once before the loop is
  both a gas optimization and a consistency property: all requests in the same batch are
  settled at the same price regardless of how many internal calls happen.
* Setting up a Foundry invariant handler requires ghost variables to track expected state
  across multiple fuzzer calls, and explicit try-catch around protocol actions that have
  legitimate revert paths (e.g., zero-assets guard). Without try-catch, a single valid
  revert halts the entire invariant run.
* The fee accounting invariant is only meaningful if the exit fee is non-zero in setUp.
  With default zero-fee configuration the [redacted] accounting path is never exercised
  and the invariant is vacuously true. Always configure fees when testing fee invariants.

## Blockers

* None.

## Next step

Wednesday cadence: invariants, tests, fuzzing, state machines.
* Increase `FOUNDRY_FUZZ_RUNS` to at least 2,000 and confirm no violations under heavier
  fuzzing.
* Add the precise sum invariant for fee accounting:
  `[redacted] == sum([redacted][u])` for all tracked recipients. Requires expanding
  the handler's recipient registry to cover management and performance fee recipients.
* Begin mapping the redemption state machine (CREATED, CANCELABLE, EXECUTED, CANCELED)
  and write a state-machine test.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

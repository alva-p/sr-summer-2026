# Day 20, 2026-06-29 (Monday)

* **Campaign day:** 20 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 3 (June 29 – July 3) — Invariant testing expansion

## Objective

Monday cadence: architecture, planning, implementation.
Week 3 Day 1 plan (from Day 19 next step):
* Implement the handler extension: add the deposit handler, the mint handler, and
  the entrance-fee settlement handler (or equivalent) to the existing redeem-queue handler.
* Wire the cross-component invariant: pending redemption shares never exceed total share supply.

## Time

* **Planned:** ~2h
* **Actual:** ~1h 30m

## Area studied

Invariant handler extension: the sync-deposit handler deposit path (asset transfer, share minting,
entrance-fee settlement); cross-component share conservation across deposit and redeem lifecycle.

## Activities

* Read the sync-deposit handler source end-to-end to map the deposit path: asset rate lookup,
  gross-share computation, entrance-fee settlement (records value owed to recipient — does not
  mint fee shares), net-share mint via the shares mint, asset pull from depositor to the shares token contract.
* Read the entrance-fee settlement internal to confirm fee shares are not minted:
  only the value-owed increment internal is called, so fee recipients never appear in `balanceOf`.
* Extended the redeem-queue handler with the deposit handler: deploys the full sync-deposit handler
  path — deals asset to actor, approves deposit handler, refreshes rate + share price, registers
  entrance-fee recipient, calls the deposit handler with try/catch.
* Added the sync-deposit handler harness state variable and constructor parameter to the handler.
* Pre-registered the entrance-fee-recipient getter in the handler constructor alongside the existing
  exit/management/performance fee recipients.
* Updated the redeem-queue invariant suite setUp: deployed and initialized the sync-deposit handler harness,
  registered it as a deposit handler in the shares token contract, disabled the staleness guard
  (the staleness setter (set to max)) so time warps don't block deposits, set 0.5%
  entrance fee with a dedicated entrance-fee recipient.
* Added `INV-CROSS-01` (`invariant_cross_sharesFullyAccountedFor`): exact equality
  total share supply equals the sum of actor balances plus the queue's held balance.
  Rationale: the handler models the full share lifecycle; entrance fees do not mint shares, so
  every share in supply must be held by a tracked actor or sitting in the queue.

## Tests / experiments

* Compiled clean (no warnings) with `forge build --force`.
* Ran full suite at 256 runs × 128,000 calls per invariant: **7/7 pass, 0 reverts, 0 discards**.
  the deposit handler was called ~21,000 times per invariant, confirming the deposit path
  participates meaningfully in the fuzzer's call distribution.

## Hypotheses generated

* None with sufficient signal to log. The new deposit path exercised entrance-fee accounting
  at scale; no unexpected interactions with the redeem queue were observed.

## Hypotheses discarded

* None.

## AI usage

* Read source files and traced the deposit flow (the sync-deposit handler, the fee handler).
* Wrote both modified files (the redeem-queue handler, the redeem-queue invariant suite).
* Drafted this journal entry.

## Human verification

* Reviewed the deposit internal and the fee-settlement internal directly
  before designing the deposit handler — the try/catch scope and try/catch rationale are grounded
  in the actual revert paths (a zero-shares revert guard).
* Verified that fee shares are NOT minted by tracing the value-owed increment internal in the fee handler —
  confirmed the shares mint is never called on the fee recipient's behalf.
* Ran the suite end-to-end locally and inspected the call-distribution table before recording
  results as passing.
* Checked that `INV-CROSS-01` comment correctly states the no-mint property of the entrance fee.

## Public learnings

* An entrance fee that records value owed (rather than minting fee shares) simplifies share
  conservation: `totalSupply == sum(actorBalances) + queueBalance` becomes an exact equality
  invariant with no fee-recipient carve-outs needed. If the design had minted fee shares instead,
  the invariant would require iterating over fee recipients too — a broader tracking surface.
* When extending a Foundry invariant handler to cover a new protocol action, the most common
  pitfall is missing a guard that causes the action to revert silently and reduces coverage.
  For the deposit handler, refreshing both the asset rate and the last share value before calling
  the deposit ensures the action always reaches the fee and mint logic, not just the validation
  reverts.

## Blockers

* None.

## Next step

Tuesday June 30 plan:
* Introduce the adversarial actor: a caller with no shares attempting a redemption request
  (expect revert; confirm ghost state is not corrupted if the handler has no explicit guard).
* Run the extended suite with `FOUNDRY_FUZZ_RUNS=2000` and confirm no violations.
* If no failures: classify the run as clean and move to the precision/rounding analysis on Thursday.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

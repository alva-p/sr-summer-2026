# Day 21, 2026-06-30 (Tuesday)

* **Campaign day:** 21 of 83 (SR Summer 2026: 2026-06-10 to 2026-08-31)
* **Week:** Week 3 (June 29 – July 3) — Invariant testing expansion

## Objective

Tuesday cadence: extend coverage, stress-test suite, confirm clean baseline.
Week 3 Day 2 plan (from Day 20 next step):
* Introduce the adversarial actor: a caller with zero shares attempting a redemption request
  (expect revert; confirm ghost state is not corrupted when the handler has no explicit guard).
* Run the extended suite and confirm no violations.
* If clean: classify the run as the Week 3 adversarial baseline and prepare the
  precision/rounding analysis surface for Thursday.

## Time

* **Planned:** ~2h
* **Actual:** ~1h

## Area studied

Adversarial handler design and ghost-state integrity; interaction between ERC20 `[redacted]`
revert path and Foundry invariant accounting.

## Activities

* Added `handler_[redacted]Adversarial` to `[redacted].sol`: a dedicated caller
  (`makeAddr("adversary")`) with zero share balance attempts `[redacted]` with a bounded
  non-zero `sharesAmount`. The handler has no early-exit balance guard — the revert is expected
  to come from the protocol's `[redacted]`, not from a defensive skip in the handler.
  Ghost state is updated only on the unexpected-success branch; the catch block is empty by
  design, confirming that a revert from the protocol does not corrupt accounting.
* Verified `forge build --force` is clean (no warnings).
* Ran the full invariant suite: 7/7 pass, 0 reverts, 0 discards.
  `handler_[redacted]Adversarial` was called ~18,000 times per invariant.

## Tests / experiments

* Full invariant suite (256 runs × 500 depth = 128,000 calls per invariant, 7 invariants):
  **7/7 pass, 0 violations, 0 discards**.
* `handler_[redacted]Adversarial`: ~18,000 calls per invariant, zero succeeded
  (as expected — `[redacted]` always reverts for a zero-balance caller).
* Discovered: `FOUNDRY_FUZZ_RUNS` controls fuzz tests only; invariant tests use
  `FOUNDRY_INVARIANT_RUNS`. The day-20 next-step note had the wrong env var name.
  The suite ran at Foundry's default (256 runs), not 2000. The result is still a valid
  adversarial baseline at the current depth.

## Hypotheses generated

* None. The adversarial path confirmed that the protocol's share-transfer guard is the
  effective gatekeeper: there is no path for a zero-balance caller to register a request
  and corrupt queue state.

## Hypotheses discarded

* None.

## AI usage

* Read `[redacted].[redacted]` to confirm the revert path (`[redacted]`)
  and design the adversarial handler accordingly.
* Wrote `handler_[redacted]Adversarial` in `[redacted].sol`.
* Drafted this journal entry.

## Human verification

* Traced `[redacted]` in source: confirms the call reaches `[redacted]` before any
  protocol-level revert for a zero-balance caller (`_shares > 0` passes, the `[redacted]`
  is the first real gate for ownership).
* Inspected the Foundry call-distribution table: `handler_[redacted]Adversarial` appears
  with ~18,000 calls per invariant and 0 reverts (try/catch absorbs the expected ERC20 revert
  at the handler level, so Foundry counts it as a non-revert call).
* Confirmed 7/7 invariants pass before writing results.

## Public learnings

* Adversarial handler design rule: do NOT guard `handler_[redacted]Adversarial` with
  `if (balance == 0) return`. The point is to let the protocol's own access control be the
  gate. If you skip in the handler, you're not testing whether the protocol rejects the call;
  you're just skipping the test entirely.
* `FOUNDRY_FUZZ_RUNS` and `FOUNDRY_INVARIANT_RUNS` are distinct environment variables in
  Foundry. Setting the fuzz one has no effect on invariant test depth or run count.
* When wrapping a protocol call in `try/catch` inside an invariant handler, Foundry records
  the call as non-reverting (from the handler's perspective). Zero reverts in the distribution
  table is expected — it does not mean the protocol never reverted; it means every revert was
  caught and handled.

## Blockers

* None.

## Next step

Wednesday July 1 plan:
* Begin precision and rounding analysis on the redeem-queue execution path:
  `[redacted].calcValueOfSharesAmount` and `[redacted].convertValueToAssetAmount`.
* Identify the rounding direction (floor vs. ceil) and whether it consistently favors the vault.
* Draft at least one invariant candidate: e.g., user assets out are always <= gross value due
  (no value leak toward the redeemer).

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

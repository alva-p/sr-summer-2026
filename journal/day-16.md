# Day 16, 2026-06-25 (Thursday)

* **Campaign day:** 16 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 2 (June 22-26) — Shares, Valuation and Fees

## Objective

Thursday cadence: adversarial scenarios, hypothesis validation, PoCs.
Continuing from Day 15:
* Map adversarial scenarios against the five formalized invariants. For each invariant,
  identify which assumptions a malicious actor would need to violate it and whether those
  assumptions are reachable given the protocol's access control.
* Review the share-price caching in the redeem-execution function: the share price is captured
  once per batch call, not per individual request. Determine whether this creates any
  exploitable ordering assumption or price-snapshot risk.
* Explore whether setting a fee recipient to `address(0)` mid-flight (between
  the redeem-request function and the redeem-execution function) can cause fee value to be silently burned
  rather than credited to a valid address.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

Adversarial scenario analysis; share-price caching review; fee-recipient edge cases.

## Activities

* Read the async redeem-queue contract, the fee handler, the value-helpers library, and the
  relevant sections of the valuation handler in full.
* Mapped adversarial scenarios against all six formalized invariants, identifying the
  assumptions each one relies on and whether those assumptions are reachable from an
  unprivileged caller.
* Noted an access-control asymmetry between entrance/exit fee setters and management/
  performance fee setters: the exit-fee setter and the entrance-fee setter allow `recipient = address(0)`
  without validation, while the management-fee setter and the performance-fee setter enforce
  `require(_recipient != address(0))`. This is consistent with the documented "burned if
  `address(0)`" behavior, but creates a risk of silent fee burning mid-flight if the admin
  changes the recipient between the redeem-request function and the redeem-execution function.

## Tests / experiments

* Wrote a mid-flight fee-recipient test file with 3 tests:
  - the baseline fee-credit test: baseline — alice receives fee value (10e18
    value units) after execution; actor receives 990e6 net assets.
  - the mid-flight fee-burn test: admin changes
    the exit-fee recipient to `address(0)` between the redeem-request function and
    the redeem-execution function; the value-owed accumulator stays 0, alice gets 0, actor still
    receives 990e6 (same net payout as baseline).
  - the payout-symmetry test: confirms that changing the fee destination
    (credited vs. burned) does not affect the user's asset payout.
* All 3 tests pass (forge test, Solc 0.8.28).

## Hypotheses generated

* None with exploitable signal. All six invariants hold under adversarial analysis at the
  current access-control model; any violation requires admin-level access or a malicious
  registered component.

## Hypotheses discarded

* H-ORDERING: share-price caching in the redeem-execution function creates an exploitable
  ordering assumption within a batch. Discarded: category "wrong assumption". The price
  is fixed once per batch call by design; the admin controls execution timing and ordering,
  so no unprivileged actor can exploit intra-batch price snapshots.
* H-QUEUE02-BYPASS: an active request could end up with `sharesAmount == 0` while
  `controller != address(0)`. Discarded: category "documented behavior / impossible path".
  the request-removal internal deletes the entire struct atomically; no function modifies
  `sharesAmount` independently.

## AI usage

* Proposed the adversarial mapping framework (invariant, assumption needed to violate,
  access-control check, verdict).
* Analyzed the async redeem-queue contract and the fee handler and produced the mapping table.
* Identified the entrance/exit fee recipient = `address(0)` asymmetry vs. management/
  performance fee setters.
* Drafted this journal entry.

## Human verification

* All source files read directly before analysis. Invariant-to-code mapping verified
  line-by-line against the redeem-execution function, the fee-settlement internal,
  the request-removal internal, and the redeem-request function.
* The exit-fee setter and the management-fee setter signatures compared directly to confirm the
  asymmetric validation.
* The "burned if `address(0)`" comment in the fee-handler storage struct verified as the
  authoritative design intent for this behavior.

## Public learnings

* An invariant suite tells you what the protocol guarantees; adversarial mapping tells you
  what assumptions those guarantees rest on. For each invariant, the useful question is:
  "what would a caller need to be able to do to break this?" If the answer requires
  admin-level access, the invariant is robust for unprivileged attackers but still has a
  trust surface.
* Not all invariants are equally load-bearing: some (INV-QUEUE-02, INV-LASTID-01,
  INV-SUPPLY-01) hold unconditionally from the code structure alone. Others
  (INV-QUEUE-01) rely on the access-control model of the broader system. Knowing which
  is which helps focus manual review on the right attack surface.
* A fee configuration asymmetry (some setters allow `address(0)`, others forbid it) is
  worth noting even when each setter has an explicit rationale. The inconsistency means
  operators need to understand the distinction to avoid inadvertent fee burning.
* When testing "what happens if config changes mid-flight," write three tests: baseline
  (normal path), mid-flight (changed path), and symmetry (what stays the same across
  both). The symmetry test catches assumptions that are easy to miss when looking at each
  case in isolation.

## Blockers

* None.

## Next step

Friday cadence: quality review, metrics, retrospective, public contribution, plan for
next week.
* Compile Week 2 metrics and update `data/daily-metrics.csv`.
* Write the weekly retrospective (what was covered, what tests exist, open questions for
  Week 3).
* Prepare a sanitized public post about the adversarial mapping technique (or the
  mid-flight config testing pattern) as the community contribution for the week.
* Draft Week 3 plan: handlers, actors, preconditions, fuzzing depth.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). The mid-flight fee
      recipient scenario is a behavioral edge case confirmed to be documented behavior, not
      an active vulnerability.

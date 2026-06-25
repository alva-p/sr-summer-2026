# Day 16, 2026-06-25 (Thursday)

* **Campaign day:** 16 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 2 (June 22-26) — Shares, Valuation and Fees

## Objective

Thursday cadence: adversarial scenarios, hypothesis validation, PoCs.
Continuing from Day 15:
* Map adversarial scenarios against the five formalized invariants. For each invariant,
  identify which assumptions a malicious actor would need to violate it and whether those
  assumptions are reachable given the protocol's access control.
* Review the share-price caching in `[redacted]`: the share price is captured
  once per batch call, not per individual request. Determine whether this creates any
  exploitable ordering assumption or price-snapshot risk.
* Explore whether setting a fee recipient to `address(0)` mid-flight (between
  `[redacted]` and `[redacted]`) can cause fee value to be silently burned
  rather than credited to a valid address.

## Time

* **Planned:** ~2h
* **Actual:**

## Area studied

Adversarial scenario analysis; share-price caching review; fee-recipient edge cases.

## Activities

* Read `[redacted].sol` and `[redacted].sol` in full.
* Mapped adversarial scenarios against all six formalized invariants, identifying the
  assumptions each one relies on and whether those assumptions are reachable from an
  unprivileged caller.
* Noted an access-control asymmetry between entrance/exit fee setters and management/
  performance fee setters: `[redacted]` and `[redacted]` allow `recipient = address(0)`
  without validation, while `[redacted]` and `[redacted]` enforce
  `require(_recipient != address(0))`. This is consistent with the documented "burned if
  `address(0)`" behavior, but creates a risk of silent fee burning mid-flight if the admin
  changes the recipient between `[redacted]` and `[redacted]`.

## Tests / experiments

* None today (adversarial analysis session). Tests for the two edge cases carried forward
  to next session.

## Hypotheses generated

* None with exploitable signal. All six invariants hold under adversarial analysis at the
  current access-control model; any violation requires admin-level access or a malicious
  registered component.

## Hypotheses discarded

* H-ORDERING: share-price caching in `[redacted]` creates an exploitable
  ordering assumption within a batch. Discarded: category "wrong assumption". The price
  is fixed once per batch call by design; the admin controls execution timing and ordering,
  so no unprivileged actor can exploit intra-batch price snapshots.
* H-QUEUE02-BYPASS: an active request could end up with `sharesAmount == 0` while
  `controller != address(0)`. Discarded: category "documented behavior / impossible path".
  `[redacted]` deletes the entire struct atomically; no function modifies
  `sharesAmount` independently.

## AI usage

* Proposed the adversarial mapping framework (invariant, assumption needed to violate,
  access-control check, verdict).
* Analyzed `[redacted].sol` and `[redacted].sol` and produced the mapping table.
* Identified the entrance/exit fee recipient = `address(0)` asymmetry vs. management/
  performance fee setters.
* Drafted this journal entry.

## Human verification

* All source files read directly before analysis. Invariant-to-code mapping verified
  line-by-line against `[redacted]`, `[redacted]`,
  `[redacted]`, and `[redacted]`.
* The `[redacted]` and `[redacted]` signatures compared directly to confirm the
  asymmetric validation.
* The "burned if `address(0)`" comment in `[redacted]` struct verified as the
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

## Blockers

* None.

## Next step

* Part 2: deep-dive on the share-price caching in `[redacted]` (read
  `[redacted].get[redacted]()` and trace how the price is produced; confirm
  whether any external manipulation path exists at the access-control level).
* Part 3: write a unit test that exercises the fee recipient mid-flight scenario
  (`[redacted]` changed from non-zero to `address(0)` between `[redacted]` and
  `[redacted]`) and verify the "silent burn" behavior is exact and complete.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md).

# Day 32, 2026-07-13 (Monday)

* **Campaign day:** 32 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 5 (July 13-17) — debt accounting and integrations

## Objective

Open Week 5 by closing the cleanup carried over from the Day 31 week close. The Day 30 batch
value-effect / order-independence property was reasoned and recorded but never committed as a running
invariant, so the committed suite stood at 11 while the journal described 12. Today's deliverables:
re-commit that property as INV-BATCH-02 so the suite matches the recorded reasoning, then scope the
Week 5 debt surface against the actual component so the rest of the week has an honest starting point.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The batch execute value path (aggregate payout and shares burned versus the sum of each id computed
independently at the execution-time price), and a first scoping pass over the component the Week 5
roadmap points at: the credit/debt line-item tracker that records signed values written down linearly
over time.

## Activities

* Reconstructed the missing INV-BATCH-02 from the Day 30 design and committed it for real this time.
  Read the execute loop again first to be sure the independent per-id computation mirrors the protocol
  exactly: exit fee on gross shares, then value-of-shares at the share price read once before the loop,
  then value converted to the asset amount. Every id settles at the same snapshotted price and no
  per-id term feeds the next, so the aggregate must equal the independent sum and must not depend on
  the order of ids in the array.
* Added a handler action that settles an all-live batch at a share price perturbed between request and
  execution, optionally shuffling the id order, and compares the vault asset outflow and the supply
  burn against the independent per-id sum computed with the protocol's own view math. The ghost flag
  flips only on a divergence. Excluded ids whose independent payout rounds to zero at the current
  price, since those make the protocol revert the whole batch by design and would make the check
  vacuous rather than exercise it.
* Added the INV-BATCH-02 assertion to the suite and documented it alongside the others.
* Added two deterministic state-machine tests: the same multiset of requests settled in two different
  id orders pays byte-for-byte identical totals, and a batch settled after the share price moves pays
  the execution-time rate rather than the request-time rate.
* Scoped the Week 5 debt surface against the component instead of assuming the generic roadmap wording
  applies as-is. The target's debt equivalent is a linear credit/debt tracker that stores line-items
  as a signed total value written down linearly over a duration, with discrete settlement and time as
  first-class inputs. That maps cleanly onto the Week 5 checklist of debt creation/modification/repay,
  sign and scale review, and conversions, and it is a signed-arithmetic plus temporal surface rather
  than a borrow/collateral one. Recorded it as the Week 5 entry point; did not open it today.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Re-committed the batch value-effect / order-independence property as INV-BATCH-02, bringing the
  committed redeem-queue invariant suite from 11 to 12. Full suite green at the default 256 runs /
  depth 500, 128,000 calls per invariant, zero reverts. The new value-effect action fired ~9.7k times
  across the run.
* The two new deterministic state-machine tests pass, and the existing state-machine suite stays green
  (14 tests total in that file).

## Hypotheses generated

* None new. The signed-value linear write-down in the debt tracker is noted as a surface to open next,
  not a hypothesis.

## Hypotheses discarded

* None today.

## AI usage

* Reconstructed the invariant and the two deterministic tests from the Day 30 journal design, and
  cross-checked the independent per-id math against the execute loop so the ghost mirrors the protocol
  rather than an approximation of it.

## Human verification

* Re-read the execute loop myself to confirm the share price is read once before the loop and that no
  per-id term crosses into the next id, which is why order-independence must hold by construction and
  the exact-equality check is the right one rather than a rounding tolerance.
* Ran the invariant suite to green (12 invariants, zero reverts) and confirmed the value-effect action
  actually fires rather than short-circuiting, so the check is non-vacuous.
* Ran the two deterministic tests and read the failure the first time (the actor ran out of shares
  across two full batches), fixed the fixture, and reran to green rather than masking it.
* Ran `make safety-check` and read the output before marking the entry ready.

## Public learnings

* A property that lives only in a journal is not a committed test. Closing a week by diffing the
  described work against the test tree caught the gap on Day 31; the honest fix is to rebuild the
  property and run it, not to quietly edit the count. The rebuild also forces you to re-derive why the
  property holds, which is worth more than the line of code.
* When the aggregate of a loop should equal the sum of its parts, the strong check is to compute the
  parts independently with the code's own math and assert exact equality, not a tolerance. If there is
  genuinely no cross-item term and a single shared price, exact equality is correct and a tolerance
  would only hide a real drift.
* When a generic roadmap says "study the debt surface", scope the word against the actual component
  before planning the week. Here the debt surface is a signed linear write-down tracker, not a
  borrow/collateral module, so the sign, scale, conversion and temporal angles matter and the
  liquidation angle does not.

## Blockers

* None.

## Next step

Open the credit/debt line-item tracker. Read how a signed total value is written down linearly over
its duration and how discrete settlement interacts with the linear portion, then review signs and
scales at the boundaries (negative totals, zero and max durations, the write-down crossing its end)
and the conversions into the shares value asset. Record candidate surfaces before building anything.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes an invariant re-commit
      for a generic redemption-queue value property and a scoping note on a debt-tracker component
      described only in generic terms, with no target-specific finding or exploit detail.

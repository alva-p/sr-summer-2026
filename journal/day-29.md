# Day 29, 2026-07-08 (Wednesday)

* **Campaign day:** 29 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 4 (July 6-10) — redemption, queues and temporal state

## Objective

Push the redeem queue toward multi-id settlement, closing the Day 28 next step: model a batch
execute that mixes valid, already-settled, and duplicate ids in one array and check that a
partially-failing batch settles either all or none of its ids, with no id left half-settled and no
shares stranded. Until today the invariant suite only ever executed a single id per call, so the
loop's atomicity across a mixed batch was never fuzzed.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The batch-execute loop and its (absent) per-id error handling. The execute function iterates the id
array with no per-id try/catch, so any id that resolves to a zeroed request forces a zero-payout and
reverts the whole call. Two batch shapes had never been fuzzed: a duplicate id in one array, and a
mix of a live id with an already-settled one. Both should force the entire call to revert atomically
rather than settle a prefix of the batch.

## Activities

* Added a batch-execute action to the invariant handler: it builds a 1-4 id array drawn from the
  known id space and, when a poison flag is set, forces a duplicate so the must-revert case is
  reliably exercised.
* Wrote a predicate that classifies each batch as cleanly settleable (all ids live, no duplicates)
  or not, snapshots each id's shares before the call, and drives ghost accounting from the outcome:
  a success on a settleable batch decrements pending shares and marks every id settled; a revert
  asserts no shares were burned and no supply moved.
* Added INV-BATCH-01 (batch execute is atomic — all-or-none), reading a ghost flag that only a
  partial settlement would ever set: a revert that still moved shares/supply, or a success on a
  batch that could not cleanly settle.
* Added two non-vacuity counters (clean batches that settled, poison batches that reverted with no
  movement) so both branches can be shown reachable rather than assumed.
* Added three deterministic batch tests to the state-machine suite (all-valid settles every id;
  duplicate reverts and settles none; already-settled id in the batch reverts and settles none) as
  the deterministic backing for the fuzzed invariant.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Extended the redeem-queue invariant suite from ten invariants to eleven (added INV-BATCH-01) and
  from eleven handler actions to twelve (added the batch-execute action).
* Full suite green: 11 invariants pass at the default 256 runs / depth 500, 128,000 calls each, zero
  reverts across all twelve handler actions. The new batch action fired ~10.7k times.
* Added three deterministic state-machine tests for batch atomicity; all pass.

## Hypotheses generated

* None. Every poison batch reverted whole and moved no shares; every clean batch settled all its
  ids. No prefix of a failing batch ever committed.

## Hypotheses discarded

* The "a mixed batch could settle the valid ids before hitting the bad one" concern is discarded as
  documented behaviour: the execute loop settles ids in order, but a Solidity revert on a later id
  rolls back the whole transaction, including the earlier ids' burns and payouts. There is no
  partial-commit path because there is no per-id try/catch and no external call that could swallow
  the revert. The atomicity is provided by EVM revert semantics, not by explicit all-or-none logic.

## AI usage

* Drafted the batch-execute action, the settleable predicate, the atomicity invariant, and the three
  deterministic tests matching the existing suite style, and drafted this entry.
* Cross-checked that a duplicate id and an already-settled id both route to the same zero-payout
  revert, so one guard covers both poison shapes.

## Human verification

* Traced the execute loop by hand: a dead id (already deleted, or the second hit of a duplicate)
  reads a zeroed request, so the shares-to-value conversion yields zero and the zero-assets guard
  reverts. Because the revert unwinds the whole call, any earlier id's burn and payout in the same
  batch are rolled back — the settleable predicate's revert branch is therefore genuinely all-or-none.
* Confirmed the deterministic tests bite: the duplicate and already-settled cases assert both that
  the call reverts with the expected selector and that the queue's share balance and total supply are
  byte-for-byte unchanged afterward, so a partial commit would fail the assertion, not pass silently.
* Verified the two non-vacuity counters can only advance on genuinely distinct branches (a settleable
  success vs a non-settleable revert), so a green invariant with both branches reached is meaningful.
* Ran `make safety-check` and read the output before marking the entry ready.

## Public learnings

* Atomicity of a batch operation is often a property of the platform, not the code: a loop with no
  per-item error handling and no swallowed reverts is all-or-none for free, because one revert
  unwinds the whole transaction. The bug to hunt for is the opposite — a try/catch or low-level call
  inside the loop that lets a failing item be skipped while its siblings commit.
* A single-item test proves a transition; it does not prove the transition composes when several
  items with different states share one call. The valuable increment is fuzzing a mixed batch (live,
  settled, duplicate) and asserting the failing case leaves zero footprint, not just that it reverts.
* Non-vacuity for a two-branch action is worth making explicit: a predicate that splits inputs into
  "should settle" and "should revert" plus a counter on each branch turns "the invariant passed" into
  "the invariant passed and both branches were actually exercised thousands of times".

## Blockers

* None.

## Next step

Continue Week 4 by stressing the batch against ordering and value effects rather than just membership:
model a large batch of all-live ids under a share price that changes between requests and execution,
and check that the summed assets paid out and shares burned match the per-id sum regardless of batch
ordering (no cross-id interference or rounding drift accumulating across the loop).

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes generic all-or-none
      batch-atomicity invariant testing of an ERC7540-like redeem queue with no target or finding
      specifics.

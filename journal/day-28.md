# Day 28, 2026-07-07 (Tuesday)

* **Campaign day:** 28 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 4 (July 6-10) — redemption, queues and temporal state

## Objective

Model the redemption queue's temporal state as invariants, closing the Day 27 next step: a request
cannot be cancelled before its minimum duration has elapsed, and a request cannot be settled twice
(no cancel-then-execute or execute-then-execute double-spend on the single-id path). Until today the
cancel window and the settlement guards were only exercised as isolated state-machine transitions,
never under the interleaved multi-action invariant run.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The redeem queue's temporal guards over their full lifecycle: the min-duration lock that gates a
controller's own cancel, and the delete-on-settlement step that is supposed to make every request id
one-shot. Two transitions had never been fuzzed in combination with the rest of the queue: an
attempted cancel inside the lock window, and a second settlement attempt against an id that a
previous cancel or execute had already removed.

## Activities

* Added an early-cancel action to the invariant handler: it picks a live request whose
  `canCancelTime` has not yet elapsed and, as the controller, attempts the cancel call. Success is
  unreachable if the window holds; a success flips a bypass ghost that the new invariant reads.
* Added a double-settle action: it picks an id the handler has already settled and attempts to
  settle it again through either the execute or the cancel path (fuzzer-chosen), flagging both a
  success and any share movement on a revert.
* Instrumented the two existing settlement paths (successful cancel, successful execute) to record
  each settled id through a shared helper, so a second settlement of the same id from any path trips
  the double-settle detector rather than passing silently.
* Added INV-TIME-01 (cancel window cannot be bypassed) and INV-TIME-02 (a request id is settled at
  most once), each reading a ghost flag that only an actual guard failure would ever set.
* Confirmed the deterministic versions of these guards already live in the state-machine suite, so
  today's work is the fuzzed, interleaved version rather than a duplicate of the isolated checks.
* Ran the repo safety check before treating the entry as ready.

## Tests / experiments

* Extended the redeem-queue invariant suite from eight invariants to ten (added INV-TIME-01 and
  INV-TIME-02) and from nine handler actions to eleven (added early-cancel and double-settle).
* Full suite green: 10 invariants pass at the default 256 runs / depth 500, 128,000 calls each, zero
  reverts across all eleven handler actions.
* Confirmed the two new actions are non-vacuous: the early-cancel action fired ~11.5k times and the
  double-settle action ~11.5-11.8k times, both reaching their guarded branches (a live request still
  inside its lock window, and an already-settled id) rather than early-returning every call.

## Hypotheses generated

* None. The cancel window held on every in-window attempt and no id was ever settled twice, including
  under interleaved cancel and execute against the same id.

## Hypotheses discarded

* The "execute races the cancel window" concern from the Day 27 next step is discarded as documented
  behaviour: the execute call has no timing gate, so the admin can fulfil a request before its
  controller's cancel window opens. This is the intended async-fulfilment model, not a defect; the
  min-duration lock only gates the controller's own cancel (an anti-grief measure), and the
  no-double-settlement invariant confirms a fulfilled id cannot then also be cancelled for a refund.

## AI usage

* Drafted the two new handler actions, the shared settlement-marking helper, and the two temporal
  invariants matching the existing suite style, and drafted this entry.
* Cross-checked that marking settlement in both existing success paths makes the double-settle
  detector cover cancel-then-execute and execute-then-execute, not just repeated calls on one path.

## Human verification

* Traced the cancel guard by hand: the cancel call requires `block.timestamp >= canCancelTime`, and
  `canCancelTime` is set to creation time plus the min duration on the request call, so an in-window
  attempt can only revert. The early-cancel action's success branch is therefore genuinely
  unreachable and the green flag is meaningful.
* Traced both double-settlement paths: settlement deletes the request, so a re-execute hits the
  zero-shares `ZeroAssets` guard and a re-cancel hits the zeroed-controller `Unauthorized` guard.
  Both revert before touching shares, which the balance-unchanged check in the action confirms.
* Verified each new assertion bites: a cancel that escaped the lock, or a second settlement that
  moved shares, would set its ghost and fail the run, so the green result is not vacuous.
* Ran `make safety-check` and read the output before marking the entry ready.

## Public learnings

* Isolated state-machine tests prove a guard holds for one transition; they do not prove it holds
  when that transition is interleaved with every other action against shared state. The valuable
  increment over a deterministic revert test is fuzzing the same guard inside the full handler, where
  a cancel and an execute can race the same id across thousands of randomised call sequences.
* A one-shot resource (a request that must settle exactly once) is best checked not by asserting the
  happy path but by making a second settlement a fuzzer-callable action and detecting any success or
  any state movement on the expected revert. The guard you trust is the one an adversarial action
  repeatedly failed to break.
* A timing gate that looks like it protects a user can protect the opposite party: here the
  min-duration lock restricts the controller's own cancel, not the admin's fulfilment, so "can this
  be executed before the window" is a design question, not a bug, and the conservation invariants are
  what actually foreclose a double-spend.

## Blockers

* None.

## Next step

Continue Week 4 by pushing the redeem queue toward partial and batched settlement: the current suite
only ever executes a single id per call. Model a multi-id execute batch (mixed valid,
already-settled, and duplicate ids in one array) and check that a partially-failing batch settles
either all or none of its ids, with no id left half-settled and no shares stranded.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes generic temporal-state
      invariant testing of an ERC7540-like redeem queue with no target or finding specifics.

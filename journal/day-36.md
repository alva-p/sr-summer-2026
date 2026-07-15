# Day 36, 2026-07-17 (Friday)

* **Campaign day:** 36 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 5 (July 13-17) — debt accounting and integrations

## Objective

Close the remaining Week 5 angle: the fee-handler interaction in the aggregate, where fees owed are
subtracted from the total positions value before the per-share division. Check the subtraction's underflow
and revert behavior at the boundary where fees owed approach total value, and whether the dynamic-fee
settlement that sets fees-owed can be influenced or ordered within the same update to distort the per-share
result an unprivileged actor then consumes.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The aggregation that turns total positions value into a per-share value: the dynamic-fee settlement that
runs first and grows fees-owed, the re-read of total fees-owed, the subtraction of that owed from the
positions value, and the division by share supply. Also the caller restrictions on the settlement and the
path by which an unprivileged actor later consumes the resulting per-share snapshot.

## Activities

* Traced the aggregate end to end. The order is: settle dynamic fees (this mutates fees-owed), then re-read
  total fees-owed, then subtract that owed from total positions value, then divide by supply. There are two
  distinct checked subtractions on the path: one inside the settlement (positions minus the already-owed
  balance, to form the fee base) and one in the aggregate itself (positions minus total owed, to form the
  per-share base).
* Established which subtraction is the binding one. The aggregate's subtraction can only underflow if total
  owed exceeds positions value, but the freshly settled dynamic fees are bounded: each is a fraction of the
  net-of-owed base, so settling them can never by itself push total owed above positions value. That means
  the aggregate subtraction only underflows under the *same* condition that already reverted the earlier
  subtraction inside the settlement. The settlement's subtraction is the binding one.
* Characterized the failure mode. When accumulated fees-owed exceeds the current positions value, the whole
  share-value update reverts. This is a liveness stop on valuation, and it is documented in the function's
  own natspec as a revert condition, not a silent corruption.
* Confirmed the access control. The settlement entrypoint restricts its caller to the aggregator, and the
  aggregator's update entrypoints are admin-or-owner only. So an unprivileged actor cannot call, trigger,
  reorder, or front-run the settlement.
* Checked the internal ordering of the settlement: the management fee reduces the net base before the
  performance fee is computed on it, and the base already nets out every previously owed fee, including the
  entrance and exit fees settled by other users' deposits and redeems since the last update. The settlement's
  fee base and the aggregate's per-share base net different quantities, so there is no double subtraction
  between them.
* Checked the consume path. The permissionless mint reads the *stored* snapshot share value, not a freshly
  settled one, so there is no atomic path where an unprivileged actor influences the settlement inputs and
  consumes the distorted per-share result in the same transaction.
* Considered whether unprivileged deposits or redeems could drive owed above positions to grief valuation
  liveness. A deposit raises positions by the assets brought in and raises owed by only a fee fraction of
  that, so it cannot invert the inequality; the exit leg retains its fee rather than paying it out. The only
  lever that inverts it is dynamic fees accumulating through a value drawdown, which is an operator-config
  and market condition, not an unprivileged action.

## Tests / experiments

* None built. This was a reading and tracing pass whose deliverable was resolving the Week 5 fee-aggregate
  question, not a committed property. The suite was not touched and stays at its prior state.

## Hypotheses generated

* No new hypothesis with demonstrated unprivileged impact. Recorded generically the valuation-liveness
  revert (fees-owed exceeding positions value stops the share-value update) as a robustness and trust
  observation, bounded to operator-config and market-drawdown conditions rather than an untrusted-actor
  driver.

## Hypotheses discarded

* The fee-handler aggregate subtraction as an unprivileged distortion or extraction angle: closed as
  reviewed. The subtraction is a checked operation whose only failure is a documented revert; the binding
  revert sits inside the settlement, which is doubly access-controlled (only the aggregator may call it, and
  the aggregator's entrypoints are admin-or-owner). There is no unprivileged path to trigger, reorder, or
  front-run it, and no atomic influence-then-consume chain because the consumer reads a stored snapshot.
* Unprivileged deposit/redeem as a driver to invert the owed-versus-positions inequality and grief valuation
  liveness: closed. A deposit raises positions by more than it raises owed, and the exit fee is retained,
  so neither leg can push owed above positions on its own.

## AI usage

* Used AI to enumerate the callers of the settlement entrypoint, to confirm the operands and ordering of the
  two subtractions on the aggregation path, and to confirm that the permissionless consume path reads the
  stored snapshot rather than re-running the settlement.

## Human verification

* Re-read the aggregate and the settlement by hand to confirm which of the two subtractions is binding, and
  verified myself that the newly settled dynamic fees are bounded fractions of the net-of-owed base, which is
  what makes the settlement's subtraction the binding one and the aggregate's a consequence of it.
* Confirmed by hand the settlement's caller restriction to the aggregator and the admin-or-owner gate on the
  aggregator's update entrypoints, rather than trusting the enumeration, since the whole "not unprivileged"
  conclusion rests on that gate.

## Public learnings

* A checked subtraction that can revert is a documented liveness boundary, not automatically an exploit. The
  question is who can drive the operands to the boundary and what happens there: here the only outcome is the
  update reverting, and only an operator-config plus market condition reaches it.
* When a path has two subtractions of the same quantity, find the binding one by bounding the operands.
  Freshly settled fees were provably a fraction of the net base, so the later subtraction could only fail
  where the earlier one already had. The second check is redundant with the first, not an independent risk.
* A "distortion" of a derived value is only an unprivileged exploit if the actor can influence the input and
  consume the output atomically. An admin-gated push that stores a snapshot breaks that chain: the consumer
  reads yesterday's number, and cannot bend the settlement that produced it.

## Blockers

* None.

## Next step

Week 5 is closing. Move to the position-tracker aggregation that produces the total positions value the fee
settlement and per-share division both consume, focusing on trackers that read an external balance live.
Examine whether the timing gap between an unprivileged balance change on such a tracker and the operator's
next snapshot creates a consumable window, revisiting the accepted-risk donation/inflation boundary from a
value-timing angle rather than a direct-manipulation one.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes a generic reading pass over
      an aggregation that subtracts fees owed from a positions value before a per-share division, discussing
      the subtraction's revert boundary, the access control on the settlement, and the snapshot consume path
      in generic terms, with no target name, contract identifier, or target-specific finding or exploit
      detail.

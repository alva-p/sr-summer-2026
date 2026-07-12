# Day 33, 2026-07-14 (Tuesday)

* **Campaign day:** 33 of 83 (SR Summer 2026: 2026-06-09 to 2026-08-31)
* **Week:** Week 5 (July 13-17) — debt accounting and integrations

## Objective

Open the Week 5 entry point that Day 32 scoped: the signed linear credit/debt line-item tracker. Read
how a signed total value is written down linearly over its duration, how discrete settlement interacts
with the linear portion, review signs, scales and boundaries at the edges (negative totals, zero and
max durations, the write-down crossing its end), and trace how the component's value converts into the
aggregate positions value and the share price. Record candidate surfaces before building anything.

## Time

* **Planned:** ~2h
* **Actual:** ~2h

## Area studied

The linear write-down math for a signed per-item value (settled portion plus a pro-rated portion that
vests over a duration), and the path by which one position tracker's aggregate value flows into the
valuation aggregate and then into the net share value.

## Activities

* Read the whole component. It is a pure function of admin-set state plus `block.timestamp`, no external
  calls: an admin adds line-items with a signed total value, a start and a duration, and each item's
  value is a settled portion plus a pro-rated portion that vests linearly across the duration. Duration
  zero is a discrete change at the start timestamp. Values are quoted directly in the shares value
  asset, so there is no per-item unit conversion inside the component.
* Checked the rounding direction of the pro-rata write-down under both signs. The pro-rata uses signed
  integer division, which in Solidity truncates toward zero rather than toward negative infinity. For a
  positive item (a credit) that lowers the reported magnitude, which is conservative. For a negative
  item (a debt) it also lowers the magnitude, i.e. it reports *less* debt than the exact pro-rata during
  the entire vesting window. A single formula therefore rounds credits and debts in opposite economic
  directions, and the debt direction inflates the aggregate value.
* Traced that bias all the way to the output rather than stopping at the component. The tracker value is
  summed into the aggregate tracked-positions value, and the aggregate is what divides into supply to
  produce the net share value, so a debt understated during vesting inflates the share price by the same
  amount. Confirmed the direction end to end.
* Checked the width boundaries. The settled-plus-total case is computed at the item's own integer width,
  not the wide accumulator width, so an admin setting the settled and total portions near the type
  maximum with the same sign reverts on that item, which reverts the aggregate read and stalls the
  share-value update. Inputs are admin-set, so this is self-inflicted rather than an external DoS.
* Checked the negative-aggregate boundary. The aggregate is cast to unsigned and reverts if the total
  goes negative (documented behavior). The rounding bias pushes the total up, away from that revert, so
  it reinforces the inflate-NAV direction rather than tripping the revert.
* Recorded the candidate surfaces. Did not build any test or PoC today; this was the reading pass the
  Day 32 next step called for.

## Tests / experiments

* None built today. Reading and tracing pass only; the deliverable was the recorded surface list, not a
  committed property. The existing suite was not touched and stays at its Day 32 state.

## Hypotheses generated

* One candidate surface, recorded generically in the private workspace: a sign-dependent rounding
  direction in the linear write-down, where the same pro-rata truncation is conservative for a positive
  item but inflates the aggregate for a negative one, and the inflation carries through to the share
  price. Not yet a hypothesis with a demonstrated impact, since every input is admin-set; the open
  question is whether any repeatable, no-cost path makes it matter.

## Hypotheses discarded

* The item-width overflow that stalls the share-value update: noted and set aside as low, category
  documented-behavior / no external impact, because both operands are admin-set and the revert is
  self-inflicted rather than reachable by an unprivileged actor.

## AI usage

* Used AI to read the component in full and to cross-check the rounding direction under both signs and
  the integer-width boundaries against the actual code, and to trace the value path into the aggregate
  and the share price.

## Human verification

* Re-derived the truncation-toward-zero direction by hand for a positive and a negative total to confirm
  the credit and debt cases round in opposite economic directions, rather than trusting the phrase
  "rounds down", which is not well defined once the value can be negative.
* Read the aggregate path myself to confirm the tracker value is summed with the same sign and that the
  negative-aggregate cast reverts, so I could state the bias direction and the revert direction with the
  code in front of me rather than from the component in isolation.

## Public learnings

* Signed integer division truncates toward zero, not toward negative infinity, so a single pro-rata
  formula shared by positive and negative line-items rounds them in opposite economic directions. Once a
  tracked value can be negative, "rounds down" stops being well defined and you have to check the sign
  before you can say whether a rounding choice is conservative.
* A rounding bias only matters at the output, so trace it there before judging it. A per-item bias that
  looks negligible can point the same direction as the share price, and the only way to know its sign at
  the output is to follow it through the aggregate and the division, not to reason about the one line
  where it happens.
* When an arithmetic edge is only reachable by a privileged, trusted input, record it and move on rather
  than building a PoC for it. The reading pass is worth more spent finding a path an unprivileged actor
  can drive than proving an admin can stall their own fund.

## Blockers

* None.

## Next step

Decide whether the sign-dependent rounding surface has any repeatable, no-cost path that an unprivileged
actor can influence, given the inputs are admin-set. If it does not, record it as reviewed with that
reason and move to the next Week 5 angle: the external dependencies and the conversions on the paths that
consume the aggregate value, per the Week 5 checklist.

## Confidentiality check

- [x] This entry contains no active vulnerabilities, hypotheses tied to a specific in-scope
      contract, exploit sequences, PoCs, report content, or other information listed in
      [SECURITY_AND_DISCLOSURE.md](../SECURITY_AND_DISCLOSURE.md). It describes a generic reading pass
      over a signed linear write-down component in generic terms, with no target name, contract
      identifier, or target-specific finding or exploit detail.
